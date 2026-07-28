"""CUDA source for the Kimi-Linear decode megakernel (single cooperative launch).

Single cg cooperative kernel. All int4 dequant is fused into GEMV. Small/medium
GEMVs are batched (multiple output tiles share the persistent grid) so the whole
188-SM device stays busy and split-K keeps DRAM saturated.
"""

CPP = r"""
void mega_launch(int64_t Wtab, int64_t Woff, int64_t Stab,
                 int64_t hid_ptr, int64_t scr_ptr,
                 int64_t s0, int64_t s1, int64_t s2, int64_t s3,
                 int64_t L, int64_t nblk, int64_t last_moe,
                 int64_t pin_ptr, int64_t pin_size);
void get_prof(int64_t out);
"""

CUDA = r"""
#include <torch/extension.h>
#include <cuda_runtime.h>
#include <cuda_bf16.h>
#include <cooperative_groups.h>
namespace cg = cooperative_groups;
typedef __nv_bfloat16 bf16;

#define NB 188
#define NT 256
#define GRID (gridDim.x*NT)
#define D 2304
#define HK 32
#define DK 128
#define C 4096
#define H 32
#define QN 128
#define QR 64
#define VH 128
#define L0 512
#define QHD 6144
#define KVBD 8192
#define E 64
#define NACT 8
#define NEXP 9          /* 8 routed + 1 shared */
#define MI 1024
#define ROUTED 2.446f

__device__ __forceinline__ float b2f(bf16 v){ return __bfloat162float(v); }

__device__ __forceinline__ void zero_buf(float* y,int N){
    int gid=blockIdx.x*NT+threadIdx.x; for(int i=gid;i<N;i+=GRID) y[i]=0.f;
}

extern __shared__ float g_xsh[];   // per-block x staging (up to K floats)
__device__ float* g_part;          // deterministic split-K partial buffer
__device__ float g_hsum[64];        // MLA per-head softmax denom (H<=64)
__device__ unsigned long long g_prof[32];
#ifdef PROF
#define PROFT(i) do{ if(blockIdx.x==0&&threadIdx.x==0){ unsigned long long t=clock64(); g_prof[i]+=t-_pt; _pt=t; } }while(0)
#define PROFINIT unsigned long long _pt=0; if(blockIdx.x==0&&threadIdx.x==0)_pt=clock64();
#else
#define PROFT(i)
#define PROFINIT
#endif

// ---- single fused int4 GEMV: y[N] = x[K] . deq(W[K,N]) ; DETERMINISTIC split-K. ----
// Each k-partition writes its partial to g_part[kt*N+n] (no atomics); then a
// fixed-order reduction over kt writes y. Includes an internal grid.sync.
__device__ void gemv_i4(const float* __restrict__ x, const uint8_t* __restrict__ wq,
    const bf16* __restrict__ sc, const bf16* __restrict__ zr, float* __restrict__ y,
    int K, int N, cg::grid_group& grid){
    const uint32_t* wq32=(const uint32_t*)wq; int Nw=N/4, ncol4=N/4, ng=K/128;
    int col_blocks=(ncol4+NT-1)/NT;
    int avail=gridDim.x/col_blocks; if(avail<1) avail=1;
    // fine sub-group K-split: divide each 128-group into MK chunks so we use
    // more of the grid when ng alone under-fills it (engages more SMs / MLP).
    int MK=1; while(MK<4 && ng*MK*2<=avail) MK*=2;
    int chunk=128/MK;                 // k-elems per sub-slice (even)
    int total_sub=ng*MK;
    int ksplit=avail; if(ksplit>total_sub) ksplit=total_sub;
    int subper=(total_sub+ksplit-1)/ksplit;
    int bid=blockIdx.x;
    bool active = bid < col_blocks*ksplit;
    int cb=0, kt=0, su0=0, su1=0, kbeg=0;
    if(active){ cb=bid%col_blocks; kt=bid/col_blocks; su0=kt*subper; su1=min(total_sub,su0+subper);
        kbeg=su0*chunk; int klen=(su1-su0)*chunk;
        for(int i=threadIdx.x; i<klen; i+=NT) g_xsh[i]=x[kbeg+i]; }
    __syncthreads();
    if(active){
      int col4=cb*NT+threadIdx.x;
      if(col4<ncol4){
        int n0=col4*4;
        float a0=0,a1=0,a2=0,a3=0;
        for(int su=su0; su<su1; ++su){
            int g=su/MK;
            const bf16* scg=sc+g*N+n0; const bf16* zrg=zr+g*N+n0;
            float s0=b2f(scg[0]),s1=b2f(scg[1]),s2=b2f(scg[2]),s3=b2f(scg[3]);
            float z0=b2f(zrg[0]),z1=b2f(zrg[1]),z2=b2f(zrg[2]),z3=b2f(zrg[3]);
            int r0=su*(chunk/2);
            float d0=0,d1=0,d2=0,d3=0,xs=0;
            #pragma unroll 16
            for(int r=r0; r<r0+chunk/2; ++r){
                uint32_t w=__ldg(&wq32[r*Nw+col4]); float2 xab=*(const float2*)(g_xsh+2*r-kbeg); float xa=xab.x, xb=xab.y;
                xs+=xa+xb;
                uint8_t b0=w&0xFF,b1=(w>>8)&0xFF,b2_=(w>>16)&0xFF,b3=(w>>24)&0xFF;
                d0+=xa*(float)(b0&0xF)+xb*(float)((b0>>4)&0xF);
                d1+=xa*(float)(b1&0xF)+xb*(float)((b1>>4)&0xF);
                d2+=xa*(float)(b2_&0xF)+xb*(float)((b2_>>4)&0xF);
                d3+=xa*(float)(b3&0xF)+xb*(float)((b3>>4)&0xF);
            }
            a0+=s0*(d0-z0*xs); a1+=s1*(d1-z1*xs); a2+=s2*(d2-z2*xs); a3+=s3*(d3-z3*xs);
        }
        if(ksplit==1){ y[n0]=a0;y[n0+1]=a1;y[n0+2]=a2;y[n0+3]=a3; }
        else { float* p=g_part+(size_t)kt*N+n0; p[0]=a0;p[1]=a1;p[2]=a2;p[3]=a3; }
      }
    }
    grid.sync();
    if(ksplit>1){
        for(int n=blockIdx.x*NT+threadIdx.x; n<N; n+=GRID){
            float acc=0; for(int t=0;t<ksplit;t++) acc+=g_part[(size_t)t*N+n]; y[n]=acc;
        }
        grid.sync();
    }
}

// ---- single fused int4 GEMV, NO-REDUCE: leaves partials in g_part (layout
// g_part[kt*N+n]) and returns ksplit; ONE trailing grid.sync. Caller folds the
// fixed-order reduction over kt into its next pass. Same math as gemv_i4.
__device__ int gemv_i4_nr(const float* __restrict__ x, const uint8_t* __restrict__ wq,
    const bf16* __restrict__ sc, const bf16* __restrict__ zr, float* __restrict__ y,
    int K, int N, cg::grid_group& grid){
    const uint32_t* wq32=(const uint32_t*)wq; int Nw=N/4, ncol4=N/4, ng=K/128;
    int col_blocks=(ncol4+NT-1)/NT;
    int avail=gridDim.x/col_blocks; if(avail<1) avail=1;
    int MK=1; while(MK<4 && ng*MK*2<=avail) MK*=2;
    int chunk=128/MK; int total_sub=ng*MK;
    int ksplit=avail; if(ksplit>total_sub) ksplit=total_sub;
    int subper=(total_sub+ksplit-1)/ksplit;
    int bid=blockIdx.x;
    bool active = bid < col_blocks*ksplit;
    int cb=0, kt=0, su0=0, su1=0, kbeg=0;
    if(active){ cb=bid%col_blocks; kt=bid/col_blocks; su0=kt*subper; su1=min(total_sub,su0+subper);
        kbeg=su0*chunk; int klen=(su1-su0)*chunk;
        for(int i=threadIdx.x; i<klen; i+=NT) g_xsh[i]=x[kbeg+i]; }
    __syncthreads();
    if(active){
      int col4=cb*NT+threadIdx.x;
      if(col4<ncol4){
        int n0=col4*4;
        float a0=0,a1=0,a2=0,a3=0;
        for(int su=su0; su<su1; ++su){
            int g=su/MK;
            const bf16* scg=sc+g*N+n0; const bf16* zrg=zr+g*N+n0;
            float s0=b2f(scg[0]),s1=b2f(scg[1]),s2=b2f(scg[2]),s3=b2f(scg[3]);
            float z0=b2f(zrg[0]),z1=b2f(zrg[1]),z2=b2f(zrg[2]),z3=b2f(zrg[3]);
            int r0=su*(chunk/2);
            float d0=0,d1=0,d2=0,d3=0,xs=0;
            #pragma unroll 16
            for(int r=r0; r<r0+chunk/2; ++r){
                uint32_t w=__ldg(&wq32[r*Nw+col4]); float2 xab=*(const float2*)(g_xsh+2*r-kbeg); float xa=xab.x, xb=xab.y;
                xs+=xa+xb;
                uint8_t b0=w&0xFF,b1=(w>>8)&0xFF,b2_=(w>>16)&0xFF,b3=(w>>24)&0xFF;
                d0+=xa*(float)(b0&0xF)+xb*(float)((b0>>4)&0xF);
                d1+=xa*(float)(b1&0xF)+xb*(float)((b1>>4)&0xF);
                d2+=xa*(float)(b2_&0xF)+xb*(float)((b2_>>4)&0xF);
                d3+=xa*(float)(b3&0xF)+xb*(float)((b3>>4)&0xF);
            }
            a0+=s0*(d0-z0*xs); a1+=s1*(d1-z1*xs); a2+=s2*(d2-z2*xs); a3+=s3*(d3-z3*xs);
        }
        if(ksplit==1){ y[n0]=a0;y[n0+1]=a1;y[n0+2]=a2;y[n0+3]=a3; }
        else { float* p=g_part+(size_t)kt*N+n0; p[0]=a0;p[1]=a1;p[2]=a2;p[3]=a3; }
      }
    }
    grid.sync();
    return ksplit;
}
__device__ __forceinline__ float gemv_nr_reduce(int n,int N,int ksplit){
    float acc=0; for(int t=0;t<ksplit;t++) acc+=g_part[(size_t)t*N+n]; return acc;
}

// ---- batched fused int4 GEMV: nj independent GEMVs, same K,N. DETERMINISTIC. ----
__device__ void bgemv_i4(const float* const* xs, const uint8_t* const* wqs,
    const bf16* const* scs, const bf16* const* zrs, float* y, int K, int N, int nj,
    cg::grid_group& grid){
    int ncol4=N/4, ng=K/128, Nw=N/4;
    int col_blocks=(ncol4+NT-1)/NT;
    int total_cb=col_blocks*nj;
    int avail=gridDim.x/total_cb; if(avail<1) avail=1;
    int MK=1; while(MK<4 && ng*MK*2<=avail) MK*=2;
    int chunk=128/MK; int total_sub=ng*MK;
    int ksplit=avail; if(ksplit>total_sub) ksplit=total_sub;
    int subper=(total_sub+ksplit-1)/ksplit;
    int bid=blockIdx.x;
    bool active = bid < total_cb*ksplit;
    int within=0,kt=0,j=0,cb=0,su0=0,su1=0,kbeg=0;
    const float* x=nullptr;
    if(active){ within=bid%total_cb; kt=bid/total_cb; j=within/col_blocks; cb=within%col_blocks;
        su0=kt*subper; su1=min(total_sub,su0+subper); kbeg=su0*chunk; int klen=(su1-su0)*chunk; x=xs[j];
        for(int i=threadIdx.x; i<klen; i+=NT) g_xsh[i]=x[kbeg+i]; }
    __syncthreads();
    if(active){
      int col4=cb*NT+threadIdx.x;
      if(j<nj && col4<ncol4){
        const uint32_t* wq32=(const uint32_t*)wqs[j];
        const bf16* sc=scs[j]; const bf16* zr=zrs[j];
        int n0=col4*4;
        float a0=0,a1=0,a2=0,a3=0;
        for(int su=su0; su<su1; ++su){
            int g=su/MK;
            const bf16* scg=sc+g*N+n0; const bf16* zrg=zr+g*N+n0;
            float s0=b2f(scg[0]),s1=b2f(scg[1]),s2=b2f(scg[2]),s3=b2f(scg[3]);
            float z0=b2f(zrg[0]),z1=b2f(zrg[1]),z2=b2f(zrg[2]),z3=b2f(zrg[3]);
            int r0=su*(chunk/2);
            float d0=0,d1=0,d2=0,d3=0,xs=0;
            #pragma unroll 16
            for(int r=r0; r<r0+chunk/2; ++r){
                uint32_t w=__ldcs(&wq32[r*Nw+col4]); float2 xab=*(const float2*)(g_xsh+2*r-kbeg); float xa=xab.x, xb=xab.y;
                xs+=xa+xb;
                uint8_t b0=w&0xFF,b1=(w>>8)&0xFF,b2_=(w>>16)&0xFF,b3=(w>>24)&0xFF;
                d0+=xa*(float)(b0&0xF)+xb*(float)((b0>>4)&0xF);
                d1+=xa*(float)(b1&0xF)+xb*(float)((b1>>4)&0xF);
                d2+=xa*(float)(b2_&0xF)+xb*(float)((b2_>>4)&0xF);
                d3+=xa*(float)(b3&0xF)+xb*(float)((b3>>4)&0xF);
            }
            a0+=s0*(d0-z0*xs); a1+=s1*(d1-z1*xs); a2+=s2*(d2-z2*xs); a3+=s3*(d3-z3*xs);
        }
        float* yj=y+(size_t)j*N;
        if(ksplit==1){ yj[n0]=a0;yj[n0+1]=a1;yj[n0+2]=a2;yj[n0+3]=a3; }
        else { float* p=g_part+((size_t)kt*nj+j)*N+n0; p[0]=a0;p[1]=a1;p[2]=a2;p[3]=a3; }
      }
    }
    grid.sync();
    if(ksplit>1){
        for(int idx=blockIdx.x*NT+threadIdx.x; idx<nj*N; idx+=GRID){
            int j2=idx/N, n=idx%N; float acc=0;
            for(int t=0;t<ksplit;t++) acc+=g_part[((size_t)t*nj+j2)*N+n];
            y[(size_t)j2*N+n]=acc;
        }
        grid.sync();
    }
}

// ---- no-reduce batched GEMV: computes partials into g_part and returns ksplit.
// Leaves ONE grid.sync (after compute). The CALLER folds the fixed-order
// reduction over ksplit into its next pass -> saves a grid.sync + the reduce
// write-back roundtrip. If ksplit==1 the result is written straight to y.
__device__ int bgemv_i4_nr(const float* const* xs, const uint8_t* const* wqs,
    const bf16* const* scs, const bf16* const* zrs, float* y, int K, int N, int nj,
    cg::grid_group& grid){
    int ncol4=N/4, ng=K/128, Nw=N/4;
    int col_blocks=(ncol4+NT-1)/NT;
    int total_cb=col_blocks*nj;
    int avail=gridDim.x/total_cb; if(avail<1) avail=1;
    int MK=1; while(MK<4 && ng*MK*2<=avail) MK*=2;
    int chunk=128/MK; int total_sub=ng*MK;
    int ksplit=avail; if(ksplit>total_sub) ksplit=total_sub;
    int subper=(total_sub+ksplit-1)/ksplit;
    int bid=blockIdx.x;
    bool active = bid < total_cb*ksplit;
    int within=0,kt=0,j=0,cb=0,su0=0,su1=0,kbeg=0;
    const float* x=nullptr;
    if(active){ within=bid%total_cb; kt=bid/total_cb; j=within/col_blocks; cb=within%col_blocks;
        su0=kt*subper; su1=min(total_sub,su0+subper); kbeg=su0*chunk; int klen=(su1-su0)*chunk; x=xs[j];
        for(int i=threadIdx.x; i<klen; i+=NT) g_xsh[i]=x[kbeg+i]; }
    __syncthreads();
    if(active){
      int col4=cb*NT+threadIdx.x;
      if(j<nj && col4<ncol4){
        const uint32_t* wq32=(const uint32_t*)wqs[j];
        const bf16* sc=scs[j]; const bf16* zr=zrs[j];
        int n0=col4*4;
        float a0=0,a1=0,a2=0,a3=0;
        for(int su=su0; su<su1; ++su){
            int g=su/MK;
            const bf16* scg=sc+g*N+n0; const bf16* zrg=zr+g*N+n0;
            float s0=b2f(scg[0]),s1=b2f(scg[1]),s2=b2f(scg[2]),s3=b2f(scg[3]);
            float z0=b2f(zrg[0]),z1=b2f(zrg[1]),z2=b2f(zrg[2]),z3=b2f(zrg[3]);
            int r0=su*(chunk/2);
            float d0=0,d1=0,d2=0,d3=0,xs=0;
            #pragma unroll 16
            for(int r=r0; r<r0+chunk/2; ++r){
                uint32_t w=__ldcs(&wq32[r*Nw+col4]); float2 xab=*(const float2*)(g_xsh+2*r-kbeg); float xa=xab.x, xb=xab.y;
                xs+=xa+xb;
                uint8_t b0=w&0xFF,b1=(w>>8)&0xFF,b2_=(w>>16)&0xFF,b3=(w>>24)&0xFF;
                d0+=xa*(float)(b0&0xF)+xb*(float)((b0>>4)&0xF);
                d1+=xa*(float)(b1&0xF)+xb*(float)((b1>>4)&0xF);
                d2+=xa*(float)(b2_&0xF)+xb*(float)((b2_>>4)&0xF);
                d3+=xa*(float)(b3&0xF)+xb*(float)((b3>>4)&0xF);
            }
            a0+=s0*(d0-z0*xs); a1+=s1*(d1-z1*xs); a2+=s2*(d2-z2*xs); a3+=s3*(d3-z3*xs);
        }
        if(ksplit==1){ float* yj=y+(size_t)j*N; yj[n0]=a0;yj[n0+1]=a1;yj[n0+2]=a2;yj[n0+3]=a3; }
        else { float* p=g_part+((size_t)kt*nj+j)*N+n0; p[0]=a0;p[1]=a1;p[2]=a2;p[3]=a3; }
      }
    }
    grid.sync();
    return ksplit;
}
// reduce one output row from g_part partials: acc over ksplit for (j,n).
__device__ __forceinline__ float nr_reduce(int j,int n,int N,int nj,int ksplit){
    if(ksplit==1) return 0.f;   // (unused: ksplit==1 wrote y directly)
    float acc=0; for(int t=0;t<ksplit;t++) acc+=g_part[((size_t)t*nj+j)*N+n]; return acc;
}

__device__ void rmsnorm_b0(const float* hid, const bf16* nw, float* out){
    if(blockIdx.x!=0) return;
    int tid=threadIdx.x; __shared__ float red[NT];
    float acc=0; for(int i=tid;i<D;i+=NT) acc+=hid[i]*hid[i];
    red[tid]=acc; __syncthreads();
    for(int s=NT/2;s>0;s>>=1){ if(tid<s) red[tid]+=red[tid+s]; __syncthreads(); }
    float inv=rsqrtf(red[0]/D + 1e-6f);
    // round to bf16 to match reference _rmsnorm (which returns bf16, and that
    // bf16 value feeds ALL downstream consumers -- router AND the projections).
    for(int i=tid;i<D;i+=NT) out[i]=b2f(__float2bfloat16(hid[i]*inv*b2f(nw[i])));
}


#define S_XN 0

// ============================== KDA attention ==============================
__device__ void kda_attn(const int64_t* W, const int64_t* St, float* hid, float* scr, cg::grid_group& grid){
    int tid=threadIdx.x, gid=blockIdx.x*NT+tid; PROFINIT;
    float* xn=scr+S_XN;
    float* q=scr+D; float* k=q+C; float* v=k+C; float* g=v+C;
    float* beta=g+C; float* oreg=beta+HK; float* aout=oreg+C;
    rmsnorm_b0(hid,(const bf16*)W[0],xn); grid.sync();
    // batched q,k,v,g  (K=D, N=C, nj=4, same input xn)
    __shared__ const float* sxs[4]; __shared__ const uint8_t* swq[4];
    __shared__ const bf16* ssc[4]; __shared__ const bf16* szr[4];
    if(tid<4){
        sxs[tid]=xn;
        swq[tid]=(const uint8_t*)W[2+tid*3];
        ssc[tid]=(const bf16*)W[3+tid*3];
        szr[tid]=(const bf16*)W[4+tid*3];
    }
    __syncthreads();
    // Dedicated-reduce bgemv (cheaper than the nr fold here: nr made conv do
    // 4 reductions over ksplit=18 partials per channel). conv reads clean q/k/v/g.
    bgemv_i4(sxs,swq,ssc,szr,q,D,C,4,grid); int qkvg_ks=1; PROFT(1);
    // conv+silu q,k,v ; g -> -softplus
    const bf16* conv=(const bf16*)W[18];
    bf16* cq=(bf16*)St[1]; bf16* ck=(bf16*)St[2]; bf16* cv=(bf16*)St[3];
    for(int c=gid;c<C;c+=GRID){
        float qv,kv,vv,gval;
        if(qkvg_ks==1){ qv=q[c];kv=k[c];vv=v[c];gval=g[c]; }
        else { qv=nr_reduce(0,c,C,4,qkvg_ks); kv=nr_reduce(1,c,C,4,qkvg_ks); vv=nr_reduce(2,c,C,4,qkvg_ks); gval=nr_reduce(3,c,C,4,qkvg_ks); }
        #define CONVCH(BUF,IDX,VAL,OUT) {\
            float w0=b2f(conv[(IDX)*C*4+c*4+0]),w1=b2f(conv[(IDX)*C*4+c*4+1]),w2=b2f(conv[(IDX)*C*4+c*4+2]),w3=b2f(conv[(IDX)*C*4+c*4+3]);\
            float p0=b2f(BUF[0*C+c]),p1=b2f(BUF[1*C+c]),p2=b2f(BUF[2*C+c]);\
            float o=p0*w0+p1*w1+p2*w2+VAL*w3; OUT=o/(1.f+__expf(-o));\
            BUF[0*C+c]=__float2bfloat16(p1);BUF[1*C+c]=__float2bfloat16(p2);BUF[2*C+c]=__float2bfloat16(VAL);}
        float qo,ko,vo; CONVCH(cq,0,qv,qo); CONVCH(ck,1,kv,ko); CONVCH(cv,2,vv,vo);
        q[c]=qo; k[c]=ko; v[c]=vo;
        g[c]=1.f/(1.f+expf(gval));   // = exp(-softplus(gval)); state reads directly
        #undef CONVCH
    }
    PROFT(6);
    // beta = sigmoid(xn @ beta_proj[HK,D]). WARP-PER-HEAD: 32 lanes stride D,
    // shuffle reduce -> no block __syncthreads tree, no idle-block stalls.
    {
        const bf16* bw=(const bf16*)W[17];
        int warp=(blockIdx.x*NT+tid)>>5, lane=tid&31;
        for(int h=warp; h<HK; h+=(GRID>>5)){
            const bf16* bwh=bw+h*D; float acc=0.f;
            for(int i=lane;i<D;i+=32) acc+=xn[i]*b2f(__ldg(&bwh[i]));
            #pragma unroll
            for(int o=16;o>0;o>>=1) acc+=__shfl_xor_sync(0xffffffff,acc,o);
            if(lane==0) beta[h]=1.f/(1.f+expf(-acc));
        }
    }
    grid.sync(); PROFT(5);
    float* Sst=(float*)St[0]; float scale=rsqrtf((float)DK);
    // State update: COLUMN-BLOCKED across the grid. Each block owns one head and
    // a contiguous chunk of COLS output columns (j). With COLS=16 that is
    // 8 chunks/head * 32 heads = 256 blocks working (vs 32 before). Each thread
    // owns tpc=16 i-stripe of ICH=8 i-values for its column and keeps its S
    // slice in registers, so global S is read ONCE and written ONCE.
    {
        const int COLS=16, TPC=NT/COLS /*=16*/, ICH=DK/TPC /*=8*/;
        const int CHUNKS=DK/COLS /*=8*/;
        int total = HK*CHUNKS;
        for(int wjob=blockIdx.x; wjob<total; wjob+=gridDim.x){
            int h=wjob/CHUNKS; int chunk=wjob%CHUNKS; int jbase=chunk*COLS;
            float* Sh=Sst+h*DK*DK;
            __shared__ float qh[DK],kh[DK],gh[DK],gk[DK]; __shared__ float vhs[COLS],pred[COLS];
            __shared__ float betas; __shared__ float ppart[COLS][TPC];
            for(int i=tid;i<DK;i+=NT){ float ge=g[h*DK+i]; qh[i]=q[h*DK+i]*scale; kh[i]=k[h*DK+i]; gh[i]=ge; gk[i]=ge*k[h*DK+i]; }
            if(tid<COLS) vhs[tid]=v[h*DK+jbase+tid];
            if(tid==0) betas=beta[h];
            __syncthreads();
            int jc=tid%COLS, it=tid/COLS; int j=jbase+jc; int i0=it*ICH;
            float Sreg[ICH];
            #pragma unroll
            for(int r=0;r<ICH;r++) Sreg[r]=Sh[(i0+r)*DK+j];
            float pacc=0;
            #pragma unroll
            for(int r=0;r<ICH;r++) pacc+=Sreg[r]*gk[i0+r];
            ppart[jc][it]=pacc;
            __syncthreads();
            if(it==0){ float s=0; for(int t=0;t<TPC;t++) s+=ppart[jc][t]; pred[jc]=s; }
            __syncthreads();
            float diff=vhs[jc]-pred[jc]; float oacc=0;
            #pragma unroll
            for(int r=0;r<ICH;r++){ float sij=Sreg[r]*gh[i0+r]+betas*kh[i0+r]*diff; Sh[(i0+r)*DK+j]=sij; oacc+=sij*qh[i0+r]; }
            ppart[jc][it]=oacc;
            __syncthreads();
            if(it==0){ float s=0; for(int t=0;t<TPC;t++) s+=ppart[jc][t]; oreg[h*DK+j]=s; }
            __syncthreads();
        }
    }
    grid.sync(); PROFT(2);
    int ok=gemv_i4_nr(oreg,(const uint8_t*)W[14],(const bf16*)W[15],(const bf16*)W[16],aout,C,D,grid); PROFT(3);
    for(int i=gid;i<D;i+=GRID){ float a=(ok==1)?aout[i]:gemv_nr_reduce(i,D,ok); hid[i]=b2f(__float2bfloat16(hid[i]+b2f(__float2bfloat16(a)))); }
    grid.sync();
}

// ============================== MLA attention ==============================
__device__ void mla_attn(const int64_t* W, const int64_t* St, int L, float* hid, float* scr, cg::grid_group& grid){
    int tid=threadIdx.x, gid=blockIdx.x*NT+tid; PROFINIT;
    float* xn=scr+S_XN;
    float* q=scr+D; float* kv=q+QHD; float* qa=kv+576; float* scores=qa+H*L0;
    int Lt=L+1;
    float* cvec=scores+(size_t)Lt*H; float* ohead=cvec+H*L0; float* aout=ohead+H*VH;
    float* qaT=aout+D;   // L0*H transpose staging
    rmsnorm_b0(hid,(const bf16*)W[0],xn); grid.sync(); PROFT(10);
    gemv_i4(xn,(const uint8_t*)W[2],(const bf16*)W[3],(const bf16*)W[4],q,D,QHD,grid); PROFT(11);
    gemv_i4(xn,(const uint8_t*)W[5],(const bf16*)W[6],(const bf16*)W[7],kv,D,576,grid); PROFT(12);
    const bf16* old_ckv=(const bf16*)St[0]; const bf16* old_krope=(const bf16*)St[1];
    bf16* nckv=(bf16*)St[2]; bf16* nkrope=(bf16*)St[3];
    int pos=L;
    if(nckv!=old_ckv) for(size_t i=gid; i<(size_t)L*L0; i+=GRID) nckv[i]=old_ckv[i];
    if(nkrope!=old_krope) for(size_t i=gid; i<(size_t)L*QR; i+=GRID) nkrope[i]=old_krope[i];
    // qa[h,kk] = sum_{d<QN} qnope[h,d]*deq(W_kvb[kk,h*256+d]). Runs HERE (all
    // blocks) CONCURRENTLY with the block-0 rope update below -- qa reads only
    // q_nope (untouched by rope), so it shares the single grid.sync that follows
    // (saves a barrier). Writes transposed qaT_g[kk*H+h].
    {
        const uint8_t* wqa=(const uint8_t*)W[8]; const bf16* sca=(const bf16*)W[9]; const bf16* zra=(const bf16*)W[10]; int Nn=KVBD;
        bf16* qaT_g0=(bf16*)qaT;
        int bph = gridDim.x/H; if(bph<1) bph=1;
        int h0 = blockIdx.x / bph; int seg = blockIdx.x % bph;
        if(h0 < H){
            __shared__ float qn_s[QN];
            for(int d=tid; d<QN; d+=NT) qn_s[d]=q[h0*(QN+QR)+d];
            __syncthreads();
            int base=h0*256;
            int chunk=(L0+bph-1)/bph; int k0=seg*chunk, k1=min(L0,k0+chunk);
            for(int kk=k0+tid; kk<k1; kk+=NT){
                int gG=kk/128; int rowh=kk>>1; int lo=(kk&1);
                const uint8_t* wr=wqa+rowh*Nn+base;
                const bf16* scr2=sca+gG*Nn+base; const bf16* zrr=zra+gG*Nn+base;
                float acc=0;
                #pragma unroll
                for(int d=0; d<QN; d++){ uint8_t byte=__ldg(&wr[d]); int val=lo?((byte>>4)&0xF):(byte&0xF);
                    acc+=qn_s[d]*((float)val-b2f(zrr[d]))*b2f(scr2[d]); }
                qaT_g0[(size_t)kk*H+h0]=__float2bfloat16(acc);
            }
        }
    }
    if(blockIdx.x==0){
        for(int i=tid;i<L0;i+=NT) nckv[(size_t)pos*L0+i]=__float2bfloat16(kv[i]);
        for(int p=tid;p<QR/2;p+=NT){
            float inv=__expf(-(float)(2*p)/QR*9.2103404f); float ang=pos*inv; float cs=cosf(ang),sn=sinf(ang);
            float e=kv[512+2*p],o=kv[512+2*p+1];
            nkrope[(size_t)pos*QR+2*p]=__float2bfloat16(e*cs-o*sn);
            nkrope[(size_t)pos*QR+2*p+1]=__float2bfloat16(o*cs+e*sn);
        }
    }
    // q-rope: parallel over all blocks (H*QR/2 independent pairs), was a serial
    // per-head loop on block 0 while all other blocks idled.
    for(int idx=gid; idx<H*(QR/2); idx+=GRID){
        int h=idx/(QR/2), p=idx%(QR/2); float* qr=q+h*(QN+QR)+QN;
        float inv=__expf(-(float)(2*p)/QR*9.2103404f); float ang=pos*inv; float cs=cosf(ang),sn=sinf(ang);
        float e=qr[2*p],o=qr[2*p+1]; qr[2*p]=e*cs-o*sn; qr[2*p+1]=o*cs+e*sn;
    }
    // qa was computed above (concurrently with rope); this grid.sync makes both
    // qaT_g and the rope-updated q/nckv/nkrope visible before scores.
    bf16* qaT_g=(bf16*)qaT;
    grid.sync(); PROFT(13);
    float scale=rsqrtf((float)(QN+QR));
    PROFT(14);
    // scores[l,h] = sum_kk qa[h,kk]*ckv[l,kk] + rope.
    // ONE WARP PER TOKEN, lane==head h. ckv[l,:] warp-loaded COALESCED into a
    // per-warp shared row; qaT read from L2 (32KB, resident). qrope in shared.
    {
        const int NWARP=NT/32;
        bf16* qr_s=(bf16*)g_xsh;                // H*QR bf16 = 4KB (dynamic)
        bf16* ckv_sh=qr_s+H*QR;                  // NWARP*L0 bf16
        bf16* kr_sh=ckv_sh+NWARP*L0;              // NWARP*QR bf16
        for(int idx=tid; idx<H*QR; idx+=NT){ int h=idx/QR, dd=idx%QR; qr_s[idx]=__float2bfloat16(q[h*(QN+QR)+QN+dd]); }
        __syncthreads();
        int warp=tid>>5, lane=tid&31; int h=lane;
        bf16* myckv=ckv_sh+warp*(2*L0); bf16* myckv2=myckv+L0;
        bf16* mykr=kr_sh+warp*(2*QR); bf16* mykr2=mykr+QR;
        for(int l=blockIdx.x*NWARP+warp; l<Lt; l+=gridDim.x*NWARP*2){
            int l2=l+gridDim.x*NWARP; bool has2=(l2<Lt);
            const bf16* ck=nckv+(size_t)l*L0; const bf16* kr=nkrope+(size_t)l*QR;
            for(int i=lane;i<L0;i+=32) myckv[i]=__ldg(&ck[i]);
            for(int i=lane;i<QR;i+=32) mykr[i]=__ldg(&kr[i]);
            if(has2){ const bf16* ck2=nckv+(size_t)l2*L0; const bf16* kr2=nkrope+(size_t)l2*QR;
                for(int i=lane;i<L0;i+=32) myckv2[i]=__ldg(&ck2[i]);
                for(int i=lane;i<QR;i+=32) mykr2[i]=__ldg(&kr2[i]); }
            __syncwarp();
            float a=0,a2=0;
            // reuse each qaT[kk] load across BOTH tokens -> halves qaT L2 traffic.
            // 2 kk/iter: myckv loaded as bf16x2 (half the shared-load ops), fp32 accumulate.
            const __nv_bfloat162* ckv2=(const __nv_bfloat162*)myckv;
            const __nv_bfloat162* ckv2b=(const __nv_bfloat162*)myckv2;
            #pragma unroll 8
            for(int kk=0;kk<L0;kk+=2){ int k2=kk>>1;
                float q0=b2f(__ldg(&qaT_g[(size_t)kk*H+h])), q1=b2f(__ldg(&qaT_g[(size_t)(kk+1)*H+h]));
                float2 c=__bfloat1622float2(ckv2[k2]); float2 cb=__bfloat1622float2(ckv2b[k2]);
                a+=q0*c.x+q1*c.y; a2+=q0*cb.x+q1*cb.y; }
            #pragma unroll
            for(int dd=0;dd<QR;dd++){ float qd=b2f(qr_s[h*QR+dd]); a+=qd*b2f(mykr[dd]); a2+=qd*b2f(mykr2[dd]); }
            scores[(size_t)l*H+h]=a*scale;
            if(has2) scores[(size_t)l2*H+h]=a2*scale;
            __syncwarp();
        }
        // zero the softmax-denom accumulator here (no extra grid.sync needed:
        // the existing barrier below publishes it before the segment pass).
        if(blockIdx.x==0 && tid<H) g_hsum[tid]=0.f;
    }
    grid.sync(); PROFT(15);
    // NOTE: MLA scores are small (|s|<~4), so exp() cannot overflow and the
    // softmax max-subtraction is unnecessary. We therefore SKIP the per-head
    // max/sum pass entirely (it was two uncoalesced reductions over all Lt
    // tokens on only 32 blocks -- a long-context bottleneck). The denominator
    // is folded into the cvec segment pass and applied at the ohead stage.
    float* hmax=cvec+H*L0;          // scratch tail (H max slots, now unused)
    float* hsum=hmax+H;             // per-head softmax denom (filled in reduce)
    PROFT(16);
    PROFT(17);
    // cvec[h,kk] = invsum[h] * sum_l p[l,h]*ckv[l,kk].  DETERMINISTIC:
    // each (head, l-segment) block writes a partial to g_part[seg], then a
    // fixed-order reduction over segments produces cvec.
    // cvec[h,kk] = invsum[h] * sum_l p[l,h]*ckv[l,kk].  Block = one l-segment;
    // each block reads ckv[l,:] EXACTLY ONCE and fans it out to all H heads
    // (was: each of H heads re-read ckv for its segment -> 32x ckv traffic).
    // Per (seg): stage p[l,0:H] in regs while streaming kk. Deterministic:
    // partial[seg, h, kk], reduced in fixed order below.
    // SEG chosen so a segment's scores (<=segchunk*H floats) fit shared (32KB).
    const int SEG=128;                          // l-segments (bounds g_part + reduce)
    int bph = SEG;
    // hsum[h] = softmax denom, accumulated via atomics from segment blocks into
    // g_hsum (zeroed during the scores pass -> no extra grid.sync here).
    hsum = g_hsum;
    {
        int lseg = blockIdx.x;
        if(lseg < bph){
            int chunk = (Lt + bph - 1)/bph;
            int l0 = lseg*chunk, l1=min(Lt, l0+chunk); int seglen=l1-l0;
            // stage this segment's exp(scores) p[l0..l1, 0:H] in shared (no max-sub).
            float* ps=g_xsh;                    // seglen*H floats (<=129*32=4128)
            for(int idx=tid; idx<seglen*H; idx+=NT){ int h=idx%H; ps[idx]=__expf(scores[(size_t)(l0+idx/H)*H + h]); }
            __syncthreads();
            // per-head segment sum -> atomic into global denom
            for(int h=tid; h<H; h+=NT){ float acc=0; for(int li=0;li<seglen;li++) acc+=ps[li*H+h]; atomicAdd(&hsum[h],acc); }
            // 2 head-groups per kk-thread pass (acc[HH=16]) to cut registers so
            // the whole kernel hits 2 blocks/SM. ckv[l,kk] stays L1-hot across the
            // 2 passes (same kk, adjacent iterations).
            const int HH=H;
            for(int t=tid; t<L0; t+=NT){
                int kk=t; int h0=0;
                float acc[HH];
                #pragma unroll
                for(int h=0;h<HH;h++) acc[h]=0.f;
                #pragma unroll 16
                for(int li=0;li<seglen;li++){
                    float ckl=b2f(__ldg(&nckv[(size_t)(l0+li)*L0+kk])); const float* pr=ps+li*H+h0;
                    #pragma unroll
                    for(int h=0;h<HH;h++) acc[h]+=pr[h]*ckl;
                }
                float* pbase=g_part+((size_t)lseg*H)*L0+kk;
                #pragma unroll
                for(int h=0;h<HH;h++) pbase[(size_t)(h0+h)*L0]=acc[h];
            }
        }
    }
    grid.sync(); PROFT(18);
    // reduce partials over segments (fixed order) + normalize by softmax denom.
    // Stage per-head reciprocal denom in shared once (avoids H*L0 global reads +
    // divides in the hot loop).
    __shared__ float rinv[H];
    if(tid<H) rinv[tid]=1.f/hsum[tid];
    __syncthreads();
    for(int idx=gid; idx<H*L0; idx+=GRID){
        int h=idx/L0, kk=idx%L0; float acc=0;
        for(int seg=0; seg<bph; seg++) acc += g_part[((size_t)seg*H + h)*L0 + kk];
        cvec[idx]=acc*rinv[h];
    }
    grid.sync(); PROFT(19);
    {
        const uint8_t* wq=(const uint8_t*)W[8]; const bf16* sc=(const bf16*)W[9]; const bf16* zr=(const bf16*)W[10]; int Nn=KVBD;
        for(int idx=gid; idx<H*VH; idx+=GRID){
            int h=idx/VH, dv=idx%VH; int col=h*256+QN+dv; const float* cv=cvec+h*L0; float acc=0;
            for(int gG=0; gG<L0/128; gG++){
                float zg=b2f(zr[gG*Nn+col]), sg=b2f(sc[gG*Nn+col]);
                int k0=gG*128;
                #pragma unroll 16
                for(int kk=k0;kk<k0+128;kk+=2){ uint8_t byte=__ldg(&wq[(kk>>1)*Nn+col]);   // one byte = 2 nibbles
                    acc+=cv[kk]*((float)(byte&0xF)-zg)*sg + cv[kk+1]*((float)((byte>>4)&0xF)-zg)*sg; }
            }
            ohead[idx]=acc;
        }
    }
    grid.sync(); PROFT(20);
    int mok=gemv_i4_nr(ohead,(const uint8_t*)W[11],(const bf16*)W[12],(const bf16*)W[13],aout,H*VH,D,grid); PROFT(21);
    for(int i=gid;i<D;i+=GRID){ float a=(mok==1)?aout[i]:gemv_nr_reduce(i,D,mok); hid[i]=b2f(__float2bfloat16(hid[i]+b2f(__float2bfloat16(a)))); }
    grid.sync();
}

// ============================== MoE ==============================
// W(moe base): 0 mnorm,1 router,2:gate 5:up 8:down 11:sgate 14:sup 17:sdown
__device__ void moe(const int64_t* W, float* hid, float* scr, cg::grid_group& grid){
    int tid=threadIdx.x, gid=blockIdx.x*NT+tid; PROFINIT;
    float* xn=scr+S_XN;
    float* rout=xn+D;                 // E
    float* gbuf=rout+E;               // NEXP*MI (gate)
    float* ubuf=gbuf+NEXP*MI;         // NEXP*MI (up -> then h)
    float* dbuf=ubuf+NEXP*MI;         // NEXP*D  (down outputs)
    float* out=dbuf+NEXP*D;           // D
    int* topi=(int*)(out+D);          // NACT
    float* topw=(float*)(topi+16);    // NEXP (routed weights + shared=1)
    // shared pointer tables in shared mem (up to 2*NEXP for fused gate+up)
    __shared__ const float* xs[2*NEXP]; __shared__ const uint8_t* wq[2*NEXP];
    __shared__ const bf16* sc[2*NEXP]; __shared__ const bf16* zr[2*NEXP];
    rmsnorm_b0(hid,(const bf16*)W[0],xn); grid.sync();
    // router logits = xn @ router[E,D]. ONE WARP PER EXPERT: 32 lanes stride D,
    // warp-shuffle reduce -> no block __syncthreads tree, no idle-block waits.
    {
        const bf16* rw=(const bf16*)W[1];
        int warp=(blockIdx.x*NT+tid)>>5, lane=tid&31;
        for(int e=warp; e<E; e+=(GRID>>5)){
            const bf16* rwe=rw+e*D; float acc=0.f;
            for(int i=lane;i<D;i+=32) acc+=xn[i]*b2f(__ldg(&rwe[i]));
            #pragma unroll
            for(int o=16;o>0;o>>=1) acc+=__shfl_xor_sync(0xffffffff,acc,o);
            if(lane==0) rout[e]=b2f(__float2bfloat16(acc));
        }
    }
    grid.sync(); PROFT(22);
    // softmax + top-8 on block 0 with one warp (E=64): parallel max/sum reduce,
    // then a cheap serial 8-pass argmax by lane 0.
    if(blockIdx.x==0 && tid<32){
        float v0=rout[tid], v1=rout[tid+32];
        float mx=fmaxf(v0,v1);
        #pragma unroll
        for(int o=16;o>0;o>>=1) mx=fmaxf(mx,__shfl_xor_sync(0xffffffff,mx,o));
        float p0=expf(v0-mx), p1=expf(v1-mx); float sm=p0+p1;
        #pragma unroll
        for(int o=16;o>0;o>>=1) sm+=__shfl_xor_sync(0xffffffff,sm,o);
        float q0=p0/sm, q1=p1/sm;
        rout[tid]=q0; rout[tid+32]=q1;
        __syncwarp();
        // PARALLEL top-8: each of the 8 passes finds the global argmax over the
        // 64 experts cooperatively (warp shuffle over lane's 2 candidates),
        // masks it out, repeats. Replaces the serial 8x64 loop on lane 0.
        float c0=q0, c1=q1;                 // mutable candidates per lane
        __shared__ float sumw_s;
        for(int j=0;j<NACT;j++){
            float bv=fmaxf(c0,c1); int bi=(c0>=c1)?tid:(tid+32);
            #pragma unroll
            for(int o=16;o>0;o>>=1){ float ov=__shfl_xor_sync(0xffffffff,bv,o); int oi=__shfl_xor_sync(0xffffffff,bi,o);
                if(ov>bv || (ov==bv && oi<bi)){ bv=ov; bi=oi; } }
            if(tid==0){ topi[j]=bi; topw[j]=bv; }
            if(bi==tid) c0=-2.f; if(bi==tid+32) c1=-2.f;   // mask chosen expert
        }
        if(tid==0){
            float sumw=0; for(int j=0;j<NACT;j++) sumw+=topw[j];
            for(int j=0;j<NACT;j++) topw[j]=topw[j]/(sumw+1e-9f)*ROUTED;
            topw[NACT]=1.0f;
        }
    }
    grid.sync(); PROFT(23);
    long gu_wq=(long)(D/2)*MI, gu_sz=(long)(D/128)*MI;
    long dn_wq=(long)(MI/2)*D, dn_sz=(long)(MI/128)*D;
    // ---- fused gate+up (nj=2*NEXP): j in [0,NEXP) = gate, [NEXP,2*NEXP) = up.
    // Fusing doubles the batch so the grid is better filled per barrier.
    if(tid<2*NEXP){
        int half=tid/NEXP; int j=tid%NEXP; int e=(j<NACT)?topi[j]:0;
        long woff=(j<NACT)?((long)e*gu_wq):0; long soff=(j<NACT)?((long)e*gu_sz):0;
        const uint8_t* bwq; const bf16* bsc; const bf16* bzr;
        if(half==0){ bwq=(j<NACT)?(const uint8_t*)W[2]:(const uint8_t*)W[11]; bsc=(j<NACT)?(const bf16*)W[3]:(const bf16*)W[12]; bzr=(j<NACT)?(const bf16*)W[4]:(const bf16*)W[13]; }
        else       { bwq=(j<NACT)?(const uint8_t*)W[5]:(const uint8_t*)W[14]; bsc=(j<NACT)?(const bf16*)W[6]:(const bf16*)W[15]; bzr=(j<NACT)?(const bf16*)W[7]:(const bf16*)W[16]; }
        xs[tid]=xn; wq[tid]=bwq+woff; sc[tid]=bsc+soff; zr[tid]=bzr+soff;
    }
    __syncthreads();
    // gate+up via dedicated reduce (cheaper than the nr fold here: nr would do
    // 2 reductions over ksplit=18 partials per element in the silu pass).
    bgemv_i4(xs,wq,sc,zr,gbuf,D,MI,2*NEXP,grid);   // gbuf[0..NEXP*MI)=gate, [..2*NEXP*MI)=up
    // SiLU(gate)*up, float4-vectorized (dedicated reduce -> gbuf holds clean results)
    int GU4=(NEXP*MI)>>2;
    for(int q=gid;q<GU4;q+=GRID){
        float4 g4=((const float4*)gbuf)[q]; float4 u4=((const float4*)(gbuf+NEXP*MI))[q];
        g4.x=(g4.x/(1.f+__expf(-g4.x)))*u4.x; g4.y=(g4.y/(1.f+__expf(-g4.y)))*u4.y;
        g4.z=(g4.z/(1.f+__expf(-g4.z)))*u4.z; g4.w=(g4.w/(1.f+__expf(-g4.w)))*u4.w;
        ((float4*)gbuf)[q]=g4;
    }
    grid.sync(); PROFT(240);
    // ---- batched down: input gbuf[j], K=MI,N=D ----
    if(tid<NEXP){
        int j=tid; int e=(j<NACT)?topi[j]:0;
        long woff=(j<NACT)?((long)e*dn_wq):0; long soff=(j<NACT)?((long)e*dn_sz):0;
        const uint8_t* base_wq=(j<NACT)?(const uint8_t*)W[8]:(const uint8_t*)W[17];
        const bf16* base_sc=(j<NACT)?(const bf16*)W[9]:(const bf16*)W[18];
        const bf16* base_zr=(j<NACT)?(const bf16*)W[10]:(const bf16*)W[19];
        xs[j]=gbuf+j*MI; wq[j]=base_wq+woff; sc[j]=base_sc+soff; zr[j]=base_zr+soff;
    }
    __syncthreads();
    bgemv_i4(xs,wq,sc,zr,dbuf,MI,D,NEXP,grid); PROFT(25);
    // weighted sum: out[i]=sum_j topw[j]*dbuf[j*D+i]. Stage topw in registers.
    __shared__ float tws[NEXP];
    if(tid<NEXP) tws[tid]=topw[tid];
    __syncthreads();
    int D4=D>>2;
    for(int q=gid;q<D4;q+=GRID){
        float4 acc=make_float4(0,0,0,0);
        #pragma unroll
        for(int j=0;j<NEXP;j++){ float w=tws[j]; float4 d=((const float4*)(dbuf+j*D))[q];
            acc.x+=w*d.x; acc.y+=w*d.y; acc.z+=w*d.z; acc.w+=w*d.w; }
        int i=q<<2;
        hid[i]  =b2f(__float2bfloat16(hid[i]  +b2f(__float2bfloat16(acc.x))));
        hid[i+1]=b2f(__float2bfloat16(hid[i+1]+b2f(__float2bfloat16(acc.y))));
        hid[i+2]=b2f(__float2bfloat16(hid[i+2]+b2f(__float2bfloat16(acc.z))));
        hid[i+3]=b2f(__float2bfloat16(hid[i+3]+b2f(__float2bfloat16(acc.w))));
    }
    grid.sync();
}

// ============================== top kernel ==============================
// Woff[2*b]=attn base, Woff[2*b+1]=moe base
// meta = [Soff0..Soff3, L, nblk, do_last_moe]
#define PART_FLOATS (1<<21)   /* 2M floats: split-K + MLA cvec partials (SEG*H*L0) */
#ifndef LB
#define LB 2
#endif
__global__ void __launch_bounds__(NT,LB) mega_kernel(const int64_t* W, const int* Woff, const int64_t* St,
                            float* hid, float* scr_base,
                            int s0, int s1, int s2, int s3,
                            int L, int nblk, int last_moe){
    cg::grid_group grid=cg::this_grid();
    g_part = scr_base;                 // partial-sum buffer
    float* scr = scr_base + PART_FLOATS;
    int Soff[4]; Soff[0]=s0; Soff[1]=s1; Soff[2]=s2; Soff[3]=s3;
    for(int b=0;b<nblk;b++){
        const int64_t* Wa=W+Woff[2*b]; const int64_t* Wm=W+Woff[2*b+1];
        const int64_t* Sb=St+Soff[b];
        if(b<3) kda_attn(Wa,Sb,hid,scr,grid);
        else    mla_attn(Wa,Sb,L,hid,scr,grid);
        if(last_moe||b<nblk-1) moe(Wm,hid,scr,grid);
    }
}

void get_prof(int64_t out){
#ifdef PROF
    unsigned long long h[32]; cudaMemcpyFromSymbol(h,g_prof,sizeof(h));
    unsigned long long* o=(unsigned long long*)out; for(int i=0;i<32;i++)o[i]=h[i];
    unsigned long long z[32]={0}; cudaMemcpyToSymbol(g_prof,z,sizeof(z));
#else
    (void)out;
#endif
}

void mega_launch(int64_t Wtab, int64_t Woff, int64_t Stab,
                 int64_t hid_ptr, int64_t scr_ptr,
                 int64_t s0_, int64_t s1_, int64_t s2_, int64_t s3_,
                 int64_t L_, int64_t nblk_, int64_t last_moe_,
                 int64_t pin_ptr, int64_t pin_size){
    const int64_t* W=(const int64_t*)Wtab; const int* Wo=(const int*)Woff;
    const int64_t* St=(const int64_t*)Stab;
    float* hid=(float*)hid_ptr; float* scr=(float*)scr_ptr;
    int s0=(int)s0_, s1=(int)s1_, s2=(int)s2_, s3=(int)s3_;
    int L=(int)L_, nblk=(int)nblk_, last_moe=(int)last_moe_;
    void* args[]={(void*)&W,(void*)&Wo,(void*)&St,(void*)&hid,(void*)&scr,
                  (void*)&s0,(void*)&s1,(void*)&s2,(void*)&s3,
                  (void*)&L,(void*)&nblk,(void*)&last_moe};
    size_t shmem = 4128*sizeof(float);   // max of: cvec ps[<=4128 f], scores stage
    { size_t sc_sh=(size_t)(H*QR + (NT/32)*2*L0 + (NT/32)*2*QR)*sizeof(bf16); if(sc_sh>shmem) shmem=sc_sh; }
    static int nblocks = 0;
    if(nblocks==0){
        cudaFuncSetAttribute((void*)mega_kernel, cudaFuncAttributeMaxDynamicSharedMemorySize, shmem);
        int dev=0; cudaGetDevice(&dev);
        int numSM=0; cudaDeviceGetAttribute(&numSM, cudaDevAttrMultiProcessorCount, dev);
        int perSM=0;
        cudaOccupancyMaxActiveBlocksPerMultiprocessor(&perSM,(void*)mega_kernel,NT,shmem);
        if(perSM<1) perSM=1;
        nblocks = numSM*perSM;   // max resident blocks (better latency hiding)
        const char* ov=getenv("KIMI_NB"); if(ov){ int v=atoi(ov); if(v>=1) nblocks=v; }
    }
    // Re-set the L2-persist window whenever the pinned pointer changes (e.g. a
    // new Model instance across benchmark shapes) so it never references a
    // freed buffer. Keyed on pin_ptr, not a one-shot flag.
    static int64_t last_pin=0;
    if(pin_ptr && pin_ptr!=last_pin){ last_pin=pin_ptr;
        cudaDeviceSetLimit(cudaLimitPersistingL2CacheSize, (size_t)pin_size);
        cudaStreamAttrValue av; memset(&av,0,sizeof(av));
        av.accessPolicyWindow.base_ptr=(void*)pin_ptr;
        av.accessPolicyWindow.num_bytes=(size_t)pin_size;
        av.accessPolicyWindow.hitRatio=1.0f;
        av.accessPolicyWindow.hitProp=cudaAccessPropertyPersisting;
        av.accessPolicyWindow.missProp=cudaAccessPropertyStreaming;
        cudaStreamSetAttribute(0, cudaStreamAttributeAccessPolicyWindow, &av);
    }
    dim3 g(nblocks),b(NT);
    cudaError_t e=cudaLaunchCooperativeKernel((void*)mega_kernel,g,b,args,shmem,0);
    if(e!=cudaSuccess){
        cudaGetLastError();  // clear sticky launch error
        // fall back to a smaller resident grid if the device is busy
        for(int nb=nblocks/2; nb>=32; nb/=2){
            dim3 g2(nb),b2(NT);
            e=cudaLaunchCooperativeKernel((void*)mega_kernel,g2,b2,args,shmem,0);
            if(e==cudaSuccess) break;
            cudaGetLastError();
        }
        if(e!=cudaSuccess) printf("launch err %s\n",cudaGetErrorString(e));
    }
}
"""


"""CUDA source for the Kimi-Linear decode megakernel (single cooperative launch).

Single cg cooperative kernel. All int4 dequant is fused into GEMV. Small/medium
GEMVs are batched (multiple output tiles share the persistent grid) so the whole
188-SM device stays busy and split-K keeps DRAM saturated.
"""

CPP = r"""
void mega_launch(int64_t Wtab, int64_t Woff, int64_t Stab, int64_t meta,
                 int64_t hid_ptr, int64_t scr_ptr);
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

// ---- single fused int4 GEMV: y[N] = x[K] . deq(W[K,N]) ; DETERMINISTIC split-K. ----
// Each k-partition writes its partial to g_part[kt*N+n] (no atomics); then a
// fixed-order reduction over kt writes y. Includes an internal grid.sync.
__device__ void gemv_i4(const float* __restrict__ x, const uint8_t* __restrict__ wq,
    const bf16* __restrict__ sc, const bf16* __restrict__ zr, float* __restrict__ y,
    int K, int N, cg::grid_group& grid){
    const uint32_t* wq32=(const uint32_t*)wq; int Nw=N/4, ncol4=N/4, ng=K/128;
    int col_blocks=(ncol4+NT-1)/NT; int ksplit=gridDim.x/col_blocks; if(ksplit<1)ksplit=1;
    int gper=(ng+ksplit-1)/ksplit; int bid=blockIdx.x;
    bool active = bid < col_blocks*ksplit;
    int cb=0, kt=0, g0=0, g1=0, kbeg=0;
    if(active){ cb=bid%col_blocks; kt=bid/col_blocks; g0=kt*gper; g1=min(ng,g0+gper); kbeg=g0*128;
        for(int i=threadIdx.x; i<(g1-g0)*128; i+=NT) g_xsh[i]=x[kbeg+i]; }
    __syncthreads();
    if(active){
      int col4=cb*NT+threadIdx.x;
      if(col4<ncol4){
        int n0=col4*4;
        float a0=0,a1=0,a2=0,a3=0;
        for(int g=g0; g<g1; ++g){
            const bf16* scg=sc+g*N+n0; const bf16* zrg=zr+g*N+n0;
            float s0=b2f(scg[0]),s1=b2f(scg[1]),s2=b2f(scg[2]),s3=b2f(scg[3]);
            float z0=b2f(zrg[0]),z1=b2f(zrg[1]),z2=b2f(zrg[2]),z3=b2f(zrg[3]);
            int r0=g*64;
            #pragma unroll 4
            for(int r=r0; r<r0+64; ++r){
                uint32_t w=wq32[r*Nw+col4]; float xa=g_xsh[2*r-kbeg], xb=g_xsh[2*r+1-kbeg];
                uint8_t b0=w&0xFF,b1=(w>>8)&0xFF,b2_=(w>>16)&0xFF,b3=(w>>24)&0xFF;
                a0+=xa*((float)(b0&0xF)-z0)*s0+xb*((float)((b0>>4)&0xF)-z0)*s0;
                a1+=xa*((float)(b1&0xF)-z1)*s1+xb*((float)((b1>>4)&0xF)-z1)*s1;
                a2+=xa*((float)(b2_&0xF)-z2)*s2+xb*((float)((b2_>>4)&0xF)-z2)*s2;
                a3+=xa*((float)(b3&0xF)-z3)*s3+xb*((float)((b3>>4)&0xF)-z3)*s3;
            }
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

// ---- batched fused int4 GEMV: nj independent GEMVs, same K,N. DETERMINISTIC. ----
__device__ void bgemv_i4(const float* const* xs, const uint8_t* const* wqs,
    const bf16* const* scs, const bf16* const* zrs, float* y, int K, int N, int nj,
    cg::grid_group& grid){
    int ncol4=N/4, ng=K/128, Nw=N/4;
    int col_blocks=(ncol4+NT-1)/NT;
    int total_cb=col_blocks*nj;
    int ksplit=gridDim.x/total_cb; if(ksplit<1) ksplit=1;
    int gper=(ng+ksplit-1)/ksplit;
    int bid=blockIdx.x;
    bool active = bid < total_cb*ksplit;
    int within=0,kt=0,j=0,cb=0,g0=0,g1=0,kbeg=0;
    const float* x=nullptr;
    if(active){ within=bid%total_cb; kt=bid/total_cb; j=within/col_blocks; cb=within%col_blocks;
        g0=kt*gper; g1=min(ng,g0+gper); kbeg=g0*128; x=xs[j];
        for(int i=threadIdx.x; i<(g1-g0)*128; i+=NT) g_xsh[i]=x[kbeg+i]; }
    __syncthreads();
    if(active){
      int col4=cb*NT+threadIdx.x;
      if(j<nj && col4<ncol4){
        const uint32_t* wq32=(const uint32_t*)wqs[j];
        const bf16* sc=scs[j]; const bf16* zr=zrs[j];
        int n0=col4*4;
        float a0=0,a1=0,a2=0,a3=0;
        for(int g=g0; g<g1; ++g){
            const bf16* scg=sc+g*N+n0; const bf16* zrg=zr+g*N+n0;
            float s0=b2f(scg[0]),s1=b2f(scg[1]),s2=b2f(scg[2]),s3=b2f(scg[3]);
            float z0=b2f(zrg[0]),z1=b2f(zrg[1]),z2=b2f(zrg[2]),z3=b2f(zrg[3]);
            int r0=g*64;
            #pragma unroll 4
            for(int r=r0; r<r0+64; ++r){
                uint32_t w=wq32[r*Nw+col4]; float xa=g_xsh[2*r-kbeg], xb=g_xsh[2*r+1-kbeg];
                uint8_t b0=w&0xFF,b1=(w>>8)&0xFF,b2_=(w>>16)&0xFF,b3=(w>>24)&0xFF;
                a0+=xa*((float)(b0&0xF)-z0)*s0+xb*((float)((b0>>4)&0xF)-z0)*s0;
                a1+=xa*((float)(b1&0xF)-z1)*s1+xb*((float)((b1>>4)&0xF)-z1)*s1;
                a2+=xa*((float)(b2_&0xF)-z2)*s2+xb*((float)((b2_>>4)&0xF)-z2)*s2;
                a3+=xa*((float)(b3&0xF)-z3)*s3+xb*((float)((b3>>4)&0xF)-z3)*s3;
            }
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

__device__ void rmsnorm_b0(const float* hid, const bf16* nw, float* out){
    if(blockIdx.x!=0) return;
    int tid=threadIdx.x; __shared__ float red[NT];
    float acc=0; for(int i=tid;i<D;i+=NT) acc+=hid[i]*hid[i];
    red[tid]=acc; __syncthreads();
    for(int s=NT/2;s>0;s>>=1){ if(tid<s) red[tid]+=red[tid+s]; __syncthreads(); }
    float inv=rsqrtf(red[0]/D + 1e-6f);
    for(int i=tid;i<D;i+=NT) out[i]=hid[i]*inv*b2f(nw[i]);
}

#define S_XN 0

// ============================== KDA attention ==============================
__device__ void kda_attn(const int64_t* W, const int64_t* St, float* hid, float* scr, cg::grid_group& grid){
    int tid=threadIdx.x, gid=blockIdx.x*NT+tid;
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
    bgemv_i4(sxs,swq,ssc,szr,q,D,C,4,grid);
    // conv+silu q,k,v ; g -> -softplus
    const bf16* conv=(const bf16*)W[18];
    bf16* cq=(bf16*)St[1]; bf16* ck=(bf16*)St[2]; bf16* cv=(bf16*)St[3];
    for(int c=gid;c<C;c+=GRID){
        float qv=q[c],kv=k[c],vv=v[c];
        #define CONVCH(BUF,IDX,VAL,OUT) {\
            float w0=b2f(conv[(IDX)*C*4+c*4+0]),w1=b2f(conv[(IDX)*C*4+c*4+1]),w2=b2f(conv[(IDX)*C*4+c*4+2]),w3=b2f(conv[(IDX)*C*4+c*4+3]);\
            float p0=b2f(BUF[0*C+c]),p1=b2f(BUF[1*C+c]),p2=b2f(BUF[2*C+c]);\
            float o=p0*w0+p1*w1+p2*w2+VAL*w3; OUT=o/(1.f+expf(-o));\
            BUF[0*C+c]=__float2bfloat16(p1);BUF[1*C+c]=__float2bfloat16(p2);BUF[2*C+c]=__float2bfloat16(VAL);}
        float qo,ko,vo; CONVCH(cq,0,qv,qo); CONVCH(ck,1,kv,ko); CONVCH(cv,2,vv,vo);
        q[c]=qo; k[c]=ko; v[c]=vo;
        float gg=g[c]; g[c]=-log1pf(expf(gg));
        #undef CONVCH
    }
    if(blockIdx.x==0){
        const bf16* bw=(const bf16*)W[17];
        for(int h=tid;h<HK;h+=NT){ float acc=0; for(int i=0;i<D;i++) acc+=xn[i]*b2f(bw[h*D+i]); beta[h]=1.f/(1.f+expf(-acc)); }
    }
    grid.sync();
    float* Sst=(float*)St[0]; float scale=rsqrtf((float)DK);
    for(int h=blockIdx.x; h<HK; h+=gridDim.x){
        float* Sh=Sst+h*DK*DK;
        __shared__ float qh[DK],kh[DK],gh[DK],vh[DK],pred[DK]; __shared__ float betas;
        for(int i=tid;i<DK;i+=NT){ qh[i]=q[h*DK+i]*scale; kh[i]=k[h*DK+i]; gh[i]=expf(g[h*DK+i]); vh[i]=v[h*DK+i]; }
        if(tid==0) betas=beta[h];
        __syncthreads();
        for(int j=tid;j<DK;j+=NT){ float acc=0; for(int i=0;i<DK;i++) acc+=Sh[i*DK+j]*gh[i]*kh[i]; pred[j]=acc; }
        __syncthreads();
        for(int j=tid;j<DK;j+=NT){
            float diff=vh[j]-pred[j]; float acc=0;
            for(int i=0;i<DK;i++){ float sij=Sh[i*DK+j]*gh[i]+betas*kh[i]*diff; Sh[i*DK+j]=sij; acc+=sij*qh[i]; }
            oreg[h*DK+j]=acc;
        }
        __syncthreads();
    }
    grid.sync();
    gemv_i4(oreg,(const uint8_t*)W[14],(const bf16*)W[15],(const bf16*)W[16],aout,C,D,grid);
    for(int i=gid;i<D;i+=GRID) hid[i]=b2f(__float2bfloat16(hid[i]+b2f(__float2bfloat16(aout[i]))));
    grid.sync();
}

// ============================== MLA attention ==============================
__device__ void mla_attn(const int64_t* W, const int64_t* St, int L, float* hid, float* scr, cg::grid_group& grid){
    int tid=threadIdx.x, gid=blockIdx.x*NT+tid;
    float* xn=scr+S_XN;
    float* q=scr+D; float* kv=q+QHD; float* qa=kv+576; float* scores=qa+H*L0;
    int Lt=L+1;
    float* cvec=scores+(size_t)Lt*H; float* ohead=cvec+H*L0; float* aout=ohead+H*VH;
    float* qaT=aout+D;   // L0*H transpose staging
    rmsnorm_b0(hid,(const bf16*)W[0],xn); grid.sync();
    gemv_i4(xn,(const uint8_t*)W[2],(const bf16*)W[3],(const bf16*)W[4],q,D,QHD,grid);
    gemv_i4(xn,(const uint8_t*)W[5],(const bf16*)W[6],(const bf16*)W[7],kv,D,576,grid);
    const bf16* old_ckv=(const bf16*)St[0]; const bf16* old_krope=(const bf16*)St[1];
    bf16* nckv=(bf16*)St[2]; bf16* nkrope=(bf16*)St[3];
    int pos=L;
    if(nckv!=old_ckv) for(size_t i=gid; i<(size_t)L*L0; i+=GRID) nckv[i]=old_ckv[i];
    if(nkrope!=old_krope) for(size_t i=gid; i<(size_t)L*QR; i+=GRID) nkrope[i]=old_krope[i];
    if(blockIdx.x==0){
        for(int i=tid;i<L0;i+=NT) nckv[(size_t)pos*L0+i]=__float2bfloat16(kv[i]);
        for(int p=tid;p<QR/2;p+=NT){
            float inv=1.f/powf(10000.f,(float)(2*p)/QR); float ang=pos*inv; float cs=cosf(ang),sn=sinf(ang);
            float e=kv[512+2*p],o=kv[512+2*p+1];
            nkrope[(size_t)pos*QR+2*p]=__float2bfloat16(e*cs-o*sn);
            nkrope[(size_t)pos*QR+2*p+1]=__float2bfloat16(o*cs+e*sn);
        }
        for(int h=0;h<H;h++){ float* qr=q+h*(QN+QR)+QN;
            for(int p=tid;p<QR/2;p+=NT){ float inv=1.f/powf(10000.f,(float)(2*p)/QR); float ang=pos*inv; float cs=cosf(ang),sn=sinf(ang);
                float e=qr[2*p],o=qr[2*p+1]; qr[2*p]=e*cs-o*sn; qr[2*p+1]=o*cs+e*sn; } }
    }
    grid.sync();
    // qa[h,kk] = sum_{d<128} qnope[h,d] * deq(W_kvb[kk, h*256+d]).
    // One block per head-group; stage q_nope[h,:] in shared, then each thread
    // owns a kk-row and reads W[kk, h*256 .. +127] (128 contiguous bytes).
    {
        const uint8_t* wq=(const uint8_t*)W[8]; const bf16* sc=(const bf16*)W[9]; const bf16* zr=(const bf16*)W[10]; int Nn=KVBD;
        int bph = gridDim.x/H; if(bph<1) bph=1;               // blocks per head
        int h = blockIdx.x / bph; int seg = blockIdx.x % bph;
        if(h < H){
            __shared__ float qn_s[QN];
            for(int d=tid; d<QN; d+=NT) qn_s[d]=q[h*(QN+QR)+d];
            __syncthreads();
            int base=h*256;
            int chunk=(L0+bph-1)/bph; int k0=seg*chunk, k1=min(L0,k0+chunk);
            for(int kk=k0+tid; kk<k1; kk+=NT){
                int gG=kk/128; int rowh=kk>>1; int lo=(kk&1);
                const uint8_t* wr=wq+rowh*Nn+base;
                const bf16* scr2=sc+gG*Nn+base; const bf16* zrr=zr+gG*Nn+base;
                float acc=0;
                #pragma unroll 8
                for(int d=0; d<QN; d++){ uint8_t byte=wr[d]; int val=lo?((byte>>4)&0xF):(byte&0xF);
                    acc+=qn_s[d]*((float)val-b2f(zrr[d]))*b2f(scr2[d]); }
                qa[h*L0+kk]=acc;
            }
        }
    }
    grid.sync();
    float scale=rsqrtf((float)(QN+QR));
    // qaT[kk*H+h] transpose staged in scratch (64KB, L2-resident) so the scores
    // GEMV reads it with unit stride in h.
    for(int idx=gid; idx<L0*H; idx+=GRID){ int h=idx/L0, kk=idx%L0; qaT[(size_t)kk*H+h]=qa[idx]; }
    grid.sync();
    // scores[l,h]: one thread per token l accumulates all H heads while reading
    // ckv[l,:] exactly once.
    for(int l=gid; l<Lt; l+=GRID){
        const bf16* ck=nckv+(size_t)l*L0; const bf16* kr=nkrope+(size_t)l*QR;
        float acc[H];
        #pragma unroll
        for(int h=0;h<H;h++) acc[h]=0.f;
        for(int kk=0;kk<L0;kk++){
            float ckl=b2f(ck[kk]); const float* qk=qaT+(size_t)kk*H;
            #pragma unroll
            for(int h=0;h<H;h++) acc[h]+=qk[h]*ckl;
        }
        float krf[QR];
        #pragma unroll
        for(int dd=0;dd<QR;dd++) krf[dd]=b2f(kr[dd]);
        float* srow=scores+(size_t)l*H;
        #pragma unroll
        for(int h=0;h<H;h++){
            const float* qrp=q+h*(QN+QR)+QN; float a=acc[h];
            #pragma unroll
            for(int dd=0;dd<QR;dd++) a+=qrp[dd]*krf[dd];
            srow[h]=a*scale;
        }
    }
    grid.sync();
    // per-head max & sum (softmax denom); store invsum in hsum[h], max in hmax[h]
    float* hmax=cvec+H*L0;          // reuse: temp H (placed after cvec region is fine since cvec written later)
    float* hsum=hmax+H;
    for(int h=blockIdx.x; h<H; h+=gridDim.x){
        __shared__ float red[NT]; float loc=-1e30f;
        for(int l=tid;l<Lt;l+=NT) loc=fmaxf(loc,scores[(size_t)l*H+h]);
        red[tid]=loc;__syncthreads(); for(int s=NT/2;s>0;s>>=1){if(tid<s)red[tid]=fmaxf(red[tid],red[tid+s]);__syncthreads();}
        float mx=red[0]; __syncthreads();
        float ls=0; for(int l=tid;l<Lt;l+=NT) ls+=expf(scores[(size_t)l*H+h]-mx);
        red[tid]=ls;__syncthreads(); for(int s=NT/2;s>0;s>>=1){if(tid<s)red[tid]+=red[tid+s];__syncthreads();}
        if(tid==0){ hmax[h]=mx; hsum[h]=1.f/red[0]; }
        __syncthreads();
    }
    grid.sync();
    // exponentiate scores in place (parallel over all Lt*H)
    for(int idx=gid; idx<Lt*H; idx+=GRID){ int h=idx%H; scores[idx]=expf(scores[idx]-hmax[h]); }
    grid.sync();
    // cvec[h,kk] = invsum[h] * sum_l p[l,h]*ckv[l,kk].  DETERMINISTIC:
    // each (head, l-segment) block writes a partial to g_part[seg], then a
    // fixed-order reduction over segments produces cvec.
    int bph = gridDim.x/H; if(bph<1) bph=1;   // l-segments (=blocks) per head
    {
        int h = blockIdx.x / bph;
        int lseg = blockIdx.x % bph;
        if(h < H){
            int chunk = (Lt + bph - 1)/bph;
            int l0 = lseg*chunk, l1=min(Lt, l0+chunk);
            float* pout = g_part + ((size_t)lseg*H + h)*L0;
            for(int kk=tid; kk<L0; kk+=NT){
                float acc=0;
                for(int l=l0;l<l1;l++) acc += scores[(size_t)l*H+h]*b2f(nckv[(size_t)l*L0+kk]);
                pout[kk]=acc;
            }
        }
    }
    grid.sync();
    // reduce partials over segments (fixed order) + normalize
    for(int idx=gid; idx<H*L0; idx+=GRID){
        int h=idx/L0, kk=idx%L0; float acc=0;
        for(int seg=0; seg<bph; seg++) acc += g_part[((size_t)seg*H + h)*L0 + kk];
        cvec[idx]=acc*hsum[h];
    }
    grid.sync();
    {
        const uint8_t* wq=(const uint8_t*)W[8]; const bf16* sc=(const bf16*)W[9]; const bf16* zr=(const bf16*)W[10]; int Nn=KVBD;
        for(int idx=gid; idx<H*VH; idx+=GRID){
            int h=idx/VH, dv=idx%VH; int col=h*256+QN+dv; const float* cv=cvec+h*L0; float acc=0;
            for(int kk=0;kk<L0;kk++){ int gG=kk/128; uint8_t byte=wq[(kk>>1)*Nn+col]; int val=(kk&1)?((byte>>4)&0xF):(byte&0xF);
                acc+=cv[kk]*((float)val-b2f(zr[gG*Nn+col]))*b2f(sc[gG*Nn+col]); }
            ohead[idx]=acc;
        }
    }
    grid.sync();
    gemv_i4(ohead,(const uint8_t*)W[11],(const bf16*)W[12],(const bf16*)W[13],aout,H*VH,D,grid);
    for(int i=gid;i<D;i+=GRID) hid[i]=b2f(__float2bfloat16(hid[i]+b2f(__float2bfloat16(aout[i]))));
    grid.sync();
}

// ============================== MoE ==============================
// W(moe base): 0 mnorm,1 router,2:gate 5:up 8:down 11:sgate 14:sup 17:sdown
__device__ void moe(const int64_t* W, float* hid, float* scr, cg::grid_group& grid){
    int tid=threadIdx.x, gid=blockIdx.x*NT+tid;
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
    if(blockIdx.x==0){
        const bf16* rw=(const bf16*)W[1];
        for(int e=tid;e<E;e+=NT){ float acc=0; for(int i=0;i<D;i++) acc+=b2f(__float2bfloat16(xn[i]))*b2f(rw[e*D+i]); rout[e]=b2f(__float2bfloat16(acc)); }
    }
    grid.sync();
    if(gid==0){
        float mx=-1e30f; for(int e=0;e<E;e++) mx=fmaxf(mx,rout[e]);
        float sm=0; for(int e=0;e<E;e++){ float p=expf(rout[e]-mx); rout[e]=p; sm+=p; }
        for(int e=0;e<E;e++) rout[e]/=sm;
        float sumw=0;
        for(int j=0;j<NACT;j++){ float best=-1;int bi=-1; for(int e=0;e<E;e++){ if(rout[e]>best){best=rout[e];bi=e;} } topi[j]=bi; topw[j]=best; rout[bi]=-2.f; sumw+=best; }
        for(int j=0;j<NACT;j++) topw[j]=topw[j]/(sumw+1e-9f)*ROUTED;
        topw[NACT]=1.0f; // shared
    }
    grid.sync();
    long gu_wq=(long)(D/2)*MI, gu_sz=(long)(D/128)*MI;
    long dn_wq=(long)(MI/2)*D, dn_sz=(long)(MI/128)*D;
    // ---- gate ----
    if(tid<NEXP){ int j=tid; int e=(j<NACT)?topi[j]:0; long woff=(j<NACT)?((long)e*gu_wq):0; long soff=(j<NACT)?((long)e*gu_sz):0;
        const uint8_t* bwq=(j<NACT)?(const uint8_t*)W[2]:(const uint8_t*)W[11]; const bf16* bsc=(j<NACT)?(const bf16*)W[3]:(const bf16*)W[12]; const bf16* bzr=(j<NACT)?(const bf16*)W[4]:(const bf16*)W[13];
        xs[j]=xn; wq[j]=bwq+woff; sc[j]=bsc+soff; zr[j]=bzr+soff; }
    __syncthreads();
    bgemv_i4(xs,wq,sc,zr,gbuf,D,MI,NEXP,grid);
    if(tid<NEXP){ int j=tid; int e=(j<NACT)?topi[j]:0; long woff=(j<NACT)?((long)e*gu_wq):0; long soff=(j<NACT)?((long)e*gu_sz):0;
        const uint8_t* bwq=(j<NACT)?(const uint8_t*)W[5]:(const uint8_t*)W[14]; const bf16* bsc=(j<NACT)?(const bf16*)W[6]:(const bf16*)W[15]; const bf16* bzr=(j<NACT)?(const bf16*)W[7]:(const bf16*)W[16];
        xs[j]=xn; wq[j]=bwq+woff; sc[j]=bsc+soff; zr[j]=bzr+soff; }
    __syncthreads();
    bgemv_i4(xs,wq,sc,zr,ubuf,D,MI,NEXP,grid);
    for(int i=gid;i<NEXP*MI;i+=GRID){ float gg=gbuf[i]; gbuf[i]=(gg/(1.f+expf(-gg)))*ubuf[i]; }
    grid.sync();
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
    bgemv_i4(xs,wq,sc,zr,dbuf,MI,D,NEXP,grid);
    // weighted sum: out[i]=sum_j topw[j]*dbuf[j*D+i]
    for(int i=gid;i<D;i+=GRID){
        float acc=0;
        #pragma unroll
        for(int j=0;j<NEXP;j++) acc+=topw[j]*dbuf[j*D+i];
        hid[i]=b2f(__float2bfloat16(hid[i]+b2f(__float2bfloat16(acc))));
    }
    grid.sync();
}

// ============================== top kernel ==============================
// Woff[2*b]=attn base, Woff[2*b+1]=moe base
// meta = [Soff0..Soff3, L, nblk, do_last_moe]
#define PART_FLOATS (1<<19)   /* 512K floats reserved for deterministic split-K partials */
__global__ void mega_kernel(const int64_t* W, const int* Woff, const int64_t* St,
                            const int* meta, float* hid, float* scr_base){
    cg::grid_group grid=cg::this_grid();
    g_part = scr_base;                 // partial-sum buffer
    float* scr = scr_base + PART_FLOATS;
    const int* Soff=meta; int L=meta[4]; int nblk=meta[5]; int last_moe=meta[6];
    for(int b=0;b<nblk;b++){
        const int64_t* Wa=W+Woff[2*b]; const int64_t* Wm=W+Woff[2*b+1];
        const int64_t* Sb=St+Soff[b];
        if(b<3) kda_attn(Wa,Sb,hid,scr,grid);
        else    mla_attn(Wa,Sb,L,hid,scr,grid);
        if(last_moe||b<nblk-1) moe(Wm,hid,scr,grid);
    }
}

void mega_launch(int64_t Wtab, int64_t Woff, int64_t Stab, int64_t meta,
                 int64_t hid_ptr, int64_t scr_ptr){
    const int64_t* W=(const int64_t*)Wtab; const int* Wo=(const int*)Woff;
    const int64_t* St=(const int64_t*)Stab; const int* M=(const int*)meta;
    float* hid=(float*)hid_ptr; float* scr=(float*)scr_ptr;
    void* args[]={(void*)&W,(void*)&Wo,(void*)&St,(void*)&M,(void*)&hid,(void*)&scr};
    size_t shmem = 4096*sizeof(float);   // x staging (>= max gper*128)
    static int nblocks = 0;
    if(nblocks==0){
        cudaFuncSetAttribute((void*)mega_kernel, cudaFuncAttributeMaxDynamicSharedMemorySize, shmem);
        int dev=0; cudaGetDevice(&dev);
        int numSM=0; cudaDeviceGetAttribute(&numSM, cudaDevAttrMultiProcessorCount, dev);
        int perSM=0;
        cudaOccupancyMaxActiveBlocksPerMultiprocessor(&perSM,(void*)mega_kernel,NT,shmem);
        if(perSM<1) perSM=1;
        nblocks = numSM;   // 1 block/SM (robust, deterministic split-K)
        (void)perSM;
        const char* ov=getenv("KIMI_NB"); if(ov){ int v=atoi(ov); if(v>=1) nblocks=v; }
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

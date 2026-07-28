import os
os.environ.setdefault("CUDA_HOME","/tmp/cudatk")
import torch, torch.nn.functional as F, copy
from torch.utils.cpp_extension import load_inline
import reference as R

cpp = "torch::Tensor mla_attn(int64_t Wtab,int64_t Stab,torch::Tensor hid,torch::Tensor scr,int64_t L);"
src = r'''
#include <torch/extension.h>
#include <cuda_runtime.h>
#include <cuda_bf16.h>
#include <cooperative_groups.h>
namespace cg=cooperative_groups;
typedef __nv_bfloat16 bf16;
#define NB 188
#define NT 256
#define GRID (NB*NT)
#define D 2304
#define H 32
#define QN 128
#define QR 64
#define VH 128
#define L0 512
#define QH 6144   /* H*(QN+QR) */
#define KVB 8192  /* H*(QN+VH) */
__device__ __forceinline__ float b2f(bf16 v){return __bfloat162float(v);}
__device__ void gemv_i4(const float* x,const uint8_t* wq,const bf16* sc,const bf16* zr,float* y,int K,int N){
    const uint32_t* wq32=(const uint32_t*)wq; int Nw=N/4,ncol4=N/4,ng=K/128;
    int col_blocks=(ncol4+NT-1)/NT; int ksplit=NB/col_blocks; if(ksplit<1)ksplit=1;
    int gper=(ng+ksplit-1)/ksplit; int bid=blockIdx.x;
    if(bid>=col_blocks*ksplit) return; int cb=bid%col_blocks,kt=bid/col_blocks;
    int col4=cb*NT+threadIdx.x; if(col4>=ncol4)return; int n0=col4*4; int g0=kt*gper,g1=min(ng,g0+gper);
    float a0=0,a1=0,a2=0,a3=0;
    for(int g=g0;g<g1;++g){
        const bf16* scg=sc+g*N+n0; const bf16* zrg=zr+g*N+n0;
        float s0=b2f(scg[0]),s1=b2f(scg[1]),s2=b2f(scg[2]),s3=b2f(scg[3]);
        float z0=b2f(zrg[0]),z1=b2f(zrg[1]),z2=b2f(zrg[2]),z3=b2f(zrg[3]); int r0=g*64;
        #pragma unroll 4
        for(int r=r0;r<r0+64;++r){ uint32_t w=wq32[r*Nw+col4]; float xa=x[2*r],xb=x[2*r+1];
            uint8_t b0=w&0xFF,b1=(w>>8)&0xFF,b2_=(w>>16)&0xFF,b3=(w>>24)&0xFF;
            a0+=xa*((float)(b0&0xF)-z0)*s0+xb*((float)((b0>>4)&0xF)-z0)*s0;
            a1+=xa*((float)(b1&0xF)-z1)*s1+xb*((float)((b1>>4)&0xF)-z1)*s1;
            a2+=xa*((float)(b2_&0xF)-z2)*s2+xb*((float)((b2_>>4)&0xF)-z2)*s2;
            a3+=xa*((float)(b3&0xF)-z3)*s3+xb*((float)((b3>>4)&0xF)-z3)*s3; }
    }
    if(ksplit==1){y[n0]=a0;y[n0+1]=a1;y[n0+2]=a2;y[n0+3]=a3;}
    else{atomicAdd(&y[n0],a0);atomicAdd(&y[n0+1],a1);atomicAdd(&y[n0+2],a2);atomicAdd(&y[n0+3],a3);}
}
__device__ __forceinline__ void zero_buf(float* y,int N){int gid=blockIdx.x*NT+threadIdx.x;for(int i=gid;i<N;i+=GRID)y[i]=0.f;}
// W: 0 anorm,1 mnorm, 2 q(3),5 kv_a(3),8 kv_b(3),11 o(3)
// scratch: S_XN 0; S_Q D; S_KV D+QH; S_QA ...; scores ; cvec ; ohead ; attn_out
#define S_XN 0
#define S_Q D
#define S_KV (D+QH)         /* 576 */
#define S_QA (S_KV+576)     /* H*512 */
#define S_SCORE (S_QA+H*L0) /* L*H */
#define S_CVEC_BASE (S_SCORE) /* will place scores then cvec; but scores needs L*H up to 16384*32 huge! */
// scores L*H can be 16384*32=524288 floats -> fine 2MB. cvec H*512=16384. ohead H*128=4096. attn_out D.
__global__ void mla_k(const int64_t* W,const int64_t* St,float* hid,float* scr,int L){
    cg::grid_group grid=cg::this_grid();
    int tid=threadIdx.x,gid=blockIdx.x*NT+tid;
    const bf16* anorm=(const bf16*)W[0];
    if(blockIdx.x==0){
        float acc=0; for(int i=tid;i<D;i+=NT)acc+=hid[i]*hid[i];
        __shared__ float red[NT]; red[tid]=acc;__syncthreads();
        for(int s=NT/2;s>0;s>>=1){if(tid<s)red[tid]+=red[tid+s];__syncthreads();}
        float inv=rsqrtf(red[0]/D+1e-6f);
        for(int i=tid;i<D;i+=NT)scr[S_XN+i]=hid[i]*inv*b2f(anorm[i]);
    }
    grid.sync();
    zero_buf(scr+S_Q,QH); zero_buf(scr+S_KV,576); grid.sync();
    gemv_i4(scr+S_XN,(const uint8_t*)W[2],(const bf16*)W[3],(const bf16*)W[4],scr+S_Q,D,QH); grid.sync();
    gemv_i4(scr+S_XN,(const uint8_t*)W[5],(const bf16*)W[6],(const bf16*)W[7],scr+S_KV,D,576); grid.sync();
    // rope on q_rope (per head, [H,QR] located at scr[S_Q + h*(QN+QR)+QN]) and k_rope (scr[S_KV+512..576])
    // build cos/sin for pos=L (0-index new token position == old length L)
    int pos=L;
    // write new c_kv and k_rope into caches: caches are ckv[L+1,512], krope[L+1,64]. old part prefilled at [0..L). new at index L.
    bf16* ckv=(bf16*)St[0]; bf16* krope=(bf16*)St[1];
    // apply rope to k_rope then store
    if(blockIdx.x==0){
        for(int i=tid;i<L0;i+=NT) ckv[(size_t)pos*L0+i]=__float2bfloat16(scr[S_KV+i]);
        // k_rope rope
        for(int p=tid;p<QR/2;p+=NT){
            float inv=1.f/powf(10000.f,(float)(2*p)/QR);
            float ang=pos*inv; float cs=cosf(ang),sn=sinf(ang);
            float e=scr[S_KV+512+2*p], o=scr[S_KV+512+2*p+1];
            krope[(size_t)pos*QR+2*p]=__float2bfloat16(e*cs-o*sn);
            krope[(size_t)pos*QR+2*p+1]=__float2bfloat16(o*cs+e*sn);
        }
        // q_rope rope in place
        for(int h=0;h<H;h++){
            float* qr=scr+S_Q+h*(QN+QR)+QN;
            for(int p=tid;p<QR/2;p+=NT){
                float inv=1.f/powf(10000.f,(float)(2*p)/QR);
                float ang=pos*inv; float cs=cosf(ang),sn=sinf(ang);
                float e=qr[2*p],o=qr[2*p+1];
                qr[2*p]=e*cs-o*sn; qr[2*p+1]=o*cs+e*sn;
            }
        }
    }
    grid.sync();
    // qa[h,k] = sum_d q_nope[h,d]*Wk[h,k,d]; Wk from kv_b weight. kv_b: input L0=512, output KVB=8192 layout [512, H*(QN+VH)] row-major over out.
    // Wb[k, h*(QN+VH)+ (0..QN) ] = Wk ; need dequant of kv_b weight. That's expensive as full [512,8192].
    // qa[h,kk] = sum_d qnope[h,d] * Wb[kk, h*256 + d]  (d in 0..127)
    // Compute over grid: assign (h,kk) pairs. total H*512=16384.
    zero_buf(scr+S_QA,H*L0); grid.sync();
    {
        const uint8_t* wq=(const uint8_t*)W[8]; const bf16* sc=(const bf16*)W[9]; const bf16* zr=(const bf16*)W[10];
        int Kk=L0, Nn=KVB; int Nw=Nn/4; const uint32_t* wq32=(const uint32_t*)wq; int ng=Kk/128;
        // iterate over pairs (h,kk): out index. We need Wb[kk, h*256 + d] for d in 0..127.
        // Reformulate: qa[h*L0+kk] = sum_{d<128} qnope[h,d]*deq(wq[kk, h*256+d]).
        // parallel over (h,kk) = idx in [0,16384)
        for(int idx=gid; idx<H*L0; idx+=GRID){
            int h=idx/L0, kk=idx%L0;
            const float* qnope=scr+S_Q+h*(QN+QR);
            int ncol=h*256; // start column
            float acc=0;
            // rows = kk (the K dim of kv_b = 512). group g=kk/128
            int g=kk/128;
            // deq of wq[kk, col]: wq packed along K(=512) so row index kk//2, nibble. column=col (0..8191)
            // sc/zr indexed [g, col]
            for(int d=0; d<128; d++){
                int col=ncol+d;
                int row=kk; // K index
                uint8_t byte=wq[(row/2)*Nn + col];
                int val=(row&1)?((byte>>4)&0xF):(byte&0xF);
                float s=b2f(sc[g*Nn+col]), z=b2f(zr[g*Nn+col]);
                acc += qnope[d]*((float)val - z)*s;
            }
            scr[S_QA+idx]=acc;
        }
    }
    grid.sync();
    // scores[l,h] = (sum_k qa[h,k]*ckv[l,k]*scale) + (sum_d qrope[h,d]*krope[l,d]*scale)
    float scale=rsqrtf((float)(QN+QR));
    int Ltot=L+1;
    // assign each (l,h)
    for(int idx=gid; idx<Ltot*H; idx+=GRID){
        int l=idx/H, h=idx%H;
        const bf16* ck=ckv+(size_t)l*L0; const bf16* kr=krope+(size_t)l*QR;
        const float* qa=scr+S_QA+h*L0; const float* qrp=scr+S_Q+h*(QN+QR)+QN;
        float acc=0; for(int k=0;k<L0;k++) acc+=qa[k]*b2f(ck[k]);
        for(int dd=0;dd<QR;dd++) acc+=qrp[dd]*b2f(kr[dd]);
        scr[S_SCORE+(size_t)l*H+h]=acc*scale;
    }
    grid.sync();
    // softmax over l for each head, then cvec[h,k]=sum_l p[l,h]*ckv[l,k]
    // do softmax: one head per block computing max,sum over L
    int cvec_off = S_SCORE + Ltot*H;
    for(int h=blockIdx.x; h<H; h+=NB){
        __shared__ float mx, sm;
        float local=-1e30f;
        for(int l=tid;l<Ltot;l+=NT){ float v=scr[S_SCORE+(size_t)l*H+h]; local=fmaxf(local,v);}
        __shared__ float red[NT]; red[tid]=local;__syncthreads();
        for(int s=NT/2;s>0;s>>=1){if(tid<s)red[tid]=fmaxf(red[tid],red[tid+s]);__syncthreads();}
        if(tid==0)mx=red[0]; __syncthreads();
        float ls=0; for(int l=tid;l<Ltot;l+=NT){ float e=expf(scr[S_SCORE+(size_t)l*H+h]-mx); scr[S_SCORE+(size_t)l*H+h]=e; ls+=e;}
        red[tid]=ls;__syncthreads();
        for(int s=NT/2;s>0;s>>=1){if(tid<s)red[tid]+=red[tid+s];__syncthreads();}
        if(tid==0)sm=red[0];__syncthreads();
        float invsm=1.f/sm;
        // cvec[h,k]=sum_l p*ckv[l,k]
        for(int k=tid;k<L0;k+=NT){
            float acc=0; for(int l=0;l<Ltot;l++) acc+=scr[S_SCORE+(size_t)l*H+h]*b2f(ckv[(size_t)l*L0+k]);
            scr[cvec_off+h*L0+k]=acc*invsm;
        }
    }
    grid.sync();
    // ohead[h,dv]=sum_k cvec[h,k]*Wv[h,k,dv]; Wv=Wb[k, h*256+QN+dv]
    int ohead_off = cvec_off + H*L0;
    {
        const uint8_t* wq=(const uint8_t*)W[8]; const bf16* sc=(const bf16*)W[9]; const bf16* zr=(const bf16*)W[10];
        int Nn=KVB;
        for(int idx=gid; idx<H*VH; idx+=GRID){
            int h=idx/VH, dv=idx%VH; int col=h*256+QN+dv;
            const float* cvec=scr+cvec_off+h*L0;
            float acc=0;
            for(int kk=0;kk<L0;kk++){ int g=kk/128; uint8_t byte=wq[(kk/2)*Nn+col]; int val=(kk&1)?((byte>>4)&0xF):(byte&0xF);
                float s=b2f(sc[g*Nn+col]),z=b2f(zr[g*Nn+col]); acc+=cvec[kk]*((float)val-z)*s; }
            scr[ohead_off+idx]=acc;
        }
    }
    grid.sync();
    int attnout_off = ohead_off + H*VH;
    zero_buf(scr+attnout_off,D); grid.sync();
    gemv_i4(scr+ohead_off,(const uint8_t*)W[11],(const bf16*)W[12],(const bf16*)W[13],scr+attnout_off,H*VH,D); grid.sync();
    for(int i=gid;i<D;i+=GRID)hid[i]=scr[attnout_off+i];
}
torch::Tensor mla_attn(int64_t Wtab,int64_t Stab,torch::Tensor hid,torch::Tensor scr,int64_t L){
    const int64_t* W=(const int64_t*)Wtab;const int64_t* St=(const int64_t*)Stab;
    float* h=hid.data_ptr<float>();float* s=scr.data_ptr<float>();int Li=L;
    void* args[]={(void*)&W,(void*)&St,(void*)&h,(void*)&s,(void*)&Li};
    dim3 g(NB),b(NT);cudaLaunchCooperativeKernel((void*)mla_k,g,b,args,0,0);
    cudaError_t e=cudaDeviceSynchronize();if(e!=cudaSuccess)printf("err %s\n",cudaGetErrorString(e));
    return hid;
}
'''
mod=load_inline(name="dev_mla",cpp_sources=cpp,cuda_sources=src,functions=["mla_attn"],extra_cuda_cflags=["-O3","-arch=sm_120"],verbose=False)

torch.manual_seed(0)
cfg=R.build_config({"n_experts":64})
m=R.Model(cfg).cuda().eval()
ctx=2048
st=R.init_state(cfg,ctx,0)
h=R.init_token(cfg,0)
blk=m.blocks[3]; mla=blk.attn
st_t=copy.deepcopy(st[3])
xn=R._rmsnorm(h,blk.attn_norm)
with torch.no_grad():
    o_t=mla.step(xn,st_t)  # updates st_t caches to L+1
# allocate new caches sized L+1
L=ctx
ckv_new=torch.zeros(L+1,512,dtype=torch.bfloat16,device='cuda'); ckv_new[:L]=st[3]["c_kv"]
krope_new=torch.zeros(L+1,64,dtype=torch.bfloat16,device='cuda'); krope_new[:L]=st[3]["k_rope"]
def qlp(ql): return [ql.w_q.data_ptr(),ql.scales.data_ptr(),ql.zeros.data_ptr()]
W=[blk.attn_norm.data_ptr(),blk.moe_norm.data_ptr()]
W+=qlp(mla.q_proj)+qlp(mla.kv_a)+qlp(mla.kv_b)+qlp(mla.o_proj)
Wt=torch.tensor(W,dtype=torch.int64,device='cuda')
St=torch.tensor([ckv_new.data_ptr(),krope_new.data_ptr()],dtype=torch.int64,device='cuda')
hid=h.float().clone()
scr=torch.zeros(4_000_000,device='cuda')
out=mod.mla_attn(Wt.data_ptr(),St.data_ptr(),hid,scr,L)
torch.cuda.synchronize()
print("mla out cos",F.cosine_similarity(o_t.float(),out.float(),dim=0).item())
print("ckv cos",F.cosine_similarity(st_t["c_kv"].float().flatten(),ckv_new.float().flatten(),dim=0).item())
print("krope cos",F.cosine_similarity(st_t["k_rope"].float().flatten(),krope_new.float().flatten(),dim=0).item())

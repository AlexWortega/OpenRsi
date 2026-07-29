import os,sys,time,random,statistics,torch
os.environ.setdefault("CUDA_HOME","/tmp/cudatk")
from torch.utils.cpp_extension import load_inline
import reference, solution, megakernel_src as mk
def LV(n,lb,rreg): return load_inline(name=n,cpp_sources=mk.CPP,cuda_sources=mk.CUDA,functions=["mega_launch"],extra_cuda_cflags=["-O3","-arch=sm_120","--use_fast_math","-DLB="+str(lb),"-maxrregcount="+str(rreg)],verbose=False)
A=LV("qA",6,40); B=LV("qB",int(sys.argv[1]),int(sys.argv[2]))
cfg=reference.build_config({"n_experts":64}); ref=reference.Model(cfg).cuda().eval()
_o=solution.Model._build_weights
def pb(s):
    _o(s)
    if hasattr(s,'_fm'): s._mod=s._fm
solution.Model._build_weights=pb
def mkm(m):
    x=solution.Model(cfg).cuda().eval(); x.load_state_dict(ref.state_dict()); x._fm=m; return x
mA=mkm(A); mB=mkm(B)
def one(m,ctx,steps=30):
    h=reference.init_token(cfg,7); st=reference.init_state(cfg,ctx,7)
    with torch.no_grad():
        for _ in range(3): h,st=m.step(h,st)
    torch.cuda.synchronize(); t0=time.perf_counter()
    with torch.no_grad():
        for _ in range(steps): h,st=m.step(h,st)
    torch.cuda.synchronize(); return (time.perf_counter()-t0)/steps*1e3
for ctx in (2048,16384):
    for _ in range(3): one(mA,ctx); one(mB,ctx)
    R=[]
    for _ in range(25):
        if random.random()<0.5: a=one(mA,ctx); b=one(mB,ctx)
        else: b=one(mB,ctx); a=one(mA,ctx)
        R.append(a/b)
    print(f"ctx={ctx} med(base_LB2R128 / cand_LB{sys.argv[1]}R{sys.argv[2]})={statistics.median(R):.4f}")

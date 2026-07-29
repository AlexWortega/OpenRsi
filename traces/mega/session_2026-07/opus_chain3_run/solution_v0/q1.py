import os,sys,time,random,statistics,torch,importlib.util
os.environ.setdefault("CUDA_HOME","/tmp/cudatk")
from torch.utils.cpp_extension import load_inline
import reference, solution, megakernel_src as base_mk
def LV(n,mk): return load_inline(name=n,cpp_sources=mk.CPP,cuda_sources=mk.CUDA,functions=["mega_launch"],extra_cuda_cflags=["-O3","-arch=sm_120","--use_fast_math","-DLB=2","-maxrregcount=128"],verbose=False)
A=LV("qa",base_mk)
spec=importlib.util.spec_from_file_location("cm",sys.argv[1]); cm=importlib.util.module_from_spec(spec); spec.loader.exec_module(cm)
B=LV("qb",cm)
cfg=reference.build_config({"n_experts":64}); ref=reference.Model(cfg).cuda().eval()
_o=solution.Model._build_weights
def pb(s):
    _o(s)
    if hasattr(s,'_fm'): s._mod=s._fm
solution.Model._build_weights=pb
def mk(m):
    x=solution.Model(cfg).cuda().eval(); x.load_state_dict(ref.state_dict()); x._fm=m; return x
mA=mk(A); mB=mk(B)
def one(m,ctx,st_seed=7,steps=30):
    h=reference.init_token(cfg,st_seed); st=reference.init_state(cfg,ctx,st_seed)
    with torch.no_grad():
        for _ in range(3): h,st=m.step(h,st)
    torch.cuda.synchronize(); t0=time.perf_counter()
    with torch.no_grad():
        for _ in range(steps): h,st=m.step(h,st)
    torch.cuda.synchronize(); return (time.perf_counter()-t0)/steps*1e3
ctx=16384
for _ in range(3): one(mA,ctx); one(mB,ctx)
R=[]
for _ in range(30):
    if random.random()<0.5: a=one(mA,ctx); b=one(mB,ctx)
    else: b=one(mB,ctx); a=one(mA,ctx)
    R.append(a/b)
print(f"ctx16384 med_ratio(A/B)={statistics.median(R):.4f}")
import torch.nn.functional as F
h=reference.init_token(cfg,2); sr=reference.init_state(cfg,ctx,2); ss=reference.init_state(cfg,ctx,2)
with torch.no_grad(): orf,_=ref.step(h.clone(),sr); osf,_=mB.step(h.clone(),ss)
print("cos",F.cosine_similarity(orf.float(),osf.float(),dim=0).item())

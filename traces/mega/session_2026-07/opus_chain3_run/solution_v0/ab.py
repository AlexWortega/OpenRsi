# A/B tester: compiles baseline megakernel_src.py and a candidate file, interleaves timing.
import os, sys, time, torch, importlib.util
os.environ.setdefault("CUDA_HOME","/tmp/cudatk")
from torch.utils.cpp_extension import load_inline
import reference, solution

import os as _os
def load_variant(name, src_module, lb=None, rreg=None):
    lb = lb or _os.environ.get("AB_LB","2")
    rreg = rreg or _os.environ.get("AB_RREG","128")
    return load_inline(name=name, cpp_sources=src_module.CPP, cuda_sources=src_module.CUDA,
        functions=["mega_launch"],
        extra_cuda_cflags=["-O3","-arch=sm_120","--use_fast_math","-DLB="+str(lb),"-maxrregcount="+str(rreg)],
        verbose=False)

def build_model(mod):
    cfg = reference.build_config({"n_experts":64})
    ref = reference.Model(cfg).cuda().eval()
    m = solution.Model(cfg).cuda().eval()
    m.load_state_dict(ref.state_dict(), strict=True)
    m._MOD_OVERRIDE = mod
    # patch: force this model to use given module
    orig_get = solution._get_module
    m.cfg  # noqa
    return m, cfg, ref

import megakernel_src as base_mk
base_mod = load_variant("kimi_base_ab", base_mk, lb=2, rreg=128)

# candidate
cand_path = sys.argv[1] if len(sys.argv)>1 else None
if cand_path:
    spec = importlib.util.spec_from_file_location("cand_mk", cand_path)
    cand_mk = importlib.util.module_from_spec(spec); spec.loader.exec_module(cand_mk)
    cand_mod = load_variant("kimi_cand_ab", cand_mk, lb=_os.environ.get("CAND_LB","2"), rreg=_os.environ.get("CAND_RREG","128"))
else:
    cand_mod = load_variant("kimi_cand_ab2", base_mk, lb=_os.environ.get("CAND_LB","2"), rreg=_os.environ.get("CAND_RREG","128"))

cfg = reference.build_config({"n_experts":64})
ref = reference.Model(cfg).cuda().eval()

def mk_model(mod):
    m = solution.Model(cfg).cuda().eval()
    m.load_state_dict(ref.state_dict(), strict=True)
    # override module
    m._forced_mod = mod
    return m

# Patch Model to use forced module
_orig_build = solution.Model._build_weights
def _patched_build(self):
    _orig_build(self)
    if hasattr(self,'_forced_mod'): self._mod = self._forced_mod
solution.Model._build_weights = _patched_build

mA = mk_model(base_mod)
mB = mk_model(cand_mod)

def run(m, ctx, steps):
    h = reference.init_token(cfg,7); st = reference.init_state(cfg,ctx,7)
    with torch.no_grad():
        for _ in range(steps): h,st=m.step(h,st)
    return h,st

def onetrial(m, ctx, steps):
    h = reference.init_token(cfg,7); st = reference.init_state(cfg,ctx,7)
    with torch.no_grad():
        for _ in range(3): h,st=m.step(h,st)
    torch.cuda.synchronize()
    t0=time.perf_counter()
    with torch.no_grad():
        for _ in range(steps): h,st=m.step(h,st)
    torch.cuda.synchronize()
    return (time.perf_counter()-t0)/steps*1e3

import random, statistics
for ctx in (2048,8192,16384):
    steps=30
    run(mA,ctx,5); run(mB,ctx,5); torch.cuda.synchronize()
    ratios=[]; As=[]; Bs=[]
    for _ in range(40):
        # tightly paired: measure A then B (order flipped randomly), ratio per rep
        if random.random()<0.5:
            a=onetrial(mA,ctx,steps); b=onetrial(mB,ctx,steps)
        else:
            b=onetrial(mB,ctx,steps); a=onetrial(mA,ctx,steps)
        ratios.append(a/b); As.append(a); Bs.append(b)
    med=statistics.median(ratios)
    print(f"ctx={ctx}: A(base)min={min(As):.4f} B(cand)min={min(Bs):.4f}  med_ratio(A/B)={med:.4f}  (>1 = B faster)")

# correctness of B vs reference
print("--- correctness B ---")
for seed in (0,1,2):
    for ctx in (2048,8192):
        h=reference.init_token(cfg,seed); str_=reference.init_state(cfg,ctx,seed); sts=reference.init_state(cfg,ctx,seed)
        with torch.no_grad():
            orf,_=ref.step(h.clone(),str_); osf,_=mB.step(h.clone(),sts)
        cos=torch.nn.functional.cosine_similarity(orf.float(),osf.float(),dim=0).item()
        print(f"  seed{seed} ctx{ctx}: cos={cos:.4f}")

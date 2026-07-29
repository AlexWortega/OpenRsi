import os, torch
os.environ.setdefault("CUDA_HOME","/tmp/cudatk")
import megakernel_src as _mk
from torch.utils.cpp_extension import load_inline
MOD = load_inline(name="kimi_prof", cpp_sources=_mk.CPP, cuda_sources=_mk.CUDA,
    functions=["mega_launch","get_prof"],
    extra_cuda_cflags=["-O3","-arch=sm_120","--use_fast_math","-DLB=6","-maxrregcount=40","-DPROF"],
    verbose=False)
import solution, reference, shapes
sol = solution
# monkeypatch module getter to reuse MOD
sol._MOD = MOD
def _get(): return MOD
sol._get_module = _get
cfg = reference.build_config({"n_experts":64})
m = solution.Model(cfg).cuda().eval()
ref = reference.Model(cfg).cuda().eval()
m.load_state_dict(ref.state_dict(), strict=True)
for ctx in (2048,16384):
    st = reference.init_state(cfg, ctx, 7)
    h = reference.init_token(cfg, 7)
    with torch.no_grad():
        for _ in range(5): h,st = m.step(h,st)
    torch.cuda.synchronize()
    buf = torch.zeros(32, dtype=torch.int64)
    MOD.get_prof(buf.data_ptr())  # reset
    N=50
    with torch.no_grad():
        for _ in range(N): h,st = m.step(h,st)
    torch.cuda.synchronize()
    buf = torch.zeros(32, dtype=torch.int64)
    MOD.get_prof(buf.data_ptr())
    p = buf.tolist()
    total = sum(p)
    names = {1:"kda_qkvg",6:"kda_conv",5:"kda_beta",2:"kda_state",3:"kda_o",
             10:"mla_rms",11:"mla_q",12:"mla_kva",13:"mla_qa/rope",15:"mla_scores",
             18:"mla_cvec",19:"mla_reduce",20:"mla_ohead",21:"mla_o",
             22:"moe_router",23:"moe_top",24:"moe_gu",25:"moe_down"}
    print(f"=== ctx={ctx} total cyc/step={total/N:.0f} ===")
    for i in sorted(names):
        if p[i]: print(f"  {names[i]:14s} {p[i]/N:10.0f}  {100*p[i]/total:5.1f}%")

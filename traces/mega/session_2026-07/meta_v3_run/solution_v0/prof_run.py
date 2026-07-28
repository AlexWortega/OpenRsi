import os, torch, time
os.environ.setdefault("CUDA_HOME","/tmp/cudatk")
import megakernel_src as _mk
from torch.utils.cpp_extension import load_inline
MOD = load_inline(name="kimi_prof", cpp_sources=_mk.CPP, cuda_sources=_mk.CUDA,
    functions=["mega_launch","get_prof"],
    extra_cuda_cflags=["-O3","-arch=sm_120","--use_fast_math","-DPROF"], verbose=False)
import solution, reference as ref, shapes
# monkeypatch solution to use prof module
solution._MOD = MOD
cfg = ref.build_config({"n_experts":64})
dev = torch.device("cuda:0")
m = solution.Model(cfg).to(dev).eval()
rm = ref.Model(cfg).to(dev).eval()
m.load_state_dict(rm.state_dict())
for ctx in (2048,8192,16384):
    st = ref.init_state(cfg, ctx, 7); tok = ref.init_token(cfg,7)
    with torch.no_grad():
        for _ in range(5): h,st = m.step(tok.clone() if False else h if False else tok, st)
    torch.cuda.synchronize()
    out = torch.zeros(32, dtype=torch.int64)
    MOD.get_prof(out.data_ptr())
    # run a fixed number for averaging
    st = ref.init_state(cfg, ctx, 7)
    N=20
    with torch.no_grad():
        for _ in range(N): h,st = m.step(tok, st)
    torch.cuda.synchronize()
    MOD.get_prof(out.data_ptr())
    o = out.tolist()
    labels={1:'kda_qkvg_gemv',6:'kda_conv',5:'kda_beta+sync',2:'kda_state',3:'kda_oproj',
            10:'mla_rms',11:'mla_qproj',12:'mla_kva',13:'mla_qa',14:'mla_x',15:'mla_scores',
            16:'mla_softmax_denom',17:'mla_exp',18:'mla_cvec',19:'mla_cvec_reduce',20:'mla_ohead',21:'mla_oproj',
            22:'moe_router',23:'moe_topk',24:'moe_gateup',25:'moe_down'}
    tot=sum(o)
    print(f"=== ctx={ctx} total cycles={tot} ({tot/N:.0f}/step) ===")
    for i in sorted(labels):
        if o[i]: print(f"  {labels[i]:20s} {o[i]/N:12.0f}  {100*o[i]/tot:5.1f}%")

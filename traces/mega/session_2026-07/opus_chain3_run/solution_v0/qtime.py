import os, sys, time, torch
os.environ.setdefault("CUDA_HOME","/tmp/cudatk")
import solution, reference
cfg = reference.build_config({"n_experts":64})
ref = reference.Model(cfg).cuda().eval()
m = solution.Model(cfg).cuda().eval()
m.load_state_dict(ref.state_dict(), strict=True)
def timeit(ctx, steps=40):
    h = reference.init_token(cfg,7); st = reference.init_state(cfg,ctx,7)
    with torch.no_grad():
        for _ in range(5): h,st=m.step(h,st)
    torch.cuda.synchronize()
    best=1e9
    for _ in range(5):
        t0=time.perf_counter()
        with torch.no_grad():
            for _ in range(steps): h,st=m.step(h,st)
        torch.cuda.synchronize()
        best=min(best,(time.perf_counter()-t0)/steps)
    return best*1e3
for ctx in (2048,8192,16384):
    print(f"ctx={ctx}: {timeit(ctx):.4f} ms/tok  NB={os.environ.get('KIMI_NB','auto')} LB={os.environ.get('KIMI_LB','2')} RREG={os.environ.get('KIMI_RREG','128')}")

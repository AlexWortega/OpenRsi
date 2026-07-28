import torch,time
import solution as S, reference as R
cfg=S.build_config({"n_experts":64})
m=S.Model(cfg).cuda().eval(); rm=R.Model(cfg).cuda().eval(); m.load_state_dict(rm.state_dict())
for ctx in (2048,8192,16384):
    h=R.init_token(cfg,7); st=R.init_state(cfg,ctx,7)
    with torch.no_grad():
        for _ in range(5): h,st=m.step(h,st)
    torch.cuda.synchronize(); t=time.perf_counter()
    with torch.no_grad():
        for _ in range(50): h,st=m.step(h,st)
    torch.cuda.synchronize(); print(f"ctx {ctx}: {(time.perf_counter()-t)/50*1e3:.3f} ms")

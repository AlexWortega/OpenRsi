import os, torch, time, statistics
os.environ.setdefault("CUDA_HOME","/tmp/cudatk")
import solution, reference as ref
cfg = ref.build_config({"n_experts":64})
dev=torch.device("cuda:0")
m=solution.Model(cfg).to(dev).eval(); rm=ref.Model(cfg).to(dev).eval()
m.load_state_dict(rm.state_dict())
for ctx in (2048,8192,16384):
    st=ref.init_state(cfg,ctx,7); tok=ref.init_token(cfg,7)
    with torch.no_grad():
        for _ in range(10): h,st=m.step(tok,st)
    torch.cuda.synchronize()
    ts=[]
    for _ in range(30):
        st=ref.init_state(cfg,ctx,7)
        torch.cuda.synchronize(); t0=time.perf_counter()
        with torch.no_grad():
            for _ in range(16): h,st=m.step(tok,st)
        torch.cuda.synchronize(); ts.append((time.perf_counter()-t0)/16*1e3)
    ts.sort()
    print(f"ctx={ctx}: min={ts[0]:.3f} med={statistics.median(ts):.3f} ms/tok")

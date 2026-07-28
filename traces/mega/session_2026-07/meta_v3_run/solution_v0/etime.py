import os, torch, statistics
os.environ.setdefault("CUDA_HOME","/tmp/cudatk")
import solution, reference as ref
cfg=ref.build_config({"n_experts":64}); dev=torch.device("cuda:0")
m=solution.Model(cfg).to(dev).eval(); rm=ref.Model(cfg).to(dev).eval(); m.load_state_dict(rm.state_dict())
res={}
for ctx in (2048,8192,16384):
    st=ref.init_state(cfg,ctx,7); tok=ref.init_token(cfg,7)
    with torch.no_grad():
        for _ in range(20): h,st=m.step(tok,st)
    torch.cuda.synchronize()
    samples=[]
    for _ in range(200):
        st=ref.init_state(cfg,ctx,7)
        e0=torch.cuda.Event(True); e1=torch.cuda.Event(True)
        e0.record()
        with torch.no_grad(): h,st=m.step(tok,st)
        e1.record(); torch.cuda.synchronize()
        samples.append(e0.elapsed_time(e1))
    samples.sort()
    p10=samples[len(samples)//10]
    res[ctx]=samples[0]
    print(f"ctx={ctx}: min={samples[0]:.3f} p10={p10:.3f} med={statistics.median(samples):.3f} ms")
import math
g=math.exp(sum(math.log(v) for v in res.values())/3)
print(f"geomean min: {g:.3f} ms")

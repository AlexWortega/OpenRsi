import os,time,math
os.environ["CUDA_HOME"]="/tmp/cudatk"
import torch, reference as ref, solution
cfg=ref.build_config({"n_experts":64})
sol=solution.Model(cfg).cuda().eval(); refm=ref.Model(cfg).cuda().eval()
sol.load_state_dict(refm.state_dict(),strict=True); sol._build_weights()
if os.environ["M"]=="none": sol._pin_ptr=0; sol._pin_size=0
def bench(L,trials=50,inner=20):
  st=ref.init_state(cfg,L,7); h=ref.init_token(cfg,7)
  with torch.no_grad():
    for _ in range(8): h,st=sol.step(h,st)
  torch.cuda.synchronize(); best=1e9
  for _ in range(trials):
    t0=time.perf_counter()
    for _ in range(inner):
      with torch.no_grad(): h,st=sol.step(h,st)
    torch.cuda.synchronize(); best=min(best,(time.perf_counter()-t0)/inner)
  return best*1e3
r={L:bench(L) for L in [2048,8192,16384]}
g=math.exp(sum(math.log(v) for v in r.values())/3)
print(f"M={os.environ['M']}: 2048={r[2048]:.4f} 8192={r[8192]:.4f} 16384={r[16384]:.4f} gmean={g:.4f}")

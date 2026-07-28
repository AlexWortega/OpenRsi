import torch,time,reference as R,solution as S
cfg=R.build_config({'n_experts':64})
rm=R.Model(cfg).cuda().eval(); sm=S.Model(cfg).cuda().eval(); sm.load_state_dict(rm.state_dict())
for ctx in (2048,8192,16384):
    tok=R.init_token(cfg,7)
    st=R.init_state(cfg,ctx,7)
    # warmup + reuse (note MLA cache grows, but for timing keep fixed by resetting)
    for _ in range(3):
        s=[dict(x) for x in st]  # shallow copy dicts
        h,_=sm.step(tok.clone(),s)
    torch.cuda.synchronize()
    # time just step with pre-made state list
    it=100
    states=[[dict(x) for x in st] for _ in range(it)]
    torch.cuda.synchronize(); t0=time.perf_counter()
    for i in range(it):
        h,_=sm.step(tok.clone(),states[i])
    torch.cuda.synchronize()
    print(f'ctx={ctx}: {(time.perf_counter()-t0)/it*1e3:.3f} ms/step',flush=True)

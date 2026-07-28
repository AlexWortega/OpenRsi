import torch,time,reference as R,solution as S
cfg=R.build_config({'n_experts':64})
rm=R.Model(cfg).cuda().eval(); sm=S.Model(cfg).cuda().eval(); sm.load_state_dict(rm.state_dict())
def timeit(ctx,nblk,lastmoe,it=50):
    st=R.init_state(cfg,ctx,7); tok=R.init_token(cfg,7)
    sm._dbg_nblk=nblk; sm._dbg_last_moe=lastmoe
    for _ in range(3):
        s=R.init_state(cfg,ctx,7); h,_=sm.step(tok.clone(),s)
    torch.cuda.synchronize(); t0=time.perf_counter()
    for _ in range(it):
        s=R.init_state(cfg,ctx,7); h,_=sm.step(tok.clone(),s)
    torch.cuda.synchronize()
    return (time.perf_counter()-t0)/it*1e3
for ctx in (2048,8192,16384):
    print(f'ctx={ctx}: nblk1={timeit(ctx,1,1):.3f} nblk2={timeit(ctx,2,1):.3f} nblk3={timeit(ctx,3,1):.3f} nblk4={timeit(ctx,4,1):.3f} ms',flush=True)

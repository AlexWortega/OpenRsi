import torch,time,reference as R,solution as S
cfg=R.build_config({'n_experts':64})
rm=R.Model(cfg).cuda().eval(); sm=S.Model(cfg).cuda().eval(); sm.load_state_dict(rm.state_dict())
sm._build_weights()
tok=R.init_token(cfg,7)
def raw(ctx,nblk,lastmoe,it=200):
    st=R.init_state(cfg,ctx,7)
    Sptrs=[];Soff=[];Lval=0
    for i,blk in enumerate(sm.blocks):
        Soff.append(len(Sptrs)); s=st[i]
        if blk.kind=='K': Sptrs+=[s['S'].data_ptr(),s['cq'].data_ptr(),s['ck'].data_ptr(),s['cv'].data_ptr()]
        else:
            L=s['c_kv'].shape[0]; Lval=L
            nc=torch.empty(L+1,512,dtype=torch.bfloat16,device='cuda'); nk=torch.empty(L+1,64,dtype=torch.bfloat16,device='cuda')
            Sptrs+=[s['c_kv'].data_ptr(),s['k_rope'].data_ptr(),nc.data_ptr(),nk.data_ptr()]
    St=torch.tensor(Sptrs,dtype=torch.int64,device='cuda')
    meta=torch.tensor(Soff+[Lval,nblk,lastmoe],dtype=torch.int32,device='cuda')
    hid=tok.float().contiguous()
    need=6_000_000; 
    if sm._scr is None or sm._scr.numel()<need: sm._scr=torch.empty(need,device='cuda')
    scr=sm._scr; mod=sm._mod
    for _ in range(5): mod.mega_launch(sm._Wt.data_ptr(),sm._Woff.data_ptr(),St.data_ptr(),meta.data_ptr(),hid.data_ptr(),scr.data_ptr())
    torch.cuda.synchronize(); t0=time.perf_counter()
    for _ in range(it): mod.mega_launch(sm._Wt.data_ptr(),sm._Woff.data_ptr(),St.data_ptr(),meta.data_ptr(),hid.data_ptr(),scr.data_ptr())
    torch.cuda.synchronize(); return (time.perf_counter()-t0)/it*1e3
for ctx in (2048,8192,16384):
    a1=raw(ctx,1,0); a1m=raw(ctx,1,1); a2m=raw(ctx,2,1); a3m=raw(ctx,3,1); a4a=raw(ctx,4,0); a4=raw(ctx,4,1)
    print(f'ctx={ctx}: kda_attn={a1:.3f} +moe={a1m:.3f} b2={a2m:.3f} b3={a3m:.3f} +mla_attn={a4a:.3f} full={a4:.3f}',flush=True)

import torch,torch.nn.functional as F,reference as R,solution as S
cfg=R.build_config({'n_experts':64})
rm=R.Model(cfg).cuda().eval(); sm=S.Model(cfg).cuda().eval(); sm.load_state_dict(rm.state_dict())
tok=R.init_token(cfg,7)
def ref_partial(nblk,last_moe):
    st=R.init_state(cfg,2048,7); h=tok.clone()
    with torch.no_grad():
        for i in range(nblk):
            blk=rm.blocks[i]
            hn=R._rmsnorm(h,blk.attn_norm); h=h+blk.attn.step(hn,st[i])
            if last_moe or i<nblk-1:
                hn2=R._rmsnorm(h,blk.moe_norm); h=h+blk.moe.step(hn2)
    return h
for nblk in (1,2,3,4):
  for lm in (0,1):
    sm._dbg_nblk=nblk; sm._dbg_last_moe=lm
    st=R.init_state(cfg,512,7)
    with torch.no_grad(): o_s,_=sm.step(tok.clone(),st)
    st2=R.init_state(cfg,512,7)
    # ref_partial uses ctx 512 too
    h=tok.clone()
    with torch.no_grad():
        for i in range(nblk):
            blk=rm.blocks[i]
            hn=R._rmsnorm(h,blk.attn_norm); h=h+blk.attn.step(hn,st2[i])
            if lm or i<nblk-1:
                hn2=R._rmsnorm(h,blk.moe_norm); h=h+blk.moe.step(hn2)
    o_r=h
    print(f'nblk={nblk} lastmoe={lm} cos={F.cosine_similarity(o_r.float().flatten(),o_s.float().flatten(),dim=0).item():.5f}',flush=True)
    del st,st2; torch.cuda.empty_cache()

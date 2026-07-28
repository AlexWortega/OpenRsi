import torch,torch.nn.functional as F,reference as R,solution as S
cfg=R.build_config({'n_experts':64})
rm=R.Model(cfg).cuda().eval(); sm=S.Model(cfg).cuda().eval(); sm.load_state_dict(rm.state_dict())
for ctx in (2048,8192):
    st_r=R.init_state(cfg,ctx,7); st_s=R.init_state(cfg,ctx,7); tok=R.init_token(cfg,7)
    with torch.no_grad():
        o_r,_=rm.step(tok.clone(),st_r); o_s,_=sm.step(tok.clone(),st_s)
    print('ctx',ctx,'cos',F.cosine_similarity(o_r.float().flatten(),o_s.float().flatten(),dim=0).item(),flush=True)

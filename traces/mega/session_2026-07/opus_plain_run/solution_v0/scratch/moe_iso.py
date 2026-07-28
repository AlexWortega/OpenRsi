import torch,torch.nn.functional as F,reference as R
cfg=R.build_config({'n_experts':64})
rm=R.Model(cfg).cuda().eval()
tok=R.init_token(cfg,7); st=R.init_state(cfg,512,7); h=tok.clone()
with torch.no_grad():
  for i,blk in enumerate(rm.blocks):
    hn=R._rmsnorm(h,blk.attn_norm); h=h+blk.attn.step(hn,st[i])
    hn2_bf=R._rmsnorm(h,blk.moe_norm)
    o_ref=blk.moe.step(hn2_bf)
    xn=hn2_bf.float()
    probs=torch.softmax((xn@blk.moe.router.weight.float().t()),-1)
    w,idx=torch.topk(probs,8); w=w/(w.sum()+1e-9)*cfg.routed_scaling
    out=torch.zeros(cfg.hidden,device='cuda')
    def ffn_f(x,eg,eu,ed,e):
        g=eg.weight_bf(e).float(); u=eu.weight_bf(e).float(); d=ed.weight_bf(e).float()
        hh=F.silu(x@g)*(x@u); return hh@d
    for j in range(8): out=out+w[j]*ffn_f(xn,blk.moe.gate,blk.moe.up,blk.moe.down,int(idx[j]))
    out=out+ffn_f(xn,blk.moe.s_gate,blk.moe.s_up,blk.moe.s_down,0)
    print(f'blk {i} moe: emul vs ref cos={F.cosine_similarity(o_ref.float(),out.float(),dim=0).item():.6f}',flush=True)
    h=h+o_ref

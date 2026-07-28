import torch, torch.nn.functional as F, copy
import reference as R
torch.manual_seed(0)
cfg = R.build_config({"n_experts":64})
m = R.Model(cfg).cuda().eval()
st = R.init_state(cfg, 2048, 0)
h = R.init_token(cfg, 0)
mla = m.blocks[3].attn
x = R._rmsnorm(h, m.blocks[3].attn_norm)
st_ref = copy.deepcopy(st[3])
with torch.no_grad():
    o_ref = mla.step(x, st_ref)

with torch.no_grad():
    H=cfg.mla_heads; qn=cfg.qk_nope; qr=cfg.qk_rope; vh=cfg.v_head; L0=cfg.kv_lora
    pos = st[3]["c_kv"].shape[0]
    q = mla.q_proj(x).view(H, qn+qr)
    q_nope = q[:,:qn].float()
    q_rope = q[:,qn:]
    kv = mla.kv_a(x)
    c_kv = kv[:L0]; k_rope = kv[L0:]
    cos,sin = R._rope_cossin(pos, qr, cfg.rope_theta, x.device)
    q_rope = R._apply_rope(q_rope,cos,sin).float()
    k_rope = R._apply_rope(k_rope,cos,sin)
    ckv = torch.cat([st[3]["c_kv"], c_kv[None]],0).float()   # [L,512]
    krope = torch.cat([st[3]["k_rope"], k_rope[None]],0).float() # [L,64]
    Wb = mla.kv_b.weight_bf().float().view(L0, H, qn+vh)
    Wk = Wb[:,:,:qn].permute(1,0,2).contiguous()  # [H,512,128]
    Wv = Wb[:,:,qn:].permute(1,0,2).contiguous()  # [H,512,128]
    qa = torch.einsum('hd,hkd->hk', q_nope, Wk)  # [H,512]
    L = ckv.shape[0]
    s_nope = torch.einsum('hk,lk->lh', qa, ckv)
    s_rope = torch.einsum('hd,ld->lh', q_rope, krope)
    scores = (s_nope+s_rope)*mla.scale
    p = torch.softmax(scores, dim=0)  # [L,H]
    # context in latent space: cvec[h,:] = sum_l p[l,h]*ckv[l,:] -> [H,512]
    cvec = torch.einsum('lh,lk->hk', p, ckv)  # [H,512]
    o = torch.einsum('hk,hkd->hd', cvec, Wv)  # [H,128]
    o_abs = mla.o_proj(o.reshape(H*vh).to(torch.bfloat16))
print("cos", F.cosine_similarity(o_ref.float().flatten(), o_abs.float().flatten(), dim=0).item())

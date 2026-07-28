import torch,time,reference as R,solution as S
cfg=R.build_config({'n_experts':64})
rm=R.Model(cfg).cuda().eval(); sm=S.Model(cfg).cuda().eval(); sm.load_state_dict(rm.state_dict())
ctx=8192
tok=R.init_token(cfg,7); st=R.init_state(cfg,ctx,7)
sm._build_weights()
# prebuild fixed St/meta for MLA fixed L; just call kernel repeatedly with same buffers
mod=sm._mod
# do one step to set up buffers
h,_=sm.step(tok.clone(),[dict(x) for x in st]); torch.cuda.synchronize()
# time raw mega_launch by replaying with cached tensors
# reconstruct args like step but once
import types
# measure python overhead of building tensors:
def build_only():
    Sptrs=[]; Soff=[]; Lval=0
    for i,blk in enumerate(sm.blocks):
        Soff.append(len(Sptrs)); s=st[i]
        if blk.kind=='K': Sptrs+=[s['S'].data_ptr(),s['cq'].data_ptr(),s['ck'].data_ptr(),s['cv'].data_ptr()]
        else:
            L=s['c_kv'].shape[0]; Lval=L
            Sptrs+=[s['c_kv'].data_ptr(),s['k_rope'].data_ptr(),s['c_kv'].data_ptr(),s['k_rope'].data_ptr()]
    St=torch.tensor(Sptrs,dtype=torch.int64,device='cuda')
    meta=torch.tensor(Soff+[Lval,4,1],dtype=torch.int32,device='cuda')
    return St,meta
torch.cuda.synchronize(); t0=time.perf_counter(); it=200
for _ in range(it): St,meta=build_only()
torch.cuda.synchronize(); print('build tensors',(time.perf_counter()-t0)/it*1e3,'ms')
St,meta=build_only()
hid=tok.float().contiguous(); scr=sm._scr
torch.cuda.synchronize(); t0=time.perf_counter()
for _ in range(it):
    mod.mega_launch(sm._Wt.data_ptr(),sm._Woff.data_ptr(),St.data_ptr(),meta.data_ptr(),hid.data_ptr(),scr.data_ptr())
torch.cuda.synchronize(); print('raw kernel',(time.perf_counter()-t0)/it*1e3,'ms')

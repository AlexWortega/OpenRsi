import torch, time
# measure achievable bandwidth on this MIG slice
N = 1<<28  # 256M elements
a = torch.empty(N, dtype=torch.uint8, device='cuda')
b = torch.empty(N, dtype=torch.uint8, device='cuda')
for _ in range(3): b.copy_(a)
torch.cuda.synchronize()
t0=time.perf_counter()
it=20
for _ in range(it): b.copy_(a)
torch.cuda.synchronize()
dt=(time.perf_counter()-t0)/it
print(f"copy {N} bytes each way, {2*N/dt/1e9:.0f} GB/s")

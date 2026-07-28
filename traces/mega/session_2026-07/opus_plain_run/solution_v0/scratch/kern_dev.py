"""Standalone dev harness for the megakernel: build source, test KDA stage vs torch."""
import os
os.environ.setdefault("CUDA_HOME","/tmp/cudatk")
import torch, math
from torch.utils.cpp_extension import load_inline

# ---- layout constants ----
d=2304; Hk=32; Dk=128; C=Hk*Dk  # 4096
SHORT=4
# scratch float offsets
OFF={}
cur=0
def alloc(name,n):
    global cur
    OFF[name]=cur; cur+=n
alloc('xn',d)
alloc('xn2',d)
alloc('q',C); alloc('k',C); alloc('v',C); alloc('g',C)
alloc('beta',Hk)
alloc('attn_out',d)
alloc('moe_out',d)
alloc('hid',d)
SCRATCH_FLOATS=cur
print("scratch floats",SCRATCH_FLOATS)

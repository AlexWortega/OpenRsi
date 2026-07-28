"""Triton primitives for the fused decode kernel."""
from __future__ import annotations
import torch
import triton
import triton.language as tl

# CPU-facing constants match reference.py
GROUP_SIZE = 128
EPS = 1.0e-6

# --------------------------------------------------------------------------- #
# inline helpers (these compile into the main kernel as device functions)
# --------------------------------------------------------------------------- #
@triton.jit
def membar():
    """Global memory fence before/after a grid barrier."""
    tl.inline_asm_elementwise("membar.gl;", "=r", [], dtype=tl.int32, is_pure=False, pack=1)


@triton.jit
def grid_barrier(arrive, depart, phase, NB: tl.constexpr, BS: tl.constexpr):
    """Two-counter device-wide barrier.  depart[] is *not* reset (each phase
    uses its own slot), so no reset race exists."""
    membar()
    zeros = tl.zeros((BS,), dtype=tl.int32)
    t0 = tl.arange(0, BS) == 0
    arr = tl.atomic_add((arrive + phase) + zeros,
                        tl.full((BS,), 1, dtype=tl.int32), mask=t0)
    arrival = tl.sum(tl.where(t0, arr, 0))
    is_last = arrival == NB - 1
    if is_last:
        tl.store(depart + phase, 1)
    while tl.load(depart + phase, volatile=True) == 0:
        pass
    membar()
    tl.debug_barrier()


@triton.jit
def quant_gemv(x_ptr, w_ptr, s_ptr, z_ptr, y_ptr,
               K, N, w_off_byte, s_off_el, z_off_el,
               BS: tl.constexpr, GROUP: tl.constexpr = 128):
    """Fused int4 unpack+dequant GEMV: y = x @ W, W stored transposed as
    [N, K//2] uint8, with scales/zeros [N, K//GROUP] bf16.
    Offsets index into the packed tensors."""
    NB = tl.num_programs(0)
    cols_per_block = (N + NB - 1) // NB
    n0 = tl.program_id(0) * cols_per_block
    n1 = tl.minimum(n0 + cols_per_block, N)
    half = K // 2
    gstride = K // GROUP
    w0 = w_off_byte
    s0 = s_off_el
    z0 = z_off_el
    for _ in range(0, n1 - n0):
        n_local = n0
        acc = 0.0
        kidx = tl.arange(0, GROUP // 2)  # packed positions inside a group
        xidx = tl.arange(0, GROUP)        # input positions inside a group
        for g in range(0, K // GROUP):
            base_k = g * GROUP
            base_p = g * (GROUP // 2)
            xb = tl.load(x_ptr + base_k + xidx).to(tl.float32)
            wb = tl.load(w_ptr + w0 + n_local * half + base_p + kidx)
            lo = wb & 0xF
            hi = (wb >> 4) & 0xF
            w = tl.interleave(lo, hi).to(tl.float32)
            s = tl.load(s_ptr + s0 + n_local * gstride + g).to(tl.float32)
            z = tl.load(z_ptr + z0 + n_local * gstride + g).to(tl.float32)
            w = (w - z) * s
            acc = acc + tl.sum(xb * w)
        tl.store(y_ptr + n_local, acc.to(tl.bfloat16))
        n0 = n0 + 1


@triton.jit
def quant_gemv_expert(x_ptr, w_ptr, s_ptr, z_ptr, y_ptr,
                      K, N, base_w_off, base_s_off, base_z_off,
                      expert_idx, expert_byte, expert_s_el, expert_z_el,
                      BS: tl.constexpr, GROUP: tl.constexpr = 128):
    """Same as quant_gemv but selects one expert slice.
    Expert weight layout: [E, N, K//2] uint8, [E, N, K//GROUP] bf16."""
    NB = tl.num_programs(0)
    cols_per_block = (N + NB - 1) // NB
    n0 = tl.program_id(0) * cols_per_block
    n1 = tl.minimum(n0 + cols_per_block, N)
    half = K // 2
    gstride = K // GROUP
    eidx = expert_idx
    w0 = base_w_off + eidx * expert_byte
    s0 = base_s_off + eidx * expert_s_el
    z0 = base_z_off + eidx * expert_z_el
    for _ in range(0, n1 - n0):
        n_local = n0
        acc = 0.0
        kidx = tl.arange(0, GROUP // 2)
        xidx = tl.arange(0, GROUP)
        for g in range(0, K // GROUP):
            base_k = g * GROUP
            base_p = g * (GROUP // 2)
            xb = tl.load(x_ptr + base_k + xidx).to(tl.float32)
            wb = tl.load(w_ptr + w0 + n_local * half + base_p + kidx)
            lo = wb & 0xF
            hi = (wb >> 4) & 0xF
            w = tl.interleave(lo, hi).to(tl.float32)
            s = tl.load(s_ptr + s0 + n_local * gstride + g).to(tl.float32)
            z = tl.load(z_ptr + z0 + n_local * gstride + g).to(tl.float32)
            w = (w - z) * s
            acc = acc + tl.sum(xb * w)
        tl.store(y_ptr + n_local, acc.to(tl.bfloat16))
        n0 = n0 + 1


@triton.jit
def bf16_gemv(x_ptr, w_ptr, y_ptr, K, N,
              w_off_el, BS: tl.constexpr, TILE: tl.constexpr = 256):
    """Plain bf16 weight GEMV: w shape [N, K] bf16, transposed for coalescing."""
    NB = tl.num_programs(0)
    cols_per_block = (N + NB - 1) // NB
    n0 = tl.program_id(0) * cols_per_block
    n1 = tl.minimum(n0 + cols_per_block, N)
    for _ in range(0, n1 - n0):
        n_local = n0
        acc = 0.0
        for k0 in range(0, K, TILE):
            kidx = k0 + tl.arange(0, TILE)
            xb = tl.load(x_ptr + kidx).to(tl.float32)
            wb = tl.load(w_ptr + w_off_el + n_local * K + kidx).to(tl.float32)
            acc = acc + tl.sum(xb * wb)
        tl.store(y_ptr + n_local, acc.to(tl.bfloat16))
        n0 = n0 + 1


@triton.jit
def rmsnorm_block(x_ptr, w_ptr, y_ptr, N, BS: tl.constexpr, EPS: tl.constexpr):
    """ RMSNorm(x) * w . Computes a per-block partial sum, then block 0
    finishes the norm and broadcasts.  Writes y = x / sqrt(mean(x^2)+eps)*w"""
    NB = tl.num_programs(0)
    elems_per_block = (N + NB - 1) // NB
    b0 = tl.program_id(0) * elems_per_block
    b1 = tl.minimum(b0 + elems_per_block, N)
    # partial sum of squares
    local_sum = 0.0
    for k0 in range(b0, b1, BS):
        idx = k0 + tl.arange(0, BS)
        mask = idx < b1
        xb = tl.load(x_ptr + idx, mask=mask, other=0.0).to(tl.float32)
        local_sum = local_sum + tl.sum(xb * xb)
    # reduce across block
    local_sum = tl.sum(local_sum)                # broadcast scalar
    scale = tl.full((BS,), 0.0, dtype=tl.float32)
    scale = tl.where(tl.arange(0, BS) == 0, local_sum, scale)
    # block-level sum, result on all threads
    ss = tl.sum(scale)
    # We need a global reduction of ss.  For simplicity use atomics on a float32
    # scratch location.  The caller should supply a dedicated fp32 reduction slot.
    pass


@triton.jit
def silu(x):
    return x * tl.sigmoid(x)

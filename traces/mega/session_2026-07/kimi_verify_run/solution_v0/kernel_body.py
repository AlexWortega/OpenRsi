"""Generated CUDA kernel body for the fused step (sidecar of solution.py)."""
from __future__ import annotations
import math


def _add_kernel_body(cfg, info, mc):
    D = cfg.hidden
    C = cfg.kda_heads * cfg.kda_head_dim
    H = cfg.kda_heads
    Dh = cfg.kda_head_dim
    KV = cfg.kv_lora
    QN = cfg.qk_nope
    QR = cfg.qk_rope
    VH = cfg.v_head
    Q_HEAD = QN + QR
    E = cfg.n_experts
    KACT = cfg.n_active
    M = cfg.moe_inter

    def _(x):
        return str(x)

    body = f'''
__global__ void step_kernel(Params* p, int L) {{
    const int tid = threadIdx.x;
    const int bid = blockIdx.x;
    const int nb = gridDim.x;
    int ph = 0;

    for (int i = bid * blockDim.x + tid; i < {_(info["ws_el"])}; i += nb * blockDim.x) p->ws[i] = f2b(0.0f);
    for (int i = bid * blockDim.x + tid; i < {_(info["fws_el"])}; i += nb * blockDim.x) p->fws[i] = 0.0f;
    for (int i = bid; i < {_(info["sync_el"])}; i += nb) p->sync[i] = 0;
    __syncthreads();
    barrier(p->sync, ph++);

    int cur = OFF_H0;
    int nxt = OFF_H1;
'''

    for b in range(len(cfg.pattern)):
        blk = cfg.pattern[b]
        anorm_off = info["params_off"][f"ANORM{b}"]
        mnorm_off = info["params_off"][f"MNORM{b}"]
        body += f'''
    // ----- layer {b} ({blk}) -----
    if (bid == 0) p->fws[FWS_RMS] = 0.0f;
    barrier(p->sync, ph++);
    {{
        float partial = 0.0f;
        for (int i = bid * blockDim.x + tid; i < D; i += nb * blockDim.x) {{
            float v = b2f(p->ws[cur + i]);
            partial += v * v;
        }}
        __shared__ float sd[BLOCK_SIZE];
        sd[tid] = partial; __syncthreads();
        for (int s = blockDim.x / 2; s > 0; s >>= 1) {{
            if (tid < s) sd[tid] += sd[tid + s];
            __syncthreads();
        }}
        if (tid == 0) atomicAdd(p->fws + FWS_RMS, sd[0] / (float)D);
    }}
    barrier(p->sync, ph++);
    {{
        float invrms = rsqrtf(p->fws[FWS_RMS] + 1e-6f);
        for (int i = bid * blockDim.x + tid; i < D; i += nb * blockDim.x) {{
            p->ws[OFF_XN + i] = f2b(b2f(p->ws[cur + i]) * invrms * b2f(p->params[{_(anorm_off)} + i]));
        }}
    }}
    barrier(p->sync, ph++);
'''
        if blk == "K":
            body += f'''
    quant_gemv(p->attn_w, p->attn_s, p->attn_z, p->ws + OFF_XN, p->ws + OFF_TA + 0*C,   D, C, AOFF_Q{b}, ASOFF_Q{b}, AZOFF_Q{b}, p, 0);
    quant_gemv(p->attn_w, p->attn_s, p->attn_z, p->ws + OFF_XN, p->ws + OFF_TA + 1*C,   D, C, AOFF_K{b}, ASOFF_K{b}, AZOFF_K{b}, p, 0);
    quant_gemv(p->attn_w, p->attn_s, p->attn_z, p->ws + OFF_XN, p->ws + OFF_TA + 2*C,   D, C, AOFF_V{b}, ASOFF_V{b}, AZOFF_V{b}, p, 0);
    quant_gemv(p->attn_w, p->attn_s, p->attn_z, p->ws + OFF_XN, p->ws + OFF_TA + 3*C,   D, C, AOFF_G{b}, ASOFF_G{b}, AZOFF_G{b}, p, 0);
    barrier(p->sync, ph++);
'''
            conv_off = info["params_off"][f"CONV{b}"]
            kidx = info["kda_layers"].index(b)
            cq = f"cq{kidx}"; ck = f"ck{kidx}"; cv = f"cv{kidx}"
            body += f'''
    {{
        const int C_local = C;
        for (int c = bid * blockDim.x + tid; c < C_local; c += nb * blockDim.x) {{
            float acc[3];
            acc[0] = acc[1] = acc[2] = 0.0f;
            for (int t = 0; t < WIN; ++t) {{
                float prev_q = b2f(p->{cq}[t * C_local + c]);
                float prev_k = b2f(p->{ck}[t * C_local + c]);
                float prev_v = b2f(p->{cv}[t * C_local + c]);
                acc[0] += prev_q * b2f(p->params[{_(conv_off)} + 0 * C_local * SHORTC + c * SHORTC + t]);
                acc[1] += prev_k * b2f(p->params[{_(conv_off)} + 1 * C_local * SHORTC + c * SHORTC + t]);
                acc[2] += prev_v * b2f(p->params[{_(conv_off)} + 2 * C_local * SHORTC + c * SHORTC + t]);
            }}
            float raw_q = b2f(p->ws[OFF_TA + 0*C_local + c]);
            float raw_k = b2f(p->ws[OFF_TA + 1*C_local + c]);
            float raw_v = b2f(p->ws[OFF_TA + 2*C_local + c]);
            acc[0] += raw_q * b2f(p->params[{_(conv_off)} + 0 * C_local * SHORTC + c * SHORTC + WIN]);
            acc[1] += raw_k * b2f(p->params[{_(conv_off)} + 1 * C_local * SHORTC + c * SHORTC + WIN]);
            acc[2] += raw_v * b2f(p->params[{_(conv_off)} + 2 * C_local * SHORTC + c * SHORTC + WIN]);
            p->ws[OFF_TA + 0*C_local + c] = f2b(silu(acc[0]));
            p->ws[OFF_TA + 1*C_local + c] = f2b(silu(acc[1]));
            p->ws[OFF_TA + 2*C_local + c] = f2b(silu(acc[2]));
            for (int t = 0; t < WIN - 1; ++t) {{
                p->{cq}[t * C_local + c] = p->{cq}[(t + 1) * C_local + c];
                p->{ck}[t * C_local + c] = p->{ck}[(t + 1) * C_local + c];
                p->{cv}[t * C_local + c] = p->{cv}[(t + 1) * C_local + c];
            }}
            p->{cq}[(WIN - 1) * C_local + c] = f2b(raw_q);
            p->{ck}[(WIN - 1) * C_local + c] = f2b(raw_k);
            p->{cv}[(WIN - 1) * C_local + c] = f2b(raw_v);
        }}
    }}
    barrier(p->sync, ph++);
'''
            beta_off = info["params_off"][f"BETA{b}"]
            body += f'''
    bf16_gemv(p->params + {_(beta_off)}, p->ws + OFF_XN, p->ws + OFF_TB, D, H, 0, ph, p);
    barrier(p->sync, ph++);
'''
            S = f"S{kidx}"
            body += f'''
    for (int i = bid * blockDim.x + tid; i < C; i += nb * blockDim.x) p->fws[FWS_O + i] = 0.0f;
    __syncthreads();
    barrier(p->sync, ph++);
    {{
        const int C_local = C;
        const int Dh_local = Dh;
        __shared__ float ksh[Dh];
        __shared__ float psh[BLOCK_SIZE];
        for (int flat = bid; flat < C_local; flat += nb) {{
            int h = flat / Dh_local;
            int i = flat % Dh_local;
            float q_i = b2f(p->ws[OFF_TA + 0*C_local + flat]);
            float k_i = b2f(p->ws[OFF_TA + 1*C_local + flat]);
            float g_i = b2f(p->ws[OFF_TA + 3*C_local + flat]);
            float beta_h = b2f(p->ws[OFF_TB + h]);
            float expg = 1.0f / (1.0f + expf(g_i));
            for (int d = tid; d < Dh_local; d += blockDim.x) ksh[d] = b2f(p->ws[OFF_TA + 1*C_local + h * Dh_local + d]);
            __syncthreads();
            float pred_part = 0.0f;
            for (int d = tid; d < Dh_local; d += blockDim.x) {{
                float s_old = b2f(p->{S}[flat * Dh_local + d]);
                pred_part += s_old * ksh[d];
            }}
            psh[tid] = pred_part; __syncthreads();
            for (int s = blockDim.x / 2; s > 0; s >>= 1) {{
                if (tid < s) psh[tid] += psh[tid + s];
                __syncthreads();
            }}
            float pred = psh[0];
            const __nv_bfloat16* vptr = p->ws + OFF_TA + 2*C_local + h * Dh_local;
            for (int j = tid; j < Dh_local; j += blockDim.x) {{
                float s_old = b2f(p->{S}[flat * Dh_local + j]);
                float v_j = b2f(vptr[j]);
                float snew = s_old * expg + beta_h * k_i * (v_j - pred);
                p->{S}[flat * Dh_local + j] = f2b(snew);
                atomicAdd(p->fws + FWS_O + h * Dh_local + j, q_i * snew);
            }}
            __syncthreads();
        }}
    }}
    barrier(p->sync, ph++);
'''
            body += f'''
    for (int i = bid * blockDim.x + tid; i < C; i += nb * blockDim.x)
        p->ws[OFF_TB + i] = f2b(p->fws[FWS_O + i]);
    __syncthreads();
    barrier(p->sync, ph++);
    quant_gemv(p->attn_w, p->attn_s, p->attn_z, p->ws + OFF_TB, p->ws + OFF_TA, C, D, AOFF_O{b}, ASOFF_O{b}, AZOFF_O{b}, p, 0);
    barrier(p->sync, ph++);
'''
        else:
            body += f'''
    quant_gemv(p->attn_w, p->attn_s, p->attn_z, p->ws + OFF_XN, p->ws + OFF_TA + 0,        D, H*Q_HEAD, AOFF_MQ{b}, ASOFF_MQ{b}, AZOFF_MQ{b}, p, 0);
    quant_gemv(p->attn_w, p->attn_s, p->attn_z, p->ws + OFF_XN, p->ws + OFF_TA + H*Q_HEAD,  D, KV+QR,   AOFF_MKVA{b}, ASOFF_MKVA{b}, AZOFF_MKVA{b}, p, 0);
    barrier(p->sync, ph++);
'''
            body += f'''
    {{
        float inv[QR/2];
        for (int rr = tid; rr < QR/2; rr += blockDim.x) {{
            inv[rr] = 1.0f / powf({_(cfg.rope_theta)}f, 2.0f * (float)rr / (float)QR);
        }}
        for (int pair = bid * blockDim.x + tid; pair < H * QR / 2; pair += nb * blockDim.x) {{
            int h = pair / (QR/2);
            int r = (pair % (QR/2));
            float ang = (float)L * inv[r];
            float c = cosf(ang), s = sinf(ang);
            int base = OFF_TA + h * Q_HEAD + QN + 2*r;
            float e = b2f(p->ws[base]);
            float o = b2f(p->ws[base + 1]);
            p->ws[base]     = f2b(e * c - o * s);
            p->ws[base + 1] = f2b(o * c + e * s);
        }}
        for (int r = bid * blockDim.x + tid; r < QR/2; r += nb * blockDim.x) {{
            float ang = (float)L * inv[r];
            float c = cosf(ang), s = sinf(ang);
            int base = OFF_TA + H*Q_HEAD + KV + 2*r;
            float e = b2f(p->ws[base]);
            float o = b2f(p->ws[base + 1]);
            p->ws[base]     = f2b(e * c - o * s);
            p->ws[base + 1] = f2b(o * c + e * s);
        }}
        for (int j = bid * blockDim.x + tid; j < KV; j += nb * blockDim.x) {{
            p->c_kv[L * KV + j] = p->ws[OFF_TA + H*Q_HEAD + j];
        }}
        for (int j = bid * blockDim.x + tid; j < QR; j += nb * blockDim.x) {{
            p->k_rope[L * QR + j] = p->ws[OFF_TA + H*Q_HEAD + KV + j];
        }}
    }}
    barrier(p->sync, ph++);
'''
            body += f'''
    quant_gemv(p->kvba_w, p->kvba_s, p->kvba_z,
               p->ws + OFF_TA, p->ws + OFF_TB, H*QN, KV,
               0, 0, 0, p, 0);
    barrier(p->sync, ph++);
'''
            body += f'''
    if (bid == 0) {{ p->fws[FWS_MAX] = -1e30f; p->fws[FWS_SUM] = 0.0f; }}
    for (int j = bid * blockDim.x + tid; j < KV; j += nb * blockDim.x) p->fws[FWS_Z + j] = 0.0f;
    __syncthreads();
    barrier(p->sync, ph++);
    {{
        const int Len = L + 1;
        const int KV_local = KV;
        const int QR_local = QR;
        __shared__ float sdot[BLOCK_SIZE];
        float local_max = -1e30f;
        for (int pos = bid; pos < Len; pos += nb) {{
            sdot[tid] = 0.0f;
            for (int j = tid; j < KV_local; j += blockDim.x) sdot[tid] += b2f(p->c_kv[pos * KV_local + j]) * b2f(p->ws[OFF_TB + j]);
            __syncthreads();
            for (int s = blockDim.x / 2; s > 0; s >>= 1) {{
                if (tid < s) sdot[tid] += sdot[tid + s];
                __syncthreads();
            }}
            float score = sdot[0] * {_(1.0 / math.sqrt(QN + QR))}f;
            score += b2f(p->ws[OFF_TA + QN + tid]) * 0.0f; // dummy keep q rope? no
            sdot[tid] = 0.0f;
            for (int j = tid; j < QR_local; j += blockDim.x) sdot[tid] += b2f(p->k_rope[pos * QR_local + j]) * b2f(p->ws[OFF_TA + QN + j]);
            __syncthreads();
            for (int s = blockDim.x / 2; s > 0; s >>= 1) {{
                if (tid < s) sdot[tid] += sdot[tid + s];
                __syncthreads();
            }}
            score += sdot[0] * {_(1.0 / math.sqrt(QN + QR))}f;
            if (score > local_max) local_max = score;
        }}
        sdot[tid] = local_max; __syncthreads();
        for (int s = blockDim.x / 2; s > 0; s >>= 1) {{
            if (tid < s) sdot[tid] = fmaxf(sdot[tid], sdot[tid + s]);
            __syncthreads();
        }}
        if (tid == 0) atomicMaxFloat(p->fws + FWS_MAX, sdot[0]);
    }}
    barrier(p->sync, ph++);
    {{
        const int Len = L + 1;
        const int KV_local = KV;
        const int QR_local = QR;
        __shared__ float sdot[BLOCK_SIZE];
        float local_sum = 0.0f;
        for (int pos = bid; pos < Len; pos += nb) {{
            sdot[tid] = 0.0f;
            for (int j = tid; j < KV_local; j += blockDim.x) sdot[tid] += b2f(p->c_kv[pos * KV_local + j]) * b2f(p->ws[OFF_TB + j]);
            __syncthreads();
            for (int s = blockDim.x / 2; s > 0; s >>= 1) {{
                if (tid < s) sdot[tid] += sdot[tid + s];
                __syncthreads();
            }}
            float score = sdot[0] * {_(1.0 / math.sqrt(QN + QR))}f;
            sdot[tid] = 0.0f;
            for (int j = tid; j < QR_local; j += blockDim.x) sdot[tid] += b2f(p->k_rope[pos * QR_local + j]) * b2f(p->ws[OFF_TA + QN + j]);
            __syncthreads();
            for (int s = blockDim.x / 2; s > 0; s >>= 1) {{
                if (tid < s) sdot[tid] += sdot[tid + s];
                __syncthreads();
            }}
            score += sdot[0] * {_(1.0 / math.sqrt(QN + QR))}f;
            local_sum += expf(score - p->fws[FWS_MAX]);
        }}
        sdot[tid] = local_sum; __syncthreads();
        for (int s = blockDim.x / 2; s > 0; s >>= 1) {{
            if (tid < s) sdot[tid] += sdot[tid + s];
            __syncthreads();
        }}
        if (tid == 0) atomicAdd(p->fws + FWS_SUM, sdot[0]);
    }}
    barrier(p->sync, ph++);
    {{
        const int Len = L + 1;
        const int KV_local = KV;
        const int QR_local = QR;
        __shared__ float sdot[BLOCK_SIZE];
        __shared__ float zsh[KV];
        for (int j = tid; j < KV_local; j += blockDim.x) zsh[j] = 0.0f;
        __syncthreads();
        for (int pos = bid; pos < Len; pos += nb) {{
            sdot[tid] = 0.0f;
            for (int j = tid; j < KV_local; j += blockDim.x) sdot[tid] += b2f(p->c_kv[pos * KV_local + j]) * b2f(p->ws[OFF_TB + j]);
            __syncthreads();
            for (int s = blockDim.x / 2; s > 0; s >>= 1) {{
                if (tid < s) sdot[tid] += sdot[tid + s];
                __syncthreads();
            }}
            float score = sdot[0] * {_(1.0 / math.sqrt(QN + QR))}f;
            sdot[tid] = 0.0f;
            for (int j = tid; j < QR_local; j += blockDim.x) sdot[tid] += b2f(p->k_rope[pos * QR_local + j]) * b2f(p->ws[OFF_TA + QN + j]);
            __syncthreads();
            for (int s = blockDim.x / 2; s > 0; s >>= 1) {{
                if (tid < s) sdot[tid] += sdot[tid + s];
                __syncthreads();
            }}
            score += sdot[0] * {_(1.0 / math.sqrt(QN + QR))}f;
            float prob = expf(score - p->fws[FWS_MAX]) / p->fws[FWS_SUM];
            for (int j = tid; j < KV_local; j += blockDim.x) zsh[j] += prob * b2f(p->c_kv[pos * KV_local + j]);
        }}
        __syncthreads();
        for (int j = bid * blockDim.x + tid; j < KV_local; j += nb * blockDim.x) {{
            atomicAdd(p->fws + FWS_Z + j, zsh[j]);
        }}
    }}
    barrier(p->sync, ph++);
    for (int j = bid * blockDim.x + tid; j < KV; j += nb * blockDim.x)
        p->ws[OFF_TB + j] = f2b(p->fws[FWS_Z + j]);
    __syncthreads();
    barrier(p->sync, ph++);
    quant_gemv(p->attn_w, p->attn_s, p->attn_z, p->ws + OFF_TB, p->ws + OFF_TA, KV, C, AOFF_MKVB{b}, ASOFF_MKVB{b}, AZOFF_MKVB{b}, p, 0);
    barrier(p->sync, ph++);
    quant_gemv(p->attn_w, p->attn_s, p->attn_z, p->ws + OFF_TA, p->ws + OFF_TA, C, D, AOFF_MO{b}, ASOFF_MO{b}, AZOFF_MO{b}, p, 0);
    barrier(p->sync, ph++);
'''

        body += f'''
    for (int i = bid * blockDim.x + tid; i < D; i += nb * blockDim.x) {{
        p->ws[nxt + i] = f2b(b2f(p->ws[cur + i]) + b2f(p->ws[OFF_TA + i]));
    }}
    barrier(p->sync, ph++);

    if (bid == 0) p->fws[FWS_RMS] = 0.0f;
    barrier(p->sync, ph++);
    {{
        float partial = 0.0f;
        for (int i = bid * blockDim.x + tid; i < D; i += nb * blockDim.x) {{
            float v = b2f(p->ws[nxt + i]);
            partial += v * v;
        }}
        __shared__ float sd[BLOCK_SIZE];
        sd[tid] = partial; __syncthreads();
        for (int s = blockDim.x / 2; s > 0; s >>= 1) {{
            if (tid < s) sd[tid] += sd[tid + s];
            __syncthreads();
        }}
        if (tid == 0) atomicAdd(p->fws + FWS_RMS, sd[0] / (float)D);
    }}
    barrier(p->sync, ph++);
    {{
        float invrms = rsqrtf(p->fws[FWS_RMS] + 1e-6f);
        for (int i = bid * blockDim.x + tid; i < D; i += nb * blockDim.x) {{
            p->ws[OFF_XN + i] = f2b(b2f(p->ws[nxt + i]) * invrms * b2f(p->params[{_(mnorm_off)} + i]));
        }}
    }}
    barrier(p->sync, ph++);
'''
        router_off = info["params_off"][f"ROUTER{b}"]
        body += f'''
    bf16_gemv(p->params + {_(router_off)}, p->ws + OFF_XN, p->ws + OFF_TA, D, E, 0, ph, p);
    barrier(p->sync, ph++);
    if (bid == 0) {{
        float probs[E];
        for (int e = 0; e < E; ++e) probs[e] = b2f(p->ws[OFF_TA + e]);
        float maxp = probs[0];
        for (int e = 1; e < E; ++e) if (probs[e] > maxp) maxp = probs[e];
        float sump = 0.0f;
        for (int e = 0; e < E; ++e) {{ probs[e] = expf(probs[e] - maxp); sump += probs[e]; }}
        for (int e = 0; e < E; ++e) probs[e] /= sump;
        for (int j = 0; j < KACT; ++j) {{
            int best = 0;
            for (int e = 1; e < E; ++e) if (probs[e] > probs[best]) best = e;
            p->sync[TOPK_I_OFF + j] = best;
            p->fws[FWS_TMP + E + j] = probs[best];
            probs[best] = -1.0f;
        }}
        float wsum = 0.0f;
        for (int j = 0; j < KACT; ++j) wsum += p->fws[FWS_TMP + E + j];
        for (int j = 0; j < KACT; ++j) p->fws[FWS_TMP + E + j] = p->fws[FWS_TMP + E + j] / wsum * RSCALE;
    }}
    barrier(p->sync, ph++);
'''
        body += f'''
    for (int eidx = 0; eidx < KACT; ++eidx) {{
        int ex = p->sync[TOPK_I_OFF + eidx];
        float ew = p->fws[FWS_TMP + E + eidx];
        quant_gemv_expert(p->moe_gate_w, p->moe_gate_s, p->moe_gate_z, p->ws + OFF_XN, p->ws + OFF_TB + 0,
                          MOE_GATE_K, MOE_GATE_N, MOE_GATE_B{b}_WOFF, MOE_GATE_B{b}_SOFF, MOE_GATE_B{b}_ZOFF,
                          ex, MOE_GATE_EXBYTE, MOE_GATE_EXSEL, p);
        quant_gemv_expert(p->moe_up_w, p->moe_up_s, p->moe_up_z, p->ws + OFF_XN, p->ws + OFF_TB + M,
                          MOE_UP_K, MOE_UP_N, MOE_UP_B{b}_WOFF, MOE_UP_B{b}_SOFF, MOE_UP_B{b}_ZOFF,
                          ex, MOE_UP_EXBYTE, MOE_UP_EXSEL, p);
        for (int m = bid * blockDim.x + tid; m < M; m += nb * blockDim.x) {{
            float g_ = silu(b2f(p->ws[OFF_TB + m]));
            float u_ = b2f(p->ws[OFF_TB + M + m]);
            p->ws[OFF_TB + m] = f2b(g_ * u_);
        }}
        __syncthreads();
        quant_gemv_expert(p->moe_down_w, p->moe_down_s, p->moe_down_z, p->ws + OFF_TB, p->ws + OFF_TB,
                          MOE_DOWN_K, MOE_DOWN_N, MOE_DOWN_B{b}_WOFF, MOE_DOWN_B{b}_SOFF, MOE_DOWN_B{b}_ZOFF,
                          ex, MOE_DOWN_EXBYTE, MOE_DOWN_EXSEL, p);
        for (int i = bid * blockDim.x + tid; i < D; i += nb * blockDim.x) {{
            p->ws[nxt + i] = f2b(b2f(p->ws[nxt + i]) + ew * b2f(p->ws[OFF_TB + i]));
        }}
        __syncthreads();
    }}
    for (int eidx = 0; eidx < SHARED; ++eidx) {{
        int ex = eidx;
        quant_gemv_expert(p->moe_sg_w, p->moe_sg_s, p->moe_sg_z, p->ws + OFF_XN, p->ws + OFF_TB + 0,
                          MOE_SGATE_K, MOE_SGATE_N, MOE_SGATE_B{b}_WOFF, MOE_SGATE_B{b}_SOFF, MOE_SGATE_B{b}_ZOFF,
                          ex, MOE_SGATE_EXBYTE, MOE_SGATE_EXSEL, p);
        quant_gemv_expert(p->moe_su_w, p->moe_su_s, p->moe_su_z, p->ws + OFF_XN, p->ws + OFF_TB + M,
                          MOE_S_UP_K, MOE_S_UP_N, MOE_S_UP_B{b}_WOFF, MOE_S_UP_B{b}_SOFF, MOE_S_UP_B{b}_ZOFF,
                          ex, MOE_S_UP_EXBYTE, MOE_S_UP_EXSEL, p);
        for (int m = bid * blockDim.x + tid; m < M; m += nb * blockDim.x) {{
            float g_ = silu(b2f(p->ws[OFF_TB + m]));
            float u_ = b2f(p->ws[OFF_TB + M + m]);
            p->ws[OFF_TB + m] = f2b(g_ * u_);
        }}
        __syncthreads();
        quant_gemv_expert(p->moe_sd_w, p->moe_sd_s, p->moe_sd_z, p->ws + OFF_TB, p->ws + OFF_TB,
                          MOE_S_DOWN_K, MOE_S_DOWN_N, MOE_S_DOWN_B{b}_WOFF, MOE_S_DOWN_B{b}_SOFF, MOE_S_DOWN_B{b}_ZOFF,
                          ex, MOE_S_DOWN_EXBYTE, MOE_S_DOWN_EXSEL, p);
        for (int i = bid * blockDim.x + tid; i < D; i += nb * blockDim.x) {{
            p->ws[nxt + i] = f2b(b2f(p->ws[nxt + i]) + b2f(p->ws[OFF_TB + i]));
        }}
        __syncthreads();
    }}
    barrier(p->sync, ph++);
    {{ int tmp = cur; cur = nxt; nxt = tmp; }}
'''

    body += f'''
}}
'''
    return body

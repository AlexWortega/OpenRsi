"""Fixed WB2 eval harness. Imports the agent's model.py (must define
train_and_predict(Xtr,Ytr,Xte,meta,time_budget_s,device)->Yte_pred), runs it under a
fixed compute budget on one GPU, scores area-weighted RMSE + persistence skill.

#2 (stolen from AIDE k_fold_validation): OPENRSI_WB_REPEATS=R repeats train+eval with
different seeds and reports the MEAN skill (robust fitness) + std, so RSI selection is
not fooled by single-run training noise. Prints one JSON line."""
import sys, json, time, importlib.util, numpy as np, os
def load(npz):
    d = np.load(npz); return {k: d[k] for k in d.files}
def wrmse_ch(pred, true, w):
    wse = (pred - true) ** 2 * w[None, None, :, None]
    return np.sqrt(wse.mean(axis=(0, 2, 3)))  # (C,)
def main():
    model_dir = sys.argv[1]; budget_s = float(sys.argv[2]); gpu = sys.argv[3] if len(sys.argv) > 3 else "0"
    repeats = int(os.environ.get("OPENRSI_WB_REPEATS", "1"))
    os.environ["CUDA_VISIBLE_DEVICES"] = gpu
    import torch
    d = load("/mnt/storage/wb2/data/wb2_72h.npz")
    Xtr, Ytr, Xte, Yte, w = d["Xtr"], d["Ytr"], d["Xte"], d["Yte"], d["w"]
    meta = {"mean": d["mean"], "std": d["std"], "lat": d["lat"], "lon": d["lon"], "channels": list(d["channels"])}
    spec = importlib.util.spec_from_file_location("model", os.path.join(model_dir, "model.py"))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    pers = wrmse_ch(Xte, Yte, w)  # persistence baseline (deterministic)

    skills, rz, rt, tsecs = [], [], [], []
    for r in range(repeats):
        torch.manual_seed(1234 + r); np.random.seed(1234 + r)
        t0 = time.time()
        pred = np.asarray(m.train_and_predict(Xtr.copy(), Ytr.copy(), Xte.copy(), meta, budget_s, device), dtype="float32")
        tsecs.append(time.time() - t0)
        assert pred.shape == Yte.shape, f"pred shape {pred.shape} != {Yte.shape}"
        assert np.isfinite(pred).all(), "non-finite predictions"
        rmse = wrmse_ch(pred, Yte, w)
        skills.append(1.0 - float(np.mean(rmse / pers))); rz.append(float(rmse[0])); rt.append(float(rmse[1]))

    sk = np.array(skills)
    print(json.dumps({
        "ok": True, "skill": float(sk.mean()), "skill_std": float(sk.std(ddof=1)) if repeats > 1 else 0.0,
        "repeats": repeats, "skills": [round(s, 4) for s in skills],
        "rmse_z500": float(np.mean(rz)), "rmse_t850": float(np.mean(rt)),
        "pers_z500": float(pers[0]), "pers_t850": float(pers[1]),
        "train_s": round(float(np.mean(tsecs)), 1), "budget_s": budget_s,
        "overran": float(np.mean(tsecs)) > budget_s * 1.2}))
if __name__ == "__main__":
    try: main()
    except Exception as e:
        import traceback; print(json.dumps({"ok": False, "error": f"{type(e).__name__}: {e}", "trace": traceback.format_exc()[-800:]}))

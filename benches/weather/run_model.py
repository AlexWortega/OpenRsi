"""Fixed WB2 eval harness. Imports the agent's model.py (must define
train_and_predict(Xtr,Ytr,Xte,meta,time_budget_s,device)->Yte_pred), runs it under a
fixed compute budget on one GPU, scores area-weighted RMSE + persistence skill.
Prints one JSON line."""
import sys, json, time, importlib.util, numpy as np, os
def load(npz):
    d = np.load(npz); return {k: d[k] for k in d.files}
def wrmse_ch(pred, true, w):
    wse = (pred - true) ** 2 * w[None, None, :, None]
    return np.sqrt(wse.mean(axis=(0, 2, 3)))  # (C,)
def main():
    model_dir = sys.argv[1]; budget_s = float(sys.argv[2]); gpu = sys.argv[3] if len(sys.argv) > 3 else "0"
    os.environ["CUDA_VISIBLE_DEVICES"] = gpu
    import torch
    d = load("/mnt/storage/wb2/data/wb2_72h.npz")
    Xtr, Ytr, Xte, Yte, w = d["Xtr"], d["Ytr"], d["Xte"], d["Yte"], d["w"]
    meta = {"mean": d["mean"], "std": d["std"], "lat": d["lat"], "lon": d["lon"], "channels": list(d["channels"])}
    spec = importlib.util.spec_from_file_location("model", os.path.join(model_dir, "model.py"))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    t0 = time.time()
    pred = m.train_and_predict(Xtr.copy(), Ytr.copy(), Xte.copy(), meta, budget_s, device)
    train_s = time.time() - t0
    pred = np.asarray(pred, dtype="float32")
    assert pred.shape == Yte.shape, f"pred shape {pred.shape} != {Yte.shape}"
    assert np.isfinite(pred).all(), "non-finite predictions"
    rmse = wrmse_ch(pred, Yte, w)
    pers = wrmse_ch(Xte, Yte, w)  # persistence baseline
    skill = 1.0 - float(np.mean(rmse / pers))  # persistence skill score (>0 beats persistence)
    print(json.dumps({"ok": True, "skill": skill, "rmse_z500": float(rmse[0]), "rmse_t850": float(rmse[1]),
                      "pers_z500": float(pers[0]), "pers_t850": float(pers[1]),
                      "train_s": round(train_s, 1), "budget_s": budget_s, "overran": train_s > budget_s * 1.2}))
if __name__ == "__main__":
    try: main()
    except Exception as e:
        import traceback; print(json.dumps({"ok": False, "error": f"{type(e).__name__}: {e}", "trace": traceback.format_exc()[-800:]}))

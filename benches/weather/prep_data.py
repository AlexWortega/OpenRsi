"""Prep a small WeatherBench2 64x32 ERA5 subset: 72h z500/t850 forecast.
X=state at init (00/12 UTC), Y=state at init+72h. Arrays are (N,C,lat=32,lon=64)."""
import numpy as np, xarray as xr, os
OUT = "/mnt/storage/wb2/data"
URL = "gs://weatherbench2/datasets/era5/1959-2022-6h-64x32_equiangular_conservative.zarr"
TRAIN_YEARS = slice("2017-01-01", "2019-12-31"); TEST_YEARS = slice("2020-01-01", "2020-12-31")
LEAD_STEPS = 12  # 12 x 6h = 72h
print("opening zarr ...", flush=True)
ds = xr.open_zarr(URL, storage_options={"token": "anon"}, chunks=None)
z = ds["geopotential"].sel(level=500); t = ds["temperature"].sel(level=850)
def grab(years):
    zz = z.sel(time=years).transpose("time","latitude","longitude").load().values.astype("float32")
    tt = t.sel(time=years).transpose("time","latitude","longitude").load().values.astype("float32")
    return np.stack([zz, tt], axis=1), z.sel(time=years).time.values   # (T,2,32,64)
print("loading train ...", flush=True); Xtr_full, ttr = grab(TRAIN_YEARS)
print("loading test  ...", flush=True); Xte_full, tte = grab(TEST_YEARS)
lat = ds.latitude.values.astype("float32"); lon = ds.longitude.values.astype("float32")
def pairs(full, times):
    hours = times.astype("datetime64[h]").astype(int) % 24
    idx = np.where((hours == 0) | (hours == 12))[0]; idx = idx[idx + LEAD_STEPS < full.shape[0]]
    return full[idx], full[idx + LEAD_STEPS]
Xtr, Ytr = pairs(Xtr_full, ttr); Xte, Yte = pairs(Xte_full, tte)
mean = Xtr.mean(axis=(0,2,3), keepdims=True); std = Xtr.std(axis=(0,2,3), keepdims=True)
w = np.cos(np.deg2rad(lat)); w = (w / w.mean()).astype("float32")   # (32,) lat weights
def wrmse(pred, true):
    wse = (pred - true) ** 2 * w[None, None, :, None]
    per = np.sqrt(wse.mean(axis=(0,2,3))); return per, float(per.mean())
pers_ch, pers = wrmse(Xte, Yte)
clim = Ytr.mean(axis=0, keepdims=True); clim_ch, climv = wrmse(np.repeat(clim, len(Yte), 0), Yte)
np.savez_compressed(os.path.join(OUT, "wb2_72h.npz"), Xtr=Xtr, Ytr=Ytr, Xte=Xte, Yte=Yte,
    lat=lat, lon=lon, w=w, mean=mean.astype("float32"), std=std.astype("float32"),
    channels=np.array(["z500","t850"]))
print(f"SAVED train={Xtr.shape} test={Xte.shape}", flush=True)
print(f"BASELINE persistence wRMSE: z500={pers_ch[0]:.2f} t850={pers_ch[1]:.3f} mean={pers:.3f}", flush=True)
print(f"BASELINE climatology wRMSE: z500={clim_ch[0]:.2f} t850={clim_ch[1]:.3f} mean={climv:.3f}", flush=True)

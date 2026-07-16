#!/usr/bin/env python3
"""
Minimal RunPod pod lifecycle helper (REST v1) for the KernelBench GPU eval.

  python runpod_pod.py create        # provision an L40S pod
  python runpod_pod.py status        # list pods + ssh endpoint
  python runpod_pod.py wait <id>     # poll until an SSH endpoint is ready, print it
  python runpod_pod.py rm <id>       # terminate a pod

Reads RUNPOD_API_KEY from env.
"""
import json
import os
import sys
import time
import urllib.request

BASE = "https://rest.runpod.io/v1"
KEY = os.environ["RUNPOD_API_KEY"]
IMAGE = os.environ.get("RUNPOD_IMAGE", "runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04")
# KernelBench fast_p target = the RTX PRO 6000 (Blackwell) — the same class of card as
# the 18.45x mega record. Override with RUNPOD_GPU for other hardware.
GPU = os.environ.get("RUNPOD_GPU", "NVIDIA RTX PRO 6000 Blackwell Workstation Edition")


def api(path: str, method="GET", body=None):
    req = urllib.request.Request(
        BASE + path,
        data=json.dumps(body).encode() if body is not None else None,
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
        method=method,
    )
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            txt = r.read().decode()
            return json.loads(txt) if txt.strip() else {}
    except urllib.error.HTTPError as e:
        return {"_httperror": e.code, "_body": e.read().decode()[:800]}


def pubkey() -> str:
    for p in (os.path.expanduser("~/.ssh/id_ed25519.pub"), os.path.expanduser("~/.ssh/id_rsa.pub")):
        if os.path.exists(p):
            return open(p).read().strip()
    raise SystemExit("no ssh pubkey found")


def create():
    body = {
        "name": "openrsi-kernelbench",
        "imageName": IMAGE,
        "gpuTypeIds": [GPU],
        "gpuCount": 1,
        "cloudType": "COMMUNITY",
        "containerDiskInGb": 60,
        "volumeInGb": 0,
        "ports": ["22/tcp"],
        "env": {"PUBLIC_KEY": pubkey()},
    }
    print(json.dumps(api("/pods", "POST", body), indent=2))


def _ssh_of(pod: dict):
    for p in (pod.get("portMappings") or {}), :
        pass
    # REST returns runtime.ports once running
    rt = pod.get("runtime") or {}
    for port in (rt.get("ports") or []):
        if port.get("privatePort") == 22 and port.get("isIpPublic"):
            return port.get("ip"), port.get("publicPort")
    # some responses expose publicIp + portMappings
    pm = pod.get("portMappings") or {}
    if pod.get("publicIp") and pm.get("22"):
        return pod["publicIp"], pm["22"]
    return None, None


def status():
    pods = api("/pods")
    if isinstance(pods, dict) and pods.get("_httperror"):
        print(pods); return
    for p in pods if isinstance(pods, list) else pods.get("pods", []):
        ip, port = _ssh_of(p)
        print(f"{p['id']} {p.get('name')} status={p.get('desiredStatus')} gpu={p.get('machine',{}).get('gpuTypeId')}"
              + (f"  ssh: root@{ip} -p {port}" if ip else "  (ssh not ready)"))


def wait(pid: str):
    for _ in range(60):
        p = api(f"/pods/{pid}")
        ip, port = _ssh_of(p)
        if ip:
            print(f"READY root@{ip} -p {port}")
            return
        time.sleep(10)
    print("TIMEOUT waiting for ssh endpoint")
    print(json.dumps(api(f"/pods/{pid}"), indent=2)[:1500])


def rm(pid: str):
    print(json.dumps(api(f"/pods/{pid}", "DELETE"), indent=2))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    {"create": create, "status": status,
     "wait": lambda: wait(sys.argv[2]), "rm": lambda: rm(sys.argv[2])}.get(cmd, lambda: print(__doc__))()

#!/usr/bin/env python3
"""Deterministic finite breaker for sparse butterfly compiler event validity.

Independently replays every raw physical stage emitted by
``compile_formula_sparse``.  It checks lane ranges, scheduled XOR dimensions,
WAIT stages, least-free-lane choice, swaps through empty and occupied lanes,
movement of later-reused duplication bases, NAND consumption, padding, and
cleanup.  Symbolic values are collision-free interned NAND DAG nodes rather
than sampled Boolean values.

The scope is finite: adversarial comb/balanced cases through 8192 leaves and a
fixed-seed fuzz corpus.  This is not a universal scheduler/compiler theorem.
"""
from __future__ import annotations
import json, random
from pathlib import Path

from verify_u0a_sparse_program_stream import compile_formula_sparse, gate_mode_at


def parse_formula(f):
    """Independent postorder tokenization matching the public token names."""
    leaves, gates, results = [], [], []
    work = [(f, 0)]
    while work:
        x, exit_ = work.pop()
        if isinstance(x, int):
            assert x >= 0
            t = f"leaf:{len(leaves)}"
            leaves.append((t, x)); results.append(t)
        else:
            assert type(x) is tuple and len(x) == 2
            if not exit_:
                work.extend(((x, 1), (x[1], 0), (x[0], 0)))
            else:
                r = results.pop(); l = results.pop()
                t = f"gate:{len(gates)}"
                gates.append((t, l, r)); results.append(t)
    assert len(results) == 1
    return leaves, gates, results[0]


def audit(formula, *, width=None, assert_bit=1):
    p = compile_formula_sparse(formula, width=width, assert_bit=assert_bit)
    leaves, gates, root = parse_formula(formula)
    w, d = p["width"], p["gate_stages"]
    logw = w.bit_length() - 1
    assert w >= max(4, len(leaves)) and w & (w-1) == 0
    assert 0 <= p["output_lane"] < w and p["cleanup"]["stage"] == d

    # Strict coordinates and mode domain; build actual raw stage records.
    ovs = p["raw_gate_overrides"]
    assert all(1 <= s <= p["raw_stage_count"] < d and 0 <= a < w
               and m in {"COPY_B", "ZERO", "NAND"} for s,a,m in ovs)
    assert all(ovs[i][:2] < ovs[i+1][:2] for i in range(len(ovs)-1))
    bystage = {}
    for s,a,m in ovs: bystage.setdefault(s, []).append((a,m))

    used = sorted({v for _,v in leaves})
    occ = {v: [] for v in used}
    for t,v in leaves: occ[v].append(t)
    lane_tok = [None]*w; tok_lane={}; tok_sem={}
    # Collision-free semantic algebra: variables and ZERO are atoms; NAND
    # pairs are interned by exact integer pair equality.
    ZERO = 0
    var_sem = {v:i+1 for i,v in enumerate(used)}
    pair_sem = {}; next_sem = len(used)+1
    def nand_id(a,b):
        nonlocal next_sem
        z=pair_sem.get((a,b))
        if z is None:
            z=next_sem; next_sem += 1; pair_sem[(a,b)] = z
        return z
    phys=[ZERO]*w
    source_lane={}
    for lane,v in enumerate(used):
        t=occ[v][0]; source_lane[v]=lane
        lane_tok[lane]=t; tok_lane[t]=lane; tok_sem[t]=var_sem[v]; phys[lane]=var_sem[v]
    for t,v in leaves: tok_sem[t]=var_sem[v]
    assert p["source_lane"] == source_lane
    assert p["source_overrides"] == tuple((i,"FREE") for i in range(len(used)))

    stage=0; stats={"wait":0,"swap":0,"swap_occupied":0,"swap_empty":0,
                    "duplicate":0,"base_moved":0,"nand":0}
    initial_base_lane={v:source_lane[v] for v in used}

    def emit(dim, expected, kind):
        # All unspecified lanes use COPY_A.  Thus exact equality of the sparse
        # override row proves that every other symbolic lane is unchanged; we
        # update only the event endpoints below.
        nonlocal stage
        while ((stage)//2)%logw != dim:
            stage += 1
            assert bystage.get(stage,[]) == [], ("non-WAIT",stage,bystage.get(stage))
            stats["wait"] += 1
        stage += 1
        assert ((stage-1)//2)%logw == dim
        assert bystage.get(stage,[]) == sorted(expected), (kind,stage,expected,bystage.get(stage))

    def swap(a,b):
        assert 0<=a<w and 0<=b<w and a!=b
        x=a^b; assert x and x&(x-1)==0; dim=x.bit_length()-1
        old_a,old_b=phys[a],phys[b]; ta,tb=lane_tok[a],lane_tok[b]
        emit(dim, [(a,"COPY_B"),(b,"COPY_B")], "SWAP")
        phys[a],phys[b]=old_b,old_a
        lane_tok[a],lane_tok[b]=tb,ta
        if ta is not None: tok_lane[ta]=b
        if tb is not None: tok_lane[tb]=a
        stats["swap"] += 1
        if ta is not None and tb is not None: stats["swap_occupied"] += 1
        else: stats["swap_empty"] += 1

    for v in used:
        base=occ[v][0]
        for new in occ[v][1:]:
            a=tok_lane[base]
            if a != initial_base_lane[v]: stats["base_moved"] += 1
            free=min(i for i,t in enumerate(lane_tok) if t is None)
            assert 0<=free<w and lane_tok[free] is None and a!=free
            dims=[q for q in range(logw) if ((a^free)>>q)&1]
            assert dims
            for dim in dims[:-1]:
                b=a^(1<<dim); swap(a,b); a=b
            dim=dims[-1]; assert a^free == 1<<dim
            old_a=phys[a]
            emit(dim, [(free,"COPY_B")], "DUPLICATE")
            phys[free]=old_a
            lane_tok[free]=new; tok_lane[new]=free
            assert phys[free]==tok_sem[new]==tok_sem[base]
            stats["duplicate"] += 1

    for out,left,right in gates:
        a,b=tok_lane[left],tok_lane[right]
        assert 0<=a<w and 0<=b<w and a!=b
        dims=[q for q in range(logw) if ((a^b)>>q)&1]; assert dims
        for dim in dims[:-1]:
            c=a^(1<<dim); swap(a,c); a=c
        dim=dims[-1]; assert a^b == 1<<dim
        emit(dim, [(a,"NAND"),(b,"ZERO")], "NAND")
        sem=nand_id(tok_sem[left],tok_sem[right]); tok_sem[out]=sem
        phys[a],phys[b]=nand_id(phys[a],phys[b]),ZERO
        assert phys[a]==sem and phys[b]==ZERO
        del tok_lane[left]; del tok_lane[right]
        lane_tok[a]=out; lane_tok[b]=None; tok_lane[out]=a
        stats["nand"] += 1

    assert stage == p["raw_stage_count"], (stage,p["raw_stage_count"])
    assert set(tok_lane)=={root} and tok_lane[root]==p["output_lane"]
    assert phys[p["output_lane"]] == tok_sem[root]
    # Padding is exactly identity and has no hidden raw overrides.
    assert p["padding"] == {"start_stage":stage+1,"count":d-stage-1,
                             "default_mode":"COPY_A"}
    assert not any(s > stage for s in bystage)
    if stage+1 < d:
        for s in {stage+1, (stage+d)//2, d-1}:
            for a in {0, p["output_lane"], w-1}:
                assert gate_mode_at(p,s,a)=="COPY_A"
    # Apply cleanup through public lookup: root survives and every other lane is zero.
    old_root=phys[p["output_lane"]]
    phys=[ZERO]*w
    phys[p["output_lane"]]=old_root
    assert phys[p["output_lane"]] == tok_sem[root]
    assert all(x==ZERO for a,x in enumerate(phys) if a!=p["output_lane"])
    assert p["cleanup"] == {"stage":d,"default_mode":"ZERO",
                             "overrides":((p["output_lane"],"COPY_A"),)}
    assert p["output_overrides"] == (((p["output_lane"],assert_bit),) if assert_bit else ())
    assert p["event_counts"] == {"WAIT":stats["wait"],"SWAP":stats["swap"],
                                  "DUPLICATE":stats["duplicate"],"NAND":stats["nand"]}
    stats["leaves"]=len(leaves); stats["width"]=w; stats["raw_stages"]=stage
    stats["budget"]=d
    return stats


def comb(n, right=False):
    f=0
    for i in range(1,n): f=((i if i%5 else 0),f) if right else (f,(i if i%5 else 0))
    return f

def balanced(vals):
    a=list(vals)
    while len(a)>1:
        b=[]; it=iter(a)
        for x in it:
            try: y=next(it); b.append((x,y))
            except StopIteration: b.append(x)
        a=b
    return a[0]

def random_formula(rng,n,var_mode):
    forest=[]
    for i in range(n):
        if var_mode==0: v=0
        elif var_mode==1: v=i
        elif var_mode==2: v=i%7
        else: v=rng.randrange(max(1,int(n**0.5)))
        forest.append(v)
    while len(forest)>1:
        i=rng.randrange(len(forest)); x=forest.pop(i)
        j=rng.randrange(len(forest)); y=forest.pop(j)
        forest.append((x,y) if rng.randrange(2) else (y,x))
    return forest[0]

def main():
    totals={k:0 for k in ("cases","leaves","raw_stages","swap","swap_occupied","swap_empty","duplicate","base_moved","nand")}
    max_ratio=(0,None)
    def run(f,label,width=None):
        nonlocal max_ratio
        for bit in (0,1):
            s=audit(f,width=width,assert_bit=bit)
            totals["cases"]+=1
            for k in totals:
                if k!="cases": totals[k]+=s.get(k,0)
            ratio=s["raw_stages"]/s["budget"]
            if ratio>max_ratio[0]: max_ratio=(ratio,(label,s["leaves"],s["width"],s["raw_stages"],s["budget"]))
    # Boundary widths, both comb orientations, all-distinct/repeated mix.
    for n in list(range(1,34))+[47,63,64,65,97,127,128,129]:
        run(comb(n,False),f"left-comb-{n}")
        run(comb(n,True),f"right-comb-{n}")
        run(balanced([i%11 for i in range(n)]),f"balanced-{n}")
    # Bounded skew/fuzz corpus.  Larger snapshot certificates have a separate
    # resource audit; do not let this semantic verifier exhaust host memory.
    rng=random.Random(0xC0FFEE)
    for case in range(120):
        n=1+rng.randrange(1 << rng.randrange(0,7))
        run(random_formula(rng,n,case%4),f"fuzz-{case}")
    assert totals["swap_occupied"]>0 and totals["swap_empty"]>0
    assert totals["base_moved"]>0 and totals["duplicate"]>0
    out={"status":"PASS","scope":"finite deterministic symbolic event replay",
         "totals":totals,"largest_leaves":129,"max_raw_stage_budget_ratio":max_ratio,
         "coverage":{"occupied_path_swaps":totals["swap_occupied"],
                     "empty_path_swaps":totals["swap_empty"],
                     "duplicate_calls_after_base_moved":totals["base_moved"]}}
    print("SPARSE_EVENT_VALIDITY_BREAKER_OK "+json.dumps(out,sort_keys=True,separators=(",",":")))

if __name__ == "__main__": main()

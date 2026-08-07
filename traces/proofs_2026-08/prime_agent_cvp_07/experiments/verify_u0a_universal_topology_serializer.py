#!/usr/bin/env python3
"""Finite verifier for the U0a candidate serializer.

This is deliberately only a finite construction/audit at widths 8, 16, 32.
It emits the complete sparse integer matrices C and D=[I|-C].  It does not
claim universality, CVP soundness, a class exclusion, or a gap.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path

WIDTHS = (8, 16, 32)
GATE_MODES = ("COPY_A", "COPY_B", "NAND", "ZERO", "ONE")
SOURCE_MODES = ("FREE", "FIX0", "FIX1")
EXPECTED_FILE_SHA256 = {
    8: "9d8e92513da40159823453eb18259136575abfa30eef3446d91c952c571b920b",
    16: "82eb62256d3d485bef91b2b68144de1b43139dfb0e7fdd6bf596d5f1e9515d01",
    32: "b0cd6e7c807b6ee08e5d9922fbc4e4853b375b8da0f7ced9b1b3fe67ae6c5652",
}


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()


def sha(obj):
    return hashlib.sha256(canonical(obj)).hexdigest()


def gate_value(mode, a, b):
    if mode == "COPY_A": return a
    if mode == "COPY_B": return b
    if mode == "NAND": return 1 - a*b
    if mode == "ZERO": return 0
    if mode == "ONE": return 1
    raise ValueError(mode)


def legal_source(mode, bit):
    return mode == "FREE" or (mode == "FIX0" and bit == 0) or (mode == "FIX1" and bit == 1)


def make_factor(width, gate_stages=None):
    """Emit the fixed numerical topology for any power-of-two width and depth.

    With ``gate_stages=None`` this retains the three hash-frozen shallow
    artifacts.  A positive explicit depth repeats the same deterministic
    butterfly offset schedule and is used by the chain-depth verifier.
    """
    assert width >= 2 and width & (width-1) == 0
    logw = width.bit_length()-1
    stages = 2*logw + 2 if gate_stages is None else int(gate_stages)
    assert stages >= 1
    rows, cols = [], []
    rentries = []
    row_by_id = {}
    node_cols = {}

    def add_row(rid, kind, target_role, **meta):
        i = len(rows)
        assert rid not in row_by_id
        row_by_id[rid] = i
        rows.append({"index":i, "id":rid, "kind":kind,
                     "target_role":target_role, **meta})
        rentries.append(defaultdict(int))
        return i

    # Rows.  NORM rows are the explicit DROP guards.  A missing local
    # selector leaves a unit normalization residual.
    for s in range(stages+1):
        nk = "source" if s == 0 else "gate"
        for lane in range(width):
            add_row(f"norm:{s}:{lane}", "NORM_DROP_GUARD", "FIXED_ONE",
                    stage=s, lane=lane, node_kind=nk, drop_guard=True)
    for lane in range(width):
        for mode in SOURCE_MODES:
            add_row(f"srcprog:{lane}:{mode}", "SOURCE_PROGRAM", "PROGRAM_BIT",
                    stage=0, lane=lane, mode=mode)
    for s in range(1, stages+1):
        for lane in range(width):
            for mode in GATE_MODES:
                add_row(f"gateprog:{s}:{lane}:{mode}", "GATE_PROGRAM", "PROGRAM_BIT",
                        stage=s, lane=lane, mode=mode)
    edge_rows = {}
    for s in range(1, stages+1):
        off = 1 << (((s-1)//2) % logw)
        for lane in range(width):
            parents = {"A": lane, "B": lane ^ off}
            for port in ("A", "B"):
                ri = add_row(f"edge:{s}:{lane}:{port}", "EDGE_CONSISTENCY", "FIXED_ZERO",
                             stage=s, lane=lane, port=port,
                             parent_stage=s-1, parent_lane=parents[port], offset=off)
                edge_rows[(s,lane,port)] = ri
    # Growing dyadic separator checks are explicit redundant integer sums of
    # edge equations.  They are fixed by topology, not by a program.
    separator_specs = []
    for s in range(1, stages+1):
        for port in ("A", "B"):
            for q in range(1, logw+1):
                size = 1 << q
                for start in range(0, width, size):
                    ri = add_row(f"sep:{s}:{port}:{size}:{start}", "DYADIC_SEPARATOR", "FIXED_ZERO",
                                 stage=s, port=port, block_start=start, block_size=size,
                                 redundant_sum_of_edges=True)
                    separator_specs.append((ri, [(s,lane,port) for lane in range(start,start+size)]))
    for lane in range(width):
        add_row(f"output:{lane}", "OUTPUT_INTERFACE", "OUTPUT_BIT",
                stage=stages, lane=lane)

    def add_col(cid, kind, stage, lane, state):
        j=len(cols)
        cols.append({"index":j,"id":cid,"kind":kind,"stage":stage,"lane":lane,
                     "state":state,"physical_selector":True})
        node_cols.setdefault((stage,lane), []).append(j)
        rentries[row_by_id[f"norm:{stage}:{lane}"]][j] += 1
        return j

    # Source local-state columns.  FREE has two legal witness values; FIX0 and
    # FIX1 each have one.  This makes free versus pinned inputs target-programmable.
    for lane in range(width):
        for mode in SOURCE_MODES:
            for bit in (0,1):
                if not legal_source(mode,bit): continue
                j=add_col(f"src:{lane}:{mode}:{bit}", "SOURCE_SELECTOR", 0,lane,
                          {"mode":mode,"bit":bit})
                rentries[row_by_id[f"srcprog:{lane}:{mode}"]][j] += 1

    # Every gate mode has all four input combinations and its forced output.
    for s in range(1, stages+1):
        for lane in range(width):
            for mode in GATE_MODES:
                for a in (0,1):
                    for b in (0,1):
                        c=gate_value(mode,a,b)
                        j=add_col(f"gate:{s}:{lane}:{mode}:{a}{b}{c}", "GATE_SELECTOR",s,lane,
                                  {"mode":mode,"a":a,"b":b,"c":c})
                        rentries[row_by_id[f"gateprog:{s}:{lane}:{mode}"]][j] += 1

    # Put an explicit identity copy of every selector into the physical y
    # coordinates.  Thus the ROADMAP objective ||y-target_y||^2 charges z,
    # even though z is auxiliary in D(y,z)=0.  This blocks invisible C-kernel
    # moves in the constraint-only rows; it is not a soundness theorem.
    for j,col in enumerate(cols):
        ri=add_row(f"physical:{j}", "PHYSICAL_SELECTOR", "FIXED_ZERO",
                   selector_column=j, selector_id=col["id"], physical_coordinate=True)
        rentries[ri][j] = 1

    # Edge equations are child input minus producer output.
    def outbit(col):
        st=cols[col]["state"]
        return st["bit"] if cols[col]["kind"]=="SOURCE_SELECTOR" else st["c"]
    for s in range(1, stages+1):
        off=1 << (((s-1)//2)%logw)
        for lane in range(width):
            for port,parent_lane in (("A",lane),("B",lane^off)):
                ri=edge_rows[(s,lane,port)]
                key=port.lower()
                for j in node_cols[(s,lane)]: rentries[ri][j] += cols[j]["state"][key]
                for j in node_cols[(s-1,parent_lane)]: rentries[ri][j] -= outbit(j)
    # Materialize separator rows as exact sums of already materialized edges.
    for ri, edges in separator_specs:
        for e in edges:
            for j,v in rentries[edge_rows[e]].items(): rentries[ri][j] += v
    # Last-stage output interface.
    for lane in range(width):
        ri=row_by_id[f"output:{lane}"]
        for j in node_cols[(stages,lane)]: rentries[ri][j] += outbit(j)

    C=[]
    for i,d in enumerate(rentries):
        for j,v in sorted(d.items()):
            if v: C.append([i,j,v])
    m,k=len(rows),len(cols)
    D=[[i,i,1] for i in range(m)] + [[i,m+j,-v] for i,j,v in C]
    D.sort()
    topology=[]
    for s in range(1,stages+1):
        off=1 << (((s-1)//2)%logw)
        topology.append({"stage":s,"offset":off,
                         "parents":"A=(stage-1,lane), B=(stage-1,lane XOR offset)"})
    payload={
      "schema":"u0a-butterfly-nand-copy-factor-v1",
      "finite_claim_only":True,
      "width":width,"log2_width":logw,"gate_stages":stages,
      "semantics":{
        "source_modes":list(SOURCE_MODES),"gate_modes":list(GATE_MODES),
        "gate_truth":"COPY_A=a; COPY_B=b; NAND=1-a*b; ZERO=0; ONE=1",
        "constraint":"D(y,z)=0 iff y=Cz",
        "lattice_embedding":"B=C (C includes an explicit selector-identity row block), target=target_y",
        "drop":"each local node has target-one NORM_DROP_GUARD",
      },
      "topology":topology,
      "target_interface":{
        "mutable_row_kinds":["SOURCE_PROGRAM","GATE_PROGRAM","OUTPUT_INTERFACE"],
        "fixed_row_targets":{"NORM_DROP_GUARD":1,"EDGE_CONSISTENCY":0,"DYADIC_SEPARATOR":0,"PHYSICAL_SELECTOR":0},
        "source_program":"one-hot FREE/FIX0/FIX1 per source",
        "gate_program":"one-hot COPY_A/COPY_B/NAND/ZERO/ONE per gate",
        "output":"one desired bit per last-stage lane",
        "z_target":"all zero",
      },
      "row_marks":rows,"column_marks":cols,
      "C":{"shape":[m,k],"entries":C},
      "D":{"shape":[m,m+k],"entries":D},
    }
    payload["component_hashes"]={
      "rows":sha(rows),"columns":sha(cols),"C":sha(payload["C"]),"D":sha(payload["D"]),
    }
    payload["payload_hash_excluding_this_field"]=sha(payload)
    return payload, node_cols, row_by_id


def make_program(payload, flavor):
    w=payload["width"]; L=payload["gate_stages"]
    source_bits=[(i ^ (i>>1)) & 1 for i in range(w)]
    if flavor == "identity_free":
        source_modes=["FREE"]*w
        modes={(s,i):"COPY_A" for s in range(1,L+1) for i in range(w)}
    elif flavor == "all_nand_pinned":
        source_modes=["FIX1" if b else "FIX0" for b in source_bits]
        modes={(s,i):"NAND" for s in range(1,L+1) for i in range(w)}
    elif flavor == "mixed_reconvergent":
        source_modes=["FREE"]*w
        modes={(s,i):GATE_MODES[(3*s+5*i+s*i)%len(GATE_MODES)]
               for s in range(1,L+1) for i in range(w)}
    else: raise ValueError(flavor)
    vals={(0,i):source_bits[i] for i in range(w)}
    logw=w.bit_length()-1
    for s in range(1,L+1):
        off=1 << (((s-1)//2)%logw)
        for i in range(w):
            a,b=vals[(s-1,i)],vals[(s-1,i^off)]
            vals[(s,i)]=gate_value(modes[(s,i)],a,b)
    return source_modes,modes,vals,[vals[(L,i)] for i in range(w)]


def honest_vector(payload, source_modes, modes, vals):
    cols=payload["column_marks"]
    lookup={c["id"]:c["index"] for c in cols}
    w=payload["width"]; L=payload["gate_stages"]
    z=[0]*len(cols)
    for i in range(w):
        mode=source_modes[i]; bit=vals[(0,i)]
        z[lookup[f"src:{i}:{mode}:{bit}"]]=1
    logw=w.bit_length()-1
    for s in range(1,L+1):
        off=1 << (((s-1)//2)%logw)
        for i in range(w):
            mode=modes[(s,i)]; a=vals[(s-1,i)]; b=vals[(s-1,i^off)]; c=vals[(s,i)]
            z[lookup[f"gate:{s}:{i}:{mode}:{a}{b}{c}"]]=1
    return z


def target_y(payload, source_modes, modes, outputs):
    t=[]
    for r in payload["row_marks"]:
        kind=r["kind"]
        if kind=="NORM_DROP_GUARD": v=1
        elif kind in ("EDGE_CONSISTENCY","DYADIC_SEPARATOR","PHYSICAL_SELECTOR"): v=0
        elif kind=="SOURCE_PROGRAM": v=int(source_modes[r["lane"]]==r["mode"])
        elif kind=="GATE_PROGRAM": v=int(modes[(r["stage"],r["lane"])]==r["mode"])
        elif kind=="OUTPUT_INTERFACE": v=outputs[r["lane"]]
        else: raise AssertionError(kind)
        t.append(v)
    return t


def matvec(shape, entries, x):
    y=[0]*shape[0]
    for i,j,v in entries: y[i]+=v*x[j]
    return y


def audit(payload):
    m,k=payload["C"]["shape"]
    assert payload["D"]["shape"] == [m,m+k]
    # Exact systematic identity and -C, with no omitted or duplicate entry.
    expect={(i,i):1 for i in range(m)}
    for i,j,v in payload["C"]["entries"]: expect[(i,m+j)]=-v
    got={(i,j):v for i,j,v in payload["D"]["entries"]}
    assert len(got)==len(payload["D"]["entries"]) and got==expect
    assert all(isinstance(v,int) and v != 0 for _,_,v in payload["C"]["entries"])
    # Audit every serialized local state, not only those used by examples.
    for col in payload["column_marks"]:
        st=col["state"]
        if col["kind"]=="SOURCE_SELECTOR":
            assert legal_source(st["mode"],st["bit"])
        else:
            assert st["c"]==gate_value(st["mode"],st["a"],st["b"])
    byrow=defaultdict(list)
    for i,j,v in payload["C"]["entries"]: byrow[i].append((j,v))
    physical=[r for r in payload["row_marks"] if r["kind"]=="PHYSICAL_SELECTOR"]
    assert len(physical)==k
    for r in physical:
        assert byrow[r["index"]] == [(r["selector_column"],1)]
    mutable={"SOURCE_PROGRAM","GATE_PROGRAM","OUTPUT_INTERFACE"}
    targets=[]
    node_count=payload["width"]*(payload["gate_stages"]+1)
    for flavor in ("identity_free","all_nand_pinned","mixed_reconvergent"):
        sm,gm,vals,outs=make_program(payload,flavor)
        z=honest_vector(payload,sm,gm,vals)
        t=target_y(payload,sm,gm,outs)
        Cz=matvec(payload["C"]["shape"],payload["C"]["entries"],z)
        assert sum(z)==node_count and sum(a*a for a in z)==node_count
        # All nonphysical constraint coordinates match; the physical identity
        # coordinates carry exactly the selected z entries and hence energy N.
        for i,r in enumerate(payload["row_marks"]):
            if r["kind"]=="PHYSICAL_SELECTOR":
                assert Cz[i]-t[i] == z[r["selector_column"]]
            else:
                assert Cz[i]==t[i]
        assert sum((a-b)**2 for a,b in zip(Cz,t))==node_count
        # D(Cz,z)=0, checked through the actual serialized D.
        assert matvec(payload["D"]["shape"],payload["D"]["entries"],Cz+z)==[0]*m
        assert set(t) <= {0,1}
        targets.append(t)
    # Across examples, every changed target coordinate is declared mutable.
    for i,r in enumerate(payload["row_marks"]):
        if len({t[i] for t in targets})>1: assert r["kind"] in mutable
        if r["kind"] not in mutable:
            assert {t[i] for t in targets} == ({1} if r["kind"]=="NORM_DROP_GUARD" else {0})
    # Nontrivial fixed fanout and reconvergence certificates in the topology.
    edge_rows=[r for r in payload["row_marks"] if r["kind"]=="EDGE_CONSISTENCY"]
    parent_counts=defaultdict(int)
    for r in edge_rows: parent_counts[(r["parent_stage"],r["parent_lane"])]+=1
    assert max(parent_counts.values()) >= 2
    # At stage 2, each gate's two parents have a common stage-0 ancestor in
    # the two-step butterfly dependency graph (an explicit diamond).
    assert payload["gate_stages"]>=2
    w=payload["width"]; logw=w.bit_length()-1
    def parents(s,lane):
        off=1 << (((s-1)//2)%logw); return {lane,lane^off}
    diamonds=0
    for lane in range(w):
        p=parents(2,lane)
        anc=[set().union(*(parents(1,x) for x in [q])) for q in p]
        if len(set.intersection(*anc))>0: diamonds+=1
    assert diamonds==w
    # Hashes stored inside the payload must recompute exactly.
    assert payload["component_hashes"]["rows"]==sha(payload["row_marks"])
    assert payload["component_hashes"]["columns"]==sha(payload["column_marks"])
    assert payload["component_hashes"]["C"]==sha(payload["C"])
    assert payload["component_hashes"]["D"]==sha(payload["D"])
    tmp=dict(payload); h=tmp.pop("payload_hash_excluding_this_field")
    assert h==sha(tmp)
    return {"width":w,"row_count":m,"selector_columns":k,"D_columns":m+k,
            "C_nnz":len(payload["C"]["entries"]),"D_nnz":len(payload["D"]["entries"]),
            "honest_energy":node_count,"diamonds":diamonds,
            **payload["component_hashes"]}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--write",action="store_true",help="rewrite deterministic factor artifacts")
    args=ap.parse_args()
    outdir=Path(__file__).with_name("artifacts")
    outdir.mkdir(exist_ok=True)
    summaries=[]
    for w in WIDTHS:
        payload,_,_=make_factor(w)
        summary=audit(payload)
        path=outdir/f"u0a_universal_topology_w{w}.json"
        data=json.dumps(payload,sort_keys=True,indent=2).encode()+b"\n"
        filehash=hashlib.sha256(data).hexdigest()
        if args.write: path.write_bytes(data)
        assert path.exists(), f"missing frozen artifact {path}; run once with --write"
        assert path.read_bytes()==data, f"artifact drift: {path}"
        assert w in EXPECTED_FILE_SHA256, f"width {w} lacks frozen hash"
        assert filehash==EXPECTED_FILE_SHA256[w]
        summary["file_sha256"]=filehash
        summaries.append(summary)
    print(json.dumps(summaries,indent=2,sort_keys=True))
    print("PASS: finite U0a candidate factors and three honest programs per width")

if __name__=="__main__": main()

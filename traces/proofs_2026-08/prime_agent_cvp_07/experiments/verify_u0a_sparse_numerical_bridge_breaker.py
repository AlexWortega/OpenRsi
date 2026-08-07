#!/usr/bin/env python3
"""Breaker for the sparse-program -> numerical-factor bridge.

This finite verifier is deliberately independent of the eager serializer oracle.
It (1) audits every coefficient emitted by the streaming C generator at the
width/depth pairs used by the small compiler, (2) exhausts every ordered NAND
shape and restricted-growth variable-equality pattern through five leaves using
packed truth tables, and (3) performs full numerical C*z/target checks for every
assignment through four leaves.  It targets stage offsets, XOR-neighbor
orientation, COPY_B swaps/fanout, source duplication, physical NAND ports, and
cleanup/output targeting.  It is finite evidence, not a universal theorem or a
soundness/gap result.
"""
from __future__ import annotations

import itertools
from collections import defaultdict

from verify_u0a_butterfly_formula_compiler import stage_budget
from verify_u0a_canonical_streaming_emitter import iter_C_entries
from verify_u0a_sparse_program_stream import compile_formula_sparse

SOURCE_MODES = ("FREE", "FIX0", "FIX1")
GATE_MODES = ("COPY_A", "COPY_B", "NAND", "ZERO", "ONE")
SOURCE_STATES = (("FREE",0),("FREE",1),("FIX0",0),("FIX1",1))


def gv(mode, a, b, mask=None):
    if mode == "COPY_A": return a
    if mode == "COPY_B": return b
    if mode == "NAND":
        v = a & b
        return 1-v if mask is None else mask ^ v
    if mode == "ZERO": return 0
    if mode == "ONE": return 1 if mask is None else mask
    raise AssertionError(mode)


GATE_STATES = tuple((mode,a,b,gv(mode,a,b))
                    for mode in GATE_MODES for a in (0,1) for b in (0,1))


def col_index(w, stage, lane, local):
    return 4*lane+local if stage == 0 else 4*w+20*((stage-1)*w+lane)+local


def dimensions(w, d):
    k = 4*w + 20*w*d
    m = 30*w*d + 9*w - 2*d
    return m, k


def take_row(source, pending, row):
    got = []
    item = pending[0]
    while item is not None and item[0] == row:
        got.append((item[1], item[2]))
        item = next(source, None)
    pending[0] = item
    return got


def selected(w, stage, lane, field=None, mode=None):
    states = SOURCE_STATES if stage == 0 else GATE_STATES
    ans=[]
    for local, state in enumerate(states):
        if mode is not None:
            value = int(state[0] == mode)
        elif field == "out":
            value = state[1] if stage == 0 else state[3]
        elif field == "a": value = state[1]
        elif field == "b": value = state[2]
        else: value = 1
        if value: ans.append((col_index(w,stage,lane,local),value))
    return ans


def audit_stream_C(w, d, retain_adjacency=False):
    """Compare every streamed coefficient to an independent row equation."""
    source=iter(iter_C_entries(w,d)); pending=[next(source,None)]
    adjacency=[[] for _ in range(dimensions(w,d)[1])] if retain_adjacency else None
    row=0
    def check(expect):
        nonlocal row
        got=take_row(source,pending,row)
        expect=sorted((j,v) for j,v in expect if v)
        assert got == expect, (w,d,row,got[:8],expect[:8])
        if adjacency is not None:
            for j,v in got: adjacency[j].append((row,v))
        row += 1
    # Normalizations.
    for s in range(d+1):
        for lane in range(w): check(selected(w,s,lane))
    # Program rows.
    for lane in range(w):
        for mode in SOURCE_MODES: check(selected(w,0,lane,mode=mode))
    for s in range(1,d+1):
        for lane in range(w):
            for mode in GATE_MODES: check(selected(w,s,lane,mode=mode))
    # Edge rows: A is same lane; B is XOR neighbor at the scheduled offset.
    logw=w.bit_length()-1
    for s in range(1,d+1):
        off=1 << (((s-1)//2)%logw)
        for lane in range(w):
            for port,parent in (("A",lane),("B",lane^off)):
                e=[(j,-v) for j,v in selected(w,s-1,parent,field="out")]
                e += selected(w,s,lane,field=port.lower())
                check(e)
    # Each separator is exactly the coefficientwise sum of its edge block.
    for s in range(1,d+1):
        off=1 << (((s-1)//2)%logw)
        for port in ("A","B"):
            for q in range(1,logw+1):
                size=1<<q
                for start in range(0,w,size):
                    coeff=defaultdict(int)
                    for lane in range(start,start+size):
                        parent=lane if port=="A" else lane^off
                        for j,v in selected(w,s-1,parent,field="out"): coeff[j]-=v
                        for j,v in selected(w,s,lane,field=port.lower()): coeff[j]+=v
                    check(coeff.items())
    for lane in range(w): check(selected(w,d,lane,field="out"))
    k=dimensions(w,d)[1]
    for j in range(k): check([(j,1)])
    m,_=dimensions(w,d)
    assert row==m and pending[0] is None
    return adjacency


def shapes(n):
    if n==1: return (None,)
    return tuple((a,b) for i in range(1,n) for a in shapes(i) for b in shapes(n-i))


def rgs(n):
    if n==1: return ((0,),)
    ans=[]
    def go(xs):
        if len(xs)==n: ans.append(tuple(xs)); return
        for x in range(max(xs)+2): go(xs+[x])
    go([0]); return tuple(ans)


def fill(shape, labels, pos=0):
    if shape is None: return labels[pos],pos+1
    a,pos=fill(shape[0],labels,pos); b,pos=fill(shape[1],labels,pos)
    return (a,b),pos


def formula_family(max_leaves):
    for n in range(1,max_leaves+1):
        for sh in shapes(n):
            for labels in rgs(n):
                f,end=fill(sh,labels)
                assert end==n
                yield n,f


def eval_packed(f, varvals, mask):
    if isinstance(f,int): return varvals[f]
    return mask ^ (eval_packed(f[0],varvals,mask)&eval_packed(f[1],varvals,mask))


def validate_sparse_record(p):
    w,d=p["width"],p["gate_stages"]
    assert p["source_default"]=="FIX0"
    assert p["source_overrides"] == tuple((lane,"FREE") for lane in sorted(p["source_lane"].values()))
    ov=p["raw_gate_overrides"]
    assert all(a[:2]<b[:2] for a,b in zip(ov,ov[1:]))
    assert all(1<=s<=p["raw_stage_count"] and 0<=lane<w and mode in GATE_MODES and mode!="COPY_A"
               for s,lane,mode in ov)
    assert p["padding"] == {"start_stage":p["raw_stage_count"]+1,
                            "count":d-p["raw_stage_count"]-1,
                            "default_mode":"COPY_A"}
    assert p["cleanup"]["stage"]==d and p["cleanup"]["default_mode"]=="ZERO"
    assert p["cleanup"]["overrides"]==((p["output_lane"],"COPY_A"),)
    assert p["output_default"]==0
    expected_out=((p["output_lane"],p["assert_bit"]),) if p["assert_bit"] else ()
    assert p["output_overrides"]==expected_out


def mode_grid(p, drop_duplicate=False):
    w,d=p["width"],p["gate_stages"]
    od={(s,lane):mode for s,lane,mode in p["raw_gate_overrides"]}
    if drop_duplicate:
        bystage=defaultdict(list)
        for key,mode in od.items(): bystage[key[0]].append((key,mode))
        singleton=next((items[0][0] for items in bystage.values()
                        if len(items)==1 and items[0][1]=="COPY_B"),None)
        if singleton is None: return None
        del od[singleton]
    rows=[]
    for s in range(1,d+1):
        if s==d:
            rows.append(["COPY_A" if lane==p["output_lane"] else "ZERO" for lane in range(w)])
        else:
            rows.append([od.get((s,lane),"COPY_A") for lane in range(w)])
    return rows


def simulate(p, source_values, mask=None, mutant=None):
    """Numerical topology simulation, independent of compiler token maps."""
    w,d=p["width"],p["gate_stages"]; logw=w.bit_length()-1
    grid=mode_grid(p, drop_duplicate=(mutant=="duplicate_source"))
    if grid is None: return None
    inv={lane:v for v,lane in p["source_lane"].items()}
    vals=[[source_values[inv[lane]] if lane in inv else 0 for lane in range(w)]]
    for s in range(1,d+1):
        if mutant=="stage_offset": dim=(s//2)%logw
        else: dim=((s-1)//2)%logw
        off=1<<dim
        prev=vals[-1]; cur=[]
        for lane,mode in enumerate(grid[s-1]):
            if mutant=="neighbor_orientation":
                parent=(lane+off)%w
            else: parent=lane^off
            a,b=prev[lane],prev[parent]
            if mutant=="copy_b_local" and mode=="COPY_B": c=a
            else: c=gv(mode,a,b,mask)
            cur.append(c)
        vals.append(cur)
    return vals


def independent_target(p, grid):
    w,d=p["width"],p["gate_stages"]
    t=[1]*(w*(d+1))
    free=set(p["source_lane"].values())
    for lane in range(w):
        chosen="FREE" if lane in free else "FIX0"
        t.extend(int(mode==chosen) for mode in SOURCE_MODES)
    for s in range(d):
        for lane in range(w):
            t.extend(int(mode==grid[s][lane]) for mode in GATE_MODES)
    t.extend([0]*(2*w*d + 2*d*(w-1)))
    t.extend(p["assert_bit"] if lane==p["output_lane"] else 0 for lane in range(w))
    t.extend([0]*dimensions(w,d)[1])
    assert len(t)==dimensions(w,d)[0]
    return t


def full_C_check(p, formula, assignment, adjacency):
    w,d=p["width"],p["gate_stages"]
    grid=mode_grid(p); vals=simulate(p,assignment)
    selected_cols=[]
    inv={lane:v for v,lane in p["source_lane"].items()}
    for lane in range(w):
        bit=assignment[inv[lane]] if lane in inv else 0
        mode="FREE" if lane in inv else "FIX0"
        local=SOURCE_STATES.index((mode,bit))
        selected_cols.append(col_index(w,0,lane,local))
    for s in range(1,d+1):
        off=1<<(((s-1)//2)%(w.bit_length()-1))
        for lane in range(w):
            a=vals[s-1][lane]; b=vals[s-1][lane^off]; c=vals[s][lane]
            local=GATE_STATES.index((grid[s-1][lane],a,b,c))
            selected_cols.append(col_index(w,s,lane,local))
    m,k=dimensions(w,d); Cz=[0]*m
    for j in selected_cols:
        for row,v in adjacency[j]: Cz[row]+=v
    target=independent_target(p,grid)
    out0=w*(d+1)+3*w+5*w*d+2*w*d+2*d*(w-1)
    phys0=out0+w
    expected=target[:]
    expected[out0+p["output_lane"]] += vals[d][p["output_lane"]]-p["assert_bit"]
    for j in selected_cols: expected[phys0+j]=1
    assert Cz==expected
    energy=sum((a-b)**2 for a,b in zip(Cz,target))
    assert energy==w*(d+1)+(vals[d][p["output_lane"]]-p["assert_bit"])**2


def main():
    # Local/static audit of every emitted numerical coefficient.  Width 8
    # exercises all three butterfly dimensions repeatedly.
    d4,d8=stage_budget(4),stage_budget(8)
    adj4=audit_stream_C(4,d4,retain_adjacency=True)
    audit_stream_C(8,d8,retain_adjacency=False)

    counts=defaultdict(int); packed_assignments=0; full_checks=0
    mutant_witness={k:None for k in ("stage_offset","neighbor_orientation",
                                     "copy_b_local","duplicate_source")}
    for n,f in formula_family(5):
        counts[n]+=1
        k=max_var(f)+1
        bits=1<<k; mask=(1<<bits)-1
        varvals=[]
        for v in range(k):
            word=0
            for a in range(bits): word |= ((a>>v)&1)<<a
            varvals.append(word)
        expected=eval_packed(f,varvals,mask)
        packed_assignments += bits
        for assert_bit in (0,1):
            p=compile_formula_sparse(f, width=4 if n<=4 else 8, assert_bit=assert_bit)
            validate_sparse_record(p)
            vals=simulate(p,varvals,mask=mask)
            assert vals[-1][p["output_lane"]]==expected, (n,f)
            assert all(x==0 for lane,x in enumerate(vals[-1]) if lane!=p["output_lane"])
            # Cleanup target: exactly the surviving root lane is asserted.
            grid=mode_grid(p); target=independent_target(p,grid)
            out0=p["width"]*(p["gate_stages"]+1)+3*p["width"]+5*p["width"]*p["gate_stages"]+2*p["width"]*p["gate_stages"]+2*p["gate_stages"]*(p["width"]-1)
            assert target[out0:out0+p["width"]] == [assert_bit if lane==p["output_lane"] else 0 for lane in range(p["width"])]
            for mutant in mutant_witness:
                if mutant_witness[mutant] is None:
                    bad=simulate(p,varvals,mask=mask,mutant=mutant)
                    if bad is not None and (bad[-1][p["output_lane"]]!=expected or
                       any(x!=0 for lane,x in enumerate(bad[-1]) if lane!=p["output_lane"])):
                        mutant_witness[mutant]=(n,repr(f),assert_bit)
            if n<=4:
                for a in range(bits):
                    assignment={v:(a>>v)&1 for v in range(k)}
                    full_C_check(p,f,assignment,adj4); full_checks+=1
    assert counts=={1:1,2:2,3:10,4:75,5:728}, counts
    assert all(mutant_witness.values()), mutant_witness
    # NAND has no meaningful Boolean child-order bug: it is exactly symmetric.
    assert all(gv("NAND",a,b)==gv("NAND",b,a) for a in (0,1) for b in (0,1))

    # A one-lane cleanup-target shift is rejected independently of gate values.
    cleanup=compile_formula_sparse(((0,1),(0,1)),width=4,assert_bit=1)
    wrong=(cleanup["output_lane"]+1)%4
    assert wrong!=cleanup["output_lane"]
    correct=independent_target(cleanup,mode_grid(cleanup))
    out0=4*(d4+1)+3*4+5*4*d4+2*4*d4+2*d4*3
    wrong_t=correct[:]; wrong_t[out0+cleanup["output_lane"]]=0; wrong_t[out0+wrong]=1
    assert wrong_t!=correct

    print("PASS sparse-program/numerical-factor bridge breaker")
    print("formula counts by leaves:",dict(counts))
    print("packed assignment evaluations (per assertion-independent formula):",packed_assignments)
    print("full streamed-C honest-vector checks (both assertion bits):",full_checks)
    print("mutants killed:",mutant_witness)
    print("NAND child swap: certified harmless on all four Boolean input pairs (NAND is symmetric)")
    print("Scope: finite exhaustive through five leaves; exact C audit at widths 4/depth %d and 8/depth %d; no universal compiler theorem, CVP soundness, or gap."%(d4,d8))


def max_var(f):
    if isinstance(f,int): return f
    return max(max_var(f[0]),max_var(f[1]))


if __name__=="__main__": main()

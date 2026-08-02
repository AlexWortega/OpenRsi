#!/usr/bin/env python3
# Question: can nonuniform cluster sizes and per-vertex missing palettes amplify a seed more efficiently than uniform blow-up?
# For each verified local seed, exact cluster weights are R_{|M_v|}-1 under the missing-color lemma.
import json,math
cases=[('experiments/local_26_g5_s4.json',5),('experiments/local_57_g6_s5.json',6),('experiments/cyclic127_local40.json',5),('experiments/cyclic251_local60.json',6)]
# Only one missing color in these cases, so each cluster has size two and no nonuniform gain.
for path,k in cases:
 d=json.load(open(path));N=d.get('N',len(d.get('vertices',[])));print(path,N,'global',k,'one-step order',2*N)

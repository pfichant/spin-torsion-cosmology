#!/usr/bin/env python3
"""
Script Name : check_reproduction.py
Author      : Pascal Fichant
Version     : 1.0 (16/10/2026)
Description : compares results_cmb_seeds.json and, if present, results_planck_data_zreio6.json (your runs)
              with reference/results_cmb_seeds_REFERENCE.json and reference/results_planck_data_zreio6_REFERENCE.json
              (run of 16/10/2026: fresh virtual environment, patched CLASS 3.3.2, no cache).
              Pass if every f_95 agrees within the tolerance (default 2 %).
"""
import json, sys
tol = float(sys.argv[1]) if len(sys.argv) > 1 else 0.02
a = json.load(open('results_cmb_seeds.json')); b = json.load(open('reference/results_cmb_seeds_REFERENCE.json'))
bad = 0; n = 0
for sec in ('validate', 'bounds'):
    for ra, rb in zip(a.get(sec, []), b[sec]):
        assert ra['case'] == rb['case'], (ra['case'], rb['case'])
        for k in ('Planck-like', 'S4-like'):
            va, vb = ra[k]['f_95'], rb[k]['f_95']; n += 1
            ok = (va is None and vb is None) or (va and vb and abs(va / vb - 1) < tol)
            bad += not ok
            print(f"{'OK ' if ok else 'BAD'} {rb['case']:60s} {k:12s} {ra[k]['f_95_str']:>10s} vs {rb[k]['f_95_str']:>10s}")
import os
if os.path.exists('results_planck_data_zreio6.json'):                       # Part 2 (real Planck data)
    a2 = json.load(open('results_planck_data_zreio6.json')); b2 = json.load(open('reference/results_planck_data_zreio6_REFERENCE.json'))
    for k, rb in b2.items():
        if isinstance(rb, dict) and 'f_95' in rb:
            va, vb = a2[k]['f_95'], rb['f_95']; n += 1
            ok = (va is None and vb is None) or (va and vb and abs(va / vb - 1) < tol); bad += not ok
            print(f"{'OK ' if ok else 'BAD'} Planck data, z_reio >= 6: {k:52s} {va:.2e} vs {vb:.2e}")
print(f"{n - bad}/{n} bounds reproduced within {tol*100:.0f} %"); sys.exit(1 if bad else 0)

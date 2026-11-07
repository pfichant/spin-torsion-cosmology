#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
Project     : Einstein-Cartan Framework (ECF) - Macro-Knot seeds and the CMB
Script Name : ecf_cmb_seeds_planck_data.py
Author      : Pascal Fichant
Version     : 1.0 (16/10/2026)
Status      : working note, not yet part of a deposited paper
Description :
    Bounds on accreting 10^5 Msun seeds from the REAL Planck 2018 data, as a
    complement to the forecast in ecf_cmb_seeds.py.

    * Likelihood: Planck 2018 high-ell plik_lite TT,TE,EE (l >= 30; data and
      covariance from the Planck Legacy Archive as distributed with
      planck-lite-py, github.com/heatherprince/planck-lite-py), calibration
      A_planck with prior 1 +- 0.0025, plus a Gaussian prior on the TOTAL
      optical depth, tau = 0.0506 +- 0.0086 (Planck 2018 VI, Eq. 4, lowE alone).
    * Energy deposition: f_eff(z) computed with DarkAges 1.2.0 (Stocker et al.
      2018) for the accreting-PBH spectra of Poulin et al. 2017 (disk) and
      Ali-Haimoud & Kamionkowski 2017 (spherical), M = 1e5 Msun, Planck
      background (files feff_*_1e5_planckbg.dat, produced by make_feff.sh);
      or on-the-spot f_eff = 1 (soft thermal thin-disk spectrum, upper case).
    * Profile likelihood: for each f, chi^2 is minimised over (omega_b,
      omega_cdm, H0, ln10^10 A_s, n_s, z_reio, A_planck) by Gauss-Newton steps
      with a Jacobian computed once at the f = 0 best fit, each step checked by
      an exact CLASS evaluation; Delta chi^2 uses the exact values.
      95 % bound at Delta chi^2 = 3.84.
    * Background: Planck 2018 best fit (the data are not fitted by the ECF
      closure background without the spin term; the injection signal itself
      changes by < 2 % between the two backgrounds, see ecf_cmb_seeds.py).

Usage       : python3 ecf_cmb_seeds_planck_data.py   (needs patched CLASS, see class_patch/)
              ZREIO_MIN=6 python3 ecf_cmb_seeds_planck_data.py   (adds the quasar floor z_reio >= 6)
              PLANCK_LITE_DIR=<path to planck-lite-py>  (default ./planck-lite-py)
Output      : results_planck_data.json
=============================================================================
"""
import os, sys, json
import numpy as np
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
PL_DIR = os.environ.get('PLANCK_LITE_DIR', os.path.join(HERE, 'planck-lite-py'))
sys.path.insert(0, PL_DIR)
from planck_lite_py import PlanckLitePy

NPROC = int(os.environ.get('NPROC', '8'))
LMAX = 2600
M = 1e5
RHO_DM = 0.12 * 2.775e11
TAU_LOWE, SIG_TAU = 0.0506, 0.0086
SIG_AP = 0.0025
ZREIO_MIN = float(os.environ['ZREIO_MIN']) if os.environ.get('ZREIO_MIN') else None   # e.g. 6: reionisation over by z = 5.3 (Bosman et al. 2022)
P0 = dict(omega_b=0.02237, omega_cdm=0.1200, H0=67.36, ln10A=3.044, n_s=0.9649, z_reio=7.67)
KEYS = ['omega_b', 'omega_cdm', 'H0', 'ln10A', 'n_s', 'z_reio']
STEP = dict(omega_b=1e-4, omega_cdm=1e-3, H0=0.3, ln10A=0.005, n_s=0.004, z_reio=0.3)
PL = PlanckLitePy(data_directory=os.path.join(PL_DIR, 'data'), year=2018, spectra='TTTEEE', use_low_ell_bins=False)


def feff_path(name):
    import classy
    base = os.path.dirname(classy.__file__)          # CLASS prepends its base path without a separator
    return '/' + os.path.relpath(os.path.join(HERE, f'feff_{name}_1e5_planckbg.dat'), base)


CASES = {  # name: (PBH_LMODE, recipe, deposition, f grid; refined near the 95 % threshold)
    'Eddington, hard spectrum (DarkAges disk f(z))': ('edd', 'disk', 'disk', [1e-10, 1e-9, 2e-9, 3e-9, 4e-9, 6e-9, 1e-8]),
    'Eddington, soft spectrum (on-the-spot f_eff = 1)': ('edd', 'disk', 'spot', [1e-11, 1e-10, 2e-10, 3e-10, 4e-10, 6e-10, 1e-9]),
    'Disk recipe Poulin, capped (DarkAges disk f(z))': ('cap', 'disk', 'disk', [1e-8, 5e-8, 1e-7, 1.5e-7, 2e-7, 3e-7, 1e-6]),
    'Spherical recipe AHK, capped (DarkAges sph f(z))': ('cap', 'sph', 'sph', [1e-7, 5e-7, 1e-6, 1.5e-6, 2e-6, 3e-6, 1e-5])}


def run(job):
    p, lmode, recipe, dep, f = job
    os.environ['PBH_LMODE'] = lmode; os.environ['PBH_ZCUT'] = '0'
    from classy import Class
    c = Class()
    d = {'output': 'tCl,pCl,lCl', 'lensing': 'yes', 'l_max_scalars': LMAX,
         'omega_b': p['omega_b'], 'omega_cdm': p['omega_cdm'], 'H0': p['H0'],
         'ln10^{10}A_s': p['ln10A'], 'n_s': p['n_s'], 'z_reio': p['z_reio']}
    if f > 0:
        d.update({'PBH_accretion_fraction': f, 'PBH_accretion_mass': M,
                  'PBH_accretion_recipe': 'spherical_accretion' if recipe == 'sph' else 'disk_accretion'})
        if recipe != 'sph':
            d.update({'PBH_accretion_ADAF_delta': 1e-3, 'PBH_accretion_eigenvalue': 0.01})
        d.update({'f_eff_type': 'on_the_spot', 'f_eff': 1.0} if dep == 'spot' else
                 {'f_eff_type': 'from_file', 'f_eff_file': feff_path(dep)})
    try:
        c.set(d); c.compute()
    except Exception as e:
        return None
    cl = c.lensed_cl(LMAX); T2 = 2.7255e6 ** 2
    l = np.arange(LMAX + 1); fac = l * (l + 1) / (2 * np.pi)
    Dl = [(cl[k] * T2 * fac)[2:] for k in ('tt', 'te', 'ee')]
    tau = c.get_current_derived_parameters(['tau_reio'])['tau_reio']
    c.struct_cleanup(); c.empty()
    return np.concatenate(binned(*Dl)), tau


def binned(Dtt, Dte, Dee, ellmin=2):
    """Binned C_l vector exactly as in PlanckLitePy.loglike (calibration 1)."""
    ls = np.arange(len(Dtt)) + ellmin; fac = ls * (ls + 1) / (2 * np.pi)
    out = []
    for D, nb, bmin, bmax, w, pl in ((Dtt, PL.nbintt, PL.blmin_TT, PL.blmax_TT, PL.bin_w_TT, PL.plmin_TT),
                                    (Dte, PL.nbinte, PL.blmin, PL.blmax, PL.bin_w, PL.plmin),
                                    (Dee, PL.nbinee, PL.blmin, PL.blmax, PL.bin_w, PL.plmin)):
        C = D / fac
        out.append(np.array([np.sum(C[bmin[i] + pl - ellmin:bmax[i] + pl + 1 - ellmin] * w[bmin[i]:bmax[i] + 1]) for i in range(nb)]))
    return out


def wall(p):
    """Optional floor on z_reio (steep quadratic wall, width 0.05)."""
    if ZREIO_MIN is None or p['z_reio'] >= ZREIO_MIN: return 0.0
    return ((ZREIO_MIN - p['z_reio']) / 0.05) ** 2


def chi2(X, tau, Ap, p=None):
    Y = PL.X_data - X / Ap ** 2
    return Y @ PL.fisher @ Y + ((tau - TAU_LOWE) / SIG_TAU) ** 2 + ((Ap - 1) / SIG_AP) ** 2 + (wall(p) if p is not None else 0.0)


def pmap(jobs):
    with Pool(NPROC, maxtasksperchild=1) as P:
        return P.map(run, jobs)


def jacobian(p, case=('none', 'disk', 'spot'), f=0.0):
    jobs = []
    for k in KEYS:
        for s in (+1, -1):
            q = dict(p); q[k] += s * STEP[k]; jobs.append((q,) + case + (f,))
    R = pmap(jobs)
    JX = np.array([(R[2 * i][0] - R[2 * i + 1][0]) / (2 * STEP[k]) for i, k in enumerate(KEYS)])
    Jt = np.array([(R[2 * i][1] - R[2 * i + 1][1]) / (2 * STEP[k]) for i, k in enumerate(KEYS)])
    return JX, Jt


def gn_step(X, tau, Ap, JX, Jt, p=None):
    """Gauss-Newton step in (6 parameters, A_planck) for the chi^2 above."""
    F = PL.fisher
    r = PL.X_data - X / Ap ** 2
    Jfull = np.vstack([JX / Ap ** 2, 2 * X / Ap ** 3 * (-1)])          # d(model)/d(param) ; model = X/Ap^2
    A = Jfull @ F @ Jfull.T; b = Jfull @ F @ r
    gt = np.concatenate([Jt, [0.0]]); A += np.outer(gt, gt) / SIG_TAU ** 2; b += gt * (TAU_LOWE - tau) / SIG_TAU ** 2
    ga = np.zeros(7); ga[6] = 1; A += np.outer(ga, ga) / SIG_AP ** 2; b += ga * (1 - Ap) / SIG_AP ** 2
    if ZREIO_MIN is not None and p is not None and p['z_reio'] <= ZREIO_MIN + 0.3:   # linearised wall
        gz = np.zeros(7); gz[5] = 1; A += np.outer(gz, gz) / 0.05 ** 2; b += gz * max(ZREIO_MIN - p['z_reio'], 0.0) / 0.05 ** 2
    return np.linalg.solve(A, b)


def shifted(p, Ap, dx):
    q = dict(p)
    for i, k in enumerate(KEYS): q[k] += dx[i]
    return q, Ap + dx[6]


def fit_batch(p, Ap, case, fl, JX, Jt, nit=3):
    """Profile chi^2 for each f in fl. Every CLASS evaluation runs in a fresh process (pmap)."""
    st = [dict(p=dict(p), Ap=Ap) for _ in fl]
    R = pmap([(s_['p'],) + case + (f,) for s_, f in zip(st, fl)])
    for s_, r in zip(st, R):
        s_['X'], s_['tau'] = r; s_['c'] = chi2(r[0], r[1], s_['Ap'], s_['p']); s_['active'] = True
    for _ in range(nit):
        idx = [i for i, s_ in enumerate(st) if s_['active']]
        if not idx: break
        cand = []                                   # line search: full, half and quarter Gauss-Newton steps
        for i in idx:
            dx = gn_step(st[i]['X'], st[i]['tau'], st[i]['Ap'], JX, Jt, st[i]['p'])
            for a in (1.0, 0.5, 0.25):
                cand.append((i,) + shifted(st[i]['p'], st[i]['Ap'], a * dx))
        R = pmap([(q,) + case + (fl[i],) for i, q, Aq in cand])
        best = {}
        for (i, q, Aq), r in zip(cand, R):
            if r is None: continue
            cq = chi2(r[0], r[1], Aq, q)
            if cq < best.get(i, (np.inf,))[0]: best[i] = (cq, q, Aq, r)
        for i in idx:
            if i in best and best[i][0] < st[i]['c'] - 1e-3:
                cq, q, Aq, r = best[i]; st[i].update(p=q, Ap=Aq, X=r[0], tau=r[1], c=cq)
            else:
                st[i]['active'] = False
    return st


def main():
    out = {}
    # 1. f = 0 best fit (two Jacobians, Gauss-Newton with exact checks)
    p, Ap = dict(P0), 1.0
    for _ in range(2):
        JX, Jt = jacobian(p)
        b0 = fit_batch(p, Ap, ('none', 'disk', 'spot'), [0.0], JX, Jt, nit=5)[0]
        p, Ap = b0['p'], b0['Ap']
    JX, Jt = jacobian(p)
    c0, tau0 = b0['c'], b0['tau']
    out['bestfit_f0'] = dict(chi2=c0, params=p, A_planck=Ap, tau=tau0)
    print(f"f = 0 best fit: chi2 = {c0:.2f} (plik_lite 613 bins + priors), tau = {tau0:.4f}, A_planck = {Ap:.4f}, {p}", flush=True)
    for name, (lmode, recipe, dep, fl) in CASES.items():
        case = (lmode, recipe, dep)
        st = fit_batch(p, Ap, case, [1e-14] + fl, JX, Jt, nit=6)   # first entry: module on, negligible f
        ref = st[0]['c']; st = st[1:]
        rows = [dict(f=f, dchi2=s_['c'] - ref, tau=s_['tau'], z_reio=s_['p']['z_reio']) for f, s_ in zip(fl, st)]
        x = np.array([r['f'] for r in rows]); y = np.array([r['dchi2'] for r in rows])
        ok = np.where(y >= 3.84)[0]
        if len(ok) == 0: f95, s = None, f'> {x.max():.1e}'
        elif ok[0] == 0: f95, s = None, f'< {x[0]:.1e}'
        else:
            i = ok[0]; f95 = float(np.exp(np.interp(np.log(3.84), np.log(np.maximum(y[i-1:i+1], 1e-6)), np.log(x[i-1:i+1])))); s = f'{f95:.2e}'
        out[name] = dict(rows=rows, f_95=f95, n_95=(f95 * RHO_DM / M if f95 else None), reference_chi2=ref)
        print(f"{name}\n   " + "  ".join(f"f={r['f']:.1e}: dchi2={r['dchi2']:.2f} (tau={r['tau']:.4f}, z_reio={r['z_reio']:.2f})" for r in rows), flush=True)
        print(f"   f_95 = {s}" + (f"  ->  n_95 = {f95 * RHO_DM / M:.2e} Mpc^-3" if f95 else ''), flush=True)
    out['z_reio_min'] = ZREIO_MIN
    json.dump(out, open('results_planck_data.json' if ZREIO_MIN is None else f'results_planck_data_zreio{ZREIO_MIN:g}.json', 'w'), indent=1, default=float)


if __name__ == '__main__':
    main()

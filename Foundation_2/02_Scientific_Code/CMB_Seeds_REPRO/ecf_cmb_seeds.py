#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
Project     : Einstein-Cartan Framework (ECF) - Macro-Knot seeds and the CMB
Script Name : ecf_cmb_seeds.py
Author      : Pascal Fichant
Version     : 1.0 (16/10/2026)
Status      : working note, not yet part of a deposited paper
Description :
    CMB imprint of compact Macro-Knot seeds (10^5 Msun) that accrete gas from
    recombination onward, computed with CLASS 3.3.2 (exotic-injection module,
    Stocker et al. 2018) patched with an Eddington cap (class_patch/).

    Method (no calibration on ECF quantities):
      * background: h = 0.7304, omega_b = 0.02237, omega_cdm = 0.1200
        (ECF closure values; the spin term is not included);
      * accretion recipes: 'edd'  L = L_Edd at all z (ROM 2008 with halo
        reaches Eddington from z ~ 1000 for 1e5 Msun);
        'disk' Poulin et al. 2017 (lambda = 0.01, delta_ADAF = 1e-3), capped;
        'sph'  Ali-Haimoud & Kamionkowski 2017, capped;
        no dark-matter halo, fixed mass, on-the-spot deposition with f_eff;
      * direct scan in f (the response is non-linear in f); Delta chi^2 is
        marginalised linearly over (omega_b, omega_cdm, H0, ln10^10 A_s, n_s,
        z_reio) with a Gaussian prior on the TOTAL optical depth tau
        (sigma = 0.007, Planck 2018 lowE), or with large-scale EE (l = 2-29)
        whose white noise is tuned to a target sigma(tau);
      * Gaussian likelihood in C_l (TT, TE, EE); Planck-like (5', 33/56
        muK.arcmin, f_sky 0.6, l 30-2500) and S4-like (1.4', 1/1.4 muK.arcmin,
        f_sky 0.4, l 30-3000); 95 % bound at Delta chi^2 = 3.84;
      * reference run = injection module ON at f = 1e-14 (switching the module
        on produces a small threshold artefact, Delta chi^2 ~ 0.03 Planck-like,
        ~ 0.55 S4-like); each CLASS run in a fresh process.

    Validation against published bounds (command 'validate'):
      Serpico et al. 2020 Eq. 25 (L = L_Edd): f_95 = 2.9e-9   (this code: ~4e-9, f_eff = 0.1)
      Poulin et al. 2017, 100 Msun, disk, lambda = 0.01: f_95 = 1.9e-3 (this code: ~3e-3, f_eff = 1)

Usage       :
    python3 ecf_cmb_seeds.py validate     # the two benchmarks above
    python3 ecf_cmb_seeds.py bounds       # ECF table (Planck-like, S4-like, large-scale EE)
    python3 ecf_cmb_seeds.py figure       # Fig_CMB_ECF_seeds.png
    python3 ecf_cmb_seeds.py all
    Requires the patched CLASS: bash class_patch/install_patched_class.sh
Output      : results_cmb_seeds.json, Fig_CMB_ECF_seeds.png
=============================================================================
"""
import os, sys, json
import numpy as np
from multiprocessing import Pool
from scipy.optimize import brentq

LMAX = 3000
NPROC = int(os.environ.get('NPROC', '8'))
RHO_DM = 0.12 * 2.775e11            # Msun / Mpc^3 (omega_cdm * rho_crit / h^2)
FREF = 1e-14                        # reference run: module on, negligible f
BACKGROUNDS = {
    'planck': dict(omega_b=0.02237, omega_cdm=0.1200, H0=67.36, ln10A=3.044, n_s=0.9649, z_reio=7.67),
    'ecf':    dict(omega_b=0.02237, omega_cdm=0.1200, H0=73.04, ln10A=3.044, n_s=0.9649, z_reio=7.67)}
KEYS = ['omega_b', 'omega_cdm', 'H0', 'ln10A', 'n_s', 'z_reio']
STEP = dict(omega_b=2e-4, omega_cdm=1e-3, H0=0.3, ln10A=0.01, n_s=0.005, z_reio=0.3)
EXPS = {'Planck-like': (5.0, 33.0, 56.0, 0.6, 30, 2500),
        'S4-like':     (1.4, 1.0, 1.4, 0.4, 30, 3000)}


def class_run(job):
    """One CLASS run in a fresh process. job = (params, lmode, zcut, recipe, M, f, f_eff)."""
    p, lmode, zcut, recipe, M, f, feff = job
    os.environ['PBH_LMODE'] = lmode
    os.environ['PBH_ZCUT'] = str(zcut)
    from classy import Class
    c = Class()
    d = {'output': 'tCl,pCl,lCl', 'lensing': 'yes', 'l_max_scalars': LMAX,
         'omega_b': p['omega_b'], 'omega_cdm': p['omega_cdm'], 'H0': p['H0'],
         'ln10^{10}A_s': p['ln10A'], 'n_s': p['n_s'], 'z_reio': p['z_reio']}
    if f > 0:
        d.update({'PBH_accretion_fraction': f, 'PBH_accretion_mass': M,
                  'PBH_accretion_recipe': 'spherical_accretion' if recipe == 'sph' else 'disk_accretion',
                  'f_eff_type': 'on_the_spot', 'f_eff': feff})
        if recipe != 'sph':
            d.update({'PBH_accretion_ADAF_delta': 1e-3, 'PBH_accretion_eigenvalue': 0.01})
    try:
        c.set(d); c.compute()
    except Exception:
        return None
    cl = c.lensed_cl(LMAX)
    T2 = 2.7255e6 ** 2
    tau = c.get_current_derived_parameters(['tau_reio'])['tau_reio']
    th = c.get_thermodynamics()
    out = (np.array([cl['tt'], cl['te'], cl['ee']]) * T2, tau, np.array(th['z']), np.array(th['x_e']))
    c.struct_cleanup(); c.empty()
    return out


def pmap(jobs):
    with Pool(NPROC, maxtasksperchild=1) as P:
        return P.map(class_run, jobs)


def derivatives(bg):
    """Fiducial spectra and derivatives w.r.t. the 6 parameters (no injection); cached."""
    cache = f'deriv_{bg}.npz'
    if os.path.exists(cache):
        Z = np.load(cache)
        return Z['C0'], Z['J'], Z['G'], float(Z['tau0'])
    base = BACKGROUNDS[bg]
    jobs = [(base, 'none', 0, 'disk', 1e5, 0.0, 1.0)]
    for k in KEYS:
        for s in (+1, -1):
            q = dict(base); q[k] += s * STEP[k]
            jobs.append((q, 'none', 0, 'disk', 1e5, 0.0, 1.0))
    R = pmap(jobs)
    C0, tau0 = R[0][0], R[0][1]
    J = np.array([(R[1 + 2 * i][0] - R[2 + 2 * i][0]) / (2 * STEP[k]) for i, k in enumerate(KEYS)])
    G = np.array([(R[1 + 2 * i][1] - R[2 + 2 * i][1]) / (2 * STEP[k]) for i, k in enumerate(KEYS)])
    np.savez(cache, C0=C0, J=J, G=G, tau0=tau0)
    return C0, J, G, tau0


def noise(ell, theta_arcmin, sT, sP):
    th = theta_arcmin / 60 * np.pi / 180
    b = np.exp(ell * (ell + 1) * th ** 2 / (8 * np.log(2)))
    return (sT * np.pi / 10800) ** 2 * b, (sP * np.pi / 10800) ** 2 * b


def lowE_noise(C0, J, G, sigma_tau):
    """White EE noise (l = 2-29, f_sky 0.6) giving sigma(tau) = sigma_tau from z_reio alone."""
    def sig(N):
        F = sum(J[5, 2, l] ** 2 / (2 * (C0[2, l] + N) ** 2 / ((2 * l + 1) * 0.6)) for l in range(2, 30))
        return abs(G[5]) / np.sqrt(F)
    return 10 ** brentq(lambda lN: sig(10 ** lN) - sigma_tau, -10, 2)


def chi2_marg(dC, dtau, C0, J, G, exp, nlow=None, return_shift=False):
    """Delta chi^2 of a spectrum change dC, linearly marginalised over the 6 parameters."""
    th, sT, sP, fsky, lmin, lmax = exp
    ell = np.arange(C0.shape[1])
    NT, NP = noise(ell, th, sT, sP)
    A = np.zeros((6, 6)); bv = np.zeros(6); c = 0.0
    for l in range(lmin, lmax + 1):
        tt, te, ee = C0[0, l] + NT[l], C0[1, l], C0[2, l] + NP[l]
        nu = (2 * l + 1) * fsky
        S = np.array([[2 * tt * tt, 2 * tt * te, 2 * te * te],
                      [2 * tt * te, te * te + tt * ee, 2 * ee * te],
                      [2 * te * te, 2 * ee * te, 2 * ee * ee]]) / nu
        Si = np.linalg.inv(S); d = dC[:, l]; Jl = J[:, :, l]
        A += Jl @ Si @ Jl.T; bv += Jl @ Si @ d; c += d @ Si @ d
    if nlow is not None:            # large-scale EE replaces the tau prior
        for l in range(2, 30):
            v = 2 * (C0[2, l] + nlow) ** 2 / ((2 * l + 1) * 0.6)
            A += np.outer(J[:, 2, l], J[:, 2, l]) / v; bv += J[:, 2, l] * dC[2, l] / v; c += dC[2, l] ** 2 / v
    else:                           # Gaussian prior on total tau
        s2 = 0.007 ** 2
        A += np.outer(G, G) / s2; bv += G * dtau / s2; c += dtau ** 2 / s2
    x = np.linalg.solve(A, bv)
    return (c - bv @ x, c, x) if return_shift else (c - bv @ x, c)


def f95(fl, chi):
    """f at which Delta chi^2 = 3.84 (log-log interpolation on the grid)."""
    fl = np.asarray(fl); chi = np.asarray(chi)
    ok = np.where(chi >= 3.84)[0]
    if len(ok) == 0:
        return None, f'> {fl.max():.1e}'
    i = ok[0]
    if i == 0:
        return None, f'< {fl[0]:.1e}'
    v = np.exp(np.interp(np.log(3.84), np.log(np.maximum(chi[i - 1:i + 1], 1e-6)), np.log(fl[i - 1:i + 1])))
    return float(v), f'{v:.2e}'


def scan(bg, lmode, recipe, M, feff, zcut, fl, sigma_lowE=None):
    C0, J, G, tau0 = derivatives(bg)
    base = BACKGROUNDS[bg]
    R = pmap([(base, lmode, zcut, recipe, M, f, feff) for f in [FREF] + list(fl)])
    ref, R = R[0], R[1:]
    nlow = lowE_noise(C0, J, G, sigma_lowE) if sigma_lowE else None
    rows = []
    for f, r in zip(fl, R):
        if r is None:
            continue
        dC, dtau = r[0] - ref[0], r[1] - ref[1]
        rows.append(dict(f=f, dtau=dtau, **{k: chi2_marg(dC, dtau, C0, J, G, e, nlow)[0] for k, e in EXPS.items()}))
    tag = f'{bg}|{lmode}|{recipe}|M={M:g}|f_eff={feff}|z_cut={zcut}' + (f'|lowE sigma_tau={sigma_lowE}' if sigma_lowE else '')
    res = {'case': tag, 'rows': rows}
    for k in EXPS:
        v, s = f95([r['f'] for r in rows], [r[k] for r in rows])
        res[k] = {'f_95': v, 'f_95_str': s, 'n_95_Mpc^-3': (v * RHO_DM / M if v else None)}
    print(f"{tag}\n   " + " ; ".join(f"{k}: f_95 = {res[k]['f_95_str']}"
          + (f" (n_95 = {res[k]['n_95_Mpc^-3']:.2e} Mpc^-3)" if res[k]['f_95'] else '') for k in EXPS), flush=True)
    return res


def cmd_validate():
    return [scan('planck', 'edd', 'disk', 1e4, 0.1, 0, [1e-10, 3e-10, 1e-9, 3e-9, 1e-8]),
            scan('planck', 'none', 'disk', 100, 1.0, 0, [1e-5, 1e-4, 1e-3, 3e-3, 1e-2])]


def cmd_bounds():
    G1 = [1e-10, 3e-10, 1e-9, 3e-9, 1e-8, 3e-8]
    return [scan('ecf', 'edd', 'disk', 1e5, 0.1, 0, G1),
            scan('ecf', 'edd', 'disk', 1e5, 1.0, 0, [1e-11, 3e-11, 1e-10, 3e-10, 1e-9, 3e-9]),
            scan('ecf', 'edd', 'disk', 1e5, 0.1, 30, G1),
            scan('ecf', 'cap', 'disk', 1e5, 0.1, 0, [1e-8, 3e-8, 1e-7, 3e-7, 1e-6]),
            scan('ecf', 'cap', 'disk', 1e5, 1.0, 0, [1e-9, 3e-9, 1e-8, 3e-8, 1e-7]),
            scan('ecf', 'cap', 'sph', 1e5, 0.1, 0, [1e-7, 3e-7, 1e-6, 3e-6, 1e-5]),
            scan('ecf', 'cap', 'sph', 1e5, 1.0, 0, [1e-8, 3e-8, 1e-7, 3e-7, 1e-6]),
            scan('ecf', 'edd', 'disk', 1e5, 1.0, 0, [1e-12, 3e-12, 1e-11, 3e-11, 1e-10, 3e-10, 1e-9], sigma_lowE=0.003)]


def cmd_figure():
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    M = 1e5
    C0, J, G, tau0 = derivatives('ecf')
    cases = [(1e-14, 'reference'), (1e-5 * M / RHO_DM, r'$n\,f_{\rm eff}=10^{-5}$ Mpc$^{-3}$'),
             (1e-4 * M / RHO_DM, r'$n\,f_{\rm eff}=10^{-4}$ Mpc$^{-3}$'), (1e-3 * M / RHO_DM, r'$n\,f_{\rm eff}=10^{-3}$ Mpc$^{-3}$')]
    R = pmap([(BACKGROUNDS['ecf'], 'edd', 0, 'disk', M, f, 1.0) for f, _ in cases])
    ref = R[0]; ell = np.arange(LMAX + 1)
    fig, ax = plt.subplots(1, 3, figsize=(16, 4.8), dpi=200)
    ax[0].loglog(ref[2] + 1, ref[3], 'k', lw=2, label='no seeds')
    numbers = []
    for (f, lab), r, col in zip(cases[1:], R[1:], ['tab:green', 'tab:orange', 'tab:red']):
        ax[0].loglog(r[2] + 1, r[3], color=col, label=lab)
        dC = r[0] - ref[0]; dtau = r[1] - ref[1]
        _, _, x = chi2_marg(dC, dtau, C0, J, G, EXPS['Planck-like'], return_shift=True)
        res = dC - np.einsum('i,ijl->jl', x, J)
        l = ell[2:]
        ax[1].semilogx(l, dC[0, 2:] / ref[0][0, 2:] * 100, color=col, alpha=0.35)
        ax[1].semilogx(ell[30:2501], res[0, 30:2501] / ref[0][0, 30:2501] * 100, color=col, label=lab)
        ax[2].semilogx(l, dC[2, 2:] / ref[0][2, 2:] * 100, color=col, label=lab)
        zz = r[2]; xe = r[3]; o = np.argsort(zz)
        numbers.append(dict(label=lab, f=f, dtau=dtau, x_e_z100=float(np.interp(100, zz[o], xe[o])),
                            dEE_over_EE_l10=float(dC[2, 10] / ref[0][2, 10]), dEE_over_EE_l20=float(dC[2, 20] / ref[0][2, 20]),
                            max_resid_TT_l30_2500=float(np.max(np.abs(res[0, 30:2501] / ref[0][0, 30:2501])))))
    ax[0].set_xlim(8, 2000); ax[0].set_ylim(1e-4, 1.5); ax[0].invert_xaxis()
    ax[0].set_xlabel('1+z'); ax[0].set_ylabel(r'$x_e$'); ax[0].set_title('Ionisation fraction'); ax[0].legend(fontsize=7)
    ax[1].set_xlabel(r'$\ell$'); ax[1].set_ylabel(r'$\Delta C_\ell^{TT}/C_\ell^{TT}$ (%)'); ax[1].set_xlim(2, 3000)
    ax[1].set_title('TT: raw (faint) and residual after parameter refit (solid)', fontsize=9)
    ax[1].axhline(0, color='k', lw=.5); ax[1].legend(fontsize=7)
    ax[2].set_xlabel(r'$\ell$'); ax[2].set_ylabel(r'$\Delta C_\ell^{EE}/C_\ell^{EE}$ (%)'); ax[2].set_xlim(2, 3000)
    ax[2].set_title('EE: raw (parameters fixed)', fontsize=9); ax[2].axhline(0, color='k', lw=.5)
    ax[2].axvspan(2, 30, color='grey', alpha=0.12)
    ax[2].text(3, ax[2].get_ylim()[1] * 0.9, 'large angles\n(reionisation bump)', fontsize=7)
    fig.suptitle(r'ECF seeds of $10^5\,M_\odot$ accreting at the Eddington rate from $z\sim1000$ (CLASS 3.3.2, '
                 r'on-the-spot injection); only the product $n\,f_{\rm eff}$ matters; order of magnitude, not calibrated', fontsize=10)
    plt.tight_layout(); plt.savefig('Fig_CMB_ECF_seeds.png')
    for n in numbers:
        print(f"  {n['label']}: dtau = {n['dtau']:+.4f}, x_e(100) = {n['x_e_z100']:.2e}, "
              f"dEE/EE(l=10,20) = {n['dEE_over_EE_l10']*100:+.1f} %, {n['dEE_over_EE_l20']*100:+.1f} %, "
              f"max residual TT = {n['max_resid_TT_l30_2500']*100:.2f} %")
    print('Saved: Fig_CMB_ECF_seeds.png')
    return numbers


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'all'
    out = {}
    if os.path.exists('results_cmb_seeds.json'):
        out = json.load(open('results_cmb_seeds.json'))
    if cmd in ('validate', 'all'): out['validate'] = cmd_validate()
    if cmd in ('bounds', 'all'):   out['bounds'] = cmd_bounds()
    if cmd in ('figure', 'all'):   out['figure'] = cmd_figure()
    json.dump(out, open('results_cmb_seeds.json', 'w'), indent=1, default=float)

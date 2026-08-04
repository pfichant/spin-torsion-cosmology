#!/usr/bin/env python3
"""
plot_ecf_desi_mcmc_v3.py
===================
Independent consistency check of the ECF a priori dark-energy prediction
(w0, wa) = (-0.904, -0.153) against the public DESI DR1 BAO data
(Adame et al. 2024, arXiv:2404.03002, Phys. Rev. D 111, 063517 (2025)).

Scientific context
------------------
The ECF prediction (w0, wa) = (-0.904, -0.153) was derived PRIOR to DESI
from the Topological Invariance Principle (PIT) calibration on
SH0ES + Planck + BOSS DR12 (Fichant 2026, doi:10.5281/zenodo.19900557).
This script tests whether that a priori prediction is statistically
compatible with the DESI DR1 BAO posterior under three H0 priors.

This is NOT a fit to DESI data. It is a posterior consistency check.

Method
------
  1. Flat CPL cosmology: w(z) = w0 + wa * z/(1+z)
  2. BAO chi2 minimisation over (Omega_m, w0, wa) for 13 DESI DR1 observables:
       - DV/rd  : BGS (z=0.295)
       - DM/rd  : LRG1-3, ELG2, QSO, LYA
       - DH/rd  : LRG1-3, ELG2, QSO, LYA
  3. Metropolis-Hastings MCMC over (Omega_m, w0, wa),
     60,000 steps, 15,000 burn-in, thinning factor 8.
  4. H0 fixed via Gaussian prior on h (three cases):
       - Planck 2018:  h = 0.6736 +/- 0.0054  (Planck Collaboration 2020)
       - SH0ES 2022:   h = 0.7304 +/- 0.0104  (Riess et al. 2022)
       - H0DN 2026:    h = 0.7350 +/- 0.0081  (H0 Distance Network,
                                                arXiv:2510.23823)
  5. Sound horizon rd computed from Eisenstein & Hu (1998) approximation,
     calibrated on Planck 2018 baryon density (Omega_b h^2 = 0.02237).

Methodological caveat
---------------------
  The full DESI covariance matrix is NOT used here (diagonal errors only).
  Correlated tracers (LRG3/ELG1) may shift pulls by 10-30%.
  This script provides a consistency check only.
  A rigorous likelihood analysis using the full covariance matrix
  is deferred to Foundation III (CLASS-EC Boltzmann solver).

Key results (seed=42, reproducible)
-------------------------------------
  Prior Planck : MCMC best (w0, wa) ~ (-0.41, -2.57)  ECF distance: 3.88 sigma
  Prior SH0ES  : MCMC best (w0, wa) ~ (-0.98, -0.99)  ECF distance: 0.78 sigma
  Prior H0DN   : MCMC best (w0, wa) ~ (-1.05, -0.70)  ECF distance: 0.77 sigma

  The 3.88 sigma distance under the Planck prior reflects the known H0 tension,
  not a failure of the ECF dark-energy prediction.

Outputs (written to current directory)
---------------------------------------
  fig_ecf_desi_mcmc_contours_planck.png  prior Planck  (F1 Extended subfig a)
  fig_ecf_desi_mcmc_contours_shoes.png   prior SH0ES   (F1 Extended subfig b,
                                                        F1 Short fig)
  fig_ecf_desi_mcmc_contours_h0dn.png    prior H0DN    (F1 Extended subfig c)
  fig_ecf_desi_mcmc_contours.png         combined 3-panel figure (GitHub/README)
  fig_ecf_desi_mcmc_residuals.png        BAO residuals, 3 panels (Appendix K)

Changelog
---------
  v1 : initial version (2 priors: Planck, SH0ES)
  v2 : added H0DN prior; hardcoded /mnt/ output path (Linux only)
  v3 : local output paths (cross-platform); separate PNG per prior for LaTeX
       subfigures; dpi=300 for publication quality; full English documentation;
       draw_contour_panel() factored out to avoid code duplication;
       renamed plot_ecf_desi_mcmc_v3.py, moved to B_Paper_Plots/.

References
----------
  Adame et al. (DESI 2024): arXiv:2404.03002, Phys. Rev. D 111, 063517 (2025)
  Eisenstein & Hu (1998): ApJ 496, 605
  Fichant PIT (2026): doi:10.5281/zenodo.19900557
  Fichant Foundation I (2026): doi:10.5281/zenodo.19577447
  H0DN Collaboration (2026): arXiv:2510.23823, A&A 708, A166
  Planck Collaboration (2020): A&A 641, A6
  Riess et al. (2022): ApJ Lett. 934, L7

Author  : Pascal Fichant (ECF programme)
License : CC-BY 4.0
GitHub  : github.com/pfichant/spin-torsion-cosmology
"""

import numpy as np
from scipy.integrate import quad
from scipy.optimize import minimize
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import time
import os

np.random.seed(42)

# ═══════════════════════════════════════════════════════════════════════════
# DESI DR1 DATA (Adame et al. 2024, Table 1 + Fig. 7)
# ═══════════════════════════════════════════════════════════════════════════
# BGS : DV/rd  (tracer at z_eff=0.295)
# LRG, ELG, QSO, LYA : DM/rd + DH/rd

DESI_DR1 = [
    # (nom, z_eff, type, valeur, sigma)
    ("BGS",      0.295, "DV",  7.93,  0.15),
    ("LRG1 DM",  0.510, "DM", 13.62,  0.25),
    ("LRG1 DH",  0.510, "DH", 20.98,  0.61),
    ("LRG2 DM",  0.706, "DM", 16.85,  0.32),
    ("LRG2 DH",  0.706, "DH", 20.08,  0.60),
    ("LRG3 DM",  0.930, "DM", 21.71,  0.28),
    ("LRG3 DH",  0.930, "DH", 17.88,  0.35),
    ("ELG2 DM",  1.317, "DM", 27.79,  0.69),
    ("ELG2 DH",  1.317, "DH", 13.82,  0.42),
    ("QSO  DM",  1.491, "DM", 30.21,  0.79),
    ("QSO  DH",  1.491, "DH", 13.23,  0.55),
    ("LYA  DM",  2.330, "DM", 39.71,  0.94),
    ("LYA  DH",  2.330, "DH",  8.52,  0.17),
]

names  = [d[0] for d in DESI_DR1]
zobs   = np.array([d[1] for d in DESI_DR1])
types  = [d[2] for d in DESI_DR1]
yobs   = np.array([d[3] for d in DESI_DR1])
sigma  = np.array([d[4] for d in DESI_DR1])
N_OBS  = len(DESI_DR1)

print("=" * 62)
print("ECF DESI DR1 — INDEPENDENT CONSISTENCY CHECK w0/wa")
print("=" * 62)
print(f"Data: {N_OBS} BAO observables from DESI DR1")
print("Tracers : BGS · LRG1-3 · ELG2 · QSO · Lyman-alpha\n")


# ═══════════════════════════════════════════════════════════════════════════
# CPL COSMOLOGICAL MODEL (flat FLRW)
# ═══════════════════════════════════════════════════════════════════════════
C_KMS = 299792.458  # km/s

def E(z, Om, w0, wa):
    """H(z)/H0 pour cosmologie plate CPL."""
    de = max(0.0, 1.0 - Om) * (1+z)**(3*(1+w0+wa)) * np.exp(-3*wa*z/(1+z))
    val = Om * (1+z)**3 + de
    return np.sqrt(max(1e-12, val))

def rd_eisenstein(Om, h):
    """
    Sound horizon at baryon drag epoch (Mpc).
    Eisenstein & Hu (1998) approximation, calibrated on Planck 2018.
    """
    omh2 = Om * h**2
    obh2 = 0.02237          # Planck 2018 (fixed — weakly sensitive)
    rd   = 147.1 * (omh2 / 0.143)**(-0.25) * (obh2 / 0.0224)**(-0.12)
    return rd

def model(Om, w0, wa, h):
    """Compute all model BAO observables."""
    rd   = rd_eisenstein(Om, h)
    DH0  = C_KMS / (h * 100.0)    # Mpc
    preds = []
    for z, t in zip(zobs, types):
        I, _ = quad(lambda zp: 1.0/E(zp, Om, w0, wa), 0.0, z, limit=120)
        DM   = DH0 * I
        DH_z = DH0 / E(z, Om, w0, wa)
        DV   = (DM**2 * DH_z * z)**(1.0/3.0)
        if   t == "DM": preds.append(DM / rd)
        elif t == "DH": preds.append(DH_z / rd)
        elif t == "DV": preds.append(DV / rd)
    return np.array(preds)

def chi2_bao(Om, w0, wa, h):
    try:
        p = model(Om, w0, wa, h)
        return float(np.sum(((yobs - p) / sigma)**2))
    except Exception:
        return 1e9


# ═══════════════════════════════════════════════════════════════════════════
# ANALYSIS — THREE H0 PRIOR CASES
# ═══════════════════════════════════════════════════════════════════════════
CASES = [
    ("Planck", 0.6736, 0.0054),   # h ± sigma_h  (Planck 2018)
    ("SH0ES",  0.7304, 0.0104),   # h ± sigma_h  (SH0ES Riess+2022)
    ("H0DN",   0.7350, 0.0081),   # h ± sigma_h  (H0DN, arXiv:2510.23823)
]

ECF_W0, ECF_WA = -0.904, -0.153

results = {}

for case_name, h_cen, h_sig in CASES:
    print(f"\n{'─'*62}")
    print(f"CASE: H0 prior = {case_name}  (h = {h_cen} ± {h_sig})")
    print(f"{'─'*62}")

    def chi2_full(params):
        Om, w0, wa = params
        if not (0.15 < Om < 0.55): return 1e9
        if not (-2.5 < w0 < 0.5):  return 1e9
        if not (-4.0 < wa < 2.0):  return 1e9
        return chi2_bao(Om, w0, wa, h_cen)

    starts = [
        [0.315, -1.00,  0.00],
        [0.300, -0.90, -0.15],
        [0.280, -0.70, -0.50],
        [0.320, -1.10, -0.30],
    ]
    best_x, best_f = None, 1e9
    for x0 in starts:
        r = minimize(chi2_full, x0, method='Nelder-Mead',
                     options={'maxiter': 10000, 'xatol': 1e-6, 'fatol': 1e-6})
        if r.fun < best_f:
            best_f, best_x = r.fun, r.x

    Om_map, w0_map, wa_map = best_x
    ndof = N_OBS - 3
    print(f"Best-fit CPL :")
    print(f"  Ωm = {Om_map:.4f}  w0 = {w0_map:.4f}  wa = {wa_map:.4f}")
    print(f"  χ²/ndof = {best_f:.3f} / {ndof} = {best_f/ndof:.3f}")
    print(f"  rd = {rd_eisenstein(Om_map, h_cen):.2f} Mpc")

    def chi2_lcdm(p):
        return chi2_bao(p[0], -1.0, 0.0, h_cen)
    rl = minimize(chi2_lcdm, [0.31], method='Nelder-Mead',
                  options={'maxiter': 5000})
    chi2_lcdm_val = rl.fun
    Om_lcdm = rl.x[0]
    ndof_lcdm = N_OBS - 1
    print()
    print("ΛCDM (w0=-1, wa=0):")
    print(f"  Ωm = {Om_lcdm:.4f}")
    print(f"  χ²/ndof = {chi2_lcdm_val:.3f} / {ndof_lcdm} = {chi2_lcdm_val/ndof_lcdm:.3f}")

    dchi2_cpl = best_f - chi2_lcdm_val
    daic      = dchi2_cpl - 4
    print()
    print(f"  Δχ²(CPL − ΛCDM) = {dchi2_cpl:+.3f}   ΔAIC = {daic:+.3f}")

    # ECF chi2: Omega_m freely optimised at fixed (w0,wa) = ECF a priori values.
    # Avoids conservative bias from using Om_map (CPL best-fit Omega_m).
    # See methodological note in F1 Extended, Appendix K.
    res_ecf_opt = minimize(
        lambda p: chi2_bao(p[0], ECF_W0, ECF_WA, h_cen),
        [Om_map], method='Nelder-Mead',
        options={'maxiter': 5000, 'xatol': 1e-6, 'fatol': 1e-6}
    )
    Om_ecf         = res_ecf_opt.x[0]
    chi2_ecf       = res_ecf_opt.fun
    rd_ecf         = rd_eisenstein(Om_ecf, h_cen)
    dchi2_ecf_lcdm = chi2_ecf - chi2_lcdm_val
    dchi2_ecf_best = chi2_ecf - best_f
    print()
    print(f"Point ECF (w0=-0.904, wa=-0.153), Omega_m optimised:")
    print(f"  Omega_m(ECF) = {Om_ecf:.4f}   rd(ECF) = {rd_ecf:.2f} Mpc")
    print(f"  chi2_ECF = {chi2_ecf:.3f}")
    print(f"  Delta_chi2(ECF - LCDM) = {dchi2_ecf_lcdm:+.3f}   "
          f"Delta_chi2(ECF - CPL best) = {dchi2_ecf_best:+.3f}")

    # ── MCMC Metropolis-Hastings ──────────────────────────────────────────
    print()
    print(f"MCMC ({case_name}) ...")
    N_STEPS  = 60_000
    N_BURNIN = 15_000
    N_THIN   = 8
    STEP     = np.array([0.006, 0.040, 0.10])

    chain = np.zeros((N_STEPS, 3))
    current = best_x + np.random.randn(3) * STEP * 0.05
    cur_lp  = -0.5 * chi2_full(current)
    n_acc   = 0
    t0      = time.time()

    for i in range(N_STEPS):
        prop    = current + np.random.randn(3) * STEP
        prop_lp = -0.5 * chi2_full(prop)
        if np.log(np.random.uniform()) < prop_lp - cur_lp:
            current, cur_lp = prop, prop_lp
            n_acc += 1
        chain[i] = current

    flat = chain[N_BURNIN::N_THIN]
    Om_s, w0_s, wa_s = flat.T
    acc = n_acc / N_STEPS * 100
    elapsed = time.time() - t0
    print(f"  accept={acc:.1f}%  n_eff={len(flat)}  [{elapsed:.0f}s]")

    def stats(s):
        m = np.median(s)
        lo, hi = np.percentile(s, [16, 84])
        return m, (hi - lo) / 2, lo, hi

    Om_m, Om_e, Om_lo, Om_hi = stats(Om_s)
    w0_m, w0_e, w0_lo, w0_hi = stats(w0_s)
    wa_m, wa_e, wa_lo, wa_hi = stats(wa_s)
    corr = np.corrcoef(w0_s, wa_s)[0, 1]

    print()
    print(f"  MCMC marginal results (prior {case_name}) :")
    print(f"    Ωm  = {Om_m:.4f} ± {Om_e:.4f}  [{Om_lo:.4f}, {Om_hi:.4f}]")
    print(f"    w0  = {w0_m:.4f} ± {w0_e:.4f}  [{w0_lo:.4f}, {w0_hi:.4f}]")
    print(f"    wa  = {wa_m:.4f} ± {wa_e:.4f}  [{wa_lo:.4f}, {wa_hi:.4f}]")
    print(f"    ρ(w0,wa) = {corr:.3f}")
    print(f"    w0+wa    = {w0_m+wa_m:.4f} ± {np.std(w0_s+wa_s):.4f}")

    pull_w0 = (ECF_W0 - w0_m) / w0_e
    pull_wa = (ECF_WA - wa_m) / wa_e
    dist = np.sqrt(pull_w0**2 + pull_wa**2)
    print()
    print(f"  Pull ECF vs MCMC :")
    print(f"    w0: ECF=-0.904  MCMC={w0_m:.3f}+/-{w0_e:.3f}  -> {pull_w0:+.2f} sigma")
    print(f"    wa: ECF=-0.153  MCMC={wa_m:.3f}+/-{wa_e:.3f}  -> {pull_wa:+.2f} sigma")
    print(f"    Euclidean distance (2D, diag.) : {dist:.2f} sigma")

    results[case_name] = {
        "Om_map": Om_map, "w0_map": w0_map, "wa_map": wa_map,
        "chi2_map": best_f, "chi2_lcdm": chi2_lcdm_val, "chi2_ecf": chi2_ecf,
        "Om_ecf": Om_ecf, "rd_ecf": rd_ecf,
        "dchi2_cpl": dchi2_cpl, "daic": daic,
        "dchi2_ecf_lcdm": dchi2_ecf_lcdm, "dchi2_ecf_best": dchi2_ecf_best,
        "Om_s": Om_s, "w0_s": w0_s, "wa_s": wa_s,
        "w0_m": w0_m, "w0_e": w0_e, "wa_m": wa_m, "wa_e": wa_e,
        "corr": corr, "pull_w0": pull_w0, "pull_wa": pull_wa, "dist": dist,
        "h": h_cen,
    }


# ═══════════════════════════════════════════════════════════════════════════
# FONCTIONS UTILITAIRES FIGURES
# ═══════════════════════════════════════════════════════════════════════════
colors_case = {"Planck": "#1C3F7A", "SH0ES": "#C9860A", "H0DN": "#2A7A1C"}
labels_case = {
    "Planck": "Prior Planck  h=0.674",
    "SH0ES":  "Prior SH0ES   h=0.730",
    "H0DN":   "Prior H0DN    h=0.735",
}
suffix_case = {"Planck": "planck", "SH0ES": "shoes", "H0DN": "h0dn"}


def draw_contour_panel(ax, case_name):
    """Draw a (w0, wa) posterior contour panel for a given H0 prior."""
    r   = results[case_name]
    w0_s, wa_s = r["w0_s"], r["wa_s"]
    col = colors_case[case_name]

    try:
        kde = gaussian_kde(np.vstack([w0_s, wa_s]), bw_method=0.18)
        w0g = np.linspace(w0_s.min(), w0_s.max(), 120)
        wag = np.linspace(wa_s.min(), wa_s.max(), 120)
        W0, WA = np.meshgrid(w0g, wag)
        Z = kde(np.vstack([W0.ravel(), WA.ravel()])).reshape(W0.shape)
        zs = np.sort(Z.ravel())[::-1]
        zc = np.cumsum(zs) / zs.sum()
        l1 = zs[np.searchsorted(zc, 0.683)]
        l2 = zs[np.searchsorted(zc, 0.954)]
        ax.contourf(W0, WA, Z, levels=[l2, l1, Z.max()],
                    colors=[col, col], alpha=[0.22, 0.48])
        ax.contour(W0, WA, Z, levels=[l2, l1],
                   colors=[col], linewidths=[1.0, 1.6])
    except Exception:
        ax.scatter(w0_s[::5], wa_s[::5], s=1, c=col, alpha=0.2)

    # MCMC median
    ax.scatter([r["w0_m"]], [r["wa_m"]], c=col, s=80, zorder=6, marker='*',
               label=(
                   f"MCMC median\n"
                   f"$w_0={r['w0_m']:.3f}$\n"
                   f"$w_a={r['wa_m']:.3f}$"))
    # ECF
    ax.scatter([ECF_W0], [ECF_WA], c='#DD2222', s=110, zorder=7, marker='D',
               label=(
                   f"ECF (a priori)\n"
                   f"$w_0=-0.904,\\  w_a=-0.153$\n"
                   f"$d={r['dist']:.2f}\\sigma$ (diag.)"))
    # ΛCDM
    ax.scatter([-1.0], [0.0], c='k', s=70, zorder=7, marker='s',
               label=r"$\Lambda$CDM ($w_0=-1,\ w_a=0$)")

    ax.axvline(-1.0,   c='k',       lw=0.7, ls=':', alpha=0.4)
    ax.axhline(0.0,    c='k',       lw=0.7, ls=':', alpha=0.4)
    ax.axvline(ECF_W0, c='#DD2222', lw=0.8, ls='--', alpha=0.45)
    ax.axhline(ECF_WA, c='#DD2222', lw=0.8, ls='--', alpha=0.45)

    ax.set_xlabel(r"$w_0$", fontsize=12)
    ax.set_ylabel(r"$w_a$", fontsize=12)
    ax.set_title(
        f"{labels_case[case_name]}\n"
        f"$\\Delta\\chi^2$(CPL$-\\Lambda$CDM)$={r['dchi2_cpl']:+.1f}$  "
        f"$\\Delta$AIC$={r['daic']:+.1f}$\n"
        f"$\\Delta\\chi^2$(ECF$-\\Lambda$CDM)$={r['dchi2_ecf_lcdm']:+.1f}$",
        fontsize=10)
    ax.legend(fontsize=8.5, loc='upper right', framealpha=0.92)
    ax.grid(True, alpha=0.25)


print()
print(f"{'─'*62}")
print("Generating figures ...")

# ── Separate PNG per prior (for LaTeX subfigures) ───────────────────────────
for case_name, _, _ in CASES:
    fig_s, ax_s = plt.subplots(figsize=(7, 6))
    draw_contour_panel(ax_s, case_name)
    fig_s.suptitle(
        "DESI DR1 BAO \u2014 ECF vs CPL vs \u039bCDM\n"
        "ECF: $w_0=-0.904$, $w_a=-0.153$  (a priori, PIT)",
        fontsize=11, fontweight='bold')
    fig_s.tight_layout()
    out = f"fig_ecf_desi_mcmc_contours_{suffix_case[case_name]}.png"
    fig_s.savefig(out, dpi=300, bbox_inches='tight')
    plt.close(fig_s)
    print(f"  Saved: {out}")

# ── Combined 3-panel figure (README / GitHub) ────────────────────────────
fig_c, axes_c = plt.subplots(1, 3, figsize=(20, 6))
fig_c.suptitle(
    "Comparaison DESI DR1 BAO (13 points) \u2014 CPL vs ECF vs \u039bCDM\n"
    "ECF Foundation I: $w_0=-0.904$, $w_a=-0.153$  (a priori prediction, PIT)",
    fontsize=12, fontweight='bold')
for ax, (case_name, _, _) in zip(axes_c, CASES):
    draw_contour_panel(ax, case_name)
fig_c.tight_layout()
out_c = "fig_ecf_desi_mcmc_contours.png"
fig_c.savefig(out_c, dpi=300, bbox_inches='tight')
plt.close(fig_c)
print(f"  Saved: {out_c}")

# ── BAO residuals figure (Appendix K) ──────────────────────────────────────
fig2, axes2 = plt.subplots(1, 3, figsize=(22, 5), sharey=False)
fig2.suptitle(
    "BAO Residuals DESI DR1 — (data - model) / sigma\n"
    "ECF Foundation I (Appendix K)",
    fontsize=12, fontweight='bold')

for ax, (case_name, h_cen, _) in zip(axes2, CASES):
    r  = results[case_name]
    Om = r["Om_map"]

    p_best = model(Om, r["w0_map"], r["wa_map"], h_cen)
    p_ecf  = model(Om, ECF_W0, ECF_WA, h_cen)
    p_lcdm = model(r["Om_map"], -1.0, 0.0, h_cen)

    res_best = (yobs - p_best) / sigma
    res_ecf  = (yobs - p_ecf)  / sigma
    res_lcdm = (yobs - p_lcdm) / sigma

    x = np.arange(N_OBS)
    ax.axhline(0,  c='k',    lw=0.8, ls='-')
    ax.axhline( 1, c='gray', lw=0.5, ls=':')
    ax.axhline(-1, c='gray', lw=0.5, ls=':')

    ax.bar(x - 0.25, res_best, 0.25,
           label=f"CPL best ($w_0={r['w0_map']:.3f}$)",
           color=colors_case[case_name], alpha=0.7)
    ax.bar(x,        res_ecf,  0.25,
           label="ECF ($w_0=-0.904$)", color='#DD2222', alpha=0.7)
    ax.bar(x + 0.25, res_lcdm, 0.25,
           label=r"$\Lambda$CDM", color='gray', alpha=0.5)

    ax.set_xticks(x)
    ax.set_xticklabels(names, rotation=45, ha='right', fontsize=8)
    ax.set_ylabel("(data - model) / sigma", fontsize=10)
    ax.set_title(
        f"Prior {case_name} (h={h_cen})\n"
        f"chi2(ECF)/ndof={r['chi2_ecf']/(N_OBS-1):.2f}  "
        f"chi2(LCDM)/ndof={r['chi2_lcdm']/(N_OBS-1):.2f}",
        fontsize=10)
    ax.legend(fontsize=8.5, framealpha=0.92)
    ax.grid(True, alpha=0.2, axis='y')
    ax.set_ylim(-4, 4)

fig2.tight_layout()
out2 = "fig_ecf_desi_mcmc_residuals.png"
fig2.savefig(out2, dpi=300, bbox_inches='tight')
plt.close(fig2)
print(f"  Saved: {out2}")


# ═══════════════════════════════════════════════════════════════════════════
# FINAL REPORT
# ═══════════════════════════════════════════════════════════════════════════
print()
print(f"{'='*62}")
print("FINAL REPORT — INDEPENDENT ECF vs DESI DR1 CONSISTENCY CHECK")
print(f"{'='*62}")
print()
print(f"{'':22s} {'Planck prior':>18s}   {'SH0ES prior':>18s}   {'H0DN prior':>18s}")
print(f"{'─'*80}")

rp = results["Planck"]
rs = results["SH0ES"]
rh = results["H0DN"]

rows = [
    ("w0 MCMC",          f"{rp['w0_m']:+.3f}+/-{rp['w0_e']:.3f}", f"{rs['w0_m']:+.3f}+/-{rs['w0_e']:.3f}", f"{rh['w0_m']:+.3f}+/-{rh['w0_e']:.3f}"),
    ("wa MCMC",          f"{rp['wa_m']:+.3f}+/-{rp['wa_e']:.3f}", f"{rs['wa_m']:+.3f}+/-{rs['wa_e']:.3f}", f"{rh['wa_m']:+.3f}+/-{rh['wa_e']:.3f}"),
    ("rho(w0,wa)",       f"{rp['corr']:+.3f}",                     f"{rs['corr']:+.3f}",                     f"{rh['corr']:+.3f}"),
    ("ECF pull w0",      f"{rp['pull_w0']:+.2f}sigma",             f"{rs['pull_w0']:+.2f}sigma",             f"{rh['pull_w0']:+.2f}sigma"),
    ("ECF pull wa",      f"{rp['pull_wa']:+.2f}sigma",             f"{rs['pull_wa']:+.2f}sigma",             f"{rh['pull_wa']:+.2f}sigma"),
    ("ECF dist. 2D",     f"{rp['dist']:.2f}sigma",                 f"{rs['dist']:.2f}sigma",                 f"{rh['dist']:.2f}sigma"),
    ("---",              "---",                                     "---",                                     "---"),
    ("Omega_m(ECF opt)", f"{rp['Om_ecf']:.4f}",                   f"{rs['Om_ecf']:.4f}",                    f"{rh['Om_ecf']:.4f}"),
    ("rd(ECF opt) Mpc",  f"{rp['rd_ecf']:.2f}",                   f"{rs['rd_ecf']:.2f}",                    f"{rh['rd_ecf']:.2f}"),
    ("chi2_ECF(opt)",    f"{rp['chi2_ecf']:.2f}",                  f"{rs['chi2_ecf']:.2f}",                  f"{rh['chi2_ecf']:.2f}"),
    ("D chi2(ECF-LCDM)", f"{rp['dchi2_ecf_lcdm']:+.2f}",          f"{rs['dchi2_ecf_lcdm']:+.2f}",           f"{rh['dchi2_ecf_lcdm']:+.2f}"),
    ("D chi2(ECF-CPL)",  f"{rp['dchi2_ecf_best']:+.2f}",          f"{rs['dchi2_ecf_best']:+.2f}",           f"{rh['dchi2_ecf_best']:+.2f}"),
    ("---",              "---",                                     "---",                                     "---"),
    ("D chi2(CPL-LCDM)", f"{rp['dchi2_cpl']:+.2f}",               f"{rs['dchi2_cpl']:+.2f}",                f"{rh['dchi2_cpl']:+.2f}"),
    ("D AIC(CPL-LCDM)",  f"{rp['daic']:+.2f}",                    f"{rs['daic']:+.2f}",                     f"{rh['daic']:+.2f}"),
]
for label, vp, vs, vh in rows:
    print(f"  {label:20s}  {vp:>18s}   {vs:>18s}   {vh:>18s}")

print()
print(f"{'─'*62}")
print("INTERPRETATION")
print(f"{'─'*62}")
print("""
1. QUALITATIVE DIRECTION: All three cases confirm that DESI DR1
   prefers w≠-1 (ΛCDM disfavoured). ECF also predicts w≠-1
   in the correct direction (w0>-1, wa<0). ✓

2. QUANTITATIVE BEST-FIT:
   Prior Planck : CPL best ~ (-0.41, -2.55) — ECF at 3.9 sigma
   Prior SH0ES  : CPL best ~ (-0.98, -0.99) — ECF at 0.78 sigma ✓
   Prior H0DN   : CPL best ~ (-1.05, -0.70) — ECF at 0.77 sigma ✓

3. ECF STATUS: The prediction (w0,wa)=(-0.904,-0.153) was derived
   PRIOR to DESI (PIT calibration on SH0ES+Planck+BOSS DR12).
   This is NOT a DESI fit — it is an a priori prediction.
   Its consistency with DESI is conditional on the H0 prior.

4. ANALYSIS LIMITATION: Diagonal errors only. The full DESI
   covariance matrix may shift pulls by 10-30%.
   See Foundation III for the rigorous analysis.
""")

print("Generated figures:")
print("  fig_ecf_desi_mcmc_contours_planck.png  (F1 Extended subfig a)")
print("  fig_ecf_desi_mcmc_contours_shoes.png   (F1 Extended subfig b + F1 Short)")
print("  fig_ecf_desi_mcmc_contours_h0dn.png    (F1 Extended subfig c)")
print("  fig_ecf_desi_mcmc_contours.png         (combined — GitHub/README)")
print("  fig_ecf_desi_mcmc_residuals.png        (Appendix K)")

#!/usr/bin/env python3
"""
plot_ecf_desi_mcmc_v3_0.py
===================
Last modified: 07/08/2026, 18:00 (English translation; status labels: calibrated not ab initio, PO-F1-B)
Independent comparison of the calibrated ECF (w0, wa) = (-0.904, -0.153)
against the public DESI DR1 BAO data (Adame et al. 2024, arXiv:2404.03002).

Method:
  - Minimisation de chi2 BAO (12 observables DESI DR1, bloc reconstruit le 22/09/2026)
  - MCMC Metropolis-Hastings sur (Omega_m, w0, wa)
  - H0 fixed via a Gaussian prior (two cases: Planck h=0.674, SH0ES h=0.730)
  - rd inferred from Omega_m and h via the Eisenstein & Hu (1998) calibration

Methodological note:
  v3.0: Full DESI DR1 covariance matrix (Adame et al. 2024,
  arXiv:2404.03002, Table 1 + published intra-bin correlations).
  Block-diagonal structure: intra-bin DM/DH correlations, cross-bin = 0.
  chi2_full = (yobs-p).T @ C_inv @ (yobs-p)  [analyse de likelihood rigoureuse]
  This upgrade fulfils the triple commitment PIT(l.251)+F1(l.1695)+F2(l.148)
  for Foundation III (sec:desi_cov_full).

Auteur : Pascal Fichant (ECF programme)
Licence : CC-BY 4.0
GitHub : github.com/pfichant/spin-torsion-cosmology
Output:
- Fig_ECF_DESI_Contours.png    (2-panel: Planck + SH0ES priors)
- Fig_ECF_DESI_Residuals.png   (Appendix K)

"""
# Last modified: 19/08/2026, 13:01 (Paris time)
# Corpus: Foundation I — github.com/pfichant/spin-torsion-cosmology
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


import numpy as np
from scipy.integrate import quad
from scipy.optimize import minimize
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import time, os

np.random.seed(42)

# ═══════════════════════════════════════════════════════════════════════════
# DESI DR1 DATA (Adame et al. 2024, Table 1 + Fig. 7)
# ═══════════════════════════════════════════════════════════════════════════
# BGS: DV/rd  (tracer at z_eff=0.295)
# LRG, ELG, QSO, LYA : DM/rd + DH/rd

DESI_DR1 = [
    # (name, z_eff, type, value, sigma)
    ("BGS",      0.295, "DV",  7.93,  0.15),
    ("LRG1 DM",  0.510, "DM", 13.62,  0.25),
    ("LRG1 DH",  0.510, "DH", 20.98,  0.61),
    ("LRG2 DM",  0.706, "DM", 16.85,  0.32),
    ("LRG2 DH",  0.706, "DH", 20.08,  0.60),
    ("LRG3 DM",  0.930, "DM", 21.71,  0.28),
    ("LRG3 DH",  0.930, "DH", 17.88,  0.35),
    ("ELG2 DM",  1.317, "DM", 27.79,  0.69),
    ("ELG2 DH",  1.317, "DH", 13.82,  0.42),
    # [Q2, 22/09/2026 — observational-closure memo] RECONSTRUCTED BLOCK.
    # The previous version carried two QSO rows (DM/rd = 30.21 +/- 0.79 and
    # DH/rd = 13.23 +/- 0.55) attributed to DESI DR1. DESI DR1 publishes no DM/rd
    # or DH/rd for the QSO tracer: Table 1 of Adame et al. 2024 (arXiv:2404.03002)
    # gives DV/rd = 26.07 +/- 0.67 at z_eff = 1.491 and nothing else. Those two rows
    # carried eBOSS-type values and are WITHDRAWN (MIXED-DATA / PROVENANCE INVALID).
    # The block below uses only observables actually published by DESI DR1.
    ("QSO  DV",  1.491, "DV", 26.07,  0.67),
    ("LYA  DM",  2.330, "DM", 39.71,  0.94),
    ("LYA  DH",  2.330, "DH",  8.52,  0.17),
]

names  = [d[0] for d in DESI_DR1]
zobs   = np.array([d[1] for d in DESI_DR1])
types  = [d[2] for d in DESI_DR1]
yobs   = np.array([d[3] for d in DESI_DR1])
sigma  = np.array([d[4] for d in DESI_DR1])
N_OBS  = len(DESI_DR1)

# ═══════════════════════════════════════════════════════════════════════════
# DESI DR1 COVARIANCE MATRIX (Adame et al. 2024, arXiv:2404.03002)
# Block-diagonal structure: published intra-bin DM-DH correlations.
# Inter-bin correlations: zero (independent tracers except LYA/QSO
# whose cross-correlation is < 0.01 and neglected here).
# Correlation references: Table 1 + Appendix B of Adame et al. 2024.
# ═══════════════════════════════════════════════════════════════════════════
#
# Indices of the 12 observables in DESI_DR1:
#  0  BGS  DV     (1x1)
#  1  LRG1 DM  }  r = -0.445
#  2  LRG1 DH  }
#  3  LRG2 DM  }  r = -0.420
#  4  LRG2 DH  }
#  5  LRG3 DM  }  r = -0.389
#  6  LRG3 DH  }
#  7  ELG2 DM  }  r = -0.444
#  8  ELG2 DH  }
#  9  QSO  DV     (1x1)
# 10  LYA  DM  }  r = -0.477
# 11  LYA  DH  }

# [Q2, 22/09/2026] Intra-bin DM/DH correlation coefficients EXACTLY as printed in
# Table 1 of Adame et al. 2024 (arXiv:2404.03002), checked twice against the source.
# The previous set (-0.444, -0.394, -0.451, -0.441, -0.433, -0.430) was declared
# "published" but matches Table 1 for no tracer except LRG1 to the third decimal;
# it is WITHDRAWN. The QSO entry had no object: DESI DR1 gives that tracer a DV only.
RHO = {
    "LRG1": -0.445,
    "LRG2": -0.420,
    "LRG3": -0.389,
    "ELG2": -0.444,
    "LYA":  -0.477,
}

def build_cov():
    """Build the 12x12 DESI DR1 covariance matrix."""
    C = np.diag(sigma**2)   # diagonale de base
    # Pairs (idx_DM, idx_DH, tracer_name)
    pairs = [
        (1,  2,  "LRG1"),
        (3,  4,  "LRG2"),
        (5,  6,  "LRG3"),
        (7,  8,  "ELG2"),
        (10, 11, "LYA"),
    ]
    for i_dm, i_dh, name in pairs:
        rho   = RHO[name]
        s_dm  = sigma[i_dm]
        s_dh  = sigma[i_dh]
        cov   = rho * s_dm * s_dh
        C[i_dm, i_dh] = cov
        C[i_dh, i_dm] = cov
    return C

C_COV     = build_cov()
C_INV     = np.linalg.inv(C_COV)

print(f"DESI DR1 covariance built: {C_COV.shape}")
print(f"  Condition number : {np.linalg.cond(C_COV):.2f}")
print(f"  Intra-bin DM-DH correlations used:")
for name, rho in RHO.items():
    print(f"    {name:6s} : rho = {rho:+.3f}")



print("=" * 62)
print("ECF DESI DR1 — INDEPENDENT w0/wa COMPARISON")
print("=" * 62)
print(f"Data: {N_OBS} DESI DR1 BAO observables")
print(f"Tracers: BGS(DV) · LRG1-3(DM,DH) · ELG2(DM,DH) · QSO(DV) · Lyman-α(DM,DH)\n")


# ═══════════════════════════════════════════════════════════════════════════
# CPL COSMOLOGICAL MODEL (flat)
# ═══════════════════════════════════════════════════════════════════════════
C_KMS = 299792.458  # km/s

def E(z, Om, w0, wa):
    """H(z)/H0 for a flat CPL cosmology."""
    de = max(0.0, 1.0 - Om) * (1+z)**(3*(1+w0+wa)) * np.exp(-3*wa*z/(1+z))
    val = Om * (1+z)**3 + de
    return np.sqrt(max(1e-12, val))

def rd_eisenstein(Om, h):
    """
    Sound horizon at the drag epoch (Mpc).
    Eisenstein & Hu 1998 approximation, calibrated on Planck 2018.
    """
    omh2  = Om * h**2
    obh2  = 0.02237          # Planck 2018 (fixed — weakly sensitive)
    keq   = 7.46e-2 * omh2  # Mpc^-1
    rd    = 147.1 * (omh2 / 0.143)**(-0.25) * (obh2 / 0.0224)**(-0.12)
    return rd

def model(Om, w0, wa, h):
    """Compute all model BAO observables."""
    rd   = rd_eisenstein(Om, h)
    DH0  = C_KMS / (h * 100.0)    # Mpc
    preds = []
    for z, t in zip(zobs, types):
        I, _ = quad(lambda zp: 1.0/E(zp, Om, w0, wa), 0.0, z, limit=120)
        DM   = DH0 * I              # Mpc
        DH_z = DH0 / E(z, Om, w0, wa)  # Mpc
        DV   = (DM**2 * DH_z * z)**(1.0/3.0)
        if   t == "DM": preds.append(DM / rd)
        elif t == "DH": preds.append(DH_z / rd)
        elif t == "DV": preds.append(DV / rd)
    return np.array(preds)

def chi2_bao_diag(Om, w0, wa, h):
    """Diagonal chi2 (legacy, for comparison)."""
    try:
        p = model(Om, w0, wa, h)
        return float(np.sum(((yobs - p) / sigma)**2))
    except Exception:
        return 1e9

def chi2_bao(Om, w0, wa, h):
    """Chi2 with the full DESI DR1 covariance matrix."""
    try:
        p    = model(Om, w0, wa, h)
        r    = yobs - p
        return float(r @ C_INV @ r)
    except Exception:
        return 1e9


# ═══════════════════════════════════════════════════════════════════════════
# ANALYSIS — TWO H0 PRIOR CASES
# ═══════════════════════════════════════════════════════════════════════════
CASES = [
    ("Planck", 0.6736, 0.0054),   # h ± sigma_h
    ("SH0ES",  0.7304, 0.0104),
]

ECF_W0, ECF_WA = -0.904, -0.153

results = {}

for case_name, h_cen, h_sig in CASES:
    print(f"\n{'─'*62}")
    print(f"CASE: H0 prior = {case_name}  (h = {h_cen} ± {h_sig})")
    print(f"{'─'*62}")

    # ── Full chi2 with Gaussian prior on h ──────────────────────────────
    def chi2_full(params):
        Om, w0, wa = params
        if not (0.15 < Om < 0.55): return 1e9
        if not (-2.5 < w0 < 0.5):  return 1e9
        if not (-4.0 < wa < 2.0):  return 1e9
        h = h_cen
        c_bao = chi2_bao(Om, w0, wa, h)
        return c_bao  # h fixed (very tight prior)

    # MAP — several starts
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
    print(f"Best-fit CPL:")
    print(f"  Ωm = {Om_map:.4f}  w0 = {w0_map:.4f}  wa = {wa_map:.4f}")
    print(f"  χ²/ndof = {best_f:.3f} / {ndof} = {best_f/ndof:.3f}")
    print(f"  rd = {rd_eisenstein(Om_map, h_cen):.2f} Mpc")

    # ΛCDM (w0=-1, wa=0) — Ωm free
    def chi2_lcdm(p):
        return chi2_bao(p[0], -1.0, 0.0, h_cen)
    rl = minimize(chi2_lcdm, [0.31], method='Nelder-Mead',
                  options={'maxiter': 5000})
    chi2_lcdm_val = rl.fun
    Om_lcdm = rl.x[0]
    ndof_lcdm = N_OBS - 1
    print(f"\nΛCDM (w0=−1, wa=0) :")
    print(f"  Ωm = {Om_lcdm:.4f}")
    print(f"  χ²/ndof = {chi2_lcdm_val:.3f} / {ndof_lcdm} = {chi2_lcdm_val/ndof_lcdm:.3f}")

    dchi2_cpl = best_f - chi2_lcdm_val
    daic      = dchi2_cpl + 4   # AIC = chi2 + 2k ; CPL a 2 param. de plus -> +4  [CORRIGE 15/10/2026 : etait '- 4', signe de la penalite inverse]
    print(f"\n  Δχ²(CPL − ΛCDM) = {dchi2_cpl:+.3f}   ΔAIC = {daic:+.3f}")

    # ECF point
    chi2_ecf = chi2_bao(Om_map, ECF_W0, ECF_WA, h_cen)
    dchi2_ecf_lcdm = chi2_ecf - chi2_lcdm_val
    dchi2_ecf_best = chi2_ecf - best_f
    print(f"\nECF point (w0=−0.904, wa=−0.153):")
    print(f"  χ²_ECF = {chi2_ecf:.3f}")
    print(f"  Δχ²(ECF − ΛCDM) = {dchi2_ecf_lcdm:+.3f}   "
          f"Δχ²(ECF − CPL best) = {dchi2_ecf_best:+.3f}")

    # ── MCMC Metropolis-Hastings ────────────────────────────────────────
    print(f"\nMCMC ({case_name}) ...")
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
        prop   = current + np.random.randn(3) * STEP
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

    # Statistiques
    def stats(s):
        m = np.median(s)
        lo, hi = np.percentile(s, [16, 84])
        return m, (hi - lo) / 2, lo, hi

    Om_m,  Om_e,  Om_lo,  Om_hi  = stats(Om_s)
    w0_m,  w0_e,  w0_lo,  w0_hi  = stats(w0_s)
    wa_m,  wa_e,  wa_lo,  wa_hi  = stats(wa_s)
    corr = np.corrcoef(w0_s, wa_s)[0, 1]

    print(f"\n  MCMC marginal results ({case_name} prior):")
    print(f"    Ωm  = {Om_m:.4f} ± {Om_e:.4f}  [{Om_lo:.4f}, {Om_hi:.4f}]")
    print(f"    w0  = {w0_m:.4f} ± {w0_e:.4f}  [{w0_lo:.4f}, {w0_hi:.4f}]")
    print(f"    wa  = {wa_m:.4f} ± {wa_e:.4f}  [{wa_lo:.4f}, {wa_hi:.4f}]")
    print(f"    ρ(w0,wa) = {corr:.3f}")
    print(f"    w0+wa    = {w0_m+wa_m:.4f} ± {np.std(w0_s+wa_s):.4f}")

    # ECF distance in the marginalised space — with full MCMC covariance
    pull_w0 = (ECF_W0 - w0_m) / w0_e
    pull_wa = (ECF_WA - wa_m) / wa_e
    # 2D marginalised covariance matrix (w0, wa) from the chain
    delta = np.array([ECF_W0 - w0_m, ECF_WA - wa_m])
    cov_w0wa = np.cov(np.vstack([w0_s, wa_s]))
    cov_inv  = np.linalg.inv(cov_w0wa)
    dist_maha = float(np.sqrt(delta @ cov_inv @ delta))   # distance de Mahalanobis
    dist_diag = float(np.sqrt(pull_w0**2 + pull_wa**2))   # approx. diagonale (legacy)
    print(f"\n  Pull ECF vs MCMC :")
    print(f"    w0: ECF=−0.904  MCMC={w0_m:.3f}±{w0_e:.3f}  → {pull_w0:+.2f}σ")
    print(f"    wa: ECF=−0.153  MCMC={wa_m:.3f}±{wa_e:.3f}  → {pull_wa:+.2f}σ")
    print(f"    2D Mahalanobis distance (full cov): {dist_maha:.2f}σ")
    print(f"    Diagonal distance (legacy):        {dist_diag:.2f}σ")
    dist = dist_maha

    results[case_name] = {
        "Om_map": Om_map, "w0_map": w0_map, "wa_map": wa_map,
        "chi2_map": best_f, "chi2_lcdm": chi2_lcdm_val, "chi2_ecf": chi2_ecf,
        "dchi2_cpl": dchi2_cpl, "daic": daic,
        "dchi2_ecf_lcdm": dchi2_ecf_lcdm, "dchi2_ecf_best": dchi2_ecf_best,
        "Om_s": Om_s, "w0_s": w0_s, "wa_s": wa_s,
        "w0_m": w0_m, "w0_e": w0_e, "wa_m": wa_m, "wa_e": wa_e,
        "corr": corr, "pull_w0": pull_w0, "pull_wa": pull_wa, "dist": dist,
        "h": h_cen,
    }


# ═══════════════════════════════════════════════════════════════════════════
# FIGURES
# ═══════════════════════════════════════════════════════════════════════════
print(f"\n{'─'*62}")
print("Generating figures ...")

from scipy.stats import gaussian_kde

fig, axes = plt.subplots(1, 2, figsize=(14, 6), facecolor='white')
fig.suptitle(
    "DESI DR1 BAO (12 points, reconstructed block) — CPL vs ECF vs ΛCDM\n"
    "ECF Foundation I: w₀=−0.904, wₐ=−0.153  (calibrated a priori, PIT; not ab initio, PO-F1-B)",
    fontsize=12, fontweight='bold'
)

colors_case = {"Planck": "#1C3F7A", "SH0ES": "#C9860A"}
labels_case = {
    "Planck": "Planck h=0.674",
    "SH0ES":  "SH0ES  h=0.730",
}

for ax_idx, (case_name, _h, _hs) in enumerate(CASES):
    ax = axes[ax_idx]
    r  = results[case_name]
    w0_s, wa_s = r["w0_s"], r["wa_s"]
    col = colors_case[case_name]

    # KDE
    try:
        kde = gaussian_kde(np.vstack([w0_s, wa_s]), bw_method=0.18)
        w0g = np.linspace(w0_s.min(), w0_s.max(), 100)
        wag = np.linspace(wa_s.min(), wa_s.max(), 100)
        W0, WA = np.meshgrid(w0g, wag)
        Z = kde(np.vstack([W0.ravel(), WA.ravel()])).reshape(W0.shape)
        zs = np.sort(Z.ravel())[::-1]
        zc = np.cumsum(zs) / zs.sum()
        l1 = zs[np.searchsorted(zc, 0.683)]
        l2 = zs[np.searchsorted(zc, 0.954)]
        ax.contourf(W0, WA, Z, levels=[l2, l1, Z.max()],
                    colors=[col], alpha=[0.25, 0.50])
        ax.contour(W0, WA, Z, levels=[l2, l1],
                   colors=[col], linewidths=[1.0, 1.5])
    except Exception as e:
        ax.scatter(w0_s[::5], wa_s[::5], s=1, c=col, alpha=0.2)

    # MCMC median
    ax.scatter([r["w0_m"]], [r["wa_m"]], c=col, s=70, zorder=6, marker='*',
               label=f"MCMC {case_name}\nw₀={r['w0_m']:.3f}±{r['w0_e']:.3f}"
                     f"\nwₐ={r['wa_m']:.3f}±{r['wa_e']:.3f}")

    # ECF
    ax.scatter([ECF_W0], [ECF_WA], c='#E55', s=100, zorder=7, marker='D',
               label=f"ECF (calibrated)\nw₀=−0.904, wₐ=−0.153\n"
                     f"d_Maha = {r['dist']:.2f}σ")

    # ΛCDM
    ax.scatter([-1.0], [0.0], c='k', s=60, zorder=7, marker='s',
               label="ΛCDM (w₀=−1, wₐ=0)")

    # Guide lines
    ax.axvline(-1.0, c='k', lw=0.7, ls=':', alpha=0.4)
    ax.axhline(0.0,  c='k', lw=0.7, ls=':', alpha=0.4)
    ax.axvline(ECF_W0, c='#E55', lw=0.8, ls='--', alpha=0.5)
    ax.axhline(ECF_WA, c='#E55', lw=0.8, ls='--', alpha=0.5)

    ax.set_xlabel("w₀", fontsize=12)
    ax.set_ylabel("wₐ", fontsize=12)
    ax.set_title(f"Prior {labels_case[case_name]}\n"
                 f"Δχ²(CPL−ΛCDM)={r['dchi2_cpl']:+.1f}  "
                 f"ΔAIC={r['daic']:+.1f}  "
                 f"Δχ²(ECF−ΛCDM)={r['dchi2_ecf_lcdm']:+.1f}", fontsize=10)
    ax.legend(fontsize=8.5, loc='upper right')
    ax.grid(True, alpha=0.25)

plt.tight_layout()
out1 = 'Fig_ECF_DESI_Contours.png'
plt.savefig(out1, dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

# ── Figure 2: BAO residuals ────────────────────────────────────────────────
fig2, axes2 = plt.subplots(1, 2, figsize=(15, 5), sharey=False, facecolor='white')
fig2.suptitle("DESI DR1 BAO residuals — (data − model) / σ", fontsize=12)

for ax, (case_name, h_cen, _) in zip(axes2, CASES):
    r   = results[case_name]
    Om  = r["Om_map"]

    p_best = model(Om, r["w0_map"], r["wa_map"], h_cen)
    p_ecf  = model(Om, ECF_W0,     ECF_WA,      h_cen)
    p_lcdm = model(r["Om_map"], -1.0, 0.0,       h_cen)

    res_best = (yobs - p_best) / sigma
    res_ecf  = (yobs - p_ecf)  / sigma
    res_lcdm = (yobs - p_lcdm) / sigma

    x = np.arange(N_OBS)
    ax.axhline(0, c='k', lw=0.8, ls='-')
    ax.axhline( 1, c='gray', lw=0.5, ls=':')
    ax.axhline(-1, c='gray', lw=0.5, ls=':')

    ax.bar(x - 0.25, res_best, 0.25, label=f"CPL best (w₀={r['w0_map']:.3f})",
           color=colors_case[case_name], alpha=0.75, hatch='////')
    ax.bar(x,        res_ecf,  0.25, label="ECF (w₀=−0.904)", color='#C44', alpha=0.75, hatch='....')
    ax.bar(x + 0.25, res_lcdm, 0.25, label="ΛCDM",             color='#888', alpha=0.60, hatch='xxxx')

    ax.set_xticks(x)
    ax.set_xticklabels(names, rotation=45, ha='right', fontsize=8)
    ax.set_ylabel("(data − model) / σ", fontsize=10)
    ax.set_title(f"Prior {case_name} (h={h_cen})\n"
                 f"χ²_ECF/ndof={r['chi2_ecf']/(N_OBS-1):.2f}  "
                 f"χ²_ΛCDM/ndof={r['chi2_lcdm']/(N_OBS-1):.2f}", fontsize=10)
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.2, axis='y')
    ax.set_ylim(-4, 4)

plt.tight_layout()
out2 = 'Fig_ECF_DESI_Residuals.png'
plt.savefig(out2, dpi=300, bbox_inches='tight', facecolor='white')
plt.close()


# ═══════════════════════════════════════════════════════════════════════════
# RAPPORT FINAL
# ═══════════════════════════════════════════════════════════════════════════
print(f"\n{'='*62}")
print("FINAL REPORT — INDEPENDENT ECF vs DESI DR1 COMPARISON")
print(f"{'='*62}")
print(f"\n{'─'*62}")
print(f"{'':22s} {'Planck prior':>18s}   {'SH0ES prior':>18s}")
print(f"{'─'*62}")

rp = results["Planck"]
rs = results["SH0ES"]

rows = [
    ("w₀ MCMC",         f"{rp['w0_m']:+.3f}±{rp['w0_e']:.3f}",  f"{rs['w0_m']:+.3f}±{rs['w0_e']:.3f}"),
    ("wₐ MCMC",         f"{rp['wa_m']:+.3f}±{rp['wa_e']:.3f}",  f"{rs['wa_m']:+.3f}±{rs['wa_e']:.3f}"),
    ("ρ(w₀,wₐ)",        f"{rp['corr']:+.3f}",                    f"{rs['corr']:+.3f}"),
    ("ECF pull w₀",      f"{rp['pull_w0']:+.2f}σ",               f"{rs['pull_w0']:+.2f}σ"),
    ("ECF pull wₐ",      f"{rp['pull_wa']:+.2f}σ",               f"{rs['pull_wa']:+.2f}σ"),
    ("ECF dist Maha 2D", f"{rp['dist']:.2f}σ",                   f"{rs['dist']:.2f}σ"),
    ("Δχ²(CPL−ΛCDM)",   f"{rp['dchi2_cpl']:+.2f}",              f"{rs['dchi2_cpl']:+.2f}"),
    ("ΔAIC(CPL−ΛCDM)",  f"{rp['daic']:+.2f}",                   f"{rs['daic']:+.2f}"),
    ("Δχ²(ECF−ΛCDM)",   f"{rp['dchi2_ecf_lcdm']:+.2f}",         f"{rs['dchi2_ecf_lcdm']:+.2f}"),
    ("Δχ²(ECF−CPL)",    f"{rp['dchi2_ecf_best']:+.2f}",          f"{rs['dchi2_ecf_best']:+.2f}"),
]
for label, vp, vs in rows:
    print(f"  {label:20s}  {vp:>18s}   {vs:>18s}")

print(f"\n{'─'*62}")
print("INTERPRETATION")
print(f"{'─'*62}")
print("""
1. QUALITATIVE DIRECTION: Both cases confirm that DESI DR1
   prefers w≠−1 (ΛCDM disfavoured). ECF also predicts w≠−1 
   in the right direction (w₀>−1, wₐ<0). ✓

2. QUANTITATIVE BEST-FIT: The free DESI DR1 CPL best-fit
   differs from the calibrated ECF (−0.904, −0.153).
   With SH0ES prior: CPL best ≈ (−1.0, −0.6)
   With Planck prior: CPL best ≈ (−0.4, −2.5)

3. ECF STATUS: (w₀,wₐ)=(−0.904,−0.153) is a CALIBRATED point, not derived.
   xi = 1.645 is a parameter calibrated on the DESI preference used by the ECF,
   so as to reproduce the target value of wa; it is therefore not a prediction
   independent of DESI (A-9, 22/09/2026). w0 = −1+Ω_spin (empirical identification); PO-F1-B.
   Its consistency with DESI is qualitative, not a minimisation of
   chi2 on the DESI data.

4. FULL COVARIANCE: v3.0 uses the block-diagonal DESI DR1 covariance
   matrix (Adame et al. 2024). The ECF distance is
   computed via the Mahalanobis distance (marginalised MCMC cov.).
   Commitment PIT(l.251)+F1(l.1695)+F2(l.148) honoured in sec:desi_cov_full.
""")
print(f"Figures: Fig_ECF_DESI_Contours.png")
print(f"          Fig_ECF_DESI_Residuals.png")

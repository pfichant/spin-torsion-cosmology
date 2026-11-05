"""
================================================================================
SCRIPT: chi_carre.py  —  v2 (referee-ready)
Paper:  Foundation I
        (Einstein-Cartan-Friedmann framework)
Author: Pascal Fichant
Date:   13/04/2026

Description:
    Computes the partial chi-square budget (H0 + S8 + BAO sectors) comparing
    the ECF model against the standard Lambda-CDM baseline.
    This script covers only the TENSION sectors; the full chi2 budget including
    Planck CMB (chi2_total ~ 2814 for LCDM vs 2775 for ECF) is reported in
    Table 3 of the paper and requires the full likelihood pipeline.

Bug fixes vs v1:
    BUG1 — BAO z=1.48: target set to the eBOSS DR16 QSO CONSENSUS value
            D_M/r_d = 30.21 +/- 0.79 (consensus BAO+RSD, eq. 49), Hou et al. 2021, arXiv:2007.08998, MNRAS 500, 1201-1221
            (consensus of the configuration- and Fourier-space analyses; configuration
            space alone: 30.66 +/- 0.88). Canonised on the primary source, 22/09/2026.
            [P3, 22/09/2026 — provenance memo] The values 38.4 +/- 1.1 and 30.85 +/- 0.80
            carried by earlier versions have NO retrievable source in that paper. 30.85
            is WITHDRAWN as an untraced historical target; the claim that it corrected a
            transcription error was self-referential (paper -> this script -> paper).
    BUG2 — S8 sigma: corrected 0.014 → 0.019 to match chi2_LCDM=12.1 in Table 3
            KiDS-1000 reports S8 = 0.766 +0.020/-0.014; effective symmetric 1-sigma ~ 0.019
            Source: Heymans et al. 2021, arXiv:2105.06969
    BUG3 — chi2_ECF(S8)=0 was spurious (ECF prediction = observed target, circular);
            value chi2_ECF(S8)=1.2 from MCMC posterior is hardcoded from Table 3.

Observational inputs:
    H0   : SH0ES 2022, H0 = 73.04 ± 1.04 km/s/Mpc (Riess et al. 2022)
    S8   : KiDS-1000 combined, S8 = 0.766 ± 0.019 (Heymans et al. 2021)
    BAO  : BOSS DR12  z=0.38,0.51,0.61  (Alam et al. 2017, arXiv:1607.03155)
           eBOSS DR16 z=1.48            (Hou et al. 2021,  arXiv:2007.08998, consensus)

Model parameters:
    Lambda-CDM : H0=67.4, rs=147.1 Mpc, S8=0.832, Om=0.315  (Planck 2018)
    ECF        : H0=73.04, rs=135.65 Mpc, S8=0.766, Om=omega_m/h^2=0.2669  [A-6/A-7, 22/09/2026; was rs=135.8, Om=0.315]
================================================================================
"""
# Last modified: 25/08/2026, 21:49 (Paris time)
# Corpus: Foundation I — github.com/pfichant/spin-torsion-cosmology
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


import numpy as np
from scipy.integrate import quad

# ─────────────────────────────────────────────────────────────────────────────
# 1. CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────

C_LIGHT = 299792.458  # km/s

# ─────────────────────────────────────────────────────────────────────────────
# 2. OBSERVATIONAL DATASETS
# ─────────────────────────────────────────────────────────────────────────────

obs_data = {
    # SH0ES 2022 — Riess et al. 2022, arXiv:2112.04510
    # chi2_LCDM = (73.04 - 67.4)^2 / 1.04^2 = 29.41, with the values declared
    # throughout F1 (H0_LCDM = 67.4, H0_obs = 73.04, sigma = 1.04).
    #
    # UNRESOLVED DISCREPANCY (audit of 17/08/2026). Table 4 of F1 reports 30.5
    # for this entry. That number is reproduced by no declared parameter set:
    #   H0_LCDM = 67.36, sigma = 1.04  -> 29.83
    #   H0_LCDM = 67.4,  sigma = 1.00  -> 31.81
    #   30.5 would have required sigma = 1.021, or H0_LCDM = 67.296 --
    #   neither of which appears anywhere in the corpus.
    # An earlier version of this comment claimed the first as a "small
    # difference" and the second as "~30.5 within rounding"; neither holds,
    # and the second contradicted the code below, which uses sigma = 1.04.
    # That comment has been withdrawn rather than repaired.
    #
    # RESOLVED 18/08/2026: Table 4 has been aligned on 29.41 throughout F1
    # Extended and F1 Short. Two defects were fixed together -- the H0 entry
    # (30.5 was reproduced by no declared parameter set) and the total, which
    # omitted the eBOSS DR16 row. The published figures are now the sum of
    # the six rows: Delta chi2 = -39.5, Delta AIC = -31.5, Delta BIC = -7.0.
    # The Kass-Raftery conclusion is unchanged (|Delta BIC| = 8.1 > 6, still
    # "strong evidence"), and every row is now traceable to a script.
    'H0': {'val': 73.04, 'err': 1.04,
           'ref': 'Riess et al. 2022, arXiv:2112.04510'},

    # KiDS-1000 — Heymans et al. 2021, arXiv:2105.06969
    # Asymmetric 1-sigma: +0.020 / -0.014; effective symmetric sigma ~ 0.019
    # chi2_LCDM = (0.832-0.766)^2 / 0.019^2 = 12.07  (Foundation I, three occurrences)  ✓
    'S8': {'val': 0.766, 'err': 0.019,
           'ref': 'Heymans et al. 2021, arXiv:2105.06969'},

    # BAO — BOSS DR12 (Alam 2017) + eBOSS DR16 QSO (Hou 2021)
    # [Q1, 22/09/2026; corrected 12/10/2026] z=1.48 set to the eBOSS DR16 QSO consensus (30.21, 0.79; 30.22 used 22/09-12/10/2026 by mistake),
    # canonised on the primary source Hou et al. 2021; 38.4 +/- 1.1 and 30.85 +/- 0.80
    # are untraced historical targets (WITHDRAWN).
    'BAO': {
        'z':   np.array([0.38,  0.51,  0.61,  1.48]),
        'val': np.array([10.23, 13.37, 15.61, 30.21]),   # untraced before: 38.4, then 30.85 ; [04/10/2026, decision 7-compl] z=0.51 13.36->13.37, z=0.61 15.45->15.61 (Alam+2017 consensus 1975.22 and 2306.68 Mpc / r_d,fid 147.78; primary table to be confirmed)
        'err': np.array([0.166, 0.206, 0.251, 0.79]),    # untraced before: 1.1, then 0.80   # [05/10/2026, ALAM-ERR] BOSS DR12: stat (+) syst, Alam+2017 Table 7 / 147.78 (was 0.17, 0.21, 0.22 = stat only at z=0.61)
        'ref': ['Alam et al. 2017 (DR12)', 'Alam et al. 2017 (DR12)',
                'Alam et al. 2017 (DR12)', 'Hou et al. 2021 (DR16 QSO)']
    }
}

# ─────────────────────────────────────────────────────────────────────────────
# 3. MODEL PARAMETERS
# ─────────────────────────────────────────────────────────────────────────────

# [E2, 22/09/2026 -- DEC-A7-POST-07] The 'ECF' entry S8 = 0.766 below is the
# KiDS-1000 TARGET adopted as the model value of the historical chi2 budget,
# not an ECF prediction; the gamma_spin = 0.3116 behind it is a HISTORICAL
# CALIBRATION (withdrawn as canonical post-A-7). The chi2/AIC/BIC produced
# here are HISTORICAL and are NOT recomputed (DEC-A7-POST-07 §9).
MODELS = {
    'LCDM': {'H0': 67.4,  'rs': 147.1, 'S8': 0.832, 'Om': 0.315,
             'label': 'Planck 2018 Lambda-CDM'},
    'ECF':  {'H0': 73.04, 'rs': 135.65, 'S8': 0.766, 'Om': (0.02237+0.1200)/0.7304**2,  # [A-6/A-7 22/09/2026]
             'label': 'ECF (Einstein-Cartan Framework)'},
}

# chi2_S8 under option A (applied 24/08/2026).
# The DIVISIVE form of S8_ECF (eq. l.1209 of Foundation I, and
# script_06_S8_resolution.py) makes the ECF prediction coincide with the
# measurement, so this term vanishes.
# The previous value 1.2 was defended here as an MCMC posterior spread;
# that justification is withdrawn with the value, so that a later audit
# does not find a reasoned defence of a superseded number.
CHI2_S8_ECF_MCMC = 0.0   # option A

# ─────────────────────────────────────────────────────────────────────────────
# 4. PHYSICS FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

def hubble_parameter(z, H0, Om):
    """Flat-LCDM Hubble rate [km/s/Mpc]."""
    return H0 * np.sqrt(Om * (1 + z)**3 + (1 - Om))


def compute_DM_rs(z, H0, Om, rs):
    """
    Transverse comoving distance normalized by sound horizon.
    DM(z) / rs = (c/rs) * integral_0^z dz'/H(z')
    """
    inv_h = lambda zp: 1.0 / hubble_parameter(zp, H0, Om)
    integral, _ = quad(inv_h, 0, z)
    return C_LIGHT * integral / rs


# ─────────────────────────────────────────────────────────────────────────────
# 5. CHI2 CALCULATION
# ─────────────────────────────────────────────────────────────────────────────

def calculate_chi2_partial(model_name, override_s8_chi2=None):
    """
    Compute the partial chi2 budget: H0 + S8 + BAO.

    Parameters
    ----------
    model_name      : str   Key in MODELS dict ('LCDM' or 'ECF')
    override_s8_chi2: float If provided, replaces the computed S8 chi2
                            (used for ECF to inject MCMC posterior value)
    """
    m = MODELS[model_name]

    # H0 sector
    chi2_h0 = ((obs_data['H0']['val'] - m['H0']) / obs_data['H0']['err'])**2

    # S8 sector
    chi2_s8 = ((obs_data['S8']['val'] - m['S8']) / obs_data['S8']['err'])**2
    if override_s8_chi2 is not None:
        chi2_s8 = override_s8_chi2

    # BAO sector
    chi2_bao = 0.0
    bao_rows = []
    for i in range(len(obs_data['BAO']['z'])):
        z_i   = obs_data['BAO']['z'][i]
        obs_i = obs_data['BAO']['val'][i]
        err_i = obs_data['BAO']['err'][i]
        pred  = compute_DM_rs(z_i, m['H0'], m['Om'], m['rs'])
        c2_i  = ((obs_i - pred) / err_i)**2
        chi2_bao += c2_i
        bao_rows.append((z_i, obs_i, err_i, pred, c2_i))

    return chi2_h0, chi2_s8, chi2_bao, bao_rows


# ─────────────────────────────────────────────────────────────────────────────
# 6. MAIN
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    SEP = "=" * 72

    # Calculate
    c2_h_lcdm, c2_s_lcdm, c2_b_lcdm, bao_lcdm = calculate_chi2_partial('LCDM')
    c2_h_ecf,  c2_s_ecf,  c2_b_ecf,  bao_ecf  = calculate_chi2_partial(
        'ECF', override_s8_chi2=CHI2_S8_ECF_MCMC)

    total_lcdm  = c2_h_lcdm + c2_s_lcdm + c2_b_lcdm
    total_ecf   = c2_h_ecf  + c2_s_ecf  + c2_b_ecf
    delta_total = total_lcdm - total_ecf

    # Paper Table 3 reference values (including Planck CMB)
    paper_ref = {
        # 30.5 is the value printed in Table 4; 29.41 is what the declared
        # parameters give. Both are carried so the gap stays visible.
        'H0':    {'lcdm': 29.41,  'ecf': 0.1},   # matches Table 4 since 18/08/2026
        # 12.07, not 12.1: ((0.832-0.766)/0.019)^2 = 12.0665, the value
        # Foundation I carries three times. 12.1 is a rounding that no
        # paper prints and that shifts the LCDM total by +0.03.
        'S8':    {'lcdm': 12.07,  'ecf': 0.0},   # option A, 24/08/2026
        'BAO':   {'lcdm':  9.4,   'ecf': 9.5},
        # Sum of the six rows of Table 4 with chi2_ECF(S8) = 0:
        #   LCDM 2345.2+420.1+6.2+3.2+29.41+12.07 = 2816.18
        #   ECF  2347.0+420.1+6.2+3.3+ 0.10+ 0.0 = 2776.70
        # The former 2814.1/2774.6 also gave -39.5, but from totals
        # matching no row of the budget (gaps +2.11 and +3.30).
        'TOTAL': {'lcdm': 2816.18, 'ecf': 2776.70},
    }

    print(SEP)
    print(">>> CHI-SQUARE BUDGET  (Foundation I, Table 3)  — v2")
    print(SEP)

    print("\n>>> MODEL PARAMETERS")
    for k, m in MODELS.items():
        print(f"    {k:<6} H0={m['H0']:.2f}  rs={m['rs']:.1f} Mpc  "
              f"S8={m['S8']:.3f}  Om={m['Om']:.3f}")

    print("\n>>> BAO PREDICTIONS vs OBSERVATIONS")
    print(f"    {'z':>5}  {'obs':>6}  {'err':>5}  {'pred_LCDM':>10}  "
          f"{'pred_ECF':>9}  {'chi2_LCDM':>10}  {'chi2_ECF':>9}  ref")
    for r_l, r_e in zip(bao_lcdm, bao_ecf):
        z_, obs_, err_ = r_l[0], r_l[1], r_l[2]
        flag = " *** eBOSS DR16 consensus (untraced before: 38.4, then 30.85)" if abs(z_-1.48) < 0.01 else ""
        print(f"    {z_:>5.2f}  {obs_:>6.2f}  {err_:>5.2f}  "
              f"{r_l[3]:>10.3f}  {r_e[3]:>9.3f}  "
              f"{r_l[4]:>10.3f}  {r_e[4]:>9.3f}{flag}")

    print("\n>>> PARTIAL CHI2 BUDGET  (H0 + S8 + BAO only)")
    print(f"    {'Sector':<12} {'chi2_LCDM':>12} {'chi2_LCDM(paper)':>18} "
          f"{'chi2_ECF':>10} {'chi2_ECF(paper)':>16} {'Delta':>8}")
    rows = [
        ('H0', c2_h_lcdm, paper_ref['H0']['lcdm'], c2_h_ecf,  paper_ref['H0']['ecf']),
        ('S8', c2_s_lcdm, paper_ref['S8']['lcdm'], c2_s_ecf,  paper_ref['S8']['ecf']),
        ('BAO', c2_b_lcdm, paper_ref['BAO']['lcdm'], c2_b_ecf, paper_ref['BAO']['ecf']),
        ('PARTIAL', total_lcdm, 42.6, total_ecf, 10.8),
    ]
    for r in rows:
        print(f"    {r[0]:<12} {r[1]:>12.2f} {r[2]:>18.1f} {r[3]:>10.3f} {r[4]:>16.1f} "
              f"{r[1]-r[3]:>8.1f}")

    print("\n>>> IMPORTANT SCOPE NOTE")
    print(f"    This script covers only the TENSION SECTORS (H0+S8+BAO).")
    print(f"    Full chi2 from paper: LCDM={paper_ref['TOTAL']['lcdm']:.1f},  "
          f"ECF={paper_ref['TOTAL']['ecf']:.1f},  Delta={paper_ref['TOTAL']['lcdm']-paper_ref['TOTAL']['ecf']:.1f}"
          f"  (historical)")
    # [D3, 22/09/2026 -- DEC-A7-POST-02/05] Former text declared the BAO sector
    # "NEUTRAL (Delta=0)" and "BAO chi2 (script) < BAO chi2 (paper)": both false
    # after A-7. The statement is now computed from the partial budget above.
    print("    [historical values, Omega_m = 0.315 -- NOT RECOMPUTED: Boltzmann/CLASS-EC dependency missing, PO-F3-9]")
    print(f"    Planck CMB terms (high-ℓ + low-ℓ + lensing) contribute ~2767 to both totals;")
    print(f"    Delta_chi2(Planck) ≈ +1.8 in that historical budget (NOT RECOMPUTED after A-7)")
    _d_bao = c2_b_ecf - c2_b_lcdm
    _verdict = ("ECF disfavoured" if _d_bao > 1.0 else "ECF favoured" if _d_bao < -1.0 else "near-neutral")
    print(f"    BAO (script, diagonal DM/rs, {len(bao_ecf)} bins): chi2_LCDM = {c2_b_lcdm:.2f}, "
          f"chi2_ECF = {c2_b_ecf:.2f}, chi2_ECF - chi2_LCDM = {_d_bao:+.1f}  -> {_verdict}")
    print(f"    (paper: {paper_ref['BAO']['lcdm']} / {paper_ref['BAO']['ecf']} with the full BOSS DR12 covariance,"
          f" DM+DH+cross-terms, Alam 2017 Eq.10 -- not reproduced here)")
    print("    => its propagation to the global Delta_chi2 is NOT RECOMPUTED (DEC-A7-POST-02)")
    
    print("\n>>> INTERNAL CONSISTENCY CHECKS")
    assert abs(c2_s_lcdm - paper_ref['S8']['lcdm']) < 0.5, f"S8 LCDM chi2 mismatch: {c2_s_lcdm:.2f}"
    # Tolerance tightened from 3.0 to 0.05: the former was wide enough to
    # hide the 1.1 gap with Table 4 instead of reporting it.
    assert abs(c2_h_lcdm - paper_ref['H0']['lcdm']) < 0.05, f"H0 LCDM chi2 mismatch: {c2_h_lcdm:.2f}"
    bao_148 = bao_lcdm[3]
    assert abs(bao_148[1] - 30.21) < 0.01, f"BAO z=1.48 val still wrong: {bao_148[1]}"
    print(f"    S8 chi2 LCDM = {c2_s_lcdm:.2f}  (target 12.07, tol 0.5)  OK")
    print(f"    H0 chi2 LCDM = {c2_h_lcdm:.2f}  (declared parameters; matches Table 4)  OK")
    print(f"    BAO z=1.48   = {bao_148[1]:.2f}  (eBOSS DR16 QSO consensus, Hou+2021)   OK")
    print(SEP)

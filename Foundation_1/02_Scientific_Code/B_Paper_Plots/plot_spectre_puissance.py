"""
Script: plot_spectre_puissance_v2.py
Paper:  Foundation I: Unified Resolution of Cosmological Tensions
Author: Pascal Fichant
Date:   21/04/2026
Version: v2 referee

Description:
    Generates Figure figeuclidpk (Sec. 4-5) — matter power spectrum P(k)
    comparing Planck LCDM and ECF, with Euclid simulated forecast and
    power-spectrum ratio panel.

    Physical model:
        P_ECF(k) = T_torsion^2(k) * P_CDM(k)

    Lorentzian torsion transfer function (Sec. 4, caption figeuclidpk):
        T^2(k) = 1 - A_sup * k^2 / (k^2 + k_cut^2)
        A_sup  = 0.15        [asymptotic suppression amplitude]
        k_cut  = 0.10 h/Mpc  [characteristic suppression scale]
        T^2(k->0)   = 1      (large scales unaffected)
        T^2(k>>k_cut) -> 0.85 (saturates; k_cut is the Lorentzian half-width)
        Note: T^2(k_cut) = 0.925 (half-amplitude, not half-maximum)

    BBKS transfer function (Bardeen 1986):
        gamma = Omega_m * h = 0.315 * 0.7304 = 0.230   [shape parameter]
        T(q)  = ln(1+2.34q)/(2.34q)
                * [1 + 3.89q + (16.1q)^2 + (5.46q)^3 + (6.71q)^4]^(-1/4)
        q     = k / gamma

    BAO oscillations:
        BAO(k,rs) = 1 + A_bao * sin(k*rs) * exp(-(k*sigma_nl)^1.5)
        A_bao   = 0.06  [oscillation amplitude, phenomenological]
        sigma_nl= 8.0   [non-linear damping scale, h/Mpc]

    Sound horizon (Sec. 3, Eq. rsECF):
        rs_LCDM = 147.1 Mpc    [Planck 2018]
        rs_ECF  = 135.8 Mpc    [F_ion = 1.2765]

    Clustering amplitudes (Sec. 5, Table tabchi2breakdown):
        S8_LCDM = 0.832,  sigma8_LCDM = 0.832 / sqrt(0.315/0.3) = 0.8119
        S8_ECF  = 0.766,  sigma8_ECF  = 0.766 / sqrt(0.315/0.3) = 0.7475
        s8_factor = (sigma8_ECF / sigma8_LCDM)^2 = 0.8476

    Euclid forecast (Sec. 6, seceuclidprediction):
        Simulated points anchored on ECF; optimal window k in [0.08, 0.30] h/Mpc.

Calibration checks (verify_calibration):
    sigma8_ECF        = 0.7475  (Sec. 5, caption figeuclidpk)
    T^2(k_cut=0.10)   = 0.9250  (half-amplitude of Lorentzian)
    T^2(3*k_cut=0.30) = 0.8650  (approaching saturation)
    T^2(k->inf)       = 0.8500  (= 1 - A_sup)
    s8_factor         = 0.8476  (= (sigma8_ECF/sigma8_LCDM)^2)

Sections impacted:
    Sec. 3 (secsoundhorizon), Sec. 4 (secsuppression, seceuclidprediction),
    Sec. 5 (secresults, tabchi2breakdown), Fig. figeuclidpk.

Changelog v1 -> v2:
    + T_torsion^2(k): corrected from global s8_factor=0.85 to exact
      Lorentzian form 1 - A_sup*k^2/(k^2+k_cut^2) [Sec. 4, caption figeuclidpk]
    + BBKS shape: gamma = Omega_m*h = 0.230 [v1 used gamma=0.21, ad hoc]
    + S8/sigma8 exact: 0.766/0.7475 [v1 rounded to 0.76]
    + s8_factor derived from (sigma8_ECF/sigma8_LCDM)^2 = 0.8476 [v1: 0.85 arbitrary]
    + Bottom panel: ratio P_ECF/P_CDM = T^2(k) [absent in v1]
    + Euclid forecast anchored on ECF [v1: intermediate rs=142 invented]
    + Optimal discrimination window k in [0.08,0.30] [absent in v1]
    + verify_calibration() with asserts on T^2, sigma8_ECF, s8_factor
    + Annotations repositioned to avoid axis-limit overflow
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np

plt.rcParams.update({
    'font.size': 11, 'axes.labelsize': 12,
    'legend.fontsize': 10, 'font.family': 'serif', 'axes.linewidth': 1.3,
})

# ---------------------------------------------------------------------------
# 1. PHYSICAL CONSTANTS
# ---------------------------------------------------------------------------
OM_M   = 0.315       # Planck 2018 matter density fraction
H_DIM  = 0.7304      # dimensionless Hubble h (ECF best-fit, Sec. 5)
N_S    = 0.965       # scalar spectral index
RS_CDM = 147.1       # sound horizon LCDM [Mpc]
RS_ECF = 135.8       # sound horizon ECF  [Mpc] — Sec. 3
S8_CDM = 0.832       # Planck 2018 — Table tabchi2breakdown
S8_ECF = 0.766       # ECF calibrated — Table tabchi2breakdown
A_SUP  = 0.15        # Lorentzian suppression amplitude — Sec. 4
K_CUT  = 0.10        # suppression scale [h/Mpc] — Sec. 4
A_BAO  = 0.06        # BAO oscillation amplitude
SIG_NL = 8.0         # BAO non-linear damping scale [h/Mpc]


# ---------------------------------------------------------------------------
# 2. CALIBRATION
# ---------------------------------------------------------------------------
def verify_calibration():
    print(">>> Calibration verification (Matter Power Spectrum v2)...")

    sig8_cdm = S8_CDM / np.sqrt(OM_M / 0.3)
    sig8_ecf = S8_ECF / np.sqrt(OM_M / 0.3)
    print(f"   sigma8_LCDM = {sig8_cdm:.4f}")
    print(f"   sigma8_ECF  = {sig8_ecf:.4f}  (target: 0.7475, Sec. 5)")
    assert abs(sig8_ecf - 0.7475) < 0.001, "FAIL: sigma8_ECF != 0.7475"

    def T2(k): return 1.0 - A_SUP * k**2 / (k**2 + K_CUT**2)
    print(f"   T2(k_cut={K_CUT})      = {T2(K_CUT):.4f}  (expected 0.9250)")
    print(f"   T2(3*k_cut={3*K_CUT}) = {T2(3*K_CUT):.4f}  (expected 0.8650)")
    print(f"   T2(k->inf)            = {1.0-A_SUP:.4f}  (= 1 - A_sup)")
    assert abs(T2(K_CUT)   - 0.9250) < 0.001, "FAIL: T2(k_cut)"
    assert abs(T2(3*K_CUT) - 0.8650) < 0.001, "FAIL: T2(3*k_cut)"
    assert abs(1.0-A_SUP   - 0.8500) < 1e-10, "FAIL: T2(inf)"

    s8_factor = (sig8_ecf / sig8_cdm)**2
    print(f"   s8_factor = (sigma8_ECF/sigma8_LCDM)^2 = {s8_factor:.4f}  (expected 0.8476)")
    assert abs(s8_factor - 0.8476) < 0.001, "FAIL: s8_factor"

    print(">>> Calibration OK.\n")


# ---------------------------------------------------------------------------
# 3. SPECTRAL MODEL
# ---------------------------------------------------------------------------
def bbks_tf(k):
    """BBKS transfer function. gamma = Omega_m * h (Bardeen 1986)."""
    gamma = OM_M * H_DIM
    q = k / gamma
    return (np.log(1 + 2.34*q) / (2.34*q)
            * (1 + 3.89*q + (16.1*q)**2 + (5.46*q)**3 + (6.71*q)**4)**(-0.25))


def bao_osc(k, rs):
    return 1.0 + A_BAO * np.sin(k * rs) * np.exp(-(k * SIG_NL)**1.5)


def T2_tors(k):
    """Lorentzian torsion transfer function squared (Sec. 4, caption fig euclid pk)."""
    return 1.0 - A_SUP * k**2 / (k**2 + K_CUT**2)


def pk_base(k, rs, s8f=1.0):
    return k**N_S * bbks_tf(k)**2 * bao_osc(k, rs) * s8f


# ---------------------------------------------------------------------------
# 4. FIGURE
# ---------------------------------------------------------------------------
def plot_matter_power_spectrum():
    verify_calibration()
    print(">>> Generating Figure: Matter Power Spectrum P(k) v2...")

    k = np.logspace(-3, np.log10(0.5), 1200)

    sig8_cdm  = S8_CDM / np.sqrt(OM_M / 0.3)
    sig8_ecf  = S8_ECF / np.sqrt(OM_M / 0.3)
    s8_factor = (sig8_ecf / sig8_cdm)**2

    pk_cdm = pk_base(k, RS_CDM, 1.0)
    pk_ecf = pk_base(k, RS_ECF, s8_factor) * T2_tors(k)

    i_ref = np.argmin(np.abs(k - 0.02))
    norm  = 5e4 / pk_cdm[i_ref]
    pk_cdm *= norm
    pk_ecf *= norm

    k_eu  = np.array([0.05, 0.08, 0.12, 0.18, 0.25, 0.35])
    pk_eu = pk_base(k_eu, RS_ECF, s8_factor) * T2_tors(k_eu) * norm
    err   = np.array([0.04, 0.035, 0.035, 0.04, 0.05, 0.07])

    ratio     = T2_tors(k)
    k_bao_cdm = np.pi / RS_CDM
    k_bao_ecf = np.pi / RS_ECF

    fig = plt.figure(figsize=(10, 8))
    fig.suptitle('ECF Matter Power Spectrum',
                 fontsize=12, fontweight='bold', y=0.99)
    gs  = gridspec.GridSpec(2, 1, height_ratios=[3, 1.1], hspace=0.08,
                            left=0.11, right=0.97, top=0.94, bottom=0.08)
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1], sharex=ax1)

    ax1.plot(k, pk_cdm, color='#1a5276', ls='--', lw=1.8,
             label=r'$\Lambda$CDM  $r_s=147.1$ Mpc, $S_8=0.832$', alpha=0.9)
    ax1.plot(k, pk_ecf, color='#c0392b', ls='-', lw=2.5,
             label=r'ECF  $r_s=135.8$ Mpc, $S_8=0.766$, $\sigma_8=0.747$')
    ax1.errorbar(k_eu, pk_eu, yerr=pk_eu*err,
                 fmt='k^', ms=5, capsize=3, lw=1.1,
                 label='Euclid (simulated, anchored on ECF)', zorder=6)
    ax1.axvspan(0.08, 0.30, color='#27ae60', alpha=0.08)
    ax1.text(0.13, 4.5e4, 'Optimal\nwindow', fontsize=8.5, color='#27ae60',
             ha='center', va='bottom', style='italic')
    ax1.axvline(k_bao_cdm, color='#1a5276', ls=':', lw=1.0, alpha=0.6)
    ax1.axvline(k_bao_ecf, color='#c0392b', ls=':', lw=1.0, alpha=0.6)
    ax1.annotate(r'$\Delta r_s=-11.3$ Mpc',
                 xy=(k_bao_ecf, 2.8e5), xytext=(0.013, 2.8e5),
                 arrowprops=dict(arrowstyle='->', lw=1.1, color='#333'),
                 fontsize=9.5, color='#333',
                 bbox=dict(boxstyle='round,pad=0.25', fc='white', ec='#bbb',
                           lw=0.7, alpha=0.92))
    ax1.annotate(r'$S_8$ suppression',
                 xy=(0.30, pk_ecf[np.argmin(np.abs(k-0.30))]),
                 xytext=(0.20, 3.0e4),
                 arrowprops=dict(arrowstyle='->', lw=1.1, color='#c0392b'),
                 fontsize=9.5, color='#c0392b',
                 bbox=dict(boxstyle='round,pad=0.25', fc='white', ec='#c0392b',
                           lw=0.7, alpha=0.92))
    ax1.set_xscale('log'); ax1.set_yscale('log')
    ax1.set_xlim(0.01, 0.5); ax1.set_ylim(1.0e4, 6e5)
    ax1.set_ylabel(r'$P(k)$  [arb. units]')
    ax1.legend(loc='upper right', framealpha=0.95)
    ax1.grid(True, which='both', ls=':', alpha=0.35, lw=0.6)
    ax1.tick_params(labelbottom=False)

    ax2.plot(k, ratio, color='#c0392b', lw=2.2,
             label=r'$P_\mathrm{ECF}/P_\mathrm{CDM}=T^2_\mathrm{tors}(k)$')
    ax2.axhline(1.0-A_SUP, color='#c0392b', ls=':', lw=1.4,
                label=r'$T^2_\infty=0.85$  ($k\gg k_\mathrm{cut}$)')
    ax2.axhline(1.0, color='#1a5276', ls='--', lw=1.1, alpha=0.55)
    ax2.axvline(K_CUT, color='#888', ls=':', lw=1.0, alpha=0.8)
    ax2.text(K_CUT*1.08, 0.998, r'$k_\mathrm{cut}$', fontsize=9,
             color='#666', va='top')
    ax2.axvspan(0.08, 0.30, color='#27ae60', alpha=0.08)
    ax2.set_xscale('log')
    ax2.set_xlim(0.01, 0.5); ax2.set_ylim(0.83, 1.02)
    ax2.set_xlabel(r'$k$  [$h\,\mathrm{Mpc}^{-1}$]')
    ax2.set_ylabel(r'Ratio $P_\mathrm{ECF}/P_\mathrm{CDM}$', fontsize=10)
    ax2.legend(loc='lower left', framealpha=0.95, ncol=2)
    ax2.grid(True, which='both', ls=':', alpha=0.35, lw=0.6)
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.2f}'))

    plt.savefig('Figure_spectre_puissance.png', dpi=300)
    print("   [SUCCESS] Saved: Figure_spectre_puissance.png")
    plt.close()


if __name__ == "__main__":
    plot_matter_power_spectrum()

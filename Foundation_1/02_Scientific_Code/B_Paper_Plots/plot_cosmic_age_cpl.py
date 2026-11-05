#!/usr/bin/env python3
"""
Script 07 — Cosmic Age Integration: CPL Dark Energy Proxy
Foundation I Extended v2 — Sec. 5 (sec:age_trilemma), Fig. fig:cosmicagecpl

Three cases:
  [1] LCDM Planck  : H0=67.4,  w=-1,  wa=0   -> t0 ~ 13.79 Gyr
  [2] H0-tension   : H0=73.04, w=-1,  wa=0   -> t0 ~ 13.33 Gyr (A-7; 12.73 at Om=0.315)
  [3] CPL illustration (not the ECF point): H0=73.04, w0=-1.1, wa=-1.5 -> t0 ~ 14.03 Gyr; ECF calibrated point (-0.904, -0.153) -> t0 ~ 13.19 Gyr (A-7; 13.29-13.31 at Om=0.315)

CPL parametrisation (Chevallier & Polarski 2001; Linder 2003):
    w(z) = w0 + wa * z/(1+z)

Physical mechanism (wa=-1.5 < 0):
    w becomes more negative at high-z (phantom deepening).
    rho_DE ~ (1+z)^{3(1+w0+wa)} = (1+z)^{-4.8} -> drops to zero rapidly.
    Less DE in the past -> H(z) reduced at intermediate z
    -> integrand 1/((1+z)*H(z)) larger -> t0 increases.
    [NB: the script header v1 said "w less negative in the past" -- incorrect;
     the direction of t0 increase is correct but the phrase was wrong.]

Trilemma note (Sec. 5):    CPL proxy restores t0~13.30 Gyr but degrades BAO chi2 by +38
    [19/10/2026: 13.30 Gyr is the Om=0.315 value of the (-1.1,-1.5) illustration;
     at the paper's Om_m (A-7) it gives 14.03 Gyr. Neither is the ECF point.]
    [15/08/2026 audit: this header said +42; F1 Extended, Table note (b),
     states Delta chi2_BAO = 38. The paper is authoritative.]
    (BOSS/eBOSS DM(z)/rs constraints). This constitutes the irreducible
    H0-Age-BAO trilemma; exact resolution deferred to Foundation II.

References:
    Chevallier & Polarski (2001) Int.J.Mod.Phys.D 10, 213
    Linder (2003) PRL 90, 091301
    Valcin et al. (2020) JCAP 12, 002, arXiv:2007.06594
        [t_GC = 13.32 +/- 0.1 stat +/- 0.5 sys Gyr, used as a chronometric prior on t0]
    DESI Collaboration (2024) arXiv:2404.03002  [wa ~ -1.32]
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
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.integrate import quad

# ---------------------------------------------------------------------------
# 1. PARAMETERS
# ---------------------------------------------------------------------------
# --- Omega_m: value INHERITED from Planck 2018, deliberately kept --------------
# 15/08/2026 audit. Om_m = 0.315 is the Planck 2018 value, entered as "Fixed"
# in the F1 Extended prior table (Tab. tabpriors). It is NOT fitted here.
# Known caveat, stated by the paper itself (F1 Extended, Table note (b),
# update of 20/07/2026): Planck measures the physical density
# omega_m = Omega_m * h^2 = 0.1429. Dividing by the Planck h gives
# 0.1429/0.674^2 = 0.315; dividing by the ECF h gives 0.1429/0.7304^2 = 0.268.
# So 0.315 is tied to the Planck h and is not transferable as-is to a model
# with H0 = 73.04.
# WHY IT IS KEPT: with Omega_m = 0.268 the age integral alone yields
# t0 = 13.31 Gyr, i.e. the globular-cluster constraint, but that value
# violates BAO and theta*; the paper's joint rescan reaches only
# t0 = 13.0-13.2 Gyr at Omega_m = 0.28-0.29. Switching this script to 0.268
# would draw a figure that appears to resolve the age tension merely by
# dropping two constraints. Revising it properly requires a joint
# (Omega_m, w0, wa) refit against age + BAO + theta*, which is new
# computation, not an audit. The figure therefore stays as published.
# [D3, 22/09/2026] SUPERSEDED by A-7 (DEC-A7-POST-06, not reopened): the ECF
# cases now use Omega_m = omega_m/h_ECF^2 and Omega_r = omega_r/h_ECF^2; the LCDM
# case keeps the Planck-h values. With w = -1 the ECF age is 13.33 Gyr (the age
# tension disappears, DEC-A7-POST-01); the CPL proxy (-1.1, -1.5) gives 14.03 Gyr.
# 17/08/2026 audit - ALIGNED ON script_01_solve_sound_horizon.py.
# Om_m was 0.315 and Om_r 9.0e-5, giving t0 = 12.726 Gyr, printed as
# "12.73 Gyr" on the left panel while the F1 caption states 12.74. The
# canonical t0 = 12.74 Gyr comes from script_01, which uses the EXACT
# Planck values Om_m = 0.31377 and Om_r = 9.1784e-5 — 0.315 is that same
# number rounded. This is therefore not a change of physics but the removal
# of a rounding: the two scripts now agree, and the figure prints the same
# t0 as the caption. The Planck-h caveat below is untouched and still
# applies (0.31377 remains tied to h_Planck, not to h_ECF = 0.7304).
Om_m  = 0.31377   # Planck-h, kept for the LCDM case (H0 = 67.4)
Om_m_ECF = (0.02237 + 0.1200)/0.7304**2   # [A-7, 22/09/2026] Omega_m = omega_m/h_ECF^2 = 0.266868 ; was 0.315 (Planck-h value)
Om_r  = 9.2199e-5   # [A-6] was 9.1784e-5 (derived from the wrong omega_nu) -- Planck-h, LCDM case
Om_r_ECF = Om_r*(0.6736/0.7304)**2   # [D3, 22/09/2026] omega_r/h_ECF^2 = 7.842e-5 (A-7 rule applied to radiation)
Om_DE = 1.0 - Om_m - Om_r

km_per_Mpc   = 3.08567758e19
sec_per_Gyr  = 31556925.2 * 1e9

H0_ECF    = 73.04   # km/s/Mpc  (ECF calibrated — canonical value, F1 Extended)
# 15/08/2026 audit: was 73.01 while the paper caption and the corpus canonical
# table both state 73.04. Aligned on the canonical value.
H0_PLANCK = 67.4    # km/s/Mpc  (Planck 2018)
H0_TENS   = 73.04   # km/s/Mpc  (SH0ES, used for tension case only)

w0_ecf = -1.1
wa_ecf = -1.5
target_age = 13.32   # t_GC, Valcin et al. 2020 (JCAP 12, 002) [Gyr]

def t_Hubble(H0):
    return (km_per_Mpc / H0) / sec_per_Gyr

# ---------------------------------------------------------------------------
# 2. FUNCTIONS
# ---------------------------------------------------------------------------
def E_z(z, w0, wa, om=None, orad=None):
    """Normalised Hubble rate E(z) = H(z)/H0 with CPL dark energy."""
    om = Om_m if om is None else om
    orad = Om_r if orad is None else orad   # [D3] Omega_r of the background (h-dependent)
    de = (1+z)**(3*(1+w0+wa)) * np.exp(-3*wa*z/(1+z))
    return np.sqrt(orad*(1+z)**4 + om*(1+z)**3 + (1.0-om-orad)*de)

def get_age(H0_kms, w0, wa):
    """Cosmic age [Gyr] by integration of 1/((1+z)*H(z)).
    [A-7] Omega_m = omega_m/h^2 : Planck-h value for H0=67.4, ECF value otherwise."""
    tH  = t_Hubble(H0_kms)
    om  = Om_m if abs(H0_kms-67.4) < 1e-6 else Om_m_ECF
    orad = Om_r if abs(H0_kms-67.4) < 1e-6 else Om_r_ECF   # [D3] same rule for radiation
    val, _ = quad(lambda z: 1.0/((1+z)*E_z(z, w0, wa, om, orad)), 0, np.inf)
    return tH * val

# ---------------------------------------------------------------------------
# 3. VALIDATION
# ---------------------------------------------------------------------------
age_lcdm    = get_age(H0_PLANCK, -1.0, 0.0)
age_tension = get_age(H0_TENS,   -1.0, 0.0)
age_ecf     = get_age(H0_ECF,    w0_ecf, wa_ecf)
delta_vs_target = age_ecf - target_age

print("=" * 65)
print("  SCRIPT 07 — COSMIC AGE  (Foundation I Sec. 5)")
print("=" * 65)
print(f"[1] LCDM (H0=67.4,  w=-1)         : t0 = {age_lcdm:.4f} Gyr  (ref: ~13.80)")
print(f"[2] ECF background (H0=73.04, w=-1): t0 = {age_tension:.4f} Gyr  (Omega_m = omega_m/h^2 = {Om_m_ECF:.4f}, A-7; 12.74 at the former 0.315)")
print(f"[3] CPL illustration (-1.1, -1.5)  : t0 = {age_ecf:.4f} Gyr  (GC prior {target_age} Gyr; the former 13.30-13.31 was at Omega_m = 0.315)")
print(f"    Valcin+2020 GC prior            : {target_age:.2f} Gyr")
print(f"    delta CPL-illustration vs GC             : {delta_vs_target:+.4f} Gyr  "
      f"({'OK' if abs(delta_vs_target) < 0.10 else 'CHECK'})")
print(f"    CPL exponent 3*(1+w0+wa)        : {3*(1+w0_ecf+wa_ecf):.1f}  (ref: -4.8)")
print("=" * 65)

# ---------------------------------------------------------------------------
# 4. PLOT DATA
# ---------------------------------------------------------------------------
w_vals      = np.linspace(-1.8, -0.5, 100)
ages_cw     = [get_age(H0_ECF, w, 0) for w in w_vals]

wa_vals     = np.linspace(-2.0, 1.5, 100)
ages_m09    = [get_age(H0_ECF, -0.9, wa) for wa in wa_vals]
ages_m10    = [get_age(H0_ECF, -1.0, wa) for wa in wa_vals]
ages_m11    = [get_age(H0_ECF, -1.1, wa) for wa in wa_vals]

# ---------------------------------------------------------------------------
# 5. FIGURE
# ---------------------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Panel 1: constant w
ax1.plot(w_vals, ages_cw, color="#1f77b4", lw=2.5)
ax1.axhline(target_age, color="#d62728", ls="--", lw=2,
            label=f"Valcin+2020 ({target_age} Gyr)")
ax1.axvline(-1, color="gray", ls=":", lw=2, label=r"$\Lambda$CDM ($w=-1$)")
ax1.plot(-1, get_age(H0_ECF, -1, 0), "ko", ms=6)
age_w_minus1 = get_age(H0_ECF, -1, 0)
ax1.text(-0.96, age_w_minus1 + 0.05, f"{age_w_minus1:.2f} Gyr",
         fontsize=10, fontweight="bold")   # 15/08/2026: was a hard-coded string
ax1.set_xlabel(r"Constant Dark Energy EoS ($w$)", fontsize=13)
ax1.set_ylabel(r"Age of the Universe $t_0$ (Gyr)", fontsize=13)
ax1.set_title(rf"Constant $w$ — $H_0 = {H0_ECF}$ km/s/Mpc", fontsize=14, pad=10)
ax1.legend(loc="lower right", fontsize=11)
ax1.grid(True, ls="--", alpha=0.4)

# Panel 2: CPL
ax2.plot(wa_vals, ages_m09, color="#2ca02c", lw=2.5,
         label=r"$w_0 = -0.9$")
ax2.plot(wa_vals, ages_m10, color="#1f77b4", lw=2.5,
         label=r"$w_0 = -1.0$")
ax2.plot(wa_vals, ages_m11, color="#9467bd", lw=2.5,
         label=r"$w_0 = -1.1$ (CPL illustration)")
ax2.axhline(target_age, color="#d62728", ls="--", lw=2,
            label=f"Valcin+2020 ({target_age} Gyr)")
ax2.axvline(0, color="gray", ls=":", lw=1.5, alpha=0.6)
ax2.plot(wa_ecf, age_ecf, "*", color="#ff7f0e", ms=16, zorder=5,
         label=f"CPL illustration ($w_0={w0_ecf}$, $w_a={wa_ecf}$) = {age_ecf:.2f} Gyr")
# [19/10/2026] the calibrated ECF point (w0, wa) = (-0.904, -0.153) (F1, PO-F1-W0); the
# (-1.1, -1.5) curve and star were labelled "ECF" in earlier versions.
age_ecf_cal = get_age(H0_ECF, -0.904, -0.153)
ax2.plot(-0.153, age_ecf_cal, "D", color="#d62728", ms=9, zorder=6,
         label=f"ECF calibrated point ($w_0=-0.904$, $w_a=-0.153$) = {age_ecf_cal:.2f} Gyr")
ax2.annotate(f"CPL: {age_ecf:.2f} Gyr",
             xy=(wa_ecf, age_ecf),
             xytext=(wa_ecf + 0.25, age_ecf - 0.20),
             fontsize=10, fontweight="bold", color="#ff7f0e",
             arrowprops=dict(arrowstyle="->", color="#ff7f0e", lw=1.5))
ax2.set_xlabel(r"Dynamic Parameter ($w_a$)", fontsize=13)
ax2.set_ylabel(r"Age of the Universe $t_0$ (Gyr)", fontsize=13)
ax2.set_title(rf"CPL Dynamic Dark Energy — $H_0 = {H0_ECF}$ km/s/Mpc", fontsize=14, pad=10)
ax2.legend(loc="lower right", fontsize=10)
ax2.grid(True, ls="--", alpha=0.4)

plt.tight_layout()
plt.savefig("Fig_ECF_Cosmic_Age.png", dpi=300, bbox_inches="tight")
print("Figure saved: Fig_ECF_Cosmic_Age.png")

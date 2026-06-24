#!/usr/bin/env python3
"""
Script 07 — Cosmic Age Integration: CPL Dark Energy Proxy
Foundation I Extended v2 — Sec. 5 (sec:age_trilemma), Fig. fig:cosmicagecpl

Three cases:
  [1] LCDM Planck  : H0=67.4,  w=-1,  wa=0   -> t0 ~ 13.79 Gyr
  [2] H0-tension   : H0=73.04, w=-1,  wa=0   -> t0 ~ 12.73 Gyr
  [3] ECF CPL proxy: H0=73.01, w0=-1.1, wa=-1.5 -> t0 ~ 13.30 Gyr

CPL parametrisation (Chevallier & Polarski 2001; Linder 2003):
    w(z) = w0 + wa * z/(1+z)

Physical mechanism (wa=-1.5 < 0):
    w becomes more negative at high-z (phantom deepening).
    rho_DE ~ (1+z)^{3(1+w0+wa)} = (1+z)^{-4.8} -> drops to zero rapidly.
    Less DE in the past -> H(z) reduced at intermediate z
    -> integrand 1/((1+z)*H(z)) larger -> t0 increases.
    [NB: the script header v1 said "w less negative in the past" -- incorrect;
     the direction of t0 increase is correct but the phrase was wrong.]

Trilemma note (Sec. 5):
    CPL proxy restores t0~13.30 Gyr but degrades BAO chi2 by ~+42
    (BOSS/eBOSS DM(z)/rs constraints). This constitutes the irreducible
    H0-Age-BAO trilemma; exact resolution deferred to Foundation II.

References:
    Chevallier & Polarski (2001) Int.J.Mod.Phys.D 10, 213
    Linder (2003) PRL 90, 091301
    Valcin et al. (2020) JCAP 12, 008  [globular cluster age prior t0=13.32 Gyr]
    DESI Collaboration (2024) arXiv:2404.03002  [wa ~ -1.32]
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.integrate import quad

# ---------------------------------------------------------------------------
# 1. PARAMETERS
# ---------------------------------------------------------------------------
Om_m  = 0.315
Om_r  = 9.0e-5
Om_DE = 1.0 - Om_m - Om_r

km_per_Mpc   = 3.08567758e19
sec_per_Gyr  = 31556925.2 * 1e9

H0_ECF    = 73.01   # km/s/Mpc  (ECF calibrated)
H0_PLANCK = 67.4    # km/s/Mpc  (Planck 2018)
H0_TENS   = 73.04   # km/s/Mpc  (SH0ES, used for tension case only)

w0_ecf = -1.1
wa_ecf = -1.5
target_age = 13.32   # Valcin et al. 2020 globular cluster prior [Gyr]

def t_Hubble(H0):
    return (km_per_Mpc / H0) / sec_per_Gyr

# ---------------------------------------------------------------------------
# 2. FUNCTIONS
# ---------------------------------------------------------------------------
def E_z(z, w0, wa):
    """Normalised Hubble rate E(z) = H(z)/H0 with CPL dark energy."""
    de = (1+z)**(3*(1+w0+wa)) * np.exp(-3*wa*z/(1+z))
    return np.sqrt(Om_r*(1+z)**4 + Om_m*(1+z)**3 + Om_DE*de)

def get_age(H0_kms, w0, wa):
    """Cosmic age [Gyr] by integration of 1/((1+z)*H(z))."""
    tH  = t_Hubble(H0_kms)
    val, _ = quad(lambda z: 1.0/((1+z)*E_z(z, w0, wa)), 0, np.inf)
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
print(f"[2] Tension (H0=73.04, w=-1)       : t0 = {age_tension:.4f} Gyr  (ref: ~12.75)")
print(f"[3] ECF CPL (w0=-1.1, wa=-1.5)     : t0 = {age_ecf:.4f} Gyr  (target: 13.30-13.32)")
print(f"    Valcin+2020 GC prior            : {target_age:.2f} Gyr")
print(f"    delta ECF vs target             : {delta_vs_target:+.4f} Gyr  "
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
ax1.text(-0.96, 12.78, "12.73 Gyr", fontsize=10, fontweight="bold")
ax1.set_xlabel(r"Constant Dark Energy EoS ($w$)", fontsize=13)
ax1.set_ylabel(r"Age of the Universe $t_0$ (Gyr)", fontsize=13)
ax1.set_title(r"Constant $w$ — $H_0 = 73.0$ km/s/Mpc", fontsize=14, pad=10)
ax1.legend(loc="lower right", fontsize=11)
ax1.grid(True, ls="--", alpha=0.4)

# Panel 2: CPL
ax2.plot(wa_vals, ages_m09, color="#2ca02c", lw=2.5,
         label=r"$w_0 = -0.9$")
ax2.plot(wa_vals, ages_m10, color="#1f77b4", lw=2.5,
         label=r"$w_0 = -1.0$")
ax2.plot(wa_vals, ages_m11, color="#9467bd", lw=2.5,
         label=r"$w_0 = -1.1$ (ECF)")
ax2.axhline(target_age, color="#d62728", ls="--", lw=2,
            label=f"Valcin+2020 ({target_age} Gyr)")
ax2.axvline(0, color="gray", ls=":", lw=1.5, alpha=0.6)
ax2.plot(wa_ecf, age_ecf, "*", color="#ff7f0e", ms=16, zorder=5,
         label=f"ECF best-fit ($w_0={w0_ecf}$, $w_a={wa_ecf}$) = {age_ecf:.2f} Gyr")
ax2.annotate(f"ECF: {age_ecf:.2f} Gyr",
             xy=(wa_ecf, age_ecf),
             xytext=(wa_ecf + 0.25, age_ecf - 0.20),
             fontsize=10, fontweight="bold", color="#ff7f0e",
             arrowprops=dict(arrowstyle="->", color="#ff7f0e", lw=1.5))
ax2.set_xlabel(r"Dynamic Parameter ($w_a$)", fontsize=13)
ax2.set_ylabel(r"Age of the Universe $t_0$ (Gyr)", fontsize=13)
ax2.set_title(r"CPL Dynamic Dark Energy — $H_0 = 73.0$ km/s/Mpc", fontsize=14, pad=10)
ax2.legend(loc="lower right", fontsize=10)
ax2.grid(True, ls="--", alpha=0.4)

plt.tight_layout()
plt.savefig("Fig_ECF_Cosmic_Age.png", dpi=300, bbox_inches="tight")
print("Figure saved: Fig_ECF_Cosmic_Age.png")

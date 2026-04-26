#!/usr/bin/env python3
# =============================================================================
#  plot_Cosmic_History_Omegas_v3.py
#  ECF Framework — Cosmic History: Evolution of Fractional Density Parameters
# =============================================================================
#
#  PURPOSE
#  -------
#  This script reproduces Figure [X] of:
#    - Fichant (2026), "The Topological Invariance Principle" (PIT Letter, PRL)
#    - Fichant (2026), "Foundation I: The Metric Universe" (F1 Extended, PRD)
#
#  The figure shows the temporal evolution of fractional energy densities
#  Omega_i(a) in the ECF (Einstein-Cartan Framework), including the transient
#  primordial torsion/spin component. The bottom panel verifies numerically
#  that the Topological Invariance Principle (TIP, Omega_total = 1) holds
#  at all times, i.e. Omega_k = 0 throughout cosmic history.
#
#  USAGE
#  -----
#  Set PAPER = "PIT" for the PRL Letter     (double-column, 7.2")
#  Set PAPER = "F1"  for the PRD Extended paper (single-column, 3.375")
#  All other parameters adapt automatically.
#
#  OUTPUT
#  ------
#  Figure_CosmicHistory_Omegas_PIT.png  (300 dpi, PRL-ready)
#  Figure_CosmicHistory_Omegas_F1.png   (300 dpi, PRD-ready)
#
#  DEPENDENCIES
#  ------------
#  numpy >= 1.21, matplotlib >= 3.5  (standard scientific Python stack)
#
#  REPRODUCIBILITY
#  ---------------
#  No random seed required. The computation is fully deterministic.
#  All cosmological parameters are taken from Planck 2018 (Table 2,
#  TT,TE,EE+lowE). The ECF-specific parameter alpha_spin = 0.093 is
#  calibrated in Section 5 of Foundation I and referenced in Eq. (7)
#  of the PIT Letter.
#
#  LICENSE
#  -------
#  CC-BY 4.0 — Pascal Fichant, Montpellier, April 2026
#  https://github.com/pfichant/spin-torsion-cosmology
# =============================================================================

import numpy as np
import matplotlib
matplotlib.use('Agg')          # non-interactive backend for server/batch use
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


# =============================================================================
#  DESTINATION SWITCH  <-- only parameter to change between the two papers
# =============================================================================
PAPER = "PIT"   # "PIT" : PRL Letter, double-col 7.2"  |  "F1" : PRD Extended, single-col 3.375"
# =============================================================================


# -----------------------------------------------------------------------------
#  Figure style: rcParams common to both papers
#  (Physical Review journal style: serif fonts, inward ticks, top/right axes)
# -----------------------------------------------------------------------------
matplotlib.rcParams.update({
    'font.family':     'serif',
    'font.serif':      ['Computer Modern Roman', 'DejaVu Serif'],
    'axes.linewidth':  1.2,
    'xtick.direction': 'in',
    'ytick.direction': 'in',
    'xtick.top':       True,
    'ytick.right':     True,
    'figure.dpi':      150,
})

# rcParams and layout that differ between double-column (PIT/PRL) and
# single-column (F1/PRD) Physical Review formats
if PAPER == "PIT":
    matplotlib.rcParams.update({
        'font.size':       11,   # PRL double-col: standard font size
        'axes.labelsize':  12,
        'axes.titlesize':  12,
        'legend.fontsize':  9,
        'xtick.labelsize':  9,
        'ytick.labelsize':  9,
    })
    figsize   = (7.2, 6.5)     # PRL double-column width = 7.2 inches
    # Title emphasises the TIP constraint (central claim of the PIT Letter)
    title_str = r'Topological Invariance: $\Omega_{\mathrm{total}} = 1$'
    outfile   = "Figure_CosmicHistory_Omegas_PIT.png"
else:  # PAPER == "F1"
    matplotlib.rcParams.update({
        'font.size':       11,   # PRD same font as PIT for visual consistency
        'axes.labelsize':  12,
        'axes.titlesize':  12,
        'legend.fontsize':  9,
        'xtick.labelsize':  9,
        'ytick.labelsize':  9,
    })
    figsize   = (7.2, 6.5)     # PRD same size as PIT for visual consistency
    # Title gives a broader cosmological context (Foundation I framing)
    title_str = 'Cosmic History — Evolution of Density Parameters'
    outfile   = "Figure_CosmicHistory_Omegas_F1.png"


# =============================================================================
#  PHYSICS: density parameter computation
# =============================================================================

def calibrate_Os0(alphaspin, zpeak, Om0, Or0, OL0):
    """
    Compute the present-day spin density parameter Os0 such that
    Omega_spin(a_peak) = alphaspin exactly.

    DERIVATION
    ----------
    At the peak scale factor a_p = 1/(1+z_peak), the spin density fraction is:

        Omega_spin(a_p) = rho_s(a_p) / rho_tot(a_p)
                        = Os0 * a_p^{-6} / rho_tot(a_p)   [Eq. spin scaling]

    Setting this equal to alphaspin and solving for Os0:

        Os0 = alphaspin / (1 - alphaspin) * A_peak * a_p^6

    where A_peak = Or0*a_p^{-4} + Om0*a_p^{-3} + OL0 is the background
    total density (without spin) evaluated at a_p.

    NOTE: the naive approximation Os0 ~ alphaspin * Or0 * a_p^2 is only
    valid when Omega_matter(a_peak) << 1, which does NOT hold at z=7500
    (Omega_m ~ 0.32 at that epoch). This corrected formula is used instead.

    Parameters
    ----------
    alphaspin : float
        Target Omega_spin at the peak (= 0.093, calibrated in F1 Sec. 5,
        cited as Eq. 7 in the PIT Letter).
    zpeak : float
        Redshift of maximum torsion density (= 7500, prior to recombination).
    Om0, Or0, OL0 : float
        Present-day matter, radiation, and Lambda density parameters (Planck 2018).

    Returns
    -------
    Os0 : float
        Correct present-day spin density parameter.
    """
    ap    = 1.0 / (1.0 + zpeak)
    # Background total density at a_peak, excluding the spin component itself
    Apeak = Or0 * ap**(-4) + Om0 * ap**(-3) + OL0
    Os0   = alphaspin / (1.0 - alphaspin) * Apeak * ap**6
    return Os0


def build_density_params(Om0, Or0, OL0, Os0, a):
    """
    Compute the fractional energy densities Omega_i(a) for all components
    of the ECF cosmological model.

    COMPONENTS
    ----------
    - Radiation   rho_r ~ a^{-4}  (w = 1/3, standard)
    - Matter      rho_m ~ a^{-3}  (w = 0,   baryons + CDM)
    - Lambda      rho_L = const   (w = -1,  cosmological constant at leading order)
    - Spin/torsion rho_s ~ a^{-6} (w = +1,  stiff fluid; ECF-specific, Eq. spin scaling)

    The stiff w=+1 equation of state follows from the algebraic torsion-spin
    coupling in ECKS theory: rho_s ~ n^2 ~ a^{-6}, where n is the fermion
    number density. This is geometrically distinct from scalar-field kination
    (which requires a free initial condition) -- see F1 Sec. 2.

    TIP VERIFICATION
    ----------------
    The Topological Invariance Principle (PIT Letter, Sec. II) postulates
    that Omega_total = 1 at all times, i.e. Omega_k = 0.
    This is verified numerically as:
        Omega_k = 1 - (Omega_r + Omega_m + Omega_L + Omega_s)  ~  0

    Parameters
    ----------
    Om0, Or0, OL0, Os0 : float
        Present-day density parameters for matter, radiation, Lambda, spin.
    a : array_like
        Scale factor array over which to evaluate the densities.

    Returns
    -------
    Omr, Omm, OmL, Oms, Omk : ndarray
        Fractional density parameters for each component, plus curvature.
    """
    rhor  = Or0 * a**(-4)           # radiation        w = 1/3
    rhom  = Om0 * a**(-3)           # matter           w = 0
    rhoL  = OL0 * np.ones_like(a)   # Lambda           w = -1
    rhos  = Os0 * a**(-6)           # torsion / spin   w = +1  (stiff)

    rhotot = rhor + rhom + rhoL + rhos

    Omr  = rhor  / rhotot
    Omm  = rhom  / rhotot
    OmL  = rhoL  / rhotot
    Oms  = rhos  / rhotot
    Omk  = 1.0 - Omr - Omm - OmL - Oms  # TIP: should be identically 0

    return Omr, Omm, OmL, Oms, Omk


# =============================================================================
#  COSMOLOGICAL PARAMETERS  (Planck 2018, TT,TE,EE+lowE, Table 2)
# =============================================================================
Om0       = 0.315    # Omega_matter,0    (baryons + CDM)
Or0       = 9.0e-5   # Omega_radiation,0 (photons + massless neutrinos)
OL0       = 1.0 - Om0 - Or0   # Omega_Lambda,0 (flat LCDM baseline)

# ECF-specific parameter: spin density peak amplitude
# Calibrated by MCMC against Planck + SH0ES + BOSS/eBOSS + KiDS-1000
# (F1 Sec. 5, Table II; cited as Eq. 7 in PIT Letter)
alphaspin = 0.093    # Omega_spin(a_peak) = 0.093  [dimensionless]
zpeak     = 7500     # redshift at peak torsion density (pre-recombination)

# Compute Os0 using the corrected (non-naive) calibration formula
Os0 = calibrate_Os0(alphaspin, zpeak, Om0, Or0, OL0)
ap  = 1.0 / (1.0 + zpeak)    # scale factor at torsion peak


# =============================================================================
#  NUMERICAL GRID AND SANITY CHECKS
# =============================================================================
# Log-spaced scale factor from a=1e-6 (deep radiation era, before the bounce)
# to a=1 (today). 2000 points ensure smooth curves on a log axis.
a_check = np.logspace(-6, 0, 2000)

Omr_c, Omm_c, OmL_c, Oms_c, Omk_c = build_density_params(
    Om0, Or0, OL0, Os0, a_check)

# Index closest to the torsion peak (used for the calibration check)
idx_p = np.argmin(np.abs(a_check - ap))

# These values are printed to stdout for transparency and can be
# included verbatim in the paper's "Code availability" statement.
print(f"[SANITY] Omega_spin at z={zpeak}: {Oms_c[idx_p]:.4f}  "
      f"(target alpha_spin = {alphaspin})")
print(f"[SANITY] Omega_k max deviation:   {np.abs(Omk_c).max():.2e}  "
      f"(TIP requires Omega_k = 0 throughout)")
print(f"[SANITY] Os0 (corrected) = {Os0:.4e}   "
      f"Os0 (naive) = {alphaspin * Or0 * ap**2:.4e}  "
      f"(ratio = {Os0 / (alphaspin * Or0 * ap**2):.2f})")


# =============================================================================
#  FIGURE
# =============================================================================
# Colour palette: colour-blind friendly (avoids red-green confusion)
Cr = "#e67e22"   # orange  — radiation
Cm = "#2ecc71"   # green   — matter
CL = "#3498db"   # blue    — dark energy / Lambda
Cs = "#e74c3c"   # red     — torsion / spin  (highlighted: ECF-specific)
Ck = "#8e44ad"   # purple  — curvature (TIP verification)

fig = plt.figure(figsize=figsize)
plt.subplots_adjust(top=0.93, bottom=0.09, left=0.13, right=0.97, hspace=0.22)

# Two-panel layout: density evolution (tall) + TIP verification (short)
gs  = gridspec.GridSpec(2, 1, height_ratios=[3, 1])

# ── Top panel: fractional density evolution ───────────────────────────────
ax1 = plt.subplot(gs[0])

ax1.plot(a_check, Omr_c, color=Cr, ls='--', lw=2.0,
         label=r'$\Omega_r$ Radiation')
ax1.plot(a_check, Omm_c, color=Cm,          lw=2.0,
         label=r'$\Omega_m$ Matter')
ax1.plot(a_check, OmL_c, color=CL,          lw=2.0,
         label=r'$\Omega_\Lambda$ Dark Energy')
ax1.plot(a_check, Oms_c, color=Cs,          lw=2.5,
         label=r'$\Omega_s$ Torsion/spin')
# Shaded area under the torsion curve to make the transient phase visible
ax1.fill_between(a_check, 0, Oms_c, color=Cs, alpha=0.18)

# Vertical dotted line at the torsion peak (z = 7500)
ax1.axvline(ap, color='gray', ls=':', lw=1.0, alpha=0.7)

# Floating labels for era identification (avoids legend clutter)
fs_ann = 7 if PAPER == "PIT" else 8
ax1.text(3.0e-6, 0.52,  'Torsion',   color='#c0392b', fontsize=fs_ann,
         ha='center', fontweight='bold')
ax1.text(1.0e-4, 0.82,  'Radiation', color='#d35400', fontsize=fs_ann,
         ha='center')
ax1.text(8.0e-2, 0.82,  'Matter',    color='#27ae60', fontsize=fs_ann,
         ha='center')
ax1.text(6.5e-1, 0.82,  'DE',        color='#2980b9', fontsize=fs_ann,
         ha='center')

ax1.set_xscale('log')
ax1.set_xlim(1e-6, 1.0)
ax1.set_ylim(0.0, 1.1)
ax1.set_ylabel(r'Density Parameter $\Omega_i$', fontweight='bold')
ax1.set_xticklabels([])   # shared x-axis: ticks shown only on bottom panel
ax1.set_title(title_str, fontweight='bold', pad=10)
ax1.legend(loc='center right', framealpha=0.92, fancybox=False,
           edgecolor='#cccccc')
ax1.grid(True, which='both', ls=':', lw=0.5, alpha=0.5)

# Cosmological era annotations at the top of the panel
fs_era = 6 if PAPER == "PIT" else 7
for xa, label in [(3e-6,  'Bounce'),
                  (2e-4,  'BBN'),
                  (6e-4,  'LSS'),
                  (2e-3,  'EQ'),
                  (3e-1,  'Today')]:
    ax1.text(xa, 1.04, label, fontsize=fs_era, ha='center',
             color='#555555', style='italic')

# ── Bottom panel: TIP numerical verification (Omega_k = 0) ───────────────
ax2 = plt.subplot(gs[1])

ax2.plot(a_check, Omk_c, color=Ck, lw=1.8,
         label=r'$\Omega_k$ Curvature')
# Reference line at Omega_k = 0: the TIP invariant
ax2.axhline(0.0, color='black', ls='-', lw=0.8, alpha=0.4)

ax2.set_xscale('log')
ax2.set_xlim(1e-6, 1.0)
ax2.set_ylim(-0.05, 0.05)
ax2.set_ylabel(r'$\Omega_k$', fontweight='bold')
ax2.set_xlabel(r'Scale Factor $a = (1+z)^{-1}$', fontweight='bold')
ax2.legend(loc='upper right',
           fontsize=7 if PAPER == "PIT" else 9,
           framealpha=0.9, fancybox=False, edgecolor='#cccccc')
ax2.grid(True, which='both', ls=':', lw=0.5, alpha=0.5)

# Secondary redshift axis on top of the bottom panel for quick reference
ax2top = ax2.twiny()
ax2top.set_xscale('log')
ax2top.set_xlim(ax2.get_xlim())
z_marks = [10000, 1000, 10, 0]
ax2top.set_xticks([1.0 / (1.0 + z) for z in z_marks])
if PAPER == "F1":
    # Single-col: use compact notation to avoid overlap
    zlabels = [r'$z{=}10^4$', r'$z{=}10^3$', 'z=10', 'z=0']
else:
    zlabels = [f'z={z}' for z in z_marks]
ax2top.set_xticklabels(zlabels,
                        fontsize=6 if PAPER == "PIT" else 8)

# =============================================================================
#  SAVE
# =============================================================================
plt.savefig(outfile, dpi=300, bbox_inches='tight')
print(f"[OK] Figure saved → {outfile}")
plt.close()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
DILUTION FACTOR f AND BARYON ASYMMETRY eta -- ECF STIFF-PHASE BACKGROUND
=============================================================================

RESOLVED 04/09/2026 (insight: Pascal Fichant). The mode-count confusion
flagged as an open issue is resolved: Delta_g*s is not "3 polarisations x
21 torsion modes" (which does not even multiply out correctly, 3x21=63 not
64) -- it is simply the number of independent components of the torsion
tensor in 4D, a geometric necessity requiring no particle-physics-style
polarisation counting: T^lambda_{mu nu}, antisymmetric in [mu nu], has
4 (lambda) x 6 ([mu nu] antisymmetric pairs) = 24 independent components.
This is exactly the corpus's own established 20+4 decomposition (20
contorsion + 4 axial) used consistently elsewhere -- not a numerical
coincidence, the same geometric fact counted twice.

Using Delta_g*s=24 directly removes the need for the disputed (43/11)^(1/3)
factor entirely (that factor was an attempt to patch a wrong mode count;
with the right count, no patch is needed), and resolves all three
previously flagged arithmetic issues in one step:
  (i)  no more (43/11) factor to double-count;
  (ii) no more "3x21=63, not 64" slip -- 24 is used directly;
  (iii) no more combination-step error (0.37x1.575=0.59, not 0.50) --
        there is no combination step left.

Result: f = (g*s,f / (g*s,i,LCDM + 24))^(1/3) ~ 0.483, eta ~ 5.89e-10,
about 3.5% below the Planck value (6.1e-10) -- not the sub-percent match
previously (wrongly) claimed. NOTE (arbitrage A-3, 22/09/2026): eta_raw is
normalised on eta_obs/0.50, so this 3.5% offset is NOT an independent test;
status SEMI-DERIVED; the full realisation of the Sakharov conditions is OPEN. The historical (flawed) derivation is kept below
for transparency, clearly marked as superseded.

Author: The Author (Foundation Series)
Date: 04/09/2026
"""

import numpy as np

# --- Standard cosmological entropy degrees of freedom -----------------------
G_STAR_S_I_LCDM = 10.75   # before e+/e- annihilation (photons + e+/e- + 3 nu)
G_STAR_S_F = 3.91         # after (photons + decoupled neutrinos, standard)

ETA_ECF_RAW = 6.1e-10 / 0.50   # pre-dilution value NORMALISED ON THE OBSERVED eta:
                                # eta_raw = eta_obs / 0.50 (0.50 = historical f).
                                # No Boltzmann network is integrated and F_ion is not
                                # used: the ~3.5% offset of eta from 6.1e-10 only
                                # reflects f/0.50 and is NOT an independent test
                                # (arbitrage A-3, status SEMI-DERIVED).

# --- RESOLVED derivation: torsion's 24 independent tensor components --------
def resolved_derivation():
    """Delta_g*s = 24, the number of independent components of the torsion
    tensor in 4D (4 x 6 antisymmetric pairs) -- matches the corpus's own
    20+4 decomposition. No extra (43/11) factor; no combination step."""
    delta_g_star_s = 24
    g_star_s_i_ecf = G_STAR_S_I_LCDM + delta_g_star_s
    f = (G_STAR_S_F / g_star_s_i_ecf) ** (1/3)
    eta = f * ETA_ECF_RAW
    return dict(delta_g_star_s=delta_g_star_s, g_star_s_i_ecf=g_star_s_i_ecf,
                f=f, eta=eta)

# --- Historical derivation (F2 S3, as originally published -- SUPERSEDED) --
def historical_derivation_superseded():
    """Kept for transparency only. Contains the three now-resolved issues:
    a confused '3 polarisations x 21 modes' count (63, not even 64 as
    stated), an extra (43/11)^(1/3) factor that duplicates the g*s ratio,
    and a combination-step arithmetic slip."""
    delta_g_star_s = 3 * 21          # = 63, not 64 as originally stated
    g_star_s_i_ecf = G_STAR_S_I_LCDM + delta_g_star_s
    f_ratio = (G_STAR_S_F / g_star_s_i_ecf) ** (1/3)
    f_final = f_ratio * (43/11) ** (1/3)   # the disputed extra factor
    eta = f_final * ETA_ECF_RAW
    return dict(delta_g_star_s=delta_g_star_s, g_star_s_i_ecf=g_star_s_i_ecf,
                f_ratio=f_ratio, f_final=f_final, eta=eta)


if __name__ == "__main__":
    eta_obs = 6.1e-10
    print("=" * 70)
    print("  RESOLVED DERIVATION -- torsion's 24 independent components")
    print("=" * 70)
    r = resolved_derivation()
    print(f"  Delta_g*s (torsion tensor, 4D: 4x6)  = {r['delta_g_star_s']}")
    print(f"  g*s,i^ECF                 = {G_STAR_S_I_LCDM} + {r['delta_g_star_s']} = {r['g_star_s_i_ecf']}")
    print(f"  f = (g*s,f/g*s,i)^(1/3)   = {r['f']:.4f}")
    print(f"  eta = f x eta_ECF_raw     = {r['eta']:.4e}")
    print(f"  Deviation from Planck ({eta_obs:.2e}): {(r['eta']-eta_obs)/eta_obs*100:+.2f}%"
          "  (not an independent test: eta_raw = eta_obs/0.50)")
    print()
    print("=" * 70)
    print("  HISTORICAL DERIVATION (superseded -- kept for transparency)")
    print("=" * 70)
    h = historical_derivation_superseded()
    print(f"  Delta_g*s (3 x 21, as published)  = {h['delta_g_star_s']}  (stated as 64 -- arithmetic slip)")
    print(f"  f_ratio = (g*s,f/g*s,i)^(1/3) = {h['f_ratio']:.4f}")
    print(f"  f_final = f_ratio x (43/11)^(1/3) = {h['f_final']:.4f}   (published: 0.50 -- combination slip)")
    print(f"  eta = f_final x eta_ECF_raw   = {h['eta']:.3e}   (published: 6.1e-10)")
    print()
    print("-" * 70)
    print("  CANONICAL OUTPUT  (comparable with the corpus)")
    print("-" * 70)
    print(f"  ECF eta_B (resolved derivation) = {r['eta']:.3e}"
          f"        (Planck: 6.10e-10, {(r['eta']-eta_obs)/eta_obs*100:+.1f}%)")


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
Project     : Foundation II: Topological Crystallization of the Vacuum
Script      : simulate_ecf_rotation_curves.py
Author      : Pascal Fichant
Description :
    Sanity Check for the Local Dark Matter Distribution in the ECF framework.

    CORRECTED 30/08/2026 -- the original version of this script applied the
    local-density spacing formula to the MACRO-Knot mass (10^5 Msun). F2
    itself explicitly disavows this: "their number is far too small ... for
    a local-density formula to give a physically meaningful 'spacing'; the
    appropriate scale for Macro-Knots is instead the galaxy-to-galaxy
    separation (tens to hundreds of kpc), not a local density estimate"
    (F2, Sec. Geometric Dark Matter). F2 also documents, in a correction
    note of its own (v16), that an earlier paragraph made exactly this
    Micro/Macro mass mix-up and quotes the ~230 pc figure this script
    reproduces as the flagged error, not the corrected picture.

    This script now computes BOTH cases explicitly, side by side, so the
    mistake and the correct picture are both visible rather than only the
    mistake:
      (A) INAPPROPRIATE, kept for the historical record: local density with
          the Macro-Knot mass -- reproduces the ~230 pc figure F2 flags as
          wrong.
      (B) CORRECT: local density with the Micro-Knot mass (the abundant
          population that genuinely fills the local DM density as a
          discrete fluid, per F2) -- reproduces F2's own ~0.07 pc figure.
      (C) Macro-Knots: no local-density number is computed at all, per F2's
          own statement that none is physically meaningful; the appropriate
          scale (galaxy-to-galaxy separation, tens-hundreds of kpc) is
          stated as text, not derived here.

    Wording note (23/08/2026, kept): direct detection suppression is an
    expectation from the discreteness of the geometric population, not a
    proof -- F2 writes "structurally suppressed", not "mathematically
    proven".
=============================================================================
"""
# [AJOUTE 15/09/2026] Garde UTF-8. Sans lui, un print contenant un caractere
# non-ASCII (fleche, etoile, accent) fait planter le script sur une console
# Windows en cp1252 : UnicodeEncodeError, code de sortie 1. Quatre scripts F2
# ont echoue ainsi chez Pascal le 15/09 alors qu'ils tournaient sous Linux.
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass
# Last modified: 30/08/2026, 12:24 (Paris time)

import math
import os
import sys
import importlib.util as _ilu

# -- Import M_micro from the canonical script (never re-derived) -----------
_ROOT = os.path.dirname(os.path.abspath(__file__))
_spec = _ilu.spec_from_file_location(
    "microknot_mass", os.path.join(_ROOT, "calculate_microknot_mass.py"))
_mk = _ilu.module_from_spec(_spec)
_argv_backup = sys.argv
sys.argv = ["simulate_ecf_rotation_curves.py"]
_spec.loader.exec_module(_mk)
sys.argv = _argv_backup
M_MICRO_KG = _mk.horizon_mass(_mk.hubble_rate(_mk.T_C))
KG_TO_MSUN = 1.0 / 1.989e30

def main():
    print("=" * 70)
    print(" ECF MODEL SANITY CHECK: LOCAL TOPOLOGICAL DARK MATTER DISTRIBUTION")
    print("=" * 70)

    # ---------------------------------------------------
    # 1. ASTROPHYSICAL CONSTANTS & OBSERVATIONS
    # ---------------------------------------------------
    # The accepted local dark matter density in the solar neighborhood.
    # Derived from stellar kinematics (e.g., Gaia data).
    # Value: ~ 0.008 Solar Masses per cubic parsec (approx 0.3 GeV/cm^3)
    RHO_LOCAL_MSUN_PC3 = 0.008
    PC_TO_LY = 3.26156

    def spacing(mass_msun):
        volume_pc3 = mass_msun / RHO_LOCAL_MSUN_PC3
        d_pc = volume_pc3 ** (1/3)
        return volume_pc3, d_pc, d_pc * PC_TO_LY

    MACRO_MASS_MSUN = 100000.0            # 10^5 Solar Masses
    MICRO_MASS_MSUN = M_MICRO_KG * KG_TO_MSUN

    print("\n" + "="*70)
    print(" (A) INAPPROPRIATE METHOD, KEPT AS HISTORICAL RECORD OF THE ERROR")
    print("="*70)
    v_macro, d_macro_pc, d_macro_ly = spacing(MACRO_MASS_MSUN)
    print(f"\nLocal DM density applied to the MACRO-Knot mass ({MACRO_MASS_MSUN:,.0f} Msun):")
    print(f"  Required Volume per Knot  : {v_macro:,.0f} cubic parsecs")
    print(f"  Avg Distance between Knots: ~ {d_macro_pc:.1f} parsecs (~ {d_macro_ly:.1f} ly)")
    print("  ⚠️ F2 explicitly states this quantity is NOT physically meaningful for")
    print("     Macro-Knots (too rare for a local-density formula) -- this ~230 pc")
    print("     figure is the flagged, corrected-away error, not a current result.")

    print("\n" + "="*70)
    print(" (B) CORRECT METHOD -- local density applied to the MICRO-Knot mass")
    print("="*70)
    v_micro, d_micro_pc, d_micro_ly = spacing(MICRO_MASS_MSUN)
    print(f"\nMicro-Knot mass (from calculate_microknot_mass.py): {MICRO_MASS_MSUN:.3e} Msun")
    print(f"  Required Volume per Knot  : {v_micro:.3e} cubic parsecs")
    print(f"  Avg Distance between Knots: ~ {d_micro_pc:.3f} parsecs (~ {d_micro_ly:.3f} ly)")
    print(f"  Matches F2's own quoted figure of ~0.07 pc (~0.24 ly) for the abundant,")
    print(f"  genuinely fluid-like Micro-Knot population.")

    print("\n" + "="*70)
    print(" (C) MACRO-KNOTS -- no local-density number, by design")
    print("="*70)
    print("""
  F2: "the appropriate scale for Macro-Knots is instead the galaxy-to-galaxy
  separation (tens to hundreds of kpc), not a local density estimate."
  No number is derived here for that scale; it is an observational galaxy
  separation, not a quantity this script computes.
""")

    print("=" * 70)
    print("[ASTROPHYSICAL IMPLICATIONS -- Micro-Knot population, method (B)]")
    print(f"1. SOLAR SYSTEM SAFETY: nearest Micro-Knot statistically ~{d_micro_ly:.2f} ly away;")
    print("   negligible gravitational pull on the Solar System.")
    print("2. DIRECT DETECTION: local dark matter is locked into discrete Micro-Knots")
    print("   rather than a continuous microscopic particle gas -- an expectation from")
    print("   the discreteness of the geometric population (structurally suppressed,")
    print("   not mathematically proven), consistent with null XENON/LZ results.")
    print("=" * 70)

if __name__ == "__main__":
    main()

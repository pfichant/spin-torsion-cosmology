#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_xi_kz_horizon.py  --  ECF Foundation III
======================================================================
Is xi_KZ = 60 Mpc or 65 Mpc? Recomputing the causal horizon on the ECF
background rather than on a LambdaCDM one.

WHY THIS SCRIPT EXISTS
----------------------
The corpus quotes three values for the Kibble-Zurek correlation length:
60 Mpc (the canonical table), 65 Mpc (F3 l.1092 and the VSF plotting
script), and a 50-80 Mpc range. The kill-switch threshold follows:
60 Mpc gives 40.4 Mpc/h, 65 Mpc gives 44 Mpc/h -- and both figures appear.

PO-F3-XI records that direct Kibble-Zurek dilution from T_EW misses the
observed scale by ~24 orders of magnitude, that hypothesis (i) -- a
different transition scale -- is quantitatively excluded, and that the
surviving hypothesis (ii) is that the defect network stays locked to the
comoving causal horizon (scaling behaviour) until a late freeze-out,
with the corpus quoting z ~ 6430.

CLOSED (30/08/2026): the corpus figure of z~6430 was itself the
LambdaCDM-background artefact this script exists to catch (see below).
Following this script's own result, the corpus (F2 and Foundation III)
has been corrected throughout to the ECF-background value, z~5145 (printed
below; the docstring said z~5153 until 15/10/2026), with
z~6430 kept only as an explicitly labelled superseded figure. The
diagnostic below is left as-is: it is what established the correction.

That statement is checkable. If (ii) holds, xi_KZ IS the comoving
particle horizon at freeze-out, and the number follows from the
background -- it is not a free choice between 60 and 65.

WHY THE BACKGROUND MATTERS HERE
-------------------------------
A first pass on a standard LambdaCDM background (H0 = 67.32) gave
64.4 Mpc at z = 6430, apparently favouring 65. But the ECF background is
NOT LambdaCDM: it carries a stiff spin fluid scaling as (1+z)^6, which
dominates at high z and shortens the horizon. Concluding from the
LambdaCDM number would be comparing the wrong quantity -- so the ECF
background is used here, imported from the calibrated script so that this
computation cannot drift from it.

Dependency: numpy, scipy. Usage: python3 check_xi_kz_horizon.py
======================================================================
"""
# Last modified: 30/08/2026, 12:24 (Paris time)

import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

import os
import importlib.util
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

_here = os.path.dirname(os.path.abspath(__file__))
_category = os.path.dirname(_here)          # .../Foundation_3/02_Scientific_Code
_found3 = os.path.dirname(_category)        # .../Foundation_3
_repo_root = os.path.dirname(_found3)        # .../spin-torsion-cosmology
_candidates = [
    os.path.join(_here, "..", "Scripts_F1", "script_01_solve_sound_horizon.py"),
    os.path.join(_here, "..", "..", "Scripts_F1", "script_01_solve_sound_horizon.py"),
    # [HARDENED 06/09/2026, again] This script moved from Scripts_F3/ root
    # into Scripts_F3/A_Core_Calculations/ (one level deeper), AND
    # script_01 moved from Scripts_F1/ root into Scripts_F1/A_Core_Calculations/
    # (same night's A/B split) -- both facts combined need this candidate.
    os.path.join(_here, "..", "..", "Scripts_F1", "A_Core_Calculations",
                 "script_01_solve_sound_horizon.py"),
    os.path.join(_here, "script_01_solve_sound_horizon.py"),
    # This working corpus's own A/B split (Scripts_F1/A_Core_Calculations,
    # no Foundation_1/02_Scientific_Code wrapper) -- added 06/09/2026 when
    # Scripts_F1 and Scripts_F2 were reorganised the same way Scripts_F3
    # already was.
    os.path.join(_here, "..", "Scripts_F1", "A_Core_Calculations",
                 "script_01_solve_sound_horizon.py"),
    # Foundation_1 mirroring Foundation_3's own 02_Scientific_Code layout,
    # under whichever category subfolder actually holds it there:
    os.path.join(_repo_root, "Foundation_1", "02_Scientific_Code",
                 "A_Core_Calculations", "script_01_solve_sound_horizon.py"),
    os.path.join(_repo_root, "Foundation_1", "02_Scientific_Code",
                 "B_Paper_Plots", "script_01_solve_sound_horizon.py"),
    os.path.join(_repo_root, "Foundation_1", "Scripts_F1",
                 "script_01_solve_sound_horizon.py"),
    os.path.join(_repo_root, "Foundation_1", "script_01_solve_sound_horizon.py"),
]
_path = None
for _c in _candidates:
    _c = os.path.normpath(_c)
    if os.path.exists(_c):
        _path = _c
        break
if _path is None:
    _path = os.path.normpath(_candidates[0])  # keep old default for the error message

_spec = importlib.util.spec_from_file_location("sh_ecf", _path)
_sh = importlib.util.module_from_spec(_spec)
try:
    _spec.loader.exec_module(_sh)
except SystemExit:
    pass

C_KM = 299792.458

print("=" * 70)
print("  xi_KZ from the causal horizon  --  ECF background")
print("=" * 70)
print(f"\n  background imported from: {os.path.basename(_path)}")
print(f"  Om_m = {_sh.Om_m:.4f}   Om_r = {_sh.Om_r:.4e}   "
      f"Om_spin_0 = {_sh.Om_spin_0:.3e}")
print(f"  stiff term: Om_spin_0 (1+z)^6   [absent from LambdaCDM]")


def chi_comoving(z, H_of_z):
    """Comoving particle horizon at redshift z: integral from z to infinity."""
    val, _ = quad(lambda zz: 1.0 / H_of_z(zz), z, np.inf, limit=400)
    return C_KM * val


print("\n" + "-" * 70)
print("  (1) Comoving horizon, ECF vs LambdaCDM")
print("-" * 70)
print(f"  {'z':>7} {'ECF (Mpc)':>12} {'LCDM (Mpc)':>12} {'ratio':>8}")
for z in (5600, 6365, 6430, 6953, 7500):
    he = chi_comoving(z, _sh.Hz_ECF)
    hl = chi_comoving(z, _sh.Hz_LCDM)
    print(f"  {z:>7} {he:>12.2f} {hl:>12.2f} {he/hl:>8.4f}")

print("\n" + "-" * 70)
print("  (2) Which z gives 60 Mpc, which gives 65 -- on the ECF background")
print("-" * 70)
for target in (60.0, 65.0):
    try:
        z = brentq(lambda zz: chi_comoving(zz, _sh.Hz_ECF) - target, 500, 60000)
        print(f"    xi_KZ = {target:.0f} Mpc  <=>  z_freeze = {z:.0f}")
    except ValueError:
        print(f"    xi_KZ = {target:.0f} Mpc  : not reachable on this background")

print("\n" + "-" * 70)
print("  (3) The corpus quotes z ~ 6430. What does the ECF background give?")
print("-" * 70)
xi_6430 = chi_comoving(6430, _sh.Hz_ECF)
h = _sh.h_planck
print(f"    xi_KZ(z=6430) = {xi_6430:.2f} Mpc = {xi_6430*h:.2f} Mpc/h")
print(f"    distance to 60 Mpc : {abs(xi_6430-60):.2f} Mpc "
      f"({100*abs(xi_6430-60)/60:.1f} %)")
print(f"    distance to 65 Mpc : {abs(xi_6430-65):.2f} Mpc "
      f"({100*abs(xi_6430-65)/65:.1f} %)")

print("\n" + "=" * 70)
print("  READING THIS")
print("=" * 70)
print("  The stiff (1+z)^6 term makes H larger at high z, hence the ECF")
print("  horizon SHORTER than the LambdaCDM one at the same redshift.")
print("  The comparison therefore has to be done on the ECF background;")
print("  the LambdaCDM number would not answer the question asked.")
print()
print("WHAT THIS DOES NOT ESTABLISH:")
print("  * that hypothesis (ii) is correct -- PO-F3-XI keeps it open, and")
print("    this script only asks what it would imply if it held;")
print("  * the freeze-out redshift itself, which is not derived anywhere;")
print("  * the 50-80 Mpc range, which comes from the VSF calibration and")
print("    is a separate statement from the horizon argument.")

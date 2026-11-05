#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
profile_likelihood_calibrated.py  --  ECF Foundation I
======================================================================
Uncertainties on the calibrated numbers, by likelihood profiling.

WHY THIS SCRIPT EXISTS
----------------------
Table tab:calibrated_budget lists five calibrated numbers and none of
them carries an uncertainty. As a cosmologist at the Laboratoire Univers
et Particules de Montpellier puts it: a result quoted without an
uncertainty is not a statistical statement. Foundation I now
says explicitly that (w0, wa) is a calibration point rather than a
measurement; this script begins to supply what is missing.

METHOD, AND WHY THIS CHAIN
--------------------------
The sound-horizon chain is used because it is the cleanest one available:
a single target with a single published uncertainty,

    r_s(ECF) = 135.65 +/- 0.2 Mpc  (A-6, 22/09/2026; was 135.8),

so the resulting interval is a genuine likelihood interval rather than an
artefact of relative weighting. (By contrast joint_fit_trilemma.py, which
also carries a chi2, warns in its own header that its numbers are
exploratory and that the required omega_m shift ranges from 19% to 46%
depending on the weight given to theta_*: an uncertainty derived there
would inherit that instability.)

For one parameter, the 1-sigma interval is the set where

    Delta chi2 = chi2(p) - chi2_min  <=  1.

Two parameters enter r_s: TAU_TOR (damping of the sound speed) and
SPIN_RAD_RATIO = Omega_spin,peak (the spin fluid amplitude). Each is
profiled with the other held at its calibrated value, which is the
appropriate statement here since the corpus treats them as separately
anchored quantities, not as a jointly fitted pair.

PROPAGATION
-----------
calibrate_w0wa.py states the two relations explicitly:

    w0 = -1 + Omega_spin,peak                  (empirical identification)
    wa = -xi * Omega_spin,peak,  xi = 1.645    (phenomenological)

These are relations, not free parameters, so the uncertainty on w0 and wa
follows from that on Omega_spin,peak by differentiation. No sampling is
needed, and none is claimed.

WHAT THIS DOES NOT ESTABLISH
----------------------------
  * not a posterior: profiling gives a frequentist interval, and the
    corpus should not describe the result as a Bayesian credible region;
  * xi = 1.645 is itself calibrated and carries no uncertainty here, so
    the interval on wa propagates Omega_spin,peak ALONE and is therefore
    a LOWER bound on the true uncertainty;
  * the r_s target uncertainty (+/- 0.2 Mpc) is taken from the corpus,
    not re-derived;
  * nothing here addresses F_ion or xi_KZ, the two remaining calibrated
    numbers of the table.

Dependency: numpy, scipy. Usage: python3 profile_likelihood_calibrated.py
======================================================================
"""

import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

import os
import numpy as np
from scipy.optimize import brentq

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------------
# Import the calibrated chain itself, so this script cannot drift from it
# ---------------------------------------------------------------------
import importlib.util
_spec = importlib.util.spec_from_file_location(
    "sound_horizon",
    os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 "script_01_solve_sound_horizon.py"))
_sh = importlib.util.module_from_spec(_spec)
# Executed under a name that is not "__main__", so any __main__ block in the
# imported script does not run: we only want its functions and constants.
try:
    _spec.loader.exec_module(_sh)
except SystemExit:
    pass

RS_TARGET = float(os.environ.get('LOTA67_RS_TARGET', '135.65'))  # [A-6 22/09/2026] was 135.8 ; env LOTA67_RS_TARGET=135.8 reproduces the old-target diagnostic
RS_SIGMA = 0.2             # Mpc, corpus stated uncertainty
TAU_CAL = _sh.TAU_TOR      # 0.9975
SPIN_CAL = _sh.SPIN_RAD_RATIO   # 0.093
XI_WA = 1.645              # calibrate_w0wa.py

print("=" * 70)
print("  Likelihood profiling of the calibrated numbers")
print("=" * 70)
print(f"\n  target : r_s(ECF) = {RS_TARGET} +/- {RS_SIGMA} Mpc")
print(f"  calibrated: TAU_TOR = {TAU_CAL},  Omega_spin,peak = {SPIN_CAL}")


def rs_of(tau=None, spin=None):
    """r_s(ECF) recomputed with one constant overridden."""
    # /!\ Om_spin_0 is computed ONCE at module load (line 131 of the imported
    # script) from SPIN_RAD_RATIO. Overriding the constant afterwards leaves
    # Om_spin_0 stale, and r_s then looks completely insensitive to the spin
    # amplitude -- which it is not. The derived quantity must be recomputed.
    old_t, old_s, old_o = _sh.TAU_TOR, _sh.SPIN_RAD_RATIO, _sh.Om_spin_0
    if tau is not None:
        _sh.TAU_TOR = tau
    if spin is not None:
        _sh.SPIN_RAD_RATIO = spin
        _sh.Om_spin_0 = spin * _sh.Om_r / (1.0 + _sh.Z_TRANS) ** 2
    try:
        val = _sh.integrate_rs(_sh.Hz_ECF, cs_scale=_sh.TAU_TOR)
    finally:
        _sh.TAU_TOR, _sh.SPIN_RAD_RATIO, _sh.Om_spin_0 = old_t, old_s, old_o
    return val


def dchi2(rs):
    return ((rs - RS_TARGET) / RS_SIGMA) ** 2


def profile(name, cal, setter, lo, hi):
    """1-sigma interval: the set where Delta chi2 <= 1."""
    c_min = dchi2(rs_of(**{setter: cal}))
    f = lambda p: dchi2(rs_of(**{setter: p})) - c_min - 1.0
    out = []
    for a, b in ((lo, cal), (cal, hi)):
        try:
            out.append(brentq(f, a, b, xtol=1e-12))
        except ValueError:
            out.append(None)
    return c_min, out


print("\n" + "-" * 70)
print("  (1) TAU_TOR")
print("-" * 70)
c0, (t_lo, t_hi) = profile("TAU_TOR", TAU_CAL, "tau", 0.980, 1.0)
print(f"    chi2 at the calibrated value : {c0:.4f}")
if t_lo and t_hi:
    sig = max(TAU_CAL - t_lo, t_hi - TAU_CAL)
    print(f"    1-sigma interval : [{t_lo:.6f}, {t_hi:.6f}]")
    print(f"    => TAU_TOR = {TAU_CAL:.4f} +/- {sig:.4f}   "
          f"({100*sig/TAU_CAL:.3f} % relative)")
else:
    print(f"    interval not bracketed in [0.980, 1.0]: lo={t_lo}, hi={t_hi}")

print("\n" + "-" * 70)
print("  (2) Omega_spin,peak")
print("-" * 70)
c0s, (s_lo, s_hi) = profile("SPIN", SPIN_CAL, "spin", 0.01, 0.30)
print(f"    chi2 at the calibrated value : {c0s:.4f}")
if s_lo and s_hi:
    sig_s = max(SPIN_CAL - s_lo, s_hi - SPIN_CAL)
    print(f"    1-sigma interval : [{s_lo:.5f}, {s_hi:.5f}]")
    print(f"    => Omega_spin,peak = {SPIN_CAL:.3f} +/- {sig_s:.3f}   "
          f"({100*sig_s/SPIN_CAL:.1f} % relative)")

    print("\n" + "-" * 70)
    print("  (3) Propagation to w0 and wa")
    print("-" * 70)
    print("    w0 = -1 + Omega_spin,peak     =>  sigma(w0) = sigma(Omega)")
    print(f"    wa = -{XI_WA} * Omega_spin,peak  =>  sigma(wa) = {XI_WA} * sigma(Omega)")
    w0 = -1 + SPIN_CAL
    wa = -XI_WA * SPIN_CAL
    print()
    print(f"    w0 = {w0:+.4f} +/- {sig_s:.4f}      (corpus quotes -0.904)")
    print(f"    wa = {wa:+.4f} +/- {XI_WA*sig_s:.4f}      (corpus quotes -0.153)")
    print()
    print("    /!\\ These are LOWER bounds on the uncertainty: xi = 1.645 is")
    print("        itself calibrated and its own error is not propagated here.")
else:
    print(f"    interval not bracketed: lo={s_lo}, hi={s_hi}")

# ---------------------------------------------------------------------
# (4) F_ion, through the S8 chain
# ---------------------------------------------------------------------
print("\n" + "-" * 70)
print("  (4) F_ion  --  S8 chain")
print("      HISTORICAL CALIBRATION: gamma_spin = 0.3116, S8_LCDM = 0.832, former Planck\n"
      "      background (DEC-A7-POST-07A); this profile belongs to the historical chain")
print("-" * 70)
S8_LCDM, S8_OBS, S8_SIG, GAMMA = 0.832, 0.766, 0.014, 0.3116
F_ION_CAL = 1.2765

def s8_of(f_ion):
    return S8_LCDM / (1.0 + (f_ion - 1.0) * GAMMA)

def dchi2_s8(f_ion):
    return ((s8_of(f_ion) - S8_OBS) / S8_SIG) ** 2

c_min_f = dchi2_s8(F_ION_CAL)
print(f"    S8(F_ion={F_ION_CAL}) = {s8_of(F_ION_CAL):.4f}   target {S8_OBS} +/- {S8_SIG}")
print(f"    chi2 at the calibrated value : {c_min_f:.4f}")
g = lambda p: dchi2_s8(p) - c_min_f - 1.0
try:
    f_lo = brentq(g, 1.0, F_ION_CAL, xtol=1e-12)
    f_hi = brentq(g, F_ION_CAL, 3.0, xtol=1e-12)
    sig_f = max(F_ION_CAL - f_lo, f_hi - F_ION_CAL)
    print(f"    1-sigma interval : [{f_lo:.4f}, {f_hi:.4f}]")
    print(f"    => F_ion = {F_ION_CAL:.4f} +/- {sig_f:.4f}   "
          f"({100*sig_f/F_ION_CAL:.1f} % relative)")
except ValueError as e:
    print(f"    interval not bracketed: {e}")
print()
print("    /!\\ F_ion is NOT a free parameter of the S8 sector: the imported")
print("        script states it is fixed by the sound-horizon calibration, and")
print("        that only gamma_spin is adjusted. The interval above therefore")
print("        answers 'how far could F_ion move before S8 leaves its band',")
print("        NOT 'what does the S8 data measure F_ion to be'.")

# ---------------------------------------------------------------------
# (5) xi_KZ -- not constrainable today, and the corpus says why
# ---------------------------------------------------------------------
print("\n" + "-" * 70)
print("  (5) xi_KZ  --  NOT profiled, deliberately")
print("-" * 70)
print("    The Void Size Function test on DESIVAST DR1 reaches only")
print("    R_max = 31.7 Mpc/h, while the ECF threshold sits at 40.4 Mpc/h (xi_KZ = 60 Mpc):")
print("    the BGS sample (z < 0.24) does not extend far enough to bound")
print("    the parameter. Foundation III states this and defers the")
print("    definitive test to Euclid DR1. No interval is quoted here,")
print("    because the data cannot supply one.")

print("\n" + "=" * 70)
print("  READING THIS")
print("=" * 70)
print("  These are FREQUENTIST profile intervals, not Bayesian credible")
print("  regions. They say: within the sound-horizon chain alone, and with")
print("  the other calibrated constants held fixed, this is the range over")
print(f"  which the parameter stays compatible with r_s = {RS_TARGET} +/- {RS_SIGMA} Mpc.")
print()
print("  They do NOT convert the calibration point into a measurement.")
print("  What they do is make comparisons statistical: a statement such as")
print("  'agrees to 2.4%' can now be read against a width.")

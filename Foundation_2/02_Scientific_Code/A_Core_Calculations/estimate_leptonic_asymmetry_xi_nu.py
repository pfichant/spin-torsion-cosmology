#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
LEPTONIC (NEUTRINO) CHIRAL ASYMMETRY -- ORDER-OF-MAGNITUDE ESTIMATE (ECF)
=============================================================================

ABSTRACT:
    The geometric chiral-splitting mechanism of Foundation II (Appendix,
    "Chiral Selection: Microphysics") is universal to any Dirac fermion: it
    is derived from the Einstein-Cartan action for a generic spin-1/2 field
    coupled only to the gravitational spin connection, with no gauge field
    and no dependence on electric, colour, or weak-isospin charge (confirmed
    03-04/09/2026, see Scripts_F2/../Suivi_Recherche/dossiers/
    ECF_NOTE_ABJ_terminologie_F2.md for the full derivation history).

    This script asks the natural follow-up question: if the SAME mechanism
    that produces the observed baryon asymmetry eta_B ~ 6.1e-10 also acts on
    neutrinos, what neutrino degeneracy parameter xi_nu = mu_nu/T does it
    predict, and is that prediction within reach of current observational
    bounds?

STATUS -- READ BEFORE CITING:
    This is an ORDER-OF-MAGNITUDE ESTIMATE BY ANALOGY, not a first-principles
    derivation. Two ingredients specific to the baryon calculation are
    carried over UNCHECKED for neutrinos:
      (a) the survival/dilution fraction f ~ 0.50 computed for baryons
          (entropy dilution across e+/e- annihilation) is assumed to apply
          at the SAME order of magnitude to the neutrino sector; neutrinos
          do not annihilate away via strong or electromagnetic interactions
          the way quark-antiquark pairs do, so this is the weakest link in
          the estimate;
      (b) whether cosmological neutrinos are Dirac or Majorana particles is
          NOT specified anywhere in the ECF corpus (checked exhaustively,
          04/09/2026); a Majorana nature would change what "lepton number
          conservation" even means here. The estimate below assumes Dirac,
          matching the generic field used in the appendix's own derivation.
    Open track: PO-F2-NU (Foundation II). Not a citable prediction until (a)
    and (b) are resolved by a dedicated calculation.

METHOD:
    1. Take eta_ECF (pre-dilution baryon asymmetry), calibrated in
       Foundation II from the Foundation I background (F_ion = 1.2765).
    2. By the universality of the chiral-splitting mechanism, assume the
       pre-dilution LEPTONIC asymmetry is of the SAME order (same Delta_mu,
       same underlying rho_spin -- the mechanism does not distinguish
       fermion species).
    3. Convert a number-asymmetry-like quantity into the neutrino
       degeneracy parameter xi_nu using the standard relation between a
       small chemical-potential-driven asymmetry and xi (Kolb & Turner
       1990-style leading-order expansion): eta_nu ~ (pi^2/12) * xi_nu, i.e.
       xi_nu ~ eta_nu * 12/pi^2 for xi_nu << 1.
    4. Compare to published BBN / CMB+LSS bounds on xi_nu (Sec. "Bounds"
       below; see also arXiv:2606.28135 for a recent combined analysis).

Dependency: none beyond the standard library. Usage:
    python3 estimate_leptonic_asymmetry_xi_nu.py
=============================================================================
"""
# Last modified: 04/09/2026 (Paris time)
# Corpus: Foundation II -- github.com/pfichant/spin-torsion-cosmology
import math
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# ---------------------------------------------------------------------------
# 1. INPUTS -- taken directly from Foundation II, Sec. 3 (Chiral Baryogenesis)
# ---------------------------------------------------------------------------
ETA_ECF_PRE_DILUTION = 1.2e-9   # eta_ECF, calibrated on the F1 background
F_SURVIVAL_BARYON = 0.50        # f, entropy-dilution survival fraction (derived, F2 Eq. fECF_derived)
ETA_OBSERVED = 6.1e-10          # eta = f * eta_ECF, matches Planck to 0.5%

# Sanity check: reproduce the corpus's own published chain before estimating
# anything new. If this does not match, stop -- the inputs above are stale.
_eta_check = F_SURVIVAL_BARYON * ETA_ECF_PRE_DILUTION
assert abs(_eta_check - ETA_OBSERVED) / ETA_OBSERVED < 0.02, (
    f"F2's own baryon chain does not reproduce: f*eta_ECF = {_eta_check:.3e}, "
    f"expected {ETA_OBSERVED:.3e}. Inputs are stale -- fix before trusting "
    f"anything below."
)

# ---------------------------------------------------------------------------
# 2. PUBLISHED BOUNDS ON THE NEUTRINO DEGENERACY PARAMETER xi_nu = mu_nu/T
#    (literature values, NOT computed here -- see search citations in the
#    module docstring and PO-F2-NU note for sources)
# ---------------------------------------------------------------------------
BOUNDS_XI_NU = {
    "BBN, historical tight bound (electron flavour)":      0.07,
    "BBN, electron flavour, relaxed analysis":             1.1,
    "BBN, mu/tau flavour":                                 6.9,
    "CMB+LSS combined, 2-sigma (recent analysis)":         0.7,
}


def estimate_xi_nu(eta_pre_dilution: float, f_survival_guess: float) -> float:
    """
    Convert a pre-dilution chiral-asymmetry-like quantity into an estimated
    present-day xi_nu, using the SAME survival fraction as baryons as a
    rough stand-in (ingredient (a) flagged as unchecked in the docstring).

    eta_nu ~ (pi^2/12) * xi_nu  =>  xi_nu ~ eta_nu * 12 / pi^2
    (leading-order relation for a small Fermi-Dirac chemical-potential
    asymmetry; see e.g. Kolb & Turner, "The Early Universe", ch. 3).
    """
    eta_nu_post_dilution = f_survival_guess * eta_pre_dilution
    xi_nu = eta_nu_post_dilution * 12.0 / math.pi**2
    return xi_nu


def main() -> None:
    print("Leptonic (neutrino) chiral asymmetry -- order-of-magnitude estimate")
    print("=" * 74)
    print(f"  eta_ECF (pre-dilution, calibrated F2)     = {ETA_ECF_PRE_DILUTION:.2e}")
    print(f"  f (baryon survival fraction, derived F2)  = {F_SURVIVAL_BARYON:.2f}")
    print(f"  eta_B = f * eta_ECF                        = {_eta_check:.2e}  "
          f"(F2/Planck: {ETA_OBSERVED:.2e}, check OK)")
    print()
    print("  Assuming the SAME order-unity survival fraction applies to the")
    print("  leptonic sector (UNCHECKED -- see module docstring, caveat (a)):")
    xi_nu_est = estimate_xi_nu(ETA_ECF_PRE_DILUTION, F_SURVIVAL_BARYON)
    print(f"    xi_nu (estimated)                        ~ {xi_nu_est:.2e}")
    print()
    print("-" * 74)
    print("  COMPARISON TO PUBLISHED BOUNDS (literature, not computed here)")
    print("-" * 74)
    for label, bound in BOUNDS_XI_NU.items():
        ratio = bound / xi_nu_est
        print(f"    {label:48s} |xi_nu| < {bound:>5.2f}   "
              f"(bound is {ratio:.1e}x larger than the estimate)")
    print("-" * 74)
    print()
    print("CONCLUSION (order-of-magnitude, not a first-principles result):")
    print("  The universal geometric mechanism, applied to neutrinos by analogy,")
    print("  predicts an asymmetry SEVEN TO EIGHT ORDERS OF MAGNITUDE below every")
    print("  published observational bound. This is not an exclusion of the")
    print("  mechanism -- it is a statement that the predicted effect is currently")
    print("  undetectable, not that it is wrong or forbidden.")
    print()
    print("  This does NOT resolve PO-F2-NU: the Dirac/Majorana question and the")
    print("  leptonic survival fraction remain open (see module docstring).")
    print("=" * 74)

    # ── CANONICAL OUTPUT (style matches calculate_baryon_asymmetry.py) ─────
    print()
    print("-" * 62)
    print("  CANONICAL OUTPUT  (comparable with the corpus)")
    print("-" * 62)
    print(f"  ECF xi_nu (order-of-magnitude estimate) = {xi_nu_est:.2e}"
          f"   (tightest published bound: 0.07, i.e. ~{0.07/xi_nu_est:.0e}x above)")


if __name__ == "__main__":
    main()

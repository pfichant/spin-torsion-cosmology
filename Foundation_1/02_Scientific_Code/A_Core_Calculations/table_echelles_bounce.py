"""
================================================================================
SCRIPT: table_echelles_bounce.py — v2
Paper: Foundation I: The Metric Universe (Extended), Appendix H & I
Author: Pascal Fichant (2026)
================================================================================
DESCRIPTION:
  Generates a contextual scale comparison table from today's observable universe
  down to the ECF primordial bounce, placing the bounce radius in perspective
  against familiar physical objects.

VALIDATION STATUS (independent audit, 2026-04-15):
  v1 → v2 corrections:
    1. R_bounce hardcoded (1e-6) → DERIVED explicitly from A_MIN and R_UNIV.
       A_MIN = (rho_rad0 / rho_Planck)^(1/4) = 1.69×10^-32 (paper: 10^-32 ✓)
       R_bounce = R_UNIV × A_MIN = 1e26 × 1.69e-32 = 1.69e-6 m  ✓
    2. Row ordering fixed: rows now sorted by physical size (descending) so
       the Compression column decreases monotonically. Bounce row was last
       in v1 despite being physically LARGER than the Neutron row → confusing.
    3. Column header clarified: 'R_univ / R_scale' distinguishes context
       (how much bigger is universe than this object) from 'R_univ/R_bounce',
       which equals 1/a_min. Both are now labeled explicitly.
    4. Physical labels added: R_univ documented as Hubble-scale OOM proxy;
       Earth = diameter OOM; Bounce = entire observable universe compressed
       to the size of a bacterium (~1 µm).
    5. Cross-reference added to paper Appendix H/I for a_min derivation.

INPUTS (traceable to paper Appendix H):
  rho_Planck = 5.15×10^96 kg/m^3   Planck density — paper App. H
  rho_rad0   = 4.2×10^-31 kg/m^3   Present radiation density (photons + nu)
  A_MIN      = (rho_rad0/rho_Planck)^(1/4)   derived — paper App. H, Eq. a_min
  R_UNIV     = 1e26 m               Hubble-scale proxy (actual comoving ≈ 4.4×10^26 m)

KEY PHYSICAL INTERPRETATION:
  The bounce does NOT compress the universe to nuclear or sub-nuclear density.
  The entire observable universe is compressed to ~1 µm (bacterium scale).
  This is a geometric bounce at the Planck DENSITY, not Planck LENGTH.
================================================================================
"""

import math

# =============================================================================
# 1. CONSTANTS
# =============================================================================
# Planck density — paper Appendix H (Weyssenhoff-fluid critical density)
rho_Planck = 5.15e96    # kg/m^3

# Present-day radiation energy density (CMB photons + cosmic neutrino background)
# See paper Appendix H: rho_rad,0 = 4.2×10^-31 kg/m^3
rho_rad0   = 4.2e-31    # kg/m^3

# Minimum scale factor (paper App. H, Eq. a_min):  a_min = (rho_rad0/rho_Planck)^(1/4)
A_MIN = (rho_rad0 / rho_Planck)**0.25

# Observable universe — Hubble-scale order-of-magnitude proxy
# Actual comoving radius ≈ 4.4×10^26 m; Hubble radius c/H0 ≈ 1.27×10^26 m.
# 1e26 m is used as a round OOM reference consistent with the paper.
R_UNIV = 1e26           # m

# Bounce radius: R_bounce = R_univ × a_min  (derived, NOT hardcoded)
R_bounce = R_UNIV * A_MIN


# =============================================================================
# 2. HELPERS
# =============================================================================
def sci_notation(x):
    """Return '10^n' where n = nearest integer of log10(x)."""
    if x == 0:
        return "0"
    exp = int(round(math.log10(abs(x))))
    return f"10^{exp}"


# =============================================================================
# 3. TABLE DATA
# =============================================================================
# Rows ordered by physical size DESCENDING for monotone Compression column.
# Label, physical size (m), descriptive note
rows = [
    ("Observable Univ.",  R_UNIV,    "Hubble-scale proxy (OOM)"),
    ("Earth (diameter)", 1e7,         "~12,742 km — OOM 10^7 m"),
    ("Bounce (ECF)",      R_bounce,   f"R_univ × a_min = 1e26 × {A_MIN:.1e} m"),
    ("Atom (H, Bohr)",   1e-10,       "Bohr radius 0.053 nm → OOM 10^-10 m"),
    ("Neutron",           1e-15,      "Charge radius ~0.8 fm → OOM 10^-15 m"),
]


# =============================================================================
# 4. MAIN OUTPUT
# =============================================================================
if __name__ == "__main__":
    print(">>> Generating Table: Physical Scales at the Bounce (v2)\n")

    # --- Derived a_min verification ---
    print(f"  A_MIN = (rho_rad0/rho_Planck)^(1/4)")
    print(f"        = ({rho_rad0:.2e} / {rho_Planck:.2e})^0.25")
    print(f"        = {A_MIN:.2e}  [paper App. H: 10^-32]")
    print(f"  R_bounce = R_UNIV × A_MIN = {R_UNIV:.0e} × {A_MIN:.2e} = {R_bounce:.2e} m")
    print(f"  Compression at bounce = R_UNIV/R_bounce = 1/A_MIN = {1.0/A_MIN:.2e}\n")

    # --- Main table ---
    print(f"| {'Scale':<20} | {'Physical Size':<14} | {'R_univ/R_scale':<15} | {'Notes':<38} |")
    print(f"|{'-'*22}|{'-'*16}|{'-'*17}|{'-'*40}|")

    for name, size, note in rows:
        size_str  = sci_notation(size) + " m"
        ratio_str = sci_notation(R_UNIV / size)
        print(f"| {name:<20} | {size_str:<14} | {ratio_str:<15} | {note:<38} |")

    print()
    print("  (*) Column 'R_univ/R_scale':")
    print("      For reference objects (Earth/Atom/Neutron): ratio = size of universe")
    print("        relative to that object — a contextual scale comparison.")
    print("      For Bounce row: ratio = 1/A_MIN = compression factor of the universe")
    print("        from today to the bounce — a direct cosmological quantity.")
    print("      Physical reading: the ENTIRE observable universe at the bounce fits")
    print(f"        into a sphere of radius ~{R_bounce*1e6:.1f} µm (bacterium scale).")
    print("      This is a density bounce (rho ~ rho_Planck), NOT a size singularity.")
    print()
    print("  Cross-reference: paper Appendix H (Eq. a_min), Appendix I (bounce physics).")

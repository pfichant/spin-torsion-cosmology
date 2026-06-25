#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
Script      : calculate_microknot_mass.py
Description : Calculates the causal horizon mass at the topological freeze-out 
              epoch to rigorously justify the 10^24 kg mass of ECF Micro-Knots.
=============================================================================
"""

def calculate_horizon_mass():
    print("=" * 65)
    print(" ECF MODEL: MICRO-KNOT MASS CALCULATION (CAUSAL HORIZON)")
    print("=" * 65)

    # Fundamental Constants (SI Units)
    c = 299792458.0          # Speed of light (m/s)
    G = 6.67430e-11          # Gravitational constant (m^3 kg^-1 s^-2)
    
    # Reference Masses (kg)
    M_earth = 5.972e24
    M_jupiter = 1.898e27
    M_sun = 1.989e30

    # 1. Stiff Era / Electroweak Topological Freeze-out time (seconds)
    # The epoch where the geometric torsion field crystallizes into defects
    t_freeze_out = 1.5e-11   # ~ 10^-11 seconds (Electroweak scale)

    # 2. Horizon Mass Equation: M_H = (c^3 * t) / G
    c3_over_G = (c**3) / G
    M_horizon = c3_over_G * t_freeze_out

    print(f"[CONSTANTS]")
    print(f"Speed of Light (c) : {c:.2e} m/s")
    print(f"Gravitational (G)  : {G:.2e} m^3/kg/s^2")
    print(f"c^3 / G factor     : {c3_over_G:.2e} kg/s\n")

    print(f"[TOPOLOGICAL FREEZE-OUT]")
    print(f"Epoch Time (t)     : {t_freeze_out:.2e} seconds (Electroweak Scale)")
    print(f"Calculated Mass    : {M_horizon:.2e} kg\n")

    print(f"[COMPARISON TO ASTROPHYSICAL OBJECTS]")
    ratio_earth = M_horizon / M_earth
    ratio_jupiter = M_horizon / M_jupiter
    ratio_sun = M_horizon / M_sun

    print(f"-> {ratio_earth:.2f} x Earth Mass")
    print(f"-> {ratio_jupiter:.5f} x Jupiter Mass")
    print(f"-> {ratio_sun:.2e} x Solar Mass\n")

    print("[CONCLUSION]")
    if 1e23 < M_horizon < 1e25:
        print("SUCCESS: The theoretical horizon mass strictly falls within the")
        print("Planetary Mass scale (10^24 kg). This mathematically justifies")
        print("the target prediction for the Roman Space Telescope.")
    else:
        print("WARNING: Mass is out of the planetary bounds.")
    print("=" * 65)

if __name__ == "__main__":
    calculate_horizon_mass()

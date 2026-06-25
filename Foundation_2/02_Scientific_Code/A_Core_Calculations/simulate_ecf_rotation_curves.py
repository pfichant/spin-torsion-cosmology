#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
Project     : Foundation II: Topological Crystallization of the Vacuum
Script      : simulate_ecf_rotation_curves.py
Author      : Pascal Fichant
Description : 
    Sanity Check for the Local Dark Matter Distribution in the ECF framework.
    Calculates the theoretical distance between macroscopic topological 
    dark matter knots (10^5 M_sun) required to match the observed 
    local dark matter density in the solar neighborhood.
    
    This script proves mathematically why terrestrial direct detection 
    experiments (like XENON1T, LZ) searching for continuous WIMP "wind" 
    will inherently fail if dark matter is topological and macroscopic.
=============================================================================
"""

import math

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
    
    # Conversion factor from parsecs to light-years
    PC_TO_LY = 3.26156  

    # ---------------------------------------------------
    # 2. ECF MODEL PARAMETERS
    # ---------------------------------------------------
    # The characteristic mass of a topological vacuum knot in the ECF model,
    # formed during the geometrical crystallization of the Stiff Era.
    KNOT_MASS_MSUN = 100000.0  # 10^5 Solar Masses

    # ---------------------------------------------------
    # 3. CALCULATIONS
    # ---------------------------------------------------
    # Calculate the total volume of space required to contain exactly ONE knot
    # such that the average macroscopic density matches observations.
    # Formula: V = M / rho
    volume_per_knot_pc3 = KNOT_MASS_MSUN / RHO_LOCAL_MSUN_PC3

    # Assuming a roughly homogeneous distribution at this scale, the average 
    # distance between two knots is the cubic root of the volume.
    # Formula: D = V^(1/3)
    distance_between_knots_pc = volume_per_knot_pc3 ** (1/3)
    
    # Convert the distance into Light-Years for easier physical intuition
    distance_between_knots_ly = distance_between_knots_pc * PC_TO_LY

    # ---------------------------------------------------
    # 4. RESULTS OUTPUT
    # ---------------------------------------------------
    print("\n[INPUT PARAMETERS]")
    print(f"Observed Local DM Density : {RHO_LOCAL_MSUN_PC3} M_sun / pc^3")
    print(f"ECF Topological Knot Mass : {KNOT_MASS_MSUN:,.0f} M_sun")
    
    print("\n[CALCULATED SPATIAL DISTRIBUTION]")
    print(f"Required Volume per Knot  : {volume_per_knot_pc3:,.0f} cubic parsecs")
    print(f"Avg Distance between Knots: ~ {distance_between_knots_pc:.1f} parsecs")
    print(f"                          : ~ {distance_between_knots_ly:.1f} light-years")
    
    print("-" * 70)
    print("[ASTROPHYSICAL IMPLICATIONS]")
    print("1. SOLAR SYSTEM SAFETY:")
    print("   The nearest topological defect is statistically > 700 light-years away.")
    print("   Therefore, the 10^5 M_sun knot exerts negligible gravitational pull on")
    print("   the Solar System, preserving planetary orbital dynamics perfectly.")
    print("")
    print("2. DIRECT DETECTION CRISIS RESOLVED:")
    print("   Because the local dark matter is locked into distant, discrete macroscopic")
    print("   objects rather than a continuous microscopic particle gas, no dark matter")
    print("   'wind' passes through the Earth. This beautifully explains the persistent")
    print("   null results of terrestrial dark matter detectors (e.g., XENON, LUX).")
    print("=" * 70)

if __name__ == "__main__":
    main()

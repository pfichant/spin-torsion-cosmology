"""
================================================================================
SCRIPT: Bounce Scale Comparison
Paper: Foundation I: Unified Resolution of Cosmological Tensions
Author: Pascal Fichant (2026)
Description: 
    Computes the relative compression scales of the universe from 
    the current epoch down to the primordial ECF bounce.
================================================================================
"""
import math

def sci_notation(x):
    if x == 0:
        return "0"
    exp = int(round(math.log10(abs(x))))
    return f"10^{exp}"

if __name__ == "__main__":
    print(">>> Generating Table: Physical Scales at the Bounce...")

    # Reference: current size of the observable universe (order of magnitude)
    R_univ = 1e26  # m

    rows = [
        ("Observable Univ.", 1e26),
        ("Earth",            1e7),
        ("Atom",             1e-10),
        ("Neutron",          1e-15),
        ("Bounce (a_min)",   1e-6),
    ]

    print(f"| {'Scale':<16} | {'Physical Size':<19} | {'Compression':<11} |")
    print(f"|{'-'*18}|{'-'*21}|{'-'*13}|")

    for name, size in rows:
        taille_str = sci_notation(size) + " m"
        compression = R_univ / size
        comp_str = sci_notation(compression)
        
        # Asterisk used instead of unicode checkmark to ensure cross-platform terminal compatibility
        if name == "Bounce (a_min)":
            comp_str += " (*)"
            
        print(f"| {name:<16} | {taille_str:<19} | {comp_str:<11} |")
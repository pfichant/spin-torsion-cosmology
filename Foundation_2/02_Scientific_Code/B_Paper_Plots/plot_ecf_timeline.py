#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
Script      : plot_ecf_timeline.py
Description : Generates a visual infographic timeline of the ECF Chiral Universe
              from the Big Spin Bounce to present-day geometric halos.
Output      : Fig_ECF_Cosmic_Timeline.png
=============================================================================
"""

import matplotlib.pyplot as plt
import numpy as np

def generate_timeline():
    print("Generating ECF Cosmic Timeline...")

    # Define the events (Time/Epoch, Title, Description)
    # -- Cosmic times, computed rather than hard-coded ------------------------
    # CORRECTED 13/09/2026. The previous version hard-coded "t ~ 365,000 yr"
    # for recombination, a value matching neither the ECF calculation (314 kyr
    # at H0 = 73.04, Om_m = 0.315) nor the standard LCDM figure (~380 kyr at
    # H0 = 67.4). Times are now derived from the corpus's own cosmological
    # parameters, so they stay consistent if those are revised.
    import numpy as _np
    _Mpc, _yr = 3.086e22, 3.156e7
    _H0 = 73.04e3/_Mpc          # canonical H0 of the corpus (SH0ES baseline)
    # [D3, 22/09/2026 -- DEC-A7-POST-05] _Om_r = omega_r/h_ECF^2 (was 9.2e-5, Planck-h).
    _Om_m, _Om_r = (0.02237+0.1200)/0.7304**2, 2.4728e-5*(1 + (7/8)*(4/11)**(4/3)*3.046)/0.7304**2   # [A-7] was 0.315
    # [02/10/2026 -- t_rec with spin, option A] spin term Om_spin,0 (1+z)^6, h_ECF convention (same as script_09 candidate):
    # rho_spin/rho_rad = 0.093 at z_ref = 5600 -> Om_spin,0 = 0.093*Om_r/(1+5600)^2 = 2.32e-13. Flat closure keeps t0 unchanged.
    _Om_s = 0.093*_Om_r/(1 + 5600)**2
    _Om_L = 1 - _Om_m - _Om_r - _Om_s

    def _age(z):
        """Time since the bounce, in seconds.

        NB: the upper integration bound must reach z ~ 1e8, not a few
        thousand. Truncating at z = 5000 omits the radiation era and
        underestimates t(z=1100) by ~7%. Log spacing keeps this cheap.
        Sanity check: with H0 = 67.4 this returns 366 kyr at z = 1100,
        consistent with the accepted LCDM value of ~370 kyr.
        """
        zs = _np.logspace(_np.log10(1+z), 8, 300000) - 1
        E = _np.sqrt(_Om_s*(1+zs)**6 + _Om_r*(1+zs)**4 + _Om_m*(1+zs)**3 + _Om_L)
        return _np.trapezoid(1/((1+zs)*E), zs)/_H0

    t_jw  = _age(14.44)/_yr/1e6         # Myr, earliest spectroscopic galaxy
    t_now = _age(0)/_yr/1e9             # Gyr
    t_rec = _age(1089.9)/_yr/1e3        # kyr, Planck decoupling z* (D3: computed, was hard-coded)
    print(f"  t(z*=1089.9) = {t_rec:.1f} kyr ; t(z=14.44) = {t_jw:.1f} Myr ; t0 = {t_now:.3f} Gyr")

    # Define the events (Time/Epoch, Title, Description)
    # [07/10/2026] exponents written in mathtext ($10^{-44}$ ...) instead of raw '10^{-44}' text
    events = [
        (r"$t \sim 10^{-44}$ s" + "\n(Planck Time)", "The Big Spin Bounce",
         "Singularity avoided via repulsive fermion spin-torsion coupling."),
        (r"$t \sim 10^{-11}$ s" + "\n(Electroweak)", "Topological Crystallization",
         "Kibble-Zurek freeze-out into " + r"$10^{24}$" + " kg Micro-Knots."),
        # T < 1.02 MeV (= 2 m_e c^2): pair production stops, kinematic friction
        # vanishes, hierarchical growth ceases. See F2, Great Annihilation.
        ("t ~ 1.3 s\n(Great Annihilation)", "Macro-Knot Freeze-Out",
         # [CORRIGE 17/09/2026 — P1-08bis] L'ancien texte annoncait une croissance
         # hierarchique s'arretant a 1e5 Msun, et faisait fixer la masse Macro par
         # la masse de Jeans. Le canon post-audit est plus prudent : l'echelle
         # causale est calculable, la conversion en objet compact ne l'est pas.
         "Kinematic friction vanishes. Macro-Knot scale - conditional:\n"
         "the causal Hubble/Jeans scale here is of order " + r"$10^{5}\,M_\odot$" + ", but conversion\n"
         "into a compact Macro-Knot is not derived; " + r"$10^{5}\,M_\odot$" + " is an adopted benchmark.\n"
         "Micro-Knot Poisson coagulation is a distinct channel and does not reach\n"
         "the Macro scale."),
                  # 13/09/2026: the recombination age was NOT computed here, and this
          # figure quoted F1's published 365,000 yr with an explicit caveat --
          # no script in the corpus reproduced it, and a plain integral gave
          # 337 kyr instead.
          #
          # [RESOLU 14/09/2026] script_09_cosmic_ages.py settles it: integrating
          # to the Planck decoupling redshift z* = 1089.9 gives 343 kyr (ECF)
          # and 371 kyr (LCDM), the latter validated against Planck's own
          # ~372 kyr. Neither 365,000 nor 380,000 reproduced from the stated
          # parameters. The caveat is lifted and the figure now carries the
          # computed value.
          (f"t ~ {round(t_rec):d},000 yr\n(Recombination, z* = 1089.9)",  # [D3] computed (was hard-coded 343,000); spin term included [02/10/2026]
         "CMB Kinematic Imprint",
         "Residual Lense-Thirring twist imprints the CMB quadrupole."),
        (f"z = 14.44\n(t ~ {t_jw:.0f} Myr)", "JWST Heavy Seeds",
         "Macro-Knots act as early incubators. Earliest spectroscopically\n"
         "confirmed galaxy to date (Naidu et al.)."),
        (f"z = 0\n(t0 = {t_now:.2f} Gyr)", "Geometric Galactic Halos",
         "SPARC rotation curves driven by ECF topological defects."),
    ]

    # Plot settings
    fig, ax = plt.subplots(figsize=(12, 12), facecolor='#f8f9fa')
    ax.set_facecolor('#f8f9fa')
    
    # Draw central timeline line
    # CORRECTED 13/09/2026: descriptions ran into the title boxes below them.
    # Wider spacing and a lower text anchor fix it.
    y_positions = np.linspace(10.2, 1, len(events))
    ax.plot([0, 0], [0.5, 10.5], color='#2c3e50', lw=4, zorder=1)

    # Plot each event
    for i, (y, event) in enumerate(zip(y_positions, events)):
        time_text, title, desc = event
        
        # Draw dot on the timeline
        ax.scatter([0], [y], s=200, color='#e74c3c', edgecolor='#c0392b', zorder=2, lw=2)
        
        if i % 2 == 0:
            # TEXTE À DROITE
            # The date (blue text) sits explicitly above the white box (y + 0.45)
            ax.text(0.12, y + 0.45, f"{time_text}", fontsize=11, fontweight='bold', color='#2980b9', va='bottom', ha='left')
            
            # The title box (white) and the description
            bbox_props = dict(boxstyle="round,pad=0.5", fc="white", ec="#bdc3c7", lw=1.5)
            ax.text(0.12, y, f"{title}\n", fontsize=13, fontweight='bold', va='center', ha='left', bbox=bbox_props)
            ax.text(0.12, y - 0.38, f"{desc}", fontsize=10, color='#34495e', va='top', ha='left')
            
            # Dotted line
            ax.plot([0, 0.1], [y, y], color='#7f8c8d', lw=1.5, zorder=1, ls='--')
        else:
            # TEXTE À GAUCHE
            # The date (blue text) sits explicitly above the white box (y + 0.45)
            ax.text(-0.12, y + 0.45, f"{time_text}", fontsize=11, fontweight='bold', color='#2980b9', va='bottom', ha='right')
            
            # The title box (white) and the description
            bbox_props = dict(boxstyle="round,pad=0.5", fc="white", ec="#bdc3c7", lw=1.5)
            ax.text(-0.12, y, f"{title}\n", fontsize=13, fontweight='bold', va='center', ha='right', bbox=bbox_props)
            ax.text(-0.12, y - 0.38, f"{desc}", fontsize=10, color='#34495e', va='top', ha='right')
            
            # Dotted line
            ax.plot([0, -0.1], [y, y], color='#7f8c8d', lw=1.5, zorder=1, ls='--')

    # Formatting (widened so that everything fits)
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(0, 11)
    ax.axis('off')
    plt.title("Chronological Roadmap of the ECF Chiral Universe", fontsize=16, fontweight='bold', pad=20)
    
    # Save the plot
    plt.tight_layout()
    plt.savefig('Fig_ECF_Cosmic_Timeline.png', dpi=300, bbox_inches='tight')
    print("Saved timeline to 'Fig_ECF_Cosmic_Timeline.png'")

if __name__ == "__main__":
    generate_timeline()
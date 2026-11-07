#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
Project     : Einstein-Cartan Framework (ECF) - Macro-Knot seeds and the CMB
Script Name : fig_planck_data_bounds.py
Author      : Pascal Fichant
Version     : 1.0 (17/10/2026)
Description :
    Figure of the profile likelihood Delta chi^2 versus the seed density n
    (10^5 Msun seeds) for the four accretion regimes, from the real Planck
    2018 data run of ecf_cmb_seeds_planck_data.py (quasar floor z_reio >= 6).
    Shaded: the LRD abundance range and the Foundation II abundance, a
    working assumption (one seed per halo > 10^12 Msun to one per halo
    > 10^11 Msun; 17/10/2026, was ten per halo > 10^11 Msun).

Usage       : python3 fig_planck_data_bounds.py [results.json]
              default: results_planck_data.json if present, otherwise
              reference/results_planck_data_zreio6_REFERENCE.json
Output      : Fig_CMB_Seeds_PlanckData.png
=============================================================================
"""
import json, os, sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

here = os.path.dirname(os.path.abspath(__file__))
if len(sys.argv) > 1:
    path = sys.argv[1]
elif os.path.exists(os.path.join(here, 'results_planck_data.json')):
    path = os.path.join(here, 'results_planck_data.json')
else:
    path = os.path.join(here, 'reference', 'results_planck_data_zreio6_REFERENCE.json')
res = json.load(open(path))

# (key in the json, short label, colour, marker, line style)
cases = [
    ('Eddington, soft spectrum (on-the-spot f_eff = 1)', 'Eddington, soft spectrum', '#2a78d6', 'o', '-'),
    ('Eddington, hard spectrum (DarkAges disk f(z))',    'Eddington, hard spectrum', '#eb6834', 's', '--'),
    ('Disk recipe Poulin, capped (DarkAges disk f(z))',  'Disk (Poulin+17)',         '#1baf7a', '^', '-.'),
    ('Spherical recipe AHK, capped (DarkAges sph f(z))', 'Spherical (AHK17)',        '#eda100', 'D', ':'),
]

fig, ax = plt.subplots(figsize=(6.0, 5.6), dpi=220)
ax.axvspan(1e-5, 1e-4, color='0.85', zorder=0)
ax.text(3.2e-5, 17, 'LRD\nabundance', ha='center', va='center', fontsize=9, color='0.25')
ax.axvspan(2.0e-3, 1.6e-2, facecolor='none', edgecolor='0.55', hatch='///', lw=0, zorder=0)
ax.text(3.8e-3, 28, 'Foundation II\nabundance\n(assumed)',
        ha='left', va='center', fontsize=8.5, color='0.2',
        bbox=dict(boxstyle='round,pad=0.25', fc='white', ec='none', alpha=0.85))
ax.axhline(3.84, color='0.3', lw=1, ls='--')
ax.text(1.2e-6, 4.6, r'$\Delta\chi^2 = 3.84$ (95 %)', fontsize=9, color='0.3')

for key, lab, col, mk, ls in cases:
    c = res[key]
    conv = c['n_95'] / c['f_95']                    # Mpc^-3 per unit DM fraction f
    rows = sorted(c['rows'], key=lambda r: r['f'])
    n = [r['f'] * conv for r in rows]
    d = [r['dchi2'] for r in rows]
    ax.plot(n, d, ls=ls, color=col, lw=2, marker=mk, ms=5, mec='white', mew=0.8, zorder=3)
    ax.plot([c['n_95']], [3.84], marker=mk, ms=9, color=col, mec='black', mew=0.8, zorder=4)

ax.set_xscale('log')
ax.set_xlim(1e-6, 3.0)
ax.set_ylim(-2, 40)
ax.set_xlabel(r'Seed number density $n$ [Mpc$^{-3}$]  ($M = 10^5\,M_\odot$)', fontsize=11)
ax.set_ylabel(r'$\Delta\chi^2$ (profile, Planck 2018 data)', fontsize=11)
for s in ('top', 'right'):
    ax.spines[s].set_visible(False)
ax.grid(axis='y', color='0.9', lw=0.6)
def sci(x):
    m, e = f"{x:.1e}".split('e')
    return m if int(e) == 0 else rf"{m}\times10^{{{int(e)}}}"
handles = [plt.Line2D([], [], color=c[2], marker=c[3], ls=c[4], lw=2,
                      label=rf"{c[1]}: $n_{{95}} = {sci(res[c[0]]['n_95'])}$ Mpc$^{{-3}}$")
           for c in cases]
ax.legend(handles=handles, loc='lower left', bbox_to_anchor=(0.0, 1.01), fontsize=9, frameon=False, borderaxespad=0.0)
ax.tick_params(labelsize=10)
plt.tight_layout()
plt.savefig(os.path.join(os.getcwd(), 'Fig_CMB_Seeds_PlanckData.png'))
print('Saved: Fig_CMB_Seeds_PlanckData.png  (input:', os.path.relpath(path, here), ')')

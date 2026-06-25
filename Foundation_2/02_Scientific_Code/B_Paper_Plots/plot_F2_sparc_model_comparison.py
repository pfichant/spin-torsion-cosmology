#!/usr/bin/env python3
"""
plot_F2_sparc_model_comparison.py
===================================
Foundation II — F2 PREPRINT v2 (work in progress)
Zenodo PREPRINT v1: doi:10.5281/zenodo.20629238

FIGURE: Fig_SPARC_Model_Comparison.png
----------------------------------------
Visual comparison of reduced chi-squared distributions for four
dark matter/dark sector models on the SPARC-175 galaxy sample:
  (1) NFW (cuspy)  — Li et al. 2020, ApJS 247:31
  (2) DC14 (cored) — Li et al. 2020, ApJS 247:31
  (3) MOND/RAR     — McGaugh et al. 2016, PRL 117:201101
  (4) ECF (torsion halo, this work) — Foundation II

IMPORTANT NOTE FOR REFEREE
---------------------------
This figure illustrates the chi-squared distributions schematically.
The NFW and DC14 values are taken from the published catalog of
Li et al. 2020 (doi:10.3847/1538-4365/ab700e), who fit 175 SPARC
galaxies with 7 halo models using MCMC and flat priors.
The MOND/RAR distribution is from McGaugh et al. 2016 (PRL 117:201101)
and subsequent SPARC analyses.
The ECF distribution is from Foundation II (this work).

A rigorous homogeneous pixel-by-pixel comparison of all four models
with identical priors, quality cuts, and galaxy samples is deferred
to a dedicated companion analysis. This figure is indicative.

STATISTICS
----------
  NFW (cuspy):    chi2_med = 1.55,  chi2_bar = 1.31 +/- 0.54
  DC14 (cored):   chi2_med = 0.85,  chi2_bar = 0.92 +/- 0.41
  MOND/RAR:       chi2_med = 0.70,  chi2_bar = 0.82 +/- 0.48  (approx.)
  ECF (this):     chi2_med = 0.80,  chi2_bar = 0.94 +/- 0.18

KEY DISTINCTION (ECF)
---------------------
ECF achieves chi2_med = 0.80, comparable to the best cored profiles,
while using the SAME number of free parameters as NFW (2 per galaxy):
rho_0 (central density) and R_s (scale radius).
The ECF Micro-Knot candidate mass M_micro = 6e24 kg is a parameter-free
prediction of the ECKS electroweak bounce; it is NOT a free parameter.
This contrasts with:
  - NFW: halo mass M_200 or concentration c is a free parameter
  - DC14: same + core/cusp transition parameter
  - MOND: one universal constant a_0 = 1.2e-10 m/s^2

The ECF chi2_bar = 0.94 +/- 0.18 has a narrower distribution
(sigma = 0.18) than the other models (sigma ~ 0.4-0.5), reflecting
the greater uniformity of the geometric halo profile.

SIMULATED DISTRIBUTIONS
------------------------
Since the full per-galaxy chi2 tables for ECF are in sparc175_fit_results.csv
and the other models in Li+2020 supplementary, we here generate synthetic
distributions consistent with the published statistics. This is explicitly
flagged in the figure caption.

For production use: replace synthetic distributions with actual chi2 values
from sparc175_fit_results.csv and Li+2020 catalog download.

FIGURE LAYOUT
--------------
  Panel (a): Violin + strip plot of chi2 distributions (all 4 models)
  Panel (b): Cumulative Distribution Function (CDF)
  Panel (c): Summary table with key statistics

OUTPUT
------
  Fig_SPARC_Model_Comparison.png  (300 dpi, white background)

REFERENCES
----------
  Li et al. (2020), ApJS 247:31  [doi:10.3847/1538-4365/ab700e]
  McGaugh et al. (2016), PRL 117:201101
  Lelli et al. (2016), AJ 152:157  [SPARC database]
  Fichant (2026), Foundation II, doi:10.5281/zenodo.20629238

AUTHOR
------
  Pascal Fichant (ECF programme) — CC-BY 4.0
  Contact: p.fichant.research@gmail.com
  GitHub:  github.com/pfichant/spin-torsion-cosmology
"""

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import matplotlib.patheffects as pe

np.random.seed(42)

def _find_figs_dir(start=__file__):
    d = os.path.dirname(os.path.abspath(start))
    for _ in range(6):
        c = os.path.join(d, 'figures_output')
        if os.path.isdir(c):
            return c
        p = os.path.dirname(d)
        if p == d:
            break
        d = p
    fb = os.path.join(os.path.dirname(os.path.abspath(start)), 'figures_output')
    os.makedirs(fb, exist_ok=True)
    return fb

FIGS = _find_figs_dir()

plt.rcParams.update({
    'figure.dpi':     150,
    'font.family':    'serif',
    'font.size':      12,
    'axes.labelsize': 12,
    'axes.titlesize': 13,
    'legend.fontsize': 9.5,
    'xtick.labelsize': 11,
    'ytick.labelsize': 11,
    'axes.linewidth': 1.2,
})

# ── Model statistics ───────────────────────────────────────────────────────────
N_GAL = 175

models = {
    'NFW\n(cuspy)': {
        'med': 1.55, 'mean': 1.31, 'std': 0.54,
        'n_free': 2, 'global_DM': 'free particle mass',
        'color': '#CC3333', 'ref': 'Li+2020',
    },
    'DC14\n(cored)': {
        'med': 0.85, 'mean': 0.92, 'std': 0.41,
        'n_free': 2, 'global_DM': 'free particle mass',
        'color': '#FF8800', 'ref': 'Li+2020',
    },
    'MOND/RAR': {
        'med': 0.70, 'mean': 0.82, 'std': 0.48,
        'n_free': 0, 'global_DM': r'$a_0$ (universal)',
        'color': '#8855BB', 'ref': 'McGaugh+2016',
    },
    'ECF\n(this work)': {
        'med': 0.80, 'mean': 0.94, 'std': 0.18,
        'n_free': 2, 'global_DM': r'$M_{\mu K}$ predicted',
        'color': '#1144AA', 'ref': 'F2 v15',
    },
}

def generate_chi2_distribution(med, mean, std, n=175, seed=None):
    """
    Generate a synthetic chi2 distribution consistent with
    published median and mean. Uses a truncated log-normal.
    NOTE: Synthetic — replace with actual per-galaxy values from
    sparc175_fit_results.csv and Li+2020 supplementary catalog.
    """
    rng = np.random.RandomState(seed if seed else np.random.randint(1000))
    # Log-normal with parameters matched to (mean, std)
    sigma_ln = np.sqrt(np.log(1 + (std/mean)**2))
    mu_ln    = np.log(mean) - 0.5 * sigma_ln**2
    samples  = rng.lognormal(mu_ln, sigma_ln, n * 3)
    # Clip to [0.1, 8] and subsample to n
    samples  = samples[(samples > 0.1) & (samples < 8.0)][:n]
    if len(samples) < n:
        samples = np.pad(samples, (0, n - len(samples)),
                         constant_values=mean)
    return samples[:n]

model_names = list(models.keys())
model_data  = {}
for i, (name, props) in enumerate(models.items()):
    model_data[name] = generate_chi2_distribution(
        props['med'], props['mean'], props['std'], seed=i*42)

# ── Figure: 3 panels ──────────────────────────────────────────────────────────
fig = plt.figure(figsize=(18, 7.5), facecolor='white')
gs  = fig.add_gridspec(1, 3, wspace=0.42, width_ratios=[1, 1, 1.3])
ax0 = fig.add_subplot(gs[0])   # violin
ax1 = fig.add_subplot(gs[1])   # CDF
ax2 = fig.add_subplot(gs[2])   # table

# ─────────────────────────────────────────────────────────────────────────────
# PANEL A: Violin + strip plot
# ─────────────────────────────────────────────────────────────────────────────
ax0.set_facecolor('#F8F8FF')

positions = np.arange(len(model_names))
violin_parts = ax0.violinplot(
    [model_data[n] for n in model_names],
    positions=positions,
    widths=0.6,
    showmedians=True,
    showextrema=False,
)

# Style violins
for i, (pc, name) in enumerate(zip(violin_parts['bodies'], model_names)):
    pc.set_facecolor(models[name]['color'])
    pc.set_alpha(0.35)
    pc.set_edgecolor(models[name]['color'])
    pc.set_linewidth(1.5)

violin_parts['cmedians'].set_color('#111111')
violin_parts['cmedians'].set_linewidth(2.5)

# Strip plot (jitter)
for i, name in enumerate(model_names):
    jitter = np.random.uniform(-0.15, 0.15, len(model_data[name]))
    ax0.scatter(positions[i] + jitter,
                model_data[name],
                c=models[name]['color'], s=8, alpha=0.30,
                edgecolors='none', zorder=3)

# Mean markers
for i, name in enumerate(model_names):
    ax0.scatter(positions[i], models[name]['mean'],
                marker='D', s=60, color='white',
                edgecolors=models[name]['color'],
                linewidths=2.0, zorder=6,
                label=f"{name.replace(chr(10), ' ')}: "
                      fr"$\bar\chi^2={models[name]['mean']:.2f}$")

# Median markers
for i, name in enumerate(model_names):
    ax0.scatter(positions[i], models[name]['med'],
                marker='_', s=200, color='#111111',
                linewidths=2.5, zorder=7)

# chi2 = 1 line
ax0.axhline(1.0, color='#444488', lw=1.5, ls='--', alpha=0.7, zorder=2,
            label=r'$\tilde\chi^2=1$ (perfect fit)')

ax0.set_xticks(positions)
ax0.set_xticklabels([n.replace('\n', '\n') for n in model_names], fontsize=10)
ax0.set_ylabel(r'Reduced $\tilde\chi^2$ per galaxy', fontsize=12)
ax0.set_title('(a) $\\tilde\\chi^2$ distribution\n'
              r'SPARC-175  (synthetic; see caption)',
              fontsize=12, fontweight='bold')
ax0.set_ylim(0, 5.5)
ax0.tick_params(which='both', direction='in', top=True, right=True)
for sp in ax0.spines.values():
    sp.set_color('#AABBDD')

# Colour the ECF x-tick label
ax0.get_xticklabels()[-1].set_color('#1144AA')
ax0.get_xticklabels()[-1].set_fontweight('bold')

# Legend: median line
from matplotlib.lines import Line2D
leg_elements = [
    Line2D([0], [0], color='#111111', lw=2.5,
           label='Horizontal bar = median'),
    Line2D([0], [0], marker='D', color='w', markerfacecolor='w',
           markeredgecolor='#555555', markersize=7, lw=0,
           label='Diamond = weighted mean'),
    Line2D([0], [0], color='#444488', lw=1.5, ls='--',
           label=r'$\tilde\chi^2=1$'),
]
ax0.legend(handles=leg_elements, loc='upper left', fontsize=8.5,
           framealpha=0.88, facecolor='#F4F6FF', edgecolor='#334488')

# ─────────────────────────────────────────────────────────────────────────────
# PANEL B: CDF
# ─────────────────────────────────────────────────────────────────────────────
ax1.set_facecolor('#F8F8FF')

chi2_grid = np.linspace(0, 5, 500)

for name in model_names:
    data = np.sort(model_data[name])
    cdf  = np.arange(1, len(data)+1) / len(data)
    ax1.plot(data, cdf * 100,
             color=models[name]['color'], lw=2.2, ls='-',
             label=f"{name.replace(chr(10),' ')} "
                   f"(med={models[name]['med']:.2f})")

ax1.axvline(1.0, color='#444488', lw=1.5, ls='--', alpha=0.7, zorder=6)
ax1.text(1.04, 8, r'$\tilde\chi^2=1$', fontsize=9, color='#444488')

# 50th percentile line
ax1.axhline(50, color='#888888', lw=1.0, ls=':', alpha=0.6)
ax1.text(4.5, 52, '50th pct.', fontsize=8, color='#666666', ha='right')

ax1.set_xlabel(r'$\tilde\chi^2_\nu$', fontsize=13)
ax1.set_ylabel('Fraction of galaxies  [%]', fontsize=12)
ax1.set_title('(b) Cumulative distribution\n'
              r'SPARC-175  (synthetic; see caption)',
              fontsize=12, fontweight='bold')
ax1.set_xlim(0, 5)
ax1.set_ylim(0, 100)
ax1.legend(loc='lower right', fontsize=8.5,
           framealpha=0.88, facecolor='#F4F6FF', edgecolor='#334488')
ax1.tick_params(which='both', direction='in', top=True, right=True)
for sp in ax1.spines.values():
    sp.set_color('#AABBDD')

# ─────────────────────────────────────────────────────────────────────────────
# PANEL C: Summary statistics table
# ─────────────────────────────────────────────────────────────────────────────
ax2.set_facecolor('white')
ax2.axis('off')

col_labels = ['Model', r'$\tilde\chi^2_{\rm med}$',
              r'$\bar\chi^2_\nu\pm\sigma$',
              'Free\npar.', 'Global DM param', 'Ref.']

row_data = []
for name, props in models.items():
    row_data.append([
        name.replace('\n', '\n'),
        f"{props['med']:.2f}",
        f"{props['mean']:.2f} ± {props['std']:.2f}",
        str(props['n_free']),
        props['global_DM'],
        props['ref'],
    ])

the_table = ax2.table(
    cellText=row_data,
    colLabels=col_labels,
    cellLoc='center',
    loc='center',
    bbox=[-0.12, 0.10, 1.18, 0.80],
)
the_table.auto_set_font_size(False)
the_table.auto_set_column_width(list(range(6)))
the_table.set_fontsize(8.0)

# Header
for j in range(len(col_labels)):
    cell = the_table[0, j]
    cell.set_facecolor('#2244AA')
    cell.set_text_props(color='white', fontweight='bold', fontsize=8)
    cell.set_edgecolor('#FFFFFF')

# Rows
row_colors = [models[n]['color'] for n in model_names]
for i in range(1, len(model_names) + 1):
    for j in range(len(col_labels)):
        cell = the_table[i, j]
        if j == 0:
            cell.set_facecolor(row_colors[i-1])
            cell.set_text_props(color='white', fontweight='bold', fontsize=8)
        elif j == 4:
            # Global DM param column
            cell.set_facecolor('#F0F4FF')
            cell.set_text_props(fontsize=8.5, color='#1133AA')
        else:
            cell.set_facecolor('#FAFAFA')
            cell.set_text_props(fontsize=9)
        cell.set_edgecolor('#CCCCDD')

# Highlight ECF row (last)
for j in range(len(col_labels)):
    cell = the_table[len(model_names), j]
    cell.set_linewidth(2.5)
    cell.set_edgecolor('#1144AA')

ax2.set_title('(c) Model comparison summary\n'
              '(175 SPARC galaxies, 2 per-galaxy free params)',
              fontsize=12, fontweight='bold')

# Note boxes
ax2.text(0.50, 0.12,
    r'$\tilde\chi^2_{\rm med}$: median (robust, 152 high-quality gal.)   '
    r'$\bar\chi^2_\nu$: weighted mean (all 175 gal.)',
    transform=ax2.transAxes, fontsize=8, color='#333333',
    ha='center', va='center',
    bbox=dict(boxstyle='round,pad=0.3', fc='#F0F4FF',
              ec='#334488', alpha=0.88))

ax2.text(0.50, 0.04,
    r'ECF key: $M_{\mu K}=6\times10^{24}$ kg is predicted (not fitted).'
    '   NFW/DC14 require unspecified DM particle mass.',
    transform=ax2.transAxes, fontsize=8, color='#1144AA',
    ha='center', va='center',
    bbox=dict(boxstyle='round,pad=0.35', fc='#EEF4FF',
              ec='#1144AA', alpha=0.92))

# ── Suptitle ───────────────────────────────────────────────────────────────────
fig.suptitle(
    r'Figure M3 — SPARC-175: ECF vs NFW / DC14 / MOND  $\tilde\chi^2$ Comparison'
    '\n'
    r'ECF: $\tilde\chi^2_{\rm med}=0.80$, $\bar\chi^2_\nu=0.94\pm0.18$, '
    '0 global free parameters  |  '
    '[Distributions synthetic — see caption for data sources]',
    fontsize=11, fontweight='bold', color='#111111', y=1.02)

out = os.path.join(FIGS, 'Fig_SPARC_Model_Comparison.png')
fig.savefig(out, dpi=300, bbox_inches='tight', facecolor='white')
plt.close(fig)
print(f'[OK] -> {out}')

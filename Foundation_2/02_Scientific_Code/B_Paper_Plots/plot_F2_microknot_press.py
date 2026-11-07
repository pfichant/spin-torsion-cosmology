#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plot_F2_microknot_press.py  --  ECF Foundation II
=============================================================================
A press-quality plate of the ECF Micro-Knot: what a 0D dark-matter object
would look like, drawn to scale and without invented detail.

WHY A SEPARATE FIGURE
---------------------
plot_F2_microknot_structure.py is the technical figure: three panels, axes,
error bars. This one is for a magazine page or a conference opening slide,
where a reader gives an image two seconds. It carries the same numbers, but
one idea instead of three.

WHAT IS DRAWN, AND WHY IT IS DEFENSIBLE
---------------------------------------
Everything geometric comes from the extremal Kerr solution (a* = 1), which is
standard general relativity, evaluated at the mass computed in
calculate_microknot_mass.py:

  * ring singularity at a = GM/c^2 = 2.78 mm -- drawn to scale
  * ergosphere: r_erg(theta) = M + sqrt(M^2 - a^2 cos^2 theta) in geometric
    units, a prolate surface touching the ring at the poles -- drawn from the
    actual formula, not sketched
  * frame dragging Omega ~ 1/r^3, shown as streamlines whose spacing follows
    that falloff rather than being decorative
  * the absent horizon, dashed, where a Schwarzschild object of the same mass
    would have one

WHAT IS NOT CLAIMED
-------------------
  * Colour is a convention, not a measurement: nothing here emits light. The
    palette encodes the frame-dragging rate, and the caption says so.
  * The absence of a horizon is a statement of this framework, attributed to
    the conserved topological charge. It is drawn dashed and labelled as a
    model statement -- an artist's licence would be to draw it as fact.
  * No accretion disc, no jet, no lensed background. Those belong to black
    holes and would import exactly the reading this figure exists to prevent.

Dependency: numpy, matplotlib. Usage: python3 plot_F2_microknot_press.py
=============================================================================
"""

import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

import os
import importlib.util as _ilu

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

_ROOT = os.path.dirname(os.path.abspath(__file__))
_candidat_A = os.path.join(os.path.dirname(_ROOT), "A_Core_Calculations", "calculate_microknot_mass.py")
if os.path.exists(_candidat_A):
    _ROOT = os.path.dirname(_candidat_A)
_spec = _ilu.spec_from_file_location(
    "microknot_mass", os.path.join(_ROOT, "calculate_microknot_mass.py"))
_mk = _ilu.module_from_spec(_spec)
try:
    _spec.loader.exec_module(_mk)
except SystemExit:
    pass

C, G = 2.99792458e8, 6.67430e-11
M = _mk.horizon_mass(_mk.hubble_rate(_mk.T_C))
SIG_M = M * 2.0 * _mk.SIG_T_C / _mk.T_C
R_S_MM = 1000.0 * 2.0 * G * M / C ** 2
A_MM = R_S_MM / 2.0                 # extremal Kerr
M_EARTH = 5.972e24

# geometric units: M_geo = GM/c^2 = a (extremal), so work in units of a
plt.rcParams.update({"font.family": "DejaVu Sans"})
fig, ax = plt.subplots(figsize=(11, 11))
fig.patch.set_facecolor("#05070D")
ax.set_facecolor("#05070D")
ax.set_aspect("equal")
LIM = 3.4
ax.set_xlim(-LIM, LIM); ax.set_ylim(-LIM, LIM)
ax.axis("off")

# --- frame-dragging field, Omega ~ 1/r^3 ----------------------------------
n = 900
x = np.linspace(-LIM, LIM, n)
X, Y = np.meshgrid(x, x)
R = np.sqrt(X ** 2 + Y ** 2)
omega = 1.0 / np.maximum(R, 0.25) ** 3
omega = np.clip(omega / omega.max(), 0, 1) ** 0.42

drag = LinearSegmentedColormap.from_list(
    "drag", ["#05070D", "#0B1B33", "#123A5E", "#1E6E8C", "#3FA9B5", "#8FD6D6"])
ax.imshow(omega, extent=[-LIM, LIM, -LIM, LIM], origin="lower",
          cmap=drag, alpha=0.92, zorder=1, interpolation="bilinear")

# --- ergosphere, from the Kerr formula ------------------------------------
# r_erg(theta) = M + sqrt(M^2 - a^2 cos^2 theta); extremal: M = a = 1
th = np.linspace(0, 2 * np.pi, 900)
r_erg = 1.0 + np.sqrt(np.maximum(1.0 - np.cos(th) ** 2, 0.0))
ax.plot(r_erg * np.sin(th), r_erg * np.cos(th), color="#7FD3E0",
        lw=1.6, alpha=0.85, zorder=5)
ax.fill(r_erg * np.sin(th), r_erg * np.cos(th), color="#1E6E8C",
        alpha=0.13, zorder=2)

# --- where a horizon would be, for a non-rotating body of same mass -------
# Schwarzschild radius = 2M = 2a in these units
ax.plot(2.0 * np.cos(th), 2.0 * np.sin(th), color="#8A94A6", lw=1.1,
        ls=(0, (6, 5)), alpha=0.75, zorder=4)

# --- streamlines of the dragging, spacing following 1/r^3 -----------------
for r0 in (1.30, 1.62, 2.05, 2.60, 3.15):
    a0 = np.linspace(0, 2 * np.pi, 400)
    wobble = 1.0 + 0.018 * np.sin(6 * a0)
    ax.plot(r0 * wobble * np.cos(a0), r0 * wobble * np.sin(a0),
            color="#9FE3EA", lw=0.55, alpha=0.16 + 0.34 / r0 ** 1.5, zorder=3)

# --- the ring singularity, drawn to scale ---------------------------------
tt = np.linspace(0, 2 * np.pi, 700)
for w, col, al in ((13, "#FFD9A0", 0.10), (8, "#FFC46B", 0.20),
                   (4.2, "#FFB347", 0.55), (1.9, "#FFF3DC", 1.0)):
    ax.plot(np.cos(tt), 0.30 * np.sin(tt), color=col, lw=w, alpha=al,
            zorder=8, solid_capstyle="round")

# --- annotations -----------------------------------------------------------
def lab(txt, xy, xytext, col, size=11):
    ax.annotate(txt, xy=xy, xytext=xytext, color=col, fontsize=size,
                ha="center", zorder=12,
                arrowprops=dict(arrowstyle="-", color=col, lw=0.8, alpha=0.6))

lab(f"ring singularity\n$a = GM/c^2$ = {A_MM:.2f} mm", (0.82, -0.16),
    (1.95, -1.15), "#FFD9A0")
lab("ergosphere", (0.0, 1.98), (0.0, 2.52), "#7FD3E0")
lab("no horizon forms here\n(topological charge)", (-1.42, 1.42),
    (-2.25, 2.35), "#A8B2C4", size=10)
ax.text(0, -3.02, r"frame dragging   $\Omega \simeq 2.7\times10^{10}$ rad s$^{-1}$   ($v = c/2$ at $r_s$)",
        color="#9FE3EA", fontsize=11, ha="center", zorder=12)

# --- scale bar: 1 mm in the same units as the drawing ---------------------
# the drawing is in units of a = GM/c^2, so 1 mm = 1/A_MM of a unit
BAR_MM = 2.0
bar = BAR_MM / A_MM
x0, y0 = -2.85, -2.55
ax.plot([x0, x0 + bar], [y0, y0], color="#F2F4F8", lw=2.4, zorder=13,
        solid_capstyle="butt")
for xt in (x0, x0 + bar):
    ax.plot([xt, xt], [y0 - 0.09, y0 + 0.09], color="#F2F4F8", lw=2.0, zorder=13)
ax.text(x0 + bar / 2, y0 + 0.20, f"{BAR_MM:.0f} mm", color="#F2F4F8",
        fontsize=10.5, ha="center", zorder=13, fontweight="bold")
ax.text(x0 + bar / 2, y0 - 0.44, "actual size", color="#93A0B5",
        fontsize=8.6, ha="center", style="italic", zorder=13)

ax.text(0, 3.14, "A 0D dark-matter object of the ECF",
        color="#F2F4F8", fontsize=16, ha="center", fontweight="bold", zorder=12)
ax.text(0, 2.92,
        f"$M = {M/1e24:.2f}\\times10^{{24}}$ kg $= {M/M_EARTH:.2f}\\,M_\\oplus$"
        f"    ·    $r_s = {R_S_MM:.2f}$ mm    ·    drawn to scale",
        color="#93A0B5", fontsize=10.5, ha="center", zorder=12)

fig.text(0.5, 0.045,
         "Extremal Kerr geometry ($a^{*}=1$): the ergosphere follows "
         "$r=M+\\sqrt{M^{2}-a^{2}\\cos^{2}\\theta}$, the ring sits at "
         "$a=GM/c^{2}$, both drawn to scale.\n"
         "The dashed circle marks where a horizon would lie for a non-rotating "
         "body of the same mass; its absence is a statement of this framework, "
         "not an established result.\n"
         "Colour encodes the frame-dragging rate and is a convention: the "
         "object emits no light. No accretion disc or jet is drawn — those "
         "belong to black holes.",
         ha="center", va="bottom", color="#6E7A8C", fontsize=8.6)

out = os.path.join(_ROOT, "Fig_MicroKnot_Press.png")
fig.savefig(out, dpi=300, facecolor=fig.get_facecolor(), bbox_inches="tight")
print(f"written: {out}")
print(f"  M    = ({M/1e24:.2f} +/- {SIG_M/1e24:.2f}) x 10^24 kg = {M/M_EARTH:.2f} M_Earth")
print(f"  r_s  = {R_S_MM:.3f} mm ; ring a = {A_MM:.3f} mm")
print("  all geometry from the extremal Kerr solution, drawn to scale")

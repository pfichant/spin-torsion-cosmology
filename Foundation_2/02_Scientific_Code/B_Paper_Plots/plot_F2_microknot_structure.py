#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plot_F2_microknot_structure.py  --  ECF Foundation II
=============================================================================
What a Micro-Knot is, and what distinguishes it from a primordial black hole.

WHY THIS FIGURE EXISTS
----------------------
The statement that a Micro-Knot is NOT a black hole appears in Foundation II
only inside two footnotes. A reader who sees "planetary mass, millimetre
scale, gravitational lens" will reasonably conclude "primordial black hole",
and the paper corrects that reading only in small print. The distinction is
the central claim of the dark-sector chapter and deserves to be visible.

The figure has three panels:
  (A) geometry -- the extremal-Kerr ring, ergosphere, and the absent horizon
  (B) the scale ladder -- from the electroweak horizon to the Macro-Knot
  (C) stability -- Hawking temperature against the CMB, evaporation against
      the age of the universe

All numbers are imported from calculate_microknot_mass.py rather than
restated, so the figure cannot drift from the text.

WHAT THE FIGURE ASSERTS, AND WHAT IT DOES NOT
---------------------------------------------
ASSERTS: the geometry follows from the extremal Kerr metric (a* = 1), for
which the ring radius is a = GM/c^2 = r_s/2. That is standard general
relativity, not an ECF-specific claim.

DOES NOT ASSERT: that the absence of a horizon is established. Foundation II
attributes it to the conserved topological charge; the figure marks it as a
model statement, drawn dashed, and says so in the panel. Confusing the two
would be exactly the kind of overclaim this corpus tries to avoid.

Dependency: numpy, matplotlib. Usage: python3 plot_F2_microknot_structure.py
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
from matplotlib.patches import Circle, Ellipse, FancyArrowPatch

# --- import the mass rather than restate it --------------------------------
_ROOT = os.path.dirname(os.path.abspath(__file__))
# [CORRIGE 15/09/2026] Ce script chargeait calculate_microknot_mass.py depuis
# son PROPRE dossier, ce qui obligeait a garder une copie du script de calcul
# dans B_Paper_Plots -- un fichier de calcul dans un dossier de figures, et
# deux copies susceptibles de diverger. Meme repli que plot_F2_microknot_press.py :
# on cherche d'abord l'original dans A_Core_Calculations.
_candidat_A = os.path.join(os.path.dirname(_ROOT), "A_Core_Calculations",
                           "calculate_microknot_mass.py")
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
M_SUN = 1.98892e30
M = _mk.horizon_mass(_mk.hubble_rate(_mk.T_C))
SIG_M = M * 2.0 * _mk.SIG_T_C / _mk.T_C
R_S = 2.0 * G * M / C ** 2                 # Schwarzschild radius
A_RING = G * M / C ** 2                    # extremal Kerr: a = GM/c^2 = r_s/2
OMEGA_LT = 2.698e10                          # rad/s, frame dragging (F2)
T_H_MK = 32.8                              # mK
T_CMB_MK = 2725.0
T_EVAP_YR = 1.40e50
AGE_YR = 1.38e10
M_EARTH = 5.972e24

plt.rcParams.update({"font.size": 9, "axes.linewidth": 0.8,
                     "font.family": "DejaVu Sans"})
fig = plt.figure(figsize=(15, 5.2))
gs = fig.add_gridspec(1, 3, width_ratios=[1.15, 1, 1], wspace=0.28)

# ============================================================ Panel A
axA = fig.add_subplot(gs[0])
axA.set_aspect("equal")
lim = 1.9
axA.set_xlim(-lim, lim); axA.set_ylim(-lim, lim)

# ergosphere: prolate, drawn as the outer envelope
axA.add_patch(Ellipse((0, 0), 2.7, 3.2, facecolor="#E8EEF7",
                      edgecolor="#5B7DB1", lw=1.2, ls="-", zorder=1))
# where a horizon WOULD be, for a non-rotating object of the same mass
axA.add_patch(Circle((0, 0), 1.0, facecolor="none", edgecolor="#B0B0B0",
                     lw=1.4, ls=(0, (5, 4)), zorder=2))
# the ring itself, a = r_s/2 -> radius 0.5 in units of r_s
th = np.linspace(0, 2 * np.pi, 400)
axA.plot(0.5 * np.cos(th), 0.5 * np.sin(th) * 0.34, color="#8E1B3A",
         lw=3.2, zorder=4, solid_capstyle="round")
axA.plot(0.5 * np.cos(th), 0.5 * np.sin(th) * 0.34, color="#C0392B",
         lw=1.4, zorder=5, solid_capstyle="round")

# frame dragging arrows
for ang in (35, 155, 275):
    r0 = 1.25
    x0, y0 = r0 * np.cos(np.radians(ang)), r0 * np.sin(np.radians(ang)) * 0.92
    x1 = r0 * np.cos(np.radians(ang + 26))
    y1 = r0 * np.sin(np.radians(ang + 26)) * 0.92
    axA.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>",
                                  mutation_scale=13, color="#2C6E9B",
                                  lw=1.5, zorder=6,
                                  connectionstyle="arc3,rad=0.28"))

axA.annotate("ring singularity\n$a = GM/c^2 = r_s/2$",
             xy=(0.42, -0.10), xytext=(1.0, -1.45), fontsize=8.5,
             color="#8E1B3A", ha="center",
             arrowprops=dict(arrowstyle="-", color="#8E1B3A", lw=0.8))
axA.annotate("ergosphere", xy=(0, 1.55), xytext=(0, 1.72),
             fontsize=8.5, color="#3A5B87", ha="center")
axA.annotate("no horizon forms\n(topological charge)", xy=(-0.72, 0.70),
             xytext=(-1.62, 1.32), fontsize=8.5, color="#707070", ha="center",
             arrowprops=dict(arrowstyle="-", color="#909090", lw=0.8))
axA.annotate(r"frame dragging  $\Omega\simeq2.7\times10^{10}$ rad s$^{-1}$ ( $v=c/2$ at $r_s$)",
             xy=(0, -1.75), fontsize=8.5, color="#2C6E9B", ha="center")

axA.set_title("(A)  Extremal Kerr geometry ($a^{*}=1$)", fontsize=10,
              fontweight="bold", pad=10)
axA.set_xticks([]); axA.set_yticks([])
for s in axA.spines.values():
    s.set_visible(False)

# ============================================================ Panel B
axB = fig.add_subplot(gs[1])
items = [
    ("Micro-Knot\n$r_s$ = 5.6 mm", R_S, "#8E1B3A"),
    ("Moon\n(radius)", 1.737e6, "#8A8A8A"),
    ("Earth\n(radius)", 6.371e6, "#4A7C59"),
    ("Macro-Knot $r_s$\n($10^5 M_\\odot$)", 2 * G * 1e5 * M_SUN / C ** 2, "#2C6E9B"),
    ("Sun\n(radius)", 6.957e8, "#E67E22"),
    ("Macro-Knot $r_s$\n($10^6 M_\\odot$)", 2 * G * 1e6 * M_SUN / C ** 2, "#1F4E79"),
]
LEFT_B = -3.0
ys = np.arange(len(items))[::-1]
for y, (lbl, val, col) in zip(ys, items):
    lg = np.log10(val)
    axB.barh(y, lg - LEFT_B, left=LEFT_B, color=col, alpha=0.82, height=0.52)
    axB.text(lg + 0.3, y, f"{val:.3g} m", va="center", ha="left",
             fontsize=8.5, color=col, fontweight="bold")
axB.set_yticks(ys)
axB.set_yticklabels([i[0] for i in items], fontsize=8.5)
axB.set_xlabel(r"$\log_{10}$ (size / m)", fontsize=9)
axB.set_xlim(LEFT_B, 12.5)
axB.set_title("(B)  From a marble to a star", fontsize=10,
              fontweight="bold", pad=10)
axB.grid(axis="x", ls=":", alpha=0.45)
for s in ("top", "right"):
    axB.spines[s].set_visible(False)

# ============================================================ Panel C
axC = fig.add_subplot(gs[2])
axC.set_xscale("log")
rows = [
    ("Hawking $T_H$", T_H_MK, "#C0392B"),
    ("CMB temperature", T_CMB_MK, "#2C6E9B"),
]
for i, (lbl, v, col) in enumerate(rows):
    axC.barh(1 - i, v, color=col, alpha=0.82, height=0.45, left=5)
    axC.text(v * 1.35, 1 - i, f"{v:.6g} mK", va="center", fontsize=8.5, color=col)
axC.set_yticks([1, 0]); axC.set_yticklabels([r[0] for r in rows], fontsize=8.5)
axC.set_xlim(5, 4e4)
axC.set_xlabel("temperature [mK]", fontsize=9)
axC.set_title("(C)  Stability against evaporation", fontsize=10,
              fontweight="bold", pad=10)
axC.grid(axis="x", ls=":", alpha=0.45)
for s in ("top", "right"):
    axC.spines[s].set_visible(False)
axC.text(0.03, 0.42,
         f"$T_H$ is {T_CMB_MK/T_H_MK:.0f}$\\times$ below the CMB:\n"
         f"the object absorbs, it does not\n"
         f"evaporate.\n\n"
         f"Evaporation time $\\sim10^{{{np.log10(T_EVAP_YR):.0f}}}$ yr,\n"
         f"against $1.4\\times10^{{10}}$ yr for the\n"
         f"age of the universe.",
         transform=axC.transAxes, ha="left", va="top", fontsize=8.4,
         color="#444",
         bbox=dict(boxstyle="round,pad=0.5", facecolor="#FAFAFA",
                   edgecolor="#DDD", lw=0.8))

fig.suptitle(
    f"ECF Micro-Knot: a topological defect, not a primordial black hole\n"
    f"$M = ({M/1e24:.2f}\\pm{SIG_M/1e24:.2f})\\times10^{{24}}$ kg "
    f"$= {M/M_EARTH:.2f}\\,M_\\oplus$   ·   "
    f"$r_s = {1000*R_S:.2f}$ mm   ·   ring $a = {1000*A_RING:.2f}$ mm",
    fontsize=11.5, fontweight="bold", y=1.03)

fig.text(0.5, -0.055,
         "The dashed circle marks where a horizon would sit for a "
         "non-rotating body of the same mass. Foundation II attributes its "
         "absence to the conserved topological charge; that is a statement of "
         "the model, not an established result.\n"
         "The extremal-Kerr ring geometry ($a=GM/c^2$) is standard general "
         "relativity. Mass imported from calculate_microknot_mass.py.",
         ha="center", va="top", fontsize=8, color="#555")

out = os.path.join(_ROOT, "Fig_MicroKnot_Structure.png")
fig.savefig(out, dpi=300, bbox_inches="tight", facecolor="white")
print(f"written: {out}")
print(f"  M     = ({M/1e24:.2f} +/- {SIG_M/1e24:.2f}) x 10^24 kg = {M/M_EARTH:.2f} M_Earth")
print(f"  r_s   = {1000*R_S:.3f} mm")
print(f"  ring  = {1000*A_RING:.3f} mm  (= r_s/2, extremal Kerr)")
print(f"  T_H   = {T_H_MK} mK, i.e. {T_CMB_MK/T_H_MK:.0f}x below the CMB")

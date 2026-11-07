#!/usr/bin/env python3
"""
plot_ECF_frame_dragging_cascade.py

Synthesis figure for Foundation III: the "fossilized frame-dragging" cascade.

A single image summarizing how the parent black hole's spin propagates,
via frame-dragging (Lense-Thirring), across four scales of the ECF corpus:

    parent spin a*  ->  child chiral axis  ->  Pi_GW / P-violation  ->  homochirality

The same Penrose function f(a*) that governs the energy flux (PO-F3-1),
the viability threshold (PO-F3-SEUIL) and the bounce thermodynamics
(PO-F3-4) also governs the chirality it imprints. A single symmetry
breaking (parity P) is transmitted from the Kerr metric down to the
handedness of biological molecules.

Output: Fig_ECF_FrameDragging_Cascade.png  (300 dpi, publication quality)
"""

# UTF-8 guard: added 24/08/2026 so the script does not
# crash on a Windows cp1252 console.
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
from matplotlib.collections import LineCollection
import matplotlib.font_manager as fm

# ----------------------------------------------------------------------
# Aesthetic configuration
# ----------------------------------------------------------------------
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["DejaVu Serif"],
    "mathtext.fontset": "dejavuserif",
    "axes.linewidth": 0.0,
})

# Deep-space palette
BG        = "#0a0e1a"   # near-black navy
PANEL     = "#131a2e"   # panel fill
INK       = "#e8ecf5"   # near-white text
MUTED     = "#8b97b5"   # muted labels
GOLD      = "#f2c14e"   # accent / spin
CYAN      = "#4fd0e0"   # geometry
VIOLET    = "#b57edc"   # cosmology
ROSE      = "#e87a90"   # biology
GREEN     = "#7fd18b"   # established status

STAGE_COLORS = [GOLD, CYAN, VIOLET, ROSE]


def penrose_f(a):
    """Extractable rotational-energy fraction (Penrose-Christodoulou)."""
    return 1.0 - np.sqrt((1.0 + np.sqrt(1.0 - a**2)) / 2.0)


# ----------------------------------------------------------------------
# Figure scaffold
# ----------------------------------------------------------------------
fig = plt.figure(figsize=(15, 9.2), dpi=300)
fig.patch.set_facecolor(BG)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 15)
ax.set_ylim(0, 9.2)
ax.axis("off")
ax.set_facecolor(BG)


# ----------------------------------------------------------------------
# Title
# ----------------------------------------------------------------------
ax.text(7.5, 8.72, "The Fossilized Frame-Dragging Cascade",
        ha="center", va="center", color=INK, fontsize=25, weight="bold")
ax.text(7.5, 8.24,
        "One symmetry breaking (parity $P$), transmitted from the Kerr metric to the handedness of life",
        ha="center", va="center", color=MUTED, fontsize=12.5, style="italic")


# ----------------------------------------------------------------------
# Helper: rounded panel
# ----------------------------------------------------------------------
def panel(x, y, w, h, color, lw=1.6, fill=PANEL, alpha=1.0):
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.18",
        linewidth=lw, edgecolor=color, facecolor=fill, alpha=alpha,
        mutation_aspect=1.0, zorder=3)
    ax.add_patch(box)
    return box


def arrow(x0, y0, x1, y1, color, lw=2.6, style="-|>", ms=22, rad=0.0):
    a = FancyArrowPatch(
        (x0, y0), (x1, y1),
        arrowstyle=style, mutation_scale=ms,
        linewidth=lw, color=color,
        connectionstyle=f"arc3,rad={rad}", zorder=4,
        capstyle="round")
    ax.add_patch(a)
    return a


# ----------------------------------------------------------------------
# Four stage panels along a gentle descending diagonal
# ----------------------------------------------------------------------
# positions (lower-left corners) and sizes
PW, PH = 3.05, 2.35
stage_xy = [
    (0.55, 5.35),   # Stage 1 - parent spin (F3)
    (4.05, 5.35),   # Stage 2 - chiral axis (F2)
    (7.55, 5.35),   # Stage 3 - Pi_GW / P-violation (F2)
    (11.05, 5.35),  # Stage 4 - homochirality (biology)
]
titles = [
    "1.  PARENT SPIN",
    "2.  CHIRAL AXIS",
    "3.  $P$-VIOLATION",
    "4.  HOMOCHIRALITY",
]
scales = ["Foundation III  ·  strong gravity",
          "Foundation II  ·  primordial geometry",
          "Foundation II  ·  cosmology",
          "biology  ·  Bennu / interstellar ice"]
subs = [
    "Kerr black hole rotates:\nframe-dragging $g_{t\\phi}\\propto a^*$",
    "Entrainment imprinted in\nthe newborn white hole:\n$\\sigma^2_{\\rm baby}\\propto a^*$",
    "Broken mirror symmetry:\nchiral vacuum, $\\Pi_{\\rm GW}$\ngravitational-wave asymmetry",
    "Left-handed amino acids;\nracemic constraints from\nOSIRIS-REx samples",
]

for (x, y), title, scale, sub, col in zip(stage_xy, titles, scales, subs, STAGE_COLORS):
    panel(x, y, PW, PH, col)
    # top accent bar
    ax.add_patch(FancyBboxPatch((x, y + PH - 0.42), PW, 0.42,
                 boxstyle="round,pad=0.02,rounding_size=0.18",
                 linewidth=0, facecolor=col, alpha=0.20, zorder=3.5))
    ax.text(x + 0.22, y + PH - 0.21, title, ha="left", va="center",
            color=col, fontsize=13.5, weight="bold", zorder=5)
    ax.text(x + PW/2, y + PH - 0.70, scale, ha="center", va="center",
            color=MUTED, fontsize=8.0, style="italic", zorder=5)
    # description text sits in the upper-middle; lower third holds the icon
    ax.text(x + PW/2, y + PH - 1.32, sub, ha="center", va="center",
            color=INK, fontsize=9.6, zorder=5, linespacing=1.4)

# connecting arrows between stages (with propagation label)
for i in range(3):
    x0 = stage_xy[i][0] + PW
    x1 = stage_xy[i+1][0]
    yc = stage_xy[i][1] + PH/2
    arrow(x0 + 0.04, yc, x1 - 0.04, yc, INK, lw=2.4, ms=20)

# [CORRECTED 08/09/2026] Labels were single-line horizontal and wider than
# the 0.45-unit gap between panels, so they overlapped the neighbouring
# boxes. Rotated to vertical: the gap constrains width, not height.
arrow_labels = ["frame-dragging", "$P$-breaking", "chiral chemistry"]
for i, lab in enumerate(arrow_labels):
    x0 = stage_xy[i][0] + PW
    x1 = stage_xy[i+1][0]
    xc = (x0 + x1) / 2
    yc = stage_xy[i][1] + PH/2
    ax.text(xc, yc + 0.62, lab, ha="center", va="center",
            color=MUTED, fontsize=7.6, style="italic", zorder=5,
            rotation=90)


# ----------------------------------------------------------------------
# Stage-1 inset: a spinning Kerr black hole with frame-dragging swirl
# ----------------------------------------------------------------------
cx, cy = stage_xy[0][0] + PW/2, stage_xy[0][1] + 0.72
# frame-dragging spiral (compact, sits in the lower half of the panel)
theta = np.linspace(0, 3.6 * np.pi, 400)
r = 0.025 + 0.030 * theta
xs = cx + r * np.cos(theta)
ys = cy + r * np.sin(theta) * 0.60   # slight ellipticity
pts = np.array([xs, ys]).T.reshape(-1, 1, 2)
segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
lc = LineCollection(segs, colors=GOLD,
                    linewidths=np.linspace(0.3, 2.0, len(segs)),
                    alpha=0.55, zorder=4)
ax.add_collection(lc)
# central black hole + accretion glow
ax.add_patch(Circle((cx, cy), 0.19, color="#000000", zorder=5))
ax.add_patch(Circle((cx, cy), 0.19, fill=False, lw=1.4, edgecolor=GOLD, zorder=6))
ax.add_patch(Circle((cx, cy), 0.09, color=GOLD, alpha=0.9, zorder=6))

# ----------------------------------------------------------------------
# Stage-2 inset: chiral axis (a helix winding around a vertical axis)
# ----------------------------------------------------------------------
cx2, cy2 = stage_xy[1][0] + PW/2, stage_xy[1][1] + 0.72
tt = np.linspace(0, 3.0*np.pi, 200)
hx = cx2 + 0.30*np.cos(tt)
hy = cy2 - 0.42 + (tt/(3.0*np.pi))*0.84
ax.plot(hx, hy, color=VIOLET, lw=2.2, zorder=5, solid_capstyle="round")
ax.plot(cx2 + 0.30*np.cos(tt+np.pi), hy, color=VIOLET, lw=1.1,
        alpha=0.45, zorder=4, solid_capstyle="round")
arrow(cx2, cy2 - 0.52, cx2, cy2 + 0.52, MUTED, lw=1.2, ms=12)

# ----------------------------------------------------------------------
# Stage-3 inset: broken mirror symmetry (two arcs, one struck through)
# ----------------------------------------------------------------------
cx3, cy3 = stage_xy[2][0] + PW/2, stage_xy[2][1] + 0.72
# left-handed and right-handed curved arrows, asymmetric weights
arc = np.linspace(-0.7*np.pi, 0.7*np.pi, 100)
ax.plot(cx3 - 0.34 + 0.22*np.cos(arc), cy3 + 0.22*np.sin(arc),
        color=VIOLET, lw=2.6, zorder=5, solid_capstyle="round")
ax.plot(cx3 + 0.34 - 0.22*np.cos(arc), cy3 + 0.22*np.sin(arc),
        color=MUTED, lw=1.0, alpha=0.5, zorder=5, solid_capstyle="round")
# dashed mirror line
ax.plot([cx3, cx3], [cy3 - 0.42, cy3 + 0.42], color=MUTED, lw=0.9,
        ls=(0, (3, 3)), zorder=4)

# ----------------------------------------------------------------------
# Stage-4 inset: a chiral molecule (central C with four distinct groups)
# ----------------------------------------------------------------------
cx4, cy4 = stage_xy[3][0] + PW/2, stage_xy[3][1] + 0.72
ax.add_patch(Circle((cx4, cy4), 0.075, color=ROSE, zorder=6))
bond_ang = [90, 210, 330, 25]
bond_len = [0.40, 0.36, 0.36, 0.30]
bond_c   = [INK, ROSE, CYAN, GOLD]
for ang, ln, bc in zip(bond_ang, bond_len, bond_c):
    ex = cx4 + ln*np.cos(np.radians(ang))
    ey = cy4 + ln*np.sin(np.radians(ang))
    ax.plot([cx4, ex], [cy4, ey], color=bc, lw=1.8, zorder=5,
            solid_capstyle="round")
    ax.add_patch(Circle((ex, ey), 0.055, color=bc, zorder=6))


# ----------------------------------------------------------------------
# Central spine: the invariant f(a*) that governs every stage
# ----------------------------------------------------------------------
# (baseline spine removed; the f(a*) ribbon below carries the invariant)

# The f(a*) curve as a ribbon under the cascade
ax_curve = fig.add_axes([0.085, 0.085, 0.63, 0.235])
ax_curve.set_facecolor(PANEL)
for spine in ax_curve.spines.values():
    spine.set_color("#2a3450")
    spine.set_linewidth(1.0)
a = np.linspace(0, 0.998, 400)
f = penrose_f(a)
ax_curve.plot(a, f, color=GOLD, lw=2.8, zorder=5)
ax_curve.fill_between(a, 0, f, color=GOLD, alpha=0.10, zorder=4)
# mark the extremal bound
ax_curve.axhline(penrose_f(0.998), color=MUTED, lw=0.9, ls=":", zorder=3)
ax_curve.text(0.02, penrose_f(0.998) + 0.006,
              "extremal bound $f<0.29$", color=MUTED, fontsize=8.5,
              va="bottom", ha="left")
ax_curve.set_xlim(0, 1.0)
ax_curve.set_ylim(0, 0.32)
ax_curve.set_xlabel("dimensionless spin  $a^*$", color=INK, fontsize=10)
ax_curve.set_ylabel("$f(a^*)$", color=INK, fontsize=11)
ax_curve.tick_params(colors=MUTED, labelsize=8.5)
ax_curve.set_title(
    "The single invariant  $f(a^*)=1-\\sqrt{(1+\\sqrt{1-a^{*2}})/2}$",
    color=INK, fontsize=10.5, pad=6)

# annotate the three roles it plays
roles = [
    (0.30, "energy flux\n(PO-F3-1)"),
    (0.60, "viability\n(PO-F3-SEUIL)"),
    (0.88, "thermal regime\n(PO-F3-4)"),
]
for ax_pos, lab in roles:
    ax_curve.axvline(ax_pos, color=CYAN, lw=0.8, ls="--", alpha=0.5, zorder=3)
    ax_curve.text(ax_pos, 0.30, lab, color=CYAN, fontsize=7.6,
                  ha="center", va="top", linespacing=1.2)


# ----------------------------------------------------------------------
# Right-hand status box: established / proposed / to prove
# ----------------------------------------------------------------------
sx, sy, sw, sh = 10.55, 0.55, 3.75, 3.35
panel(sx, sy, sw, sh, "#2a3450", lw=1.3, fill="#0f1526")
ax.text(sx + sw/2, sy + sh - 0.32, "Epistemic status",
        ha="center", va="center", color=INK, fontsize=12.5, weight="bold")

status_items = [
    (GREEN,  "ESTABLISHED",
     "Frame-dragging is real (Gravity\nProbe B), scales as $a^*$, carries\nintrinsic chirality."),
    (GOLD,   "PROPOSED",
     "It is the origin of the child's\nchiral axis \u2014 an imprint, with\nno spin extracted from the parent."),
    (ROSE,   "TO BE PROVEN",
     "Dynamical ECKS junction; axis\norientation preserved through the\nbounce; imprint $\\to\\sigma^2_{\\rm baby}$ law."),
]
yy = sy + sh - 0.92
for col, head, body in status_items:
    ax.add_patch(Circle((sx + 0.32, yy), 0.075, color=col, zorder=6))
    ax.text(sx + 0.54, yy, head, ha="left", va="center",
            color=col, fontsize=10.5, weight="bold", zorder=6)
    ax.text(sx + 0.54, yy - 0.44, body, ha="left", va="center",
            color=INK, fontsize=8.6, zorder=6, linespacing=1.35)
    yy -= 1.02


# ----------------------------------------------------------------------
# Footer
# ----------------------------------------------------------------------
ax.text(7.5, 0.22,
        "Einstein-Cartan Framework  ·  Foundation III  ·  the parent spin $a^*$ is the single parameter "
        "threading strong gravity, cosmological chirality, and prebiotic handedness",
        ha="center", va="center", color=MUTED, fontsize=8.8, style="italic")


# ----------------------------------------------------------------------
# Export
# ----------------------------------------------------------------------
outfile = "Fig_ECF_FrameDragging_Cascade.png"
fig.savefig(outfile, dpi=300, facecolor=BG, bbox_inches="tight", pad_inches=0.15)
print(f"Saved: {outfile}")

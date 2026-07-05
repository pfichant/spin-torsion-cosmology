#!/usr/bin/env python3
"""
plot_ECF_genealogy.py
Intellectual genealogy of the Einstein-Cartan Framework (ECF).

A sober filiation diagram showing the established foundations the ECF
builds on, the parallel modern spin-torsion cosmology programme it sits
within, and the single incremental contribution of the ECF itself.

Design principles (deliberately NON-marketing):
  - The ECF box is at the SAME visual level as other recent works,
    not at the apex of a pyramid.
  - Every arrow means "builds on", never "surpasses".
  - All entries carry exact references (year, journal/arXiv) so a
    specialist can verify each claim.
  - No superlatives, no colour hierarchy implying ECF superiority.

All references verified July 2026.
Edit the WORKS list to update; the layout adapts automatically.
"""

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# ══════════════════════════════════════════════════════════════
# DATA — each work placed on an explicit (col, row) grid.
# col: 0=foundations 1=ECKS bounce 2=parallel modern 3=ECF
# row: vertical slot within column (0 = top)
# ══════════════════════════════════════════════════════════════
WORKS = [
    # id, label(short bold), ref(detail), col, row, is_ecf
    ("cartan",   "É. Cartan (1922)",
     "Torsion in the affine\nconnection\nC.R. Acad. Sci. 174", 0, 0, False),
    ("sciama",   "Sciama · Kibble (1961)",
     "Spin–torsion coupling\nfoundational ECSK theory", 0, 1, False),
    ("trautman", "Trautman (1973)",
     "Spin and singularity\navoidance\nNature Phys. Sci. 242", 0, 2, False),
    ("hehl",     "Hehl et al. (1976)",
     "Reference review of\nECSK gravity\nRev. Mod. Phys. 48, 393", 0, 3, False),

    ("pop2010",  "Popławski (2010)",
     "Cosmology with torsion\nPhys. Lett. B 694", 1, 1, False),
    ("pop2012",  "Popławski (2012)",
     "Big bounce from spin\n& torsion\nGRG 44, 1007", 1, 2, False),
    ("pop2016",  "Popławski (2016)",
     "Universe in a black hole\nApJ 832, 96", 1, 3, False),

    ("magueijo", "Magueijo·Zlosnik·Kibble (2013)",
     "Cosmology with a spin\nPhys. Rev. D 87, 063504", 2, 1, False),
    ("alexander","Alexander et al. (2014)",
     "Fermi-bounce cosmology\nPhys. Rev. D 90, 123510", 2, 2, False),
    ("unger",    "Unger · Popławski (2019)",
     "Big bounce & closed\nuniverse, ApJ 870, 78", 2, 3, False),
    ("shaposh",  "Shaposhnikov et al. (2021)",
     "Einstein-Cartan portal\nto dark matter, PRL 126", 2, 4, False),

    ("ecf",      "ECF — this work (2026)",
     "Phenomenological application\nof the ECKS bounce to H₀/S₈;\ntopological dark sector;\nfalsifiable observational tests", 3, 1, True),
]

COLUMN_TITLES = {
    0: "Geometric foundations\n1922 – 1976",
    1: "Modern ECKS bounce\n2010 – 2016",
    2: "Parallel spin-torsion\ncosmology · 2013 – 2021",
    3: "Present work\n2026",
}

# "builds on" arrows
ARROWS = [
    ("cartan", "sciama"), ("sciama", "trautman"), ("sciama", "hehl"),
    ("hehl", "pop2010"), ("trautman", "pop2010"), ("sciama", "pop2010"),
    ("pop2010", "pop2012"), ("pop2012", "pop2016"),
    ("pop2012", "magueijo"), ("pop2012", "alexander"), ("pop2016", "unger"),
    ("pop2010", "ecf"), ("pop2012", "ecf"), ("pop2016", "ecf"),
    ("magueijo", "ecf"), ("hehl", "ecf"),
]

# ══════════════════════════════════════════════════════════════
# LAYOUT — explicit grid
# ══════════════════════════════════════════════════════════════
COL_X = {0: 1.6, 1: 5.0, 2: 8.4, 3: 11.8}
ROW_DY = 1.7
ROW_TOP = 8.5
BOX_W, BOX_H = 2.7, 1.05

def pos(col, row):
    return COL_X[col], ROW_TOP - row * ROW_DY

POS = {wid: pos(col, row) for wid, _, _, col, row, _ in WORKS}

fig, ax = plt.subplots(figsize=(15, 10.5), facecolor="white")
ax.set_xlim(0, 13.4)
ax.set_ylim(-1.2, 10.2)
ax.axis("off")

COL_FILL = {0: "#EDF2F4", 1: "#E1EDF4", 2: "#EEEAF3", 3: "#FBEDE4"}
COL_EDGE = {0: "#8D99AE", 1: "#4F86A8", 2: "#8E7CA6", 3: "#C4703A"}

# Column headers
for col, title in COLUMN_TITLES.items():
    ax.text(COL_X[col], 9.7, title, ha="center", va="center",
            fontsize=11, fontweight="bold", color="#2B2D42", linespacing=1.3)

# Arrows behind boxes
for src, dst in ARROWS:
    x0, y0 = POS[src]; x1, y1 = POS[dst]
    ecf_t = (dst == "ecf")
    # exit right edge, enter left edge
    p0 = (x0 + BOX_W/2, y0)
    p1 = (x1 - BOX_W/2, y1)
    arr = FancyArrowPatch(
        p0, p1, arrowstyle="-|>", mutation_scale=13,
        color="#C4703A" if ecf_t else "#9AA5B4",
        alpha=0.6 if ecf_t else 0.4,
        lw=1.5 if ecf_t else 1.0,
        connectionstyle="arc3,rad=0.08", zorder=1,
    )
    ax.add_patch(arr)

# Boxes
for wid, label, ref, col, row, is_ecf in WORKS:
    x, y = POS[wid]
    box = FancyBboxPatch(
        (x - BOX_W/2, y - BOX_H/2), BOX_W, BOX_H,
        boxstyle="round,pad=0.03,rounding_size=0.10",
        facecolor=COL_FILL[col], edgecolor=COL_EDGE[col],
        lw=2.2 if is_ecf else 1.3, zorder=2,
    )
    ax.add_patch(box)
    ax.text(x, y + BOX_H/2 - 0.22, label, ha="center", va="center",
            fontsize=8.6 if is_ecf else 8.2, fontweight="bold",
            color="#1D1F2A", zorder=3)
    ax.text(x, y - 0.12, ref, ha="center", va="center",
            fontsize=7.2, color="#4A4A55", linespacing=1.18, zorder=3)

fig.suptitle("From Cartan's Torsion to the Einstein–Cartan Framework",
             fontsize=16, fontweight="bold", color="#2B2D42", y=0.985)

# ══════════════════════════════════════════════════════════════
# ECF INTERNAL STRUCTURE — PIT as keystone, four papers as corpus
# Drawn as a framed panel below/around the ECF box, sober style.
# ══════════════════════════════════════════════════════════════
ex, ey = POS["ecf"]
# Keystone label: PIT
ax.text(ex, ey - BOX_H/2 - 0.55,
        "organising principle:", ha="center", va="center",
        fontsize=7.0, color="#8A8A8A", style="italic")
kb = FancyBboxPatch(
    (ex - BOX_W/2, ey - BOX_H/2 - 1.35), BOX_W, 0.62,
    boxstyle="round,pad=0.03,rounding_size=0.08",
    facecolor="#F6E4D6", edgecolor="#C4703A", lw=1.6, zorder=2)
ax.add_patch(kb)
ax.text(ex, ey - BOX_H/2 - 0.90,
        "Topological Invariance\nPrinciple (PIT)", ha="center", va="center",
        fontsize=8.0, fontweight="bold", color="#8A4A1F",
        linespacing=1.15, zorder=3)
ax.text(ex, ey - BOX_H/2 - 1.62,
        "the geometric postulate\nfrom which the corpus follows",
        ha="center", va="center", fontsize=6.6, color="#8A8A8A",
        style="italic", linespacing=1.15)

# Corpus references (four papers) as a compact reference list
corpus = [
    "PIT Letter — zenodo.19900557",
    "Foundation I — zenodo.19577447",
    "Foundation II — zenodo.20629238",
    "Foundation III (in prep.)",
]
cy0 = ey - BOX_H/2 - 2.35
for i, c in enumerate(corpus):
    ax.text(ex, cy0 - i*0.30, c, ha="center", va="center",
            fontsize=6.7, color="#4A4A55")

# thin connector from ECF box down to PIT keystone
ax.plot([ex, ex], [ey - BOX_H/2, ey - BOX_H/2 - 0.73],
        color="#C4703A", lw=1.2, alpha=0.6, zorder=1)

ax.text(6.7, -0.95,
        "Intellectual genealogy. Arrows denote \u201cbuilds on\u201d. The ECF is a phenomenological application of the established "
        "ECKS bounce, shown at the same level as other recent spin-torsion\ncosmology programmes — it does not modify the "
        "underlying gravitational theory. Its contribution is the calibrated confrontation with H\u2080/S\u2088 data and the "
        "topological dark sector. All references verified.",
        ha="center", va="bottom", fontsize=7.8, color="#5A5A5A",
        style="italic", linespacing=1.4)

plt.tight_layout(rect=[0, 0.02, 1, 0.96])
out = "Fig_ECF_Genealogy.png"
plt.savefig(out, dpi=200, bbox_inches="tight", facecolor="white")
print(f"Saved: {out}")
plt.close()

#!/usr/bin/env python3
"""
Fig_Gamma_macro_z.png -- Macro-Knot collision rate, field halo vs galactic centre.

Matplotlib version, written 13/09/2026.

WHY THIS VERSION
    The original (plot_gamma_macro_z.py) uses Plotly, whose write_image
    requires a Chrome binary. When Chrome is absent the script dies at the
    write_image call -- before writing the .meta.json, which therefore remains
    that of an earlier run. Matplotlib has no such dependency.

PHYSICS CHANGE (13/09/2026)
    N_macro_MW: 1e3 -> 1.0 per halo.
    The 1e3 value contradicted the working assumption of F2 (Sec. 4.4,
    "O(1) per galactic volume", i.e. a mass fraction f_macro ~ 1e-7 to 1e-6;
    not derived, corrected 17/10/2026) by two to three orders of magnitude.
    The assumed value is retained.

    Consequence: the curve drops by three decades. Annotations hard-coded on
    the old position have been re-anchored -- otherwise the "rapid coagulation
    zone" band floats above the curve marking nothing, and the vertical labels
    cross it.
"""
import json
import os
import sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# -- Physical constants ------------------------------------------------------
G    = 6.674e-11
Msun = 1.989e30
kpc  = 3.086e19
yr   = 3.156e7

# -- Macro-Knot parameters (F2, App. D) --------------------------------------
M_macro    = 1e5 * Msun          # kg
v_galaxy   = 300e3               # m/s
N_macro_MW = 1.0                 # per halo -- CORRECTED 13/09/2026 (was 1e3)
R_halo     = 30 * kpc
V_halo     = (4/3) * np.pi * R_halo**3

n_macro_halo     = N_macro_MW / V_halo
sigma_grav_macro = np.pi * (2*G*M_macro/v_galaxy**2)**2
Gamma_macro_0    = n_macro_halo * sigma_grav_macro * v_galaxy

# Galactic centre: density x1000, velocity x3
n_macro_GC       = 1000 * n_macro_halo
v_GC             = 3 * v_galaxy
sigma_grav_GC    = np.pi * (2*G*M_macro/v_GC**2)**2
Gamma_macro_GC_0 = n_macro_GC * sigma_grav_GC * v_GC

z = np.logspace(0, 13, 600)
gamma_halo = Gamma_macro_0    * (1+z)**1.5
gamma_GC   = Gamma_macro_GC_0 * (1+z)**1.5

# -- Cosmic time since the bounce ---------------------------------------------
# Flat radiation+matter, adequate for the orders of magnitude shown here.
# [D3, 22/09/2026 -- DEC-A7-POST-05] LCDM reference, not the ECF background (A-7):
# H0 = 2.2e-18 s^-1 (~68 km/s/Mpc) with Planck-h Omegas, for orders of magnitude only. Kept.
H0, Om_r, Om_m = 2.2e-18, 9.2e-5, 0.315
z_eq = Om_m/Om_r - 1

def t_since_bounce(zz):
    """Time elapsed since the bounce, in seconds."""
    if zz > z_eq:
        return 1/(2*H0*np.sqrt(Om_r)*(1+zz)**2)
    return 2/(3*H0*np.sqrt(Om_m)*(1+zz)**1.5)

def fmt_time(t):
    """Human-readable time label."""
    if t < 1e-3:   return f"{t:.0e} s"
    if t < 60:     return f"{t:.2g} s"
    if t < 3600:   return f"{t/60:.0f} min"
    if t < 86400:  return f"{t/3600:.0f} h"
    if t < 3.156e7:return f"{t/86400:.0f} days"
    if t < 3.156e10: return f"{t/3.156e7:.0f} yr"
    return f"{t/3.156e7:.2g} yr"

# -- Figure ------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6.2), dpi=200)
ax.set_facecolor("white")
fig.patch.set_facecolor("white")

ax.loglog(z, gamma_halo, color="#2E86C1", lw=2.8,
          label="Macro-Knots (halo field)", zorder=5)
ax.fill_between(z, gamma_halo, 1e-40, color="#2E86C1", alpha=0.05, zorder=1)
ax.loglog(z, gamma_GC, color="#8E44AD", lw=2.2, ls="--",
          label="Macro-Knots (galactic centre)", zorder=5)

# Vertical bounds anchored on the data, with margin
y_lo = min(gamma_halo.min(), gamma_GC.min()) / 30
y_hi = max(gamma_halo.max(), gamma_GC.max()) * 30
ax.set_ylim(y_lo, y_hi)
ax.set_xlim(1, 1e13)

# -- Vertical markers --------------------------------------------------------
# Labels are placed at a fixed fraction of the axis height, so they follow the
# data instead of being hard-coded.
# Only events that belong to the process being plotted are marked. Recombination
# and first-galaxy formation were removed on 13/09/2026: Macro-Knot coagulation
# is over by t ~ 1.3 s, so later epochs bear no causal relation to this curve,
# and marking them invited a comparison the framework does not make. Those
# epochs are treated where they belong -- the Macro-Knot -> LRD -> SMBH chain
# has its own figures in F2.
for zv, label, frac in [
    # [15/10/2026, F2-A15] was "QGP freeze-out (Macro-Knot crystallisation)": F2 sets the Macro-Knot
    # scale by the horizon mass at the Great Annihilation, not by a QGP freeze-out.
    (1e12, "QGP transition\n(not a Macro-Knot epoch)", 0.055),
]:
    label = f"{label}\n[{fmt_time(t_since_bounce(zv))} after the bounce]"
    ax.axvline(zv, color="#bbbbbb", ls=":", lw=1.3, zorder=2)
    y_lab = y_lo * (y_hi/y_lo)**frac
    ax.annotate(label, xy=(zv, y_lab), xytext=(-12, 0),
                textcoords="offset points", ha="right", va="center",
                fontsize=9, color="#555555",
                bbox=dict(boxstyle="round,pad=0.3", fc="white",
                          ec="#cccccc", alpha=0.93), zorder=6,
                arrowprops=dict(arrowstyle="->", color="#999999", lw=1.0,
                                shrinkA=2, shrinkB=1))

# -- Merger regimes, split by the "one merger per Hubble time" threshold -------
# This threshold is what makes the plot readable: above it an object undergoes
# at least one collision over cosmic history, below it essentially none.
y_hub = 1/(13.8e9*yr)

ax.axhspan(y_hub, y_hi, color="#27AE60", alpha=0.055, zorder=0)
ax.axhspan(y_lo, y_hub, color="#7F8C8D", alpha=0.045, zorder=0)
ax.axhline(y_hub, color="#27AE60", ls="--", lw=1.6, zorder=4)

ax.annotate("MERGERS HAPPEN\nat least one per object over cosmic history",
            xy=(1.5, y_hub), xytext=(0, 9), textcoords="offset points",
            ha="left", va="bottom", fontsize=8.5, color="#1E8449",
            fontweight="bold", linespacing=1.5, zorder=8,
            bbox=dict(boxstyle="round,pad=0.35", fc="white",
                      ec="#27AE60", lw=0.9, alpha=0.93))

ax.annotate("MERGERS NEGLIGIBLE\nan object crosses cosmic history untouched",
            xy=(1.5, y_hub), xytext=(0, -9), textcoords="offset points",
            ha="left", va="top", fontsize=8.5, color="#5D6D7E",
            fontweight="bold", linespacing=1.5, zorder=8,
            bbox=dict(boxstyle="round,pad=0.35", fc="white",
                      ec="#95A5A6", lw=0.9, alpha=0.93))

ax.annotate(f"1 merger / Hubble time  ({y_hub:.0e} s$^{{-1}}$)",
            xy=(1e13, y_hub), xytext=(-6, 5), textcoords="offset points",
            ha="right", va="bottom", fontsize=8.5, color="#1E8449", zorder=8)

# -- Where the halo curve crosses that threshold ------------------------------
z_cross = ((y_hub/Gamma_macro_0)**(1/1.5)) - 1
if 1 < z_cross < 1e13:
    t_cross = t_since_bounce(z_cross)
    ax.plot([z_cross], [y_hub], "o", ms=7, mfc="white",
            mec="#27AE60", mew=2, zorder=9)
    ax.annotate(f"kinetic rate drops below the Hubble threshold\n"
                f"at z $\\approx$ {z_cross:.0e} ({fmt_time(t_cross)} after the bounce)\n"
                "-- NOT the end of coagulation: that came earlier,\n"
                "at the Great Annihilation (see marker)",
                xy=(z_cross, y_hub), xytext=(14, -46),
                textcoords="offset points", ha="left", va="top",
                fontsize=8.5, color="#1E8449", linespacing=1.6, zorder=9,
                bbox=dict(boxstyle="round,pad=0.35", fc="white",
                          ec="#27AE60", lw=0.9, alpha=0.93),
                arrowprops=dict(arrowstyle="-", color="#27AE60", lw=0.9))

# -- Great Annihilation: where topological growth actually stops --------------
# F2: "This cataclysm abruptly removes the kinematic friction, forcing the
# topological growth to instantly cease" -- at T < 1.02 MeV, i.e. z ~ 4.3e9.
# [REQUALIFIE 17/09/2026 — MEMO 43] C'est la fin de la coagulation des
# MICRO-Knots. La coagulation ne produit pas les Macro-Knots : sa masse
# typique sature vers 6.8e-5 Msun, neuf ordres sous le benchmark Macro.
z_GA = 4.34e9
ax.axvline(z_GA, color="#D35400", ls="-", lw=2.0, alpha=0.75, zorder=4)
ax.annotate("GREAT ANNIHILATION (a process, not an instant)\n"
            f"pair-production threshold T < 2m$_e$c$^2$ = 1.02 MeV, "
            f"{fmt_time(t_since_bounce(z_GA))} after the bounce\n"
            "F2 works with the window T ~ 0.16-1.6 MeV\n"
            "kinematic friction removed -> topological growth ceases",
            xy=(z_GA, y_lo*(y_hi/y_lo)**0.80), xytext=(-10, 0),
            textcoords="offset points", ha="right", va="center",
            fontsize=8.5, color="#A04000", fontweight="bold", linespacing=1.5,
            zorder=9, bbox=dict(boxstyle="round,pad=0.35", fc="white",
                                ec="#D35400", lw=1.1, alpha=0.95))

# -- Rapid coagulation zone (QGP freeze-out) ----------------------------------
m = (z >= 1e11) & (z <= 1e13)
ax.axvspan(1e11, 1e13, color="#E74C3C", alpha=0.05, zorder=0)
ax.annotate("Rapid Micro-Knot coagulation",
            xy=(1e13, y_hi), xytext=(-6, -14), textcoords="offset points",
            ha="right", va="top", fontsize=8.5, color="#C0392B",
            linespacing=1.5, zorder=8,
            bbox=dict(boxstyle="round,pad=0.3", fc="white",
                      ec="#E74C3C", lw=0.9, alpha=0.93))

ax.set_xlabel("Redshift  z", fontsize=11)
ax.set_ylabel(r"$\Gamma_{\rm macro}$   [s$^{-1}$]", fontsize=11)
ax.set_title("Macro-Knot collision rate $\\Gamma(z)$ — field halo vs galactic centre — ECF F2",
             fontsize=13, pad=38)
ax.grid(True, which="major", color="#f0f0f0", lw=0.8)
ax.grid(True, which="minor", color="#f8f8f8", lw=0.5)
ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.075), ncol=2,
          frameon=True, facecolor="#f5f5f5", edgecolor="#aaaaaa", fontsize=10)

fig.tight_layout()

# -- Output ------------------------------------------------------------------
# Written next to this script, not to the current working directory: running
# from another folder (or a synced one such as OneDrive) otherwise sends the
# file somewhere unexpected.
OUT_DIR = Path(__file__).resolve().parent
png = OUT_DIR / "Fig_Gamma_macro_z.png"
meta = OUT_DIR / "Fig_Gamma_macro_z.png.meta.json"

def write_png(target):
    """Save the figure, falling back to a suffixed name if the file is locked."""
    try:
        fig.savefig(target, dpi=200, facecolor="white")
        return target
    except OSError as exc:
        # Windows raises OSError 22 / 13 when the PNG is open in a viewer, or
        # when a cloud-synced folder holds a placeholder file.
        alt = target.with_name(target.stem + "_new" + target.suffix)
        print(f"[warning] could not write {target.name} ({exc.errno}: {exc.strerror}).",
              file=sys.stderr)
        print("          The file is probably open in an image viewer, or the",
              file=sys.stderr)
        print("          folder is cloud-synced. Writing to a new name instead.",
              file=sys.stderr)
        fig.savefig(alt, dpi=200, facecolor="white")
        return alt

written = write_png(png)

meta_payload = {
    "caption": "Macro-Knot collision rate \u0393_macro(z) \u2014 field halo vs galactic centre \u2014 ECF Foundation II",
    "description": ("Log-log evolution of the Macro-Knot collision rate, comparing halo "
                    "field and galactic centre (density x1000, velocity x3) from today to "
                    "QGP freeze-out. Normalised on N_macro = O(1) per halo (corrected "
                    "13/09/2026 from 1e3, which was inconsistent with the assumed "
                    "O(1) per galactic volume, i.e. f_macro ~ 1e-7 to 1e-6). The green dashed line "
                    "marks one merger per Hubble time; the orange line marks the Great "
                    "Annihilation, where topological growth actually ceases.")
}
try:
    with open(written.with_suffix(written.suffix + ".meta.json"), "w",
              encoding="utf-8") as f:
        json.dump(meta_payload, f, ensure_ascii=False)
except OSError as exc:
    print(f"[warning] could not write the .meta.json ({exc.strerror}).", file=sys.stderr)

print(f"Gamma_macro_0    = {Gamma_macro_0:.3e} s^-1")
print(f"Gamma_macro_GC_0 = {Gamma_macro_GC_0:.3e} s^-1")
print(f"{written.name} written to {written.parent} (matplotlib, no Chrome dependency)")

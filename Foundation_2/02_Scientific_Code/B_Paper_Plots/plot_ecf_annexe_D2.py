#!/usr/bin/env python3
"""
plot_ecf_annexe_D2.py
=====================
Génère les 5 figures de l'Annexe D.2 de Foundation II (ECF).

Figures produites :
    fig_ECF_Eps_top_q.png          — ε_top(q, ξ_T)
    fig_ECF_fmerger_vs_M.png       — f_peak vs M_tot + bandes instrumentales
    fig_ECF_Channel_Partition.png  — Partition canaux Régime I et II
    fig_KnotStar_Lx_vs_b.png       — L_X vs b, 3 sous-régimes Knot-Star
    fig_ECF_Ringdown_Tail.png      — Ringdown GR vs queue torsion

Usage :
    python plot_ecf_annexe_D2.py [--light] [--dpi 300] [--outdir ./figs]

Dépendances : numpy, matplotlib
Licence     : CC BY 4.0 — Pascal Fichant, 2026
"""

import argparse, os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ── CLI ──────────────────────────────────────────────────────────────────
parser = argparse.ArgumentParser(description="ECF Annexe D.2 figures")
parser.add_argument("--light",  action="store_true", help="White background (journal print)")
parser.add_argument("--dpi",    type=int, default=170, help="Output DPI (default 170)")
parser.add_argument("--outdir", type=str, default=".",  help="Output directory")
args = parser.parse_args()

os.makedirs(args.outdir, exist_ok=True)

# ── THEME — fond blanc journal, palette publication ───────────────────────
BG  = "white"
FG  = "#1a1a2e"
GR  = "#d0d4dd"
C_BLUE  = "#1565c0"
C_ORA   = "#e65100"
C_PUR   = "#6a1b9a"
C_GRN   = "#2e7d32"
C_YEL   = "#f9a825"
C_RED   = "#c62828"
C_TEAL  = "#00695c"
C_PIN   = "#880e4f"
# --light flag conservé pour compatibilité mais sans effet (toujours blanc)
# ── Légende : fond clair pour lisibilité ──────────────────────────────────
LEGEND_KW = dict(
    facecolor='#f5f5f5',
    edgecolor='#aaaaaa',
    framealpha=0.97,
    labelcolor='#1a1a2e',
    fontsize=9.5,
)


# ── CONSTANTES ────────────────────────────────────────────────────────────
C_SI   = 3e8          # m/s
G_SI   = 6.674e-11    # m³ kg⁻¹ s⁻²
MSUN   = 1.989e30     # kg
PC_M   = 3.086e16     # m/pc

def savefig(fig, name):
    path = os.path.join(args.outdir, name)
    fig.savefig(path, dpi=max(args.dpi, 300), bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"  → {path}")

def styled_ax(ax, fig):
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.tick_params(colors=FG, which="both", labelsize=10)
    for sp in ax.spines.values(): sp.set_edgecolor(GR)
    ax.grid(True, which="major", color=GR, lw=0.7)
    ax.xaxis.label.set_color(FG)
    ax.yaxis.label.set_color(FG)
    ax.title.set_color(FG)

# ═══════════════════════════════════════════════════════════════════════════
# FIG 1 — ε_top(q, ξ_T)
# ═══════════════════════════════════════════════════════════════════════════
print("Fig 1 — ε_top(q, ξ_T) ...")
q = np.linspace(0.01, 1.0, 500)
eps_bbh = 0.054 * 4*q / (1+q)**2

fig, ax = plt.subplots(figsize=(9, 5.5))
styled_ax(ax, fig)
cases = [(0.30, C_TEAL, "--", r"$\xi_T=0.30$  (minor merger)"),
         (1.00, C_GRN,  "-",  r"$\xi_T=1.00$  (BBH equiv.)"),
         (1.45, C_ORA,  "-",  r"$\xi_T=1.45$  (torsion mid)"),
         (1.85, C_PIN,  "-",  r"$\xi_T=1.85$  (torsion max)")]
for xi, col, ls, lbl in cases:
    ax.plot(q, eps_bbh*xi, color=col, lw=2.2, ls=ls, label=lbl)
ax.axhspan(0.01, 0.10, alpha=0.07, color=C_PUR, label=r"ECF range $[0.01, 0.10]$")
ax.axhline(0.054, color=C_GRN, lw=0.7, ls=":", alpha=0.6)
ax.text(0.02, 0.056, "NR max (q=1)", color=C_GRN, fontsize=8.5)
ax.set_xlim(0, 1); ax.set_ylim(0, 0.12)
ax.set_xlabel("Mass ratio  q = M1/M2", fontsize=12)
ax.set_ylabel("eps_top  (GW fraction)", fontsize=12)
ax.legend(**LEGEND_KW)
ax.set_title(r"ECF Constructive Merger Efficiency  eps_top(q, xi_T)" + "\n" +
             "vs mass ratio — Appendix D.2 §Regime I", fontsize=11)
savefig(fig, "fig_ECF_Eps_top_q.png")

# ═══════════════════════════════════════════════════════════════════════════
# FIG 2 — f_peak vs M_tot
# ═══════════════════════════════════════════════════════════════════════════
print("Fig 2 — f_peak vs M_tot ...")
M_kg = np.logspace(20, 42, 600)
M_Ms = M_kg / MSUN
f_pk = C_SI**3 / (6*np.pi*G_SI*M_kg)

fig, ax = plt.subplots(figsize=(9, 5.5))
styled_ax(ax, fig)
ax.grid(True, which="minor", color=GR, lw=0.25, alpha=0.4)
ax.loglog(M_Ms, f_pk, color=C_PUR, lw=2.8, label=r"$f_{\rm peak}=c^3/(6\pi GM)$")
bands = [(1e-9, 1e-6, "PTA/SKA", C_TEAL), (1e-4, 1e-1, "LISA", C_ORA),
         (10, 1e4, "ET/LIGO", C_GRN)]
for flo, fhi, lbl, col in bands:
    ax.axhspan(flo, fhi, alpha=0.13, color=col)
    ax.text(M_Ms[-1]*0.35, (flo*fhi)**0.5, lbl, color=col,
            fontsize=9, ha="right", va="center", fontweight="bold")
mass_cases = [(2e24/MSUN, "mu+mu", C_BLUE), (1e3, "mu+M", C_TEAL),
              (2e5, "M+M",  C_ORA),  (1e6, "Mh+M", C_PIN)]
for M, lbl, col in mass_cases:
    f = C_SI**3 / (6*np.pi*G_SI*M*MSUN)
    ax.scatter([M], [f], color=col, s=80, zorder=5)
    ax.annotate(lbl, (M, f), textcoords="offset points", xytext=(8,5), color=col, fontsize=9.5)
ax.set_xlim(M_Ms[0], M_Ms[-1]); ax.set_ylim(1e-12, 1e13)
ax.set_xlabel("M_tot  [Msun]", fontsize=12)
ax.set_ylabel("f_peak  [Hz]", fontsize=12)
ax.legend(**LEGEND_KW)
ax.set_title("ECF Merger GW Peak Frequency vs M_tot\nInstrument bands — Appendix D.2", fontsize=11)
savefig(fig, "fig_ECF_fmerger_vs_M.png")

# ═══════════════════════════════════════════════════════════════════════════
# FIG 3 — Channel partition
# ═══════════════════════════════════════════════════════════════════════════
print("Fig 3 — Channel partition ...")
fig, axes = plt.subplots(1, 2, figsize=(13, 5.5))
fig.patch.set_facecolor(BG)
# Régime I
ax = axes[0]; ax.set_facecolor(BG)
labels_I = ["GW", "Kinetic", "EM sec."]; mids_I = [94.5, 3, 0.5]; err_I = [4.5, 2, 0.5]
bars = ax.bar(labels_I, mids_I, color=[C_PUR, C_TEAL, C_ORA], width=0.5,
              yerr=err_I, capsize=6, error_kw=dict(color=FG, lw=1.5))
ax.set_ylim(0, 115); ax.set_ylabel("Energy fraction [%]", fontsize=11, color=FG)
ax.tick_params(colors=FG, labelsize=11)
for sp in ax.spines.values(): sp.set_edgecolor(GR)
ax.grid(True, axis="y", color=GR, lw=0.7)
ax.set_title("Regime I — Constructive Merger\n(same helicity)", fontsize=10.5, color=FG)
for bar, v, e in zip(bars, mids_I, err_I):
    ax.text(bar.get_x()+bar.get_width()/2, v+e+2,
            f"{int(v-e)}–{int(v+e)}%", ha="center", color=FG, fontsize=9)
# Régime II
ax2 = axes[1]; ax2.set_facecolor(BG)
ch = ["y/X", "Plasma", "GW", "nu", "X soft"]
micro = [50, 32.5, 3, 10, 5]; macro = [20, 10, 30, 7.5, 10]
merr  = [10, 7.5, 2, 5, 0];   Merr = [10, 5, 10, 2.5, 5]
cols2 = [C_ORA, C_TEAL, C_PUR, C_YEL, C_RED]
x = np.arange(len(ch)); w = 0.35
ax2.bar(x-w/2, micro, w, color=cols2, alpha=0.9, yerr=merr, capsize=4,
        error_kw=dict(color=FG, lw=1.2), label="Micro-Knot")
ax2.bar(x+w/2, macro, w, color=cols2, alpha=0.55, yerr=Merr, capsize=4,
        error_kw=dict(color=FG, lw=1.2), label="Macro-Knot", hatch="///")
ax2.set_xticks(x); ax2.set_xticklabels(ch, fontsize=11, color=FG)
ax2.set_ylim(0, 75); ax2.set_ylabel("Energy fraction [%]", fontsize=11, color=FG)
ax2.tick_params(colors=FG, labelsize=10)
for sp in ax2.spines.values(): sp.set_edgecolor(GR)
ax2.grid(True, axis="y", color=GR, lw=0.7)
ax2.legend(**LEGEND_KW)
ax2.set_title("Regime II — Annihilation\n(opposite helicity)", fontsize=10.5, color=FG)
fig.suptitle("ECF Merger Channel Partition — Appendix D.2", fontsize=12, color=FG, fontweight="bold", y=1.01)
fig.tight_layout()
savefig(fig, "fig_ECF_Channel_Partition.png")

# ═══════════════════════════════════════════════════════════════════════════
# FIG 4 — Knot-Star L_X vs b
# ═══════════════════════════════════════════════════════════════════════════
# Physical model (corrected v2) :
#   M_knot  = 1e5 Msun Macro-Knot
#   v_rel   = 10 km/s  (typical star/Knot relative velocity in galactic halo)
#   R_capt  = G M / v²   [m] → [pc]  ≈ 4.3 pc   (gravitational capture radius)
#   L_Edd   = 1.3e38 erg/s  (Eddington for 1e5 Msun, in CGS)
#   Fly-by  : L_X = L_Edd * (R_capt/b)²              (b > R_capt, tidal)
#   Capture : L_X = L_Edd * 50 * (R_capt/b)^1.5      (b < R_capt, accretion)
#   Merger  : L_X ~ 1e44 erg/s  plateau               (b < R_capt/10, BH)
print("Fig 4 — Knot-Star L_X vs b ...")
b_pc    = np.logspace(-4, 2, 800)
M_knot  = 1e5 * MSUN                          # kg
v_rel   = 10e3                                 # m/s — typical halo encounter velocity
R_capt  = G_SI * M_knot / v_rel**2 / PC_M     # parsecs ≈ 4.3 pc
b_mer   = R_capt / 10.0                        # merger threshold (pc)

L_Edd_cgs = 1.3e31 * 1e7                       # erg/s (W → CGS)

L_fly = L_Edd_cgs * (R_capt / b_pc)**2
L_cap = np.where(b_pc < R_capt,
                 L_Edd_cgs * 50 * (R_capt / b_pc)**1.5,
                 np.nan)
L_mer = np.where(b_pc < b_mer, 1e44 * np.ones_like(b_pc), np.nan)

fig, ax = plt.subplots(figsize=(9, 5.5))
styled_ax(ax, fig)
ax.grid(True, which="minor", color=GR, lw=0.25, alpha=0.4)

ax.loglog(b_pc, L_fly, color=C_TEAL, lw=2,   ls="--",
          label=r"Fly-by (tidal)  $L\propto b^{-2}$")
ax.loglog(b_pc, L_cap, color=C_ORA,  lw=2,   ls="-",
          label=r"Partial capture  $L\propto b^{-3/2}$")
ax.loglog(b_pc, L_mer, color=C_PIN,  lw=2.5, ls="-",
          label=r"Full merger (BH)  $L\sim10^{44}$ erg/s")

ax.axvline(R_capt, color=FG,    lw=1.0, ls=":", alpha=0.8)
ax.axvline(b_mer,  color=C_PIN, lw=0.8, ls=":", alpha=0.7)
ax.text(R_capt*1.15, 2e34, f"$R_{{\\rm capt}}\\approx{R_capt:.1f}$ pc\n"
        r"$(v_{\rm rel}=10$ km/s)", color=FG, fontsize=8.5)
ax.text(b_mer*1.15,  2e34, f"$b_{{\\rm mer}}\\approx{b_mer:.2f}$ pc",
        color=C_PIN, fontsize=8.5)

ax.axhspan(1e38, 1e42, alpha=0.08, color=C_GRN, label="FXT/EP obs. range")
ax.text(5, 3e42, "FXT/EP range", color=C_GRN, fontsize=9)

ax.set_xlim(b_pc[0], b_pc[-1]); ax.set_ylim(1e32, 1e50)
ax.set_xlabel("Impact param.  b  [pc]", fontsize=12)
ax.set_ylabel(r"$L_X$  [erg/s]", fontsize=12)
ax.legend(**LEGEND_KW)
ax.set_title("Knot-Star  $L_X$ vs impact parameter\n3 sub-regimes — Appendix D.2",
             fontsize=11)
savefig(fig, "fig_KnotStar_Lx_vs_b.png")

# FIG 5 — Ringdown tail
# ═══════════════════════════════════════════════════════════════════════════
print("Fig 5 — Ringdown tail ...")
M_tot  = 2e5*MSUN
tau_GR = G_SI*M_tot/C_SI**3
tau_T  = 0.01*PC_M/C_SI
t = np.logspace(np.log10(tau_GR*0.1), np.log10(tau_T*5), 800)
h_GR = np.exp(-t/tau_GR)
h_T  = np.exp(-t/tau_GR) + 0.02*np.exp(-t/tau_T)

fig, ax = plt.subplots(figsize=(9, 5.5))
styled_ax(ax, fig)
ax.grid(True, which="minor", color=GR, lw=0.25, alpha=0.4)
ax.loglog(t, h_GR, color=C_BLUE, lw=2, ls="--", label="Standard BBH ringdown")
ax.loglog(t, h_T,  color=C_PIN,  lw=2.5, label="ECF Knot-Star (torsion tail)")
ax.axvline(tau_GR, color=C_BLUE, lw=0.9, ls=":", alpha=0.8)
ax.text(tau_GR*1.3, 5e-1, "tau_GR~1s", color=C_BLUE, fontsize=9)
ax.axvline(tau_T, color=C_PIN, lw=0.9, ls=":", alpha=0.8)
ax.text(tau_T*1.3, 5e-2, "tau_T~1e6s", color=C_PIN, fontsize=9)
ax.axhspan(1e-3, 1e-2, alpha=0.07, color=C_PUR)
ax.text(tau_T*2, 3e-3, "LISA floor", color=C_PUR, fontsize=8.5)
ax.set_xlim(t[0], t[-1]); ax.set_ylim(1e-4, 2)
ax.set_xlabel("Time  t  [s]", fontsize=12)
ax.set_ylabel("GW amplitude h (norm.)", fontsize=12)
ax.legend(**LEGEND_KW)
ax.set_title("ECF Extended Ringdown: GR vs Torsion tail\nFalsifiable LISA — Appendix D.2", fontsize=11)
savefig(fig, "fig_ECF_Ringdown_Tail.png")

print("\nDone — 5 figures saved to", args.outdir)

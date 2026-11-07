#!/usr/bin/env python3
"""
plot_ECF_falsifiability_timeline.py

Falsifiability timeline for the Einstein-Cartan Framework (Foundation III).
Each ECF prediction is a KILL-SWITCH: an observation that, if it comes out
the "wrong" way, constrains the stated ECF sector or template. Shows WHEN each
# test arrives (2026 onward; schedule-dependent)
and WHICH outcome would constrain which sector.

DESIGN: light background, PRINT-SAFE / grayscale-safe (staged greys + distinct
marker shapes). Two-column layout: timeline + cards on top, logic panel below.

Output: Fig_ECF_Falsifiability_Timeline.png (300 dpi)
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
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch

plt.rcParams.update({
    "font.family": "serif", "font.serif": ["DejaVu Serif"],
    "mathtext.fontset": "dejavuserif", "axes.linewidth": 0.0,
})

BG="#ffffff"; INK="#1a1a1a"; MUTED="#5c5c5c"; FAINT="#b8b8b8"; PANEL="#f4f2ec"
C_NEAR="#8a1c3b"; C_MID="#1f5f8b"; C_FAR="#3a7d34"; C_FAR2="#c07a00"

# (year, date, probe, prediction, kill_condition, color, marker)
rows = [
 (2026.85,"Nov 2026","DESI DR2 (published) / Euclid DR1",
  "calibrated $(w_0,w_a)$: $d_{\\rm Maha}=2.03\\sigma$ (DESI DR1, Planck prior)",
  "agreement with $\\Lambda$CDM at $<1\\sigma$",C_NEAR,"o"),
 (2027.5,"mid-2027","Euclid DR1-Complete / DESI LRG",
  "void-size excess at $R>\\xi_{\\rm KZ}=60\\,$Mpc comoving ($\\times2.1$)",
  "no void excess at $R>\\xi_{\\rm KZ}$ (KZ sector constrained)",C_NEAR,"s"),
 (2028.0,"schedule-dep.","DESI full 5-yr / Rubin LSST",
  "dark-energy direction $w_0>-1,\\ w_a<0$",
  "$w_a>0$ or $w_0<-1$",C_MID,"D"),
 (2035.0,"launch ~2035","LISA",
  "blue GW background $n_T>0$, $\\Pi_{\\rm GW}\\approx0.20\\pm0.05$ (calibrated template)",
  "$n_T\\leq0$ (chiral-GW template constrained)",C_FAR2,"P"),
 (2036.5,"launch JFY2036","LiteBIRD (ISAS/JAXA)",
  "CMB birefringence $\\beta>0.1°$ (chiral $B$-modes)",
  "$\\beta$ consistent with $0$",C_FAR,"^"),
]

fig=plt.figure(figsize=(15,9.4),dpi=300); fig.patch.set_facecolor(BG)
ax=fig.add_axes([0,0,1,1]); ax.set_xlim(0,15); ax.set_ylim(0,9.4); ax.axis("off")

ax.text(7.5,9.0,"How the Einstein-Cartan Framework Can Be Constrained",
        ha="center",va="center",color=INK,fontsize=23,weight="bold")
ax.text(7.5,8.52,"Roadmap of discriminating tests, 2026 onward \u2014 each adverse result constrains the stated sector or template, not the model",
        ha="center",va="center",color=MUTED,fontsize=12,style="italic")

# ---- timeline ----
t0,t1=2025.5,2038.5   # horizon indicatif : les calendriers de mission glissent
def X(y): return 0.9+(y-t0)/(t1-t0)*(14.1-0.9)
yax=7.75
ax.plot([X(t0),X(t1)],[yax,yax],color=INK,lw=2.0,zorder=3,solid_capstyle="round")
ax.add_patch(FancyArrowPatch((X(t1)-0.02,yax),(X(t1)+0.28,yax),
    arrowstyle="-|>",mutation_scale=20,color=INK,lw=2.0,zorder=3))
for yr in [2026,2028,2030,2032,2034,2036]:
    ax.plot([X(yr),X(yr)],[yax-0.10,yax+0.10],color=INK,lw=1.3,zorder=3)
    ax.text(X(yr),yax+0.26,str(yr),ha="center",va="bottom",color=MUTED,fontsize=9.5)
ax.text(X(t1)+0.30,yax+0.28,"year",ha="left",va="bottom",color=MUTED,fontsize=9.5,style="italic")
# markers on timeline
for yr,date,probe,pred,kill,col,mk in rows:
    ax.scatter([X(yr)],[yax],marker=mk,s=95,color=col,edgecolors=INK,linewidths=0.9,zorder=6)

# ---- cards (wide, full width) ----
card_w, card_h = 13.2, 0.92
x_left = 0.9
row_y0 = 6.60
dy = 1.00
for i,(yr,date,probe,pred,kill,col,mk) in enumerate(rows):
    cy=row_y0-i*dy
    # connector timeline -> card
    ax.plot([X(yr),X(yr)],[yax-0.12,cy+card_h/2],color=FAINT,lw=1.0,ls=(0,(2,2)),zorder=2)
    ax.add_patch(FancyBboxPatch((x_left,cy-card_h/2),card_w,card_h,
        boxstyle="round,pad=0.02,rounding_size=0.09",linewidth=1.5,
        edgecolor=col,facecolor=PANEL,zorder=4))
    # left chip: marker + date + probe
    ax.add_patch(FancyBboxPatch((x_left,cy-card_h/2),3.0,card_h,
        boxstyle="round,pad=0.02,rounding_size=0.09",linewidth=0,
        facecolor=col,alpha=0.15,zorder=4.5))
    ax.scatter([x_left+0.34],[cy+0.20],marker=mk,s=68,color=col,edgecolors=INK,linewidths=0.8,zorder=6)
    ax.text(x_left+0.58,cy+0.20,date,ha="left",va="center",color=col,fontsize=10,weight="bold",zorder=6)
    ax.text(x_left+0.20,cy-0.22,probe,ha="left",va="center",color=INK,fontsize=8.8,style="italic",zorder=6)
    # middle: ECF predicts
    ax.text(x_left+3.25,cy+0.20,"ECF predicts",ha="left",va="center",color=C_FAR,fontsize=8.2,weight="bold",zorder=6)
    ax.text(x_left+5.05,cy+0.20,pred,ha="left",va="center",color=INK,fontsize=9.2,zorder=6)
    # bottom: falsified if
    ax.text(x_left+3.25,cy-0.22,"Constrained if",ha="left",va="center",color=C_NEAR,fontsize=8.2,weight="bold",zorder=6)
    ax.text(x_left+5.05,cy-0.22,kill,ha="left",va="center",color=INK,fontsize=9.2,zorder=6)
    # divider between predict / falsify columns
    ax.plot([x_left+4.95,x_left+4.95],[cy-card_h/2+0.12,cy+card_h/2-0.12],color=FAINT,lw=0.7,zorder=5)

# ---- bottom logic strip (four horizontal blocks) ----
strip_y = 1.30
bx0 = 0.9; bw = 13.2
ax.add_patch(FancyBboxPatch((bx0,0.55),bw,1.35,
    boxstyle="round,pad=0.02,rounding_size=0.10",linewidth=1.3,
    edgecolor=MUTED,facecolor="#faf8f2",zorder=3))
ax.text(bx0+0.25,1.68,"Why this matters:",ha="left",va="center",color=INK,fontsize=11,weight="bold",zorder=5)
ax.text(bx0+2.55,1.68,"a theory that forbids nothing explains nothing \u2014 each row states the observation that would constrain the stated sector or template.",
        ha="left",va="center",color=INK,fontsize=9.5,style="italic",zorder=5)
# three phase summaries
phases = [
 (C_NEAR,"2026-27  near-term","growth tension + void excess (DESI, Euclid) \u2014 fastest paths to constrain the stated sectors."),
 (C_MID, "schedule-dep.","sign of $(w_0,w_a)$ from DESI full 5-yr / Rubin LSST discriminates ECF from a cosmological constant."),
 (C_FAR2,"2035-37  smoking gun","parity violation: CMB birefringence (LiteBIRD) + blue chiral GW background (LISA). $n_T\\leq0$ constrains the chiral-GW template."),
]
yy=1.28
for col,head,body in phases:
    ax.add_patch(Circle((bx0+0.32,yy),0.05,color=col,zorder=6))
    ax.text(bx0+0.50,yy,head+":",ha="left",va="center",color=col,fontsize=8.8,weight="bold",zorder=6)
    ax.text(bx0+2.55,yy,body,ha="left",va="center",color=INK,fontsize=8.6,zorder=6)
    yy-=0.30

ax.text(7.5,0.22,
        "Einstein-Cartan Framework  \u00b7  Foundation III  \u00b7  predictions stated with the conditions under which they are constrained (a sector or template, not the whole framework)",
        ha="center",va="center",color=MUTED,fontsize=8.4,style="italic")

fig.savefig("Fig_ECF_Falsifiability_Timeline.png",dpi=300,facecolor=BG,bbox_inches="tight",pad_inches=0.15)
print("Saved.")

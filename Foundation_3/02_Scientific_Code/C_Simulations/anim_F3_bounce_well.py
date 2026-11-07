#!/usr/bin/env python3

# UTF-8 guard: added 24/08/2026 so the script does not
# crash on a Windows cp1252 console.
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

# =============================================================================
#  ECF / Foundation III — Pedagogical animation of the "bounce well"
#  Fichant, P. (2026).   File: anim_F3_bounce_well.py
#  [English translation: 25/08/2026 — all displayed text and comments.]
#
#  LOCATION (GitHub repository spin-torsion-cosmology):
#     Foundation_3/02_Scientific_Code/C_Simulations/anim_F3_bounce_well.py
#  OUTPUTS:
#     Foundation_3/02_Scientific_Code/C_Simulations/output_simulations/
#         anim_F3_bounce_well.mp4   (presentation, talk)
#         anim_F3_bounce_well.gif   (mail, web, README)
# =============================================================================
#
#  PURPOSE
#  -------
#  Animate the central mechanism of the Landau-Ginzburg route: the deformation
#  of the energy landscape V(T) as the Cartan threshold is crossed, and the
#  "fall" of the order parameter (axial torsion) into one of the two valleys --
#  that is, THE CHOICE OF THE CHIRALITY of the universe.
#
#  WHAT SETS THE DEPTH OF THE TWO WELLS?
#  -------------------------------------
#      V(T) = alpha (chi_c - chi) T^2  +  beta T^4  -  h T
#             \______ EVEN _______/   \__ EVEN __/  \__ ODD __/
#
#  The first two terms are EVEN: perfectly symmetric under T -> -T.
#  Only the -h*T term is ODD: it, and it alone, tilts the landscape. It lowers
#  the energy on the side where T carries the sign of h:
#      h > 0 (positive parent spin) -> RIGHT well deeper -> D chirality
#      h < 0                        -> LEFT well deeper  -> L chirality
#      h = 0                        -> STRICTLY equal wells -> RANDOM chirality
#  The whole chiral-selection mechanism rests on this single term.
#
#  WHERE ARE THE MINIMA AND THE MAXIMUM?
#  -------------------------------------
#  They are the three roots of the cubic
#      V'(T) = 4 beta T^3 + 2 alpha (chi_c - chi) T - h = 0
#  At the bounce peak (chi = 1.8, h = +0.02):
#      T = -0.8881  ->  LEFT MINIMUM             (V = -0.3022)
#      T = -0.0125  ->  MAXIMUM (unstable hump)  (V = +0.0001)
#      T = +0.9006  ->  RIGHT MINIMUM            (V = -0.3380)  <-- the deeper one
#  Note that the maximum is NOT exactly at T = 0: it is slightly shifted to the
#  side OPPOSITE to the bias. This is another signature of the asymmetry.
#
#  FIDELITY PRINCIPLE
#  ------------------
#  The RED ball does NOT follow a hand-drawn trajectory: it follows the EXACT
#  NUMERICAL SOLUTION of the equation of motion
#      T'' + 3 H(t) T' + dV/dT = 0
#  integrated here (and by lg_bounce_dynamics.py). The animation IS the result,
#  not an illustration of it.
#
#  WHAT IS NOT SHOWN  (deliberately)
#  ---------------------------------
#  No "child universe", no galaxy, no Einstein-Rosen bridge: these elements are
#  CONJECTURAL, and depicting them would lend them an appearance of established
#  fact. The animation is strictly limited to what is DEMONSTRATED
#  (items LG-1, LG-2, LG-3, LG-5, LG-6).
#
#  Reproducibility: Python >= 3.9; numpy, scipy, matplotlib. Deterministic.
# =============================================================================

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter, PillowWriter
from matplotlib.lines import Line2D
from scipy.integrate import solve_ivp

# --- Sortie portable, rangee dans output_simulations/ ------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR    = os.path.join(SCRIPT_DIR, 'output_simulations')
os.makedirs(OUT_DIR, exist_ok=True)

MAKE_GIF = True

# =============================================================================
#  PHYSIQUE  (identique a lg_bounce_dynamics.py)
# =============================================================================
ALPHA, BETA, CHI_C = 1.0, 0.5, 1.0
CHI_MAX, WIDTH, H_AMP = 1.8, 3.0, 0.35
H_BIAS = 0.02                       # chiral bias h ∝ H (kinetic helicity, NOT a*)

chi_profile    = lambda t: CHI_MAX * np.exp(-t**2 / (2*WIDTH**2))
hubble_profile = lambda t: H_AMP * (t/WIDTH) * np.exp(-t**2 / (2*WIDTH**2))
V     = lambda T, chi, h: ALPHA*(CHI_C-chi)*T**2 + BETA*T**4 - h*T
dVdT  = lambda T, chi, h: 2*ALPHA*(CHI_C-chi)*T + 4*BETA*T**3 - h

def rhs(t, y, h):
    T, Td = y
    return [Td, -3*hubble_profile(t)*Td - dVdT(T, chi_profile(t), h)]

def critical_points(chi, h):
    """Les 3 racines de V'(T)=0 : (min gauche, maximum, min droit)."""
    r = np.roots([4*BETA, 0.0, 2*ALPHA*(CHI_C - chi), -h])
    r = np.sort(np.real(r[np.abs(np.imag(r)) < 1e-9]))
    return tuple(r) if len(r) == 3 else None

# --- Exact trajectory, TIGHTENED, with a FREEZE FRAME at the moment of choice
#  Pacing: the essential part unfolds between t = -3 and t = +5. We therefore
#  sample that window finely, and the rest coarsely (silent approach, late
#  oscillations). Target duration: ~9 s at 20 fps.
T_SPAN = (-6.5, 9.5)
FPS    = 24
#  End at t = 9.5: torsion is POSITIVE there, consistent with h > 0. (Ending
#  on a negative phase of the damping oscillation would be misleading.)

t_intro = np.linspace(T_SPAN[0], -3.4, 16)     # approche : rapide
t_act   = np.linspace(-3.4,  4.6, 105)         # l'action : au ralenti
t_fin   = np.linspace(4.6,  T_SPAN[1], 22)     # oscillations : condensees
t_core  = np.unique(np.concatenate([t_intro, t_act, t_fin]))

sol = solve_ivp(rhs, T_SPAN, [1e-3, 0.0], args=(H_BIAS,),
                t_eval=t_core, rtol=1e-9, atol=1e-12)

i_choice = int(np.argmax(np.abs(sol.y[0]) > 0.45))   # instant du basculement
PAUSE_FRAMES = 20                                    # ~0.8 s annotated freeze
order = (list(range(i_choice)) + [i_choice]*PAUSE_FRAMES
         + list(range(i_choice, len(t_core))))
t_arr, T_arr = sol.t[order], sol.y[0][order]
is_pause = np.array([False]*i_choice + [True]*PAUSE_FRAMES
                    + [False]*(len(t_core) - i_choice))
chi_arr, H_arr = chi_profile(t_arr), hubble_profile(t_arr)

#  Chirality is LOCKED during the super-critical window: it is the sign
#  acquired in the double well. Late oscillations (chi < 1) make T oscillate
#  about a small equilibrium of sign h, sometimes crossing zero -- displaying
#  the INSTANTANEOUS sign would then be misleading. We therefore store the
#  locked sign, established at the bottom of the well.
_sc = chi_arr > CHI_C
LOCKED_SIGN = np.sign(T_arr[_sc][np.argmax(np.abs(T_arr[_sc]))]) if _sc.any() else 0.0
LOCKED_TXT  = "RIGHT (+)" if LOCKED_SIGN > 0 else "LEFT (-)"

print(f"Trajectory: {len(t_arr)} frames (incl. {PAUSE_FRAMES} freeze) "
      f"-> {len(t_arr)/FPS:.1f} s a {FPS} fps")
print(f"T_final = {T_arr[-1]:+.4f}  ->  chirality "
      f"{'RIGHT (D)' if T_arr[-1] > 0 else 'LEFT (L)'}")
cp0 = critical_points(CHI_MAX, H_BIAS)
print(f"At the bounce peak: min_L = {cp0[0]:+.4f} | max = {cp0[1]:+.4f} "
      f"| min_R = {cp0[2]:+.4f}")

# =============================================================================
#  FIGURE
# =============================================================================
fig, (axV, axT) = plt.subplots(2, 1, figsize=(9.2, 8.6),
                               height_ratios=[2.3, 1.0],
                               gridspec_kw=dict(hspace=0.38))
fig.patch.set_facecolor('white')
Tgrid = np.linspace(-1.7, 1.7, 500)
RED, BLUE = '#c0392b', '#5b7fa6'

# --- Panneau haut : le paysage d'energie ------------------------------------
axV.set_facecolor('white')
(curve,) = axV.plot([], [], '-', color='0.15', lw=2.4, zorder=3)
(trail,) = axV.plot([], [], '-', color=RED, lw=1.3, alpha=0.35, zorder=4)
(ball,)  = axV.plot([], [], 'o', color=RED, ms=15, mec='0.15', mew=1.4, zorder=8)
(mL,)    = axV.plot([], [], 'v', color=BLUE, ms=9, mfc='white', mew=1.3, zorder=6)
(mR,)    = axV.plot([], [], 'v', color=RED,  ms=9, mfc='white', mew=1.3, zorder=6)
(mMax,)  = axV.plot([], [], '^', color='0.45', ms=8, mfc='white', mew=1.1, zorder=6)
axV.axvline(0, color='0.88', lw=0.8, zorder=1)
axV.axhline(0, color='0.88', lw=0.8, zorder=1)

lblDeep = axV.text(0, 0, '', fontsize=9, color=RED, ha='center', va='top',
                   zorder=7, weight='bold')
lblMax  = axV.text(0, 0, '', fontsize=8.5, color='0.4', ha='center', va='bottom',
                   zorder=7)

axV.set_xlim(-1.7, 1.7); axV.set_ylim(-0.85, 1.45)
axV.set_xlabel(r"axial torsion  $\mathcal{T}$   "
               r"$\longleftarrow$ L chirality      D chirality $\longrightarrow$",
               fontsize=10.5)
axV.set_ylabel(r"energy  $V(\mathcal{T})$", fontsize=11)
axV.grid(alpha=0.18, lw=0.5)

# Legend: what is the red ball?
axV.legend(handles=[
    Line2D([], [], marker='o', color='w', mfc=RED, mec='0.15', ms=10,
           label=r"torsion $\mathcal{T}(t)$ — exact solution"),
    Line2D([], [], marker='v', color='w', mfc='white', mec=RED, ms=9,
           label="minima: the 2 chiralities"),
    Line2D([], [], marker='^', color='w', mfc='white', mec='0.45', ms=9,
           label="maximum: unstable"),
], loc='upper left', bbox_to_anchor=(0.0, 0.90), fontsize=8.5, framealpha=0.95)

phase_txt = axV.text(0.5, 1.06, '', transform=axV.transAxes, ha='center',
                     fontsize=12.5, weight='bold')
info_txt  = axV.text(0.018, 0.99, '', transform=axV.transAxes, va='top',
                     fontsize=8.8, family='monospace',
                     bbox=dict(fc='white', ec='0.8', alpha=0.93, pad=4))
note_txt  = axV.text(0.5, 0.025, '', transform=axV.transAxes, ha='center',
                     fontsize=9.5, style='italic', color='0.3')

# --- INSET, placed TOP RIGHT (no longer overlaps the trajectory) ------------
axZ = axV.inset_axes([0.745, 0.615, 0.235, 0.335])
axZ.set_facecolor('#fcfcfc')
(barL,) = axZ.plot([], [], 's', color=BLUE, ms=10, mec='0.2', mew=0.8)
(barR,) = axZ.plot([], [], 's', color=RED,  ms=10, mec='0.2', mew=0.8)
(lnL,)  = axZ.plot([], [], '-', color=BLUE, lw=1.6)
(lnR,)  = axZ.plot([], [], '-', color=RED,  lw=1.6)
axZ.set_xlim(-0.7, 0.7); axZ.set_xticks([-0.33, 0.33])
axZ.set_xticklabels(['L', 'D'], fontsize=9)
axZ.tick_params(axis='y', labelsize=6.5)
axZ.set_title("well depth", fontsize=8.5, pad=3)
zoom_txt = axZ.text(0.5, 0.05, '', transform=axZ.transAxes, ha='center',
                    fontsize=8, color='0.25', weight='bold')
axZ.grid(alpha=0.2, lw=0.4)

# --- Panneau bas : la criticite ---------------------------------------------
axT.set_facecolor('white')
axT.plot(t_core, chi_profile(t_core), '-', color='0.35', lw=1.7, zorder=2)
axT.axhline(CHI_C, color=RED, ls=':', lw=1.4, zorder=2)
axT.fill_between(t_core, 0, 2.0, where=chi_profile(t_core) > CHI_C,
                 color='#f7dcd7', alpha=0.8, zorder=0)
axT.text(0.0, 1.92, 'super-critical window', ha='center', va='top',
         fontsize=9, color='#8e2f22')
axT.text(T_SPAN[1]-0.3, CHI_C+0.08, r'$\chi_c=1$  (Cartan threshold)',
         ha='right', fontsize=9, color=RED)
(cursor,) = axT.plot([], [], 'o', color=RED, ms=8, zorder=5)
(vline,)  = axT.plot([], [], '-', color=RED, lw=1.0, alpha=0.5, zorder=4)
axT.set_xlim(*T_SPAN); axT.set_ylim(0, 2.0)
axT.set_xlabel(r"time  $t$   (Planck units)", fontsize=10.5)
axT.set_ylabel(r"$\chi=\rho/\rho_c$", fontsize=11)
axT.grid(alpha=0.18, lw=0.5)

fig.suptitle("The bounce well: how the universe chooses its chirality",
             fontsize=13.5, weight='bold', y=0.975)
fig.text(0.5, 0.006,
         r"Only the odd term $-h\,\mathcal{T}$ tilts the landscape: it deepens the well "
         r"on the side of $h\propto\mathcal{H}$ (kinetic helicity, not simple rotation) — "
         r"without it, both wells would be equal, and chirality would be drawn at random.",
         ha='center', fontsize=8.5, color='0.45')

TRAIL = 45

def update(i):
    t, T, chi, Hh, paused = t_arr[i], T_arr[i], chi_arr[i], H_arr[i], is_pause[i]

    curve.set_data(Tgrid, V(Tgrid, chi, H_BIAS))
    ball.set_data([T], [V(T, chi, H_BIAS)])
    j = max(0, i - TRAIL)
    trail.set_data(T_arr[j:i+1], V(T_arr[j:i+1], chi_arr[j:i+1], H_BIAS))

    cp = critical_points(chi, H_BIAS) if chi > CHI_C else None
    if cp:
        TL, TM, TR = cp
        VL, VM, VR = (V(x, chi, H_BIAS) for x in cp)
        mL.set_data([TL], [VL]); mR.set_data([TR], [VR]); mMax.set_data([TM], [VM])

        deep_R = VR < VL
        Td, Vd = (TR, VR) if deep_R else (TL, VL)
        lblDeep.set_position((Td, Vd - 0.055))
        lblDeep.set_text("DEEPER WELL")
        lblDeep.set_color(RED if deep_R else BLUE)
        lblMax.set_position((TM, VM + 0.06)); lblMax.set_text("unstable")

        barL.set_data([-0.33], [VL]); barR.set_data([0.33], [VR])
        lnL.set_data([-0.33, -0.33], [0, VL]); lnR.set_data([0.33, 0.33], [0, VR])
        lo = min(VL, VR)*1.45 - 0.02
        axZ.set_ylim(lo, max(0.02, -lo*0.13))
        gain = abs((VR - VL)/VL)*100 if VL else 0.0
        zoom_txt.set_text(f"{'D' if deep_R else 'L'} deeper by {gain:.0f} %")
    else:
        for a in (mL, mR, mMax, barL, barR, lnL, lnR):
            a.set_data([], [])
        for a in (lblDeep, lblMax, zoom_txt):
            a.set_text('')

    if paused:
        phase = "||   THE CHOICE  —  torsion tips to the right"
        note  = ("both wells look identical... but the right one is deeper: "
                 "the bias $h\\propto\\mathcal{H}$ (helicity) is what settles it")
        phase_txt.set_color(RED)
    elif chi < CHI_C and t < 0:
        phase, note = "1 — Sub-critical: a single valley", \
                      "torsion rests at zero"
        phase_txt.set_color('0.25')
    elif chi > CHI_C and t < 0:
        phase, note = "2 — The threshold is crossed: the double well opens", \
                      "$\\mathcal{T}=0$ becomes unstable — a choice must be made"
        phase_txt.set_color(RED)
    elif chi > CHI_C and t < 1.6:
        phase, note = "3 — The fall: the universe picks its hand", \
                      "the bias $h\\propto\\mathcal{H}$ (helicity) tilts the landscape"
        phase_txt.set_color(RED)
    elif chi > CHI_C:
        phase, note = "4 — Oscillations: nothing damps them ($H\\approx0$)", \
                      "chirality is already locked in"
        phase_txt.set_color('#b9770e')
    else:
        phase, note = "5 — The well closes again — chirality remains", \
                      "sign acquired: preserved"
        phase_txt.set_color('0.25')

    phase_txt.set_text(phase); note_txt.set_text(note)
    if chi > CHI_C:                       # in the double well: current sign
        chir = "-" if abs(T) < 0.02 else ("RIGHT (+)" if T > 0 else "LEFT (-)")
    elif t > 0:                           # well closed again: chirality LOCKED
        chir = LOCKED_TXT + "  [verrouillee]"
    else:                                 # avant le seuil : rien de decide
        chir = "-"
    info_txt.set_text(f"t   = {t:+6.2f}\nchi = {chi:5.3f}\nH   = {Hh:+6.3f}\n"
                      f"T   = {T:+6.3f}\nchirality: {chir}")
    cursor.set_data([t], [chi]); vline.set_data([t, t], [0, chi])

    return (curve, ball, trail, mL, mR, mMax, cursor, vline, phase_txt,
            info_txt, note_txt, barL, barR, lnL, lnR, zoom_txt, lblDeep, lblMax)

anim = FuncAnimation(fig, update, frames=len(t_arr), interval=55, blit=False)

mp4 = os.path.join(OUT_DIR, 'anim_F3_bounce_well.mp4')
anim.save(mp4, writer=FFMpegWriter(fps=FPS, bitrate=2800), dpi=110)
print(f"MP4 written: {mp4}")

if MAKE_GIF:
    gif = os.path.join(OUT_DIR, 'anim_F3_bounce_well.gif')
    anim.save(gif, writer=PillowWriter(fps=FPS), dpi=70)
    print(f"GIF written: {gif}")

plt.close(fig)
print("\nReminder: this animation shows ONLY what is demonstrated.\n"
      "No child universe is depicted -- that aspect remains conjectural.")

# ⚠️ SUPERSEDED 15/09/2026 -- do not run.
#
# This Plotly version writes the same file as plot_gamma_macro_z_mpl.py:
# Fig_Gamma_macro_z.png. Whichever runs last silently overwrites the other --
# the exact defect that cost a fortnight on the DESI MCMC figures.
#
# The matplotlib version is authoritative: Plotly image export needs Chrome,
# absent from the reproduction environment, so this script cannot produce the
# figure at all there. Kept, not deleted: its parameter values document what
# the figure looked like before the 13/09 correction (N_macro 1e3 -> O(1)).
#
# Found by check_figure_freshness.py, written by the test bench on 15/09.

"""
ECF Foundation II - Figure Appendix D
Macro-Knot collision rate Γ_macro(z) = Γ0 × (1+z)^(3/2)
+ Galactic-centre concentration effect
Pascal Fichant 2026
"""
# [AJOUTE 15/09/2026] Garde UTF-8. Sans lui, un print contenant un caractere
# non-ASCII (fleche, etoile, accent) fait planter le script sur une console
# Windows en cp1252 : UnicodeEncodeError, code de sortie 1. Quatre scripts F2
# ont echoue ainsi chez Pascal le 15/09 alors qu'ils tournaient sous Linux.
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np
import plotly.graph_objects as go
import json

# ── Physical constants ───────────────────────────────────────────────────────
G    = 6.674e-11
c    = 3e8
Msun = 1.989e30
kpc  = 3.086e19
yr   = 3.156e7
Gyr  = yr * 1e9

# ── Macro-Knot parameters (F2, App. D) ──────────────────────────────────
M_macro          = 1e5 * Msun      # kg
v_galaxy         = 300e3           # m/s
N_macro_MW       = 1.0             # per halo -- CORRECTED 13/09/2026:
                                   # was 1e3, inconsistent with the working
                                   # assumption of F2, O(1) per galactic volume
                                   # (f_macro ~ 1e-7 to 1e-6 is the matching mass
                                   # ratio, not a derivation; 17/10/2026).
R_halo           = 30 * kpc
V_halo           = (4/3) * np.pi * R_halo**3
n_macro_halo     = N_macro_MW / V_halo
sigma_grav_macro = np.pi * (2*G*M_macro/v_galaxy**2)**2
Gamma_macro_0    = n_macro_halo * sigma_grav_macro * v_galaxy   # field halo, today

# Galactic centre: density ~1000x higher, velocity ~3x higher
n_macro_GC       = 1000 * n_macro_halo
v_GC             = 3 * v_galaxy
sigma_grav_GC    = np.pi * (2*G*M_macro/v_GC**2)**2
Gamma_macro_GC_0 = n_macro_GC * sigma_grav_GC * v_GC

z = np.logspace(0, 13, 600)
gamma_macro_halo = Gamma_macro_0    * (1+z)**1.5
gamma_macro_GC   = Gamma_macro_GC_0 * (1+z)**1.5

# ── Plot ─────────────────────────────────────────────────────────────────────
fig = go.Figure()

# Halo curve
fig.add_trace(go.Scatter(
    x=z, y=gamma_macro_halo,
    mode='lines',
    name='Macro-Knots (halo field)',
    line=dict(color='#2E86C1', width=3),
    fill='tozeroy', fillcolor='rgba(46,134,193,0.06)',
    hovertemplate='z = %{x:.2e}<br>Γ_halo = %{y:.2e} s⁻¹<extra></extra>'
))

# Galactic centre curve
fig.add_trace(go.Scatter(
    x=z, y=gamma_macro_GC,
    mode='lines',
    name='Macro-Knots (galactic centre)',
    line=dict(color='#8E44AD', width=2.5, dash='dash'),
    hovertemplate='z = %{x:.2e}<br>Γ_GC = %{y:.2e} s⁻¹<extra></extra>'
))

# Vertical markers
# CORRECTED 13/09/2026: all three labels sat at y=1e-20 and crossed the curve
# after renormalisation (N_macro 1e3 -> 1). They are now spread vertically,
# below the curve at each point.
for zv, label, y_lab in [
    (1e12,  "QGP freeze-out<br>(Macro-Knot crystallisation)", 1e-18),
    (1100,  "Recombination",                                   1e-27),
    # CORRECTED 13/09/2026: was z=10 (~470 Myr), predating the JWST record
    # already cited in F2 (Naidu et al., z_spec = 14.44 -> 280 Myr).
    (14.44, "Earliest confirmed galaxy<br>(JWST, z = 14.44)",    1e-31),
]:
    fig.add_vline(x=zv, line_dash='dot', line_color='#bbb', line_width=1.5)
    fig.add_annotation(
        x=np.log10(zv), xref='x',
        y=y_lab, yref='y',
        text=label, showarrow=False, xanchor='right',
        font=dict(size=9.5, color='#666'),
        bgcolor='rgba(255,255,255,0.85)', borderpad=3
    )

# "Rapid coagulation zone" at QGP
# CORRECTED 13/09/2026: the band ran from 1e-6 to 1e3, anchored on the old
# normalisation. After correction the curve peaks near 1e-9, so the band is
# re-anchored on the range actually spanned, and its label moved left so it no
# longer overlaps the "1 merger / Hubble time" label.
fig.add_hrect(y0=1e-14, y1=1e-8,
              x0=np.log10(1e11), x1=np.log10(1e13),
              fillcolor='rgba(231,76,60,0.06)', line_width=0,
              annotation_text="Rapid Micro-Knot coagulation zone",
              annotation_position="top left",
              annotation_font=dict(size=9, color='#C0392B'))

# 1 merger / Hubble time line
fig.add_hline(y=1/(13.8e9*yr), line_dash='dash', line_color='#27AE60', line_width=1.5,
              annotation_text='1 merger / Hubble time',
              annotation_position='bottom right',   # CORRECTED 13/09/2026: was 'top right',
              annotation_font=dict(size=9, color='#27AE60'))

fig.update_xaxes(
    type='log', title_text='Redshift  z',
    showgrid=True, gridcolor='#f0f0f0'
)
fig.update_yaxes(
    type='log', title_text='Γ_macro  [s⁻¹]',
    showgrid=True, gridcolor='#f0f0f0'
)
fig.update_layout(
    title=dict(
        text="Macro-Knot collision rate Γ(z) — field halo vs galactic centre — ECF F2"
             "<br><span style='font-size:13px;font-weight:normal'>"
             "Γ(z) = Γ₀(1+z)^(3/2) | σ_grav = π(2GM/v²)² | N_macro ~ O(1)/halo</span>",
        x=0.5, font=dict(size=15)
    ),
    plot_bgcolor='white', paper_bgcolor='white',
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5),
    margin=dict(l=70, r=30, t=120, b=60)
)

fig.write_image("Fig_Gamma_macro_z.png", scale=2)
with open("Fig_Gamma_macro_z.png.meta.json","w") as f:
    json.dump({
        "caption": "Macro-Knot collision rate Γ_macro(z) — field halo vs galactic centre — ECF Foundation II",
        "description": "Log-log evolution of Macro-Knot collision rate, comparing halo field and galactic centre (density ×1000) from today to QGP freeze-out. Rapid coagulation zone highlighted."
    }, f)
print("✅ Fig_Gamma_macro_z.png saved")

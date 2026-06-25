"""
ECF Foundation II v19 - Figure Appendix D
Macro-Knot collision rate Γ_macro(z) = Γ0 × (1+z)^(3/2)
+ Galactic-centre concentration effect
Pascal Fichant 2026
"""
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
N_macro_MW       = 1e3             # per halo
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
for zv, label in [
    (1e12,  "QGP freeze-out<br>(Macro-Knot crystallisation)"),
    (1100,  "Recombination"),
    (10,    "First galaxies"),
]:
    fig.add_vline(x=zv, line_dash='dot', line_color='#bbb', line_width=1.5)
    fig.add_annotation(
        x=np.log10(zv), xref='x',
        y=1e-20, yref='y',
        text=label, showarrow=False, xanchor='right',
        font=dict(size=9.5, color='#666'),
        bgcolor='rgba(255,255,255,0.85)', borderpad=3
    )

# "Rapid coagulation zone" at QGP
fig.add_hrect(y0=1e-6, y1=1e3,
              x0=np.log10(1e11), x1=np.log10(1e13),
              fillcolor='rgba(231,76,60,0.06)', line_width=0,
              annotation_text="Rapid coagulation zone<br>(bimodal mass spectrum origin)",
              annotation_position="top right",
              annotation_font=dict(size=9, color='#C0392B'))

# 1 merger / Hubble time line
fig.add_hline(y=1/(13.8e9*yr), line_dash='dash', line_color='#27AE60', line_width=1.5,
              annotation_text='1 merger / Hubble time',
              annotation_position='top right',
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
             "Γ(z) = Γ₀(1+z)^(3/2) | σ_grav = π(2GM/v²)² | N_macro ~ 10³/halo</span>",
        x=0.5, font=dict(size=15)
    ),
    plot_bgcolor='white', paper_bgcolor='white',
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5),
    margin=dict(l=70, r=30, t=120, b=60)
)

fig.write_image("Fig_Gamma_macro_z.png", scale=2)
with open("Fig_Gamma_macro_z.png.meta.json","w") as f:
    json.dump({
        "caption": "Macro-Knot collision rate Γ_macro(z) — field halo vs galactic centre — ECF F2 v19",
        "description": "Log-log evolution of Macro-Knot collision rate, comparing halo field and galactic centre (density ×1000) from today to QGP freeze-out. Rapid coagulation zone highlighted."
    }, f)
print("✅ Fig_Gamma_macro_z.png saved")

"""
ECF Foundation II - Figure Appendix D
Micro-Knot collision rate Γ_micro(z) = Γ0 × (1+z)^(3/2)
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
G   = 6.674e-11    # m³ kg⁻¹ s⁻²
c   = 3e8          # m/s
yr  = 3.156e7      # s

# ── Micro-Knot parameters (F2, App. D) ──────────────────────────────────
# [27/08/2026] Was 1e24 kg, the lower edge of the KZ window. The horizon
# mass at T_c = 159 GeV is 3.74e24 kg (calculate_microknot_mass.py).
M_micro          = 3.74e24       # kg  (planetary mass, +/- 0.05e24)
v_halo           = 200e3         # m/s (halo velocity dispersion)
# [15/10/2026] Unit fixed: 0.4 GeV/cm^3 = 0.4 * 1.783e-27 kg per cm^3 = 7.13e-22 kg/m^3.
# The former line (0.4 * 1.78e-27, read as kg/m^3) was 1e6 too low, and so was the whole curve.
rho_DM_local     = 0.4 * 1.783e-27 * 1e6  # kg/m³ (0.4 GeV/cm³)
n_micro          = rho_DM_local / M_micro
sigma_grav_micro = np.pi * (2*G*M_micro/v_halo**2)**2
Gamma_micro_0    = n_micro * sigma_grav_micro * v_halo  # today

z = np.logspace(0, 15, 600)
gamma_micro = Gamma_micro_0 * (1+z)**1.5

# ── Events of interest ─────────────────────────────────────────────────────
epochs = {
    # [27/08/2026] Was 1.5e11, which corresponds to T ~ 35 MeV -- neither
    # the electroweak transition nor any other ECF epoch. The electroweak
    # transition (T_c = 159 GeV) sits at z = 2.0e15 (build_ecf_timeline.py).
    "z_EW":   2.03e15,
    "z_rec":  1100,
    "z_today": 0,
}

# ── Plot ─────────────────────────────────────────────────────────────────────
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=z, y=gamma_micro,
    mode='lines',
    name='Micro-Knots',
    line=dict(color='#C0392B', width=3),
    fill='tozeroy', fillcolor='rgba(192,57,43,0.07)',
    hovertemplate='z = %{x:.2e}<br>Γ = %{y:.2e} s⁻¹<extra></extra>'
))

# Vertical markers
for zv, label, ypos in [
    (2.03e15, "EW transition<br>(Micro-Knot crystallisation)", 1e-14),
    (1.51e12, "QCD / QGP-hadron", 1e-20),
    (3.04e09, "Great Annihilation<br>(Macro-Knot scale)", 1e-26),
    (1100,   "Recombination", 1e-33),
]:
    fig.add_vline(x=zv, line_dash='dot', line_color='#aaa', line_width=1.5)
    fig.add_annotation(
        x=np.log10(zv), xref='x', y=ypos, yref='y',
        text=label, showarrow=False, xanchor='right',
        font=dict(size=10, color='#666'),
        bgcolor='rgba(255,255,255,0.85)', borderpad=3
    )

# [27/08/2026] The '1 encounter / 300 s' marker was removed. Gamma = 1/300
# s^-1 is not reached anywhere on this curve, and the accompanying text in
# F2 read a rate of 1e-16 s^-1 as 'one encounter every ~300 s' -- its inverse
# is 1e16 s, three hundred million years. A reference line that no point of
# the curve approaches is a line that invites the reader to misread it.
fig.add_hline(y=1.0/yr, line_dash='dash', line_color='#E67E22', line_width=1.5,
)
# [15/10/2026] Label placed explicitly at the line (log axis: y given as log10);
# the automatic hline label sat at the top of the frame, over the EW label.
fig.add_annotation(x=np.log10(30), xref='x', y=np.log10(1.0/yr), yref='y',
                   text='1 encounter / year', showarrow=False, yanchor='bottom',
                   font=dict(size=10, color='#E67E22'))

fig.update_xaxes(
    type='log', title_text='Redshift  z',
    showgrid=True, gridcolor='#f0f0f0'
)
fig.update_yaxes(
    type='log', title_text='Γ_micro  [s⁻¹]',
    showgrid=True, gridcolor='#f0f0f0'
)
fig.update_layout(
    title=dict(
        text="Micro-Knot collision rate Γ(z) — ECF F2"
             "<br><span style='font-size:13px;font-weight:normal'>"
             "Γ(z) = Γ₀(1+z)^(3/2) | σ_grav = π(2GM/v²)² | n_µ = ρ_DM/M_µ</span>",
        x=0.5, font=dict(size=16)
    ),
    plot_bgcolor='white', paper_bgcolor='white',
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5),
    margin=dict(l=70, r=30, t=110, b=60)
)

fig.write_image("Fig_Gamma_micro_z.png", scale=2)
with open("Fig_Gamma_micro_z.png.meta.json","w") as f:
    json.dump({
        "caption": "Micro-Knot collision rate Γ_micro(z) — ECF F2",
        "description": "Log-log evolution of Micro-Knot collision rate from today (z=0) to EW freeze-out."
    }, f)
print("✅ Fig_Gamma_micro_z.png saved")

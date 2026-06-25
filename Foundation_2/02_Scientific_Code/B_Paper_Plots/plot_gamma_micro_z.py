"""
ECF Foundation II v19 - Figure Appendix D
Micro-Knot collision rate Γ_micro(z) = Γ0 × (1+z)^(3/2)
Pascal Fichant 2026
"""
import numpy as np
import plotly.graph_objects as go
import json

# ── Physical constants ───────────────────────────────────────────────────────
G   = 6.674e-11    # m³ kg⁻¹ s⁻²
c   = 3e8          # m/s
yr  = 3.156e7      # s

# ── Micro-Knot parameters (F2, App. D) ──────────────────────────────────
M_micro          = 1e24          # kg  (planetary mass)
v_halo           = 200e3         # m/s (halo velocity dispersion)
rho_DM_local     = 0.4 * 1.78e-27  # kg/m³ (0.4 GeV/cm³)
n_micro          = rho_DM_local / M_micro
sigma_grav_micro = np.pi * (2*G*M_micro/v_halo**2)**2
Gamma_micro_0    = n_micro * sigma_grav_micro * v_halo  # today

z = np.logspace(0, 15, 600)
gamma_micro = Gamma_micro_0 * (1+z)**1.5

# ── Events of interest ─────────────────────────────────────────────────────
epochs = {
    "z_EW":   1.5e11,
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
    (1.5e11, "EW freeze-out<br>(Micro-Knot crystallisation)", 1e-14),
    (1100,   "Recombination", 1e-33),
]:
    fig.add_vline(x=zv, line_dash='dot', line_color='#aaa', line_width=1.5)
    fig.add_annotation(
        x=np.log10(zv), xref='x', y=ypos, yref='y',
        text=label, showarrow=False, xanchor='right',
        font=dict(size=10, color='#666'),
        bgcolor='rgba(255,255,255,0.85)', borderpad=3
    )

# Highlight "1 encounter/300 s" zone
fig.add_hline(y=1/300, line_dash='dash', line_color='#E67E22', line_width=1.5,
              annotation_text='1 encounter / 300 s', annotation_position='top right',
              annotation_font=dict(size=9, color='#E67E22'))

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

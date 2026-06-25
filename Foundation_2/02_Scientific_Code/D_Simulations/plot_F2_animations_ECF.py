#!/usr/bin/env python3
"""
plot_F2_animations_ECF.py
==========================
Foundation II — F2 PREPRINT v2 (work in progress)
Zenodo PREPRINT v1: doi:10.5281/zenodo.20629238

PURPOSE
-------
Four pedagogical GIF animations illustrating the gas dynamics around
each class of ECF topological defect. Intended for:
  - Supplementary material to Foundation II (journal submission)
  - Conference/seminar presentations
  - NotebookLM / educational context

OUTPUT FILES
------------
  Anim_ECF_0D_MicroKnot.gif    — gravitational lensing & halo accretion
  Anim_ECF_1D_TorsionString.gif — gas velocity kick & baryonic wake
  Anim_ECF_2D_ChiralWall.gif   — Israel repulsion & void formation
  Anim_ECF_3D_TorsionFluid.gif  — spatial back-reaction & w(z) evolution

PHYSICAL MODEL SUMMARY
-----------------------
All four defects share the same primordial origin: Kibble-Zurek (KZ)
crystallisation at T ~ 150 GeV, coupling constant kappa^2 = 2.0766e-43 m/J.

0D Micro-Knot (pi_2):
  - Hedgehog point defect, M = 6e24 kg = c^3 / (G * H_EW)
  - Gravitational effect: Schwarzschild lensing, no Hawking evaporation
    (T_H = 2.7 mK << T_CMB), t_evap > 1e83 yr
  - Interaction: same helicity -> coagulate; opposite -> annihilate (PO-F2-1)
  - Kill-switch: Roman (2028) tau_micro >= 1e-7, t_E ~ 0.5 h

1D Torsion String (pi_1):
  - Line defect, mu_1D ~ 1e14 kg/m = eta_EW^2 / (hbar c^3)
  - Gravitational effect: conical deficit delta = 8*pi*G*mu/c^2 ~ 1e-6 rad
    NO Newtonian 1/r^2 — only velocity kick delta_v = 4*pi*G*mu*v_s*gamma_s
  - Helical J_5 current (ECF-specific; absent in GUT strings)
  - Interaction: reconnects (never merges with 0D)
  - Kill-switch: LISA (2037) GW burst f ~ 50 mHz, torsion tail tau_T ~ 1e6 s
  - Visualisation: gas colour-coded by distance to string (coolwarm_r)

2D Chiral Wall (pi_0):
  - Surface defect, sigma_2D ~ 1e49 kg/m^2, delta_w ~ 1e-18 m
  - Gravitational effect: Israel (1966) perpendicular repulsion
    z_ddot = (8*pi*G*sigma_2D/3) * z  ->  z(t) ~ exp(sqrt(8*pi*G*sigma/3)*t)
  - Birefringence: Delta_theta = beta_ECF = 0.35 deg (achromatic)
  - Dual void mechanism:
      (1) Chiral Wall -> sharp boundary (local, perpendicular)
      (2) 3D Torsion Fluid -> sustains expansion (global, isotropic)
  - Kill-switch: LiteBIRD (2032) beta < 0.1 deg at 3-sigma

3D Torsion Fluid (no pi_k):
  - NOT a topological defect; volume-filling geometric condensate
  - f_fluid ~ 0.73 (KZ residue, not derived from first principles: PO-F2-4)
  - P_tors = -(1/4)*kappa^2*<S^2>_vol ~ -2e-82 Pa
  - w(z) = w0 + wa*(1-a) = -0.904 - 0.153*(1-a)  [PIT calibration, pre-DESI]
  - Spatial modulation: DEPLETED in halos (0D knots dominate locally),
                        AMPLIFIED in voids (Omega_m -> 0)
  - Geometric back-reaction: DM <-> DE coupled via halo/void contrast
  - Kill-switch: DESI DR3 (2027) w = -1 at 5-sigma

OPEN PROBLEMS (documented, not hidden)
---------------------------------------
  PO-F2-1: Origin of topological surplus DeltaN > 0 (link DeltaN/eta not derived)
  PO-F2-2: Helical pitch lambda_hel of Torsion Strings (not derived from ECF action)
  PO-F2-3: Chiral Wall network dilution rate and GW background
  PO-F2-4: Partition f_fluid not derived from eta_EW first principles

ANIMATION PARAMETERS
---------------------
  N_FRAMES = 80       number of frames per animation
  FPS      = 18       playback speed (frames per second)
  DPI      = 120      output resolution (web/presentation quality)
  Duration ~ 4.5 s per loop (GIF loops indefinitely)

DEPENDENCIES
------------
  numpy >= 1.24
  matplotlib >= 3.7  (includes Pillow writer for GIF export)
  Standard library: os

Install: pip install numpy matplotlib

USAGE
-----
  python plot_F2_animations_ECF.py
  # Generates 4 GIF files in figures_output/ (auto-detected)

OUTPUT PATH RESOLUTION
-----------------------
  The script searches up to 6 directory levels for a figures_output/
  folder. If not found, it creates one next to the script.
  Standard location: Foundation_2/02_Scientific_Code/simulations_output/

CANONICAL PARAMETERS (Foundation II, not fit to data)
-------------------------------------------------------
  kappa^2      = 2.0766e-43  m/J          [8*pi*G/c^4, CODATA 2018]
  w0           = -0.904                    [PIT geometric derivation]
  wa           = -0.153                    [PIT geometric derivation]
  M_micro      = 6e24 kg = c^3/(G*H_EW)   [T_EW = 150 GeV]
  mu_1D        ~ 1e14 kg/m                 [eta_EW^2]
  sigma_2D     ~ 1e49 kg/m^2              [eta_EW^4/(hbar*c)]
  <S^2>_vol    = 3.88e-39 kg^2*m/s^2     [F1 MCMC calibration]
  P_tors(z=0) ~ -2e-82 Pa                 [-(1/4)*kappa^2*<S^2>_vol]
  beta_ECF     = 0.35 deg                 [Chern-Simons, birefringence]
  xi_KZ        ~ 50-80 Mpc               [KZ comoving segment length]

REFERENCES
----------
  [KZ mechanism]  Kibble (1976) J.Phys.A 9:1387; Zurek (1985) Nature 317:505
  [Conical metric] Vilenkin (1985) Phys.Rep. 121:263
  [Israel repulsion] Israel (1966) Nuovo Cim.B 44:1
  [Birefringence] Carroll, Field & Jackiw (1990) Phys.Rev.D 41:1231
  [PIT calibration] Fichant (2026) doi:10.5281/zenodo.19900557
  [Foundation I]  Fichant (2026) doi:10.5281/zenodo.19577447
  [Foundation II] Fichant (2026) doi:10.5281/zenodo.20629238

LICENSE
-------
  CC-BY 4.0 — Pascal Fichant, Montpellier, Occitanie, France
  Contact: p.fichant.research@gmail.com
  GitHub : github.com/pfichant/spin-torsion-cosmology

NOTE FOR REFEREE
-----------------
  Trajectories and field strengths are EXAGGERATED for visual clarity
  (e.g., conical deficit shown at delta ~ 0.2 rad vs physical ~ 1e-6 rad;
  lensing deflection similarly amplified).
  All equations shown in annotation boxes are physically correct.
  Canonical values in figure labels match Foundation II canonical table
  (Table tab:ecf_defect_summary, §Topological Zoology).
"""

import os, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.animation as animation

os.environ.setdefault('PYTHONIOENCODING', 'utf-8')

def _find_figs_dir(start=__file__):
    d = os.path.dirname(os.path.abspath(start))
    for _ in range(6):
        cand = os.path.join(d, 'figures_output')
        if os.path.isdir(cand): return cand
        parent = os.path.dirname(d)
        if parent == d: break
        d = parent
    fallback = os.path.join(os.path.dirname(os.path.abspath(start)), 'figures_output')
    os.makedirs(fallback, exist_ok=True)
    return fallback

FIGS = _find_figs_dir()
BG='#FFFFFF'; BG_AX='#F8F8FF'; C_TEXT='#111111'; C_SUB='#333333'
C_TICK='#555555'; C_RED='#CC2222'; C_BLUE='#2244AA'; C_GOLD='#BB8800'
C_CYAN='#0088AA'
ANNOT_BOX = dict(boxstyle='round,pad=0.4', facecolor='#EEF2FF',
                 alpha=0.92, edgecolor='#334488', lw=1.0)
plt.rcParams.update({'figure.dpi':120,'font.family':'serif','font.size':12,
                     'axes.labelsize':12,'axes.titlesize':13,
                     'xtick.labelsize':10,'ytick.labelsize':10})
N_FRAMES=80; FPS=18

# ══════════════════════════════════════════════════════════════════════════════
# ANIMATION 1 — 0D Micro-Knot
# Phase 1 (0-25):  straight photon paths
# Phase 2 (26-55): Micro-Knot forms, geodesics deflect, hedgehog field
# Phase 3 (56-79): halo accretes, kill-switch label
# ══════════════════════════════════════════════════════════════════════════════
print('Generating Anim_ECF_0D_MicroKnot.gif ...')
fig0, ax0 = plt.subplots(figsize=(10,8), facecolor=BG)
ax0.set_facecolor(BG_AX); ax0.set_xlim(-3.5,3.5); ax0.set_ylim(-3.0,3.0)
ax0.set_aspect('equal')
ax0.set_xlabel('x  [arb. units]',color=C_SUB)
ax0.set_ylabel('y  [arb. units]',color=C_SUB)
ax0.tick_params(colors=C_TICK)
for sp in ax0.spines.values(): sp.set_color('#AABBDD')

phase0 = ax0.text(0.02,0.96,'',transform=ax0.transAxes,fontsize=11,
                  color=C_BLUE,fontweight='bold',va='top',bbox=ANNOT_BOX)
knot,  = ax0.plot([],[],  'o',color=C_TEXT,markersize=0,zorder=10,
                  markeredgecolor=C_BLUE,markeredgewidth=1.5)

# Halo rings
halo_circles=[]
for r_h,al in [(0.30,0.35),(0.55,0.20),(0.85,0.10)]:
    c=plt.Circle((0,0),r_h,color=C_BLUE,fill=False,lw=2.0,alpha=0,zorder=5)
    ax0.add_patch(c); halo_circles.append((c,al))

# Hedgehog vectors
n_vec=12; angles_v=np.linspace(0,2*np.pi,n_vec,endpoint=False); r0v=0.55
vec_art=[]
for ang in angles_v:
    ox,oy=r0v*np.cos(ang),r0v*np.sin(ang)
    ln,=ax0.plot([],[],color='#CC2288',lw=1.2,alpha=0)
    vec_art.append((ln,ox,oy,ang))

# Null geodesics
n_rays=11; y_off=np.linspace(-2.2,2.2,n_rays)
ray_lines=[]
for y0 in y_off:
    col=C_CYAN if abs(y0)<0.6 else '#6699BB'
    lw=1.8 if abs(y0)<0.6 else 1.1
    ln,=ax0.plot([],[],color=col,lw=lw,alpha=0.75,zorder=3)
    ray_lines.append((ln,y0))

# Halo accreted particles
np.random.seed(42)
n_hp=18; ha=np.random.uniform(0,2*np.pi,n_hp); hr=np.random.uniform(1.0,2.2,n_hp)
halo_pts=[]
for a,r in zip(ha,hr):
    pt,=ax0.plot([],[],  'o',color='#6688CC',markersize=5,alpha=0,zorder=4)
    halo_pts.append((pt,a,r))

ks0=ax0.text(0.54,0.06,'Kill-switch [Roman 2028]:\n'
             r'$\tau_{\rm micro}\geq10^{-7}$, $t_E\sim0.5$ h'
             '\nPhoebe (Key+2026): $1.4\sigma$ from KZ peak',
             transform=ax0.transAxes,fontsize=9.5,color=C_RED,va='bottom',
             alpha=0,bbox=dict(boxstyle='round,pad=0.4',fc='#FFF0F0',
                               ec=C_RED,alpha=0))

ax0.set_title('ECF 0D Micro-Knot — Gravitational lensing & dark matter halo\n'
              r'$M_{\mu K}=6\times10^{24}$ kg $=c^3/GH_{\rm EW}$  |  '
              r'$\pi_2(\mathcal{M})\neq\emptyset$  |  Winding $N=1$  |  '
              r'$T_H=2.7$ mK',
              color=C_TEXT,fontsize=12,fontweight='bold',pad=12)

def upd0(f):
    if f<26:
        phase0.set_text('Phase 1 — Free photons (no Micro-Knot yet)')
        knot.set_markersize(0); knot.set_data([],[])
        for c,_ in halo_circles: c.set_alpha(0)
        for ln,*_ in vec_art: ln.set_alpha(0)
        for pt,*_ in halo_pts: pt.set_alpha(0)
        ks0.set_alpha(0); ks0.get_bbox_patch().set_alpha(0)
        xt=np.linspace(-3.5,3.5,200)
        n=max(1,int(len(xt)*f/25))
        for ln,y0 in ray_lines: ln.set_data(xt[:n],y0*np.ones(n))
    elif f<56:
        p=(f-26)/29
        phase0.set_text('Phase 2 — Micro-Knot crystallises: geodesics deflect')
        knot.set_data([0],[0]); knot.set_markersize(min(14,p*18))
        for c,al in halo_circles: c.set_alpha(min(al,p*al*1.5))
        for ln,ox,oy,ang in vec_art:
            ln.set_data([ox,ox+0.28*np.cos(ang)],[oy,oy+0.28*np.sin(ang)])
            ln.set_alpha(min(0.85,p*1.2))
        xi=np.linspace(-3.5,0,100); xo=np.linspace(0,3.5,100)
        for ln,y0 in ray_lines:
            imp=abs(y0)+0.12; ad=p*0.42/(imp+0.18)
            yo=y0-np.sign(y0)*ad*(xo/(np.abs(xo)+0.3))
            ln.set_data(np.r_[xi,xo],np.r_[y0*np.ones(100),yo])
        for pt,*_ in halo_pts: pt.set_alpha(0)
        ks0.set_alpha(0); ks0.get_bbox_patch().set_alpha(0)
    else:
        p=(f-56)/23
        phase0.set_text('Phase 3 — Accreted halo: dark matter clump')
        knot.set_data([0],[0]); knot.set_markersize(14)
        for c,al in halo_circles: c.set_alpha(al)
        for i,(pt,a,r) in enumerate(halo_pts):
            rn=r-p*(r-1.05); an=a+p*0.8*(i%3-1)
            pt.set_data([rn*np.cos(an)],[rn*np.sin(an)])
            pt.set_alpha(min(0.85,p*1.2))
        ka=min(1.0,p*2); ks0.set_alpha(ka); ks0.get_bbox_patch().set_alpha(ka*0.92)
        xi=np.linspace(-3.5,0,100); xo=np.linspace(0,3.5,100)
        for ln,y0 in ray_lines:
            imp=abs(y0)+0.12; ad=0.42/(imp+0.18)
            yo=y0-np.sign(y0)*ad*(xo/(np.abs(xo)+0.3))
            ln.set_data(np.r_[xi,xo],np.r_[y0*np.ones(100),yo])
    return ([phase0,knot,ks0]+[ln for ln,_ in ray_lines]+
            [ln for ln,*_ in vec_art]+[pt for pt,*_ in halo_pts]+
            [c for c,_ in halo_circles])

ani0=animation.FuncAnimation(fig0,upd0,frames=N_FRAMES,interval=1000/FPS,blit=True)
p0=os.path.join(FIGS,'Anim_ECF_0D_MicroKnot.gif')
ani0.save(p0,writer='pillow',fps=FPS,dpi=120)
plt.close(fig0); print(f'  [OK] -> {p0}')

# ══════════════════════════════════════════════════════════════════════════════
# ANIMATION 2 — 1D Torsion String: gas dynamics along cosmic filament
# Phase 1 (0-25):  string crystallises (helix + conical metric)
# Phase 2 (26-55): velocity kick δv, gas flows toward string axis
# Phase 3 (56-79): baryonic wake, Lyman-α overdensity, mass table
# ══════════════════════════════════════════════════════════════════════════════
print('Generating Anim_ECF_1D_TorsionString.gif ...')
fig1, ax1 = plt.subplots(figsize=(12,8), facecolor=BG)
ax1.set_facecolor(BG_AX); ax1.set_xlim(-4.5,4.5); ax1.set_ylim(-3.5,3.5)
ax1.set_aspect('equal')
ax1.set_xlabel('x  (distance to string)  [arb. units]',color=C_SUB)
ax1.set_ylabel('y  (along string)  [arb. units]',color=C_SUB)
ax1.tick_params(colors=C_TICK)
for sp in ax1.spines.values(): sp.set_color('#AABBDD')

phase1=ax1.text(0.02,0.96,'',transform=ax1.transAxes,fontsize=11,
                color=C_BLUE,fontweight='bold',va='top',bbox=ANNOT_BOX)

string_ln,=ax1.plot([0,0],[-3.5,3.5],color=C_GOLD,lw=3.5,alpha=0,
                    zorder=10,label=r'1D Torsion String ($\mu_{1D}\sim10^{14}$ kg/m)')
helix_ln, =ax1.plot([],[],color='#CC2288',lw=1.8,alpha=0,zorder=11,
                    label=r'Helical axial current $\vec{J}_5$')

# Conical deficit region
cone_left =ax1.fill_betweenx([-3.5,3.5],[0,0],[-0.3,-0.3],
                               color=C_GOLD,alpha=0,zorder=2)
cone_right=ax1.fill_betweenx([-3.5,3.5],[0,0],[ 0.3, 0.3],
                               color=C_GOLD,alpha=0,zorder=2)
deficit_tx=ax1.text(0.55,0.70,
    r'Conical deficit: $\delta=8\pi G\mu_{1D}/c^2$'+'\n'+
    r'No Newtonian $1/r^2$ — only velocity kick $\delta v$',
    transform=ax1.transAxes,fontsize=9.5,color=C_GOLD,va='center',alpha=0,
    bbox=dict(boxstyle='round,pad=0.3',fc='#FFFBE8',ec=C_GOLD,alpha=0))

# Gas particles
np.random.seed(7)
n_g=55
gx0=np.concatenate([np.random.uniform(-4.0,-0.35,n_g//2),
                     np.random.uniform( 0.35, 4.0,n_g//2)])
gy0=np.random.uniform(-3.2,3.2,len(gx0))
gas_sc=ax1.scatter(gx0,gy0,c=C_CYAN,s=22,alpha=0.7,zorder=5,
                   label='Baryonic gas')

# Velocity kick arrows
n_kick=12; kick_ys=np.linspace(-3.0,3.0,n_kick)
kick_arr=[]
for ky in kick_ys:
    kx=2.2; sign=1
    for side in [1,-1]:
        a=ax1.annotate('',xy=(0,ky),xytext=(side*kx,ky),
                        arrowprops=dict(arrowstyle='->',color=C_RED,lw=1.6,alpha=0))
        kick_arr.append(a)

# Wake overdensity (narrow colored band near string)
wake_ln,=ax1.plot([],[],color=C_RED,lw=0,alpha=0,zorder=4)

mass_tx=ax1.text(0.55,0.10,
    'Intrinsic string mass:\n'
    r'1 kpc  → $\sim10^3\,M_\odot$'+'\n'
    r'1 Mpc  → $\sim10^6\,M_\odot$'+'\n'
    r'$\xi_{\rm KZ}\!\sim\!60$ Mpc → $\sim3\times10^7\,M_\odot$'+'\n\n'
    r'Baryonic wake: $\sim10^5\,M_\odot$/kpc (Lyman-$\alpha$)'+'\n'
    'Kill-switch [LISA 2037]:\n'
    r'GW burst $f\!\sim\!50$ mHz, tail $\tau_T\!\sim\!10^6$ s',
    transform=ax1.transAxes,fontsize=9.5,color=C_TEXT,va='bottom',alpha=0,
    bbox=dict(boxstyle='round,pad=0.4',fc='#EEF2FF',ec=C_BLUE,alpha=0))

ax1.set_title(
    'ECF 1D Torsion String — Conical deficit & baryonic wake formation\n'
    r'$\pi_1(\mathcal{M})\neq\emptyset$  |  '
    r'$\delta v=4\pi G\mu_{1D}v_s\gamma_s$  |  '
    r'Helical $\vec{J}_5$  |  Reconnects (never merges)',
    color=C_TEXT,fontsize=12,fontweight='bold',pad=12)
ax1.legend(loc='upper right',fontsize=9,framealpha=0.85,
           facecolor='#F4F6FF',edgecolor=C_BLUE)

def gas_pos1(f):
    if f<26: return gx0.copy(),gy0.copy()
    p=min(1.0,(f-26)/29)
    imp=np.abs(gx0)+0.1
    kick=0.65*p/(imp+0.15)
    nx=gx0-np.sign(gx0)*kick*imp
    if f>=56:
        p2=(f-56)/23
        nx=nx*(1-0.30*p2)
    return nx,gy0.copy()

def upd1(f):
    gx,gy=gas_pos1(f)
    gas_sc.set_offsets(np.c_[gx,gy])
    dists=np.abs(gx); cols=plt.cm.coolwarm_r(np.clip(dists/4.0,0,1))
    gas_sc.set_facecolor(cols)

    if f<26:
        phase1.set_text('Phase 1 — Torsion String crystallises (helical J₅)')
        p=f/25
        string_ln.set_alpha(min(1.0,p*2))
        hy=np.linspace(-3.5,3.5,300)
        hx=0.18*np.sin(5*hy)*p
        helix_ln.set_data(hx,hy); helix_ln.set_alpha(min(0.9,p*1.4))
        cone_left.set_alpha(0); cone_right.set_alpha(0)
        deficit_tx.set_alpha(min(1.0,p*2)); deficit_tx.get_bbox_patch().set_alpha(min(0.9,p*2))
        for a in kick_arr: a.arrow_patch.set_alpha(0)
        mass_tx.set_alpha(0); mass_tx.get_bbox_patch().set_alpha(0)
    elif f<56:
        phase1.set_text('Phase 2 — Velocity kick δv: gas converges to string axis')
        p=(f-26)/29
        string_ln.set_alpha(1.0)
        hy=np.linspace(-3.5,3.5,300); hx=0.18*np.sin(5*hy)
        helix_ln.set_data(hx,hy); helix_ln.set_alpha(0.9)
        aa=min(0.80,p*1.3)
        for a in kick_arr: a.arrow_patch.set_alpha(aa)
        mass_tx.set_alpha(0); mass_tx.get_bbox_patch().set_alpha(0)
    else:
        phase1.set_text('Phase 3 — Baryonic wake: Lyman-α overdensity')
        p=(f-56)/23
        hy=np.linspace(-3.5,3.5,300); hx=0.18*np.sin(5*hy)
        helix_ln.set_data(hx,hy); helix_ln.set_alpha(0.9)
        for a in kick_arr: a.arrow_patch.set_alpha(max(0,0.8-p*0.9))
        ma=min(1.0,p*2)
        mass_tx.set_alpha(ma); mass_tx.get_bbox_patch().set_alpha(ma*0.92)
        # Wake fill (red band near string)
        yw=np.linspace(-3.5,3.5,200)
        ww=0.25*(1+p*0.5)
        wake_ln.set_data(np.r_[-ww*np.ones(200),ww*np.ones(200)],
                         np.r_[yw,yw[::-1]])
        wake_ln.set_lw(0)
    return ([phase1,string_ln,helix_ln,gas_sc,deficit_tx,mass_tx,wake_ln]+
            kick_arr+[cone_left,cone_right])

ani1=animation.FuncAnimation(fig1,upd1,frames=N_FRAMES,interval=1000/FPS,blit=False)
p1=os.path.join(FIGS,'Anim_ECF_1D_TorsionString.gif')
ani1.save(p1,writer='pillow',fps=FPS,dpi=120)
plt.close(fig1); print(f'  [OK] -> {p1}')

# ══════════════════════════════════════════════════════════════════════════════
# ANIMATION 3 — 2D Chiral Wall: Israel repulsion & void formation
# Phase 1 (0-25):  σ+/σ− domains appear, Chiral Wall forms at z=0
# Phase 2 (26-55): Israel repulsion z̈∝z, gas expelled, void opens
# Phase 3 (56-79): supervoid complete, CMB photon birefringence, dual mechanism
# ══════════════════════════════════════════════════════════════════════════════
print('Generating Anim_ECF_2D_ChiralWall.gif ...')
fig2,ax2=plt.subplots(figsize=(11,9),facecolor=BG)
ax2.set_facecolor(BG_AX); ax2.set_xlim(-4.5,4.5); ax2.set_ylim(-4.2,4.2)
ax2.set_aspect('equal')
ax2.set_xlabel('x  [arb. units]',color=C_SUB)
ax2.set_ylabel('z  (perpendicular to wall)  [arb. units]',color=C_SUB)
ax2.tick_params(colors=C_TICK)
for sp in ax2.spines.values(): sp.set_color('#AABBDD')

phase2=ax2.text(0.02,0.96,'',transform=ax2.transAxes,fontsize=11,
                color=C_BLUE,fontweight='bold',va='top',bbox=ANNOT_BOX)

# Domain fills
dom_p=ax2.fill_between([-4.5,4.5],[0,0],[4.2,4.2],color='#DDEEFF',alpha=0,zorder=1)
dom_m=ax2.fill_between([-4.5,4.5],[-4.2,-4.2],[0,0],color='#FFDDDD',alpha=0,zorder=1)
lp=ax2.text( 2.8, 2.8,r'Phase $\sigma_+$'+'\n(+helicity)',fontsize=11,
             color='#2244AA',ha='center',fontweight='bold',alpha=0)
lm=ax2.text(-2.8,-2.8,r'Phase $\sigma_-$'+'\n(−helicity)',fontsize=11,
             color='#AA2222',ha='center',fontweight='bold',alpha=0)

wall_ln,=ax2.plot([-4.5,4.5],[0,0],color='#5566CC',lw=4.0,alpha=0,
                  zorder=10,label=r'2D Chiral Wall ($\sigma_{2D}\sim10^{49}$ kg/m²)')
wall_tx=ax2.text(0,0.15,r'Chiral Wall ($\delta_w\sim10^{-18}$ m)',
                 fontsize=10,color='#2244BB',ha='center',alpha=0,zorder=11,
                 bbox=dict(boxstyle='round,pad=0.3',fc='#EEF0FF',ec='#5566CC',alpha=0))

# Gas particles
np.random.seed(13)
n_up=28; n_dn=28
gxu=np.random.uniform(-4.0,4.0,n_up); gyu=np.random.uniform(0.3,3.8,n_up)
gxd=np.random.uniform(-4.0,4.0,n_dn); gyd=np.random.uniform(-3.8,-0.3,n_dn)
scu=ax2.scatter(gxu,gyu,c=C_BLUE,s=22,alpha=0,zorder=5,label='Baryonic gas (σ+)')
scd=ax2.scatter(gxd,gyd,c=C_RED, s=22,alpha=0,zorder=5,label='Baryonic gas (σ−)')

# Repulsion arrows
n_arr=9; axs=np.linspace(-3.8,3.8,n_arr)
arr_u=[]; arr_d=[]
for ax_x in axs:
    au=ax2.annotate('',xy=(ax_x,1.1),xytext=(ax_x,0.08),
                     arrowprops=dict(arrowstyle='->',color=C_RED,lw=1.8,alpha=0))
    ad=ax2.annotate('',xy=(ax_x,-1.1),xytext=(ax_x,-0.08),
                     arrowprops=dict(arrowstyle='->',color=C_RED,lw=1.8,alpha=0))
    arr_u.append(au); arr_d.append(ad)

israel_tx=ax2.text(0.56,0.52,
    'Israel (1966) repulsion:\n'
    r'$\ddot{z}=\frac{8\pi G\sigma_{2D}}{3}\,z$'+'\n'
    r'$z(t)\propto e^{\sqrt{8\pi G\sigma_{2D}/3}\,t}$'+'\n'
    r'Wall expands at $\sim c$',
    transform=ax2.transAxes,fontsize=10,color=C_RED,va='center',alpha=0,
    bbox=dict(boxstyle='round,pad=0.4',fc='#FFF0F0',ec=C_RED,alpha=0))

# CMB birefringence photon
phot_ln,=ax2.plot([],[],color='#FF8800',lw=2.8,alpha=0,zorder=8,
                   label=r'CMB photon: $\Delta\theta=\beta=0.35°$ (achromatic)')
phot_pt,=ax2.plot([],[],  'o',color='#FF8800',markersize=10,alpha=0,zorder=9)
beta_tx=ax2.text(0,0.25,r'$\beta_{\rm ECF}=0.35°$',fontsize=12,
                  color='#FF8800',ha='center',alpha=0,fontweight='bold',
                  bbox=dict(boxstyle='round,pad=0.3',fc='#FFF8EE',ec='#FF8800',alpha=0))

# Dual mechanism
dual_tx=ax2.text(0.02,0.06,
    'Dual void mechanism:\n'
    '(1) Chiral Wall → sharp boundary (local, ⊥ wall)\n'
    '(2) 3D Torsion Fluid → sustains expansion (global, isotropic)\n'
    r'Neither alone is sufficient — ECF prediction'+'\n'
    r'Kill-switch [LiteBIRD 2032]: $\beta<0.1°$ at $3\sigma$',
    transform=ax2.transAxes,fontsize=9.5,color=C_TEXT,va='bottom',alpha=0,
    bbox=dict(boxstyle='round,pad=0.4',fc='#EEF2FF',ec=C_BLUE,alpha=0))

ax2.set_title(
    'ECF 2D Chiral Wall — Israel repulsion & cosmic void formation\n'
    r'$\pi_0(\mathcal{M})\neq\emptyset$  |  $\sigma_{2D}\sim10^{49}$ kg/m²  |  '
    r'$\beta_{\rm ECF}=0.35°$  |  $R_w\sim\xi_{\rm KZ}\sim60$ Mpc',
    color=C_TEXT,fontsize=12,fontweight='bold',pad=12)
ax2.legend(loc='upper right',fontsize=9,framealpha=0.85,
           facecolor='#F4F6FF',edgecolor=C_BLUE)

def upd2(f):
    if f<26:
        phase2.set_text('Phase 1 — Chiral symmetry breaking: σ+/σ− domains form')
        p=f/25
        dom_p.set_alpha(min(0.22,p*0.28)); dom_m.set_alpha(min(0.22,p*0.28))
        lp.set_alpha(min(1.0,p*1.5)); lm.set_alpha(min(1.0,p*1.5))
        wall_ln.set_alpha(min(1.0,p*2))
        wall_tx.set_alpha(min(1.0,p*2)); wall_tx.get_bbox_patch().set_alpha(min(0.9,p*2))
        scu.set_alpha(min(0.7,p*0.9)); scd.set_alpha(min(0.7,p*0.9))
        for a in arr_u+arr_d: a.arrow_patch.set_alpha(0)
        israel_tx.set_alpha(0); israel_tx.get_bbox_patch().set_alpha(0)
        phot_ln.set_alpha(0); phot_pt.set_alpha(0); beta_tx.set_alpha(0)
        dual_tx.set_alpha(0); dual_tx.get_bbox_patch().set_alpha(0)
        scu.set_offsets(np.c_[gxu,gyu]); scd.set_offsets(np.c_[gxd,gyd])
    elif f<56:
        phase2.set_text('Phase 2 — Israel repulsion: baryonic gas expelled along z')
        p=(f-26)/29
        ef=np.exp(p*1.5)-1
        scu.set_offsets(np.c_[gxu, gyu+ef*gyu*0.40])
        scd.set_offsets(np.c_[gxd, gyd+ef*gyd*0.40])
        scu.set_alpha(0.75); scd.set_alpha(0.75)
        aa=min(0.85,p*1.4)
        for i,(au,ad) in enumerate(zip(arr_u,arr_d)):
            yt=0.08+p*1.5
            au.xy=(axs[i],yt); ad.xy=(axs[i],-yt)
            au.arrow_patch.set_alpha(aa); ad.arrow_patch.set_alpha(aa)
        israel_tx.set_alpha(min(1.0,p*2)); israel_tx.get_bbox_patch().set_alpha(min(0.9,p*2))
        phot_ln.set_alpha(0); phot_pt.set_alpha(0); beta_tx.set_alpha(0)
        dual_tx.set_alpha(0); dual_tx.get_bbox_patch().set_alpha(0)
        beta_tx.get_bbox_patch().set_alpha(0)
    else:
        phase2.set_text('Phase 3 — Supervoid + CMB birefringence β = 0.35°')
        p=(f-56)/23
        ef=np.exp(1.5)-1
        scu.set_offsets(np.c_[gxu, gyu+ef*gyu*0.40*(1+p*0.3)])
        scd.set_offsets(np.c_[gxd, gyd+ef*gyd*0.40*(1+p*0.3)])
        for a in arr_u+arr_d: a.arrow_patch.set_alpha(max(0,0.85-p*0.8))
        # Photon traverses wall
        px=-4.2+p*8.4
        phot_ln.set_data(np.linspace(-4.2,px,100),np.zeros(100))
        phot_pt.set_data([px],[0])
        pa=min(1.0,p*2)
        phot_ln.set_alpha(pa); phot_pt.set_alpha(pa)
        beta_tx.set_alpha(pa); beta_tx.get_bbox_patch().set_alpha(pa*0.9)
        da=min(1.0,p*2)
        dual_tx.set_alpha(da); dual_tx.get_bbox_patch().set_alpha(da*0.92)
        israel_tx.set_alpha(max(0.25,1.0-p*0.6))
        israel_tx.get_bbox_patch().set_alpha(max(0.25,0.9-p*0.6))

    return ([phase2,wall_ln,wall_tx,lp,lm,scu,scd,
             phot_ln,phot_pt,beta_tx,israel_tx,dual_tx,
             dom_p,dom_m]+arr_u+arr_d)

ani2=animation.FuncAnimation(fig2,upd2,frames=N_FRAMES,interval=1000/FPS,blit=False)
p2=os.path.join(FIGS,'Anim_ECF_2D_ChiralWall.gif')
ani2.save(p2,writer='pillow',fps=FPS,dpi=120)
plt.close(fig2); print(f'  [OK] -> {p2}')

print(f'\nDone — 3 animations in {FIGS}')
print('  Anim_ECF_0D_MicroKnot.gif')
print('  Anim_ECF_1D_TorsionString.gif')
print('  Anim_ECF_2D_ChiralWall.gif')

# ══════════════════════════════════════════════════════════════════════════════
# ANIMATION 4 — 3D Torsion Fluid: isotropic dark energy & void amplification
#
# Physics:
#   The 3D Torsion Fluid is NOT a topological defect (no homotopy obstruction).
#   It is the volume-filling residual condensate from the KZ crystallisation:
#     P_tors = -(1/4) * kappa^2 * <S^2>_vol  ~ -2e-82 Pa
#     w(z) = w0 + wa*(1-a) = -0.904 - 0.153*(1-a)
#   Key property: locally DEPLETED in halos (0D knots dominate),
#                 locally AMPLIFIED in voids (Omega_m -> 0).
#   This spatial modulation is the "geometric back-reaction" DM <-> DE.
#
# Phase 1 (0-25):  isotropic pressure field shown, uniform condensate
# Phase 2 (26-55): depletion near 0D halo (DM dominates locally),
#                  amplification in void (3D fluid dominates)
# Phase 3 (56-79): w(z) panel appears, DESI DR2 comparison, kill-switch
# ══════════════════════════════════════════════════════════════════════════════
print('Generating Anim_ECF_3D_TorsionFluid.gif ...')

fig3 = plt.figure(figsize=(14, 7), facecolor=BG)

# Left panel: spatial map of torsion fluid density
ax3a = fig3.add_subplot(121, facecolor=BG_AX)
ax3a.set_xlim(-4.5, 4.5)
ax3a.set_ylim(-4.0, 4.0)
ax3a.set_aspect('equal')
ax3a.set_xlabel('x  [arb. units]', color=C_SUB)
ax3a.set_ylabel('y  [arb. units]', color=C_SUB)
ax3a.set_title('Spatial distribution of\n3D Torsion Fluid density',
               color=C_TEXT, fontsize=11, fontweight='bold')
ax3a.tick_params(colors=C_TICK)
for sp in ax3a.spines.values():
    sp.set_color('#AABBDD')

# Right panel: w(z) equation of state
ax3b = fig3.add_subplot(122, facecolor=BG_AX)
ax3b.set_xlabel(r'Redshift $z$', color=C_SUB)
ax3b.set_ylabel(r'Equation of state $w(z)$', color=C_SUB)
ax3b.set_title(r'Dark energy $w(z) = w_0 + w_a(1-a)$',
               color=C_TEXT, fontsize=11, fontweight='bold')
ax3b.tick_params(colors=C_TICK)
for sp in ax3b.spines.values():
    sp.set_color('#AABBDD')
ax3b.set_xlim(0, 3.5)
ax3b.set_ylim(-1.25, -0.60)
ax3b.axhline(-1.0, color='#888888', lw=1.5, ls='--', alpha=0.7)

# ── Left panel static elements ────────────────────────────────────────────────
# Background fluid grid (density field shown as colored mesh)
nx, ny = 40, 36
xg = np.linspace(-4.3, 4.3, nx)
yg = np.linspace(-3.8, 3.8, ny)
XG, YG = np.meshgrid(xg, yg)

# 0D knot at (-2, 1) — depletes local fluid
knot_x, knot_y = -2.0, 1.0
# Void at (2, -1) — amplifies local fluid
void_x, void_y = 2.0, -1.0

def fluid_density(xx, yy, t_phase, p_sub):
    """
    Compute normalised torsion fluid density at position (xx,yy).
    t_phase: 0=uniform, 1=full modulation
    p_sub  : sub-phase progress 0->1

    Physical model:
      rho_fluid(r) ~ rho_0 * [1 - A_DM * exp(-r_knot^2/r_depl^2)
                                 + A_void * exp(-r_void^2/r_amp^2)]
    Knot depletion: 0D Micro-Knot dominates locally -> fluid depleted
    Void amplification: Omega_m->0 in void -> fluid locally dominant
    """
    r_knot = np.sqrt((xx - knot_x)**2 + (yy - knot_y)**2)
    r_void = np.sqrt((xx - void_x)**2 + (yy - void_y)**2)
    r_depl = 0.9   # depletion radius around knot
    r_amp  = 1.4   # amplification radius in void
    A_DM   = 0.72 * t_phase * p_sub
    A_void = 0.55 * t_phase * p_sub
    rho = (1.0
           - A_DM  * np.exp(-r_knot**2 / r_depl**2)
           + A_void * np.exp(-r_void**2 / r_amp**2))
    return np.clip(rho, 0.05, 1.80)

# Initial density (uniform)
Z0 = fluid_density(XG, YG, 0, 0)
im = ax3a.pcolormesh(XG, YG, Z0, cmap='RdBu_r', vmin=0.1, vmax=1.7,
                      shading='gouraud', zorder=2)
cb = fig3.colorbar(im, ax=ax3a, shrink=0.75, pad=0.02)
cb.set_label(r'$\langle S^2\rangle_{\rm vol}$ (normalised)', color=C_SUB, fontsize=9)
cb.ax.tick_params(colors=C_TICK, labelsize=8)

# 0D Micro-Knot marker
knot_mk, = ax3a.plot([knot_x], [knot_y], 'o', color=C_TEXT, markersize=13,
                      zorder=10, markeredgecolor=C_BLUE, markeredgewidth=1.5,
                      label=r'0D Micro-Knot halo (depletes fluid)')
ax3a.text(knot_x + 0.15, knot_y + 0.35, 'Dark matter\nhalo\n(fluid depleted)',
           fontsize=8.5, color=C_BLUE, fontweight='bold', zorder=11)

# Void marker
void_circle = plt.Circle((void_x, void_y), 1.2, color='#5566CC',
                           fill=False, lw=2.0, ls='--', alpha=0, zorder=8)
ax3a.add_patch(void_circle)
ax3a.text(void_x + 0.0, void_y - 1.70,
           'Cosmic void\n(fluid amplified)',
           fontsize=8.5, color='#5566CC', ha='center',
           fontweight='bold', alpha=0, zorder=11)
void_label = ax3a.texts[-1]

# Isotropic pressure arrows (8 directions, phase 1)
n_press = 8
press_arrows = []
for ang in np.linspace(0, 2*np.pi, n_press, endpoint=False):
    dx, dy = 0.55*np.cos(ang), 0.55*np.sin(ang)
    a = ax3a.annotate('', xy=(dx*1.7, dy*1.7), xytext=(dx*0.6, dy*0.6),
                       arrowprops=dict(arrowstyle='->', color=C_GOLD,
                                       lw=1.8, alpha=0))
    press_arrows.append(a)
ax3a.text(0.0, -0.45, r'$P_{\rm tors}<0$', fontsize=9, color=C_GOLD,
           ha='center', alpha=0, fontweight='bold')
press_label = ax3a.texts[-1]

# Phase label left
phase3a = ax3a.text(0.02, 0.97, '', transform=ax3a.transAxes,
                     fontsize=9.5, color=C_BLUE, fontweight='bold',
                     va='top', bbox=ANNOT_BOX)

# ── Right panel: w(z) plot (built progressively) ─────────────────────────────
w0_ecf, wa_ecf = -0.904, -0.153
z_arr = np.linspace(0, 3.5, 400)
a_arr = 1.0 / (1.0 + z_arr)
w_ecf  = w0_ecf + wa_ecf * (1.0 - a_arr)
w_lcdm = -1.0 * np.ones_like(z_arr)

# Static elements
ax3b.plot(z_arr, w_lcdm, color='#888888', lw=1.8, ls='--',
          label=r'$\Lambda$CDM: $w=-1$', alpha=0.6)
ax3b.axhspan(-1.10, -0.85, alpha=0.10, color='#228844',
             label='DESI DR2 preferred (schematic)')
ax3b.text(0.15, -1.135, 'DESI DR2\npreferred',
           fontsize=8, color='#228844', va='bottom')
ax3b.axhline(-1.057, color='#CC4444', lw=1.0, ls=':', alpha=0.5)
ax3b.text(3.3, -1.065, r'$w_0+w_a=-1.057$', fontsize=7.5,
           color='#CC4444', ha='right', alpha=0.7)

# ECF w(z) curve drawn progressively
ecf_line, = ax3b.plot([], [], color=C_RED, lw=2.8,
                       label=r'ECF: $w_0=-0.904$, $w_a=-0.153$ (a priori, PIT)')
ecf_fill  = ax3b.fill_between([], [], -1.0, alpha=0)

# Annotation on w(z) panel
wz_annot = ax3b.text(0.04, 0.08,
    r'$P_{\rm tors}=-\frac{1}{4}\kappa^2\langle S^2\rangle_{\rm vol}$' + '\n'
    r'$\kappa^2=2.0766\times10^{-43}$ m J$^{-1}$' + '\n'
    r'Dilution: $P_{\rm tors}\propto a^{-3(1+w)}$' + '\n'
    r'Kill-switch [DESI DR3 2027]:' + '\n'
    r'$w=-1$ at $5\sigma$ falsifies ECF fluid',
    transform=ax3b.transAxes, fontsize=8.5, color=C_TEXT,
    va='bottom', alpha=0,
    bbox=dict(boxstyle='round,pad=0.4', fc='#EEF2FF', ec=C_BLUE, alpha=0))

ax3b.legend(loc='upper right', fontsize=8.5,
            framealpha=0.85, facecolor='#F4F6FF', edgecolor=C_BLUE)

# Phase label right
phase3b = ax3b.text(0.02, 0.97, '', transform=ax3b.transAxes,
                     fontsize=9.5, color=C_BLUE, fontweight='bold',
                     va='top', bbox=ANNOT_BOX)

# Suptitle
fig3.suptitle(
    'ECF 3D Torsion Fluid — Volume-filling condensate & dynamical dark energy\n'
    r'No homotopy obstruction  |  $f_{\rm fluid}\sim0.73$  |  '
    r'$\langle S^2\rangle_{\rm vol}^{(0)}\simeq3.88\times10^{-39}$ kg²m/s²  |  '
    r'$P_{\rm tors}\simeq-2\times10^{-82}$ Pa',
    color=C_TEXT, fontsize=12, fontweight='bold', y=1.01)

plt.tight_layout()

def upd3(f):
    t = f / N_FRAMES

    # ── Phase 1: uniform condensate, isotropic pressure ────────────────────
    if f < 26:
        p = f / 25
        phase3a.set_text('Phase 1 — Residual torsion condensate: isotropic P < 0')
        phase3b.set_text('Phase 1 — w(z) not yet revealed')

        # Density: still uniform, gently pulsing
        pulse = 1.0 + 0.06 * np.sin(f * 0.5)
        Z = fluid_density(XG, YG, 0, 0) * pulse
        im.set_array(Z.ravel())

        # Pressure arrows fade in
        arr_alpha = min(0.80, p * 1.2)
        for a in press_arrows:
            a.arrow_patch.set_alpha(arr_alpha)
        press_label.set_alpha(arr_alpha)

        # Void circle invisible
        void_circle.set_alpha(0)
        void_label.set_alpha(0)

        # w(z) curve: just show lCDM line
        ecf_line.set_data([], [])
        wz_annot.set_alpha(0)
        wz_annot.get_bbox_patch().set_alpha(0)

    # ── Phase 2: DM depletion + void amplification ─────────────────────────
    elif f < 56:
        p = (f - 26) / 29
        phase3a.set_text('Phase 2 — Back-reaction: depleted near halo, amplified in void')
        phase3b.set_text(r'Phase 2 — $w(z)$ evolves from PIT calibration')

        # Modulated density
        Z = fluid_density(XG, YG, 1.0, p)
        im.set_array(Z.ravel())

        # Pressure arrows fade out (fluid is no longer uniform)
        arr_alpha = max(0, 0.8 - p * 1.2)
        for a in press_arrows:
            a.arrow_patch.set_alpha(arr_alpha)
        press_label.set_alpha(arr_alpha)

        # Void circle appears
        void_circle.set_alpha(min(0.85, p * 1.4))
        void_label.set_alpha(min(1.0, p * 1.6))

        # w(z) curve draws progressively
        n_pts = max(2, int(len(z_arr) * p))
        ecf_line.set_data(z_arr[:n_pts], w_ecf[:n_pts])

        wz_annot.set_alpha(0)
        wz_annot.get_bbox_patch().set_alpha(0)

    # ── Phase 3: full modulation + w(z) + kill-switch ─────────────────────
    else:
        p = (f - 56) / 23
        phase3a.set_text('Phase 3 — Geometric back-reaction: DM ↔ DE coupled')
        phase3b.set_text('Phase 3 — DESI comparison & kill-switch')

        Z = fluid_density(XG, YG, 1.0, 1.0)
        # Gentle oscillation to show fluid is dynamic
        osc = 1.0 + 0.04 * np.sin(f * 0.8)
        im.set_array((Z * osc).ravel())

        for a in press_arrows:
            a.arrow_patch.set_alpha(0)
        press_label.set_alpha(0)
        void_circle.set_alpha(0.85)
        void_label.set_alpha(1.0)

        # Full w(z) curve + fill vs LCDM
        ecf_line.set_data(z_arr, w_ecf)
        # Redraw fill (remove old, add new with alpha)
        for coll in ax3b.collections:
            if coll != im:
                try:
                    coll.remove()
                except Exception:
                    pass
        ax3b.fill_between(z_arr, w_ecf, -1.0,
                          where=(w_ecf > -1.0),
                          alpha=min(0.20, p * 0.25),
                          color=C_RED, label='_nolegend_')

        # Kill-switch annotation
        ka = min(1.0, p * 2)
        wz_annot.set_alpha(ka)
        wz_annot.get_bbox_patch().set_alpha(ka * 0.92)

    return ([phase3a, phase3b, ecf_line, wz_annot,
             void_circle, void_label, press_label, im] + press_arrows)

ani3 = animation.FuncAnimation(fig3, upd3, frames=N_FRAMES,
                                interval=1000/FPS, blit=False)
p3 = os.path.join(FIGS, 'Anim_ECF_3D_TorsionFluid.gif')
ani3.save(p3, writer='pillow', fps=FPS, dpi=120)
plt.close(fig3)
print(f'  [OK] -> {p3}')

print(f'\nDone — 4 animations in {FIGS}')
print('  Anim_ECF_0D_MicroKnot.gif')
print('  Anim_ECF_1D_TorsionString.gif')
print('  Anim_ECF_2D_ChiralWall.gif')
print('  Anim_ECF_3D_TorsionFluid.gif')

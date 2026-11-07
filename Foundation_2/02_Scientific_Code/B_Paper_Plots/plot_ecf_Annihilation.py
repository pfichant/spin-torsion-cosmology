#!/usr/bin/env python3
"""
ECF — Annihilation Knot+Anti-Knot
4 panels : Eiso vs M, Pie Micro-Knot, Observability instruments, Pie Macro-Knot

Correction 14/10/2026 : traits verticaux placés aux masses annoncées (10^5 et
10^6 Msun ; ils étaient à 2e30 et 2e31 kg, soit 1 et 10 Msun) ; repères
eta = 0,1 du panneau C calculés depuis eta*2Mc^2 (Micro-Knot 3,74e24 kg,
Macro-Knot 10^5 Msun) au lieu de valeurs écrites à la main ; eta = 0,1 est
illustratif (eta_ann est ouvert, F2 annexe eta_ann). Courbes inchangées.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np

C_LIGHT = 2.998e8          # m/s
M_SUN   = 1.989e30         # kg
M_MICRO = 3.74e24          # kg, masse Micro-Knot (F2)
M_MACRO = 1e5 * M_SUN      # kg, Macro-Knot de référence
def e_rad_erg(eta, M):     # E = eta * 2 M c^2, en erg
    return eta * 2 * M * C_LIGHT**2 * 1e7

# Colour palette tuned for a white background
BG, RED, TXT = 'white', '#c0392b', '#111111'

fig = plt.figure(figsize=(18,12), facecolor=BG)
gs  = gridspec.GridSpec(2,2, figure=fig, hspace=0.45, wspace=0.35,
                        left=0.07, right=0.97, top=0.91, bottom=0.07)

# ---- Panel A ----
axA = fig.add_subplot(gs[0,0]); axA.set_facecolor(BG)
M   = np.logspace(24,65,500)
for eta,ls,col,lbl in [(0.5,'--','#e8a0a0','η = 0.5'),(0.1,'-',RED,'η = 0.1 (illustrative)'),(0.01,':','#e8c87e','η = 0.01')]:
    axA.loglog(M, eta*2*M*(3e8)**2*1e7, ls, color=col, linewidth=2.2, label=lbl)

# Reference colours darkened, for contrast against white
# 22/10/2026 : GRB 221009A place a E_iso ~ 1.2e55 erg (Konus-Wind ; 1.0e55 Fermi-GBM ; Atteia et al. 2025,
# arXiv:2501.13505) au lieu de 1e54. Police fixee a DejaVu Sans pour la reproductibilite.
import matplotlib as _mpl
_mpl.rcParams['font.family']=['sans-serif']; _mpl.rcParams['font.sans-serif']=['DejaVu Sans']
refs=[(1e48,'#8844ee','Long GRB / SN Ia'),(1e52,'#3377ee','Long GRB'),(1.2e55,'#ee4488','Extreme GRB (221009A)'),(1e36,'#33bb77','Typical FRB')]
for e,c,lbl in refs:
    axA.axhline(e,color=c,linewidth=1.2,linestyle=':',alpha=0.7)
    axA.text(1e64,e*1.4,lbl,color=c,fontsize=7.5,va='bottom',ha='right')

for mv,ml in [(1e5*M_SUN,'10⁵ M☉'),(1e6*M_SUN,'10⁶ M☉')]:
    axA.axvline(mv,color='#c86030',linewidth=1.2,linestyle='--',alpha=0.8)
    axA.text(mv*1.1,1e38,ml,color='#c86030',fontsize=8,rotation=90)

axA.axvline(M_MICRO,color='#2a88a3',linewidth=1.2,linestyle=':',alpha=0.8)
axA.text(M_MICRO*1.2,1e38,'Micro-Knot',color='#2a88a3',fontsize=7.5,rotation=90)

axA.set_xlim(1e24,1e65); axA.set_ylim(1e34,1e62)
axA.set_xlabel('Annihilated Knot Mass M [kg]',color=TXT,fontsize=10)
axA.set_ylabel('E_iso [erg]',color=TXT,fontsize=10)
axA.set_title('E_iso = η × 2Mc² — total released energy',color=TXT,fontsize=10.5)
axA.tick_params(colors=TXT,labelsize=8)
for sp in axA.spines.values(): sp.set_edgecolor('#bbbbbb')
axA.legend(fontsize=8, facecolor='white', edgecolor='#cccccc', labelcolor=TXT, loc='upper left')

# ---- Panel B ----
axB = fig.add_subplot(gs[0,1]); axB.set_facecolor(BG)
_,_,ats = axB.pie([33,51,10,3,3], labels=['Kinetic\nPlasma','γ/X','ν','Radio\n(FRB)','GW'],
    colors=['#e8b4c8','#a8e8b4','#f0d090','#c8b4e8','#88c8e8'],
    autopct='%1.0f%%', startangle=120, pctdistance=0.65,
    textprops={'color':TXT,'fontsize':9}, wedgeprops={'edgecolor':BG,'linewidth':1.5})
for at in ats: at.set_fontsize(9); at.set_color(TXT); at.set_fontweight('bold')
axB.set_title('Micro-Knot\nM ~ 10²⁴ kg',color='#2a88a3',fontsize=12,fontweight='bold')

# ---- Panel C ----
axC = fig.add_subplot(gs[1,0]); axC.set_facecolor(BG)
insts=['Athena\n(Soft X-ray)','PTA/SKA\n(GW nHz)','LISA\n(GW mHz)','IceCube\n(νHE)','VLBI jets\n(radio)','Swift BAT\n(X-ray)','Fermi GBM\n(γ-ray)','CHIME\n(radio FRB)','Roman\n(microlensing)']
emins=[1e46,1e45,1e44,1e44,1e44,1e43,1e43,1e38,1e38]
emaxs=[1e58,1e60,1e59,1e54,1e54,1e54,1e55,1e46,1e45]
cols=['#e8b4c8','#c8b4e8','#c8b4e8','#b4e8c8','#88c8e8','#88c8e8','#b4e8b4','#88c8e8','#7ec8e3']
for i,(inst,emin,emax,col) in enumerate(zip(insts,emins,emaxs,cols)):
    axC.barh(i,np.log10(emax)-np.log10(emin),left=np.log10(emin),color=col,alpha=0.85,edgecolor='#888888',height=0.6)

axC.axvline(np.log10(e_rad_erg(0.1,M_MICRO)),color='#2a88a3',linewidth=1.5,linestyle='--')
axC.text(np.log10(e_rad_erg(0.1,M_MICRO))+0.1,8.4,'Micro η=0.1',color='#2a88a3',fontsize=8,bbox=dict(facecolor='white',edgecolor='#2a88a3',boxstyle='round,pad=0.2'))

axC.axvline(np.log10(e_rad_erg(0.1,M_MACRO)),color='#c86030',linewidth=1.5,linestyle='--')
axC.text(np.log10(e_rad_erg(0.1,M_MACRO))+0.1,8.4,'Macro η=0.1',color='#c86030',fontsize=8,bbox=dict(facecolor='white',edgecolor='#c86030',boxstyle='round,pad=0.2'))

axC.set_yticks(range(len(insts))); axC.set_yticklabels(insts,color=TXT,fontsize=8.5)
axC.set_xlabel('log₁₀(E_iso [erg])',color=TXT,fontsize=10)
axC.set_title('Instrument observability windows vs released energy',color=TXT,fontsize=10)
axC.tick_params(colors=TXT,labelsize=8)
for sp in axC.spines.values(): sp.set_edgecolor('#bbbbbb')

# ---- Panel D ----
axD = fig.add_subplot(gs[1,1]); axD.set_facecolor(BG)
_,_,ats2 = axD.pie([26,9,13,13,39], labels=['γ/X\n(GRB)','ν HE','Radio\nJets','Soft X-ray\n(Athena)','GW\n(LISA/PTA)'],
    colors=['#b4e8b4','#f0d090','#88c8e8','#e8c8a8','#c8b4e8'],
    autopct='%1.0f%%', startangle=80, pctdistance=0.65,
    textprops={'color':TXT,'fontsize':9}, wedgeprops={'edgecolor':BG,'linewidth':1.5})
for at in ats2: at.set_fontsize(9); at.set_color(TXT); at.set_fontweight('bold')
axD.set_title('Std Macro-Knot\nM ~ 10⁵ M☉',color='#c86030',fontsize=12,fontweight='bold')

fig.suptitle('ECF — Knot+Anti-Knot Annihilation: energy release, partition and observability',
             color='#1f2d3d', fontsize=14, fontweight='bold', y=0.97)

fig.savefig('Fig_ecf_Annihilation.png', dpi=300, bbox_inches='tight', facecolor=BG)
print("Saved: Fig_ecf_Annihilation.png")
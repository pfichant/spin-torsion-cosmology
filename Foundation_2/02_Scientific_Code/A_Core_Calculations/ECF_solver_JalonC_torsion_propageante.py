import numpy as np
# [D3, 22/09/2026 -- DEC-A7-POST-05] Generic rounded background (Omega_m = 0.30, no H0): NOT the A-7 ECF background (0.267). Kept (qualitative).
Om,Orad=0.30,9.2e-5; W0T,WAT=-0.904,-0.153
N=400; lna=np.linspace(np.log(1e-3),0,N); a=np.exp(lna); z=1/a-1
h=lna[1]-lna[0]
def dd(y): return np.gradient(y,lna)
def run(xi,lam,V0,nit=18):
    E=np.sqrt(Om*a**-3+Orad*a**-4+V0); p=np.zeros(N); dp=np.zeros(N)
    for _ in range(nit):
        dlnE=dd(E)/np.maximum(E,1e-30)
        p=np.zeros(N); dp=np.zeros(N)
        for i in range(N-1):
            Ei=max(E[i],1e-30); Vp=-lam*V0*np.exp(-lam*p[i])
            ddp=-(dlnE[i]+3)*dp[i]-3*Vp/Ei**2-6*xi*p[i]*(dlnE[i]+2)
            dp[i+1]=dp[i]+h*ddp; p[i+1]=p[i]+h*dp[i+1]
            if not np.isfinite(p[i+1]) or abs(p[i+1])>30: return None
        F=1-xi*p**2; V=V0*np.exp(-lam*p); den=F-dp**2/6-2*xi*p*dp
        if np.any(den<=1e-3): return None
        E2=(Om*a**-3+Orad*a**-4+V)/den
        if np.any(E2<=0) or not np.all(np.isfinite(E2)): return None
        E=0.5*E+0.5*np.sqrt(E2)
    ODE=E**2-Om*a**-3-Orad*a**-4
    return E,ODE,-1-dd(ODE)/(3*np.where(np.abs(ODE)>1e-12,ODE,1e-12))
def shoot(xi,lam):
    lo,hi=0.2,1.5
    for _ in range(18):
        mid=0.5*(lo+hi); r=run(xi,lam,mid)
        if r is None: hi=mid; continue
        if r[0][-1]>1: hi=mid
        else: lo=mid
    return 0.5*(lo+hi)
print(" xi    lam |    w0       wa    | OmDE>0 | franchit -1 ?  z_cross")
print("-"*64); best=None
for xi in [0.0,0.1,0.3]:
    for lam in [0.4,0.8]:
        V0=shoot(xi,lam); r=run(xi,lam,V0)
        if r is None: print(f"{xi:>4.2f} {lam:>5.2f} |  (pas de solution stable)"); continue
        E,ODE,w=r; m=(z<=3)&(z>=0)
        if not np.all(np.isfinite(w[m])): continue
        w0=w[-1]; sel=z<1; wa=np.polyfit(1-a[sel],w[sel]-w0,1)[0]
        ok=ODE[m].min()>0; ww=w[m]; zz=z[m]
        idx=np.where(np.diff(np.sign(ww+1)))[0]
        cross=len(idx)>0 and ok; zc=zz[idx[0]] if len(idx) else float('nan')
        print(f"{xi:>4.2f} {lam:>5.2f} | {w0:>+8.4f} {wa:>+8.4f} | {'oui' if ok else 'NON':>5} | {'OUI' if cross else 'non':>4}   {zc:>6.2f}")
        if cross:
            e=(w0-W0T)**2+(wa-WAT)**2
            if best is None or e<best[0]: best=(e,xi,lam,w0,wa,zc)
print("-"*64)
print("MEILLEUR :", f"xi={best[1]}, lam={best[2]}, w0={best[3]:+.4f}, wa={best[4]:+.4f}, z_cross={best[5]:.2f}" if best else "AUCUN franchissement")

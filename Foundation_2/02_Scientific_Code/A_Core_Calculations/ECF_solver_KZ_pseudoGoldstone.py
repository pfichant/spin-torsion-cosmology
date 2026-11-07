import numpy as np
# [D3, 22/09/2026 -- DEC-A7-POST-05] Generic rounded background (Omega_m = 0.30, no H0): NOT the A-7 ECF background (0.267). Kept (qualitative).
Om,Orad=0.30,9.2e-5; W0T,WAT=-0.904,-0.153
N=800; lna=np.linspace(np.log(1e-3),0,N); a=np.exp(lna); z=1/a-1; h=lna[1]-lna[0]
def dd(y): return np.gradient(y,lna)
def run(f,th_i,V0,nit=12):
    """V = V0[1+cos(phi/f)] ; phi_i = th_i*f ; RK4."""
    E=np.sqrt(Om*a**-3+Orad*a**-4+V0*(1+np.cos(th_i)))
    for _ in range(nit):
        dlnE=dd(E)/np.maximum(E,1e-30)
        p=np.zeros(N); dp=np.zeros(N); p[0]=th_i*f
        def acc(i,pp,dpp):
            Ei=max(E[i],1e-30); Vp=-(V0/f)*np.sin(pp/f)
            return -(dlnE[i]+3)*dpp-3*Vp/Ei**2
        for i in range(N-1):
            k1=acc(i,p[i],dp[i]);            l1=dp[i]
            k2=acc(i,p[i]+.5*h*l1,dp[i]+.5*h*k1); l2=dp[i]+.5*h*k1
            k3=acc(i,p[i]+.5*h*l2,dp[i]+.5*h*k2); l3=dp[i]+.5*h*k2
            k4=acc(min(i+1,N-1),p[i]+h*l3,dp[i]+h*k3); l4=dp[i]+h*k3
            dp[i+1]=dp[i]+h*(k1+2*k2+2*k3+k4)/6
            p[i+1]=p[i]+h*(l1+2*l2+2*l3+l4)/6
            if not np.isfinite(p[i+1]) or abs(p[i+1])>60: return None
        V=V0*(1+np.cos(p/f)); den=1-dp**2/6
        if np.any(den<=1e-3) or np.any(V<-1e-12): return None
        E2=(Om*a**-3+Orad*a**-4+V)/den
        if np.any(E2<=0) or not np.all(np.isfinite(E2)): return None
        E=0.5*E+0.5*np.sqrt(E2)
    ODE=E**2-Om*a**-3-Orad*a**-4
    return E,ODE,-1-dd(ODE)/(3*np.where(np.abs(ODE)>1e-12,ODE,1e-12))
def shoot(f,th):
    lo,hi=0.05,2.0
    for _ in range(16):
        mid=.5*(lo+hi); r=run(f,th,mid)
        if r is None: hi=mid; continue
        if r[0][-1]>1: hi=mid
        else: lo=mid
    return .5*(lo+hi)
print("f FIXE par les nombres de l'ECF ; seule liberte = phase initiale theta_i (KZ : aleatoire, O(1))")
print("   f    theta_i |    w0        wa    | ecart cible")
print("-"*56); best=None
for f in [1.30,1.45]:
    for th in [0.6,1.0,1.4,1.8,2.2]:
        V0=shoot(f,th); r=run(f,th,V0)
        if r is None: continue
        E,ODE,w=r; w0=w[-1]; sel=z<1
        wa=np.polyfit(1-a[sel],w[sel]-w0,1)[0]
        if not np.isfinite(w0) or abs(w0)>3: continue
        e=np.hypot(w0-W0T,wa-WAT)
        mark=" <=" if (best is None or e<best[0]) else ""
        print(f" {f:>5.2f} {th:>8.2f} | {w0:>+9.4f} {wa:>+8.4f} |   {e:>7.4f}{mark}")
        if best is None or e<best[0]: best=(e,f,th,w0,wa,w,ODE)
print("-"*56)
if best:
    e,f,th,w0,wa,w,ODE=best
    print(f"MEILLEUR : f={f} M_Pl, theta_i={th} rad")
    print(f"   w0={w0:+.4f} (cible {W0T}) -> ecart {abs(w0-W0T)/abs(W0T)*100:.1f}%")
    print(f"   wa={wa:+.4f} (cible {WAT}) -> ecart {abs(wa-WAT)/abs(WAT)*100:.1f}%")
    m=(z<=3)&(z>=0); print(f"   w min (z<3) = {w[m].min():+.4f} ; Omega_DE>0 : {bool(ODE[m].min()>0)}")

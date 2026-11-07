import os, sys, json, numpy as np
sys.argv=['x']; sys.path.insert(0, os.environ['PKG'])
import ecf_cmb_seeds_planck_data as E
R=json.load(open('results_planck_data.json')); b=R['bestfit_f0']; p0={k:float(v) for k,v in b['params'].items()}; Ap0=float(b['A_planck'])
case=('edd','disk','spot')
ref=E.pmap([(p0,)+case+(1e-14,)])[0]; c_ref=E.chi2(ref[0],ref[1],Ap0); tau_ref=ref[1]
out={}
for f in (7e-10,8e-10,9e-10,1e-9):
    # 1. start: z_reio scan with ln10A shifted by 2*dtau
    zs=[0.8,1.2,1.6,2.0,2.5,3.0,3.5,4.0,4.5,5.0]
    R1=E.pmap([({**p0,'z_reio':z},)+case+(f,) for z in zs])
    best=None
    for z,r in zip(zs,R1):
        if r is None: continue
        q={**p0,'z_reio':z,'ln10A':p0['ln10A']+2*(r[1]-tau_ref)}
        best=min(best,(0,z,q),key=lambda t:t[0]) if best else (0,z,q)
    cands=[{**p0,'z_reio':z,'ln10A':p0['ln10A']+2*(r[1]-tau_ref)} for z,r in zip(zs,R1) if r is not None]
    R2=E.pmap([(q,)+case+(f,) for q in cands])
    cs=[E.chi2(r[0],r[1],Ap0) if r is not None else np.inf for r in R2]
    i=int(np.argmin(cs)); p=cands[i]; Ap=Ap0
    print(f"f={f:.0e}: start z_reio={p['z_reio']}, dchi2_start={cs[i]-c_ref:.2f}", flush=True)
    # 2. Jacobian at the start point (with injection), Gauss-Newton with line search
    JX,Jt=E.jacobian(p, case, f)
    st=E.fit_batch(p, Ap, case, [f], JX, Jt, nit=6)[0]
    JX,Jt=E.jacobian(st['p'], case, f)
    st=E.fit_batch(st['p'], st['Ap'], case, [f], JX, Jt, nit=6)[0]
    out[f]=dict(dchi2=st['c']-c_ref, tau=st['tau'], z_reio=st['p']['z_reio'])
    print(f"   profiled: dchi2={st['c']-c_ref:.2f}  tau={st['tau']:.4f}  z_reio={st['p']['z_reio']:.2f}  ln10A={st['p']['ln10A']:.4f}", flush=True)
json.dump({str(k):v for k,v in out.items()}, open('diag_soft2.json','w'), indent=1, default=float)

# Verification symbolique : Friedmann Einstein-Cartan par regime (fluide de spin : eps~ = p~ = -alpha n^2, n ~ a^-3)
import sympy as sp
t=sp.symbols('t'); k,al,r0,n0,w=sp.symbols('kappa alpha rho0 n0 w',positive=True)
a=sp.Function('a')(t)
for wv in [0, sp.Rational(1,3), 1]:
    rho=r0*a**(-3*(1+wv)); n=n0*a**-3; p=wv*rho
    rt=rho-al*n**2; pt=p-al*n**2            # densite et pression totales
    H2=k/3*rt
    # Raychaudhuri : addot/a = -(k/6)(rt+3pt) ; verifier qu'elle derive de H2 (continuite totale)
    ray=-(k/6)*(rt+3*pt)
    # d/dt(H^2 a^2) = 2 adot addot  ->  addot/a = H2 + a/2 d(H2)/da
    A=sp.symbols('A',positive=True)
    H2A=H2.subs(a,A); deriv=sp.simplify(H2A + A/2*sp.diff(H2A,A))
    print('w=',wv,' coherence Raychaudhuri:',sp.simplify(deriv-ray.subs(a,A))==0)
    # en variable rho : alpha n^2 = rho*(rho/rhoc)^((1-w)/(1+w))
    R,rc=sp.symbols('R rho_c',positive=True)
    if wv!=1:
        e=(1-wv)/(1+wv)
        acc=-(k/6)*((1+3*wv)*R-4*R*(R/rc)**e)
        sol=sp.solve(sp.Eq((1+3*wv),4*(R/rc)**e),R)
        print('   addot/a au rebond (R=rc):',sp.simplify(acc.subs(R,rc)),'  changement de signe rho*/rho_c =',[sp.nsimplify(s/rc) for s in sol])
        ch5a=-(k/6)*(R*(1-4*R/rc)+3*wv*R*(1-2*R/rc))
        print('   CH5-A (schema) au rebond:',sp.simplify(ch5a.subs(R,rc)),'  changement de signe:',[sp.nsimplify(s/rc) for s in sp.solve(ch5a/R,R)])
    else:
        print('   stiff : alpha n^2/rho = cste ; H^2 = (k/3) rho (1-eps_s) : pas de zero pour eps_s<1')

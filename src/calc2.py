import numpy as np
from scipy.optimize import brentq
np.set_printoptions(precision=4, suppress=True)
d=np.degrees
print("== A: K(s+1)/(s(s+2)(s+3)(s+4))")
den=np.poly([0,-2,-3,-4]); num=np.array([1,1.])
print("den",den)
# breakaway: d/ds [den/num]=0 -> den'*num - den*num' = 0
q=np.polysub(np.polymul(np.polyder(den),num), np.polymul(den,np.polyder(num)))
r=np.roots(q); print("bk cand", r)
for s in r:
    if abs(s.imag)<1e-9: print(" s",s.real,"K", -np.polyval(den,s.real)/np.polyval(num,s.real))
print("K=.659 poles", np.roots(np.polyadd(den,0.659*num)))
# Routh for jw: char s^4+9s^3+26s^2+(24+K)s+K
Ks=np.linspace(0.01,300,300000)
def maxre(K): return max(np.roots(np.polyadd(den,K*num)).real)
Kc=brentq(maxre,1,300); print("Kcrit",Kc, np.roots(np.polyadd(den,Kc*num)))
print("== B: K(s-2)^2/((s-1)(s^2+2s+2))")
den=np.polymul([1,-1],[1,2,2]); num=np.polymul([1,-2],[1,-2]); print("char", np.polyadd(den,[0]+list(num)) )
for K in [0.1,1,10]: print(K, np.roots(np.polyadd(den,K*num)))
print("== C: K/(s(s+1)(s^2+4s+13))")
den=np.polymul([1,1,0],[1,4,13]); print(den)
print("bk", np.roots(np.polyder(den)), "K", [-np.polyval(den,x) for x in np.roots(np.polyder(den)) if abs(x.imag)<1e-9])
Kc=37.44; print("Kc roots", np.roots(np.polyadd(den,[Kc])))
p=-2+3j; th=d(np.angle(p-0))+d(np.angle(p+1))+d(np.angle(p-(-2-3j)))
print("departure", 180-th)
print("== D: 1/(s(s+20))")
os_=.315; z=-np.log(os_)/np.sqrt(np.pi**2+np.log(os_)**2); wn=10/z; wd=wn*np.sqrt(1-z*z); print(z,wn,wd, "K",wn**2)
print("== E: 1/((s+1)(s+3)(s+5))")
den=np.poly([-1,-3,-5])
sd=complex(-4/5.698, 3.44); print("sd",sd, "angle", -sum(d(np.angle(sd-p)) for p in [-1,-3,-5]), "K", np.prod([abs(sd-p) for p in [-1,-3,-5]]))
# exact zeta .2 line point
def g(wn):
    s=wn*complex(-.2,np.sqrt(1-.04)); return sum(d(np.angle(s-p)) for p in [-1,-3,-5])-180
wn=brentq(g,1,6); s=wn*complex(-.2,np.sqrt(.96)); K=np.prod([abs(s-p) for p in [-1,-3,-5]]); print("exact z=.2",s,K, "ts",4/-s.real, np.roots(np.polyadd(den,[K])))
r=np.roots(np.polyadd(den,[78.7])); print("K78.7 poles",r)
dd=r[np.argmax(r.imag)]; ts=4/-dd.real; zz=-dd.real/abs(dd); OS=np.exp(-np.pi*zz/np.sqrt(1-zz*zz)); print("ts",ts,"z",zz,"OS",OS)
# b) 3.5x faster, OS half
ts2=5.698/3.5; sig=4/ts2; OS2=.526/2; z2=-np.log(OS2)/np.sqrt(np.pi**2+np.log(OS2)**2); wd2=sig*np.sqrt(1-z2*z2)/z2
sd2=complex(-sig,wd2); print("b) ts",ts2,"sig",sig,"z",z2,"sd",sd2)
ang=-sum(d(np.angle(sd2-p)) for p in [-1,-3,-5]); print("plant angle",ang, "deficit", -180-ang)

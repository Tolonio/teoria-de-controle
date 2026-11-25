import numpy as np
from numpy.polynomial import polynomial as P
from scipy.optimize import brentq
np.set_printoptions(precision=4, suppress=True)
# Base: G=K/(s(s+1)(s+2))
print("K=1 poles", np.roots([1,3,2,1]))
# breakaway: dK/ds=0, K=-(s^3+3s^2+2s) -> 3s^2+6s+2=0
print("breakaway", np.roots([3,6,2]), "K at", -np.polyval([1,3,2,0], np.roots([3,6,2])))
# zeta=0.5 point: s = -zeta wn + j wn sqrt(1-z^2); angle condition
def ang(s): return np.angle(1/(s*(s+1)*(s+2)))
z=0.5
f=lambda wn: np.unwrap([np.angle(1/((s:=complex(-z*wn, wn*np.sqrt(1-z**2)))*(s+1)*(s+2)))])[0]
for wn in np.linspace(0.1,3,30): pass
def g(wn):
    s=complex(-z*wn, wn*np.sqrt(1-z**2))
    return np.degrees(np.angle(s)+np.angle(s+1)+np.angle(s+2))-180
wn=brentq(g,0.1,2); s=complex(-z*wn, wn*np.sqrt(1-z**2))
K=abs(s*(s+1)*(s+2)); print("zeta.5 wn",wn,"s",s,"K",K, "poles", np.roots([1,3,2,K]))
# zeta of K=1 dominant
p=np.roots([1,3,2,1]); d=p[np.argmax(p.imag)]; wn1=abs(d); print("K=1 wn",wn1,"zeta",-d.real/wn1)
# Kv with K=1
print("Kv",1/2,"ess ramp",2)
# Lag: Gc=Kc (s+0.05)/(s+0.005) ; FTMA= Kc(s+0.05)/((s+0.005)s(s^2+3s+2))
den=np.polymul([1,0.005],[1,3,2,0]); num=[1,0.05]
def char(Kc): return np.polyadd(den, Kc*np.array(num))
for Kc in [1,0.975,0.95]:
    r=np.roots(char(Kc)); dd=r[np.argmax(r.imag)]; print("lag Kc",Kc,r, "zeta",-dd.real/abs(dd), "Kv", Kc*0.05/0.005/2, "ess",1/(Kc*10/2))
# find Kc so that dominant zeta=0.5147 (keep zeta of original)
zt=-d.real/wn1
def h(Kc):
    r=np.roots(char(Kc)); dd=r[np.argmax(r.imag)]; return -dd.real/abs(dd)-zt
Kc=brentq(h,0.5,1.2); r=np.roots(char(Kc)); print("Kc for same zeta",Kc,r)
# angle contributed by lag at sd
sd=d; print("lag angle at sd deg", np.degrees(np.angle(sd+0.05)-np.angle(sd+0.005)), "mag", abs((sd+0.05)/(sd+0.005)))
print("expanded den", den, "char Kc=0.975", char(0.975))

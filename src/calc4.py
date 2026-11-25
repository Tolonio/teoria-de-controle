import numpy as np
from scipy import signal, optimize
np.set_printoptions(precision=4, suppress=True)
# motor
Ra,La,K,J,B=1,0.5,0.5,0.1,0.1
den=np.polyadd(np.polymul([J,B],[La,Ra]),[K*K]); print("motor den",den, den/den[0], "roots",np.roots(den), "dc", K/den[-1])
d=den/den[0]; n=K/den[0]; print("w/V =",n,"/",d)
# P control steady error with Kp
for Kp in [1,2,5]:
    cl=np.polyadd(d,[Kp*n]); r=np.roots(cl); print("P",Kp,r,"ess",1-Kp*n/cl[-1])
# PI: C=Kp(s+z)/s choose z=2 ; find Kp with zeta .7 on dominant
z=2
def zeta(Kp):
    cl=np.polyadd(np.polymul(d,[1,0]), Kp*n*np.array([1,z])); r=np.roots(cl); dd=r[np.argmax(r.imag)]
    return -dd.real/abs(dd) if abs(dd.imag)>1e-6 else 1
for Kp in [0.2,0.4,0.6,0.8,1,1.5]:
    cl=np.polyadd(np.polymul(d,[1,0]), Kp*n*np.array([1,z])); print("PI",Kp,np.roots(cl), zeta(Kp))
# Nyquist G=K/((s+1)(s+2)(s+3))
w=np.sqrt(11); G=1/np.polyval(np.poly([-1,-2,-3]),1j*w); print("cross",w,G)
# margins K=30
for Kn in [30]:
    f=lambda w: abs(Kn/np.polyval(np.poly([-1,-2,-3]),1j*w))-1
    wc=optimize.brentq(f,0.1,10); ph=np.degrees(np.angle(Kn/np.polyval(np.poly([-1,-2,-3]),1j*wc))); print("wc",wc,"PM",180+ph,"GM",60/Kn, 20*np.log10(60/Kn))
# state space
A=np.array([[0,1],[-2,-2]]);Bm=np.array([[0],[1]])
Kss=signal.place_poles(A,Bm,[-4+3j,-4-3j]).gain_matrix; print("K",Kss, np.linalg.eigvals(A-Bm@Kss))
# z
T=0.1;a=np.exp(-T);print("z pole",a,1-a,"Kmax",(1+a)/(1-a))
for T in [0.1,0.5,1]: a=np.exp(-T); print(T,"Kmax",(1+a)/(1-a))

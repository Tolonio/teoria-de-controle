import numpy as np
from scipy.optimize import brentq
d=np.degrees; R=np.radians
def ang(s,pts): return sum(d(np.angle(s-p)) for p in pts)
print("== E b) PID for 1/((s+1)(s+3)(s+5))")
sd=complex(-2.457,5.779)
need=-180-(-ang(sd,[-1,-3,-5]))+2   # PD must give deficit+2
zpd=-sd.real + sd.imag/np.tan(R(need)); print("PD angle",need,"zpd",zpd)
a0=d(np.angle(sd)); target=a0-2; zi= -sd.real - sd.imag/np.tan(R(180-target)); print("PI zero",zi, "check", d(np.angle(sd+zi))-a0)
zs=[-zpd,-zi]; ps=[0,-1,-3,-5]
print("total angle", ang(sd,zs)-ang(sd,ps))
K=np.prod([abs(sd-p) for p in ps])/np.prod([abs(sd-z) for z in zs]); print("K",K)
num=K*np.poly(zs); den=np.poly(ps); cl=np.polyadd(den,num); r=np.roots(cl); print("CL",r)
print("Kd,Kp,Ki", K, K*(zpd+zi), K*zpd*zi)
import scipy.signal as sg
t=np.linspace(0,8,4000); _,y=sg.step((num,cl),T=t); print("OS",y.max()-1, "ts", t[np.where(abs(y-1)>.02)[0][-1]], "yfinal", y[-1])
print("== F PID for K/(s^2+5s+4)")
sd=complex(-4,3); print("PD zero angle", 180+ang(sd,[-1,-4]) -360)
zs=[-7,-0.1]; ps=[0,-1,-4]
# find point on zeta .8 line satisfying angle with PID
def g(wn):
    s=wn*complex(-.8,.6); return ang(s,zs)-ang(s,ps)+180
for wn in np.linspace(1,8,15): print(round(wn,2), round(g(wn),2))
wn=brentq(g,4.5,5.2); s=wn*complex(-.8,.6); Kt=np.prod([abs(s-p) for p in ps])/np.prod([abs(s-z) for z in zs]); print("pt",s,"Ktot",Kt, "Kc=",Kt/5.76)
num=Kt*np.poly(zs); den=np.poly(ps); cl=np.polyadd(den,num); print("CL", np.roots(cl))
t=np.linspace(0,10,4000); _,y=sg.step((num,cl),T=t); print("OS",y.max()-1,"tp",t[y.argmax()],"ts", t[np.where(abs(y-1)>.02)[0][-1]])
# PD only check
num=3*np.poly([-7]); den=np.poly([-1,-4]); cl=np.polyadd(den,num); print("PD only K=3 CL", np.roots(cl))
print("== G lead 200/((s+10)(s+30))")
sd=complex(-40,20); print(ang(sd,[-10,-30]))
num=2.5*200; cl=np.polyadd(np.poly([-30,-50]),[num]); print(np.roots(cl), "Kp before", 200/300, "after", 500/1500)
print("== PI Routh 1/((s+1)(s+2)): s^3+3s^2+(2+Kp)s+Ki -> Ki<3(2+Kp)")

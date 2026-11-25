import numpy as np
from scipy import signal, optimize
pi=np.pi
print("== Ex 14.1"); If=220/147; Ia=45/(0.7032*If); w=1200*pi/30; Eg=0.7032*w*If; print(If,Ia,Eg,0.25*Ia+Eg, 15*746/220)
print("== Ex 14.8"); Va=.6*600; Eg=Va-.05*250; print(Va,Eg,Eg/(1.527*2.5),Eg/(1.527*2.5)*30/pi,1.527*250*2.5, 600/(250*.6))
print("== Ex 14.13"); If=1.4;Kv=.91;K1=.095;K2=100;Rm=.1;B=.3;wn=1700*pi/30;TL=50000/wn
g=Kv*If/(Rm*B+(Kv*If)**2); Va=wn/g; Vb=K1*wn; Vr=Vb+Va/K2; print("TL",TL,"g",g,"Va",Va,"Vb",Vb,"Vr",Vr)
den=Rm*B+(Kv*If)**2+K1*K2*Kv*If
dc=-Rm*TL/den; print("c dw",dc, wn+dc, (wn+dc)*30/pi)
dd=-Rm*1.1*TL/den; print("d",dd,wn+dd,(wn+dd)*30/pi)
de=-K2*Kv*If*0.1*Vr/den; print("e",de,wn+de,(wn+de)*30/pi)
print("f",wn+dd+de,(wn+dd+de)*30/pi)
d0=Rm*B+(Kv*If)**2; dg=-Rm*TL/d0; print("g",K2*Kv*If*2.31/d0, dg, wn+dg,(wn+dg)*30/pi, "reg",(1700-(wn+dg)*30/pi)/((wn+dg)*30/pi)*100)
print("h reg", (1700-(wn+dc)*30/pi)/((wn+dc)*30/pi)*100)
print("== Ex 14.14"); Rm=6.5;J=.06;Lm=.067;B=.087;Kb=1.24;Vs=220/np.sqrt(3);Kr=2.339*Vs/10;taur=1/(12*60)
Vc=220/(Kr*10)*10; Hc=Vc/20; Km=B/(Kb**2+Rm*B)
a=Rm/Lm+B/J; c=(Rm*B+Kb**2)/(J*Lm); r=np.roots([1,a,c]); t1,t2=-1/r.real.max(),-1/r.real.min(); taum=J/B
print("Vs",Vs,"Kr",Kr,"taur",taur,"Vc",Vc,"Hc",Hc,"Km",Km,"roots",r,"t1",t1,"t2",t2,"taum",taum)
tauc=t2; Kc=0.5*t1*tauc/(taur*Km*Kr*Hc*taum); K1_=Km*Kc*Kr*Hc*taum/tauc; Ki=(1/Hc)*K1_/(1+K1_); t3=t1+taur; ti=t3/(1+K1_)
te=ti+.002; Kw=Ki*Kb*.074/(B*taum); Ks=1/(2*Kw*te); taus=4*te
print("tauc",tauc,"Kc",Kc,"K1",K1_,"Ki",Ki,"t3",t3,"ti",ti,"te",te,"Kw",Kw,"Ks",Ks,"taus",taus)
# open-loop motor w/Va
num=[Kb]; den=np.polyadd(np.polymul([Lm,Rm],[J,B]),[Kb**2]); print("w/Va poles",np.roots(den),"dc",Kb/den[-1])
# ZN 2nd method on speed loop: Vc -> Kr/(1+s taur) -> motor -> tacho .074/(1+.002s)
L=np.polymul(np.polymul([taur,1],den),[.002,1]); N=Kr*Kb*.074
def mr(K): return max(np.roots(np.polyadd(L,[K*N])).real)
Kcr=optimize.brentq(mr,0.01,1e4); rr=np.roots(np.polyadd(L,[Kcr*N])); w=max(abs(rr.imag)); Pcr=2*pi/w
print("Kcr",Kcr,"w",w,"Pcr",Pcr)
Kp=.6*Kcr;Ti=.5*Pcr;Td=.125*Pcr;print("ZN PID",Kp,Ti,Td, "Ki",Kp/Ti,"Kd",Kp*Td)
# class plant
L2=[1,3,2,0]; Kcr2=6; Pcr2=2*pi/np.sqrt(2); print("aula Pcr",Pcr2, .6*Kcr2,.5*Pcr2,.125*Pcr2)
# step of eq 14.124 and 14.126 (per unit 1/Kw)
t=np.linspace(0,40,4000)  # in units of te
y1=1+np.exp(-t/2)-2*np.exp(-t/4)*np.cos(np.sqrt(3)*t/4)
y2=1+np.exp(-t/4)-2/np.sqrt(3)*np.exp(-t/4)*np.sin(np.sqrt(3)*t/4)
for y in (y1,y2):
    os_=y.max()-1; tr=t[np.argmax(y>=1)]; idx=np.where(abs(y-1)>.02)[0]; print("OS",os_,"tr",tr,"ts",t[idx[-1]])

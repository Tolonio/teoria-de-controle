import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import signal
plt.rcParams.update({"font.size": 10, "font.family": "DejaVu Sans", "savefig.dpi": 200, "savefig.bbox": "tight", "axes.grid": True, "grid.alpha": .3})
BLUE, RED, GREEN, ORANGE, GRAY, PURPLE = "#1f5fa8", "#c0392b", "#1e8449", "#d35400", "#555", "#7d3c98"
def save(n): plt.savefig(f"fig/{n}.png"); plt.close()

# ---- especificações da resposta transitória
z, wn = 0.4, 1.0; t = np.linspace(0, 14, 3000); _, y = signal.step(([wn**2], [1, 2*z*wn, wn**2]), T=t)
fig, ax = plt.subplots(figsize=(8, 3.6)); ax.plot(t, y, color=BLUE, lw=2.4); ax.axhline(1, color="k", lw=.8)
ax.axhspan(.98, 1.02, color="#d5f5e3", alpha=.7); ax.text(13.9, 1.035, "faixa de ±2%", ha="right", fontsize=8.5, color=GREEN)
td = t[np.argmax(y >= .5)]; t10 = t[np.argmax(y >= .1)]; t90 = t[np.argmax(y >= .9)]; tp = t[y.argmax()]; idx = np.where(abs(y - 1) > .02)[0]; ts = t[idx[-1]]
ax.plot(td, .5, "o", color=GRAY); ax.annotate("td: atraso (50%)", (td, .5), (td + .6, .35), fontsize=9, color=GRAY, arrowprops=dict(arrowstyle="->", color=GRAY))
ax.annotate("", (t90, .2), (t10, .2), arrowprops=dict(arrowstyle="<->", color=ORANGE)); ax.text((t10 + t90) / 2, .1, "tr: subida (10–90%)", ha="center", fontsize=9, color=ORANGE)
ax.plot([tp, tp], [0, y.max()], ":", color=RED); ax.annotate(f"Mp: sobressinal = {100*(y.max()-1):.0f}%", (tp, y.max()), (tp + .8, 1.3), fontsize=9, color=RED, arrowprops=dict(arrowstyle="->", color=RED))
ax.text(tp, -.12, "tp", ha="center", color=RED, fontsize=9)
ax.plot([ts, ts], [0, 1], ":", color=GREEN); ax.text(ts, -.12, "ts: acomodação", ha="center", color=GREEN, fontsize=9)
ax.set_ylim(-.2, 1.5); ax.set_xlabel("t (s)"); ax.set_title("Especificações da resposta transitória ao degrau (2ª ordem, ζ = 0,4, ωn = 1)", fontsize=10)
save("resp_transitoria")

# ---- ordem superior: polo extra e zero extra
t = np.linspace(0, 12, 3000); base = ([1], [1, 1, 1])
cases = [("2ª ordem pura: 1/(s²+s+1)", base, GRAY, "-"),
         ("+ polo em −1 (lento): mais lento, menos sobressinal", ([1], np.polymul([1, 1, 1], [1, 1])), BLUE, "-"),
         ("+ zero em −1: mais rápido, MAIS sobressinal", ([1, 1], [1, 1, 1]), RED, "-"),
         ("+ zero em +1 (semiplano direito): começa ao contrário", ([-1, 1], [1, 1, 1]), PURPLE, "--")]
fig, ax = plt.subplots(figsize=(8, 3.4))
for lab, sys, c, ls in cases:
    _, yy = signal.step(sys, T=t); ax.plot(t, yy, color=c, ls=ls, lw=2, label=lab)
ax.axhline(1, color="k", ls=":", lw=.8); ax.legend(fontsize=8.5); ax.set_xlabel("t (s)"); ax.set_title("Ordem superior: o que um polo ou um zero a mais faz com a resposta", fontsize=10)
save("ordem_superior")

# ---- realimentação positiva x negativa
t = np.linspace(0, 4, 800)
fig, axs = plt.subplots(1, 2, figsize=(10, 3.2))
ax = axs[0]
for K, c in [(0.5, GREEN), (1.0, ORANGE), (1.5, RED)]:
    p = K - 1; yy = (np.exp(p * t) - 1) / p if p != 0 else t
    ax.plot(t, yy, color=c, lw=2, label=f"positiva, K = {K}: polo em s = {p:+.1f}")
_, yn = signal.step(([1.5], [1, 2.5]), T=t); ax.plot(t, yn, color=BLUE, lw=2, ls="--", label="negativa, K = 1,5: polo em s = −2,5")
ax.set_ylim(0, 5); ax.legend(fontsize=7.8, loc="upper left"); ax.set_xlabel("t (s)"); ax.set_title("Planta 1/(s+1) com realimentação de ganho K", fontsize=9.5)
ax = axs[1]; K = np.linspace(0, 3, 50)
ax.plot(K, -1 - K, color=BLUE, lw=2.4, label="negativa: s = −(1 + K)"); ax.plot(K, -1 + K, color=RED, lw=2.4, label="positiva: s = K − 1")
ax.axhspan(0, 2.2, color="#fadbd8", alpha=.6); ax.axhline(0, color="k", lw=.8); ax.set_xlabel("ganho K"); ax.set_ylabel("polo de malha fechada"); ax.legend(fontsize=8); ax.set_title("Onde vai o polo", fontsize=9.5)
plt.tight_layout(); save("realim_positiva")

# ---- Bode do motor do Exemplo 14.14 (Rashid)
Rm, Lm, J, B, Kb = 6.5, .067, .06, .087, 1.24
den = np.polyadd(np.polymul([Lm, Rm], [J, B]), [Kb**2]); w = np.logspace(-1, 3.3, 600)
G = Kb / np.polyval(den, 1j * w)
fig, axs = plt.subplots(2, 1, figsize=(8, 4.8), sharex=True)
axs[0].semilogx(w, 20 * np.log10(abs(G)), color=BLUE, lw=2.2); axs[0].set_ylabel("|ω/Va| (dB)")
axs[1].semilogx(w, np.degrees(np.angle(G)), color=BLUE, lw=2.2); axs[1].set_ylabel("fase (°)"); axs[1].set_xlabel("frequência da tensão aplicada ω (rad/s)")
for wc, lab in [(5.64, "polo mecânico\n5,64 rad/s"), (92.8, "polo elétrico\n92,8 rad/s")]:
    for a in axs: a.axvline(wc, color=ORANGE, ls=":", lw=1.2)
    axs[0].text(wc * 1.08, -15 if wc < 50 else -45, lab, fontsize=8.5, color=ORANGE)
axs[0].text(.12, -10.5, "ganho estático 0,59 (rad/s)/V = −4,6 dB", fontsize=8.5); axs[0].text(14, -32, "−20 dB/déc", fontsize=8.5, color=GRAY); axs[0].text(400, -72, "−40 dB/déc", fontsize=8.5, color=GRAY)
axs[1].text(.12, -150, "fase vai de 0° a −180° (um −90° por polo)", fontsize=8.5)
axs[0].set_title("Bode do motor CC do Exemplo 14.14 (Rashid): ω(s)/Va(s) = 1,24/[(0,067s+6,5)(0,06s+0,087)+1,24²]", fontsize=9.3)
plt.tight_layout(); save("bode_motor")

# ---- ideia física do Bode: senoide entrando e saindo
fig, axs = plt.subplots(1, 3, figsize=(11, 2.6), sharey=True)
for ax, ww in zip(axs, [0.5, 5.64, 60]):
    Gw = Kb / np.polyval(den, 1j * ww); tt = np.linspace(0, 3 * 2 * np.pi / ww, 500)
    ax.plot(tt, np.sin(ww * tt), color=GRAY, label="tensão (1 V de pico)")
    ax.plot(tt, abs(Gw) / 0.59 * np.sin(ww * tt + np.angle(Gw)), color=BLUE, lw=2, label="velocidade (normalizada)")
    ax.set_title(f"ω = {ww} rad/s: ganho {abs(Gw)/0.59:.2f}, atraso {-np.degrees(np.angle(Gw)):.0f}°", fontsize=9); ax.set_xlabel("t (s)")
axs[0].legend(fontsize=7.5, loc="lower left"); plt.tight_layout(); save("bode_fisico")

# ---- Rashid: malha de velocidade otimizada (Eq. 14.123) x com compensador (Eq. 14.125), tau_e = 4,76 ms
te = 4.756e-3; t = np.linspace(0, 40 * te, 3000)
_, y1 = signal.step(([4 * te, 1], [8 * te**3, 8 * te**2, 4 * te, 1]), T=t); _, y2 = signal.step(([1], [8 * te**3, 8 * te**2, 4 * te, 1]), T=t)
fig, ax = plt.subplots(figsize=(8, 3.2)); ax.plot(t * 1000, y1, color=RED, lw=2.2, label="ótimo simétrico (Eq. 14.123): sobressinal 43,4%")
ax.plot(t * 1000, y2, color=GREEN, lw=2.2, label="com rede de compensação polo-zero (Eq. 14.125): 8,1%"); ax.axhline(1, color="k", ls=":", lw=.8)
ax.set_xlabel("t (ms)"); ax.set_ylabel("ω / ω*"); ax.legend(fontsize=8.5); ax.set_title("Malha de velocidade do Exemplo 14.14 (τe = 4,76 ms, Ks = 25,85, τs = 19,02 ms)", fontsize=9.5)
save("rashid_velocidade")

# ---- Rashid Ex 14.13: velocidade x torque de carga, malha aberta x fechada
wn = 1700 * np.pi / 30; TLn = 50000 / wn; TL = np.linspace(0, 1.2 * TLn, 50)
d0 = 0.1 * 0.3 + (0.91 * 1.4) ** 2; d1 = d0 + 0.095 * 100 * 0.91 * 1.4
fig, ax = plt.subplots(figsize=(7.5, 3.2))
ax.plot(TL, (wn - 0.1 * TL / d0) * 30 / np.pi, color=RED, lw=2.2, label="malha aberta: cai 163 rpm a plena carga (regulação 10,55%)")
ax.plot(TL, (wn - 0.1 * TL / d1) * 30 / np.pi, color=GREEN, lw=2.2, label="malha fechada: cai 19,5 rpm (regulação 1,16%)")
ax.axvline(TLn, color=GRAY, ls=":"); ax.text(TLn * 1.01, 1690, "torque nominal\n280,9 N·m", fontsize=8.5, color=GRAY)
ax.set_xlabel("torque de carga TL (N·m)"); ax.set_ylabel("velocidade (rpm)"); ax.legend(fontsize=8.5, loc="lower left")
ax.set_title("Exemplo 14.13 (Rashid): motor de 50 kW, 1700 rpm", fontsize=10); save("rashid_regulacao")

# ---- Ziegler-Nichols: aula e malha de velocidade do Ex. 14.14
fig, axs = plt.subplots(1, 2, figsize=(10.5, 3.2))
t = np.linspace(0, 25, 5000)
Kp, Ti, Td = 3.6, 2.2214, 0.5554
num = np.array([Kp * Td, Kp, Kp / Ti]); dpl = [1, 3, 2, 0]; den = np.polyadd(np.polymul(dpl, [1, 0]), num)
_, y = signal.step((num, den), T=t); _, yP = signal.step(([3.0], np.polyadd(dpl, [3.0])), T=t)
axs[0].plot(t, yP, color=GRAY, label="P com 0,5·Kcr = 3"); axs[0].plot(t, y, color=BLUE, lw=2, label="PID de Ziegler-Nichols"); axs[0].axhline(1, color="k", ls=":")
axs[0].legend(fontsize=8); axs[0].set_title("Planta da aula 1/[s(s+1)(s+2)]: Kcr = 6, Pcr = 4,44 s", fontsize=9.5); axs[0].set_xlabel("t (s)")
taur = 1 / 720; Lp = np.polymul(np.polymul([taur, 1], np.polyadd(np.polymul([Lm, Rm], [J, B]), [Kb**2])), [.002, 1]); N = 29.709 * Kb * .074
Kp, Ti, Td = 30.03, .01899, .004747
C = np.array([Kp * Td, Kp, Kp / Ti]); num = N * C; den = np.polyadd(np.polymul(Lp, [1, 0]), num)
t = np.linspace(0, .3, 6000); _, y = signal.step((num, den), T=t)
axs[1].plot(t * 1000, y, color=BLUE, lw=2, label="PID de Ziegler-Nichols"); axs[1].axhline(1, color="k", ls=":"); axs[1].legend(fontsize=8)
axs[1].set_title("Malha de velocidade do Ex. 14.14: Kcr = 50, Pcr = 38 ms", fontsize=9.5); axs[1].set_xlabel("t (ms)"); axs[1].set_ylabel("velocidade medida / referência")
plt.tight_layout(); save("zn")
for nm, yy in [("aula", None)]: pass
print("ok")

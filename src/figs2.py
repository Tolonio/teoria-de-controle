import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon
from scipy import signal
plt.rcParams.update({"font.size": 10, "font.family": "DejaVu Sans", "axes.grid": True,
                     "grid.alpha": .3, "savefig.dpi": 200, "savefig.bbox": "tight"})
BLUE, RED, GREEN, ORANGE, GRAY, PURPLE = "#1f5fa8", "#c0392b", "#1e8449", "#d35400", "#555", "#7d3c98"

def rlocus(num, den, Ks):
    out, prev = [], None
    for K in Ks:
        r = np.roots(np.polyadd(den, K * np.asarray(num, float)))
        if prev is not None:
            rr = list(r); r = np.array([rr.pop(int(np.argmin([abs(p - x) for x in rr]))) for p in prev])
        out.append(r); prev = r
    return np.array(out)
def save(n): plt.savefig(f"fig/{n}.png"); plt.close()
def axes0(ax):
    ax.axhline(0, color="k", lw=.7); ax.axvline(0, color="k", lw=.7)

# ---- A: K(s+1)/(s(s+2)(s+3)(s+4))
den = np.poly([0, -2, -3, -4]); num = [1, 1]
Ks = np.concatenate([np.linspace(0, .6586, 400), np.linspace(.6586, .66, 50), np.linspace(.66, 400, 4000)])
R = rlocus(num, den, Ks)
fig, ax = plt.subplots(figsize=(6.5, 5))
for i in range(R.shape[1]): ax.plot(R[:, i].real, R[:, i].imag, color=BLUE, lw=1.8)
ax.plot([0, -2, -3, -4], [0] * 4, "x", color="k", ms=10, mew=2); ax.plot(-1, 0, "o", mfc="white", mec="k", ms=9, mew=2)
for a in [60, -60]: ax.plot([-8/3, -8/3 + 8 * np.cos(np.radians(a))], [0, 8 * np.sin(np.radians(a))], ":", color=GRAY)
ax.plot(-8/3, 0, "o", mfc="white", mec=GRAY); ax.annotate("σa = −2,67", (-8/3, 0), (-4.6, -1.3), color=GRAY, fontsize=9, arrowprops=dict(arrowstyle="->", color=GRAY))
ax.plot(-2.39, 0, "s", color=ORANGE); ax.annotate("saída: s = −2,39\nK = 0,659", (-2.39, 0), (-4.9, 2.2), color=ORANGE, fontsize=9, arrowprops=dict(arrowstyle="->", color=ORANGE))
for s in [1, -1]: ax.plot(0, s * 4.279, "D", color=RED)
ax.annotate("cruza jω: ±j4,28\nK = 140,8", (0, 4.279), (.4, 3.2), color=RED, fontsize=9, arrowprops=dict(arrowstyle="->", color=RED))
axes0(ax); ax.set_xlim(-5, 2.5); ax.set_ylim(-6, 6); ax.set_aspect("equal")
ax.set_title("LGR de K(s+1) / [s(s+2)(s+3)(s+4)]", fontsize=10); save("lgr_A")

# ---- B: K(s-2)^2/((s-1)(s^2+2s+2))
den = np.polymul([1, -1], [1, 2, 2]); num = np.polymul([1, -2], [1, -2])
Ks = np.concatenate([np.linspace(0, 1, 800), np.linspace(1, 300, 3000)])
R = rlocus(num, den, Ks)
fig, ax = plt.subplots(figsize=(6.5, 4.2))
ax.axvspan(0, 4, color="#fadbd8", alpha=.5)
for i in range(R.shape[1]): ax.plot(R[:, i].real, R[:, i].imag, color=BLUE, lw=1.8)
ax.plot([1, -1, -1], [0, 1, -1], "x", color="k", ms=10, mew=2); ax.plot(2, 0, "o", mfc="white", mec="k", ms=11, mew=2)
ax.text(2.05, .2, "zero duplo\nem +2", fontsize=8.5)
ax.text(.15, 1.6, "semiplano direito", color=RED, fontsize=9)
axes0(ax); ax.set_xlim(-5, 3.2); ax.set_ylim(-2, 2); ax.set_title("LGR de K(s−2)² / [(s−1)(s²+2s+2)] — sempre há polo à direita", fontsize=10)
save("lgr_B")

# ---- C: K/(s(s+1)(s^2+4s+13))
den = np.polymul([1, 1, 0], [1, 4, 13])
Ks = np.concatenate([np.linspace(0, 2.825, 400), np.linspace(2.825, 2.83, 30), np.linspace(2.83, 300, 4000)])
R = rlocus([1], den, Ks)
fig, ax = plt.subplots(figsize=(6.5, 5.2))
for i in range(R.shape[1]): ax.plot(R[:, i].real, R[:, i].imag, color=BLUE, lw=1.8)
ax.plot([0, -1, -2, -2], [0, 0, 3, -3], "x", color="k", ms=10, mew=2)
for a in [45, 135, -45, -135]: ax.plot([-1.25, -1.25 + 7 * np.cos(np.radians(a))], [0, 7 * np.sin(np.radians(a))], ":", color=GRAY)
ax.plot(-.466, 0, "s", color=ORANGE); ax.annotate("saída −0,466 (K=2,83)", (-.466, 0), (-.2, -1.3), color=ORANGE, fontsize=9, arrowprops=dict(arrowstyle="->", color=ORANGE))
for s in [1, -1]: ax.plot(0, s * 1.6125, "D", color=RED)
ax.annotate("±j1,61; K = 37,44", (0, 1.6125), (.3, .8), color=RED, fontsize=9, arrowprops=dict(arrowstyle="->", color=RED))
ax.annotate("partida −142°", (-2, 3), (-4.3, 3.6), color=PURPLE, fontsize=9, arrowprops=dict(arrowstyle="->", color=PURPLE))
axes0(ax); ax.set_xlim(-5, 2.5); ax.set_ylim(-5, 5); ax.set_aspect("equal")
ax.set_title("LGR de K / [s(s+1)(s²+4s+13)]  (σa = −1,25; ±45°, ±135°)", fontsize=10); save("lgr_C")

# ---- D: P controller 1/(s(s+20))
R = rlocus([1], [1, 20, 0], np.linspace(0, 1500, 2000))
fig, ax = plt.subplots(figsize=(5.5, 4.2))
for i in range(2): ax.plot(R[:, i].real, R[:, i].imag, color=BLUE, lw=1.8)
ax.plot([0, -20], [0, 0], "x", color="k", ms=10, mew=2)
ax.plot([-10, -10], [27.2, -27.2], "*", color=GREEN, ms=13); ax.text(-9, 27.5, "−10 ± j27,2  (K = 840)", color=GREEN, fontsize=9)
r = np.linspace(0, 35, 5); th = np.arccos(.345); ax.plot(-r * np.cos(th), r * np.sin(th), "--", color=PURPLE, lw=.9); ax.text(-15, 33, "ζ = 0,345", color=PURPLE, fontsize=9)
axes0(ax); ax.set_xlim(-25, 8); ax.set_ylim(-35, 37); ax.set_title("LGR de K/[s(s+20)]: reta vertical em σ = −10", fontsize=10); save("lgr_D")

# ---- máquina com zero em +2
fig, ax = plt.subplots(figsize=(6.5, 2.6))
K = np.linspace(0, 6, 400); s = (2 * K - 4) / (K + 1)
ax.plot(K, s, color=BLUE, lw=2); ax.axhline(0, color="k", lw=.8); ax.axhspan(0, 2.2, color="#fadbd8", alpha=.6); ax.axhspan(-4.3, 0, color="#d5f5e3", alpha=.5)
for k, c in [(0, GREEN), (1, GREEN), (2, ORANGE), (3, RED)]:
    v = (2 * k - 4) / (k + 1); ax.plot(k, v, "o", color=c); ax.annotate(f"K={k}: s={v:g}", (k, v), (k + .15, v - .8 if k < 2 else v - .9), fontsize=8.5, color=c)
ax.set_xlabel("ganho K"); ax.set_ylabel("polo de MF  s"); ax.set_ylim(-4.3, 2.2)
ax.set_title("Planta (s−2)/(s+4): o polo de MF s = (2K−4)/(K+1) atravessa para a direita em K = 2", fontsize=9.5)
save("maquina_zero")

# ---- massa-mola-amortecedor
fig, ax = plt.subplots(figsize=(5.5, 2.2)); ax.axis("off"); ax.set_aspect("equal"); ax.set_xlim(-.3, 7.5); ax.set_ylim(-.3, 2.4)
ax.add_patch(Rectangle((-.2, 0), .2, 2.2, color="#999"))
xs = np.linspace(0, 3, 200); ax.plot(xs, 1.6 + .15 * np.sign(np.sin(xs * 2 * np.pi * 3)) * (abs(xs - 1.5) < 1.1), color="k", lw=1.2)
ax.text(1.5, 1.95, "mola k", ha="center")
ax.plot([0, 1.2], [.6, .6], "k", lw=1.2); ax.add_patch(Rectangle((1.2, .4), 1, .4, fill=False, lw=1.2)); ax.plot([1.6, 3], [.6, .6], "k", lw=1.2)
ax.plot([1.6, 1.6], [.45, .75], "k", lw=2); ax.text(1.7, .1, "amortecedor b", ha="center")
ax.add_patch(Rectangle((3, .2), 1.6, 1.8, fc="#eaf2fb", ec="k", lw=1.3)); ax.text(3.8, 1.1, "m", ha="center", va="center", fontsize=14)
ax.annotate("", (6.2, 1.1), (4.6, 1.1), arrowprops=dict(arrowstyle="-|>", lw=1.5)); ax.text(5.4, 1.25, "F(t)", ha="center")
ax.annotate("", (5.2, .2), (4.6, .2), arrowprops=dict(arrowstyle="-|>", color=BLUE)); ax.text(5.3, .25, "x(t)", color=BLUE)
plt.grid(False); save("massa_mola")

# ---- ON-OFF
fig, axs = plt.subplots(1, 2, figsize=(9, 2.8), gridspec_kw=dict(width_ratios=[1, 1.4]))
ax = axs[0]; h = .5
ax.plot([-2, h], [0, 0], color=BLUE, lw=2); ax.plot([-h, 2], [1, 1], color=BLUE, lw=2)
ax.plot([h, h], [0, 1], color=BLUE, lw=2); ax.plot([-h, -h], [1, 0], color=BLUE, lw=2)
ax.annotate("", (h, .55), (h, .35), arrowprops=dict(arrowstyle="-|>", color=BLUE)); ax.annotate("", (-h, .45), (-h, .65), arrowprops=dict(arrowstyle="-|>", color=BLUE))
ax.set_xticks([-h, 0, h]); ax.set_xticklabels(["−h", "0", "+h"]); ax.set_yticks([0, 1]); ax.set_yticklabels(["OFF (U_min)", "ON (U_max)"])
ax.set_xlabel("erro e = r − y"); ax.set_title("Relé com histerese (banda 2h)", fontsize=10)
ax = axs[1]
dt = .01; t = np.arange(0, 60, dt); T = np.zeros_like(t); u = np.zeros_like(t); T[0] = 18; on = 1; tau = 8; Tamb = 18; Kh = 14; delay = int(.8 / dt)
for i in range(1, len(t)):
    e = 25 - T[i - 1]
    if on and e < -h: on = 0
    elif not on and e > h: on = 1
    u[i] = on
    ud = u[i - delay] if i > delay else u[0]
    T[i] = T[i - 1] + dt / tau * (-(T[i - 1] - Tamb) + Kh * ud)
ax.plot(t, T, color=RED, label="temperatura y(t)"); ax.axhline(25, color="k", ls="--", lw=.8, label="referência 25 °C")
ax.axhspan(25 - h, 25 + h, color="#f9e79f", alpha=.6, label="banda de histerese")
ax2 = ax.twinx(); ax2.fill_between(t, 0, u, step="pre", color=BLUE, alpha=.15); ax2.set_ylim(0, 4); ax2.set_yticks([]); ax2.grid(False)
ax.set_ylim(17, 27.5); ax.set_xlabel("t (min)"); ax.set_ylabel("°C"); ax.legend(fontsize=7.5, loc="lower right")
ax.set_title("Aquecedor on-off: oscila em torno da referência (azul = resistência ligada)", fontsize=9.5)
plt.tight_layout(); save("onoff")

# ---- exercício F: PID 0.49(s+7)(s+0.1)/s com 5.76/(s^2+5s+4)
t = np.linspace(0, 6, 3000)
cl0 = np.polyadd([1, 5, 4], [5.76]); _, y0 = signal.step(([5.76], cl0), T=t)
nPD = 3 * np.poly([-7]); clPD = np.polyadd([1, 5, 4], nPD); _, y1 = signal.step((nPD, clPD), T=t)
nPID = 2.826 * np.poly([-7, -.1]); dPID = np.poly([0, -1, -4]); clPID = np.polyadd(dPID, nPID); _, y2 = signal.step((nPID, clPID), T=t)
fig, ax = plt.subplots(figsize=(6.5, 2.9))
ax.plot(t, y0, color=GRAY, label="só K = 5,76 (erro 41%)"); ax.plot(t, y1, color=ORANGE, label="PD: polos −4 ± j3")
ax.plot(t, y2, color=BLUE, label="PID: erro → 0 (lentamente)"); ax.axhline(1, color="k", ls=":", lw=.7)
ax.legend(fontsize=8); ax.set_xlabel("t (s)"); ax.set_title("Exercício 7.16 – degrau em malha fechada", fontsize=10); save("ex_pid_F")

# ---- exercício E b
sd = complex(-2.457, 5.779); K = 37.355; zs = [-3.788, -.2348]
num = K * np.poly(zs); den = np.poly([0, -1, -3, -5]); cl = np.polyadd(den, num)
t = np.linspace(0, 10, 4000); _, y = signal.step((num, cl), T=t)
cl0 = np.polyadd(np.poly([-1, -3, -5]), [78.7]); _, y0 = signal.step(([78.7], cl0), T=t)
fig, ax = plt.subplots(figsize=(6.5, 2.9))
ax.plot(t, y0, color=GRAY, label="P (K=78,7): OS 53%, erro 16%")
ax.plot(t, y, color=BLUE, label="PID: mais rápido, OS ~19%, erro → 0")
ax.axhline(1, color="k", ls=":", lw=.7); ax.legend(fontsize=8); ax.set_xlabel("t (s)"); ax.set_title("Exercício 7.14 – P × PID", fontsize=10); save("ex_pid_E")
print("ok")

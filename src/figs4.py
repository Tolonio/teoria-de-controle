import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import signal
plt.rcParams.update({"font.size": 10, "font.family": "DejaVu Sans", "savefig.dpi": 200, "savefig.bbox": "tight", "axes.grid": True, "grid.alpha": .3})
BLUE, RED, GREEN, ORANGE, GRAY, PURPLE = "#1f5fa8", "#c0392b", "#1e8449", "#d35400", "#555", "#7d3c98"

def rlocus(num, den, Ks):
    out, prev = [], None
    for K in Ks:
        r = np.roots(np.polyadd(den, K * np.asarray(num, float)))
        if prev is not None:
            rr = list(r); r = np.array([rr.pop(int(np.argmin([abs(p - x) for x in rr]))) for p in prev])
        out.append(r); prev = r
    return np.array(out)
def lgr(ax, zs, ps, Kmax, xl, yl, title, Ks=None):
    num = np.poly(zs) if len(zs) else np.array([1.]); den = np.poly(ps)
    Ks = Ks if Ks is not None else np.concatenate([np.linspace(0, Kmax * .02, 800), np.linspace(Kmax * .02, Kmax, 3000)])
    R = rlocus(num, den, Ks)
    for i in range(R.shape[1]): ax.plot(R[:, i].real, R[:, i].imag, color=BLUE, lw=1.8)
    for p in ps: ax.plot(np.real(p), np.imag(p), "x", color="k", ms=9, mew=2)
    for z in zs: ax.plot(np.real(z), np.imag(z), "o", mfc="white", mec="k", ms=8, mew=1.8)
    ax.axhline(0, color="k", lw=.6); ax.axvline(0, color="k", lw=.6); ax.set_xlim(*xl); ax.set_ylim(*yl); ax.set_title(title, fontsize=9.5)
    ax.axvspan(0, xl[1], color="#fadbd8", alpha=.5)
def save(n): plt.savefig(f"fig/{n}.png"); plt.close()

# ---- galeria LGR básico
fig, axs = plt.subplots(2, 3, figsize=(12, 7.2))
lgr(axs[0, 0], [], [-1], 10, (-8, 2), (-3, 3), "(a) 1 polo: K/(s+1)\nvai para a esquerda, sempre estável")
lgr(axs[0, 1], [], [-1, -3], 30, (-5, 2), (-5, 5), "(b) 2 polos: K/[(s+1)(s+3)]\nencontram-se em −2 e sobem: oscila, nunca instabiliza")
lgr(axs[0, 2], [], [0, -1, -3], 40, (-6, 3), (-5, 5), "(c) 3 polos: K/[s(s+1)(s+3)]\nassíntotas a ±60°: K grande instabiliza")
lgr(axs[1, 0], [-3], [0, -1], 40, (-10, 2), (-4, 4), "(d) 2 polos + 1 zero: K(s+3)/[s(s+1)]\nzero atrai: círculo e volta ao eixo")
lgr(axs[1, 1], [-2], [0, -1, -3], 60, (-6, 3), (-5, 5), "(e) = (c) + zero em −2\nzero puxa para a esquerda: estável sempre")
lgr(axs[1, 2], [1], [-1, -3], 6, (-6, 3), (-3, 3), "(f) zero à DIREITA: K(s−1)/[(s+1)(s+3)]\npolo atraído para o SPD: instável para K > 3")
for a in axs.flat: a.set_xlabel("σ", fontsize=9)
plt.tight_layout(); save("lgr_basico")

# ---- PD zero effect (slide)
fig, axs = plt.subplots(1, 2, figsize=(9.5, 3.8))
lgr(axs[0], [], [0, -1, -3], 40, (-7, 3), (-5, 5), "Só P: K/[s(s+1)(s+3)]\ncruza jω (instável para K > 12)")
lgr(axs[1], [-2], [0, -1, -3], 60, (-7, 3), (-5, 5), "PD: K·Td(s + 1/Td) com 1/Td = 2\nzero em −2: LGR fica todo à esquerda")
plt.tight_layout(); save("pd_zero")

# ---- estabilidade: s-plane x z-plane
fig, axs = plt.subplots(1, 2, figsize=(9.5, 4))
ax = axs[0]; ax.axvspan(-4, 0, color="#d5f5e3", alpha=.6); ax.axvspan(0, 2, color="#fadbd8", alpha=.7); ax.axhline(0, color="k", lw=.7); ax.axvline(0, color=ORANGE, lw=3)
ax.text(-3.8, 2.5, "ESTÁVEL\nRe(p) < 0", color=GREEN, weight="bold"); ax.text(.15, 2.5, "INSTÁVEL\nRe(p) > 0", color=RED, weight="bold"); ax.text(.08, -2.8, "eixo jω:\nmarginal", color=ORANGE, fontsize=9)
ax.set_xlim(-4, 2); ax.set_ylim(-3.2, 3.2); ax.set_title("Plano s (contínuo)", fontsize=10); ax.set_xlabel("σ"); ax.set_ylabel("jω")
ax = axs[1]; th = np.linspace(0, 2 * np.pi, 300); ax.set_facecolor("#fadbd8"); ax.fill(np.cos(th), np.sin(th), color="#d5f5e3"); ax.plot(np.cos(th), np.sin(th), color=ORANGE, lw=3)
ax.text(-.45, .15, "ESTÁVEL\n|z| < 1", color=GREEN, weight="bold"); ax.text(.75, 1.25, "INSTÁVEL |z| > 1", color=RED, weight="bold"); ax.text(-1.6, -1.45, "círculo unitário: marginal", color=ORANGE, fontsize=9)
ax.axhline(0, color="k", lw=.6); ax.axvline(0, color="k", lw=.6); ax.set_aspect("equal"); ax.set_xlim(-1.7, 1.9); ax.set_ylim(-1.6, 1.6); ax.set_title("Plano z (digital): z = e^{sT}", fontsize=10)
plt.tight_layout(); save("estab_mapas")

# ---- Nyquist
fig, axs = plt.subplots(1, 2, figsize=(10, 4.2))
w = np.concatenate([np.linspace(0, 1, 400), np.logspace(0, 2.5, 2000)])
for ax, K, c in [(axs[0], 30, GREEN), (axs[1], 90, RED)]:
    G = K / np.polyval(np.poly([-1, -2, -3]), 1j * w)
    ax.plot(G.real, G.imag, color=c, lw=2, label="ω de 0 a +∞"); ax.plot(G.real, -G.imag, color=c, lw=1.2, ls="--", label="ω negativo (espelho)")
    ax.plot(-1, 0, "P", color="k", ms=11); ax.annotate("−1", (-1, 0), (-1.25, .5), fontsize=10)
    ax.axhline(0, color="k", lw=.6); ax.axvline(0, color="k", lw=.6)
    ax.set_title(f"K = {K}: cruza o eixo real em −K/60 = {-K/60:.2f}\n" + ("não envolve −1: ESTÁVEL" if K < 60 else "envolve −1 duas vezes: INSTÁVEL"), fontsize=9.5)
    lim = max(1.8, K / 60 * 1.3); ax.set_xlim(-lim, K / 6 * 1.05); ax.set_ylim(-K / 9, K / 9); ax.legend(fontsize=8, loc="lower right")
plt.tight_layout(); save("nyquist")

# ---- Bode/margens K=30
w = np.logspace(-1, 1.5, 500); G = 30 / np.polyval(np.poly([-1, -2, -3]), 1j * w)
fig, axs = plt.subplots(2, 1, figsize=(6.5, 4.2), sharex=True)
axs[0].semilogx(w, 20 * np.log10(abs(G)), color=BLUE); axs[0].axhline(0, color="k", lw=.7); axs[0].set_ylabel("|G| (dB)")
axs[1].semilogx(w, np.unwrap(np.angle(G)) * 180 / np.pi, color=BLUE); axs[1].axhline(-180, color="k", lw=.7); axs[1].set_ylabel("fase (°)"); axs[1].set_xlabel("ω (rad/s)")
axs[0].axvline(2.35, color=GREEN, ls=":"); axs[1].axvline(2.35, color=GREEN, ls=":"); axs[0].axvline(3.317, color=RED, ls=":"); axs[1].axvline(3.317, color=RED, ls=":")
axs[1].annotate("MF = 25°", (2.35, -155), (0.15, -120), color=GREEN, arrowprops=dict(arrowstyle="->", color=GREEN))
axs[0].annotate("MG = 6 dB", (3.317, -6), (6, 10), color=RED, arrowprops=dict(arrowstyle="->", color=RED))
axs[0].set_title("Bode de 30/[(s+1)(s+2)(s+3)]: margens de ganho e de fase", fontsize=10); plt.tight_layout(); save("bode_margens")

# ---- motor CC: diagrama de blocos + respostas
fig, ax = plt.subplots(figsize=(9, 2.6)); ax.axis("off"); ax.set_xlim(0, 11); ax.set_ylim(-1.5, 1.2)
def box(x, y, t, w=1.6):
    ax.add_patch(plt.Rectangle((x - w / 2, y - .35), w, .7, fc="#eaf2fb", ec="k")); ax.text(x, y, t, ha="center", va="center", fontsize=10)
def arr(x0, y0, x1, y1, t=None):
    ax.annotate("", (x1, y1), (x0, y0), arrowprops=dict(arrowstyle="-|>", lw=1.2))
    if t: ax.text((x0 + x1) / 2, y0 + .12, t, ha="center", fontsize=9)
def sm(x, y): ax.add_patch(plt.Circle((x, y), .2, fc="white", ec="k")); ax.text(x, y, "Σ", ha="center", va="center", fontsize=8)
arr(0, 0, .9, 0, "Va"); sm(1.1, 0); ax.text(.85, -.35, "+", fontsize=9); ax.text(1.2, -.45, "−", fontsize=10)
arr(1.3, 0, 2.2, 0); box(3, 0, "1/(Las + Ra)"); arr(3.8, 0, 4.6, 0, "Ia"); box(5.2, 0, "Kt", 1); arr(5.7, 0, 6.4, 0, "T"); sm(6.6, 0); ax.text(6.45, .5, "TL (carga)", fontsize=8.5); arr(6.6, .45, 6.6, .2)
ax.text(6.7, -.42, "−", fontsize=10); arr(6.8, 0, 7.6, 0); box(8.4, 0, "1/(Js + B)"); arr(9.2, 0, 10.6, 0, "ω")
ax.plot([9.9, 9.9, 1.1], [0, -1.1, -1.1], "k", lw=1.2); arr(1.1, -1.1, 1.1, -.2); box(5.5, -1.1, "Kb (fcem)", 1.6)
save("motor_blocos")
t = np.linspace(0, 8, 3000); d = [1, 3, 7]
_, y0 = signal.step(([10], d), T=t)
cl1 = np.polyadd(d, [10]); _, y1 = signal.step(([10], cl1), T=t)
num = 10 * np.array([.6, 1.2]); den = np.polyadd(np.polymul(d, [1, 0]), num); _, y2 = signal.step((num, den), T=t)
fig, ax = plt.subplots(figsize=(6.5, 2.9))
ax.plot(t, y0 / (10 / 7), color=GRAY, label="malha aberta (normalizada)"); ax.plot(t, y1, color=ORANGE, label="P com Kp = 1: erro 41%"); ax.plot(t, y2, color=BLUE, label="PI (0,6 + 1,2/s): erro 0, OS 6%")
ax.axhline(1, color="k", ls=":", lw=.7); ax.legend(fontsize=8); ax.set_xlabel("t (s)"); ax.set_ylabel("ω / ω_ref"); ax.set_title("Controle de velocidade do motor CC: 10/(s²+3s+7)", fontsize=10)
save("motor_resp")

# ---- estado: resposta com realimentação de estados
t = np.linspace(0, 5, 2000)
_, y0 = signal.step(([1], [1, 2, 2]), T=t); _, y1 = signal.step(([25], [1, 8, 25]), T=t)
fig, ax = plt.subplots(figsize=(6.5, 2.8)); ax.plot(t, y0 * 2, color=GRAY, label="sem controle (×2 para comparar): polos −1 ± j"); ax.plot(t, y1, color=BLUE, label="u = −[23 6]x + 25r: polos −4 ± j3")
ax.axhline(1, color="k", ls=":", lw=.7); ax.legend(fontsize=8); ax.set_xlabel("t (s)"); ax.set_title("Alocação de polos na massa-mola (m=1, b=2, k=2)", fontsize=10); save("ss_resp")

# ---- transformada z: discreto
T = 0.1; a = np.exp(-T); kk = np.arange(0, 26)
fig, axs = plt.subplots(1, 2, figsize=(10, 3))
for K, c in [(5, BLUE), (15, ORANGE), (21, RED)]:
    y = np.zeros(len(kk))
    for k in range(1, len(kk)): y[k] = (a - (1 - a) * K) * y[k - 1] + (1 - a) * K
    axs[0].step(kk * T, y, where="post", color=c, label=f"K = {K}: polo z = {a - (1 - a) * K:.2f}")
axs[0].set_ylim(-3, 4.5); axs[0].legend(fontsize=8); axs[0].set_xlabel("t = kT (s)"); axs[0].set_title("Malha fechada digital de 1/(s+1), T = 0,1 s", fontsize=9.5)
Ts = np.linspace(.01, 2, 200); axs[1].plot(Ts, (1 + np.exp(-Ts)) / (1 - np.exp(-Ts)), color=PURPLE); axs[1].set_yscale("log"); axs[1].set_xlabel("período de amostragem T (s)"); axs[1].set_ylabel("K máximo estável")
axs[1].set_title("Amostrar mais devagar reduz o K estável\n(no contínuo, qualquer K seria estável)", fontsize=9.5)
plt.tight_layout(); save("z_discreto")
print("ok")

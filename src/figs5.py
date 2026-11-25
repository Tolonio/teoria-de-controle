import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle
plt.rcParams.update({"font.size": 10, "font.family": "DejaVu Sans", "savefig.dpi": 200, "savefig.bbox": "tight"})
BLUE, RED, GREEN, ORANGE, GRAY = "#1f5fa8", "#c0392b", "#1e8449", "#d35400", "#555"

def box(ax, x, y, t, w=1.7, fc="#eaf2fb"):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - .32), w, .64, boxstyle="round,pad=0.02", fc=fc, ec="k", lw=1.1)); ax.text(x, y, t, ha="center", va="center", fontsize=9.5)
def arr(ax, x0, y0, x1, y1, t=None, dy=.14):
    ax.annotate("", (x1, y1), (x0, y0), arrowprops=dict(arrowstyle="-|>", lw=1.2))
    if t: ax.text((x0 + x1) / 2, y0 + dy, t, ha="center", fontsize=9)
def sm(ax, x, y):
    ax.add_patch(Circle((x, y), .18, fc="white", ec="k")); ax.text(x, y, "Σ", ha="center", va="center", fontsize=8)

# ---- diagrams open vs closed
fig, axs = plt.subplots(2, 1, figsize=(9, 4.2))
ax = axs[0]; ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(-.8, .8); ax.set_title("MALHA ABERTA: ninguém confere o resultado", fontsize=10, loc="left", color=RED)
arr(ax, .2, 0, 1.4, 0, "referência r"); box(ax, 2.3, 0, "controlador"); arr(ax, 3.15, 0, 4.1, 0, "u"); box(ax, 5, 0, "atuador"); arr(ax, 5.85, 0, 6.8, 0); box(ax, 7.7, 0, "planta", fc="#fdebd0"); arr(ax, 8.55, 0, 9.8, 0, "saída y")
arr(ax, 7.7, .75, 7.7, .33); ax.text(7.85, .6, "perturbação", fontsize=8.5, color=ORANGE)
ax = axs[1]; ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(-1.3, .8); ax.set_title("MALHA FECHADA: mede, compara e corrige", fontsize=10, loc="left", color=GREEN)
arr(ax, .2, 0, .95, 0, "r"); sm(ax, 1.15, 0); ax.text(.85, -.35, "+", fontsize=9); ax.text(1.22, -.45, "−", fontsize=11)
arr(ax, 1.33, 0, 2.0, 0, "e"); box(ax, 2.9, 0, "controlador"); arr(ax, 3.75, 0, 4.4, 0, "u"); box(ax, 5.3, 0, "atuador"); arr(ax, 6.15, 0, 6.8, 0); box(ax, 7.7, 0, "planta", fc="#fdebd0"); arr(ax, 8.55, 0, 9.8, 0, "y")
arr(ax, 7.7, .75, 7.7, .33); ax.text(7.85, .6, "perturbação", fontsize=8.5, color=ORANGE)
ax.plot([9.1, 9.1, 6.0], [0, -1, -1], "k", lw=1.2); box(ax, 5.2, -1, "sensor H", w=1.5, fc="#e8f6ec"); ax.plot([4.45, 1.15], [-1, -1], "k", lw=1.2); arr(ax, 1.15, -1, 1.15, -.18)
plt.tight_layout(); plt.savefig("fig/malha_ab_fe.png"); plt.close()

# ---- simulation: motor speed, load at t=4 and gain drop
dt = .001; t = np.arange(0, 10, dt); r = 1.0
def sim(mode):
    w = 0; I = 0; out = []
    for tk in t:
        g = 1.43 * (0.8 if tk > 7 else 1.0)       # planta "envelhece" em t = 7 s: ganho cai 20%
        d = 0.25 if tk > 4 else 0.0                # carga entra em t = 4 s
        e = r - w
        if mode == "ab": u = r / 1.43
        elif mode == "P": u = 10 * e
        else: I += e * dt; u = 2 * e + 6 * I
        w += dt / 0.5 * (-w + g * u - d)
        out.append(w)
    return np.array(out)
fig, ax = plt.subplots(figsize=(8, 3.1))
ax.plot(t, sim("ab"), color=RED, lw=2, label="malha aberta (u calculado uma vez)")
ax.plot(t, sim("P"), color=ORANGE, lw=2, label="malha fechada com P (K = 10)")
ax.plot(t, sim("PI"), color=GREEN, lw=2, label="malha fechada com PI")
ax.axhline(1, color="k", ls=":", lw=.8); ax.axvline(4, color=GRAY, lw=.8, ls="--"); ax.axvline(7, color=GRAY, lw=.8, ls="--")
ax.text(4.05, .25, "entra carga", fontsize=8.5, color=GRAY); ax.text(7.05, .25, "planta perde 20%\nde ganho", fontsize=8.5, color=GRAY)
ax.set_ylim(0, 1.25); ax.set_xlabel("t (s)"); ax.set_ylabel("velocidade / referência"); ax.grid(alpha=.3); ax.legend(fontsize=8, loc="lower left")
ax.set_title("Motor: a malha fechada corrige carga e desgaste; a aberta não percebe", fontsize=10)
plt.savefig("fig/malha_sim.png"); plt.close()

# ---- impedance vs frequency
w = np.logspace(0, 5, 400); R, L, C = 100, 10e-3, 10e-6
fig, axs = plt.subplots(1, 2, figsize=(10, 3.4))
ax = axs[0]; ax.loglog(w, R * np.ones_like(w), color=GRAY, lw=2, label="resistor R = 100 Ω")
ax.loglog(w, w * L, color=BLUE, lw=2, label="indutor |Z| = ωL (L = 10 mH)"); ax.loglog(w, 1 / (w * C), color=RED, lw=2, label="capacitor |Z| = 1/(ωC) (C = 10 µF)")
ax.set_xlabel("ω (rad/s)"); ax.set_ylabel("|Z| (Ω)"); ax.grid(alpha=.3, which="both"); ax.legend(fontsize=8); ax.set_title("Módulo da impedância × frequência", fontsize=10)
ax.text(1.5, 3e2, "C: circuito aberto\nem baixa frequência", fontsize=8, color=RED); ax.text(2e3, 2e-2, "C: curto em\nalta frequência", fontsize=8, color=RED)
ax = axs[1]; ax.set_aspect("equal"); ax.axhline(0, color="k", lw=.6); ax.axvline(0, color="k", lw=.6)
for (x, y, c, lab) in [(1, 0, GRAY, "R: 0°"), (0, 1, BLUE, "jωL: +90°"), (0, -1, RED, "1/(jωC): −90°")]:
    ax.annotate("", (x, y), (0, 0), arrowprops=dict(arrowstyle="-|>", lw=2, color=c)); ax.text(x + (.05 if x else .07), y + (.08 if y >= 0 else -.18), lab, color=c, fontsize=9)
ax.set_xlim(-.4, 1.6); ax.set_ylim(-1.35, 1.35); ax.set_title("Impedância como número complexo", fontsize=10); ax.set_xlabel("parte real (resistência)"); ax.set_ylabel("parte imaginária (reatância)")
plt.tight_layout(); plt.savefig("fig/impedancia.png"); plt.close()
print("ok")

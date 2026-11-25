import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import signal
plt.rcParams.update({"font.size": 10, "font.family": "DejaVu Sans", "savefig.dpi": 200, "savefig.bbox": "tight"})
BLUE, RED, GREEN, ORANGE, GRAY = "#1f5fa8", "#c0392b", "#1e8449", "#d35400", "#555"

def resistor(ax, x0, y0, x1, y1, n=5, w=.12):
    L = np.hypot(x1 - x0, y1 - y0); ux, uy = (x1 - x0) / L, (y1 - y0) / L; px, py = -uy, ux
    s0 = L * .22; seg = (L - 2 * s0) / (2 * n); pts = [(x0, y0), (x0 + ux * s0, y0 + uy * s0)]
    for k in range(2 * n):
        d = s0 + seg * (k + .5); sg = 1 if k % 2 == 0 else -1
        pts.append((x0 + ux * d + px * w * sg, y0 + uy * d + py * w * sg))
    pts += [(x0 + ux * (L - s0), y0 + uy * (L - s0)), (x1, y1)]
    ax.plot(*zip(*pts), "k", lw=1.2)
def cap(ax, x0, y0, x1, y1, gap=.07, h=.2):
    L = np.hypot(x1 - x0, y1 - y0); ux, uy = (x1 - x0) / L, (y1 - y0) / L; px, py = -uy, ux
    m = ((x0 + x1) / 2, (y0 + y1) / 2); a = (m[0] - ux * gap, m[1] - uy * gap); b = (m[0] + ux * gap, m[1] + uy * gap)
    ax.plot([x0, a[0]], [y0, a[1]], "k", lw=1.2); ax.plot([b[0], x1], [b[1], y1], "k", lw=1.2)
    for c in (a, b): ax.plot([c[0] - px * h, c[0] + px * h], [c[1] - py * h, c[1] + py * h], "k", lw=2)
def W(ax, *pts): ax.plot(*zip(*pts), "k", lw=1.2)
def gnd(ax, x, y):
    W(ax, (x, y + .25), (x, y))
    for i, w in enumerate([.22, .14, .06]): ax.plot([x - w, x + w], [y - i * .08, y - i * .08], "k", lw=1.2)
def opamp(ax, x, y, s=1):
    ax.add_patch(plt.Polygon([(x, y + .6 * s), (x, y - .6 * s), (x + 1.1 * s, y)], fill=False, ec="k", lw=1.4))
    ax.text(x + .1, y + .3 * s, "−", color=RED, fontsize=12, va="center"); ax.text(x + .1, y - .3 * s, "+", color=RED, fontsize=11, va="center")
def term(ax, x, y, lab, side="l"):
    ax.plot(x, y, "o", mfc="white", mec="k", ms=5); ax.text(x - .12 if side == "l" else x + .12, y, lab, ha="right" if side == "l" else "left", va="center", fontsize=11)
def panel(ax, title):
    ax.set_aspect("equal"); ax.axis("off"); ax.set_title(title, fontsize=10, pad=4)

# grid of six circuits
fig, axs = plt.subplots(2, 3, figsize=(12, 5.8))
# 1 ideal
ax = axs[0, 0]; panel(ax, "Amp-op ideal: vo = A(v₊ − v₋)")
opamp(ax, 1, 0); W(ax, (0, .3), (1, .3)); W(ax, (0, -.3), (1, -.3)); W(ax, (2.1, 0), (2.8, 0))
term(ax, 0, .3, "v₋"); term(ax, 0, -.3, "v₊"); term(ax, 2.8, 0, "vo", "r")
ax.annotate("i₋ = 0", (0.6, .3), (0.3, .75), fontsize=9, color=BLUE, arrowprops=dict(arrowstyle="->", color=BLUE))
ax.annotate("i₊ = 0", (0.6, -.3), (0.3, -.85), fontsize=9, color=BLUE, arrowprops=dict(arrowstyle="->", color=BLUE))
ax.text(1.4, -1.05, "realimentado: v₊ = v₋", ha="center", fontsize=9.5, color=RED); ax.set_xlim(-.6, 3.4); ax.set_ylim(-1.3, 1.1)
# 2 inversor
ax = axs[0, 1]; panel(ax, "Inversor: vo = −(R/R₁)·vi")
term(ax, -.3, .3, "vi"); resistor(ax, -.3, .3, .8, .3); W(ax, (.8, .3), (1.3, .3)); ax.text(.25, .5, "R₁", ha="center")
W(ax, (1, .3), (1, 1)); resistor(ax, 1, 1, 2.2, 1); W(ax, (2.2, 1), (2.6, 1), (2.6, 0)); ax.text(1.6, 1.2, "R", ha="center")
opamp(ax, 1.3, 0); W(ax, (1.3, -.3), (1.1, -.3)); gnd(ax, 1.1, -.55); W(ax, (2.4, 0), (3, 0)); term(ax, 3, 0, "vo", "r")
ax.set_xlim(-.9, 3.6); ax.set_ylim(-1, 1.4)
# 3 nao inversor
ax = axs[0, 2]; panel(ax, "Não inversor: vo = (1 + R/R₁)·vi")
term(ax, .45, -.3, "vi"); W(ax, (.45, -.3), (1.3, -.3)); W(ax, (1.3, .3), (.9, .3), (.9, 1)); resistor(ax, .9, .3, .1, .3); ax.text(.5, .5, "R₁", ha="center"); W(ax, (.1, .3), (.1, .1)); gnd(ax, .1, -.15)
resistor(ax, .9, 1, 2.2, 1); W(ax, (2.2, 1), (2.6, 1), (2.6, 0)); ax.text(1.55, 1.2, "R", ha="center")
opamp(ax, 1.3, 0); W(ax, (2.4, 0), (3, 0)); term(ax, 3, 0, "vo", "r"); ax.set_xlim(-.9, 3.6); ax.set_ylim(-1, 1.4)
# 4 diferencial
ax = axs[1, 0]; panel(ax, "Diferencial: vo = (R/R₁)(vR − vY) = Kp·e")
term(ax, -.3, .3, "vY"); resistor(ax, -.3, .3, .8, .3); W(ax, (.8, .3), (1.3, .3)); ax.text(.25, .5, "R₁", ha="center")
term(ax, -.3, -.3, "vR"); resistor(ax, -.3, -.3, .8, -.3); W(ax, (.8, -.3), (1.3, -.3)); ax.text(.25, -.58, "R₁", ha="center")
W(ax, (1, .3), (1, 1)); resistor(ax, 1, 1, 2.2, 1); W(ax, (2.2, 1), (2.6, 1), (2.6, 0)); ax.text(1.6, 1.2, "R", ha="center")
W(ax, (1.05, -.3), (1.05, -.4)); resistor(ax, 1.05, -.4, 1.05, -1.1); gnd(ax, 1.05, -1.35); ax.text(1.2, -.75, "R")
opamp(ax, 1.3, 0); W(ax, (2.4, 0), (3, 0)); term(ax, 3, 0, "vo", "r"); ax.set_xlim(-.9, 3.6); ax.set_ylim(-1.6, 1.4)
# 5 integrador / PI
ax = axs[1, 1]; panel(ax, "PI: Zf = R₂ + 1/(sC) ⇒ −(R₂/R₁)(1 + 1/(R₂Cs))")
term(ax, -.3, .3, "vi"); resistor(ax, -.3, .3, .8, .3); W(ax, (.8, .3), (1.3, .3)); ax.text(.25, .5, "R₁", ha="center")
W(ax, (1, .3), (1, 1)); resistor(ax, 1, 1, 1.7, 1); cap(ax, 1.7, 1, 2.3, 1); W(ax, (2.3, 1), (2.6, 1), (2.6, 0)); ax.text(1.35, 1.2, "R₂", ha="center"); ax.text(2, 1.3, "C", ha="center")
opamp(ax, 1.3, 0); W(ax, (1.3, -.3), (1.1, -.3)); gnd(ax, 1.1, -.55); W(ax, (2.4, 0), (3, 0)); term(ax, 3, 0, "vo", "r"); ax.set_xlim(-.9, 3.6); ax.set_ylim(-1, 1.5)
# 6 avanço/atraso
ax = axs[1, 2]; panel(ax, "Avanço/atraso: −(R₂/R₁)(R₁C₁s+1)/(R₂C₂s+1)")
term(ax, -.5, .3, "vi"); W(ax, (-.5, .3), (-.3, .3)); W(ax, (-.3, .55), (-.3, .05))
resistor(ax, -.3, .55, .7, .55); cap(ax, -.3, .05, .7, .05); W(ax, (.7, .55), (.7, .05)); W(ax, (.7, .3), (1.3, .3)); ax.text(.2, .75, "R₁", ha="center"); ax.text(.2, -.25, "C₁", ha="center")
W(ax, (1, .3), (1, 1.4)); resistor(ax, 1, 1.4, 2.2, 1.4); cap(ax, 1, .95, 2.2, .95); W(ax, (2.2, 1.4), (2.2, .95)); W(ax, (2.2, 1.15), (2.6, 1.15), (2.6, 0))
ax.text(1.6, 1.58, "R₂", ha="center"); ax.text(1.85, .7, "C₂", ha="center")
opamp(ax, 1.3, 0); W(ax, (1.3, -.3), (1.1, -.3)); gnd(ax, 1.1, -.55); W(ax, (2.4, 0), (3, 0)); term(ax, 3, 0, "vo", "r"); ax.set_xlim(-1.1, 3.6); ax.set_ylim(-1, 1.8)
plt.tight_layout(); plt.savefig("fig/ampop.png"); plt.close()

# ---- PID comparison on 1/((s+1)(s+2))
def sim(Kp, Ki, Kd, T=8, dt=1e-3, N=30):
    x1 = x2 = I = df = 0; ep = 1; out = {k: [] for k in "tyPID"}
    for k in range(int(T / dt) + 1):
        t = k * dt; y = x1; e = 1 - y
        df = 0 if k == 0 else df + dt * N * ((e - ep) / dt - df); ep = e; I += e * dt
        uP, uI, uD = Kp * e, Ki * I, Kd * df
        if k % 10 == 0:
            for key, v in zip("tyPID", (t, y, uP, uI, uD)): out[key].append(v)
        u = uP + uI + uD; x1, x2 = x1 + dt * x2, x2 + dt * (u - 3 * x2 - 2 * x1)
    return {k: np.array(v) for k, v in out.items()}
cases = [("Só P (Kp = 8)", 8, 0, 0), ("PI (Kp = 8, Ki = 6)", 8, 6, 0), ("PD (Kp = 8, Kd = 1,5)", 8, 0, 1.5), ("PID (Kp = 10, Ki = 8, Kd = 1,5)", 10, 8, 1.5)]
fig, axs = plt.subplots(2, 4, figsize=(13, 5), sharex=True, gridspec_kw=dict(height_ratios=[1.4, 1]))
stats = []
for j, (nm, kp, ki, kd) in enumerate(cases):
    r = sim(kp, ki, kd); ax = axs[0, j]
    ax.plot(r["t"], r["y"], color=BLUE, lw=2.2); ax.axhline(1, color="k", ls=":", lw=.8); ax.set_ylim(0, 1.45); ax.set_title(nm, fontsize=9.5); ax.grid(alpha=.3)
    fin = r["y"][-1]; os_ = max(0, (r["y"].max() - fin) / fin * 100)
    idx = np.where(abs(r["y"] - fin) > .02 * fin)[0]; ts = r["t"][idx[-1]] if len(idx) else 0
    stats.append((nm, os_, ts, 1 - fin)); ax.text(7.8, .08, f"erro final = {1 - fin:.2f}\nOS = {os_:.0f}%", ha="right", fontsize=8.5)
    ax = axs[1, j]; ax.plot(r["t"], r["P"], color=GREEN, label="P"); ax.plot(r["t"], r["I"], color=ORANGE, label="I"); ax.plot(r["t"], np.clip(r["D"], -5, 12), color=RED, label="D")
    ax.set_ylim(-3, 12); ax.grid(alpha=.3); ax.set_xlabel("t (s)")
    if j == 0: ax.legend(fontsize=8, loc="upper right"); ax.set_ylabel("parcelas de u(t)"); axs[0, 0].set_ylabel("saída y(t)")
plt.tight_layout(); plt.savefig("fig/pid_comp.png"); plt.close()
for s in stats: print(s)

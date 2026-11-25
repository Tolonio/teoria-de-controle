import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, Arc
from scipy import signal
import os
os.makedirs("fig", exist_ok=True)
plt.rcParams.update({"font.size": 10, "font.family": "DejaVu Sans", "axes.grid": True,
                     "grid.alpha": .3, "savefig.dpi": 200, "savefig.bbox": "tight"})
BLUE, RED, GREEN, ORANGE, GRAY, PURPLE = "#1f5fa8", "#c0392b", "#1e8449", "#d35400", "#555", "#7d3c98"

def rlocus(num, den, Ks):
    """roots of den + K num for each K, ordered by continuity"""
    num = np.atleast_1d(num); den = np.atleast_1d(den)
    n = len(den) - 1
    out = []
    prev = None
    for K in Ks:
        c = np.polyadd(den, K * num)
        r = np.roots(c)
        if prev is not None:
            idx = []
            rr = list(r)
            for p in prev:
                j = int(np.argmin([abs(p - x) for x in rr]))
                idx.append(rr.pop(j))
            r = np.array(idx)
        out.append(r); prev = r
    return np.array(out)

def save(name):
    plt.savefig(f"fig/{name}.png"); plt.close()

# ---------- block diagrams ----------
def box(ax, x, y, w, h, txt, fc="#eaf2fb", fs=10):
    ax.add_patch(FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle="round,pad=0.02", fc=fc, ec="k", lw=1.2))
    ax.text(x, y, txt, ha="center", va="center", fontsize=fs)
def arrow(ax, x0, y0, x1, y1, txt=None, dy=.18, pos=.5):
    ax.annotate("", (x1, y1), (x0, y0), arrowprops=dict(arrowstyle="-|>", lw=1.2, color="k"))
    if txt: ax.text(x0 + (x1 - x0) * pos, y0 + dy, txt, ha="center", fontsize=10)
def summ(ax, x, y, r=.18):
    ax.add_patch(Circle((x, y), r, fc="white", ec="k", lw=1.2)); ax.text(x, y, "Σ", ha="center", va="center", fontsize=9)

fig, ax = plt.subplots(figsize=(7.5, 2.2)); ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(-1.4, 1)
arrow(ax, .2, 0, 1.32, 0, "R(s)", pos=.4); summ(ax, 1.5, 0); ax.text(1.18, -.35, "+"); ax.text(1.62, -.45, "−")
arrow(ax, 1.68, 0, 2.9, 0, "E(s)"); box(ax, 3.7, 0, 1.6, .7, "$G_c(s)$\ncontrolador")
arrow(ax, 4.5, 0, 5.7, 0, "U(s)"); box(ax, 6.5, 0, 1.6, .7, "$G_p(s)$\nplanta")
arrow(ax, 7.3, 0, 9.4, 0, "C(s) ou Y(s)", pos=.6)
ax.plot([8.6, 8.6, 1.5], [0, -1.1, -1.1], "k", lw=1.2); arrow(ax, 1.5, -1.1, 1.5, -.18)
ax.text(5, -1.0, "realimentação unitária  H(s)=1", ha="center", fontsize=9, color=GRAY)
save("malha")

# PID diagram
fig, ax = plt.subplots(figsize=(7.5, 2.8)); ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(-1.8, 1.4)
arrow(ax, .2, 0, 1.12, 0, "r(t)", pos=.4); summ(ax, 1.3, 0); ax.text(.98, -.35, "+"); ax.text(1.42, -.45, "−")
ax.plot([1.48, 2.2], [0, 0], "k", lw=1.2); ax.text(1.85, .15, "e(t)", ha="center")
for yy, t, c in [(.9, "P:  $K_p\\,e(t)$", "#d5f5d5"), (0, "I:  $K_i\\int e\\,d\\tau$", "#d4eefc"), (-.9, "D:  $K_d\\,\\dot e(t)$", "#fbd9c9")]:
    ax.plot([2.2, 2.2], [0, yy], "k", lw=1.2); arrow(ax, 2.2, yy, 2.9, yy); box(ax, 3.9, yy, 2.0, .55, t, fc=c)
    ax.plot([4.9, 5.6, 5.6], [yy, yy, yy], "k", lw=1.2)
    arrow(ax, 5.6, yy, 5.85 if yy == 0 else 6.0, 0 if yy == 0 else (0.18 if yy > 0 else -.18))
summ(ax, 6.0, 0); arrow(ax, 6.18, 0, 7.0, 0, "u(t)"); box(ax, 7.7, 0, 1.4, .6, "Planta")
arrow(ax, 8.4, 0, 9.7, 0, "y(t)"); ax.plot([9.1, 9.1, 1.3], [0, -1.6, -1.6], "k", lw=1.2); arrow(ax, 1.3, -1.6, 1.3, -.18)
save("pid")

# ---------- s-plane: poles vs response ----------
fig, ax = plt.subplots(figsize=(7, 4.2))
ax.axhline(0, color="k", lw=.8); ax.axvline(0, color="k", lw=.8)
ax.axvspan(-4, 0, color="#d5f5e3", alpha=.5); ax.axvspan(0, 2, color="#fadbd8", alpha=.6)
ax.text(-3.9, 2.6, "ESTÁVEL (semiplano esquerdo)", color=GREEN, fontsize=9, weight="bold")
ax.text(.1, 2.6, "INSTÁVEL", color=RED, fontsize=9, weight="bold")
t = np.linspace(0, 1, 60)
def mini(px, py, sig, w, col):
    tt = np.linspace(0, 6, 200); y = np.exp(sig * tt) * (np.cos(w * tt) if w else 1)
    y = y / max(1e-9, np.max(np.abs(y)))
    ax.plot(px + tt / 6 * .9, py + .35 + y * .3, color=col, lw=1)
for (x, y, col) in [(-3, 0, BLUE), (-1, 0, BLUE), (-1.5, 1.5, BLUE), (-0.4, 1.8, BLUE), (0, 1.6, ORANGE), (1, 0, RED), (1, 1.5, RED)]:
    ax.plot(x, y, "x", color=col, ms=9, mew=2)
    if y: ax.plot(x, -y, "x", color=col, ms=9, mew=2, alpha=.5)
    mini(x - .45, y, x, 2 * y if y else 0, col)
ax.set_xlim(-4, 2); ax.set_ylim(-2.5, 3); ax.set_xlabel("σ (parte real)"); ax.set_ylabel("jω (parte imaginária)")
ax.set_title("Posição do polo no plano s → forma da resposta (curvinhas = resposta ao impulso)", fontsize=9.5)
save("plano_s")

# geometry zeta wn
fig, ax = plt.subplots(figsize=(5, 3.6))
pd_ = complex(-0.3376, 0.5623)
ax.axhline(0, color="k", lw=.8); ax.axvline(0, color="k", lw=.8)
ax.plot([0, pd_.real], [0, pd_.imag], color=PURPLE, lw=1.5)
ax.plot(pd_.real, pd_.imag, "x", color=RED, ms=10, mew=2); ax.plot(pd_.real, -pd_.imag, "x", color=RED, ms=10, mew=2)
ax.plot([pd_.real, pd_.real], [0, pd_.imag], "--", color=GRAY); ax.plot([pd_.real, 0], [pd_.imag, pd_.imag], "--", color=GRAY)
ax.add_patch(Arc((0, 0), .3, .3, theta1=180 - np.degrees(np.arccos(.5148)), theta2=180, color=ORANGE, lw=1.5))
ax.text(-.25, .05, "θ", color=ORANGE, fontsize=11)
ax.text(-.34, .32, "$\\omega_n=|p_d|$", color=PURPLE, fontsize=10, rotation=-55)
ax.text(pd_.real - .02, -.09, "$-\\zeta\\omega_n=-0{,}3376$", ha="center", fontsize=9)
ax.text(.02, pd_.imag, "$j\\omega_d=j0{,}5623$", fontsize=9, va="center")
ax.text(pd_.real - .05, pd_.imag + .06, "$p_d$", color=RED)
ax.text(-.62, -.42, "$\\cos\\theta=\\zeta$", fontsize=11, color=ORANGE)
ax.set_xlim(-.7, .35); ax.set_ylim(-.7, .75); ax.set_aspect("equal"); ax.set_xlabel("σ"); ax.set_ylabel("jω")
save("geometria")

# step responses 2nd order
fig, ax = plt.subplots(figsize=(6.5, 3))
tt = np.linspace(0, 12, 600)
for z, c in [(0.1, RED), (0.3, ORANGE), (0.5147, BLUE), (0.707, GREEN), (1.0, PURPLE), (2.0, GRAY)]:
    _, y = signal.step(([1], [1, 2 * z, 1]), T=tt)
    ax.plot(tt, y, color=c, label=f"ζ = {z:g}")
ax.axhline(1, color="k", lw=.6, ls=":"); ax.set_xlabel("t (com ωn = 1 rad/s)"); ax.set_ylabel("c(t)")
ax.legend(fontsize=8, ncol=3); ax.set_title("Resposta ao degrau de $\\omega_n^2/(s^2+2\\zeta\\omega_n s+\\omega_n^2)$", fontsize=10)
save("degrau_zeta")

# ---------- main root locus: K/(s(s+1)(s+2)) ----------
den = np.array([1, 3, 2, 0.0]); num = np.array([1.0])
Ks = np.concatenate([np.linspace(0, .3849, 300), np.linspace(.3849, 40, 3000)])
R = rlocus(num, den, Ks)
fig, ax = plt.subplots(figsize=(7, 5.6))
for i in range(R.shape[1]): ax.plot(R[:, i].real, R[:, i].imag, color=BLUE, lw=1.8)
ax.plot([0, -1, -2], [0, 0, 0], "x", color="k", ms=11, mew=2.2)
for ang in [60, -60]:
    L = 5; ax.plot([-1, -1 + L * np.cos(np.radians(ang))], [0, L * np.sin(np.radians(ang))], ":", color=GRAY)
ax.plot(-1, 0, "o", mfc="white", mec=GRAY); ax.annotate("centroide σa = −1", (-1, 0), (-2.9, -1.4), fontsize=9, arrowprops=dict(arrowstyle="->", color=GRAY))
ax.plot(-0.4226, 0, "s", color=ORANGE, ms=7); ax.annotate("ponto de saída\ns = −0,4226 (K = 0,385)", (-.4226, 0), (.15, -.75), fontsize=9, color=ORANGE, arrowprops=dict(arrowstyle="->", color=ORANGE))
for s in [1, -1]: ax.plot(0, s * np.sqrt(2), "D", color=RED, ms=7)
ax.annotate("cruza jω: s = ±j1,414\nK = 6 (limite de estabilidade)", (0, 1.414), (.15, 1.9), fontsize=9, color=RED, arrowprops=dict(arrowstyle="->", color=RED))
p1 = np.roots([1, 3, 2, 1])
ax.plot(p1.real, p1.imag, "o", color=GREEN, ms=7); ax.annotate("K = 1: −0,3376 ± j0,5623\ne −2,3247", (-.3376, .5623), (-3.4, 1.3), fontsize=9, color=GREEN, arrowprops=dict(arrowstyle="->", color=GREEN))
th = np.arccos(.5); r = np.linspace(0, 3, 10); ax.plot(-r * np.cos(th), r * np.sin(th), "--", color=PURPLE, lw=1)
ax.text(-1.55, 2.55, "reta ζ = 0,5", color=PURPLE, fontsize=9)
ax.plot(-1/3, .5774, "*", color=PURPLE, ms=12); ax.annotate("ζ=0,5: s=−0,333+j0,577\nK = 1,037", (-1/3, .5774), (.3, .45), fontsize=9, color=PURPLE, arrowprops=dict(arrowstyle="->", color=PURPLE))
ax.axhline(0, color="k", lw=.7); ax.axvline(0, color="k", lw=.7)
ax.set_xlim(-3.6, 1.6); ax.set_ylim(-3, 3); ax.set_aspect("equal"); ax.set_xlabel("σ"); ax.set_ylabel("jω")
ax.set_title("Lugar das raízes de  G(s)H(s) = K / [s(s+1)(s+2)]")
save("lgr_principal")

# rule illustration: real-axis segments
fig, ax = plt.subplots(figsize=(6.5, 1.6))
ax.axhline(0, color="k", lw=.7); ax.set_yticks([]); ax.set_xlim(-4, 1); ax.set_ylim(-.6, .8)
ax.plot([0, -1, -2], [0, 0, 0], "x", color="k", ms=10, mew=2)
ax.plot([-1, 0], [0, 0], color=BLUE, lw=5); ax.plot([-4, -2], [0, 0], color=BLUE, lw=5)
for x, n in [(.5, 0), (-.5, 1), (-1.5, 2), (-3, 3)]:
    ax.text(x, .35, f"{n} à direita\n→ {'SIM' if n % 2 else 'não'}", ha="center", fontsize=8, color=BLUE if n % 2 else GRAY)
ax.grid(False); ax.set_title("Regra do eixo real: é LGR onde há nº ÍMPAR de polos+zeros à direita", fontsize=9)
save("regra_eixo")

# ---------- lead example: 4/(s(s+2)) -> Gc = 4(s+2)/(s+4) ----------
fig, axs = plt.subplots(1, 2, figsize=(9, 4), gridspec_kw=dict(width_ratios=[1,1.3]))
ax = axs[0]
Ks = np.linspace(0, 60, 2000)
R1 = rlocus([4.0], [1, 2, 0], Ks)
for i in range(2): ax.plot(R1[:, i].real, R1[:, i].imag, color=GRAY, lw=1.5, label="sem compensador" if i == 0 else None)
R2 = rlocus([4.0], [1, 4, 0], Ks)  # 4K(s+2)/((s+4)s(s+2)) = 4K/(s(s+4))
for i in range(2): ax.plot(R2[:, i].real, R2[:, i].imag, color=RED, lw=1.8, label="com avanço" if i == 0 else None)
ax.plot([0, -2], [0, 0], "x", color="k", ms=9, mew=2); ax.plot(-4, 0, "x", color=RED, ms=9, mew=2)
ax.plot(-2, 0, "o", mfc="none", mec=RED, ms=11)
sd = complex(-2, 2 * np.sqrt(3)); ax.plot([sd.real] * 2, [sd.imag, -sd.imag], "*", color=GREEN, ms=13)
ax.text(-1.85, 3.5, "$s_d=-2\\pm j3{,}46$", color=GREEN, fontsize=9)
th = np.arccos(.5); r = np.linspace(0, 5, 5); ax.plot(-r * np.cos(th), r * np.sin(th), "--", color=PURPLE, lw=.8)
ax.axhline(0, color="k", lw=.7); ax.axvline(0, color="k", lw=.7)
ax.set_xlim(-5, 1); ax.set_ylim(-4.5, 4.5); ax.set_aspect("equal"); ax.legend(fontsize=8, loc="lower left"); ax.set_title("LGR", fontsize=10)
ax = axs[1]; tt = np.linspace(0, 6, 600)
_, y0 = signal.step(([4], [1, 2, 4]), T=tt); _, y1 = signal.step(([16], [1, 4, 16]), T=tt)
ax.plot(tt, y0, color=GRAY, label="sem: ζ=0,5, ωn=2"); ax.plot(tt, y1, color=RED, label="com avanço: ζ=0,5, ωn=4")
ax.axhline(1, color="k", lw=.6, ls=":"); ax.legend(fontsize=8); ax.set_xlabel("t (s)"); ax.set_title("Degrau em malha fechada", fontsize=10)
plt.tight_layout(); save("avanco_exemplo")

# ---------- lag example (aula) ----------
fig, axs = plt.subplots(1, 2, figsize=(8, 3.4))
tt = np.linspace(0, 40, 4000)
G0 = ([1], [1, 3, 2, 1])
Kc = 0.975
numc = Kc * np.array([1, .05]); denol = np.polymul([1, .005], [1, 3, 2, 0])
G1 = (numc, np.polyadd(denol, numc))
_, y0 = signal.step(G0, T=tt); _, y1 = signal.step(G1, T=tt)
ax = axs[0]; ax.plot(tt, y0, color=GRAY, label="sem compensador"); ax.plot(tt, y1, color=BLUE, label="com atraso", ls="--")
ax.axhline(1, color="k", lw=.6, ls=":"); ax.set_xlim(0, 25); ax.legend(fontsize=8); ax.set_title("Degrau: transitório quase igual", fontsize=10); ax.set_xlabel("t (s)")
tt2 = np.linspace(0, 150, 6000)
_, r0, _ = signal.lsim(G0, tt2, tt2); _, r1, _ = signal.lsim(G1, tt2, tt2)
ax = axs[1]; ax.plot(tt2, tt2 - r0, color=GRAY, label="erro sem: → 2"); ax.plot(tt2, tt2 - r1, color=BLUE, label="erro com atraso: → 0,205")
ax.axhline(2, color=GRAY, ls=":", lw=.8); ax.axhline(.205, color=BLUE, ls=":", lw=.8)
ax.legend(fontsize=8); ax.set_title("Erro para entrada rampa  e(t)=t−c(t)", fontsize=10); ax.set_xlabel("t (s)")
plt.tight_layout(); save("atraso_exemplo")

# ---------- circuits ----------
def resistor(ax, x0, y0, x1, y1, n=6, w=.12):
    L = np.hypot(x1 - x0, y1 - y0); ux, uy = (x1 - x0) / L, (y1 - y0) / L; px, py = -uy, ux
    pts = [(x0, y0)]; seg = L * .6 / (2 * n); s0 = L * .2
    pts.append((x0 + ux * s0, y0 + uy * s0))
    for k in range(2 * n):
        d = s0 + seg * (k + .5); sgn = 1 if k % 2 == 0 else -1
        pts.append((x0 + ux * d + px * w * sgn, y0 + uy * d + py * w * sgn))
    pts.append((x0 + ux * (L - s0), y0 + uy * (L - s0))); pts.append((x1, y1))
    ax.plot(*zip(*pts), "k", lw=1.3)
def cap(ax, x0, y0, x1, y1, gap=.08, h=.22):
    L = np.hypot(x1 - x0, y1 - y0); ux, uy = (x1 - x0) / L, (y1 - y0) / L; px, py = -uy, ux
    m = ((x0 + x1) / 2, (y0 + y1) / 2)
    a = (m[0] - ux * gap, m[1] - uy * gap); b = (m[0] + ux * gap, m[1] + uy * gap)
    ax.plot([x0, a[0]], [y0, a[1]], "k", lw=1.3); ax.plot([b[0], x1], [b[1], y1], "k", lw=1.3)
    for c in (a, b): ax.plot([c[0] - px * h, c[0] + px * h], [c[1] - py * h, c[1] + py * h], "k", lw=2)
def terminals(ax, xin, xout, ytop, ybot):
    for x in (xin, xout):
        for y in (ytop, ybot): ax.plot(x, y, "o", mfc="white", mec="k", ms=6)

# lead network
fig, ax = plt.subplots(figsize=(5.2, 2.6)); ax.axis("off"); ax.set_aspect("equal")
ax.plot([0, 1], [1.5, 1.5], "k", lw=1.3); ax.plot([1, 1], [1.5, 2.1], "k", lw=1.3); ax.plot([1, 1], [1.5, 0.9], "k", lw=1.3)
resistor(ax, 1, 2.1, 3, 2.1); cap(ax, 1, .9, 3, .9)
ax.plot([3, 3], [2.1, .9], "k", lw=1.3); ax.plot([3, 5], [1.5, 1.5], "k", lw=1.3)
ax.text(2, 2.35, "$R_1$", ha="center"); ax.text(2, .5, "$C_1$", ha="center")
resistor(ax, 4, 1.5, 4, -.2); ax.text(4.25, .65, "$R_2$")
ax.plot([0, 5], [-.2, -.2], "k", lw=1.3); terminals(ax, 0, 5, 1.5, -.2)
ax.text(-.2, .65, "$e_i$", ha="right", fontsize=12); ax.text(5.2, .65, "$e_o$", fontsize=12)
ax.set_title("Rede de AVANÇO: capacitor em paralelo com o resistor série", fontsize=9.5, pad=18)
save("rede_avanco")

# lag network
fig, ax = plt.subplots(figsize=(5.2, 2.6)); ax.axis("off"); ax.set_aspect("equal")
resistor(ax, 0, 1.5, 2.2, 1.5); ax.text(1.1, 1.75, "$R_1$", ha="center")
ax.plot([2.2, 5], [1.5, 1.5], "k", lw=1.3)
resistor(ax, 3.2, 1.5, 3.2, .55); cap(ax, 3.2, .55, 3.2, -.2)
ax.text(3.45, 1.0, "$R_2$"); ax.text(3.5, .15, "$C$")
ax.plot([0, 5], [-.2, -.2], "k", lw=1.3); terminals(ax, 0, 5, 1.5, -.2)
ax.text(-.2, .65, "$e_i$", ha="right", fontsize=12); ax.text(5.2, .65, "$e_o$", fontsize=12)
ax.set_title("Rede de ATRASO: capacitor em série com R₂ no ramo de saída", fontsize=9.5, pad=18)
save("rede_atraso")

# capacitor phasor + waveforms
fig, axs = plt.subplots(1, 2, figsize=(8, 2.8))
t = np.linspace(0, 2 * np.pi * 2, 500)
ax = axs[0]; ax.plot(t, np.sin(t), color=BLUE, label="tensão v(t)"); ax.plot(t, np.cos(t), color=RED, label="corrente i(t) = C dv/dt")
ax.annotate("", (np.pi / 2 - np.pi / 2, 1.05), (np.pi / 2, 1.05), arrowprops=dict(arrowstyle="<->", color="k"))
ax.text(np.pi / 4, 1.15, "90°", ha="center", fontsize=9); ax.set_ylim(-1.3, 1.45)
ax.legend(fontsize=8, loc="lower left"); ax.set_title("No capacitor a corrente ADIANTA 90°", fontsize=10); ax.set_xticks([])
ax = axs[1]; ax.set_aspect("equal"); ax.axhline(0, color="k", lw=.6); ax.axvline(0, color="k", lw=.6)
ax.annotate("", (1, 0), (0, 0), arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=2)); ax.text(1.02, -.15, "V", color=BLUE)
ax.annotate("", (0, 1), (0, 0), arrowprops=dict(arrowstyle="-|>", color=RED, lw=2)); ax.text(.05, 1.0, "I", color=RED)
ax.add_patch(Arc((0, 0), .6, .6, theta1=0, theta2=90, color="k")); ax.text(.3, .3, "+90°")
ax.set_xlim(-.3, 1.3); ax.set_ylim(-.3, 1.2); ax.set_title("Fasores: $Z_C = 1/(j\\omega C)$", fontsize=10); ax.grid(False)
plt.tight_layout(); save("capacitor")

# lead phase plot
fig, ax = plt.subplots(figsize=(6.5, 2.8))
w = np.logspace(-1, 2, 600)
for a, c in [(.5, BLUE), (.2, ORANGE), (.1, RED)]:
    T = 1 / 2.0  # zero at 2 rad/s
    jw = 1j * w; G = (T * jw + 1) / (a * T * jw + 1)
    ph = np.degrees(np.angle(G)); ax.semilogx(w, ph, color=c, label=f"α = {a}: φmax = {np.degrees(np.arcsin((1-a)/(1+a))):.1f}°")
    wm = 1 / (T * np.sqrt(a)); ax.plot(wm, np.degrees(np.arcsin((1 - a) / (1 + a))), "o", color=c)
ax.set_xlabel("ω (rad/s)"); ax.set_ylabel("fase (graus)"); ax.legend(fontsize=8)
ax.set_title("Fase de $(Ts+1)/(\\alpha Ts+1)$ — sempre POSITIVA (avanço)", fontsize=10)
save("fase_avanco")

# first order step
fig, ax = plt.subplots(figsize=(5.5, 2.6)); tt = np.linspace(0, 5, 400); y = 1 - np.exp(-tt)
ax.plot(tt, y, color=BLUE); ax.axhline(1, ls=":", color="k", lw=.6)
ax.plot(1, 1 - np.exp(-1), "o", color=RED); ax.annotate("t = τ → 63,2%", (1, .632), (1.5, .4), color=RED, arrowprops=dict(arrowstyle="->", color=RED), fontsize=9)
ax.plot(4, 1 - np.exp(-4), "o", color=GREEN); ax.annotate("t = 4τ → 98% (ts)", (4, .982), (2.6, .75), color=GREEN, arrowprops=dict(arrowstyle="->", color=GREEN), fontsize=9)
ax.set_xlabel("t/τ"); ax.set_title("1ª ordem: $1/(\\tau s+1)$, polo em $s=-1/\\tau$", fontsize=10)
save("primeira_ordem")
print("ok")

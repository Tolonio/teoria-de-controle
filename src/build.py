import os, hashlib, io
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, Image,
                                Table, TableStyle, PageBreak, KeepTogether, CondPageBreak)

F = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("DV", F + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DVB", F + "DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DVI", F + "DejaVuSans-Oblique.ttf"))
pdfmetrics.registerFont(TTFont("DVBI", F + "DejaVuSans-BoldOblique.ttf"))
from reportlab.pdfbase.pdfmetrics import registerFontFamily
registerFontFamily("DV", normal="DV", bold="DVB", italic="DVI", boldItalic="DVBI")
pdfmetrics.registerFont(TTFont("DejaVuSansMono", F + "DejaVuSansMono.ttf")); registerFontFamily("DejaVuSansMono", normal="DejaVuSansMono", bold="DejaVuSansMono", italic="DejaVuSansMono", boldItalic="DejaVuSansMono")

NAVY = colors.HexColor("#1f3b63"); BLUE = colors.HexColor("#1f5fa8")
body = ParagraphStyle("b", fontName="DV", fontSize=10.5, leading=14.5, alignment=TA_JUSTIFY, spaceAfter=5)
bl = ParagraphStyle("bl", parent=body, leftIndent=14, bulletIndent=4, spaceAfter=2.5)
h1 = ParagraphStyle("h1", fontName="DVB", fontSize=17, leading=21, textColor=NAVY, spaceBefore=4, spaceAfter=9)
h2 = ParagraphStyle(keepWithNext=1, name="h2", fontName="DVB", fontSize=12.5, leading=16, textColor=BLUE, spaceBefore=9, spaceAfter=5)
h3 = ParagraphStyle(keepWithNext=1, name="h3", fontName="DVB", fontSize=11, leading=14, textColor=colors.HexColor("#333"), spaceBefore=6, spaceAfter=3)
cap = ParagraphStyle("cap", fontName="DVI", fontSize=8.8, leading=11, alignment=TA_CENTER, textColor=colors.HexColor("#555"), spaceAfter=8)
boxs = ParagraphStyle("bx", parent=body, fontSize=10, leading=13.5, spaceAfter=2)
tcell = ParagraphStyle("tc", fontName="DV", fontSize=9.3, leading=12, alignment=TA_CENTER)
tcellb = ParagraphStyle("tcb", parent=tcell, fontName="DVB", textColor=colors.white)

os.makedirs("eq", exist_ok=True)
plt.rcParams["mathtext.fontset"] = "cm"

def eq(tex, size=15, w=None):
    """display equation rendered with matplotlib mathtext"""
    fn = "eq/" + hashlib.md5((tex + str(size)).encode()).hexdigest() + ".png"
    if not os.path.exists(fn):
        fig = plt.figure(figsize=(.01, .01))
        fig.text(0, 0, f"${tex}$", fontsize=size)
        fig.savefig(fn, dpi=300, bbox_inches="tight", pad_inches=.03, transparent=True)
        plt.close(fig)
    from PIL import Image as PI
    im = PI.open(fn); pw, ph = im.size
    width = pw / 300 * 72 * 1.25; height = ph / 300 * 72 * 1.25
    if w and width > w: height *= w / width; width = w
    if width > 16.5 * cm: height *= 16.5 * cm / width; width = 16.5 * cm
    img = Image(fn, width=width, height=height); img.hAlign = "CENTER"
    return KeepTogether([Spacer(1, 2), img, Spacer(1, 4)])

import re as _re
_src = open(__file__, encoding="utf-8").read()
FN = {}
for _m in _re.finditer(r'fig\("(\w+)",\s*[\d.]+,\s*"Figura', _src):
    FN.setdefault(_m.group(1), len(FN) + 1)
def fig(name, width_cm, caption=None):
    if caption: caption = _re.sub(r"^Figura\s*\d*\s*–", f"Figura {FN.get(name, '')} –", caption)
    from PIL import Image as PI
    fn = f"fig/{name}.png"; im = PI.open(fn); pw, ph = im.size
    w = width_cm * cm; h = w * ph / pw
    items = [Image(fn, width=w, height=h)]
    if caption: items.append(Paragraph(caption, cap))
    return KeepTogether(items)

def P(t): return Paragraph(t, body)
def B(items): return [Paragraph(t, bl, bulletText="•") for t in items]

def box(title, content, color="#eaf2fb", border="#1f5fa8"):
    rows = [[Paragraph(f"<b>{title}</b>", ParagraphStyle("bt", parent=boxs, textColor=colors.HexColor(border)))]]
    for c in content:
        if isinstance(c, str): rows.append([Paragraph(c, boxs)])
        elif isinstance(c, KeepTogether): rows.append([c._content])
        else: rows.append([c])
    t = Table(rows, colWidths=[16.4 * cm], splitByRow=1)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.HexColor(color)),
                           ("LINEBEFORE", (0, 0), (0, -1), 3, colors.HexColor(border)),
                           ("LEFTPADDING", (0, 0), (-1, -1), 9), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                           ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                           ("TOPPADDING", (0, 0), (-1, 0), 6), ("BOTTOMPADDING", (0, -1), (-1, -1), 7)]))
    return [Spacer(1, 3), KeepTogether([t]), Spacer(1, 7)]

def dica(*c): return box("Como encarar", list(c), "#fff6e5", "#d35400")
def exemplo(title, *c): return box(title, list(c), "#eef7ee", "#1e8449")
def resumo(*c): return box("Resumo", list(c), "#eaf2fb", "#1f5fa8")

def table(rows, widths, head=True):
    data = [[Paragraph(str(c), tcellb if (head and i == 0) else tcell) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=[w * cm for w in widths])
    st = [("GRID", (0, 0), (-1, -1), .5, colors.HexColor("#aab")), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
          ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f3f6fa")])]
    if head: st.append(("BACKGROUND", (0, 0), (-1, 0), NAVY))
    t.setStyle(TableStyle(st)); return [KeepTogether([t]), Spacer(1, 8)]

S = []
# ================= CAPA =================
S += [Spacer(1, 3 * cm),
      Paragraph("Teoria de Controle", ParagraphStyle("t", fontName="DVB", fontSize=30, leading=36, textColor=NAVY, alignment=TA_CENTER)),
      Spacer(1, 10),
      Paragraph("Guia de estudo: da função de transferência ao lugar das raízes e aos compensadores de avanço e atraso",
                ParagraphStyle("st", fontName="DV", fontSize=14, leading=19, alignment=TA_CENTER, textColor=BLUE)),
      Spacer(1, 1.2 * cm), fig("lgr_principal", 12),
      Spacer(1, .6 * cm),
      Paragraph("Montado a partir das anotações da aula (sistema 1/[s(s+1)(s+2)], compensador K<sub>c</sub>(s+0,05)/(s+0,005)), "
                "com teoria, exemplos numéricos conferidos e exercícios resolvidos.", ParagraphStyle("c", parent=cap, fontSize=10, leading=13)),
      PageBreak()]

S += [Paragraph("Sumário", h1)]
for t in ["0. Como encarar a matéria (o mapa)", "A. Amplificador operacional: o controle em forma de circuito", "1. Laplace, função de transferência e diagramas de blocos", "2. Polos, zeros e a resposta do sistema",
          "3. Tipo do sistema e erro em regime permanente", "4. Lugar das raízes (LGR)", "5. Como achar o K",
          "6. Compensadores e controladores: avanço, atraso, PID e on-off", "7. Exercícios resolvidos (aula + suas listas)", "8. Exercícios propostos (com gabarito)",
          "9. Formulário de bolso e comandos do MATLAB"]:
    S.append(Paragraph(t, ParagraphStyle("su", parent=body, fontSize=11.5, leading=19, leftIndent=10)))

# ================= 0 =================
S += [Spacer(1, 10), Paragraph("0. Como encarar a matéria (o mapa)", h1),
      P("Quase todo problema desta disciplina segue o mesmo caminho. Se você souber em que etapa está, sabe qual ferramenta usar:")]
S += table([["Etapa", "Pergunta", "Ferramenta"],
            ["1. Modelar", "Como a planta se comporta?", "Função de transferência G(s)"],
            ["2. Fechar a malha", "Como fica com realimentação?", "FTMF = G/(1+GH); equação característica 1+GH=0"],
            ["3. Analisar", "É estável? Oscila? É rápido?", "Polos da malha fechada, ζ, ω<sub>n</sub>, Routh"],
            ["4. Precisão", "Segue a referência sem erro?", "Tipo do sistema, K<sub>p</sub>, K<sub>v</sub>, K<sub>a</sub>, e(∞)"],
            ["5. Ajustar ganho", "Que K deixa como eu quero?", "Lugar das raízes + condição de módulo"],
            ["6. Compensar", "Só ganho não resolve. E agora?", "Avanço (transitório), atraso (erro), PID"]],
           [3.2, 5.6, 7.6])
S += dica("Em toda questão, escreva primeiro a <b>FTMA</b> (malha aberta) e a <b>equação característica</b> 1 + FTMA = 0. "
          "Polos de malha fechada = raízes dessa equação. Erro em regime sai da FTMA. O LGR também é desenhado a partir da FTMA. "
          "Ou seja: a FTMA é o ponto de partida de quase tudo.",
          "Transitório (oscilação, rapidez) → olhe os <b>polos de malha fechada</b>. "
          "Regime (erro) → olhe o <b>tipo</b> e o <b>ganho de baixa frequência</b> da FTMA.")
S.append(CondPageBreak(25 * cm))

# ================= A amp-op =================
S += [Paragraph("A. Amplificador operacional: o controle em forma de circuito", h1),
      P("Antes das contas, vale entender <b>com que peça física</b> se monta um controlador analógico. Quase sempre é o amplificador operacional (amp-op). "
        "Somador do erro, ganho K<sub>p</sub>, integrador, derivador, avanço, atraso e PID inteiro são todos amp-ops com resistores e capacitores em volta. "
        "Dominando duas regras e uma fórmula, você lê qualquer circuito de controle."),
      Paragraph("A.1 O que é", h2),
      P("É um amplificador <b>diferencial</b> de ganho enorme: v<sub>o</sub> = A(v<sub>+</sub> − v<sub>−</sub>), com A da ordem de 10<super>5</super> a 10<super>6</super>. "
        "Tem duas entradas (inversora −, não inversora +), uma saída e é alimentado por ±V<sub>cc</sub> (ex.: ±12 V). "
        "A saída nunca passa da alimentação: se a conta der 20 V com fonte de 12 V, ela <b>satura</b> em ~12 V."),
      fig("ampop", 16.5, "Figura 0 – Amp-op ideal e os circuitos básicos usados em controle."),
      Paragraph("A.2 As duas regras de ouro (amp-op ideal)", h2)]
S += B(["<b>Regra 1 – não entra corrente nas entradas:</b> i<sub>+</sub> = i<sub>−</sub> = 0 (impedância de entrada infinita).",
        "<b>Regra 2 – curto-circuito virtual:</b> com realimentação <b>negativa</b> (saída ligada de volta à entrada −), v<sub>+</sub> = v<sub>−</sub>. "
        "Motivo: v<sub>+</sub> − v<sub>−</sub> = v<sub>o</sub>/A. Com A ≈ 10<super>5</super> e v<sub>o</sub> de poucos volts, a diferença é de microvolts, praticamente zero.",
        "Repare: o amp-op realimentado <b>já é um sistema de controle em malha fechada</b>. Ele mexe na saída até zerar o \"erro\" v<sub>+</sub> − v<sub>−</sub>."])
S += [Paragraph("A.3 Inversor e a fórmula que resolve tudo: −Z<sub>f</sub>/Z<sub>i</sub>", h2),
      P("No inversor, v<sub>+</sub> = 0 ⇒ v<sub>−</sub> = 0 (terra virtual). A corrente que entra por R<sub>1</sub>, v<sub>i</sub>/R<sub>1</sub>, não entra no amp-op (regra 1). "
        "Então ela passa toda por R: v<sub>i</sub>/R<sub>1</sub> = −v<sub>o</sub>/R ⇒ <b>v<sub>o</sub> = −(R/R<sub>1</sub>)v<sub>i</sub></b>. "
        "Trocando os resistores por impedâncias no domínio s (resistor R, capacitor 1/(sC)), vale para qualquer rede:"),
      eq(r"\frac{V_o(s)}{V_i(s)}=-\frac{Z_f(s)}{Z_i(s)}\qquad Z_R=R,\quad Z_C=\frac{1}{sC}"),
      Paragraph("A.4 Não inversor e diferencial (slides da aula)", h2),
      P("<b>Não inversor:</b> v<sub>i</sub> entra no +. Pela regra 2, v<sub>−</sub> = v<sub>i</sub>, e v<sub>−</sub> sai do divisor R<sub>1</sub>–R: v<sub>−</sub> = v<sub>o</sub>·R<sub>1</sub>/(R<sub>1</sub>+R). "
        "Logo <b>v<sub>c</sub> = (1 + R/R<sub>1</sub>)·v<sub>E</sub></b>: ganho positivo, sempre ≥ 1."),
      P("<b>Diferencial:</b> a referência v<sub>R</sub> entra pelo + e a medida do sensor v<sub>Y</sub> pelo −. Com resistores casados, <b>v<sub>c</sub> = (R/R<sub>1</sub>)(v<sub>R</sub> − v<sub>Y</sub>)</b>. "
        "Este circuito faz duas coisas ao mesmo tempo: o <b>somador</b> da malha (e = r − y) e o <b>ganho K<sub>p</sub> = R/R<sub>1</sub></b>. É um controlador proporcional completo. "
        "No slide, R é um potenciômetro: girar o potenciômetro é ajustar o K<sub>p</sub>, que é exatamente andar sobre o lugar das raízes."),
      Paragraph("A.5 Cada ação de controle é uma escolha de Z<sub>i</sub> e Z<sub>f</sub>", h2)]
S += table([["Ação", "Z<sub>i</sub> (entrada)", "Z<sub>f</sub> (realimentação)", "V<sub>o</sub>/V<sub>i</sub>", "Parâmetros"],
            ["P", "R<sub>1</sub>", "R<sub>2</sub>", "−R<sub>2</sub>/R<sub>1</sub>", "K<sub>p</sub> = R<sub>2</sub>/R<sub>1</sub>"],
            ["I (integrador)", "R<sub>1</sub>", "C", "−1/(R<sub>1</sub>Cs)", "K<sub>i</sub> = 1/(R<sub>1</sub>C)"],
            ["D (derivador)", "C", "R<sub>2</sub>", "−R<sub>2</sub>Cs", "K<sub>d</sub> = R<sub>2</sub>C"],
            ["PI", "R<sub>1</sub>", "R<sub>2</sub> em série com C", "−(R<sub>2</sub>/R<sub>1</sub>)[1 + 1/(R<sub>2</sub>Cs)]", "K<sub>p</sub> = R<sub>2</sub>/R<sub>1</sub>, T<sub>i</sub> = R<sub>2</sub>C"],
            ["PD", "R<sub>1</sub> ∥ C", "R<sub>2</sub>", "−(R<sub>2</sub>/R<sub>1</sub>)(1 + R<sub>1</sub>Cs)", "K<sub>p</sub> = R<sub>2</sub>/R<sub>1</sub>, T<sub>d</sub> = R<sub>1</sub>C"],
            ["Avanço / atraso", "R<sub>1</sub> ∥ C<sub>1</sub>", "R<sub>2</sub> ∥ C<sub>2</sub>", "−(R<sub>2</sub>/R<sub>1</sub>)(R<sub>1</sub>C<sub>1</sub>s+1)/(R<sub>2</sub>C<sub>2</sub>s+1)", "avanço se R<sub>1</sub>C<sub>1</sub> &gt; R<sub>2</sub>C<sub>2</sub>"]],
           [2.6, 2.6, 3.4, 4.6, 3.2])
S += [P("O sinal \"−\" do inversor é desfeito colocando um segundo inversor de ganho −1 em série (por isso os circuitos de compensador do Ogata usam dois amp-ops). "
        "Repare na fase: o integrador (1/s) <b>atrasa 90°</b> e o derivador (s) <b>adianta 90°</b>. É de onde vêm os nomes atraso e avanço de fase (seção 6).")]
S += exemplo("Exemplo – montar um PI com K<sub>p</sub> = 2 e T<sub>i</sub> = 0,5 s",
             P("Escolha C = 1 µF. De T<sub>i</sub> = R<sub>2</sub>C: R<sub>2</sub> = 0,5/10<super>−6</super> = <b>500 kΩ</b>. De K<sub>p</sub> = R<sub>2</sub>/R<sub>1</sub>: R<sub>1</sub> = 500k/2 = <b>250 kΩ</b>. "
               "Resultado: V<sub>o</sub>/V<sub>i</sub> = −2(1 + 1/(0,5s)) = −(2 + 4/s), ou seja, K<sub>p</sub> = 2 e K<sub>i</sub> = 4. Um inversor de ganho −1 depois corrige o sinal."),
             P("Cuidado prático: o integrador puro sem resistor em paralelo com C acumula offset e satura (é o \"wind-up\" da ação integral)."))
S += dica("Viu um amp-op numa questão? (1) Ache a realimentação negativa e aplique v<sub>+</sub> = v<sub>−</sub>. (2) Correntes nas entradas são zero. "
          "(3) Se for inversor, use direto −Z<sub>f</sub>/Z<sub>i</sub>, com capacitor = 1/(sC). Pronto: você tem a FT do controlador.")
S.append(CondPageBreak(25 * cm))

# ================= 1 FT =================
S += [Paragraph("1. Laplace, função de transferência e diagramas de blocos", h1),
      P("A <b>função de transferência</b> (FT) é a razão entre a transformada de Laplace da saída e a da entrada, "
        "considerando <b>condições iniciais nulas</b>. Ela transforma equações diferenciais em álgebra: derivar vira multiplicar por s, integrar vira dividir por s."),
      eq(r"G(s)=\frac{C(s)}{R(s)}\qquad \mathcal{L}\left\{\frac{dx}{dt}\right\}=sX(s)\qquad \mathcal{L}\left\{\int x\,dt\right\}=\frac{X(s)}{s}"),
      P("A forma geral (slide da aula) é uma razão de polinômios em s:"),
      eq(r"G_p(s)=\frac{b_0s^m+b_1s^{m-1}+\dots+b_{m-1}s+b_m}{a_0s^n+a_1s^{n-1}+\dots+a_{n-1}s+a_n}"),
      P("O grau n do denominador é a <b>ordem</b> do sistema (o número da maior derivada da EDO). Em sistemas físicos, n ≥ m (sistema <i>próprio</i>). "
        "As raízes de Q(s) (denominador) são os <b>polos</b>, e as de P(s) (numerador) são os <b>zeros</b>. Se n > m, sobram n − m <b>zeros no infinito</b>."),
      Paragraph("1.0 Transformada de Laplace: a ferramenta", h2),
      P("A analogia do seu caderno é ótima. Multiplicar XIV × VII em algarismos romanos é penoso. Você converte para 14 × 7, faz a conta fácil (98) e volta (XCVIII). "
        "Laplace faz isso com equações diferenciais: leva do domínio do tempo t para o domínio da frequência complexa s = σ + jω, onde derivadas e integrais viram multiplicação e divisão por s. "
        "Resolve-se a álgebra e volta-se com a transformada inversa."),
      eq(r"F(s)=\mathcal{L}\{f(t)\}=\int_0^{\infty}f(t)\,e^{-st}\,dt,\qquad s=\sigma+j\omega"),
      ]
S += table([["f(t)", "F(s)", "f(t)", "F(s)"],
            ["impulso δ(t)", "1", "e<super>−at</super>", "1/(s + a)"],
            ["degrau 1", "1/s", "sen ωt", "ω/(s² + ω²)"],
            ["rampa t", "1/s²", "cos ωt", "s/(s² + ω²)"],
            ["parábola t²/2", "1/s³", "e<super>−at</super>sen ωt", "ω/[(s+a)² + ω²]"],
            ["df/dt", "sF(s) − f(0)", "∫f dt", "F(s)/s"]], [3.6, 4.6, 3.6, 4.6])
S += [P("<b>Sinais de teste</b> (amplitude A): degrau A/s, rampa At → <b>A/s²</b>, parábola At²/2 → A/s³. Atenção: no caderno a rampa aparece como A/s, mas o correto é A/s². "
        "\"Sistema relaxado\" significa todas as condições iniciais nulas, a hipótese da função de transferência."),
      Paragraph("Resolvendo uma EDO em 4 passos (exemplo do caderno)", h3),
      P("y' + 2y = 1 com y(0) = 0. <b>Passos 1 e 2</b> (Laplace dos dois lados com a condição inicial): sY(s) − 0 + 2Y(s) = 1/s. "
        "<b>Passo 3</b> (isolar): Y(s) = 1/[s(s + 2)]. <b>Passo 4</b> (frações parciais e inversa): Y(s) = 0,5/s − 0,5/(s + 2) ⇒ <b>y(t) = 0,5 − 0,5e<super>−2t</super></b>. "
        "É um 1ª ordem com ganho estático K = 0,5 e τ = 0,5 s."),
      Paragraph("Resposta ao impulso e convolução", h3),
      P("Como ℒ{δ(t)} = 1, aplicando um impulso a saída é Y(s) = G(s)·1. Ou seja, a <b>resposta ao impulso g(t) = ℒ<super>−1</super>{G(s)}</b> é a própria função de transferência no tempo. "
        "O exemplo do caderno é uma marretada seca num manipulador. Para qualquer entrada, a saída é a convolução:"),
      eq(r"Y(s)=G(s)X(s)\ \Longleftrightarrow\ y(t)=\int_0^t g(\tau)\,x(t-\tau)\,d\tau"),
      P("Isso só vale para sistemas <b>lineares e invariantes no tempo</b> (LIT). Linear: vale a superposição, e dobrar a entrada dobra a saída. Invariante: as propriedades físicas não \"envelhecem\"."),

      Paragraph("1.1 Exemplo: circuito RC (1ª ordem)", h2),
      P("Resistor R em série e capacitor C na saída. Pela malha: e<sub>i</sub> = Ri + e<sub>o</sub> e i = C de<sub>o</sub>/dt. Aplicando Laplace:"),
      eq(r"E_i(s)=RCs\,E_o(s)+E_o(s)\;\Rightarrow\;\frac{E_o(s)}{E_i(s)}=\frac{1}{RCs+1}=\frac{1}{\tau s+1},\quad \tau=RC"),
      P("Tem um <b>polo</b> em s = −1/τ. A resposta ao degrau é 1 − e<super>−t/τ</super>: chega a 63,2% em t = τ e a 98% em 4τ."),
      fig("primeira_ordem", 11, "Figura 1 – Resposta ao degrau de um sistema de 1ª ordem."),
      Paragraph("1.2 Exemplo: massa-mola-amortecedor (2ª ordem)", h2),
      fig("massa_mola", 9, "Figura 0 – Massa m presa a uma mola k e a um amortecedor b, puxada pela força F(t)."),
      P("Forças na massa: mola F<sub>k</sub> = kx, amortecedor F<sub>b</sub> = b·dx/dt, inércia m·d²x/dt². Pela 2ª lei de Newton, F − kx − b·ẋ = m·ẍ:"),
      eq(r"m\ddot x+b\dot x+kx=F(t)\ \Rightarrow\ (ms^2+bs+k)X(s)=F(s)\ \Rightarrow\ G(s)=\frac{X(s)}{F(s)}=\frac{1/m}{s^2+\frac{b}{m}s+\frac{k}{m}}"),
      P("Comparando com a forma padrão s² + 2ζω<sub>n</sub>s + ω<sub>n</sub>²: <b>ω<sub>n</sub>² = k/m</b> (a mola dá a frequência) e <b>2ζω<sub>n</sub> = b/m</b> (o amortecedor dá o amortecimento), "
        "ou seja, ζ = b/(2√(km)). Em regime (ẋ = ẍ = 0) sobra kx = F: o deslocamento final é F/k. "
        "Exemplo das suas notas: m = 1, b = 2, k = 2 ⇒ s² + 2s + 2 = 0 ⇒ polos −1 ± j, ω<sub>n</sub> = √2 = 1,414, ζ = 0,707."),
      ]
S += exemplo("Exemplos de 1ª ordem do caderno: tanque de nível e barco",
             P("<b>Tanque:</b> a vazão é proporcional à diferença de nível: K[h<sub>i</sub>(t) − h<sub>o</sub>(t)] = dh<sub>o</sub>/dt. Laplace: K[H<sub>i</sub> − H<sub>o</sub>] = sH<sub>o</sub> ⇒ "
               "<b>H<sub>o</sub>/H<sub>i</sub> = K/(s + K) = 1/(τs + 1)</b>, com τ = 1/K."),
             P("Degrau de altura L: H<sub>i</sub> = L/s ⇒ H<sub>o</sub> = L/[s(τs + 1)] = A/s + B/(τs + 1). Igualando coeficientes: A = L e Aτ + B = 0 ⇒ B = −Lτ. "
               "Então H<sub>o</sub> = L[1/s − 1/(s + 1/τ)] ⇒ <b>h<sub>o</sub>(t) = L(1 − e<super>−t/τ</super>)</b>: vale 0 em t = 0, L em t → ∞ e 0,632L em t = τ."),
             P("<b>Barco (velocidade pela rotação da hélice):</b> empuxo f = Kω e atrito f<sub>B</sub> = Bv ⇒ m·dv/dt + Bv = Kω ⇒ "
               "<b>V/Ω = K/(ms + B) = (K/m)/(s + B/m)</b>. O polo é s = −B/m, sempre no semiplano esquerdo: o barco sempre estabiliza numa velocidade."))
S += [CondPageBreak(9 * cm), Paragraph("1.3 Malha aberta × malha fechada: a ideia", h2),
      P("<b>Malha aberta</b> é o controle \"cego\": a torradeira de 2 minutos não vê o pão queimando. A saída é só Y = G·R e ninguém confere o resultado. "
        "<b>Malha fechada</b> \"tem olhos\": mede a saída, compara com o que foi pedido e usa a diferença (o <b>erro</b>) para se corrigir o tempo todo."),
      ]
S += table([["Bloco", "Papel", "Braço robótico", "Controle de temperatura"],
            ["R(s) referência", "o que eu quero", "coordenada (x, y, z) da peça", "25 °C"],
            ["H(s) sensor", "os olhos", "encoders nas juntas", "termômetro lê 20 °C"],
            ["E(s) erro", "R − H·Y", "peça a 10 cm, garra a 2 cm: 8 cm", "25 − 20 = 5 °C"],
            ["G<sub>c</sub>(s) controlador", "o cérebro", "algoritmo calcula o sinal das juntas", "microcontrolador: \"está frio, potência alta\""],
            ["G<sub>a</sub>(s) atuador", "o músculo", "servomotores (torque)", "relé que liga a resistência"],
            ["G<sub>p</sub>(s) planta", "a coisa física", "braço com massa, inércia e gravidade", "volume de ar esquentando"],
            ["Y(s) saída", "o que acontece", "posição real da garra", "temperatura real"]], [3.4, 2.6, 5.0, 5.4])
S += [P("Matematicamente, cada bloco multiplica o que entra nele:"),
      eq(r"U=G_aG_c\,E,\quad Y=G_p\,U\ \Rightarrow\ \frac{Y}{E}=G_cG_aG_p=G(s);\qquad E=R-HY\ \Rightarrow\ \frac{Y}{R}=\frac{G}{1+GH}"),
      CondPageBreak(9 * cm), Paragraph("1.4 FTMA, FTMF e equação característica", h2),
      fig("malha", 15, "Figura 2 – Malha fechada com realimentação unitária (slide: Controlador → Atuador → Planta)."),
      P("<b>FTMA</b> (função de transferência de malha aberta) é o produto de tudo que está no caminho, incluindo a realimentação: G<sub>c</sub>G<sub>p</sub>H. "
        "<b>FTMF</b> (malha fechada) relaciona saída e referência:"),
      eq(r"\mathrm{FTMF}=\frac{C(s)}{R(s)}=\frac{G_cG_p}{1+G_cG_pH}\qquad\qquad E(s)=R(s)-C(s)=\frac{R(s)}{1+G_cG_p}"),
      P("A segunda expressão (do slide) é a base do erro em regime: o erro depende de 1/(1 + FTMA)."),
      ]
S += exemplo("Exemplo da aula",
             P("Planta G<sub>p</sub>(s) = 1/[s(s+1)(s+2)], com G<sub>c</sub> = 1 e H = 1."),
             eq(r"\mathrm{FTMA}=\frac{1}{s^3+3s^2+2s}\qquad \mathrm{FTMF}=\frac{\frac{1}{s^3+3s^2+2s}}{1+\frac{1}{s^3+3s^2+2s}}=\frac{1}{s^3+3s^2+2s+1}", 14),
             P("Equação característica: s<super>3</super> + 3s<super>2</super> + 2s + 1 = 0. Raízes (MATLAB, <font face='DejaVuSansMono'>roots([1 3 2 1])</font>): "
               "p<sub>1,2</sub> = −0,3376 ± j0,5623 e p<sub>3</sub> = −2,3247."))
S += dica("Truque para a FTMF com realimentação unitária: se FTMA = N(s)/D(s), então FTMF = N/(D + N). "
          "No exemplo, N = 1 e D = s<super>3</super>+3s<super>2</super>+2s, logo FTMF = 1/(s<super>3</super>+3s<super>2</super>+2s+1). Não precisa montar a fração dupla.")
S += [CondPageBreak(9 * cm), Paragraph("1.5 Diagramas de blocos, redução e Mason", h2),
      P("Três peças: o <b>bloco</b> (saída = G × entrada), o <b>somador</b> (o sinal de cada seta diz se soma ou subtrai) e o <b>ponto de ramificação</b> "
        "(o mesmo sinal segue para vários lugares). Com realimentação H(s):"),
      ]
S += B(["<b>FT do ramo direto:</b> G(s) = C(s)/E(s).",
        "<b>FT da malha de realimentação:</b> B(s)/C(s) = H(s).",
        "<b>FT de malha aberta:</b> B(s)/E(s) = G(s)H(s). <b>FTMF</b> = FT direta/(1 + FTMA) = G/(1 + GH).",
        "<b>Erro atuante</b> E = R − B (o que o controlador enxerga) × <b>erro de resposta</b> E<sub>R</sub> = R − Y (o que importa). Se H = 1, são iguais."])
S += table([["Situação", "Equivale a"],
            ["Blocos em série G<sub>1</sub> → G<sub>2</sub>", "G<sub>1</sub>G<sub>2</sub>"],
            ["Blocos em paralelo (somados)", "G<sub>1</sub> + G<sub>2</sub>"],
            ["Malha G com realimentação negativa H", "G/(1 + GH)"],
            ["Distúrbio D(s) somado antes de G<sub>2</sub>", "superposição: C/R com D = 0 e C/D com R = 0"]], [8, 8.4])
S += [Paragraph("Fórmula do ganho de Mason", h3),
      eq(r"M=\frac{1}{\Delta}\sum_k M_k\Delta_k,\qquad \Delta=1-\sum L_i+\sum L_iL_j-\dots"),
      P("M<sub>k</sub> = ganho de cada caminho direto da entrada à saída. L<sub>i</sub> = ganho de cada malha (fecha no mesmo nó em que começou, com o sinal do somador). "
        "Σ L<sub>i</sub>L<sub>j</sub> = produtos de pares de malhas que <b>não se tocam</b>. Δ<sub>k</sub> = Δ calculado só com as malhas que não tocam o caminho k.")]
S += exemplo("Exemplo do caderno – conferido",
             P("Caminhos: M<sub>1</sub> = G<sub>1</sub>G<sub>2</sub>G<sub>3</sub> e M<sub>2</sub> = G<sub>4</sub>. Malhas: −G<sub>1</sub>G<sub>2</sub>H<sub>1</sub>, −G<sub>2</sub>G<sub>3</sub>H<sub>2</sub>, −G<sub>1</sub>G<sub>2</sub>G<sub>3</sub>, −G<sub>4</sub> "
               "e +G<sub>2</sub>G<sub>4</sub>H<sub>1</sub>H<sub>2</sub> (passa por G<sub>4</sub>, −H<sub>2</sub>, G<sub>2</sub> e −H<sub>1</sub>). Todas se tocam, então não há termos de pares. Os dois caminhos tocam todas as malhas: Δ<sub>1</sub> = Δ<sub>2</sub> = 1."),
             eq(r"\frac{Y}{R}=\frac{G_1G_2G_3+G_4}{1+G_4+G_1G_2G_3+G_1G_2H_1+G_2G_3H_2-G_2G_4H_1H_2}", 13),
             P("Bate com o caderno ✓. A malha interna G<sub>1</sub>G<sub>2</sub> com H<sub>1</sub> sozinha reduz para G<sub>1</sub>G<sub>2</sub>/(1 + G<sub>1</sub>G<sub>2</sub>H<sub>1</sub>), como na sua redução."))
S += [Paragraph("Sensibilidade: por que realimentar", h3),
      P("Sensibilidade de M = G/(1+GH) a um parâmetro x é a variação percentual de M dividida pela de x: S<super>M</super><sub>x</sub> = (∂M/∂x)(x/M)."),
      eq(r"S^M_G=\frac{1}{1+GH}\qquad S^M_H=-\frac{GH}{1+GH}"),
      P("Com GH grande, S<super>M</super><sub>G</sub> → 0: a malha fechada fica <b>imune a variações da planta</b> (desgaste, temperatura, carga). Esse é o grande motivo de realimentar. "
        "Mas S<super>M</super><sub>H</sub> → −1: um erro de 1% no <b>sensor</b> vira 1% de erro na saída. A malha fechada é tão boa quanto o sensor."),
      P("<b>Fatorar a equação característica (Briot-Ruffini / divisão):</b> se você conhece uma raiz ou um fator, divida. Ex.: (s<super>3</super>+3s<super>2</super>+3s+1) ÷ (s<super>2</super>+2s+1) = s + 1 ⇒ (s+1)<super>3</super>.")]
S.append(CondPageBreak(25 * cm))

# ================= 2 polos zeros =================
S += [Paragraph("2. Polos, zeros e a resposta do sistema", h1),
      P("<b>Polos</b> são as raízes do <b>denominador</b> da FT: valores de s que fazem G(s) → ∞. "
        "Eles definem os <b>modos naturais</b> do sistema, ou seja, os termos e<super>pt</super> que aparecem na resposta. "
        "<b>Zeros</b> são as raízes do <b>numerador</b>: valores de s que fazem G(s) = 0. Eles não criam novos modos, mas mudam o <i>peso</i> de cada modo "
        "(alteram sobressinal e formato)."),
      eq(r"G(s)=K\frac{(s-z_1)(s-z_2)\cdots}{(s-p_1)(s-p_2)\cdots}"),
      fig("plano_s", 13, "Figura 3 – Onde o polo está no plano s define como a resposta se comporta."),
      ]
S += table([["Posição do polo", "Termo na resposta", "Comportamento"],
            ["Real negativo  s = −a", "e<super>−at</super>", "Decai sem oscilar (quanto mais à esquerda, mais rápido)"],
            ["Complexo  −σ ± jω<sub>d</sub>", "e<super>−σt</super>cos(ω<sub>d</sub>t)", "Oscila amortecido"],
            ["Sobre o eixo jω", "cos(ωt)", "Oscila sem parar (marginalmente estável)"],
            ["Na origem  s = 0", "constante (integrador)", "Não decai: é o que dá o \"tipo\" do sistema"],
            ["Semiplano direito", "e<super>+at</super>", "Cresce: INSTÁVEL"]], [4.4, 3.8, 8.2])
S += [P("<b>Estabilidade:</b> o sistema em malha fechada é estável se e somente se <b>todos</b> os polos de malha fechada estiverem no semiplano esquerdo (parte real < 0). "
        "Motivo: cada polo p vira um termo e<super>pt</super>. Com p = −2, e<super>−2t</super> some com o tempo. Com p = +2, e<super>2t</super> cresce sem parar. "
        "Com K = 0 o controlador está desligado e os polos de MF ficam exatamente em cima dos polos de MA."),
      ]
S += exemplo("Exemplo das suas notas: a máquina com zero em +2",
             P("Planta com um polo em −4 (estável) e um zero em +2 (semiplano direito): G(s) = (s − 2)/(s + 4). Fechando a malha com ganho K: "
               "s + 4 + K(s − 2) = 0 ⇒ <b>s = (2K − 4)/(K + 1)</b>."),
             table([["K", "polo s", "o que acontece"], ["0", "−4", "malha aberta, estável"], ["1", "−1", "mais lento, mas estável"],
                    ["2", "0", "limite: polo na origem, a saída não volta (marginal)"], ["3", "+0,5", "instável: e<super>0,5t</super> cresce sem parar"]], [2, 3, 9])[0],
             fig("maquina_zero", 12.5, "Figura 0 – Polo de malha fechada em função de K: cruza para a direita em K = 2."),
             P("Leitura física (do seu caderno): com o polo à direita, a realimentação passa a <b>ajudar o erro a crescer</b>. O carro está rápido demais, o sensor lê, "
               "mas com o K mal ajustado o controlador acelera ainda mais. Um <b>zero no semiplano direito</b> \"puxa\" os polos para lá e limita o ganho (aqui, K &lt; 2)."),
             P("<b>Cuidado com um detalhe:</b> em K = 2 o polo fica em s = 0, e isso <b>não</b> é oscilação: a resposta simplesmente não decai (fica parada ou deriva). "
               "Oscilação sem parar é um <b>par</b> de polos sobre o eixo jω (±jω), como no K = 6 do sistema da aula."))
S += [
      Paragraph("2.1 Sistemas de 2ª ordem: ζ, ω<sub>n</sub>, ω<sub>d</sub>", h2),
      eq(r"\frac{C(s)}{R(s)}=\frac{\omega_n^2}{s^2+2\zeta\omega_n s+\omega_n^2}\qquad p_d=-\zeta\omega_n\pm j\omega_d,\quad \omega_d=\omega_n\sqrt{1-\zeta^2}"),
      P("<b>ω<sub>n</sub></b> (frequência natural) é a distância do polo à origem. <b>ζ</b> (coeficiente de amortecimento) é o cosseno do ângulo com o eixo real negativo. "
        "<b>σ = ζω<sub>n</sub></b> é a parte real (velocidade de decaimento) e <b>ω<sub>d</sub></b> é a frequência de oscilação amortecida."),
      fig("degrau_zeta", 12.5, "Figura 4 – Quanto menor ζ, maior o sobressinal. ζ=1: criticamente amortecido; ζ>1: superamortecido."),
      ]
S += table([["Especificação", "Fórmula", "Depende de"],
            ["Sobressinal M<sub>p</sub>", "e<super>−ζπ/√(1−ζ²)</super>", "só de ζ"],
            ["Tempo de pico t<sub>p</sub>", "π / ω<sub>d</sub>", "parte imaginária"],
            ["Tempo de acomodação t<sub>s</sub> (2%)", "4 / (ζω<sub>n</sub>) = 4/σ", "parte real"],
            ["Tempo de acomodação t<sub>s</sub> (5%)", "3 / (ζω<sub>n</sub>)", "parte real"]], [5.6, 5.6, 5.2])
S += exemplo("Exemplo da aula (quadro branco): achar ζ e ω<sub>n</sub> a partir do polo",
             P("Polo dominante p<sub>d</sub> = −0,3376 + j0,5623. Do quadro: ω<sub>d</sub><super>2</super> = ω<sub>n</sub><super>2</super>(1−ζ<super>2</super>) = ω<sub>n</sub><super>2</super> − ω<sub>n</sub><super>2</super>ζ<super>2</super>, logo ω<sub>n</sub><super>2</super> = ω<sub>d</sub><super>2</super> + (ζω<sub>n</sub>)<super>2</super>:"),
             eq(r"\omega_n=\sqrt{0{,}5623^2+0{,}3376^2}=0{,}6559\ \mathrm{rad/s}\qquad \zeta=\frac{\zeta\omega_n}{\omega_n}=\frac{0{,}3376}{0{,}6559}=0{,}5147", 14),
             fig("geometria", 7.5),
             P("Consequências: M<sub>p</sub> = e<super>−0,5147π/√(1−0,265)</super> ≈ 15%, t<sub>s</sub>(2%) ≈ 4/0,3376 ≈ 11,8 s."))
S += [Paragraph("2.2 Polos dominantes", h2),
      P("Quando um polo está muito mais à esquerda que os outros (regra prática: parte real 5 vezes maior), seu termo e<super>−at</super> some rápido "
        "e a resposta é dominada pelos polos mais próximos do eixo jω. No exemplo, p<sub>3</sub> = −2,3247 está ~7 vezes mais longe que −0,3376. "
        "Por isso dá para tratar o sistema de 3ª ordem como um 2ª ordem com ζ ≈ 0,51 e ω<sub>n</sub> ≈ 0,66."),
      ]
S += dica("Prova costuma pedir: \"ache ζ e ω<sub>n</sub>\" → desenhe o triângulo (Figura da geometria). Hipotenusa = ω<sub>n</sub>, cateto horizontal = ζω<sub>n</sub>, "
          "cateto vertical = ω<sub>d</sub>, cos θ = ζ. Uma <b>reta saindo da origem</b> é uma reta de ζ constante; um <b>círculo</b> é ω<sub>n</sub> constante; "
          "uma <b>reta vertical</b> é t<sub>s</sub> constante.")
S.append(CondPageBreak(25 * cm))

# ================= 3 tipo e erro =================
S += [Paragraph("3. Tipo do sistema e erro em regime permanente", h1),
      P("<b>Erro em regime permanente</b> e(∞) é quanto a saída fica longe da referência depois que o transitório acabou. "
        "Calcula-se pelo <b>teorema do valor final</b>, aplicado a E(s) = R(s)/(1 + FTMA):"),
      eq(r"e(\infty)=\lim_{t\to\infty}e(t)=\lim_{s\to 0}s\,E(s)=\lim_{s\to 0}\frac{s\,R(s)}{1+G(s)H(s)}"),
      P("<b>Só vale se a malha fechada for estável.</b> Se houver polo de malha fechada no semiplano direito, o erro não converge."),
      Paragraph("3.1 O que é o \"tipo\"", h2),
      P("Escreva a FTMA na forma de constantes de tempo. O <b>tipo</b> é o expoente N de s no denominador, ou seja, "
        "o <b>número de integradores (polos na origem) da FTMA</b>:"),
      eq(r"G(s)H(s)=\frac{K(T_as+1)(T_bs+1)\cdots}{s^N(T_1s+1)(T_2s+1)\cdots}\qquad N=\mathrm{tipo}"),
      P("Cada integrador \"acumula\" erro e o empurra para zero. Por isso, quanto maior o tipo, mais tipos de entrada o sistema segue sem erro."),
      Paragraph("3.2 Constantes de erro e tabela", h2),
      eq(r"K_p=\lim_{s\to0}GH\qquad K_v=\lim_{s\to0}s\,GH\qquad K_a=\lim_{s\to0}s^2\,GH"),
      ]
S += table([["Tipo", "Degrau  R(s)=1/s", "Rampa  R(s)=1/s²", "Parábola  R(s)=1/s³"],
            ["0", "1/(1+K<sub>p</sub>)", "∞", "∞"],
            ["1", "0", "1/K<sub>v</sub>", "∞"],
            ["2", "0", "0", "1/K<sub>a</sub>"]], [2.4, 4.6, 4.6, 4.8])
S += exemplo("Exemplo da aula: erro à rampa (quadro verde)",
             P("FTMA = 1/[s(s<super>2</super>+3s+2)]: há um s isolado no denominador, logo <b>tipo 1</b>. Ao degrau o erro é zero. À rampa unitária:"),
             eq(r"e(\infty)=\lim_{s\to0}s\cdot\frac{1}{1+\frac{1}{s(s^2+3s+2)}}\cdot\frac{1}{s^2}=\frac{1}{0+\frac{1}{2}}=2", 14),
             P("De outra forma: K<sub>v</sub> = lim s·1/[s(s<super>2</super>+3s+2)] = 1/2, então e(∞) = 1/K<sub>v</sub> = 2. "
               "A especificação pedia e(∞) = 0,2, ou seja, K<sub>v</sub> = 5, <b>10 vezes maior</b>. É isso que motiva o compensador de atraso da seção 6."))
S += dica("Roteiro do erro: (1) confira se a MF é estável; (2) conte os s na origem da FTMA (tipo); "
          "(3) identifique a entrada (degrau, rampa, parábola); (4) use a tabela. Só faça o limite completo se a questão pedir.",
          "Erro grande demais? Aumentar K reduz o erro, mas muda os polos (pode oscilar ou instabilizar). "
          "Para mexer no erro sem estragar o transitório, use <b>compensador de atraso</b>.")
S.append(CondPageBreak(25 * cm))

# ================= 4 LGR =================
S += [Paragraph("4. Lugar das raízes (LGR)", h1),
      P("O <b>lugar geométrico das raízes</b> é o desenho, no plano s, do caminho que os <b>polos de malha fechada</b> percorrem quando o ganho K varia de 0 a ∞. "
        "Ele responde: \"se eu aumentar o ganho, o sistema fica mais rápido? Começa a oscilar? Fica instável? Com qual K?\""),
      P("Os polos de MF são as raízes de 1 + KG(s)H(s) = 0, ou seja, KG(s)H(s) = −1. Um número complexo é −1 quando tem módulo 1 e ângulo 180°. Daí saem as duas condições:"),
      P("<b>Condição de ângulo:</b>"), eq(r"\angle G(s)H(s)=\sum\angle\mathrm{zeros}-\sum\angle\mathrm{polos}=\pm180^\circ(2k+1)"),
      P("<b>Condição de módulo:</b>"), eq(r"|K\,G(s)H(s)|=1\ \Rightarrow\ K=\frac{\prod\ \mathrm{dist.\ aos\ polos}}{\prod\ \mathrm{dist.\ aos\ zeros}}"),
      P("A <b>condição de ângulo</b> diz <i>se</i> um ponto pertence ao LGR. A <b>condição de módulo</b> diz <i>qual K</i> leva o polo até aquele ponto."),
      Paragraph("4.1 Regras de construção", h2)]
rules = [
    "<b>Início e fim:</b> o LGR começa (K=0) nos <b>polos</b> da FTMA e termina (K→∞) nos <b>zeros</b> da FTMA. Se há n polos e m zeros, n−m ramos vão para o infinito.",
    "<b>Número de ramos</b> = número de polos da FTMA (n). O LGR é <b>simétrico</b> em relação ao eixo real.",
    "<b>Eixo real:</b> um trecho do eixo real é LGR se tiver um número <b>ímpar</b> de polos + zeros (reais) à sua direita.",
    "<b>Assíntotas:</b> os n−m ramos que vão para o infinito seguem retas com ângulos θ = ±180°(2k+1)/(n−m), saindo do centroide σ<sub>a</sub> = (Σpolos − Σzeros)/(n−m).",
    "<b>Pontos de saída/chegada</b> no eixo real: escreva K = −1/G(s)H(s) e resolva dK/ds = 0. Fique só com as raízes que estão em trechos de LGR.",
    "<b>Cruzamento com o eixo jω</b> (limite de estabilidade): use Routh-Hurwitz na equação característica, ou substitua s = jω e iguale partes real e imaginária a zero.",
    "<b>Ângulo de partida</b> de um polo complexo: θ<sub>part</sub> = 180° + Σθ<sub>z</sub> − Σθ<sub>p</sub>, usando os ângulos dos <i>outros</i> polos e zeros até esse polo. "
    "<b>Ângulo de chegada</b> a um zero complexo: θ<sub>cheg</sub> = 180° + Σθ<sub>p</sub> − Σθ<sub>z</sub>. Exemplo no Exercício 7.11.",
    "<b>Achar K num ponto:</b> condição de módulo (seção 5)."]
for i, r in enumerate(rules, 1):
    S.append(Paragraph(r, ParagraphStyle("rl", parent=body, leftIndent=18, bulletIndent=2), bulletText=f"{i}."))
S += [fig("regra_eixo", 12, "Figura 5 – Regra do eixo real para polos em 0, −1 e −2.")]
S += [CondPageBreak(8 * cm), Paragraph("4.2 Exemplo completo: K/[s(s+1)(s+2)] (o sistema da aula)", h2)]
S += exemplo("Passo a passo",
             P("<b>1. Polos e zeros:</b> polos em 0, −1, −2 (n = 3); nenhum zero (m = 0). São 3 ramos, todos indo para o infinito."),
             P("<b>2. Eixo real:</b> entre 0 e −1 (1 polo à direita, ímpar) → SIM; entre −1 e −2 (2) → não; à esquerda de −2 (3) → SIM."),
             P("<b>3. Assíntotas:</b> n − m = 3, ângulos ±60° e 180°. Centroide σ<sub>a</sub> = (0 − 1 − 2)/3 = −1."),
             P("<b>4. Ponto de saída:</b> K = −(s<super>3</super>+3s<super>2</super>+2s) ⇒ dK/ds = −(3s<super>2</super>+6s+2) = 0 ⇒ s = −0,4226 ou s = −1,5774. "
               "Só −0,4226 está em trecho de LGR. Nele, K = 0,385. Para K maior que isso, os polos viram complexos (o sistema começa a oscilar)."),
             P("<b>5. Cruzamento com jω (Routh)</b> em s<super>3</super> + 3s<super>2</super> + 2s + K = 0:"),
             table([["Linha", "Coluna 1", "Coluna 2"], ["s³", "1", "2"], ["s²", "3", "K"], ["s¹", "(6 − K)/3", "0"], ["s⁰", "K", ""]], [3, 4, 4])[0],
             P("Estável para 0 < K < 6. Com K = 6, a linha s<super>2</super> dá 3s<super>2</super> + 6 = 0 ⇒ s = ±j√2 = ±j1,414. Esse é o ponto onde o LGR cruza o eixo jω."),
             P("<b>6. Conferindo com a aula:</b> com K = 1 os polos são −0,3376 ± j0,5623 e −2,3247 (pontos verdes na Figura " + str(FN["lgr_principal"]) + ")."))
S += [fig("lgr_principal", 13.5, "Figura 6 – LGR completo com todas as marcações (assíntotas, saída, cruzamento jω, K=1 e ζ=0,5)."),
      P("No MATLAB (como na aula): <font face='DejaVuSansMono'>P=1; Q=[1 3 2 0]; rlocus(P,Q)</font>. "
        "O vetor Q é o denominador da FTMA (repare no 0 final, que é o polo na origem; foi a correção \"Qma=[1 3 2 0]\" feita em aula)."),
      ]
S += dica("Ordem segura para desenhar o LGR na prova: polos/zeros → eixo real → assíntotas → saída/chegada → Routh (cruzamento jω) → ângulos de partida. "
          "Depois esboce ligando tudo. Confira a simetria e se o número de ramos bate com o número de polos.")
S.append(CondPageBreak(25 * cm))

# ================= 5 achar K =================
S += [Paragraph("5. Como achar o K", h1),
      P("\"Achar o K\" aparece de quatro jeitos diferentes. Identifique qual a questão quer:")]
S += table([["A questão pede...", "Como fazer"],
            ["K para um polo num ponto s<sub>d</sub> dado (ou para um ζ desejado)", "Condição de módulo: K = Π|s<sub>d</sub>−p<sub>i</sub>| / Π|s<sub>d</sub>−z<sub>j</sub>|"],
            ["K máximo para estabilidade", "Routh-Hurwitz: zerar a linha s¹ (ou achar onde muda de sinal)"],
            ["K para atender um erro em regime", "K<sub>p</sub>, K<sub>v</sub> ou K<sub>a</sub> desejado → isola K"],
            ["K no ponto de saída do eixo real", "K = −1/GH avaliado no ponto onde dK/ds = 0"]], [7.6, 8.8])
S += exemplo("Exemplo 5.1 – K para ζ = 0,5 no sistema K/[s(s+1)(s+2)]",
             P("<b>1.</b> Trace a reta ζ = 0,5: ângulo θ = arccos(0,5) = 60° com o eixo real negativo. Pontos: s = ω<sub>n</sub>(−0,5 + j0,866)."),
             P("<b>2.</b> Ache o ponto da reta que satisfaz a condição de ângulo: ∠s + ∠(s+1) + ∠(s+2) = 180°. "
               "Testando (ou resolvendo numericamente), ω<sub>n</sub> = 0,667: s<sub>d</sub> = −0,333 + j0,577. Confira: 120° + 40,9° + 19,1° = 180° ✓."),
             P("<b>3.</b> Condição de módulo (produto das distâncias aos polos):"),
             eq(r"K=|s_d|\cdot|s_d+1|\cdot|s_d+2|=0{,}667\times0{,}882\times1{,}764=1{,}037", 14),
             P("Com K = 1,037 os polos de MF ficam em −0,333 ± j0,577 e −2,333. Repare que K = 1 (aula) dá ζ = 0,515, bem perto disso."))
S += exemplo("Exemplo 5.2 – K máximo e K para erro",
             P("<b>Estabilidade:</b> pelo Routh da seção 4, K<sub>máx</sub> = 6 (oscila com ω = 1,414 rad/s)."),
             P("<b>Erro à rampa ≤ 0,2:</b> K<sub>v</sub> = K/2 ≥ 5 ⇒ K ≥ 10. Mas K = 10 > 6 deixa o sistema <b>instável</b>! "
               "Conclusão: só com ganho não dá para ter erro pequeno e estabilidade ao mesmo tempo. É preciso um <b>compensador</b>."))
S += dica("Distância no plano s: |s<sub>d</sub> − p| = √[(Re)<super>2</super> + (Im)<super>2</super>] da diferença. Ângulo: arctan(Im/Re), "
          "com cuidado no quadrante (se o ponto está à esquerda do polo, o ângulo passa de 90°). "
          "No MATLAB: <font face='DejaVuSansMono'>[K,polos]=rlocfind(P,Q)</font> e clique no ponto.")
S.append(CondPageBreak(25 * cm))

# ================= 6 compensadores =================
S += [Paragraph("6. Compensadores e controladores: avanço, atraso, PID e on-off", h1),
      P("Quando ajustar só o ganho K não atende transitório e erro ao mesmo tempo, coloca-se um <b>compensador</b> G<sub>c</sub>(s) em série. "
        "Os dois clássicos têm a mesma forma, com um zero e um polo. O que muda é <b>quem vem primeiro</b>:"),
      eq(r"G_c(s)=K_c\,\frac{s+z_c}{s+p_c}"),
      P("• <b>z<sub>c</sub> &lt; p<sub>c</sub></b> (zero mais perto da origem) → <b>AVANÇO</b>.   • <b>z<sub>c</sub> &gt; p<sub>c</sub></b> (polo mais perto da origem) → <b>ATRASO</b>."),
      Paragraph("6.1 Avanço de fase: o que é", h2),
      P("Um compensador de <b>avanço de fase</b> é aquele cuja saída senoidal fica <b>adiantada</b> em relação à entrada: a fase de G<sub>c</sub>(jω) é <b>positiva</b>. "
        "No LGR, isso significa que ele <b>soma ângulo positivo</b> nos pontos do plano s e \"puxa\" o LGR para a esquerda. "
        "Resultado: polos mais rápidos e mais amortecidos, com melhor <b>transitório</b> e mais estabilidade."),
      Paragraph("6.2 De onde vem isso na elétrica: o capacitor", h2),
      P("A ideia vem do <b>capacitor</b>. Nele, i = C·dv/dt. Se v = sen(ωt), então i = ωC·cos(ωt) = ωC·sen(ωt + 90°): "
        "<b>a corrente adianta 90° em relação à tensão</b>. Em fasores, Z<sub>C</sub> = 1/(jωC) = −j/(ωC). "
        "Qualquer circuito em que o capacitor \"passa\" o sinal de alta frequência adiantado tende a adiantar a fase. "
        "A derivada faz a mesma coisa: derivar um seno o adianta em 90°. Por isso avanço ≈ ação <b>derivativa</b> (PD) suavizada."),
      fig("capacitor", 14, "Figura 7 – No capacitor, a corrente adianta 90° em relação à tensão. É a origem física do \"avanço\"."),
      Paragraph("6.3 O componente: a rede RC de avanço", h2),
      P("O circuito passivo clássico é a <b>rede de avanço</b>: um resistor R<sub>1</sub> com um capacitor C<sub>1</sub> <b>em paralelo</b> no caminho série, e R<sub>2</sub> para o terra na saída."),
      fig("rede_avanco", 9.5, "Figura 8 – Rede de avanço passiva."),
      P("Com Z<sub>1</sub> = R<sub>1</sub> ∥ C<sub>1</sub> = R<sub>1</sub>/(1 + R<sub>1</sub>C<sub>1</sub>s) e o divisor de tensão E<sub>o</sub>/E<sub>i</sub> = R<sub>2</sub>/(R<sub>2</sub> + Z<sub>1</sub>):"),
      eq(r"\frac{E_o}{E_i}=\frac{s+\frac{1}{R_1C_1}}{s+\frac{R_1+R_2}{R_1R_2C_1}}=\alpha\,\frac{Ts+1}{\alpha Ts+1},\qquad T=R_1C_1,\ \ \alpha=\frac{R_2}{R_1+R_2}<1"),
      P("Zero em −1/T e polo em −1/(αT). Como α < 1, o <b>zero fica mais perto da origem</b> que o polo, e a fase é positiva. "
        "Em baixa frequência o capacitor é circuito aberto (divisor resistivo, ganho α). Em alta, ele curto-circuita R<sub>1</sub> (ganho 1). "
        "A rede passiva <b>atenua</b> por α, e por isso na prática ela vem seguida de um amplificador de ganho 1/α, ou é feita direto com <b>amplificador operacional</b> e redes RC. "
        "O avanço máximo e a frequência onde ele ocorre são:"),
      eq(r"\phi_{max}=\arcsin\frac{1-\alpha}{1+\alpha}\qquad \omega_m=\frac{1}{T\sqrt{\alpha}}"),
      fig("fase_avanco", 12, "Figura 9 – Quanto menor α (polo mais afastado do zero), maior o avanço máximo (limite prático ~60°)."),
      ]
S += exemplo("Exemplo 6.1 – Dimensionar a rede de avanço",
             P("Queremos zero em −2 e polo em −4 (α = 0,5). Escolha C<sub>1</sub> = 1 µF. Então R<sub>1</sub> = 1/(2·10<super>−6</super>) = <b>500 kΩ</b>. "
               "Do polo: (R<sub>1</sub>+R<sub>2</sub>)/(R<sub>1</sub>R<sub>2</sub>C<sub>1</sub>) = 4 ⇒ R<sub>2</sub> = <b>500 kΩ</b>. "
               "α = 0,5 ⇒ φ<sub>max</sub> = arcsen(0,5/1,5) = <b>19,5°</b> em ω<sub>m</sub> = 2/√0,5 = 2,83 rad/s. "
               "Note que a rede vale exatamente (s+2)/(s+4): em baixa frequência ela atenua para α = 0,5 (= 2/4). Para ter o G<sub>c</sub> = 4(s+2)/(s+4) do Exemplo 6.2, basta um amplificador de ganho 4 depois da rede."))
S += [CondPageBreak(9 * cm), Paragraph("6.4 Projeto de avanço pelo LGR (deficiência angular)", h2)]
for i, r in enumerate([
    "Transforme as especificações (M<sub>p</sub>, t<sub>s</sub>) em ζ e ω<sub>n</sub>, e daí no polo desejado s<sub>d</sub> = −ζω<sub>n</sub> + jω<sub>d</sub>.",
    "Calcule o ângulo da planta em s<sub>d</sub>: ∠G(s<sub>d</sub>). Se não der −180°, falta ângulo. Essa é a <b>deficiência angular</b> φ = −180° − ∠G(s<sub>d</sub>).",
    "Posicione o zero e o polo do compensador para que ∠zero − ∠polo = φ. Opções: cancelar um polo da planta com o zero, ou o método da bissetriz.",
    "Ache K<sub>c</sub> pela condição de módulo em s<sub>d</sub>.",
    "Confira: polos dominantes de fato dominantes? Erro em regime aceitável? Simule o degrau."], 1):
    S.append(Paragraph(r, ParagraphStyle("rl2", parent=body, leftIndent=18), bulletText=f"{i}."))
S += exemplo("Exemplo 6.2 – Projeto de avanço",
             P("Planta G(s) = 4/[s(s+2)]. Sem compensador: MF = 4/(s<super>2</super>+2s+4), ζ = 0,5, ω<sub>n</sub> = 2 (t<sub>s</sub> ≈ 4 s). "
               "<b>Quero o dobro da velocidade:</b> ζ = 0,5 e ω<sub>n</sub> = 4 ⇒ s<sub>d</sub> = −2 ± j3,464."),
             P("<b>Ângulo da planta em s<sub>d</sub>:</b> ∠s<sub>d</sub> = 120°, ∠(s<sub>d</sub>+2) = 90° ⇒ ∠G = −210°. Deficiência: φ = −180° − (−210°) = <b>+30°</b> (precisa de AVANÇO)."),
             P("<b>Zero e polo:</b> ponha o zero em −2 (cancela o polo da planta). Ele contribui +90°. O polo deve contribuir 90° − 30° = 60°: "
               "p = −2 − 3,464/tan 60° = <b>−4</b>."),
             P("<b>Ganho:</b> FTMA = 4K<sub>c</sub>/[s(s+4)]. Em s<sub>d</sub>: 4K<sub>c</sub> = |s<sub>d</sub>|·|s<sub>d</sub>+4| = 4·4 = 16 ⇒ <b>K<sub>c</sub> = 4</b>."),
             eq(r"G_c(s)=4\,\frac{s+2}{s+4}\qquad \mathrm{FTMF}=\frac{16}{s^2+4s+16}\ (\zeta=0{,}5,\ \omega_n=4)", 14),
             P("Bônus: K<sub>v</sub> passou de 2 para 4, então o erro à rampa caiu de 0,5 para 0,25."),
             fig("avanco_exemplo", 15))
S += [CondPageBreak(7 * cm), Paragraph("6.5 Atraso de fase", h2),
      P("O compensador de <b>atraso</b> tem o <b>polo mais perto da origem</b> que o zero, então a fase é negativa. O objetivo dele <b>não</b> é mexer no transitório: "
        "é <b>aumentar o ganho de baixa frequência</b> (K<sub>p</sub>, K<sub>v</sub>) e com isso <b>reduzir o erro em regime</b>. "
        "O truque é colocar polo e zero <b>bem pertinho da origem e um do outro</b>. Vistos de longe (do polo dominante), eles quase se cancelam: "
        "contribuem com poucos graus (< 5°) e módulo ≈ 1, e o LGR quase não muda. Em s → 0, porém, a razão z<sub>c</sub>/p<sub>c</sub> multiplica o ganho."),
      fig("rede_atraso", 9.5, "Figura 10 – Rede de atraso passiva (o capacitor vai no ramo para o terra)."),
      eq(r"\frac{E_o}{E_i}=\frac{R_2Cs+1}{(R_1+R_2)Cs+1}=\frac{1}{\beta}\,\frac{s+\frac{1}{T}}{s+\frac{1}{\beta T}},\qquad T=R_2C,\ \ \beta=\frac{R_1+R_2}{R_2}>1"),
      ]
S += exemplo("Exemplo 6.3 – O compensador de atraso da aula, passo a passo",
             P("<b>Planta:</b> 1/[s(s+1)(s+2)] com K = 1: ζ = 0,5147 (bom transitório), mas e(∞) à rampa = 2. <b>Meta:</b> e(∞) = 0,2 sem estragar o transitório."),
             P("<b>1. Ganho necessário:</b> com G<sub>c</sub> = K<sub>c</sub>(s+z<sub>c</sub>)/(s+p<sub>c</sub>):"),
             eq(r"e(\infty)=\frac{1}{K_c\frac{z_c}{p_c}\cdot\frac{1}{2}}=0{,}2=\frac{1}{5}\ \Rightarrow\ K_c\frac{z_c}{p_c}=10", 14),
             P("<b>2. Escolha polo e zero perto da origem:</b> com K<sub>c</sub> ≈ 1 ⇒ z<sub>c</sub> = 10p<sub>c</sub>. Adotando p<sub>c</sub> = 0,005 ⇒ z<sub>c</sub> = 0,05 (ambos ~7 vezes mais perto da origem que o polo dominante −0,3376)."),
             P("<b>3. Verifique o efeito no polo dominante:</b> em s<sub>d</sub> = −0,3376 + j0,5623, o compensador contribui só −3,5° e módulo 0,97. Ótimo, quase nada."),
             P("<b>4. Reajuste K<sub>c</sub> para manter ζ:</b> a nova FTMA é K<sub>c</sub>(s+0,05)/[(s+0,005)·s(s<super>2</super>+3s+2)], "
               "com denominador s<super>4</super> + 3,005s<super>3</super> + 2,015s<super>2</super> + 0,01s. Pela condição de módulo no novo LGR, "
               "<b>K<sub>c</sub> = 0,975</b> mantém ζ ≈ 0,515, com polos dominantes em <b>−0,317 ± j0,53</b> (exatamente o que está no quadro)."),
             P("<b>5. Resultado:</b> K<sub>v</sub> = 0,975·10/2 = 4,875 ⇒ e(∞) = 0,205 ≈ 0,2 ✓. O transitório fica quase igual (Figura " + str(FN["atraso_exemplo"]) + "). "
               "O preço: surge um polo de MF lento em −0,055, perto do zero −0,05, que deixa uma \"cauda\" lenta pequena na resposta."),
             fig("atraso_exemplo", 15, "Figura 11 – Com o atraso o degrau quase não muda, mas o erro à rampa cai de 2 para ~0,2."))
S += [Paragraph("6.6 Avanço × atraso × PID", h2)]
S += table([["", "Avanço", "Atraso"],
            ["Posição", "zero mais perto da origem que o polo", "polo mais perto da origem que o zero"],
            ["Fase", "positiva (adianta)", "negativa (atrasa)"],
            ["Para que serve", "melhorar transitório e estabilidade (puxa o LGR para a esquerda)", "reduzir erro em regime sem mudar o transitório"],
            ["Parente PID", "PD (derivativo)", "PI (integral)"],
            ["Rede RC", "C em paralelo com R série", "R+C em série no ramo para o terra"],
            ["Efeito colateral", "aumenta banda, amplifica ruído", "resposta com cauda lenta"]], [3.4, 6.5, 6.5])
S += [fig("pid", 14, "Figura 12 – Controlador PID (slide da aula)."),
      eq(r"G_{PID}(s)=K_p+\frac{K_i}{s}+K_ds=\frac{K_ds^2+K_ps+K_i}{s}"),
      P("<b>P</b> reage ao erro atual. <b>I</b> acumula o erro passado e adiciona um polo na origem (sobe o <b>tipo</b> em 1, zerando o erro ao degrau). "
        "<b>D</b> reage à tendência e adiciona fase positiva (avanço). Ou seja, o PID é a versão \"ideal\" de avanço + atraso juntos.")]
S += dica("Avanço = \"vai mais rápido\" (transitório). Atraso = \"erra menos\" (regime). Se pedirem os dois, faça <b>avanço-atraso</b>: "
          "projete primeiro o avanço para o transitório e depois o atraso para o erro.")
S.append(CondPageBreak(25 * cm))

# ================= 7 exercícios resolvidos =================
S += [CondPageBreak(12 * cm), Paragraph("6.7 PID: o que é, com exemplos de P, I e D", h2),
      P("O PID é o controlador mais usado na indústria (de longe). Ele calcula o sinal de controle somando três reações ao erro e(t) = r(t) − y(t): "
        "uma ao <b>presente</b> (P), uma ao <b>passado</b> (I) e uma à <b>tendência futura</b> (D)."),
      eq(r"u(t)=K_p\,e(t)+K_i\int_0^t e\,d\tau+K_d\,\frac{de}{dt}\qquad C(s)=K_p+\frac{K_i}{s}+K_ds"),
      Paragraph("Exemplo do dia a dia: ajustar a temperatura do chuveiro", h3)]
S += B(["<b>P:</b> a água está muito fria, então você gira muito o registro; está quase boa, gira pouco. Reage ao tamanho do erro <i>agora</i>. "
        "Problema: se a caixa d'água esfria, você para perto do alvo sem chegar lá, porque o giro é proporcional a um erro que ficou pequeno. Esse é o <b>erro em regime</b> do P.",
        "<b>I:</b> você percebe que já faz um tempo que está \"um pouco frio\" e vai girando mais, aos poucos, até acertar. Ele acumula o erro e só para quando o erro zera. "
        "Problema: se exagerar, você passa do ponto e fica oscilando entre quente e frio.",
        "<b>D:</b> você sente a água esquentando <i>rápido</i> e alivia o registro <i>antes</i> de queimar. Reage à velocidade do erro: é um freio que reduz o sobressinal. "
        "Problema: se a temperatura \"tremer\" (ruído), o D reage a cada tremida."])
S += [Paragraph("Exemplo de engenharia: piloto automático de carro numa subida", h3),
      P("<b>P:</b> na subida a velocidade cai, o erro aparece e o P acelera, mas estabiliza um pouco abaixo da velocidade pedida (precisa de erro para manter acelerador extra). "
        "<b>I:</b> o erro acumulado vai aumentando o acelerador até a velocidade bater exatamente. <b>D:</b> quando a velocidade começa a voltar rápido, segura o acelerador para não passar do alvo."),
      Paragraph("Simulação: planta 1/[(s+1)(s+2)] com degrau unitário", h3),
      fig("pid_comp", 16.5, "Figura 0 – Em cima, a saída; embaixo, as parcelas P (verde), I (laranja) e D (vermelho) do sinal de controle."),
      ]
S += table([["Controlador", "Sobressinal", "t<sub>s</sub> (2%)", "Erro final", "Leitura"],
            ["Só P (K<sub>p</sub> = 8)", "18,5%", "2,6 s", "0,20", "rápido, mas para em 0,8 (erro = 1/(1 + 8/2))"],
            ["PI (K<sub>i</sub> = 6)", "22,6%", "3,0 s", "0", "a parcela I cresce até zerar o erro, com um pouco mais de oscilação"],
            ["PD (K<sub>d</sub> = 1,5)", "3,5%", "1,8 s", "0,20", "o D freia: quase sem sobressinal, mas o erro do P continua"],
            ["PID (10; 8; 1,5)", "16,2%", "2,4 s", "0", "junta os dois: erro zero e transitório controlado"]], [3.4, 2.4, 2.0, 2.0, 6.6])
S += dica("Resumo para a prova: <b>P</b> acelera e reduz o erro (sem zerar); <b>I</b> zera o erro em regime (sobe o tipo em 1) e tende a oscilar; "
          "<b>D</b> reduz o sobressinal e melhora a estabilidade (avanço de fase). PI ≈ atraso, PD ≈ avanço, PID ≈ avanço-atraso.")
S += [CondPageBreak(10 * cm), Paragraph("6.8 Ações P, I e D em detalhe", h2),
      P("Erro e(t) = r(t) − y(t): o que você quer menos o que o sistema entrega. Cada ação usa o erro de um jeito:")]
S += table([["Ação", "No tempo", "C(s)", "O que faz", "Efeito colateral"],
            ["P", "u = K<sub>p</sub>·e", "K<sub>p</sub>", "reage ao erro <b>atual</b>; aumentar K<sub>p</sub> acelera", "não zera o erro em regime; K alto oscila"],
            ["I", "u = K<sub>i</sub>∫e dt", "K<sub>i</sub>/s", "olha o <b>passado</b>: acumula o erro até zerá-lo", "deixa mais lento/oscilatório"],
            ["D", "u = K<sub>d</sub>·de/dt", "K<sub>d</sub>·s", "prevê o <b>futuro</b> pela velocidade do erro: é um freio", "amplifica ruído"]], [1.2, 3.2, 1.8, 5.6, 4.6])
S += [eq(r"PI:\ K_p\left(1+\frac{1}{T_is}\right)\qquad PD:\ K_p(1+T_ds)\qquad PID:\ K_p\left(1+\frac{1}{T_is}+T_ds\right)=K_p+\frac{K_i}{s}+K_ds"),
      P("T<sub>i</sub> é o <b>tempo integrativo</b> (K<sub>i</sub> = K<sub>p</sub>/T<sub>i</sub>) e T<sub>d</sub> o <b>tempo derivativo</b> (K<sub>d</sub> = K<sub>p</sub>T<sub>d</sub>). "
        "Com controlador C(s): FTMF = CG/(1 + CG), equação característica 1 + C(s)G(s) = 0 e erro e<sub>ss</sub> = lim<sub>s→0</sub> sR(s)/(1 + CG). "
        "Por que o P sozinho deixa erro: ele <b>precisa</b> de erro para gerar ação (u = K<sub>p</sub>e). Se o erro zerasse, o sinal de controle sumiria. O I resolve isso, porque o acumulado continua lá mesmo com e = 0.")]
S += exemplo("Exemplo das suas notas – faixa de K<sub>p</sub> e K<sub>i</sub> de um PI por Routh",
             P("G(s) = 1/[(s+1)(s+2)] e C(s) = K<sub>p</sub> + K<sub>i</sub>/s. A equação 1 + CG = 0 vira s(s<super>2</super>+3s+2) + K<sub>p</sub>s + K<sub>i</sub> = 0:"),
             eq(r"s^3+3s^2+(2+K_p)s+K_i=0", 14),
             table([["s³", "1", "2 + K<sub>p</sub>"], ["s²", "3", "K<sub>i</sub>"], ["s¹", "b<sub>1</sub> = [3(2+K<sub>p</sub>) − K<sub>i</sub>]/3", "0"], ["s⁰", "K<sub>i</sub>", ""]], [2, 7, 4], head=False)[0],
             P("Estável se K<sub>i</sub> > 0 e b<sub>1</sub> > 0 ⇒ <b>0 &lt; K<sub>i</sub> &lt; 6 + 3K<sub>p</sub></b>. "
               "(Nas suas anotações aparece K<sub>i</sub> &lt; K<sub>p</sub> + 6. Repare que o 3 multiplica o (2 + K<sub>p</sub>) inteiro.)"))
S += [Paragraph("Receita do PID pelo LGR (como nas suas listas)", h3)]
for i, r in enumerate([
    "Especificações → ζ (pelo overshoot) e σ = ζω<sub>n</sub> (pelo t<sub>s</sub>) ou ω<sub>d</sub> (pelo t<sub>p</sub>) → polo desejado s<sub>d</sub>.",
    "<b>Parte PD (avanço):</b> calcule ∠G(s<sub>d</sub>), ache a deficiência angular e coloque o zero z<sub>PD</sub> que fornece esse ângulo.",
    "<b>Parte PI (atraso):</b> zero z<sub>PI</sub> bem perto da origem (ex.: −0,1) ou escolhido para mexer pouco no polo (ex.: deslocamento de −2°, compensado no PD).",
    "K pela condição de módulo em s<sub>d</sub>. Expanda K(s+z<sub>PD</sub>)(s+z<sub>PI</sub>)/s para ler K<sub>p</sub>, K<sub>i</sub> e K<sub>d</sub>.",
    "Confira os polos de MF. O zero do PI cria um polo lento perto dele, o que deixa uma \"cauda\" na resposta."], 1):
    S.append(Paragraph(r, ParagraphStyle("rpid", parent=body, leftIndent=18), bulletText=f"{i}."))

S += [CondPageBreak(10 * cm), Paragraph("6.9 Controlador on-off (liga-desliga)", h2),
      P("É o controlador mais simples que existe. O atuador só tem <b>duas posições</b>, totalmente ligado ou totalmente desligado, e quem decide é o <b>sinal do erro</b>:"),
      eq(r"u(t)=U_{max}\ (\mathrm{ON})\ \ \mathrm{se}\ e(t)>0;\qquad u(t)=U_{min}\ (\mathrm{OFF})\ \ \mathrm{se}\ e(t)<0"),
      P("Na prática é um <b>relé</b> (ou contator, ou termostato bimetálico). Exemplos: geladeira, ferro de passar, aquecedor de aquário, boia de caixa d'água, "
        "ar-condicionado comum (não inverter). É exatamente o controlador de temperatura das suas notas: o microcontrolador vê erro positivo (está frio) e o relé liga a resistência. "
        "Quando a temperatura passa da referência, desliga."),
      Paragraph("Histerese (zona morta)", h3),
      P("Se ligasse e desligasse exatamente em e = 0, qualquer ruído no sensor faria o relé \"bater\" centenas de vezes por segundo (<i>chattering</i>), o que queima contatos. "
        "Por isso usa-se uma <b>banda de histerese</b> ±h: <b>liga quando e &gt; +h</b> e <b>desliga quando e &lt; −h</b>. Dentro da banda, mantém o estado anterior."),
      fig("onoff", 15.5, "Figura 0 – Esquerda: característica do relé com histerese. Direita: aquecedor on-off com referência de 25 °C e h = 0,5 °C."),
      P("<b>Comportamento típico:</b> a saída <b>nunca fica parada</b>. Ela oscila para sempre em torno da referência (ciclo-limite). "
        "A amplitude é maior que a banda, porque a planta tem inércia e atraso: depois que o relé desliga, a temperatura ainda sobe um pouco."),
      ]
S += exemplo("Exemplo numérico (a simulação da figura)",
             P("Forno: 8·dT/dt = −(T − 18) + 14·u, com u = 0 ou 1 (minutos e °C). Ligado, tenderia a 18 + 14 = 32 °C; desligado, volta a 18 °C. "
               "Referência 25 °C, h = 0,5 °C e um atraso de 0,8 min entre o relé e o ar."),
             P("Perto de 25 °C, ele esquenta a (32 − 25)/8 ≈ 0,875 °C/min e esfria a (25 − 18)/8 ≈ 0,875 °C/min. "
               "Além da banda de 1 °C, o atraso de 0,8 min deixa passar mais ~0,7 °C de cada lado. Resultado: <b>oscila entre ~23,9 e ~26,1 °C, com período de ~5,2 min</b> (confirmado na simulação)."),
             P("Aumentar h ⇒ menos chaveamentos (relé dura mais), porém oscilação maior. Diminuir h ⇒ temperatura mais precisa, porém o relé chaveia mais vezes."))
S += table([["", "On-off", "P / PI / PID"],
            ["Sinal de controle", "só 2 valores (ON/OFF)", "contínuo (qualquer valor)"],
            ["Saída em regime", "oscila em torno da referência", "converge (PI/PID: erro zero ao degrau)"],
            ["Atuador", "relé, contator (barato)", "precisa modular: PWM, inversor, válvula proporcional"],
            ["Análise", "não linear: <b>não</b> se usa FT nem LGR (simulação, função descritiva)", "linear: FT, LGR, Routh, erro em regime"],
            ["Quando usar", "processos lentos e tolerantes (temperatura, nível)", "precisão, rapidez, posição, velocidade"]], [3.4, 6.5, 6.5])
S += dica("Questão sobre on-off: fale em <b>duas posições</b>, <b>histerese</b>, <b>oscilação permanente</b> (ciclo-limite) e no <b>compromisso</b> banda × número de chaveamentos. "
          "Não tente calcular erro em regime com K<sub>p</sub>: o on-off não é linear.")
S.append(CondPageBreak(25 * cm))

S += [Paragraph("7. Exercícios resolvidos", h1)]
def ex(n, enun, *sol):
    return [Paragraph(f"Exercício {n}", h3), P(f"<b>Enunciado:</b> {enun}")] + box("Resolução", list(sol), "#f6f6f6", "#555")
S += ex("7.1 – Função de transferência e polos",
        "Um sistema é descrito por y'' + 4y' + 3y = 2u. Ache a FT, os polos, diga se é estável e qual o valor final ao degrau unitário.",
        P("Laplace com CI nulas: (s<super>2</super>+4s+3)Y = 2U ⇒ G(s) = 2/(s<super>2</super>+4s+3) = 2/[(s+1)(s+3)]."),
        P("Polos: −1 e −3, ambos reais negativos ⇒ <b>estável e sem oscilação</b> (superamortecido: ω<sub>n</sub> = √3 = 1,732; 2ζω<sub>n</sub> = 4 ⇒ ζ = 1,155 > 1)."),
        P("Valor final ao degrau: y(∞) = lim s·G(s)·(1/s) = G(0) = 2/3. O polo em −1 domina: t<sub>s</sub> ≈ 4 s."))
S += ex("7.2 – Tipo e erros",
        "Para realimentação unitária com G(s) = 10(s+2)/[s(s+5)], classifique o tipo e calcule o erro ao degrau, à rampa e à parábola.",
        P("Um s na origem ⇒ <b>tipo 1</b>. (A MF é estável: s<super>2</super> + 15s + 20 = 0 tem raízes negativas.)"),
        P("K<sub>p</sub> = ∞ ⇒ e<sub>degrau</sub> = 0. K<sub>v</sub> = lim s·G = 10·2/5 = 4 ⇒ e<sub>rampa</sub> = 1/4 = 0,25. K<sub>a</sub> = 0 ⇒ e<sub>parábola</sub> = ∞."))
S += ex("7.3 – K máximo por Routh",
        "Para G(s) = K/[(s+1)(s+2)(s+3)] com realimentação unitária, ache a faixa de K para estabilidade e a frequência de oscilação no limite.",
        P("Eq. característica: s<super>3</super> + 6s<super>2</super> + 11s + 6 + K = 0."),
        table([["", "", ""], ["s³", "1", "11"], ["s²", "6", "6 + K"], ["s¹", "(66 − 6 − K)/6 = (60 − K)/6", "0"], ["s⁰", "6 + K", ""]], [2, 6, 3], head=False)[0],
        P("Estável se 60 − K > 0 e 6 + K > 0 ⇒ <b>−6 < K < 60</b> (para K > 0: K < 60). No limite, 6s<super>2</super> + 66 = 0 ⇒ s = ±j√11 = <b>±j3,317 rad/s</b>."))
S += ex("7.4 – K para um ζ desejado",
        "Para G(s) = K/[s(s+4)], ache K para ζ = 0,707 e o tempo de acomodação resultante.",
        P("LGR: polos em 0 e −4. Saída do eixo em −2, e depois uma reta vertical em σ = −2. A reta ζ = 0,707 (45°) cruza a vertical em s<sub>d</sub> = −2 + j2."),
        P("Módulo: K = |s<sub>d</sub>|·|s<sub>d</sub>+4| = √8·√8 = <b>8</b>. Conferindo: s<super>2</super> + 4s + 8 = 0 ⇒ s = −2 ± j2 ✓. t<sub>s</sub>(2%) = 4/2 = <b>2 s</b>; M<sub>p</sub> ≈ 4,3%."))
S += ex("7.5 – Erro ao degrau em sistema tipo 0",
        "G(s) = K/[(s+1)(s+3)]. Qual K dá erro ao degrau de 0,2? A MF fica estável?",
        P("Tipo 0: K<sub>p</sub> = G(0) = K/3. e = 1/(1 + K/3) = 0,2 ⇒ 1 + K/3 = 5 ⇒ <b>K = 12</b>."),
        P("MF: s<super>2</super> + 4s + 3 + 12 = s<super>2</super> + 4s + 15 = 0 ⇒ s = −2 ± j3,317 ⇒ estável, ω<sub>n</sub> = 3,87, ζ = 0,516."))
S += ex("7.6 – LGR com zero",
        "Esboce o LGR de G(s) = K(s+3)/[s(s+1)] e ache os pontos de saída e de chegada no eixo real.",
        P("Polos 0 e −1, zero −3. Eixo real: [−1, 0] e (−∞, −3]. n − m = 1 ⇒ uma assíntota a 180°."),
        P("K = −s(s+1)/(s+3); dK/ds = 0 ⇒ s<super>2</super> + 6s + 3 = 0 ⇒ s = −0,551 (saída, K = 0,101) e s = −5,449 (chegada, K = 9,90)."),
        P("Entre esses pontos o LGR é um <b>círculo</b> centrado no zero (−3) com raio √6 = 2,449. Esse é um resultado clássico para 2 polos + 1 zero reais. "
          "O sistema é estável para todo K > 0."))
S.append(CondPageBreak(25 * cm))

S += [CondPageBreak(10 * cm), Paragraph("Exercícios das suas listas (conferidos)", h2),
      P("Os enunciados abaixo vêm das suas anotações. As contas foram refeitas numericamente. Onde algo diverge do caderno, está indicado.")]
S += ex("7.7 – Routh de 4ª ordem (instável)",
        "G(s) = 2/[s(s+3)] · 10/(s+1)², com realimentação unitária. O sistema em malha fechada é estável?",
        P("FTMA = 20/[s(s+3)(s+1)²]. Equação característica: s(s+3)(s<super>2</super>+2s+1) + 20 = <b>s<super>4</super> + 5s<super>3</super> + 7s<super>2</super> + 3s + 20 = 0</b>."),
        table([["s⁴", "1", "7", "20"], ["s³", "5", "3", "0"], ["s²", "(5·7 − 1·3)/5 = 6,4", "20", ""], ["s¹", "(6,4·3 − 5·20)/6,4 = −12,625", "0", ""], ["s⁰", "20", "", ""]], [2, 7, 2.5, 2.5], head=False)[0],
        P("Primeira coluna: +1, +5, +6,4, <b>−12,625</b>, +20. Há <b>2 trocas de sinal</b>, ou seja, 2 polos no semiplano direito: <b>instável</b>."))
S += ex("7.8 – Faixa de K",
        "G(s) = K/(s<super>3</super> + 4s<super>2</super> + 12s − 3). Para quais K a malha fechada é estável?",
        P("Equação característica: s<super>3</super> + 4s<super>2</super> + 12s + (K − 3) = 0. A planta sozinha é instável (o termo −3 indica um polo positivo); a realimentação é que estabiliza."),
        table([["s³", "1", "12"], ["s²", "4", "K − 3"], ["s¹", "(48 − (K − 3))/4 = (51 − K)/4", "0"], ["s⁰", "K − 3", ""]], [2, 7, 3], head=False)[0],
        P("Precisa de K − 3 > 0 e 51 − K > 0 ⇒ <b>3 &lt; K &lt; 51</b>. Em K = 51: 4s<super>2</super> + 48 = 0 ⇒ oscila em ω = √12 = 3,46 rad/s."))
S += ex("7.9 – LGR passo a passo de K(s+1)/(s⁴+9s³+26s²+24s)",
        "Construa o LGR, ache onde toca o eixo imaginário e em que condição o sistema é criticamente estável.",
        P("<b>Fatorar:</b> s(s+2)(s+3)(s+4). Polos 0, −2, −3, −4 (n = 4); zero −1 (m = 1). São 3 ramos que vão para o infinito."),
        P("<b>Eixo real:</b> [−1, 0], [−3, −2] e (−∞, −4]. <b>Assíntotas:</b> ±60° e 180°; σ<sub>a</sub> = [(0−2−3−4) − (−1)]/3 = −8/3 = <b>−2,67</b> ✓ (igual ao caderno)."),
        P("<b>Ponto de saída</b> (dK/ds = 0) entre −2 e −3: <b>s = −2,39, com K = 0,659</b>. Por isso, com K = 0,659 os polos dão −0,027, −2,39 (duplo) e −4,19, exatamente as suas anotações."),
        P("<b>Eixo imaginário</b> (Routh em s<super>4</super> + 9s<super>3</super> + 26s<super>2</super> + (24+K)s + K): zerar a linha s¹ dá K<super>2</super> − 105K − 5040 = 0 ⇒ "
          "<b>K = 140,8</b>, com ω<super>2</super> = 9K/(210 − K) ⇒ <b>ω = 4,28 rad/s</b>. Criticamente (marginalmente) estável em K = 140,8; estável para 0 &lt; K &lt; 140,8."),
        fig("lgr_A", 10.5),
        P("<b>\"Para estabilizar mais rápido sem alterar o overshoot, onde pôr o zero?\"</b> Overshoot fixo = mesmo ζ = mesma reta saindo da origem. "
          "Estabilizar mais rápido = polo mais à esquerda <i>nessa mesma reta</i> (σ maior). Escolha o novo s<sub>d</sub> nessa reta e posicione o zero (PD/avanço) "
          "para cumprir a condição de ângulo em s<sub>d</sub>. O LGR passa a cruzar a reta mais longe da origem."))
S += ex("7.10 – Zeros no semiplano direito: KG = K(s−2)²/[(s−1)(s²+2s+2)]",
        "Ache polos e zeros e verifique se algum K > 0 estabiliza.",
        P("Zeros: (s−2)<super>2</super> = 0 ⇒ s = 2 (duplo). Polos: s = 1 e s<super>2</super>+2s+2 = 0 ⇒ Δ = 4 − 8 = −4 ⇒ s = −1 ± j. São 3 polos e 2 zeros ✓."),
        P("Equação característica: (s−1)(s<super>2</super>+2s+2) + K(s−2)<super>2</super> = <b>s<super>3</super> + (1+K)s<super>2</super> − 4Ks + (4K − 2) = 0</b>. "
          "O coeficiente de s é <b>−4K &lt; 0</b> para todo K > 0. Pela condição necessária de Routh (todos os coeficientes com o mesmo sinal), "
          "<b>nenhum K > 0 estabiliza</b>. O zero duplo em +2 prende sempre um polo no semiplano direito."),
        fig("lgr_B", 11))
S += ex("7.11 – Ângulo de partida: K/[(s²+s)(s²+4s+13)]",
        "Ache assíntotas, ponto de saída, cruzamento do eixo jω e ângulo de partida dos polos complexos.",
        P("Polos: 0, −1 e s<super>2</super>+4s+13 = 0 ⇒ Δ = 16 − 52 = −36 ⇒ <b>−2 ± j3</b>. Sem zeros: 4 assíntotas a ±45° e ±135°; σ<sub>a</sub> = (0 − 1 − 2 − 2)/4 = <b>−1,25</b> ✓."),
        P("Equação característica: <b>s<super>4</super> + 5s<super>3</super> + 17s<super>2</super> + 13s + K = 0</b>. Saída do eixo real: 4s<super>3</super> + 15s<super>2</super> + 34s + 13 = 0 ⇒ s = −0,466 (K = 2,83)."),
        table([["s⁴", "1", "17", "K"], ["s³", "5", "13", "0"], ["s²", "(85 − 13)/5 = 14,4", "K", ""], ["s¹", "(187,2 − 5K)/14,4", "0", ""], ["s⁰", "K", "", ""]], [2, 6, 2.5, 2.5], head=False)[0],
        P("Estável se 0 &lt; K &lt; 187,2/5 = <b>37,44</b> ✓ (igual ao caderno). Na linha s²: 14,4s<super>2</super> + 37,44 = 0 ⇒ cruza em <b>±j1,61</b>."),
        P("<b>Partida de −2 + j3:</b> ângulos dos outros polos até ele: de 0 → 123,7°; de −1 → 108,4°; de −2 − j3 → 90°. "
          "θ<sub>part</sub> = 180° − (123,7 + 108,4 + 90) = <b>−142,1°</b>."),
        fig("lgr_C", 10.5))
S += ex("7.12 – Controlador proporcional: 1/[s(s+20)] com POS = 31,5% e t<sub>s</sub> = 0,4 s",
        "Projete um controlador P que atenda às duas especificações.",
        eq(r"\zeta=\frac{-\ln(0{,}315)}{\sqrt{\pi^2+\ln^2(0{,}315)}}=0{,}345\qquad t_s=\frac{4}{\zeta\omega_n}=0{,}4\Rightarrow\zeta\omega_n=10", 13),
        P("ω<sub>n</sub> = 10/0,345 = 28,99 rad/s e ω<sub>d</sub> = 28,99·√(1 − 0,345<super>2</super>) = 27,2 ⇒ <b>s<sub>d</sub> = −10 ± j27,2</b>."),
        P("O LGR de K/[s(s+20)] sai do eixo em dK/ds = −(2s + 20) = 0 ⇒ s = −10 e sobe na vertical σ = −10 (assíntotas ±90°, σ<sub>a</sub> = −10). "
          "O ponto desejado <b>está no LGR</b>, então só o ganho resolve (\"o proporcional só desloca os polos sobre o LGR\"). Ângulos: 110,18° + 69,82° = 180° ✓."),
        P("Módulo: K = |s<sub>d</sub>|·|s<sub>d</sub> + 20| = 28,99 · 28,99 = <b>K ≈ 840</b> ✓."),
        fig("lgr_D", 9))
S += ex("7.13 – P e depois PID para 1/[(s+1)(s+3)(s+5)]",
        "(a) Controlador P com ζ = 0,2. (b) PID (avanço-atraso) para ficar 3,5× mais rápido, com overshoot 2× menor, erro nulo e deslocamento de −2° no polo dominante.",
        P("<b>(a)</b> Na reta ζ = 0,2, a condição de ângulo dá s<sub>d</sub> = −0,702 + j3,44 (85,1° + 56,3° + 38,7° = 180,1° ✓). "
          "K = 3,45·4,14·5,51 = <b>78,7</b> ✓. Então t<sub>s</sub> = 4/0,702 = 5,70 s, OS = 52,6%, e o erro ao degrau é 1/(1 + 78,7/15) = 16% (tipo 0)."),
        P("<b>(b)</b> t<sub>s</sub>' = 5,698/3,5 = 1,628 s ⇒ σ' = 4/1,628 = 2,457. OS' = 26,3% ⇒ ζ' = 0,391 ⇒ ω<sub>d</sub>' = 5,78 ⇒ <b>s<sub>d</sub>' = −2,457 + j5,78</b> ✓."),
        P("Ângulo da planta em s<sub>d</sub>': −255,0° ⇒ faltam <b>75,0°</b>. Como o PI vai \"roubar\" 2°, o PD precisa dar 77,0°: tan 77,0° = 5,78/(z − 2,457) ⇒ <b>z<sub>PD</sub> = 3,79</b>."),
        P("PI: o zero z<sub>PI</sub> e o polo na origem devem somar −2° em s<sub>d</sub>' ⇒ <b>z<sub>PI</sub> = 0,235</b>. Módulo ⇒ <b>K = 37,4</b>:"),
        eq(r"C(s)=37{,}4\,\frac{(s+3{,}79)(s+0{,}235)}{s}\ \Rightarrow\ K_d=37{,}4,\ K_p=150,\ K_i=33{,}2", 13),
        P("Polos de MF: −2,457 ± j5,78 ✓, −3,87 e −0,218. Este último fica colado no zero −0,235 e deixa uma cauda lenta: a saída chega a ~98,7% rápido e só então vai a 100%. O OS simulado é ~19% (abaixo de 26,3% ✓)."),
        fig("ex_pid_E", 12))
S += ex("7.14 – Avanço de fase: 200/[(s+10)(s+30)] duas vezes mais rápido",
        "A malha fechada atual tem polos em −20 ± j10. Projete um avanço para ficar 2× mais rápido mantendo o overshoot.",
        P("MF: s<super>2</super> + 40s + 300 + 200 = s<super>2</super> + 40s + 500 ⇒ −20 ± j10. Mesmo ζ (mesmo ângulo) e 2× mais rápido ⇒ <b>s<sub>d</sub> = −40 ± j20</b>."),
        P("Ângulos em s<sub>d</sub>: polo −10 → 180° − arctan(20/30) = 146,31°; polo −30 → 180° − arctan(20/10) = 116,57°. Soma 262,88° ⇒ deficiência <b>82,88°</b>."),
        P("Zero <b>sobre o polo −10</b> (cancela): contribui 146,31°. O polo precisa contribuir 146,31 − 82,88 = 63,43° ⇒ tan 63,43° = 2 = 20/(p − 40) ⇒ <b>p = 50</b> ✓."),
        P("Ganho: |s<sub>d</sub> + 30| = |s<sub>d</sub> + 50| = 22,36 ⇒ 200K<sub>c</sub> = 22,36² = 500 ⇒ <b>K<sub>c</sub> = 2,5</b>. C(s) = 2,5(s+10)/(s+50). "
          "MF: s<super>2</super> + 80s + 2000 ⇒ −40 ± j20 ✓."),
        P("Efeito colateral: K<sub>p</sub> caiu de 200/300 = 0,67 para 500/1500 = 0,33 e o erro ao degrau subiu de 60% para 75%. "
          "O avanço resolve o transitório, não o erro. Para o erro seria preciso adicionar atraso ou PI."))
S += ex("7.15 – PID para K/(s²+5s+4) com ζ = 0,8 e t<sub>p</sub> = 1,047 s",
        "Projete um PID com ζ = 0,8, tempo de pico 1,047 s e erro nulo.",
        P("Polos −1 e −4. Saída do eixo: dK/ds = −(2s + 5) = 0 ⇒ −2,5. Com ζ = 0,8 (θ = 36,87°): ω<sub>d</sub> = 2,5·tan 36,87° = 1,875 ⇒ −2,5 ± j1,875 e K = 2,4·2,4 = <b>5,76</b> (erro ao degrau de 41%)."),
        P("<b>Novo polo:</b> ω<sub>d</sub> = π/1,047 = 3 ⇒ ω<sub>n</sub> = 3/0,6 = 5 ⇒ σ = 0,8·5 = 4 ⇒ <b>s<sub>d</sub> = −4 ± j3</b>."),
        P("<b>PD:</b> de −1 → θ<sub>1</sub> = 135° (distância 4,24); de −4 → θ<sub>2</sub> = 90° (distância 3). θ<sub>z</sub> − 135° − 90° = −180° ⇒ θ<sub>z</sub> = 45° ⇒ <b>zero em −7</b> ✓. "
          "Ganho total = (4,24·3)/4,24 = 3 ⇒ polos exatamente em −4 ± j3."),
        P("<b>PI:</b> zero em −0,1 (bem perto da origem). Refazendo a condição de ângulo na reta ζ = 0,8: <b>−3,87 ± j2,90</b>, com ganho total 2,826. "
          "Como a planta já tem 5,76: C(s) = (2,826/5,76)(s+7)(s+0,1)/s = <b>0,49(s+7)(s+0,1)/s</b> ✓ ⇒ K<sub>d</sub> = 0,49, K<sub>p</sub> = 3,48, K<sub>i</sub> = 0,34. "
          "(No caderno está −3,57 ± j2,9. O valor recalculado é −3,87 ± j2,90.)"),
        fig("ex_pid_F", 12))
S.append(CondPageBreak(25 * cm))

# ================= 8 propostos =================
S += [Paragraph("8. Exercícios propostos (gabarito no fim)", h1)]
props = [
    "Ache a FT E<sub>o</sub>/E<sub>i</sub> da rede de avanço da Figura " + str(FN["rede_avanco"]) + " e mostre que o zero é sempre mais lento (mais perto da origem) que o polo.",
    "Para G(s) = K/[s(s+2)(s+5)]: (a) centroide e ângulos das assíntotas; (b) ponto de saída; (c) K crítico e frequência de cruzamento do eixo jω.",
    "Um sistema de 2ª ordem tem polos em −1 ± j2. Calcule ζ, ω<sub>n</sub>, M<sub>p</sub> e t<sub>s</sub>(2%).",
    "Para G(s) = K/[s(s+1)], projete um compensador de avanço para que os polos dominantes fiquem em ζ = 0,5 e ω<sub>n</sub> = 2.",
    "No sistema da aula, por que não podemos simplesmente usar K = 10 para ter e(∞) = 0,2 à rampa? Justifique com Routh.",
    "Para G(s) = 1,06/[s(s+1)(s+2)], projete um compensador de atraso que aumente K<sub>v</sub> para ~5 sem alterar significativamente os polos dominantes.",
    "Um PI tem G<sub>c</sub> = K<sub>p</sub> + K<sub>i</sub>/s. O que acontece com o tipo do sistema e com o erro ao degrau de uma planta tipo 0?"]
for i, t in enumerate(props, 1):
    S.append(Paragraph(t, ParagraphStyle("pp", parent=body, leftIndent=20), bulletText=f"P{i}."))
S += [Spacer(1, 10), Paragraph("Gabarito", h2)]
gab = [
    "(s + 1/R<sub>1</sub>C<sub>1</sub>)/(s + (R<sub>1</sub>+R<sub>2</sub>)/(R<sub>1</sub>R<sub>2</sub>C<sub>1</sub>)). Como (R<sub>1</sub>+R<sub>2</sub>)/R<sub>2</sub> > 1, o polo é sempre maior em módulo.",
    "(a) σ<sub>a</sub> = −7/3 = −2,33; ±60° e 180°. (b) 3s<super>2</super>+14s+10 = 0 ⇒ s = −0,880. (c) Routh em s<super>3</super>+7s<super>2</super>+10s+K: K = 70, ω = √10 = 3,16 rad/s.",
    "ω<sub>n</sub> = √5 = 2,236; ζ = 1/√5 = 0,447; M<sub>p</sub> ≈ 20,8%; t<sub>s</sub> = 4/1 = 4 s.",
    "s<sub>d</sub> = −1 + j1,732; ∠G(s<sub>d</sub>) = −(120°+90°) = −210° ⇒ falta 30°. Zero em −1 (cancela) e polo em −2; K<sub>c</sub> = |s<sub>d</sub>||s<sub>d</sub>+2| = 2·2 = 4 ⇒ G<sub>c</sub> = 4(s+1)/(s+2).",
    "Routh dá estabilidade só para K < 6; com K = 10 a MF é instável e o teorema do valor final nem vale. Daí a necessidade do atraso.",
    "β ≈ 10 (K<sub>v</sub> original = 0,53): por exemplo G<sub>c</sub> = K<sub>c</sub>(s+0,05)/(s+0,005), com K<sub>c</sub> ≈ 0,9–1, reajustado pela condição de módulo no polo dominante (≈ −0,31 ± j0,55). Erro à rampa ≈ 0,2.",
    "O integrador soma um polo na origem: o tipo sobe de 0 para 1 e o erro ao degrau vai a zero (desde que a MF continue estável)."]
for i, t in enumerate(gab, 1):
    S.append(Paragraph(t, ParagraphStyle("gb", parent=body, leftIndent=20, fontSize=10, leading=13.5), bulletText=f"P{i}."))
S.append(CondPageBreak(25 * cm))

# ================= 9 formulário =================
S += [Paragraph("9. Formulário de bolso e comandos do MATLAB", h1)]
S += table([["Assunto", "Fórmula / regra"],
            ["Malha fechada", "FTMF = G/(1+GH); com GH = N/D e H=1: N/(D+N)"],
            ["Erro", "E = R/(1+GH); e(∞) = lim<sub>s→0</sub> sE(s)"],
            ["Constantes", "K<sub>p</sub>=lim GH; K<sub>v</sub>=lim sGH; K<sub>a</sub>=lim s²GH"],
            ["2ª ordem", "p = −ζω<sub>n</sub> ± jω<sub>n</sub>√(1−ζ²); ω<sub>n</sub> = |p|; ζ = cos θ"],
            ["Desempenho", "M<sub>p</sub> = e<super>−ζπ/√(1−ζ²)</super>; t<sub>p</sub> = π/ω<sub>d</sub>; t<sub>s</sub> = 4/σ (2%)"],
            ["LGR ângulo", "Σ∠zeros − Σ∠polos = ±180°(2k+1)"],
            ["LGR módulo", "K = Π dist. polos / Π dist. zeros"],
            ["Assíntotas", "θ = ±180°(2k+1)/(n−m); σ<sub>a</sub> = (Σp − Σz)/(n−m)"],
            ["Saída/chegada", "K = −1/GH; dK/ds = 0"],
            ["Avanço", "α(Ts+1)/(αTs+1), α<1; φ<sub>max</sub> = arcsen[(1−α)/(1+α)]; ω<sub>m</sub> = 1/(T√α)"],
            ["Atraso", "(Ts+1)/(βTs+1), β>1; aumenta K<sub>v</sub> por ≈ β = z<sub>c</sub>/p<sub>c</sub>"],
            ["Deficiência angular", "φ = −180° − ∠G(s<sub>d</sub>)  (>0 ⇒ avanço)"]], [4.2, 12.2])
S += [Paragraph("Comandos do MATLAB usados em aula", h2)]
S += table([["Comando", "O que faz"],
            ["P=[1]; Q=[1 3 2 0];", "numerador e denominador da FTMA (coeficientes em potências decrescentes de s)"],
            ["roots([1 3 2 1])", "raízes da equação característica (polos de MF)"],
            ["rlocus(P,Q)", "desenha o LGR"],
            ["[K,p]=rlocfind(P,Q)", "clique no LGR: devolve K e os polos naquele ponto"],
            ["step(P,Q)", "resposta ao degrau"],
            ["hold / figure(2)", "sobrepor gráficos / abrir nova janela"],
            ["G=tf(P,Q); T=feedback(G,1)", "cria a FT e fecha a malha unitária"],
            ["sgrid(0.5,[])", "desenha a reta de ζ=0,5 sobre o LGR"]], [6.2, 10.2])
S += dica("Na prova: escreva sempre a FTMA, a equação característica, o tipo e a entrada antes de calcular qualquer coisa. "
          "Metade da nota costuma estar em montar o problema certo.")

# ================= build =================
def on_page(c, d):
    if d.page == 1: return
    c.saveState(); c.setFont("DV", 8.5); c.setFillColor(colors.HexColor("#777"))
    c.drawString(2 * cm, 1.2 * cm, "Teoria de Controle – guia de estudo")
    c.drawRightString(A4[0] - 2 * cm, 1.2 * cm, f"{d.page}")
    c.setStrokeColor(colors.HexColor("#ccd")); c.line(2 * cm, 1.55 * cm, A4[0] - 2 * cm, 1.55 * cm); c.restoreState()

doc = BaseDocTemplate("Teoria_de_Controle_Guia_de_Estudo.pdf", pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm,
                      topMargin=1.8 * cm, bottomMargin=2 * cm, title="Teoria de Controle – Guia de estudo",
                      author="João Antônio Toledo Rodrigues")
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")
doc.addPageTemplates([PageTemplate(id="p", frames=[frame], onPage=on_page)])
doc.build(S)
print("ok")

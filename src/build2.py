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

KEYS = {}
def H1(text, key):
    p = Paragraph(text, h1); p._key = key; return p
def H2k(text, key):
    p = Paragraph(text, h2); p._key = key; return p

PZ = {'Função de transferência e polos': 'Polos −1 e −3, reais e negativos: estável e sem oscilação. O −1 é o <b>dominante</b> (e<super>−t</super> some 3× mais devagar que e<super>−3t</super>) e define t<sub>s</sub> ≈ 4 s. Sem zeros, nenhum efeito extra. Ganho estático 2/3.', 'Tipo e erros': 'Polo na origem ⇒ <b>tipo 1</b>: erro zero ao degrau e finito à rampa. O zero em −2 aumenta K<sub>v</sub> (10·2/5 = 4), acelera a resposta e pode aumentar o sobressinal. Polos de malha fechada −1,52 e −13,5, reais: sem oscilação, com −1,52 dominante.', 'K máximo por Routh': 'Três polos e nenhum zero ⇒ 3 assíntotas (±60°, 180°): dois ramos <b>inevitavelmente</b> cruzam o eixo jω. Por isso existe um K máximo (60). Sem polo na origem ⇒ tipo 0.', 'K para um ζ desejado': 'Dois polos (0 e −4) ⇒ o LGR sai em −2 e sobe na vertical. A parte real fica presa em −2, então t<sub>s</sub> = 2 s para qualquer K complexo e o K só escolhe o ζ. Polo na origem ⇒ tipo 1. Nenhum K instabiliza.', 'Erro ao degrau em sistema tipo 0': 'Sem polo na origem ⇒ tipo 0 ⇒ erro finito ao degrau. Mais K reduz o erro, mas a parte real fica em −2 (t<sub>s</sub> fixo) e ω<sub>d</sub> cresce: mais oscilação.', 'LGR com zero': 'O zero em −3 <b>atrai</b> os ramos: forma o círculo e eles voltam ao eixo real, um indo para o zero e o outro para −∞. Com um zero à esquerda e só 2 polos, o sistema é estável para todo K.', 'Routh de 4ª ordem': 'Polos de malha aberta 0, −3, −1 (duplo), sem zeros ⇒ 4 assíntotas a ±45° e ±135°. O par de ±45° cruza o eixo jω cedo, e o ganho 20 já passou do limite ⇒ 2 polos de malha fechada no semiplano direito.', 'Faixa de K': 'A planta tem um polo de malha aberta no semiplano direito (o termo −3). Só a realimentação com K &gt; 3 o traz para a esquerda; acima de 51 o par complexo atravessa para a direita. A estabilidade existe numa <b>janela</b> de K.', 'LGR passo a passo de K(s+1)': 'O zero −1 fica entre os polos 0 e −2 e prende um ramo no trecho [−1, 0]. Com um zero, 3 assíntotas (em vez de 4) ⇒ K crítico alto (140,8). O polo de malha fechada que vai para o zero −1 tem efeito pequeno (quase cancelado).', 'Zeros no semiplano direito': 'Zero duplo em +2 (fase não mínima) <b>puxa</b> os ramos para a direita, e o polo +1 de malha aberta já é instável. Resultado: nenhum K estabiliza. Seria preciso um compensador que mude polos e zeros, não só o ganho.', 'Ângulo de partida': 'O par −2 ± j3 parte a −142° e curva para as assíntotas de ±135° (fica estável). Quem instabiliza é o ramo saído dos polos 0 e −1, que vai para ±45°. Os polos lentos dominam a estabilidade.', 'Controlador proporcional': 'Polos 0 e −20 ⇒ LGR vertical em σ = −10: a parte real (e o t<sub>s</sub> = 0,4 s) não depende de K; o K só escolhe o ζ (POS). Polo na origem ⇒ tipo 1 (erro à rampa = 20/K).', 'P e depois PID': 'Planta tipo 0 (sem polo em 0) ⇒ o P deixa erro de 16%. O PID adiciona um <b>polo na origem</b> (tipo 1, erro zero) e dois zeros: −3,79 (parte PD, dá o ângulo que puxa o LGR para a esquerda) e −0,235 (parte PI). Esse último forma um <b>dipolo</b> com o polo de malha fechada −0,218 e deixa a cauda lenta.', 'Avanço de fase: 200': 'O zero −10 <b>cancela</b> o polo −10, o que só é seguro porque esse polo é estável e conhecido. O polo novo em −50 é rápido. Os polos de malha fechada dobram de distância à origem com o mesmo ângulo: mesmo ζ, 2× mais rápido. O ganho estático cai e o erro sobe (avanço não cuida de erro).', 'PID para K/(s²+5s+4)': 'Zero do PD em −7 dá +45° para levar o LGR a −4 ± j3. O zero do PI em −0,1 com o polo na origem forma um dipolo: erro zero, mas o polo de malha fechada −0,085 faz a aproximação final ser lenta.'}

# ================= build (two passes: page numbers for TOC and headers) =================
import json, os
LABEL = {"mapa": "Mapa", "malha": "Malha aberta/fechada", "imped": "Impedância", "ampop": "Amp-op", "ft": "Laplace e FT", "ftma": "FTMA/FTMF", "polos": "Polos e zeros", "zeta": "ζ e ωn",
         "estab": "Estabilidade", "routh": "Routh", "erro": "Erro em regime", "lgr": "LGR", "lgrb": "LGR básico", "regras": "Regras do LGR",
         "k": "Como achar K", "ctrl": "Controladores", "pid": "PID", "comp": "Avanço/atraso", "acion": "Acionamentos", "nyq": "Nyquist",
         "ss": "Estados", "trans": "Resposta transitória", "bode": "Bode", "zn": "Ziegler-Nichols", "z": "Transformada Z", "ex": "Exercícios", "prop": "Propostos", "form": "Formulário"}
PRE = {"mapa": [], "malha": ["mapa"], "imped": ["malha"], "ampop": ["imped", "malha"], "ft": ["malha", "imped"], "polos": ["ft", "ftma"], "estab": ["polos", "trans", "ftma"],
       "erro": ["ftma", "estab"], "lgr": ["polos", "zeta", "estab", "routh"], "k": ["regras", "routh", "erro"],
       "ctrl": ["malha", "trans", "erro", "lgrb", "regras", "ampop"], "comp": ["ctrl", "regras", "k", "imped", "ampop"], "acion": ["malha", "trans", "estab", "ss", "zn", "bode"],
       "nyq": ["trans", "estab", "routh", "lgr"], "ss": ["ft", "zeta", "polos", "ctrl"], "z": ["ft", "estab", "pid"],
       "ex": ["polos", "estab", "routh", "regras", "k", "pid", "comp"], "prop": ["ex", "regras", "comp"], "form": []}
CHAP = set(PRE)
class Doc(BaseDocTemplate):
    def afterFlowable(self, f):
        k = getattr(f, "_key", None)
        if k:
            KEYS.setdefault(k, self.page)
            if k in CHAP: PAGECH.setdefault(self.page, []).append(k)
def on_page(c, d):
    if d.page == 1: return
    c.saveState(); c.setFont("DV", 8.5); c.setFillColor(colors.HexColor("#777"))
    c.drawString(2 * cm, 1.2 * cm, "Teoria de Controle – guia de estudo")
    c.drawRightString(A4[0] - 2 * cm, 1.2 * cm, f"{d.page}")
    c.setStrokeColor(colors.HexColor("#ccd")); c.line(2 * cm, 1.55 * cm, A4[0] - 2 * cm, 1.55 * cm); c.restoreState()
def on_page_end(c, d):
    if d.page <= 1: return
    # chapter active on this page: last chapter started on or before this page (from the previous pass)
    ch = None
    for k, p in sorted(PREV.items(), key=lambda kv: kv[1]):
        if k in CHAP and p <= d.page: ch = k
    if not ch: return
    refs = [r for r in PRE.get(ch, []) if r in PREV and PREV[r] != d.page]
    if not refs: return
    mk = lambda rs: "Revise antes: " + "  ·  ".join(f"{LABEL[r]} p. {PREV[r]}" for r in rs)
    while len(refs) > 1 and pdfmetrics.stringWidth(mk(refs), "DVI", 8.3) > A4[0] - 4 * cm: refs = refs[:-1]
    txt = mk(refs)
    c.saveState(); c.setFont("DVI", 8.3); c.setFillColor(colors.HexColor("#7d3c98"))
    c.drawString(2 * cm, A4[1] - 1.05 * cm, txt)
    c.setStrokeColor(colors.HexColor("#e3d7f0")); c.line(2 * cm, A4[1] - 1.25 * cm, A4[0] - 2 * cm, A4[1] - 1.25 * cm); c.restoreState()

def make(path):
    d = Doc(path, pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=1.8 * cm, bottomMargin=2 * cm,
            title="Teoria de Controle – Guia de estudo", author="João Antônio Toledo Rodrigues")
    fr = Frame(d.leftMargin, d.bottomMargin, d.width, d.height, id="f")
    d.addPageTemplates([PageTemplate(id="p", frames=[fr], onPage=on_page, onPageEnd=on_page_end)])
    return d
def story():
    global S
    S = []
    
    # ================= CAPA =================
    S += [Paragraph("Teoria de Controle – guia de estudo", ParagraphStyle("t", fontName="DVB", fontSize=24, leading=29, textColor=NAVY)),
          Paragraph("Montado a partir das aulas, slides e listas (UFOP). Todas as contas foram conferidas numericamente. "
                    "No topo de cada página, a linha <i>Revise antes</i> mostra onde estão os conceitos que ela usa.",
                    ParagraphStyle("st", parent=body, fontSize=10.5, leading=14, textColor=colors.HexColor("#444"))),
          Spacer(1, 6)]
    
    S += [Paragraph("Sumário", h2)]
    TOC = [("mapa", "0. Como encarar a matéria (o mapa)"), ("malha", "A. Malha aberta e malha fechada (com exemplos)"), ("imped", "B. Impedância: resistor, capacitor e indutor"), ("ampop", "C. Amplificador operacional: o controle em forma de circuito"),
           ("ft", "1. Laplace, função de transferência e diagramas de blocos"), ("polos", "2. Polos, zeros e resposta transitória (1ª, 2ª e ordem superior)"),
           ("estab", "3. Estabilidade e instabilidade"), ("erro", "4. Tipo do sistema e erro em regime permanente"),
           ("lgr", "5. Lugar das raízes (LGR)"), ("k", "6. Como achar o K"), ("ctrl", "7. Controladores: P, I, D, PD, PI, PID, on-off, alocação de zeros, Ziegler-Nichols"),
           ("comp", "8. Compensadores: avanço e atraso de fase"), ("acion", "9. Parte de Acionamentos Elétricos (Rashid, cap. 14)"),
           ("nyq", "10. Resposta em frequência: Bode e Nyquist"), ("ss", "11. Espaço de estados"), ("z", "12. Controle digital e transformada Z"),
           ("ex", "13. Exercícios resolvidos (com o que os polos e zeros implicam)"), ("prop", "14. Exercícios propostos (com gabarito)"),
           ("form", "15. Formulário de bolso e MATLAB")]
    for key, t in TOC:
        pg = PREV.get(key, "")
        S.append(Table([[Paragraph(t, ParagraphStyle("su", parent=body, fontSize=10, leading=12.5, spaceAfter=0)), Paragraph(str(pg), ParagraphStyle("sp", parent=body, alignment=2, spaceAfter=0))]],
                       colWidths=[15 * cm, 1.4 * cm], style=TableStyle([("LINEBELOW", (0, 0), (-1, -1), .3, colors.HexColor("#ccd")), ("TOPPADDING", (0, 0), (-1, -1), 1.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5)])))
    # ================= 0 =================
    S += [Spacer(1, 10), H1("0. Como encarar a matéria (o mapa)", "mapa"),
          P("Quase todo problema desta disciplina segue o mesmo caminho. Se você souber em que etapa está, sabe qual ferramenta usar:")]
    S += table([["Etapa", "Pergunta", "Ferramenta"],
                ["1. Modelar", "Como a planta se comporta?", "Função de transferência G(s)"],
                ["2. Fechar a malha", "Como fica com realimentação?", "FTMF = G/(1+GH); equação característica 1+GH=0"],
                ["3. Analisar", "É estável? Oscila? É rápido?", "Polos da malha fechada, ζ, ω<sub>n</sub>, Routh"],
                ["4. Precisão", "Segue a referência sem erro?", "Tipo do sistema, K<sub>p</sub>, K<sub>v</sub>, K<sub>a</sub>, e(∞)"],
                ["5. Ajustar ganho", "Que K deixa como eu quero?", "Lugar das raízes + condição de módulo"],
                ["6. Compensar", "Só ganho não resolve. E agora?", "Avanço (transitório), atraso (erro), PID"]],
               [3.2, 5.6, 7.6])
    
    S += [Paragraph("Siglas e símbolos usados neste guia", h3)]
    S += table([["Sigla / símbolo", "Significa", "Sigla / símbolo", "Significa"],
                ["FT", "função de transferência", "s", "frequência complexa σ + jω (seção 1.0)"],
                ["FTMA", "FT de malha aberta (G·H)", "σ, ω<sub>d</sub>", "parte real (decaimento) e imaginária (oscilação) de um polo"],
                ["FTMF", "FT de malha fechada G/(1+GH)", "ζ, ω<sub>n</sub>", "amortecimento e frequência natural"],
                ["LGR", "lugar geométrico das raízes", "K<sub>p</sub>, K<sub>i</sub>, K<sub>d</sub>", "ganhos proporcional, integral, derivativo"],
                ["EDO", "equação diferencial ordinária", "PID", "proporcional-integral-derivativo"],
                ["CC / CA", "corrente contínua / alternada", "PWM", "modulação por largura de pulso"],
                ["fcem", "força contraeletromotriz do motor", "dB", "decibel: 20·log<sub>10</sub>|G|"]], [2.4, 5.6, 2.6, 5.8])
    S += [P("Sempre que aparecer \"condições iniciais nulas\", leia: o sistema está <b>parado e descarregado</b> no instante zero (capacitor sem carga, motor parado, mola na posição de repouso).")]
    
    S += dica("Em toda questão, escreva primeiro a <b>FTMA</b> (malha aberta) e a <b>equação característica</b> 1 + FTMA = 0. "
              "Polos de malha fechada = raízes dessa equação. Erro em regime sai da FTMA. O LGR também é desenhado a partir da FTMA. "
              "Ou seja: a FTMA é o ponto de partida de quase tudo.",
              "Transitório (oscilação, rapidez) → olhe os <b>polos de malha fechada</b>. "
              "Regime (erro) → olhe o <b>tipo</b> e o <b>ganho de baixa frequência</b> da FTMA.")
    S.append(CondPageBreak(12 * cm))
    
    
    
    # ================= A malha aberta/fechada =================
    S += [H1("A. Malha aberta e malha fechada", "malha"),
          P("Esta é a ideia que dá nome à disciplina. Um <b>sistema de controle</b> faz alguma grandeza física (a saída y: velocidade, temperatura, posição, nível) "
            "seguir um valor desejado (a <b>referência</b> r), mesmo com perturbações. Existem dois jeitos de fazer isso."),
          Paragraph("A.1 Malha aberta: o controle \"cego\"", h2),
          P("O controlador calcula a ação <b>uma vez</b>, a partir da referência, e manda para o atuador. <b>Ninguém mede o resultado.</b> "
            "Se algo mudar no caminho (carga, desgaste, temperatura ambiente), a saída erra e o controlador nem fica sabendo. Matematicamente, Y(s) = G(s)·R(s)."),
          ]
    S += table([["Exemplo de malha aberta", "Como funciona", "O que dá errado"],
                ["Torradeira de 2 minutos", "liga a resistência por um tempo fixo", "pão mais úmido ou mais grosso sai claro; pão fino queima"],
                ["Máquina de lavar por timer", "cada etapa dura um tempo programado", "não sabe se a roupa está limpa"],
                ["Semáforo de tempo fixo", "verde por 40 s, vermelho por 30 s", "não vê a fila de carros"],
                ["Irrigação por timer", "liga a água 10 min por dia", "rega mesmo depois de chover"],
                ["Motor CC ligado direto na tensão", "aplica a tensão que daria a velocidade desejada", "com carga, a velocidade cai e fica caída"]], [4.2, 5.6, 6.6])
    S += [Paragraph("A.2 Malha fechada: o controle com \"olhos\"", h2),
          P("Um <b>sensor</b> mede a saída, um <b>somador</b> compara com a referência e o controlador age sobre a diferença, o <b>erro</b> e = r − y. "
            "Enquanto houver erro, a ação continua. Por isso também se chama <b>controle por realimentação</b> (feedback). "
            "É realimentação <b>negativa</b>: a medida entra subtraindo, para que um excesso na saída reduza a ação."),
          fig("malha_ab_fe", 15, "Figura 0 – Os mesmos blocos nas duas estruturas. A diferença é o sensor e o somador fechando o caminho de volta."),
          ]
    S += table([["Exemplo de malha fechada", "Sensor", "O que ele corrige"],
                ["Ar-condicionado com termostato", "termômetro", "liga e desliga conforme a temperatura real do ambiente"],
                ["Caixa d'água com boia", "a própria boia mede o nível", "fecha a entrada quando enche, qualquer que seja o consumo"],
                ["Piloto automático do carro", "velocímetro", "acelera mais na subida, alivia na descida"],
                ["Seu corpo", "termorreceptores", "suor e calafrio mantêm ~36,5 °C"],
                ["Braço robótico", "encoders nas juntas", "chega na coordenada certa mesmo com peso na garra"],
                ["Buck com feedback (seu trabalho)", "leitura da tensão ou velocidade pelo Arduino", "ajusta o PWM quando a carga do motor muda"]], [4.6, 3.8, 8])
    S += [Paragraph("A.3 Os blocos e o papel de cada um", h2)]
    S += table([["Bloco", "Papel", "Braço robótico", "Controle de temperatura"],
                ["R(s) referência", "o que eu quero", "coordenada (x, y, z) da peça", "25 °C"],
                ["H(s) sensor", "os olhos", "encoders nas juntas", "termômetro lê 20 °C"],
                ["E(s) erro", "R − H·Y", "peça a 10 cm, garra a 2 cm: 8 cm", "25 − 20 = 5 °C"],
                ["G<sub>c</sub>(s) controlador", "o cérebro", "algoritmo calcula o sinal das juntas", "microcontrolador: \"está frio, potência alta\""],
                ["G<sub>a</sub>(s) atuador", "o músculo", "servomotores (torque)", "relé que liga a resistência"],
                ["G<sub>p</sub>(s) planta", "a coisa física", "braço com massa, inércia e gravidade", "volume de ar esquentando"],
                ["Y(s) saída", "o que acontece", "posição real da garra", "temperatura real"]], [3.4, 2.6, 5.0, 5.4])
    S += [P("<b>O que é o R − H·Y da coluna do erro?</b> É a fórmula do erro: <b>E = R − H·Y</b>, ou seja, referência menos a leitura do sensor. Y é a saída real; H é o sensor, que entrega Y multiplicado pelo seu ganho (o ponto é multiplicação). "
            "Então <b>H·Y é o que o controlador enxerga</b>, e o sinal de menos é o que torna a realimentação negativa (A.5). "
            "Se o sensor lê a grandeza direto (termômetro), H = 1 e E = R − Y = 25 − 20 = 5 °C. Se converte unidade, H aparece: no motor do Rashid (cap. 9) o sensor dá 0,095 V por rad/s, "
            "então a 100 rad/s ele entrega H·Y = 9,5 V e o erro é E = V<sub>r</sub> − 9,5 V, com a referência também em volts.")]
    S += [P("Cada bloco multiplica o que entra nele. Juntando, chega-se à <b>função de transferência de malha fechada</b>, deduzida com calma no capítulo 1:"),
          eq(r"U=G_aG_c\,E,\quad Y=G_p\,U\ \Rightarrow\ \frac{Y}{E}=G_cG_aG_p=G(s);\qquad E=R-HY\ \Rightarrow\ \frac{Y}{R}=\frac{G}{1+GH}"),
          Paragraph("A.4 Exemplo real (Acionamentos, Rashid Ex. 14.13): o motor com carga", h2),
          P("Motor CC de 50 kW, 240 V e 1700 rpm, alimentado por conversor de ganho K<sub>2</sub> = 100, com sensor de velocidade de 95 mV/(rad/s) (detalhes no capítulo 9). Torque nominal de 280,9 N·m."),
          ]
    S += B(["<b>Malha aberta:</b> regula-se a tensão para 1700 rpm a vazio. Ao entrar o torque nominal, a velocidade cai 17 rad/s, para <b>1537,7 rpm</b>. A regulação é de <b>10,55%</b>, e o controlador nunca percebe.",
            "<b>Malha fechada</b> (a medida da velocidade é comparada com a referência): com a mesma carga, a velocidade cai só 2 rad/s, para <b>1680,5 rpm</b>. A regulação é de <b>1,16%</b>.",
            "<b>Por quê?</b> A queda de velocidade fica dividida por (1 + ganho de malha). Aqui, o termo K<sub>1</sub>K<sub>2</sub>K<sub>v</sub>I<sub>f</sub> = 12,1 é somado ao denominador original 1,65: "
            "(1,65 + 12,1)/1,65 ≈ 8,3 vezes menos queda. É a <b>sensibilidade</b> reduzida pela realimentação."])
    S += [fig("rashid_regulacao", 13, "Figura 0 – Velocidade × torque de carga no Exemplo 14.13: a realimentação deixa a reta quase horizontal."),
          P("Note que mesmo em malha fechada sobra uma pequena queda. Esse controlador é só proporcional e o motor é tipo 0 (capítulo 4). Com um PI, a queda iria a zero. É por isso que os acionamentos reais usam PI (capítulo 9).")]
    S += table([["", "Malha aberta", "Malha fechada"],
                ["Precisa de sensor?", "não (mais barato e simples)", "sim"],
                ["Corrige perturbações e desgaste?", "não", "sim"],
                ["Precisão", "depende de conhecer bem a planta", "depende de um bom sensor"],
                ["Pode ficar instável?", "não, se a planta for estável", "<b>sim</b>: ganho demais faz oscilar (capítulo 3)"],
                ["Quando usar", "processo previsível, sem perturbação, erro tolerável", "precisão, perturbações, planta que muda ou instável"]], [4.4, 5.8, 6.2])
    
    S += [Paragraph("A.5 Realimentação negativa × realimentação positiva", h2),
          P("Na realimentação <b>negativa</b>, a medida entra <b>subtraindo</b> no somador: e = r − y. Se a saída passa do alvo, o erro fica negativo e a ação diminui, então o sistema se <b>autocorrige</b>. "
            "Na realimentação <b>positiva</b>, a medida entra <b>somando</b>: o sinal de volta reforça o próprio desvio, e um pequeno aumento gera mais aumento, numa \"bola de neve\"."),
          eq(r"\mathrm{negativa:}\ \frac{Y}{R}=\frac{G}{1+GH}\qquad\qquad \mathrm{positiva:}\ \frac{Y}{R}=\frac{G}{1-GH}"),
          P("Com a positiva, a equação característica vira 1 − GH = 0, e os polos são empurrados para a <b>direita</b>. Exemplo com a planta 1/(s+1) e ganho K: na negativa o polo vai para s = −(1 + K), sempre mais estável. "
            "Na positiva vai para s = K − 1, e <b>passa a ser instável quando K &gt; 1</b>."),
          fig("realim_positiva", 14, "Figura 0 – A mesma planta com realimentação positiva (polo andando para a direita) e negativa (polo andando para a esquerda)."),
          ]
    S += table([["Realimentação positiva indesejada (instabilidade)", "Realimentação positiva útil (de propósito)"],
                ["Microfonia: o microfone capta a caixa de som, que amplifica o que o microfone capta, e vem o apito", "Comparador com histerese (Schmitt trigger): base do controlador on-off (seção 7.5)"],
                ["Corrida térmica: o transistor esquenta, conduz mais, esquenta mais e queima", "Osciladores: o ganho de malha igual a 1 sustenta a oscilação de propósito"],
                ["Sinal trocado no somador ao montar o circuito: o motor dispara em vez de regular", "Memórias (latch, flip-flop): o circuito \"trava\" num estado"],
                ["A máquina com zero em +2 (seção 2): a correção passa a ajudar o erro", "Partida rápida de um dispositivo que precisa ir de um extremo ao outro"]], [8.2, 8.2])
    S += [P("No motor CC (capítulo 9), a <b>fcem</b> é uma realimentação negativa natural: velocidade maior gera fcem maior, que reduz a corrente e o torque. É ela que torna o motor estável em malha aberta (Rashid, Eq. 14.60).")]
    
    S += dica("A pergunta-chave para classificar: <b>a saída é medida e comparada com a referência?</b> Se sim, é malha fechada; se não, é aberta. "
              "Um timer, por mais \"inteligente\" que seja, é malha aberta.")
    S.append(CondPageBreak(25 * cm))
    
    
    # ================= B impedância =================
    S += [H1("B. Impedância: resistor, capacitor e indutor", "imped"),
          P("Quase todo controlador analógico e quase toda planta elétrica são feitos de resistores, capacitores e indutores. <b>Impedância</b> é o que permite tratar os três com a mesma regra da Lei de Ohm."),
          Paragraph("B.1 O que é", h2),
          P("Impedância Z é a <b>oposição que um componente oferece à corrente</b>, generalizada para sinais que variam no tempo: <b>Z = V/I</b>, medida em ohms (Ω). "
            "No resistor é só a resistência. No capacitor e no indutor, a oposição <b>depende da frequência</b> e vem com <b>defasagem</b> entre tensão e corrente. Por isso Z é um número complexo:"),
          eq(r"Z=R+jX\qquad Z_R=R\qquad Z_L=j\omega L\ \ (\to sL)\qquad Z_C=\frac{1}{j\omega C}\ \ (\to \frac{1}{sC})"),
          P("A parte real R é a <b>resistência</b> (dissipa energia). A parte imaginária X é a <b>reatância</b> (armazena energia e devolve). "
            "No domínio de Laplace troca-se jω por s, e as mesmas expressões viram funções de transferência."),
          fig("impedancia", 15, "Figura 0 – Esquerda: o resistor não depende da frequência; o indutor cresce com ω; o capacitor cai com ω. Direita: as defasagens."),
          Paragraph("B.2 O comportamento de cada um", h2)]
    S += table([["Componente", "Lei no tempo", "Impedância", "Baixa frequência (CC)", "Alta frequência", "Fase da corrente"],
                ["Resistor R", "v = R·i", "R", "R", "R", "em fase (0°)"],
                ["Indutor L", "v = L·di/dt", "jωL = sL", "curto-circuito", "circuito aberto", "atrasa 90°"],
                ["Capacitor C", "i = C·dv/dt", "1/(jωC) = 1/(sC)", "circuito aberto", "curto-circuito", "adianta 90°"]], [2.6, 2.6, 2.8, 2.9, 2.8, 2.7])
    S += [P("Intuição física: o capacitor carregado <b>bloqueia corrente contínua</b>, mas uma tensão que oscila rápido o carrega e descarrega o tempo todo e a corrente passa. "
            "O indutor <b>resiste a mudanças de corrente</b>: em CC é só um fio, mas não deixa a corrente variar rápido. "
            "As defasagens (capacitor adianta, indutor atrasa) são a origem física do \"avanço\" e do \"atraso\" de fase dos compensadores (capítulo 8)."),
          Paragraph("B.3 Como combinar (igual a resistores)", h2)]
    S += B(["<b>Série:</b> Z = Z<sub>1</sub> + Z<sub>2</sub>. Ex.: resistor + indutor da armadura do motor: Z = R<sub>a</sub> + sL<sub>a</sub>.",
            "<b>Paralelo:</b> Z = Z<sub>1</sub>Z<sub>2</sub>/(Z<sub>1</sub> + Z<sub>2</sub>). Ex.: R ∥ C = R/(1 + sRC).",
            "<b>Divisor de tensão:</b> V<sub>o</sub>/V<sub>i</sub> = Z<sub>2</sub>/(Z<sub>1</sub> + Z<sub>2</sub>). É assim que se tira a função de transferência de redes RC em uma linha."])
    S += exemplo("Exemplos: tirando funções de transferência com impedância",
                 P("<b>Filtro passa-baixas RC</b> (R em série, C na saída): V<sub>o</sub>/V<sub>i</sub> = (1/sC)/(R + 1/sC) = <b>1/(RCs + 1)</b>. Um polo em −1/RC: deixa passar baixas frequências e a resposta ao degrau é de 1ª ordem (τ = RC)."),
                 P("<b>Passa-altas</b> (C em série, R na saída): V<sub>o</sub>/V<sub>i</sub> = R/(R + 1/sC) = <b>RCs/(RCs + 1)</b>. Um zero na origem e um polo em −1/RC: bloqueia CC."),
                 P("<b>Armadura do motor:</b> I<sub>a</sub>/(V<sub>a</sub> − E<sub>a</sub>) = 1/(L<sub>a</sub>s + R<sub>a</sub>), polo em −R<sub>a</sub>/L<sub>a</sub> (capítulo 9)."),
                 P("<b>Valores:</b> com C = 10 µF a 60 Hz (ω = 377 rad/s), |Z<sub>C</sub>| = 1/(377·10<super>−5</super>) ≈ 265 Ω. A 6 kHz cai para ≈ 2,65 Ω."))
    S += dica("No amp-op (próxima seção), a função de transferência é sempre −Z<sub>f</sub>/Z<sub>i</sub>. Saber escrever a impedância de cada rede (R, 1/sC, R + 1/sC, R ∥ C) é tudo que você precisa para projetar P, I, D, PI, PD e avanço/atraso com circuitos.")
    S.append(CondPageBreak(25 * cm))
    
    # ================= A amp-op =================
    S += [H1("C. Amplificador operacional: o controle em forma de circuito", "ampop"),
          P("Com malha e impedância em mãos, vale entender <b>com que peça física</b> se monta um controlador analógico. Quase sempre é o amplificador operacional (amp-op). "
            "Somador do erro, ganho K<sub>p</sub>, integrador, derivador, avanço, atraso e PID inteiro são todos amp-ops com resistores e capacitores em volta. "
            "Dominando duas regras e uma fórmula, você lê qualquer circuito de controle."),
          Paragraph("C.1 O que é", h2),
          P("É um amplificador <b>diferencial</b> de ganho enorme: v<sub>o</sub> = A(v<sub>+</sub> − v<sub>−</sub>), com A da ordem de 10<super>5</super> a 10<super>6</super>. "
            "Tem duas entradas (inversora −, não inversora +), uma saída e é alimentado por ±V<sub>cc</sub> (ex.: ±12 V). "
            "A saída nunca passa da alimentação: se a conta der 20 V com fonte de 12 V, ela <b>satura</b> em ~12 V."),
          fig("ampop", 16.5, "Figura 0 – Amp-op ideal e os circuitos básicos usados em controle."),
          Paragraph("C.2 As duas regras de ouro (amp-op ideal)", h2)]
    S += B(["<b>Regra 1 – não entra corrente nas entradas:</b> i<sub>+</sub> = i<sub>−</sub> = 0 (impedância de entrada infinita).",
            "<b>Regra 2 – curto-circuito virtual:</b> com realimentação <b>negativa</b> (saída ligada de volta à entrada −), v<sub>+</sub> = v<sub>−</sub>. "
            "Motivo: v<sub>+</sub> − v<sub>−</sub> = v<sub>o</sub>/A. Com A ≈ 10<super>5</super> e v<sub>o</sub> de poucos volts, a diferença é de microvolts, praticamente zero.",
            "Repare: o amp-op realimentado <b>já é um sistema de controle em malha fechada</b>. Ele mexe na saída até zerar o \"erro\" v<sub>+</sub> − v<sub>−</sub>."])
    S += [Paragraph("C.3 Inversor e a fórmula que resolve tudo: −Z<sub>f</sub>/Z<sub>i</sub>", h2),
          P("No inversor, v<sub>+</sub> = 0 ⇒ v<sub>−</sub> = 0 (terra virtual). A corrente que entra por R<sub>1</sub>, v<sub>i</sub>/R<sub>1</sub>, não entra no amp-op (regra 1). "
            "Então ela passa toda por R: v<sub>i</sub>/R<sub>1</sub> = −v<sub>o</sub>/R ⇒ <b>v<sub>o</sub> = −(R/R<sub>1</sub>)v<sub>i</sub></b>. "
            "Trocando os resistores por impedâncias no domínio s (resistor R, capacitor 1/(sC)), vale para qualquer rede:"),
          eq(r"\frac{V_o(s)}{V_i(s)}=-\frac{Z_f(s)}{Z_i(s)}\qquad Z_R=R,\quad Z_C=\frac{1}{sC}"),
          Paragraph("C.4 Não inversor e diferencial (slides da aula)", h2),
          P("<b>Não inversor:</b> v<sub>i</sub> entra no +. Pela regra 2, v<sub>−</sub> = v<sub>i</sub>, e v<sub>−</sub> sai do divisor R<sub>1</sub>–R: v<sub>−</sub> = v<sub>o</sub>·R<sub>1</sub>/(R<sub>1</sub>+R). "
            "Logo <b>v<sub>c</sub> = (1 + R/R<sub>1</sub>)·v<sub>E</sub></b>: ganho positivo, sempre ≥ 1."),
          P("<b>Diferencial:</b> a referência v<sub>R</sub> entra pelo + e a medida do sensor v<sub>Y</sub> pelo −. Com resistores casados, <b>v<sub>c</sub> = (R/R<sub>1</sub>)(v<sub>R</sub> − v<sub>Y</sub>)</b>. "
            "Este circuito faz duas coisas ao mesmo tempo: o <b>somador</b> da malha (e = r − y) e o <b>ganho K<sub>p</sub> = R/R<sub>1</sub></b>. É um controlador proporcional completo. "
            "No slide, R é um potenciômetro: girar o potenciômetro é ajustar o K<sub>p</sub>, que é exatamente andar sobre o lugar das raízes."),
          Paragraph("C.5 Cada ação de controle é uma escolha de Z<sub>i</sub> e Z<sub>f</sub>", h2)]
    S += table([["Ação", "Z<sub>i</sub> (entrada)", "Z<sub>f</sub> (realimentação)", "V<sub>o</sub>/V<sub>i</sub>", "Parâmetros"],
                ["P", "R<sub>1</sub>", "R<sub>2</sub>", "−R<sub>2</sub>/R<sub>1</sub>", "K<sub>p</sub> = R<sub>2</sub>/R<sub>1</sub>"],
                ["I (integrador)", "R<sub>1</sub>", "C", "−1/(R<sub>1</sub>Cs)", "K<sub>i</sub> = 1/(R<sub>1</sub>C)"],
                ["D (derivador)", "C", "R<sub>2</sub>", "−R<sub>2</sub>Cs", "K<sub>d</sub> = R<sub>2</sub>C"],
                ["PI", "R<sub>1</sub>", "R<sub>2</sub> em série com C", "−(R<sub>2</sub>/R<sub>1</sub>)[1 + 1/(R<sub>2</sub>Cs)]", "K<sub>p</sub> = R<sub>2</sub>/R<sub>1</sub>, T<sub>i</sub> = R<sub>2</sub>C"],
                ["PD", "R<sub>1</sub> ∥ C", "R<sub>2</sub>", "−(R<sub>2</sub>/R<sub>1</sub>)(1 + R<sub>1</sub>Cs)", "K<sub>p</sub> = R<sub>2</sub>/R<sub>1</sub>, T<sub>d</sub> = R<sub>1</sub>C"],
                ["Avanço / atraso", "R<sub>1</sub> ∥ C<sub>1</sub>", "R<sub>2</sub> ∥ C<sub>2</sub>", "−(R<sub>2</sub>/R<sub>1</sub>)(R<sub>1</sub>C<sub>1</sub>s+1)/(R<sub>2</sub>C<sub>2</sub>s+1)", "avanço se R<sub>1</sub>C<sub>1</sub> &gt; R<sub>2</sub>C<sub>2</sub>"]],
               [2.6, 2.6, 3.4, 4.6, 3.2])
    S += [P("O sinal \"−\" do inversor é desfeito colocando um segundo inversor de ganho −1 em série (por isso os circuitos de compensador do Ogata usam dois amp-ops). "
            "Repare na fase: o integrador (1/s) <b>atrasa 90°</b> e o derivador (s) <b>adianta 90°</b>. É de onde vêm os nomes atraso e avanço de fase (seções 7 e 8).")]
    S += exemplo("Exemplo – montar um PI com K<sub>p</sub> = 2 e T<sub>i</sub> = 0,5 s",
                 P("Escolha C = 1 µF. De T<sub>i</sub> = R<sub>2</sub>C: R<sub>2</sub> = 0,5/10<super>−6</super> = <b>500 kΩ</b>. De K<sub>p</sub> = R<sub>2</sub>/R<sub>1</sub>: R<sub>1</sub> = 500k/2 = <b>250 kΩ</b>. "
                   "Resultado: V<sub>o</sub>/V<sub>i</sub> = −2(1 + 1/(0,5s)) = −(2 + 4/s), ou seja, K<sub>p</sub> = 2 e K<sub>i</sub> = 4. Um inversor de ganho −1 depois corrige o sinal."),
                 P("Cuidado prático: o integrador puro sem resistor em paralelo com C acumula offset e satura (é o \"wind-up\" da ação integral)."))
    S += dica("Viu um amp-op numa questão? (1) Ache a realimentação negativa e aplique v<sub>+</sub> = v<sub>−</sub>. (2) Correntes nas entradas são zero. "
              "(3) Se for inversor, use direto −Z<sub>f</sub>/Z<sub>i</sub>, com capacitor = 1/(sC). Pronto: você tem a FT do controlador.")
    S.append(CondPageBreak(25 * cm))
    
    
    # ================= 1 FT =================
    S += [H1("1. Laplace, função de transferência e diagramas de blocos", "ft"),
          P("A <b>função de transferência</b> (FT) é a razão entre a transformada de Laplace da saída e a da entrada, "
            "considerando <b>condições iniciais nulas</b>. Ela transforma equações diferenciais em álgebra: derivar vira multiplicar por s, integrar vira dividir por s."),
          eq(r"G(s)=\frac{C(s)}{R(s)}\qquad \mathcal{L}\left\{\frac{dx}{dt}\right\}=sX(s)\qquad \mathcal{L}\left\{\int x\,dt\right\}=\frac{X(s)}{s}"),
          P("A forma geral (slide da aula) é uma razão de polinômios em s:"),
          eq(r"G_p(s)=\frac{b_0s^m+b_1s^{m-1}+\dots+b_{m-1}s+b_m}{a_0s^n+a_1s^{n-1}+\dots+a_{n-1}s+a_n}"),
          P("O grau n do denominador é a <b>ordem</b> do sistema (o número da maior derivada da EDO). Em sistemas físicos, n ≥ m (sistema <i>próprio</i>). "
            "As raízes de Q(s) (denominador) são os <b>polos</b>, e as de P(s) (numerador) são os <b>zeros</b>. Se n > m, sobram n − m <b>zeros no infinito</b>."),
          Paragraph("1.0 A variável s e a transformada de Laplace", h2),
          Paragraph("O que é o s (frequência complexa)", h3),
          P("<b>s</b> é uma variável complexa, s = σ + jω, chamada <b>frequência complexa</b>. Ela representa um sinal do tipo e<super>st</super> = e<super>σt</super>·(cos ωt + j·sen ωt): "
            "a parte real <b>σ</b> diz quanto o sinal cresce (σ &gt; 0) ou decai (σ &lt; 0) por segundo, e a parte imaginária <b>ω</b> diz quão rápido ele oscila (rad/s). "
            "Por isso a unidade de s é 1/s (o mesmo que rad/s)."),
          P("A grande vantagem: derivar e<super>st</super> é só multiplicar por s, porque d(e<super>st</super>)/dt = s·e<super>st</super>. Por isso, no mundo de Laplace, <b>derivar vira multiplicar por s</b> e <b>integrar vira dividir por s</b>. "
            "Quando dizemos que um sistema tem um polo em s = −2, queremos dizer que ele contém um termo e<super>−2t</super> na resposta. Um polo em s = −1 ± j3 dá e<super>−t</super>cos 3t. "
            "O plano s (eixo horizontal σ, vertical jω) é o \"mapa\" onde desenhamos polos, zeros e o lugar das raízes. Fazendo σ = 0 (s = jω), olhamos só senoides puras, e é isso que o diagrama de Bode faz (capítulo 10)."),
    
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
    S += [
          CondPageBreak(9 * cm), H2k("1.3 FTMA, FTMF e equação característica (malha fechada em fórmulas)", "ftma"),
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
    S += [CondPageBreak(9 * cm), Paragraph("1.4 Diagramas de blocos, redução e Mason", h2),
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
    S += [H1("2. Polos, zeros e a resposta do sistema", "polos"),
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
            "Com K = 0 o controlador está desligado e os polos de malha fechada ficam exatamente em cima dos polos de MA."),
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
          H2k("2.1 Sistemas de 2ª ordem: ζ, ω<sub>n</sub>, ω<sub>d</sub>", "zeta"),
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
    
    S += [CondPageBreak(9 * cm), Paragraph("2.3 O que cada coisa representa (glossário rápido)", h2)]
    S += table([["Termo", "O que é", "O que implica no sistema"],
                ["Polo", "raiz do denominador da FT", "um modo e<super>pt</super> da resposta: define velocidade, oscilação e estabilidade"],
                ["Zero", "raiz do numerador", "não cria modo; muda o peso dos modos (mais sobressinal, ou undershoot se estiver à direita)"],
                ["Polo real negativo −a", "modo e<super>−at</super>", "decai sem oscilar; constante de tempo 1/a"],
                ["Par complexo −σ ± jω<sub>d</sub>", "modo e<super>−σt</super>cos ω<sub>d</sub>t", "oscila amortecido: σ dá o t<sub>s</sub>, ω<sub>d</sub> a frequência, o ângulo dá o ζ"],
                ["Polo na origem (1/s)", "integrador", "aumenta o tipo: zera o erro a uma classe de entrada; sozinho é marginal"],
                ["Polo no semiplano direito", "modo e<super>+at</super>", "instabilidade: a resposta cresce sem limite"],
                ["Zero no semiplano direito", "fase não mínima", "resposta começa no sentido errado (undershoot); limita o ganho possível"],
                ["Polo dominante", "o mais próximo do eixo jω", "manda no transitório; os outros somem antes"],
                ["Cancelamento polo-zero", "zero em cima de um polo", "o modo some da saída (só é seguro se o polo cancelado for estável)"],
                ["Dipolo", "polo e zero muito próximos", "efeito pequeno no transitório, mas cria uma cauda lenta"],
                ["Ganho estático G(0)", "valor final para degrau unitário", "quanto a saída anda em regime por unidade de entrada"],
                ["Equação característica", "1 + GH = 0", "suas raízes são os polos de malha fechada"]], [3.6, 4.2, 8.6])
    
    
    S += [CondPageBreak(10 * cm), H2k("2.4 Análise de resposta transitória: 1ª ordem, 2ª ordem e ordem superior", "trans"),
          P("<b>Resposta transitória</b> é a parte da resposta entre o instante em que algo muda (a referência ou uma carga) e o momento em que a saída se acomoda. Depois disso vem o <b>regime permanente</b>. "
            "Para comparar sistemas, aplica-se um sinal de teste padrão, quase sempre o <b>degrau</b> (mudança súbita de referência), e mede-se:"),
          fig("resp_transitoria", 14.5, "Figura 0 – As especificações de desempenho no tempo."),
          ]
    S += table([["Especificação", "Definição", "O que mede"],
                ["t<sub>d</sub> atraso", "tempo para chegar a 50% do valor final", "quanto demora para \"reagir\""],
                ["t<sub>r</sub> subida", "de 10% a 90% (ou de 0 a 100% em sistemas oscilatórios)", "rapidez"],
                ["t<sub>p</sub> pico", "instante do primeiro pico", "rapidez da oscilação"],
                ["M<sub>p</sub> sobressinal", "(pico − final)/final × 100%", "quanto passa do alvo (amortecimento)"],
                ["t<sub>s</sub> acomodação", "tempo para ficar dentro de ±2% (ou ±5%) do final", "quando dá para considerar \"parado\""],
                ["e<sub>ss</sub> erro em regime", "referência − valor final", "precisão (capítulo 4)"]], [3.4, 7.2, 5.8])
    S += [Paragraph("Sistemas de 1ª ordem", h3),
          eq(r"G(s)=\frac{K}{\tau s+1}\qquad y(t)=K\left(1-e^{-t/\tau}\right)\ \ \mathrm{(degrau\ unitario)}"),
          P("Um único polo em s = −1/τ. <b>K</b> é o ganho estático (onde a saída para) e <b>τ</b> a constante de tempo (quão rápido chega lá). Em t = τ a saída chega a 63,2%; em 3τ, 95%; em 4τ, 98%. "
            "t<sub>r</sub> ≈ 2,2τ, t<sub>s</sub> ≈ 4τ, e <b>nunca há sobressinal nem oscilação</b>: o polo é real. A inclinação inicial é K/τ. Para entrada rampa, a saída segue com atraso de τ. "
            "<b>Exemplos:</b> circuito RC (τ = RC), tanque (τ = 1/K), barco (τ = m/B) e, na parte de Acionamentos, o <b>conversor</b> K<sub>r</sub>/(1 + sτ<sub>r</sub>) e o <b>filtro do tacogerador</b> 0,074/(1 + 0,002s) do Rashid."),
          Paragraph("Sistemas de 2ª ordem", h3),
          eq(r"G(s)=\frac{\omega_n^2}{s^2+2\zeta\omega_n s+\omega_n^2}\qquad s=-\zeta\omega_n\pm j\omega_n\sqrt{1-\zeta^2}"),
          ]
    S += table([["ζ", "Nome", "Polos", "Resposta ao degrau"],
                ["ζ = 0", "sem amortecimento", "±jω<sub>n</sub> (sobre o eixo jω)", "oscila para sempre na frequência ω<sub>n</sub>"],
                ["0 &lt; ζ &lt; 1", "subamortecido", "par complexo", "oscila amortecido; tem sobressinal"],
                ["ζ = 1", "criticamente amortecido", "dois reais iguais", "o mais rápido sem passar do alvo"],
                ["ζ &gt; 1", "superamortecido", "dois reais distintos", "lento, sem sobressinal (parece 1ª ordem)"]], [2.2, 4, 4.6, 5.6])
    S += [eq(r"t_r=\frac{\pi-\beta}{\omega_d},\ \ \beta=\arccos\zeta\qquad t_p=\frac{\pi}{\omega_d}\qquad M_p=e^{-\zeta\pi/\sqrt{1-\zeta^2}}\qquad t_s\approx\frac{4}{\zeta\omega_n}\ (2\%)", 13),
          P("Exemplo da figura acima (ζ = 0,4, ω<sub>n</sub> = 1): ω<sub>d</sub> = 0,917, β = 66,4°, t<sub>r</sub> = 2,16 s, t<sub>p</sub> = 3,43 s, M<sub>p</sub> = 25,4%, t<sub>s</sub> ≈ 10 s pela fórmula (o envelope é conservador; a curva real entra na faixa em ~8,4 s). "
            "<b>Na parte de Acionamentos:</b> o motor CC é de 2ª ordem (constantes de tempo elétrica τ<sub>a</sub> e mecânica τ<sub>m</sub>) e sempre superamortecido (Rashid, Eq. 14.60). "
            "A malha de corrente é projetada com ζ = 0,707, ou seja, sobressinal de 4,3% (Rashid, Eq. 14.110)."),
          Paragraph("Sistemas de ordem superior", h3),
          P("Com 3 ou mais polos, a resposta é a <b>soma dos modos</b> de cada polo (é isso que as frações parciais mostram). Na prática:"),
          ]
    S += B(["<b>Polos dominantes:</b> os mais próximos do eixo jω mandam. Se os outros estão 5 vezes ou mais à esquerda, o sistema se comporta como o 2ª ordem formado pelo par dominante, e as fórmulas acima valem aproximadamente.",
            "<b>Polo a mais (à esquerda):</b> deixa a resposta mais lenta e com menos sobressinal (atrasa).",
            "<b>Zero a mais (à esquerda):</b> deixa mais rápida e com <b>mais</b> sobressinal. Quanto mais perto da origem, maior o efeito.",
            "<b>Zero à direita:</b> a resposta começa indo para o lado errado (undershoot).",
            "<b>Na parte de Acionamentos:</b> a malha de velocidade otimizada do Rashid é de 3ª ordem com um zero, e por isso tem 43,4% de sobressinal. "
            "Retirando o efeito do zero com um pré-filtro, cai para 8,1% (capítulo 9). É exatamente o efeito do zero na figura abaixo."])
    S += [fig("ordem_superior", 14, "Figura 0 – Mesmo par de polos dominantes; muda só um polo ou um zero extra.")]
    S += dica("Na prova: (1) conte os polos (ordem); (2) ache os dominantes; (3) se forem um par complexo, use as fórmulas de 2ª ordem com ζ e ω<sub>n</sub> dele; "
              "(4) diga qualitativamente o que os outros polos e zeros fazem (mais lento, mais sobressinal, undershoot).")
    
    S.append(CondPageBreak(25 * cm))
    
    
    
    # ================= 3 estabilidade =================
    S += [H1("3. Estabilidade e instabilidade: o que é, onde e por quê", "estab"),
          P("<b>Estabilidade</b> é a propriedade de, depois de uma perturbação ou de uma mudança de referência, a saída <b>voltar a se acomodar</b> num valor finito. "
            "<b>Instabilidade</b> é o contrário: a saída cresce sem parar (ou até algo físico saturar, quebrar ou desarmar). Um pêndulo pendurado é estável; um lápis em pé na ponta é instável."),
          Paragraph("3.1 As três situações", h2)]
    S += table([["Situação", "Definição", "Onde estão os polos de malha fechada", "Resposta típica"],
                ["Estável (assintoticamente)", "a resposta natural vai a zero", "todos com parte real &lt; 0 (semiplano esquerdo)", "acomoda; e<super>−at</super> some"],
                ["Marginalmente estável", "não cresce, mas não morre", "polos simples sobre o eixo jω (ou em s = 0), nenhum à direita", "oscila para sempre (±jω) ou fica parada/deriva (s = 0)"],
                ["Instável", "a resposta cresce sem limite", "pelo menos um com parte real &gt; 0, ou polo repetido sobre jω", "e<super>+at</super> ou oscilação crescente"]], [3.3, 3.6, 4.8, 4.7])
    S += [P("<b>Estabilidade BIBO</b> (entrada limitada → saída limitada): para sistemas lineares, equivale a todos os polos estarem estritamente no semiplano esquerdo. "
            "Um sistema marginal <b>não</b> é BIBO-estável: um integrador 1/s com entrada degrau (limitada) dá uma rampa (ilimitada)."),
          fig("estab_mapas", 14, "Figura 0 – Regiões de estabilidade: semiplano esquerdo no contínuo, interior do círculo unitário no digital (seção 12)."),
          Paragraph("3.2 Por que é o sinal da parte real", h2),
          P("Cada polo p = σ + jω vira um termo e<super>pt</super> = e<super>σt</super>(cos ωt + j sen ωt) na resposta. O fator e<super>σt</super> decide tudo: σ &lt; 0 encolhe, σ = 0 mantém e σ &gt; 0 cresce. "
            "A parte imaginária só decide <b>se oscila e com que frequência</b>, não se explode."),
          Paragraph("3.3 Onde e por que um sistema fica instável", h2)]
    S += B(["<b>Ganho alto demais na malha:</b> o controlador reage forte demais, passa do alvo, reage forte para o outro lado e cada volta fica maior. No LGR, é quando um ramo cruza o eixo jω (K = 6 na planta da aula).",
            "<b>Atraso e fase acumulada:</b> cada polo atrasa até 90° de fase. Com 3 ou mais polos (ou atraso de transporte, ou amostragem lenta), a correção chega \"fora de fase\" e passa a <b>reforçar</b> o erro. "
            "No Nyquist, é quando a curva envolve o ponto −1 (seção 10).",
            "<b>Realimentação positiva efetiva:</b> sinal errado no somador, ou zero/polo no semiplano direito, faz a malha ajudar o erro a crescer (o carro rápido demais que acelera mais, seção 2).",
            "<b>A própria planta instável:</b> polo de malha aberta à direita (pêndulo invertido, levitação, o Exercício 13.8). Aí a realimentação é <b>obrigatória</b> para estabilizar.",
            "<b>Amostragem:</b> no controle digital, o mesmo K que era estável no contínuo pode instabilizar se o período T for grande (seção 12)."])
    S += [Paragraph("3.4 Por que realimentar estabiliza (e por que às vezes desestabiliza)", h2),
          P("A malha fechada move os polos: 1 + KG = 0. Com K pequeno, os polos de malha fechada ficam perto dos de malha aberta. Aumentando K, eles andam pelo LGR. "
            "Se a planta tem poucos polos (1 ou 2) e nenhum zero à direita, o LGR nunca cruza o eixo jω e qualquer K é estável. Com 3 ou mais polos a mais que zeros, as assíntotas apontam para a direita e sempre existe um K crítico. "
            "Zeros à esquerda (PD, avanço) entortam o LGR para a esquerda e aumentam o K crítico. É isso que o slide quer dizer com \"acrescenta um zero, portanto aumenta a estabilidade\"."),
          H2k("3.5 Critério de Routh-Hurwitz (estabilidade sem achar as raízes)", "routh"),
          P("<b>Condição necessária:</b> todos os coeficientes da equação característica presentes e com o mesmo sinal. Se faltar um termo ou houver sinal trocado, é instável (ou marginal) e nem precisa montar a tabela. "
            "<b>Condição necessária e suficiente:</b> a tabela de Routh. O número de trocas de sinal na 1ª coluna = número de polos no semiplano direito.")]
    S += table([["Linha", "Coluna 1", "Coluna 2", "Coluna 3"],
                ["s<super>n</super>", "a<sub>0</sub>", "a<sub>2</sub>", "a<sub>4</sub>"],
                ["s<super>n−1</super>", "a<sub>1</sub>", "a<sub>3</sub>", "a<sub>5</sub>"],
                ["s<super>n−2</super>", "b<sub>1</sub> = (a<sub>1</sub>a<sub>2</sub> − a<sub>0</sub>a<sub>3</sub>)/a<sub>1</sub>", "b<sub>2</sub> = (a<sub>1</sub>a<sub>4</sub> − a<sub>0</sub>a<sub>5</sub>)/a<sub>1</sub>", "…"],
                ["s<super>n−3</super>", "c<sub>1</sub> = (b<sub>1</sub>a<sub>3</sub> − a<sub>1</sub>b<sub>2</sub>)/b<sub>1</sub>", "…", ""]], [2.2, 5.4, 5.4, 3.4])
    S += B(["<b>Zero só na 1ª coluna:</b> troque o zero por ε pequeno positivo e continue; analise o sinal com ε → 0⁺.",
            "<b>Linha inteira de zeros:</b> há raízes simétricas (pares ±jω ou ±σ). Monte o <b>polinômio auxiliar</b> com a linha de cima, derive-o e use a derivada no lugar da linha nula. "
            "As raízes do polinômio auxiliar são justamente os pontos onde o LGR cruza o eixo jω (por isso o K crítico sai daí).",
            "<b>Para achar o K crítico:</b> deixe K como letra, exija 1ª coluna positiva e resolva as desigualdades (exemplos 5.3, 13.3, 13.7 e 13.8)."])
    S += dica("Para dizer <b>onde</b> fica instável: Routh dá o K limite, a linha s² dá a frequência de oscilação, e o LGR mostra por onde os polos atravessam. "
              "Para dizer <b>por quê</b>: fale do sinal da parte real (e<super>σt</super>), do excesso de polos/atraso de fase, ou de zero/polo no semiplano direito.")
    S.append(CondPageBreak(25 * cm))
    
    # ================= 3 tipo e erro =================
    S += [H1("4. Tipo do sistema e erro em regime permanente", "erro"),
          P("<b>Erro em regime permanente</b> e(∞) é quanto a saída fica longe da referência depois que o transitório acabou. "
            "Calcula-se pelo <b>teorema do valor final</b>, aplicado a E(s) = R(s)/(1 + FTMA):"),
          eq(r"e(\infty)=\lim_{t\to\infty}e(t)=\lim_{s\to 0}s\,E(s)=\lim_{s\to 0}\frac{s\,R(s)}{1+G(s)H(s)}"),
          P("<b>Só vale se a malha fechada for estável.</b> Se houver polo de malha fechada no semiplano direito, o erro não converge."),
          Paragraph("4.1 O que é o \"tipo\"", h2),
          P("Escreva a FTMA na forma de constantes de tempo. O <b>tipo</b> é o expoente N de s no denominador, ou seja, "
            "o <b>número de integradores (polos na origem) da FTMA</b>:"),
          eq(r"G(s)H(s)=\frac{K(T_as+1)(T_bs+1)\cdots}{s^N(T_1s+1)(T_2s+1)\cdots}\qquad N=\mathrm{tipo}"),
          P("Cada integrador \"acumula\" erro e o empurra para zero. Por isso, quanto maior o tipo, mais tipos de entrada o sistema segue sem erro."),
          Paragraph("4.2 Constantes de erro e tabela", h2),
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
                   "A especificação pedia e(∞) = 0,2, ou seja, K<sub>v</sub> = 5, <b>10 vezes maior</b>. É isso que motiva o compensador de atraso da seção 8."))
    S += dica("Roteiro do erro: (1) confira se a malha fechada é estável; (2) conte os s na origem da FTMA (tipo); "
              "(3) identifique a entrada (degrau, rampa, parábola); (4) use a tabela. Só faça o limite completo se a questão pedir.",
              "Erro grande demais? Aumentar K reduz o erro, mas muda os polos (pode oscilar ou instabilizar). "
              "Para mexer no erro sem estragar o transitório, use <b>compensador de atraso</b>.")
    S.append(CondPageBreak(25 * cm))
    
    
    # ================= 4 LGR =================
    S += [H1("5. Lugar das raízes (LGR)", "lgr"),
          P("O <b>lugar geométrico das raízes</b> é o desenho, no plano s, do caminho que os <b>polos de malha fechada</b> percorrem quando o ganho K varia de 0 a ∞. "
            "Ele responde: \"se eu aumentar o ganho, o sistema fica mais rápido? Começa a oscilar? Fica instável? Com qual K?\""),
          P("Os polos de malha fechada são as raízes de 1 + KG(s)H(s) = 0, ou seja, KG(s)H(s) = −1. Um número complexo é −1 quando tem módulo 1 e ângulo 180°. Daí saem as duas condições:"),
          P("<b>Condição de ângulo:</b>"), eq(r"\angle G(s)H(s)=\sum\angle\mathrm{zeros}-\sum\angle\mathrm{polos}=\pm180^\circ(2k+1)"),
          P("<b>Condição de módulo:</b>"), eq(r"|K\,G(s)H(s)|=1\ \Rightarrow\ K=\frac{\prod\ \mathrm{dist.\ aos\ polos}}{\prod\ \mathrm{dist.\ aos\ zeros}}"),
          P("A <b>condição de ângulo</b> diz <i>se</i> um ponto pertence ao LGR. A <b>condição de módulo</b> diz <i>qual K</i> leva o polo até aquele ponto."),
          H2k("5.1 O LGR \"normal\": como polos e zeros moldam a curva", "lgrb")]
    S += [P("Antes das regras, vale ver o padrão. Os ramos <b>saem dos polos</b> e <b>vão para os zeros</b>. Se faltam zeros, vão para o infinito pelas assíntotas. "
            "Um <b>polo a mais</b> empurra o LGR para a direita (rumo à instabilidade). Um <b>zero</b> o puxa e entorta para a esquerda (mais estabilidade)."),
          fig("lgr_basico", 16.5, "Figura 0 – Seis LGRs básicos: compare (c) com (e) para ver o efeito de um zero, e (b) com (c) para ver o efeito de um polo a mais."),
          ]
    S += table([["Caso", "O que acontece", "Por quê"],
                ["1 polo", "vai para −∞ pelo eixo real; sempre estável", "1 ramo, assíntota a 180°"],
                ["2 polos reais", "se encontram no meio e sobem na vertical; oscila mas nunca instabiliza", "2 assíntotas a ±90° saindo do centroide"],
                ["3 polos", "2 ramos curvam para ±60° e cruzam o eixo jω", "n − m = 3 ⇒ assíntotas apontam para a direita"],
                ["2 polos + 1 zero à esquerda", "círculo em torno do zero e volta ao eixo; sempre estável", "o zero \"atrai\" os ramos"],
                ["Zero à direita", "um ramo é puxado para o semiplano direito", "fase não mínima: limita K"]], [3.6, 7, 5.8])
    S += [H2k("5.2 Regras de construção", "regras")]
    rules = [
        "<b>Início e fim:</b> o LGR começa (K=0) nos <b>polos</b> da FTMA e termina (K→∞) nos <b>zeros</b> da FTMA. Se há n polos e m zeros, n−m ramos vão para o infinito.",
        "<b>Número de ramos</b> = número de polos da FTMA (n). O LGR é <b>simétrico</b> em relação ao eixo real.",
        "<b>Eixo real:</b> um trecho do eixo real é LGR se tiver um número <b>ímpar</b> de polos + zeros (reais) à sua direita.",
        "<b>Assíntotas:</b> os n−m ramos que vão para o infinito seguem retas com ângulos θ = ±180°(2k+1)/(n−m), saindo do centroide σ<sub>a</sub> = (Σpolos − Σzeros)/(n−m).",
        "<b>Pontos de saída/chegada</b> no eixo real: escreva K = −1/G(s)H(s) e resolva dK/ds = 0. Fique só com as raízes que estão em trechos de LGR.",
        "<b>Cruzamento com o eixo jω</b> (limite de estabilidade): use Routh-Hurwitz na equação característica, ou substitua s = jω e iguale partes real e imaginária a zero.",
        "<b>Ângulo de partida</b> de um polo complexo: θ<sub>part</sub> = 180° + Σθ<sub>z</sub> − Σθ<sub>p</sub>, usando os ângulos dos <i>outros</i> polos e zeros até esse polo. "
        "<b>Ângulo de chegada</b> a um zero complexo: θ<sub>cheg</sub> = 180° + Σθ<sub>p</sub> − Σθ<sub>z</sub>. Exemplo no Exercício 13.11.",
        "<b>Achar K num ponto:</b> condição de módulo (seção 6)."]
    for i, r in enumerate(rules, 1):
        S.append(Paragraph(r, ParagraphStyle("rl", parent=body, leftIndent=18, bulletIndent=2), bulletText=f"{i}."))
    S += [fig("regra_eixo", 12, "Figura 5 – Regra do eixo real para polos em 0, −1 e −2.")]
    S += [CondPageBreak(8 * cm), Paragraph("5.3 Exemplo completo: K/[s(s+1)(s+2)] (o sistema da aula)", h2)]
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
    S += [H1("6. Como achar o K", "k"),
          P("\"Achar o K\" aparece de quatro jeitos diferentes. Identifique qual a questão quer:")]
    S += table([["A questão pede...", "Como fazer"],
                ["K para um polo num ponto s<sub>d</sub> dado (ou para um ζ desejado)", "Condição de módulo: K = Π|s<sub>d</sub>−p<sub>i</sub>| / Π|s<sub>d</sub>−z<sub>j</sub>|"],
                ["K máximo para estabilidade", "Routh-Hurwitz: zerar a linha s¹ (ou achar onde muda de sinal)"],
                ["K para atender um erro em regime", "K<sub>p</sub>, K<sub>v</sub> ou K<sub>a</sub> desejado → isola K"],
                ["K no ponto de saída do eixo real", "K = −1/GH avaliado no ponto onde dK/ds = 0"]], [7.6, 8.8])
    S += exemplo("Exemplo 6.1 – K para ζ = 0,5 no sistema K/[s(s+1)(s+2)]",
                 P("<b>1.</b> Trace a reta ζ = 0,5: ângulo θ = arccos(0,5) = 60° com o eixo real negativo. Pontos: s = ω<sub>n</sub>(−0,5 + j0,866)."),
                 P("<b>2.</b> Ache o ponto da reta que satisfaz a condição de ângulo: ∠s + ∠(s+1) + ∠(s+2) = 180°. "
                   "Testando (ou resolvendo numericamente), ω<sub>n</sub> = 0,667: s<sub>d</sub> = −0,333 + j0,577. Confira: 120° + 40,9° + 19,1° = 180° ✓."),
                 P("<b>3.</b> Condição de módulo (produto das distâncias aos polos):"),
                 eq(r"K=|s_d|\cdot|s_d+1|\cdot|s_d+2|=0{,}667\times0{,}882\times1{,}764=1{,}037", 14),
                 P("Com K = 1,037 os polos de malha fechada ficam em −0,333 ± j0,577 e −2,333. Repare que K = 1 (aula) dá ζ = 0,515, bem perto disso."))
    S += exemplo("Exemplo 6.2 – K máximo e K para erro",
                 P("<b>Estabilidade:</b> pelo Routh (seções 3.5 e 5.3), K<sub>máx</sub> = 6 (oscila com ω = 1,414 rad/s)."),
                 P("<b>Erro à rampa ≤ 0,2:</b> K<sub>v</sub> = K/2 ≥ 5 ⇒ K ≥ 10. Mas K = 10 > 6 deixa o sistema <b>instável</b>! "
                   "Conclusão: só com ganho não dá para ter erro pequeno e estabilidade ao mesmo tempo. É preciso um <b>compensador</b>."))
    S += dica("Distância no plano s: |s<sub>d</sub> − p| = √[(Re)<super>2</super> + (Im)<super>2</super>] da diferença. Ângulo: arctan(Im/Re), "
              "com cuidado no quadrante (se o ponto está à esquerda do polo, o ângulo passa de 90°). "
              "No MATLAB: <font face='DejaVuSansMono'>[K,polos]=rlocfind(P,Q)</font> e clique no ponto.")
    S.append(CondPageBreak(25 * cm))
    
    
    
    # ================= 7 controladores =================
    S += [H1("7. Controladores: P, I, D, PD, PI, PID, on-off e outros", "ctrl"),
          P("O controlador é o bloco G<sub>c</sub>(s) que transforma o erro e(t) em sinal de controle u(t). Cada tipo põe polos e zeros diferentes na FTMA e por isso mexe no LGR e no erro de um jeito diferente."),
          Paragraph("7.1 Proporcional-Derivativo (PD), como no slide", h2),
          P("O sinal de saída do controlador é proporcional ao erro <b>e</b> à derivada do erro:"),
          eq(r"u(t)=K_p\left(e(t)+T_d\frac{de(t)}{dt}\right)\ \Rightarrow\ G_{PD}(s)=\frac{U(s)}{E(s)}=K_p(1+sT_d)=K_pT_d\left(s+\frac{1}{T_d}\right)"),
          P("T<sub>d</sub> é a <b>constante de tempo derivativa</b>. O PD <b>acrescenta um zero em s = −1/T<sub>d</sub></b>. Pelas regras do LGR, um zero atrai os ramos e o número de assíntotas cai em 1. "
            "O lugar das raízes fica mais à esquerda, o K crítico aumenta (ou desaparece) e o sistema fica <b>mais estável e mais amortecido</b>. Fisicamente, o D antecipa: reage à velocidade do erro e freia antes de passar do alvo."),
          fig("pd_zero", 14, "Figura 0 – Mesmo sistema de 3 polos: só P (instável para K &gt; 12) × PD com zero em −2 (estável para todo K)."),
          P("Cuidados: o PD não muda o tipo (não zera erro) e o termo s amplifica ruído de alta frequência. Na prática usa-se o derivativo filtrado, T<sub>d</sub>s/(1 + T<sub>d</sub>s/N), que é exatamente um compensador de <b>avanço</b>."),
          Paragraph("7.2 A família completa de controladores", h2)]
    S += table([["Controlador", "G<sub>c</sub>(s)", "Polos/zeros que adiciona", "Para que serve"],
                ["P", "K<sub>p</sub>", "nenhum (só escolhe o ponto no LGR)", "ajuste simples de rapidez; deixa erro em tipo 0"],
                ["I", "K<sub>i</sub>/s", "polo na origem", "zera erro, mas lento e tende a instabilizar"],
                ["PI", "K<sub>p</sub>(1 + 1/(T<sub>i</sub>s))", "polo em 0 + zero em −1/T<sub>i</sub>", "zera erro ao degrau mantendo o transitório (≈ atraso)"],
                ["PD", "K<sub>p</sub>(1 + T<sub>d</sub>s)", "zero em −1/T<sub>d</sub>", "mais estabilidade e menos sobressinal (≈ avanço)"],
                ["PID", "K<sub>p</sub>(1 + 1/(T<sub>i</sub>s) + T<sub>d</sub>s)", "polo em 0 + dois zeros", "erro zero e bom transitório"],
                ["PI-D / I-PD", "D (ou P e D) aplicados só na medida y", "mesmos polos, zeros diferentes na referência", "evita o \"chute\" do derivativo quando a referência muda em degrau"],
                ["Avanço / atraso", "K<sub>c</sub>(s+z)/(s+p)", "um zero e um polo", "versões realizáveis do PD e do PI (seção 8)"],
                ["On-off", "liga/desliga", "não linear", "simples e barato; oscila sempre (7.5)"],
                ["Cascata", "malha interna + externa", "—", "motores: malha de corrente dentro da de velocidade (seção 9)"],
                ["Feedforward", "age direto pela referência ou pelo distúrbio medido", "não altera estabilidade", "antecipa perturbações conhecidas"],
                ["Realimentação de estados", "u = −Kx", "posiciona todos os polos", "projeto moderno (seção 11)"],
                ["Digital", "equação de diferenças u[k]", "polos/zeros no plano z", "Arduino, CLP, microcontrolador (seção 12)"]], [3.0, 3.6, 4.6, 5.2])
    
    S += [CondPageBreak(12 * cm), H2k("7.3 PID: o que é, com exemplos de P, I e D", "pid"),
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
    S += [CondPageBreak(10 * cm), Paragraph("7.4 Ações P, I e D em detalhe", h2),
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
        "Confira os polos de malha fechada. O zero do PI cria um polo lento perto dele, o que deixa uma \"cauda\" na resposta."], 1):
        S.append(Paragraph(r, ParagraphStyle("rpid", parent=body, leftIndent=18), bulletText=f"{i}."))
    
    S += [CondPageBreak(10 * cm), Paragraph("7.5 Controlador on-off (liga-desliga)", h2),
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
    
    S += [CondPageBreak(10 * cm), Paragraph("7.6 Alocação de zeros (e de polos)", h2),
          P("<b>Alocação de zeros</b> é escolher <b>onde ficam os zeros do controlador</b> para moldar o lugar das raízes e a resposta. Como o ganho K só move os polos <i>sobre</i> o LGR existente, "
            "os zeros (e os polos) do controlador são o que <b>muda o desenho do LGR</b>. Um zero atrai os ramos e soma ângulo positivo nos pontos acima dele; um polo repele e soma ângulo negativo. "
            "<b>Alocação de polos</b> é o mesmo raciocínio no projeto por estados (capítulo 11), em que se escolhe diretamente onde ficam todos os polos de malha fechada."),
          ]
    S += table([["Técnica", "Ideia", "Onde aparece neste guia"],
                ["Cancelamento", "pôr o zero em cima de um polo lento e estável da planta, que some da resposta", "Rashid: τ<sub>c</sub> = τ<sub>2</sub> na malha de corrente (9.7); avanço 8.2 (zero em −2); Ex. 13.14 (zero em −10)"],
                ["Deficiência angular", "posicionar o zero para fornecer o ângulo que falta para o LGR passar no polo desejado", "Ex. 13.15 (zero do PD em −7), Ex. 13.13 (−3,79)"],
                ["Zero perto da origem (PI/atraso)", "zero colado no polo do integrador: zera o erro sem mudar o transitório (dipolo)", "atraso da aula (8.5); PI do motor (9.8)"],
                ["Zero na referência / pré-filtro", "um polo no caminho da referência cancela um zero da malha fechada e reduz o sobressinal", "Rashid: rede polo-zero que baixa de 43,4% para 8,1% (9.8)"],
                ["Zero duplo do PID", "o PID de Ziegler-Nichols põe dois zeros iguais em −4/P<sub>cr</sub>", "7.7"]], [3.6, 6.4, 6.4])
    S += [P("<b>Cuidados:</b> nunca cancele um polo instável ou mal conhecido (se ele mudar um pouco, o cancelamento falha e o modo instável aparece). Zeros aumentam o sobressinal (figura de ordem superior, seção 2.4). "
            "E zero no semiplano direito não se corrige com controlador: ele limita o desempenho."),
          CondPageBreak(10 * cm), H2k("7.7 Regras de Ziegler-Nichols (sintonia de PID)", "zn"),
          P("<b>O que é:</b> um conjunto de regras empíricas (Ziegler e Nichols, 1942) para escolher K<sub>p</sub>, T<sub>i</sub> e T<sub>d</sub> de um PID <b>sem conhecer o modelo da planta</b>, só com um ensaio simples. "
            "<b>O que representa:</b> as regras buscam uma resposta com <b>razão de decaimento de 1/4</b> (cada pico tem um quarto da amplitude do anterior). É uma resposta rápida, mas com sobressinal grande (tipicamente 25 a 60%). "
            "É um <b>ponto de partida</b> para o ajuste fino, não o projeto final."),
          Paragraph("1º método: curva de reação (resposta ao degrau em malha aberta)", h3),
          P("Aplique um degrau na planta sem controlador. Se a resposta tiver forma de \"S\" (sem polo na origem e sem oscilação), trace a reta tangente no ponto de inflexão. "
            "Ela corta o eixo do tempo em <b>L</b> (atraso aparente) e chega ao valor final após <b>T</b> (constante de tempo aparente).")]
    S += table([["Controlador", "K<sub>p</sub>", "T<sub>i</sub>", "T<sub>d</sub>"],
                ["P", "T/L", "∞", "0"], ["PI", "0,9·T/L", "L/0,3", "0"], ["PID", "1,2·T/L", "2L", "0,5L"]], [4, 4, 4, 4.4])
    S += [Paragraph("2º método: ganho crítico (oscilação sustentada)", h3),
          P("Com o controle só proporcional em malha fechada, aumente K<sub>p</sub> até a saída <b>oscilar sem crescer nem morrer</b>. Esse é o <b>ganho crítico K<sub>cr</sub></b>, e o período da oscilação é <b>P<sub>cr</sub></b>. "
            "É exatamente o ponto em que o LGR cruza o eixo jω: dá para obter K<sub>cr</sub> pelo Routh e P<sub>cr</sub> = 2π/ω pela linha s² (seção 3.5).")]
    S += table([["Controlador", "K<sub>p</sub>", "T<sub>i</sub>", "T<sub>d</sub>"],
                ["P", "0,5·K<sub>cr</sub>", "∞", "0"], ["PI", "0,45·K<sub>cr</sub>", "P<sub>cr</sub>/1,2", "0"], ["PID", "0,6·K<sub>cr</sub>", "0,5·P<sub>cr</sub>", "0,125·P<sub>cr</sub>"]], [4, 4, 4, 4.4])
    S += [eq(r"G_{PID}=K_p\left(1+\frac{1}{T_is}+T_ds\right)=0{,}075\,K_{cr}P_{cr}\,\frac{(s+4/P_{cr})^2}{s}", 14),
          P("Ou seja, o PID de Ziegler-Nichols é uma <b>alocação de zeros</b> automática: um polo na origem e um <b>zero duplo em s = −4/P<sub>cr</sub></b>.")]
    S += exemplo("Exemplos: planta da aula e malha de velocidade do motor (Acionamentos)",
                 P("<b>Planta da aula, 1/[s(s+1)(s+2)]:</b> pelo Routh, K<sub>cr</sub> = 6 e ω = √2 ⇒ P<sub>cr</sub> = 2π/√2 = 4,44 s. "
                   "PID: K<sub>p</sub> = 3,6, T<sub>i</sub> = 2,22 s e T<sub>d</sub> = 0,555 s (zero duplo em −0,90). Simulando: sobressinal de ~59% e t<sub>s</sub> ≈ 13 s. É rápido, mas oscilatório, como esperado do critério de 1/4."),
                 P("<b>Parte de Acionamentos (motor do Rashid, Ex. 14.14):</b> conversor + motor + tacogerador com controle P. A oscilação sustentada aparece com K<sub>cr</sub> = 50, a 165 rad/s ⇒ P<sub>cr</sub> = 38 ms. "
                   "PID: K<sub>p</sub> = 30, T<sub>i</sub> = 19,0 ms e T<sub>d</sub> = 4,7 ms. Curiosidade: o T<sub>i</sub> = 19 ms coincide com o τ<sub>s</sub> = 19,02 ms do ótimo simétrico do livro. Sobressinal simulado de ~58%: daí a necessidade de ajuste fino ou de pré-filtro."),
                 fig("zn", 15.5))
    
    S.append(CondPageBreak(25 * cm))
    
    
    # ================= 6 compensadores =================
    S += [H1("8. Compensadores: avanço e atraso de fase", "comp"),
          P("Quando ajustar só o ganho K não atende transitório e erro ao mesmo tempo, coloca-se um <b>compensador</b> G<sub>c</sub>(s) em série. "
            "Os dois clássicos têm a mesma forma, com um zero e um polo. O que muda é <b>quem vem primeiro</b>:"),
          eq(r"G_c(s)=K_c\,\frac{s+z_c}{s+p_c}"),
          P("• <b>z<sub>c</sub> &lt; p<sub>c</sub></b> (zero mais perto da origem) → <b>AVANÇO</b>.   • <b>z<sub>c</sub> &gt; p<sub>c</sub></b> (polo mais perto da origem) → <b>ATRASO</b>."),
          Paragraph("8.1 Avanço de fase: o que é", h2),
          P("Um compensador de <b>avanço de fase</b> é aquele cuja saída senoidal fica <b>adiantada</b> em relação à entrada: a fase de G<sub>c</sub>(jω) é <b>positiva</b>. "
            "No LGR, isso significa que ele <b>soma ângulo positivo</b> nos pontos do plano s e \"puxa\" o LGR para a esquerda. "
            "Resultado: polos mais rápidos e mais amortecidos, com melhor <b>transitório</b> e mais estabilidade."),
          Paragraph("8.2 De onde vem isso na elétrica: o capacitor", h2),
          P("A ideia vem do <b>capacitor</b>. Nele, i = C·dv/dt. Se v = sen(ωt), então i = ωC·cos(ωt) = ωC·sen(ωt + 90°): "
            "<b>a corrente adianta 90° em relação à tensão</b>. Em fasores, Z<sub>C</sub> = 1/(jωC) = −j/(ωC). "
            "Qualquer circuito em que o capacitor \"passa\" o sinal de alta frequência adiantado tende a adiantar a fase. "
            "A derivada faz a mesma coisa: derivar um seno o adianta em 90°. Por isso avanço ≈ ação <b>derivativa</b> (PD) suavizada."),
          fig("capacitor", 14, "Figura 7 – No capacitor, a corrente adianta 90° em relação à tensão. É a origem física do \"avanço\"."),
          Paragraph("8.3 O componente: a rede RC de avanço", h2),
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
    S += exemplo("Exemplo 8.1 – Dimensionar a rede de avanço",
                 P("Queremos zero em −2 e polo em −4 (α = 0,5). Escolha C<sub>1</sub> = 1 µF. Então R<sub>1</sub> = 1/(2·10<super>−6</super>) = <b>500 kΩ</b>. "
                   "Do polo: (R<sub>1</sub>+R<sub>2</sub>)/(R<sub>1</sub>R<sub>2</sub>C<sub>1</sub>) = 4 ⇒ R<sub>2</sub> = <b>500 kΩ</b>. "
                   "α = 0,5 ⇒ φ<sub>max</sub> = arcsen(0,5/1,5) = <b>19,5°</b> em ω<sub>m</sub> = 2/√0,5 = 2,83 rad/s. "
                   "Note que a rede vale exatamente (s+2)/(s+4): em baixa frequência ela atenua para α = 0,5 (= 2/4). Para ter o G<sub>c</sub> = 4(s+2)/(s+4) do Exemplo 8.2, basta um amplificador de ganho 4 depois da rede."))
    S += [CondPageBreak(9 * cm), Paragraph("8.4 Projeto de avanço pelo LGR (deficiência angular)", h2)]
    for i, r in enumerate([
        "Transforme as especificações (M<sub>p</sub>, t<sub>s</sub>) em ζ e ω<sub>n</sub>, e daí no polo desejado s<sub>d</sub> = −ζω<sub>n</sub> + jω<sub>d</sub>.",
        "Calcule o ângulo da planta em s<sub>d</sub>: ∠G(s<sub>d</sub>). Se não der −180°, falta ângulo. Essa é a <b>deficiência angular</b> φ = −180° − ∠G(s<sub>d</sub>).",
        "Posicione o zero e o polo do compensador para que ∠zero − ∠polo = φ. Opções: cancelar um polo da planta com o zero, ou o método da bissetriz.",
        "Ache K<sub>c</sub> pela condição de módulo em s<sub>d</sub>.",
        "Confira: polos dominantes de fato dominantes? Erro em regime aceitável? Simule o degrau."], 1):
        S.append(Paragraph(r, ParagraphStyle("rl2", parent=body, leftIndent=18), bulletText=f"{i}."))
    S += exemplo("Exemplo 8.2 – Projeto de avanço",
                 P("Planta G(s) = 4/[s(s+2)]. Sem compensador, malha fechada = 4/(s<super>2</super>+2s+4), ζ = 0,5, ω<sub>n</sub> = 2 (t<sub>s</sub> ≈ 4 s). "
                   "<b>Quero o dobro da velocidade:</b> ζ = 0,5 e ω<sub>n</sub> = 4 ⇒ s<sub>d</sub> = −2 ± j3,464."),
                 P("<b>Ângulo da planta em s<sub>d</sub>:</b> ∠s<sub>d</sub> = 120°, ∠(s<sub>d</sub>+2) = 90° ⇒ ∠G = −210°. Deficiência: φ = −180° − (−210°) = <b>+30°</b> (precisa de AVANÇO)."),
                 P("<b>Zero e polo:</b> ponha o zero em −2 (cancela o polo da planta). Ele contribui +90°. O polo deve contribuir 90° − 30° = 60°: "
                   "p = −2 − 3,464/tan 60° = <b>−4</b>."),
                 P("<b>Ganho:</b> FTMA = 4K<sub>c</sub>/[s(s+4)]. Em s<sub>d</sub>: 4K<sub>c</sub> = |s<sub>d</sub>|·|s<sub>d</sub>+4| = 4·4 = 16 ⇒ <b>K<sub>c</sub> = 4</b>."),
                 eq(r"G_c(s)=4\,\frac{s+2}{s+4}\qquad \mathrm{FTMF}=\frac{16}{s^2+4s+16}\ (\zeta=0{,}5,\ \omega_n=4)", 14),
                 P("Bônus: K<sub>v</sub> passou de 2 para 4, então o erro à rampa caiu de 0,5 para 0,25."),
                 fig("avanco_exemplo", 15))
    S += [CondPageBreak(7 * cm), Paragraph("8.5 Atraso de fase", h2),
          P("O compensador de <b>atraso</b> tem o <b>polo mais perto da origem</b> que o zero, então a fase é negativa. O objetivo dele <b>não</b> é mexer no transitório: "
            "é <b>aumentar o ganho de baixa frequência</b> (K<sub>p</sub>, K<sub>v</sub>) e com isso <b>reduzir o erro em regime</b>. "
            "O truque é colocar polo e zero <b>bem pertinho da origem e um do outro</b>. Vistos de longe (do polo dominante), eles quase se cancelam: "
            "contribuem com poucos graus (< 5°) e módulo ≈ 1, e o LGR quase não muda. Em s → 0, porém, a razão z<sub>c</sub>/p<sub>c</sub> multiplica o ganho."),
          fig("rede_atraso", 9.5, "Figura 10 – Rede de atraso passiva (o capacitor vai no ramo para o terra)."),
          eq(r"\frac{E_o}{E_i}=\frac{R_2Cs+1}{(R_1+R_2)Cs+1}=\frac{1}{\beta}\,\frac{s+\frac{1}{T}}{s+\frac{1}{\beta T}},\qquad T=R_2C,\ \ \beta=\frac{R_1+R_2}{R_2}>1"),
          ]
    S += exemplo("Exemplo 8.3 – O compensador de atraso da aula, passo a passo",
                 P("<b>Planta:</b> 1/[s(s+1)(s+2)] com K = 1: ζ = 0,5147 (bom transitório), mas e(∞) à rampa = 2. <b>Meta:</b> e(∞) = 0,2 sem estragar o transitório."),
                 P("<b>1. Ganho necessário:</b> com G<sub>c</sub> = K<sub>c</sub>(s+z<sub>c</sub>)/(s+p<sub>c</sub>):"),
                 eq(r"e(\infty)=\frac{1}{K_c\frac{z_c}{p_c}\cdot\frac{1}{2}}=0{,}2=\frac{1}{5}\ \Rightarrow\ K_c\frac{z_c}{p_c}=10", 14),
                 P("<b>2. Escolha polo e zero perto da origem:</b> com K<sub>c</sub> ≈ 1 ⇒ z<sub>c</sub> = 10p<sub>c</sub>. Adotando p<sub>c</sub> = 0,005 ⇒ z<sub>c</sub> = 0,05 (ambos ~7 vezes mais perto da origem que o polo dominante −0,3376)."),
                 P("<b>3. Verifique o efeito no polo dominante:</b> em s<sub>d</sub> = −0,3376 + j0,5623, o compensador contribui só −3,5° e módulo 0,97. Ótimo, quase nada."),
                 P("<b>4. Reajuste K<sub>c</sub> para manter ζ:</b> a nova FTMA é K<sub>c</sub>(s+0,05)/[(s+0,005)·s(s<super>2</super>+3s+2)], "
                   "com denominador s<super>4</super> + 3,005s<super>3</super> + 2,015s<super>2</super> + 0,01s. Pela condição de módulo no novo LGR, "
                   "<b>K<sub>c</sub> = 0,975</b> mantém ζ ≈ 0,515, com polos dominantes em <b>−0,317 ± j0,53</b> (exatamente o que está no quadro)."),
                 P("<b>5. Resultado:</b> K<sub>v</sub> = 0,975·10/2 = 4,875 ⇒ e(∞) = 0,205 ≈ 0,2 ✓. O transitório fica quase igual (Figura " + str(FN["atraso_exemplo"]) + "). "
                   "O preço: surge um polo de malha fechada lento em −0,055, perto do zero −0,05, que deixa uma \"cauda\" lenta pequena na resposta."),
                 fig("atraso_exemplo", 15, "Figura 11 – Com o atraso o degrau quase não muda, mas o erro à rampa cai de 2 para ~0,2."))
    S += [Paragraph("8.6 Avanço × atraso × PID", h2)]
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
    S.append(CondPageBreak(25 * cm))
    
    
    
    # ================= 9 acionamentos (Rashid) =================
    S += [H1("9. Parte de Acionamentos Elétricos: acionamentos CC e controle", "acion")]
    S += box("Parte de Acionamentos Elétricos", ["Este capítulo é da disciplina de <b>Acionamentos Elétricos</b>. A única base é o <b>Capítulo 14 – Acionamentos CC</b> do Rashid (<i>Eletrônica de Potência</i>), que você enviou. "
             "As equações e os exemplos levam o número do livro (Eq. 14.x, Exemplo 14.x). Todas as contas dos exemplos foram refeitas e conferem. "
             "O objetivo é <b>ligar cada parte do acionamento a um conceito de controle</b> deste guia."], "#fdf2e9", "#d35400")
    S += [Paragraph("9.1 Motor CC com excitação independente (seção 14.2.1)", h2),
          P("Campo e armadura têm alimentações separadas. As equações do motor são:")]
    S += B(["Campo: v<sub>f</sub> = R<sub>f</sub>i<sub>f</sub> + L<sub>f</sub>di<sub>f</sub>/dt", "Armadura: v<sub>a</sub> = R<sub>a</sub>i<sub>a</sub> + L<sub>a</sub>di<sub>a</sub>/dt + e<sub>g</sub>",
            "Força contraeletromotriz (fcem): e<sub>g</sub> = K<sub>v</sub>ωi<sub>f</sub>", "Torque desenvolvido: T<sub>d</sub> = K<sub>t</sub>i<sub>f</sub>i<sub>a</sub> (K<sub>t</sub> = K<sub>v</sub>)",
            "Mecânica: T<sub>d</sub> = J·dω/dt + Bω + T<sub>L</sub>"])
    S += [P("Em regime permanente (derivadas nulas), Eq. 14.7: <b>ω = (V<sub>a</sub> − R<sub>a</sub>I<sub>a</sub>)/(K<sub>v</sub>I<sub>f</sub>)</b>. A velocidade pode ser controlada pela tensão da armadura V<sub>a</sub> (abaixo da velocidade nominal, a <b>torque constante</b>), "
            "pela corrente de campo I<sub>f</sub> (acima da nominal, enfraquecimento de campo, a <b>potência constante</b>) ou pela demanda de torque (I<sub>a</sub>)."),
          P("<b>Leitura de controle:</b> V<sub>a</sub> é a <b>entrada de controle</b> (o atuador mexe nela), ω é a <b>saída</b> e o torque de carga T<sub>L</sub> é uma <b>perturbação</b>: pelo termo R<sub>a</sub>I<sub>a</sub>, carga maior derruba a velocidade. Sem realimentação, nada corrige isso.")]
    S += exemplo("Exemplo 14.1 (conferido)",
                 P("Motor de 15 hp, 220 V, 2000 rpm; carga de 45 N·m a 1200 rpm; R<sub>f</sub> = 147 Ω, R<sub>a</sub> = 0,25 Ω, K<sub>v</sub> = 0,7032, V<sub>f</sub> = 220 V. "
                   "I<sub>f</sub> = 220/147 = 1,497 A; ω = 125,66 rad/s; I<sub>a</sub> = 45/(0,7032 × 1,497) = <b>42,75 A</b>; E<sub>g</sub> = 0,7032 × 125,66 × 1,497 = <b>132,28 V</b>; "
                   "V<sub>a</sub> = 0,25 × 42,75 + 132,28 = <b>142,97 V</b>; corrente nominal 15 × 746/220 = <b>50,87 A</b>."))
    S += [Paragraph("9.2 Motor série e linearização (seções 14.2.2 e 14.7.3)", h2),
          P("No motor série, a mesma corrente passa pelo campo e pela armadura (i<sub>f</sub> = i<sub>a</sub>), então T<sub>d</sub> = K<sub>t</sub>i<sub>a</sub>² (Eq. 14.76): torque de partida muito alto, por isso é usado em tração. "
            "<b>Leitura de controle:</b> o produto i<sub>a</sub>² é <b>não linear</b> e a função de transferência não vale diretamente. O livro <b>lineariza em torno do ponto de operação</b> (I<sub>a0</sub>, ω<sub>0</sub>), "
            "escrevendo cada variável como valor de operação + pequena variação Δ e desprezando produtos de variações. Resultado: ΔT<sub>d</sub> = 2K<sub>v</sub>I<sub>a0</sub>Δi<sub>a</sub> (Eq. 14.81). "
            "É a técnica padrão para aplicar Laplace, LGR e Bode a sistemas não lineares: só vale para <b>pequenos desvios</b>."),
          Paragraph("9.3 O conversor como atuador (seções 14.6.1 e 14.7.4)", h2),
          P("<b>Conversor CC-CC</b> (o buck do seu trabalho): V<sub>a</sub> = k·V<sub>s</sub> (Eq. 14.32), com k o ciclo de trabalho. "
            "<b>Retificador controlado</b> monofásico ou trifásico: V<sub>a</sub> proporcional a cos α. Com α = cos<super>−1</super>(V<sub>c</sub>/V<sub>cm</sub>), a relação fica linear (Eq. 14.85 e 14.87)."),
          ]
    S += table([["Conversor", "Ganho K<sub>r</sub>", "Atraso τ<sub>r</sub>", "τ<sub>r</sub> com f<sub>s</sub> = 60 Hz"],
                ["CC-CC", "V<sub>s</sub>/V<sub>cm</sub> (k = V<sub>c</sub>/V<sub>cm</sub>)", "T<sub>s</sub>/2", "8,333 ms"],
                ["Monofásico", "0,9·V<sub>s</sub>/V<sub>cm</sub> (Eq. 14.86)", "T<sub>s</sub>/8", "2,083 ms"],
                ["Trifásico", "2,339·V<sub>s</sub>/V<sub>cm</sub> (Eq. 14.88)", "T<sub>s</sub>/12", "1,389 ms"]], [3, 5.4, 3, 5])
    S += [eq(r"G_r(s)=K_r\,e^{-s\tau_r}\approx\frac{K_r}{1+s\tau_r}\qquad \mathrm{(Eq.\ 14.89\ e\ 14.90)}"),
          P("<b>Leitura de controle:</b> o conversor é um <b>ganho</b> mais um <b>atraso de transporte</b>. Depois que uma chave liga, o comando só muda no próximo chaveamento. O atraso é aproximado por um <b>polo rápido</b> em −1/τ<sub>r</sub>, "
            "que soma atraso de fase e reduz as margens de estabilidade (capítulo 10).")]
    S += exemplo("Exemplo 14.8 (conferido) – motor alimentado por conversor CC-CC",
                 P("V<sub>s</sub> = 600 V, k = 0,6, R<sub>a</sub> = 0,05 Ω, K<sub>v</sub> = 1,527, I<sub>a</sub> = 250 A, I<sub>f</sub> = 2,5 A. P<sub>i</sub> = 0,6 × 600 × 250 = <b>90 kW</b>; "
                   "R<sub>eq</sub> = 600/(250 × 0,6) = <b>4 Ω</b>; V<sub>a</sub> = 360 V; E<sub>g</sub> = 360 − 0,05 × 250 = 347,5 V; ω = 347,5/(1,527 × 2,5) = <b>91,03 rad/s (869,3 rpm)</b>; "
                   "T<sub>d</sub> = 1,527 × 250 × 2,5 = <b>954,4 N·m</b>."))
    S += [Paragraph("9.4 Função de transferência em malha aberta (seção 14.7.2)", h2),
          P("Com o campo constante (K<sub>b</sub> = K<sub>v</sub>I<sub>f</sub>), as equações viram um modelo em <b>espaço de estados</b> (Eq. 14.57), com estados i<sub>a</sub> e ω e entradas v<sub>a</sub> e T<sub>L</sub> (capítulo 11):"),
          P("<font face='DejaVuSansMono'>A = [ −Rm/Lm   −Kb/Lm ;  Kb/J   −B/J ]      B = [ 1/Lm   0 ;  0   −1/J ]</font>"),
          P("Os autovalores de A (Eq. 14.60) são <b>sempre reais e negativos</b>: o livro conclui que <b>o motor é estável em malha aberta</b> (capítulo 3). Em Laplace, com condições iniciais nulas, "
            "aparecem as constantes de tempo <b>τ<sub>a</sub> = L<sub>m</sub>/R<sub>m</sub></b> (elétrica, da armadura) e <b>τ<sub>m</sub> = J/B</b> (mecânica):"),
          eq(r"\frac{\omega(s)}{V_r(s)}=\frac{K_2K_vI_f/(R_mB)}{s^2\tau_a\tau_m+s(\tau_a+\tau_m)+1+(K_vI_f)^2/(R_mB)}\quad\mathrm{(Eq.\ 14.68)}", 13),
          P("A resposta ao torque de carga (Eq. 14.69) tem o mesmo denominador e um <b>zero</b> em −1/τ<sub>a</sub>. Pelo teorema do valor final (s = 0), Eq. 14.70 e 14.71: Δω = K<sub>2</sub>K<sub>v</sub>I<sub>f</sub>ΔV<sub>r</sub>/[R<sub>m</sub>B + (K<sub>v</sub>I<sub>f</sub>)²] e Δω = −R<sub>m</sub>ΔT<sub>L</sub>/[R<sub>m</sub>B + (K<sub>v</sub>I<sub>f</sub>)²]."),
          ]
    S += box("Polos e zeros nesta parte", ["<b>2ª ordem, superamortecido</b> (dois polos reais). Com o motor do Exemplo 14.14 (R<sub>m</sub> = 6,5 Ω, L<sub>m</sub> = 67 mH, J = 0,06, B = 0,087, K<sub>b</sub> = 1,24): "
             "polos em <b>−5,64</b> (τ<sub>1</sub> = 0,18 s, dominante, ligado à mecânica) e <b>−92,8</b> (τ<sub>2</sub> = 0,0108 s, ligado à parte elétrica). Ganho estático de 0,59 (rad/s)/V. "
             "Sem polo na origem ⇒ <b>tipo 0</b>: com controle P sempre sobra erro de velocidade. A fcem (K<sub>b</sub>²) soma no denominador: é uma realimentação negativa interna que estabiliza (seção A.5). "
             "O Bode desse motor está na seção 10.1."], "#f3eefb", "#7d3c98")
    S += [Paragraph("9.5 Malha fechada de velocidade (seção 14.7.5, Exemplo 14.13)", h2),
          P("Um sensor de velocidade de ganho K<sub>1</sub> fecha a malha: V<sub>e</sub> = V<sub>r</sub> − K<sub>1</sub>ω. O denominador ganha o termo <b>K<sub>1</sub>K<sub>2</sub>K<sub>v</sub>I<sub>f</sub></b> (Eq. 14.92 a 14.95):"),
          eq(r"\Delta\omega=-\frac{R_m\,\Delta T_L}{R_mB+(K_vI_f)^2+K_1K_2K_vI_f}\quad\mathrm{(Eq.\ 14.95)}", 13),
          ]
    S += table([["Item do Ex. 14.13 (50 kW, 240 V, 1700 rpm)", "Resultado"],
                ["(a) torque nominal", "280,87 N·m"], ["(b) V<sub>a</sub> e V<sub>r</sub> para 1700 rpm", "V<sub>a</sub> = 230,98 V; V<sub>b</sub> = 16,912 V; V<sub>r</sub> = 19,222 V"],
                ["(c) velocidade com torque nominal (malha fechada)", "175,98 rad/s = 1680,5 rpm"], ["(d) torque 10% acima do nominal", "1678,5 rpm"],
                ["(e) referência 10% menor", "1530 rpm"], ["(f) (d) e (e) juntos (superposição)", "1508,5 rpm"],
                ["(g) regulação em malha aberta", "1537,7 rpm a plena carga: 10,55%"], ["(h) regulação em malha fechada", "1,16% (cerca de 10 vezes menor)"]], [8.4, 8])
    S += [P("<b>Leitura de controle:</b> (1) o termo novo no denominador é o <b>ganho de malha</b>, e dividir por (1 + ganho de malha) é a <b>redução de sensibilidade</b> da seção A.4; "
            "(2) o item (f) usa <b>superposição</b>, que só vale porque o modelo é linear (seção 1.0); (3) mesmo em malha fechada sobra erro porque o controle é <b>proporcional</b> e o motor é <b>tipo 0</b> (capítulo 4). Por isso os acionamentos reais usam PI."),
          Paragraph("9.6 Controle em cascata: malha de corrente dentro da de velocidade (seção 14.7.6)", h2),
          P("A malha interna de <b>corrente</b> responde a uma súbita demanda de torque e <b>limita a corrente</b> (o controlador de velocidade alimenta um limitador que gera a referência de corrente). A malha externa é a de <b>velocidade</b>. "
            "O livro <b>desacopla</b> a fcem movendo o bloco K<sub>b</sub> para a realimentação de I<sub>a</sub> (Figura 14.30). Assim, ω/V<sub>a</sub> = (ω/I<sub>a</sub>)·(I<sub>a</sub>/V<sub>a</sub>) (Eq. 14.96 a 14.100), com dois controladores <b>PI</b>:"),
          eq(r"G_c(s)=\frac{K_c(1+s\tau_c)}{s\tau_c}\qquad G_s(s)=\frac{K_s(1+s\tau_s)}{s\tau_s}\qquad G_\omega(s)=\frac{K_\omega}{1+s\tau_\omega}\quad\mathrm{(Eq.\ 14.101\ a\ 14.103)}", 12),
          P("<b>Leitura de controle:</b> cada PI acrescenta um polo na origem (erro zero) e um zero em −1/τ (que será <b>alocado</b>, seção 7.6). O tacogerador com filtro é um sensor de 1ª ordem."),
          Paragraph("9.7 Projeto do controlador de corrente (seção 14.7.7)", h2),
          P("Ganho de malha (Eq. 14.104): K<sub>m</sub>K<sub>c</sub>K<sub>r</sub>H<sub>c</sub>/τ<sub>c</sub> · (1 + sτ<sub>c</sub>)(1 + sτ<sub>m</sub>)/[s(1 + sτ<sub>1</sub>)(1 + sτ<sub>2</sub>)(1 + sτ<sub>r</sub>)]. O livro faz três simplificações:"),
          ]
    S += B(["1 + sτ<sub>m</sub> ≈ sτ<sub>m</sub>, porque τ<sub>m</sub> é grande: o zero lento quase cancela o integrador.",
            "<b>τ<sub>c</sub> = τ<sub>2</sub></b>: o zero do PI é <b>alocado sobre o polo</b> −1/τ<sub>2</sub>, que é <b>cancelado</b> (técnica de cancelamento, seção 7.6).",
            "O que sobra é um sistema de <b>2ª ordem</b>, K/[(1 + sτ<sub>1</sub>)(1 + sτ<sub>r</sub>)]. Escolhendo <b>ζ = 0,707</b> (sobressinal de 4,3%) sai K<sub>c</sub> = τ<sub>1</sub>τ<sub>c</sub>/(2τ<sub>r</sub>K<sub>m</sub>K<sub>r</sub>H<sub>c</sub>τ<sub>m</sub>) (Eq. 14.110)."])
    S += [Paragraph("9.8 Projeto do controlador de velocidade: ótimo simétrico (seção 14.7.8)", h2),
          P("A malha de corrente fechada é aproximada por <b>1ª ordem</b>: K<sub>i</sub>/(1 + sτ<sub>i</sub>) (Eq. 14.111). Os atrasos pequenos se somam num atraso equivalente τ<sub>e</sub> = τ<sub>i</sub> + τ<sub>ω</sub>. "
            "Anulando os coeficientes de ω² e ω⁴ do módulo do denominador (para alargar a <b>banda</b>, capítulo 10), resulta o <b>ótimo simétrico</b>:"),
          eq(r"K_s=\frac{1}{2K_\omega\tau_e}\qquad \tau_s=4\tau_e\qquad \frac{\omega}{\omega_r^*}=\frac{1}{K_\omega}\,\frac{1+4s\tau_e}{1+4s\tau_e+8s^2\tau_e^2+8s^3\tau_e^3}\quad\mathrm{(Eq.\ 14.121\ a\ 14.123)}", 12),
          P("Malha fechada de <b>3ª ordem com um zero</b> em −1/(4τ<sub>e</sub>). Resultado: t<sub>r</sub> = 3,1τ<sub>e</sub>, <b>sobressinal de 43,4%</b>, t<sub>s</sub> = 16,5τ<sub>e</sub>. "
            "O sobressinal alto vem do <b>zero</b> (seção 2.4). A solução do livro é uma <b>rede de compensação polo-zero</b> 1/(1 + 4sτ<sub>e</sub>) na referência, que cancela esse zero (Eq. 14.125): "
            "t<sub>r</sub> = 7,6τ<sub>e</sub>, <b>sobressinal de 8,1%</b>, t<sub>s</sub> = 13,3τ<sub>e</sub>. Conferi os três números das duas respostas por simulação. "
            "É a troca clássica: menos sobressinal custa mais tempo de subida."),
          fig("rashid_velocidade", 13.5, "Figura 0 – Malha de velocidade do Exemplo 14.14 com e sem a rede de compensação."),
          ]
    S += table([["Exemplo 14.14 (220 V, 6,4 A, 1570 rpm; trifásico 230 V, 60 Hz)", "Resultado conferido"],
                ["(a) ganho e atraso do conversor", "K<sub>r</sub> = 29,71 V/V; τ<sub>r</sub> = 1,39 ms"], ["(b) ganho da realimentação de corrente", "H<sub>c</sub> = 7,41/20 = 0,37 V/A"],
                ["(c) constantes do motor", "K<sub>m</sub> = 0,041; polos −5,64 e −92,83 ⇒ τ<sub>1</sub> = 0,18 s, τ<sub>2</sub> = 0,0108 s; τ<sub>m</sub> = 0,69 s"],
                ["(d) controlador de corrente", "τ<sub>c</sub> = τ<sub>2</sub> = 0,0108 s; K<sub>c</sub> = 2,19"],
                ["(e) malha de corrente simplificada", "K<sub>1</sub> = 63,88; K<sub>i</sub> = 2,66; τ<sub>i</sub> = 2,76 ms; τ<sub>e</sub> = 4,76 ms; K<sub>ω</sub> = 4,07"],
                ["(f) controlador de velocidade otimizado", "K<sub>s</sub> = 25,85; τ<sub>s</sub> = 19,02 ms"]], [7.4, 9])
    S += [P("<i>Nota:</i> numa linha do cálculo de K<sub>1</sub> o livro escreve \"0,4\" no lugar de K<sub>m</sub> = 0,04. É só erro de digitação: o resultado 63,88 confere com 0,041.")]
    S += [Paragraph("9.9 Conversor CC-CC em quatro quadrantes, PLL e microcontrolador (seções 14.7.9 a 14.7.11)", h2)]
    S += B(["<b>Quatro quadrantes</b> (ponte de IGBTs): para acelerar, T<sub>1</sub>/T<sub>4</sub>/D<sub>2</sub> funcionam como <b>buck</b> (v<sub>a</sub> = δV<sub>CC</sub>, Eq. 14.127). Na frenagem regenerativa, T<sub>2</sub>/D<sub>4</sub> funcionam como <b>boost</b> e devolvem energia à fonte. O controle escolhe o modo pelo sinal do erro de velocidade.",
            "<b>PLL</b> (malha sincronizada pela fase): a velocidade vira um trem de pulsos (encoder) e é comparada <b>em fase</b> com uma referência digital. É uma realimentação muito precisa: o livro cita regulação melhor que os 0,2% dos sensores analógicos.",
            "<b>Microcontrolador:</b> lê velocidade e corrente por conversor A/D, roda as malhas de corrente e de velocidade em software, gera os pulsos, protege e diagnostica. Isso é <b>controle digital</b> (capítulo 12): o PI vira equação de diferenças e o período de amostragem passa a contar na estabilidade."])
    S += [Paragraph("9.10 Mapa: conceito de controle × onde aparece no capítulo 14", h2)]
    S += table([["Conceito deste guia", "Onde aparece no Rashid"],
                ["Malha aberta × fechada, sensibilidade (A)", "14.7.5 e Ex. 14.13: regulação de 10,55% para 1,16%"],
                ["Realimentação negativa natural (A.5)", "a fcem K<sub>b</sub>ω, que torna o motor estável em malha aberta"],
                ["Linearização", "motor série, 14.7.3"], ["Espaço de estados (11)", "Eq. 14.57 a 14.60"],
                ["1ª ordem (2.4)", "conversor K<sub>r</sub>/(1 + sτ<sub>r</sub>); filtro do tacogerador; malha de corrente fechada"],
                ["2ª ordem (2.4)", "motor (τ<sub>a</sub>, τ<sub>m</sub>); malha de corrente com ζ = 0,707"],
                ["Ordem superior e efeito do zero (2.4)", "malha de velocidade de 3ª ordem: 43,4% → 8,1%"],
                ["Tipo e erro (4)", "motor tipo 0 ⇒ erro com P; o PI zera o erro"],
                ["Alocação de zeros (7.6)", "τ<sub>c</sub> = τ<sub>2</sub>; τ<sub>s</sub> = 4τ<sub>e</sub>; rede polo-zero na referência"],
                ["Bode e banda (10)", "ótimo simétrico (\"ampliar a largura de banda\"); cantos em 1/(4τ<sub>e</sub>) e 1/τ<sub>e</sub>"],
                ["Controle digital (12)", "acionamento com microcontrolador, 14.7.11"]], [6.6, 9.8])
    S += [Paragraph("9.11 Questões de revisão do capítulo 14 ligadas a controle", h2)]
    S += B(["<b>14.8 O que é regulação de velocidade?</b> (velocidade a vazio − velocidade a plena carga)/velocidade a plena carga. Mede a sensibilidade da velocidade ao torque de carga (10,55% em malha aberta no Ex. 14.13).",
            "<b>14.24 Qual é o princípio do controle em malha fechada?</b> Medir a velocidade, comparar com a referência e usar o erro para variar o ângulo de disparo ou o ciclo de trabalho, ajustando V<sub>a</sub> até o torque desenvolvido igualar o de carga.",
            "<b>14.25 Vantagens da malha fechada?</b> Maior precisão, resposta dinâmica rápida e menor efeito de perturbações de carga e de não linearidades.",
            "<b>14.26 e 14.27 PLL?</b> Comparar a fase dos pulsos do encoder com a referência digital. Dá regulação de velocidade muito fina e imune a desvios analógicos."])
    S += [P("<i>As questões da prova de Acionamentos que você mandou em outro chat não estão acessíveis daqui. Se reenviar, elas entram nesta parte.</i>")]
    S.append(CondPageBreak(25 * cm))
    
    
    # ================= 10 Nyquist =================
    S += [H1("10. Resposta em frequência: Bode e Nyquist", "nyq"),
          P("Outra forma de olhar o mesmo sistema: aplica-se uma senoide de frequência ω e mede-se quanto ela sai amplificada (|G(jω)|) e atrasada (∠G(jω)). "
            "O <b>Bode</b> desenha módulo (dB) e fase contra log ω. O <b>diagrama de Nyquist</b> desenha G(jω)H(jω) no plano complexo, com ω indo de −∞ a +∞."),
          H2k("10.1 Diagrama de Bode: o que é, o que representa fisicamente e como interpretar", "bode"),
          P("<b>O que é:</b> dois gráficos em função da frequência ω (em escala logarítmica). O de cima é o <b>módulo</b> |G(jω)| em decibéis (20·log<sub>10</sub>|G|). O de baixo é a <b>fase</b> ∠G(jω) em graus. "
            "Obtém-se trocando s por jω na função de transferência."),
          P("<b>O que representa fisicamente:</b> aplique na entrada uma senoide de frequência ω (por exemplo, faça a tensão da armadura oscilar 1 V em torno do ponto de operação). "
            "Depois do transitório, a saída (a velocidade) também oscila na <b>mesma frequência</b>, mas <b>multiplicada por |G(jω)|</b> e <b>atrasada</b> de ∠G(jω). "
            "O Bode é a tabela completa dessa experiência para todas as frequências. Por isso dá para levantá-lo <b>medindo</b>, sem conhecer o modelo."),
          fig("bode_fisico", 15.5, "Figura 0 – Motor do Rashid (Ex. 14.14) excitado com senoides: devagar, a velocidade acompanha; rápido demais, mal se mexe e fica atrasada."),
          fig("bode_motor", 13.5, "Figura 0 – Bode do mesmo motor. Cada polo dobra a curva para baixo (−20 dB/déc) e atrasa até 90°."),
          Paragraph("Como interpretar (leitura do Bode)", h3)]
    S += B(["<b>Patamar em baixa frequência = ganho estático</b> (o G(0) do regime permanente). No motor: 0,59 (rad/s)/V, ou −4,6 dB. Se o módulo sobe sem parar em baixa frequência (−20 dB/déc desde o início), há integrador: sistema tipo 1.",
            "<b>Frequências de canto = polos e zeros.</b> Cada polo em −a dobra o módulo para baixo em ω = a (−20 dB/década) e leva a fase até −90°. Cada zero dobra para cima (+20 dB/déc, +90°). "
            "No motor: canto em 5,64 rad/s (polo mecânico, τ<sub>1</sub> = 0,18 s) e em 92,8 rad/s (polo elétrico, τ<sub>2</sub> ≈ 0,01 s). Acima de 92,8 cai a −40 dB/déc.",
            "<b>Largura de banda</b> (onde o módulo cai 3 dB abaixo do patamar): até que frequência o sistema consegue acompanhar. Banda maior significa resposta mais rápida (t<sub>r</sub> ≈ 2/banda).",
            "<b>Atenuação em alta frequência = filtro.</b> O PWM do conversor CC-CC chaveia a vários kHz (mais de 10<super>4</super> rad/s). Nessa faixa o motor atenua mais de 100 dB: a velocidade não \"vê\" o chaveamento, só o valor médio. "
            "É por isso que o Rashid pode tratar o conversor como um ganho K<sub>r</sub>.",
            "<b>Pico de ressonância:</b> aparece com polos complexos de ζ &lt; 0,707. Fisicamente, é uma frequência em que a máquina vibra muito (ex.: eixo com acoplamento elástico).",
            "<b>Fase e estabilidade:</b> quanto mais atraso de fase onde |GH| = 1 (0 dB), mais perto da instabilidade. Isso dá as <b>margens de ganho e de fase</b> (10.3)."])
    S += P("<b>Esboço assintótico (à mão):</b> (1) escreva G na forma K·(1 + s/z)…/[(1 + s/p)…]; (2) trace o patamar 20·log K até o primeiro canto; (3) a cada polo, inclinação −20 dB/déc a mais; a cada zero, +20; "
           "(4) na fase, cada polo vale −45° no canto e −90° uma década depois; cada zero, +45° e +90°."),
    S += [Paragraph("10.2 O critério de Nyquist", h2),
          eq(r"Z=N+P"),
          P("<b>P</b> = polos de malha <b>aberta</b> no semiplano direito (você sabe pela FTMA). <b>N</b> = número de voltas, no sentido horário, que a curva de Nyquist dá em torno do ponto <b>−1</b>. "
            "<b>Z</b> = polos de malha <b>fechada</b> no semiplano direito. Estável ⇔ Z = 0. Se a malha aberta é estável (P = 0), basta a curva <b>não envolver o −1</b>."),
          P("<b>Por que o −1?</b> Os polos de malha fechada satisfazem 1 + GH = 0, ou seja, GH = −1. O −1 é a mesma condição de módulo 1 e ângulo 180° do LGR. "
            "Se em alguma frequência o sinal volta com ganho ≥ 1 e invertido (180°), a realimentação \"negativa\" vira positiva e a oscilação se sustenta ou cresce."),
          fig("nyquist", 15, "Figura 0 – Nyquist de K/[(s+1)(s+2)(s+3)]: cruza o eixo real em −K/60 (ω = √11). Instável para K &gt; 60, o mesmo resultado do Routh do Exercício 13.3."),
          Paragraph("10.3 Margens de ganho e de fase (estabilidade relativa)", h2),
          P("<b>Margem de ganho:</b> quanto o ganho pode ser multiplicado até instabilizar, medida na frequência em que a fase vale −180°. <b>Margem de fase:</b> quanto atraso extra de fase cabe, medido onde |GH| = 1 (0 dB). "
            "Para K = 30 no exemplo: margem de ganho = 60/30 = 2 (6 dB) e margem de fase ≈ 25°. Regra prática de projeto: margem de fase de 45° a 60° e margem de ganho &gt; 6 dB. A margem de fase se relaciona com o amortecimento: ζ ≈ (margem de fase)/100 para margens abaixo de 70°."),
          fig("bode_margens", 11),
          ]
    S += dica("Nyquist e LGR contam a mesma história: o K em que o Nyquist passa por −1 é o K em que o LGR cruza o eixo jω, e a frequência é a mesma. "
              "O Nyquist tem duas vantagens: funciona com atraso de transporte e<super>−sT</super> (que o LGR não trata bem) e com dados medidos de resposta em frequência.")
    S.append(CondPageBreak(25 * cm))
    
    
    # ================= 11 espaço de estados =================
    S += [H1("11. Espaço de estados e controle por realimentação de estados", "ss"),
          P("A função de transferência só relaciona entrada e saída. O <b>espaço de estados</b> descreve o que acontece <b>dentro</b>: um vetor x de variáveis de estado (posição, velocidade, corrente…) "
            "que resume toda a memória do sistema. Serve para múltiplas entradas e saídas, condições iniciais e projeto moderno."),
          eq(r"\dot x=Ax+Bu,\qquad y=Cx+Du"),
          Paragraph("11.1 Da EDO para estados (massa-mola)", h2),
          P("m·ẍ + b·ẋ + kx = F. Escolha x<sub>1</sub> = x (posição) e x<sub>2</sub> = ẋ (velocidade). Então ẋ<sub>1</sub> = x<sub>2</sub> e ẋ<sub>2</sub> = (F − kx<sub>1</sub> − bx<sub>2</sub>)/m. Com m = 1, b = 2, k = 2:"),
          P("<font face='DejaVuSansMono'>A = [ 0  1 ; −2  −2 ]     B = [ 0 ; 1 ]     C = [ 1  0 ]     D = 0</font>"),
          P("<b>Ligação com polos e FT:</b> G(s) = C(sI − A)<super>−1</super>B + D. Os <b>polos são os autovalores de A</b>: det(sI − A) = s² + 2s + 2 = 0 ⇒ −1 ± j (o mesmo do capítulo 1). "
            "O mesmo sistema tem infinitas representações em estados (depende da escolha de x), mas os autovalores, e portanto a estabilidade, são sempre os mesmos."),
          Paragraph("11.2 Controle: realimentação de estados e alocação de polos", h2),
          P("Se todos os estados são medidos, use <b>u = −Kx + N·r</b>. A malha fechada vira ẋ = (A − BK)x + BNr. Agora os polos são os autovalores de <b>A − BK</b>, e com K você pode colocá-los <b>onde quiser</b>, "
            "desde que o sistema seja <b>controlável</b>: posto da matriz [B  AB  …  A<super>n−1</super>B] igual a n."),
          ]
    S += exemplo("Exemplo – levar a massa-mola para polos em −4 ± j3",
                 P("Desejado: (s + 4)² + 9 = s² + 8s + 25. Com K = [k<sub>1</sub> k<sub>2</sub>]: A − BK = [[0, 1], [−2 − k<sub>1</sub>, −2 − k<sub>2</sub>]] ⇒ det = s² + (2 + k<sub>2</sub>)s + (2 + k<sub>1</sub>)."),
                 P("Igualando: 2 + k<sub>2</sub> = 8 ⇒ <b>k<sub>2</sub> = 6</b>; 2 + k<sub>1</sub> = 25 ⇒ <b>k<sub>1</sub> = 23</b>. Controlabilidade: [B AB] = [[0, 1], [1, −2]] tem posto 2 ✓."),
                 P("Ganho de referência: o ganho estático de malha fechada é C(−(A−BK))<super>−1</super>B·N = N/25 ⇒ <b>N = 25</b> para seguir r sem erro. "
                   "O resultado é ζ = 0,8, ω<sub>n</sub> = 5, sem sobressinal visível e t<sub>s</sub> ≈ 1 s, contra 4 s do sistema solto."),
                 fig("ss_resp", 12))
    S += B(["<b>Observador (estimador de estados):</b> quando nem todos os estados são medidos, estima-se x com x̂' = Ax̂ + Bu + L(y − Cx̂). Os polos de A − LC devem ser 2 a 5 vezes mais rápidos que os do controle. "
            "Exige <b>observabilidade</b>: posto de [C; CA; …] = n.",
            "<b>Erro zero com estados:</b> acrescente um integrador do erro como estado extra (equivale ao I do PID).",
            "<b>LQR:</b> em vez de escolher polos, minimiza um custo ∫(xᵀQx + uᵀRu)dt; o MATLAB devolve K com <font face='DejaVuSansMono'>lqr(A,B,Q,R)</font>.",
            "<b>MATLAB:</b> <font face='DejaVuSansMono'>sys=ss(A,B,C,D); eig(A); rank(ctrb(A,B)); K=place(A,B,[-4+3i -4-3i]); [num,den]=ss2tf(A,B,C,D)</font>."])
    S.append(CondPageBreak(25 * cm))
    
    
    # ================= 12 transformada Z =================
    S += [H1("12. Controle digital e transformada Z", "z"),
          P("Um microcontrolador (Arduino, CLP) não vê o sinal contínuo: ele <b>amostra</b> a cada T segundos, calcula e segura a saída até a próxima amostra (segurador de ordem zero, ZOH). "
            "Os sinais viram sequências x[k] = x(kT) e as equações diferenciais viram <b>equações de diferenças</b>. A transformada Z é a \"Laplace\" desse mundo."),
          Paragraph("12.1 O que é e como funciona", h2),
          eq(r"X(z)=\mathcal{Z}\{x[k]\}=\sum_{k=0}^{\infty}x[k]\,z^{-k},\qquad z=e^{sT}"),
          P("A propriedade-chave: <b>z<super>−1</super> é um atraso de uma amostra</b>. ℒ transforma derivada em s; Z transforma atraso em z<super>−1</super>. "
            "Assim y[k] − 0,5y[k−1] = u[k−1] vira Y(z)(1 − 0,5z<super>−1</super>) = z<super>−1</super>U(z) ⇒ G(z) = 1/(z − 0,5).")]
    S += table([["x[k]", "X(z)", "x[k]", "X(z)"],
                ["impulso δ[k]", "1", "a<super>k</super>", "z/(z − a)"],
                ["degrau 1", "z/(z − 1)", "e<super>−akT</super>", "z/(z − e<super>−aT</super>)"],
                ["rampa kT", "Tz/(z − 1)²", "x[k − n] (atraso)", "z<super>−n</super>X(z)"]], [3.4, 4.8, 3.4, 4.8])
    S += [Paragraph("12.2 Estabilidade no plano z", h2),
          P("Como z = e<super>sT</super>, o semiplano esquerdo (σ &lt; 0) vira o <b>interior do círculo unitário</b> (|z| = e<super>σT</super> &lt; 1). O eixo jω vira o próprio círculo, e s = 0 vira z = 1. "
            "Logo: <b>estável ⇔ todos os polos com |z| &lt; 1</b>. Um polo em z = a gera a<super>k</super>: decai se |a| &lt; 1. Se a for negativo, alterna o sinal a cada amostra (oscila na frequência de Nyquist). "
            "Para testar sem raízes existe o critério de Jury, ou substitui-se z = (1 + w)/(1 − w) e aplica-se Routh em w."),
          Paragraph("12.3 Como aplicar: discretizar a planta com ZOH", h2),
          eq(r"G(z)=(1-z^{-1})\,\mathcal{Z}\left\{\frac{G(s)}{s}\right\}"),
          ]
    S += exemplo("Exemplo – G(s) = 1/(s+1) com T = 0,1 s",
                 P("G(s)/s = 1/s − 1/(s+1) ⇒ Z: z/(z−1) − z/(z − e<super>−T</super>). Multiplicando por (z−1)/z: "
                   "<b>G(z) = (1 − e<super>−T</super>)/(z − e<super>−T</super>) = 0,0952/(z − 0,9048)</b>. O polo s = −1 foi para z = e<super>−0,1</super> = 0,9048."),
                 P("Equação de diferenças: y[k] = 0,9048·y[k−1] + 0,0952·u[k−1]."),
                 P("Malha fechada com ganho K: polo em z = 0,9048 − 0,0952K. Estável se |z| &lt; 1 ⇒ <b>K &lt; 20</b>. No contínuo, K/(s+1) é estável para <b>qualquer</b> K: "
                   "a amostragem e o segurador acrescentam atraso, e isso cria um limite. Com T = 0,5 s o limite cai para K &lt; 4,1."),
                 fig("z_discreto", 15))
    S += [Paragraph("12.4 Como fazer controle digital: o PID no Arduino", h2),
          P("Duas rotas. (1) <b>Projetar no contínuo e discretizar</b>, trocando s pela aproximação de Tustin s ≈ (2/T)(z − 1)/(z + 1), ou por Euler s ≈ (z − 1)/T. Funciona bem se T for pequeno: 10 a 20 amostras por tempo de subida. "
            "(2) <b>Projetar direto em z</b> (LGR no plano z, com o círculo unitário como fronteira)."),
          P("PID discreto (Euler, forma posicional): integral I[k] = I[k−1] + T·e[k]; derivada D[k] = (e[k] − e[k−1])/T; "
            "u[k] = K<sub>p</sub>e[k] + K<sub>i</sub>I[k] + K<sub>d</sub>D[k]. Depois sature u (ex.: PWM entre 0 e 255) e congele o integrador quando saturar (anti-windup)."),
          P("<font face='DejaVuSansMono'>e = r - y;  I += T*e;  D = (e - e_ant)/T;  u = Kp*e + Ki*I + Kd*D;  u = constrain(u, 0, 255);  e_ant = e;  analogWrite(pino, u);</font>"),
          ]
    S += dica("Transformada Z em prova: (1) discretize com segurador de ordem zero; (2) monte 1 + KG(z) = 0; (3) estável se |z| &lt; 1; (4) valor final: y(∞) = lim<sub>z→1</sub>(z − 1)Y(z). "
              "Polo em z = 1 é o integrador digital (tipo 1).")
    S.append(CondPageBreak(25 * cm))
    
    S += [H1("13. Exercícios resolvidos", "ex"), P("Cada resolução termina com um quadro <b>Polos e zeros nesta questão</b>, que diz o que cada polo e cada zero implica no comportamento do sistema.")]
    def ex(n, enun, *sol):
        out = [Paragraph(f"Exercício {n}", h3), P(f"<b>Enunciado:</b> {enun}")] + box("Resolução", list(sol), "#f6f6f6", "#555")
        for k, v in PZ.items():
            if k in n:
                out += box("Polos e zeros nesta questão", [v], "#f3eefb", "#7d3c98"); break
        return out
    S += ex("13.1 – Função de transferência e polos",
            "Um sistema é descrito por y'' + 4y' + 3y = 2u. Ache a FT, os polos, diga se é estável e qual o valor final ao degrau unitário.",
            P("Aplicando Laplace com condições iniciais nulas (sistema parado no instante zero): (s<super>2</super>+4s+3)Y = 2U ⇒ G(s) = 2/(s<super>2</super>+4s+3) = 2/[(s+1)(s+3)]."),
            P("Polos: −1 e −3, ambos reais negativos ⇒ <b>estável e sem oscilação</b> (superamortecido: ω<sub>n</sub> = √3 = 1,732; 2ζω<sub>n</sub> = 4 ⇒ ζ = 1,155 > 1)."),
            P("Valor final ao degrau: y(∞) = lim s·G(s)·(1/s) = G(0) = 2/3. O polo em −1 domina: t<sub>s</sub> ≈ 4 s."))
    S += ex("13.2 – Tipo e erros",
            "Para realimentação unitária com G(s) = 10(s+2)/[s(s+5)], classifique o tipo e calcule o erro ao degrau, à rampa e à parábola.",
            P("Um s na origem ⇒ <b>tipo 1</b>. (A malha fechada é estável: s<super>2</super> + 15s + 20 = 0 tem raízes negativas.)"),
            P("K<sub>p</sub> = ∞ ⇒ e<sub>degrau</sub> = 0. K<sub>v</sub> = lim s·G = 10·2/5 = 4 ⇒ e<sub>rampa</sub> = 1/4 = 0,25. K<sub>a</sub> = 0 ⇒ e<sub>parábola</sub> = ∞."))
    S += ex("13.3 – K máximo por Routh",
            "Para G(s) = K/[(s+1)(s+2)(s+3)] com realimentação unitária, ache a faixa de K para estabilidade e a frequência de oscilação no limite.",
            P("Eq. característica: s<super>3</super> + 6s<super>2</super> + 11s + 6 + K = 0."),
            table([["", "", ""], ["s³", "1", "11"], ["s²", "6", "6 + K"], ["s¹", "(66 − 6 − K)/6 = (60 − K)/6", "0"], ["s⁰", "6 + K", ""]], [2, 6, 3], head=False)[0],
            P("Estável se 60 − K > 0 e 6 + K > 0 ⇒ <b>−6 < K < 60</b> (para K > 0: K < 60). No limite, 6s<super>2</super> + 66 = 0 ⇒ s = ±j√11 = <b>±j3,317 rad/s</b>."))
    S += ex("13.4 – K para um ζ desejado",
            "Para G(s) = K/[s(s+4)], ache K para ζ = 0,707 e o tempo de acomodação resultante.",
            P("LGR: polos em 0 e −4. Saída do eixo em −2, e depois uma reta vertical em σ = −2. A reta ζ = 0,707 (45°) cruza a vertical em s<sub>d</sub> = −2 + j2."),
            P("Módulo: K = |s<sub>d</sub>|·|s<sub>d</sub>+4| = √8·√8 = <b>8</b>. Conferindo: s<super>2</super> + 4s + 8 = 0 ⇒ s = −2 ± j2 ✓. t<sub>s</sub>(2%) = 4/2 = <b>2 s</b>; M<sub>p</sub> ≈ 4,3%."))
    S += ex("13.5 – Erro ao degrau em sistema tipo 0",
            "G(s) = K/[(s+1)(s+3)]. Qual K dá erro ao degrau de 0,2? A malha fechada fica estável?",
            P("Tipo 0: K<sub>p</sub> = G(0) = K/3. e = 1/(1 + K/3) = 0,2 ⇒ 1 + K/3 = 5 ⇒ <b>K = 12</b>."),
            P("Malha fechada: s<super>2</super> + 4s + 3 + 12 = s<super>2</super> + 4s + 15 = 0 ⇒ s = −2 ± j3,317 ⇒ estável, ω<sub>n</sub> = 3,87, ζ = 0,516."))
    S += ex("13.6 – LGR com zero",
            "Esboce o LGR de G(s) = K(s+3)/[s(s+1)] e ache os pontos de saída e de chegada no eixo real.",
            P("Polos 0 e −1, zero −3. Eixo real: [−1, 0] e (−∞, −3]. n − m = 1 ⇒ uma assíntota a 180°."),
            P("K = −s(s+1)/(s+3); dK/ds = 0 ⇒ s<super>2</super> + 6s + 3 = 0 ⇒ s = −0,551 (saída, K = 0,101) e s = −5,449 (chegada, K = 9,90)."),
            P("Entre esses pontos o LGR é um <b>círculo</b> centrado no zero (−3) com raio √6 = 2,449. Esse é um resultado clássico para 2 polos + 1 zero reais. "
              "O sistema é estável para todo K > 0."))
    S.append(CondPageBreak(25 * cm))
    
    S += [CondPageBreak(10 * cm), Paragraph("Exercícios das suas listas (conferidos)", h2),
          P("Os enunciados abaixo vêm das suas anotações. As contas foram refeitas numericamente. Onde algo diverge do caderno, está indicado.")]
    S += ex("13.7 – Routh de 4ª ordem (instável)",
            "G(s) = 2/[s(s+3)] · 10/(s+1)², com realimentação unitária. O sistema em malha fechada é estável?",
            P("FTMA = 20/[s(s+3)(s+1)²]. Equação característica: s(s+3)(s<super>2</super>+2s+1) + 20 = <b>s<super>4</super> + 5s<super>3</super> + 7s<super>2</super> + 3s + 20 = 0</b>."),
            table([["s⁴", "1", "7", "20"], ["s³", "5", "3", "0"], ["s²", "(5·7 − 1·3)/5 = 6,4", "20", ""], ["s¹", "(6,4·3 − 5·20)/6,4 = −12,625", "0", ""], ["s⁰", "20", "", ""]], [2, 7, 2.5, 2.5], head=False)[0],
            P("Primeira coluna: +1, +5, +6,4, <b>−12,625</b>, +20. Há <b>2 trocas de sinal</b>, ou seja, 2 polos no semiplano direito: <b>instável</b>."))
    S += ex("13.8 – Faixa de K",
            "G(s) = K/(s<super>3</super> + 4s<super>2</super> + 12s − 3). Para quais K a malha fechada é estável?",
            P("Equação característica: s<super>3</super> + 4s<super>2</super> + 12s + (K − 3) = 0. A planta sozinha é instável (o termo −3 indica um polo positivo); a realimentação é que estabiliza."),
            table([["s³", "1", "12"], ["s²", "4", "K − 3"], ["s¹", "(48 − (K − 3))/4 = (51 − K)/4", "0"], ["s⁰", "K − 3", ""]], [2, 7, 3], head=False)[0],
            P("Precisa de K − 3 > 0 e 51 − K > 0 ⇒ <b>3 &lt; K &lt; 51</b>. Em K = 51: 4s<super>2</super> + 48 = 0 ⇒ oscila em ω = √12 = 3,46 rad/s."))
    S += ex("13.9 – LGR passo a passo de K(s+1)/(s⁴+9s³+26s²+24s)",
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
    S += ex("13.10 – Zeros no semiplano direito: KG = K(s−2)²/[(s−1)(s²+2s+2)]",
            "Ache polos e zeros e verifique se algum K > 0 estabiliza.",
            P("Zeros: (s−2)<super>2</super> = 0 ⇒ s = 2 (duplo). Polos: s = 1 e s<super>2</super>+2s+2 = 0 ⇒ Δ = 4 − 8 = −4 ⇒ s = −1 ± j. São 3 polos e 2 zeros ✓."),
            P("Equação característica: (s−1)(s<super>2</super>+2s+2) + K(s−2)<super>2</super> = <b>s<super>3</super> + (1+K)s<super>2</super> − 4Ks + (4K − 2) = 0</b>. "
              "O coeficiente de s é <b>−4K &lt; 0</b> para todo K > 0. Pela condição necessária de Routh (todos os coeficientes com o mesmo sinal), "
              "<b>nenhum K > 0 estabiliza</b>. O zero duplo em +2 prende sempre um polo no semiplano direito."),
            fig("lgr_B", 11))
    S += ex("13.11 – Ângulo de partida: K/[(s²+s)(s²+4s+13)]",
            "Ache assíntotas, ponto de saída, cruzamento do eixo jω e ângulo de partida dos polos complexos.",
            P("Polos: 0, −1 e s<super>2</super>+4s+13 = 0 ⇒ Δ = 16 − 52 = −36 ⇒ <b>−2 ± j3</b>. Sem zeros: 4 assíntotas a ±45° e ±135°; σ<sub>a</sub> = (0 − 1 − 2 − 2)/4 = <b>−1,25</b> ✓."),
            P("Equação característica: <b>s<super>4</super> + 5s<super>3</super> + 17s<super>2</super> + 13s + K = 0</b>. Saída do eixo real: 4s<super>3</super> + 15s<super>2</super> + 34s + 13 = 0 ⇒ s = −0,466 (K = 2,83)."),
            table([["s⁴", "1", "17", "K"], ["s³", "5", "13", "0"], ["s²", "(85 − 13)/5 = 14,4", "K", ""], ["s¹", "(187,2 − 5K)/14,4", "0", ""], ["s⁰", "K", "", ""]], [2, 6, 2.5, 2.5], head=False)[0],
            P("Estável se 0 &lt; K &lt; 187,2/5 = <b>37,44</b> ✓ (igual ao caderno). Na linha s²: 14,4s<super>2</super> + 37,44 = 0 ⇒ cruza em <b>±j1,61</b>."),
            P("<b>Partida de −2 + j3:</b> ângulos dos outros polos até ele: de 0 → 123,7°; de −1 → 108,4°; de −2 − j3 → 90°. "
              "θ<sub>part</sub> = 180° − (123,7 + 108,4 + 90) = <b>−142,1°</b>."),
            fig("lgr_C", 10.5))
    S += ex("13.12 – Controlador proporcional: 1/[s(s+20)] com POS = 31,5% e t<sub>s</sub> = 0,4 s",
            "Projete um controlador P que atenda às duas especificações.",
            eq(r"\zeta=\frac{-\ln(0{,}315)}{\sqrt{\pi^2+\ln^2(0{,}315)}}=0{,}345\qquad t_s=\frac{4}{\zeta\omega_n}=0{,}4\Rightarrow\zeta\omega_n=10", 13),
            P("ω<sub>n</sub> = 10/0,345 = 28,99 rad/s e ω<sub>d</sub> = 28,99·√(1 − 0,345<super>2</super>) = 27,2 ⇒ <b>s<sub>d</sub> = −10 ± j27,2</b>."),
            P("O LGR de K/[s(s+20)] sai do eixo em dK/ds = −(2s + 20) = 0 ⇒ s = −10 e sobe na vertical σ = −10 (assíntotas ±90°, σ<sub>a</sub> = −10). "
              "O ponto desejado <b>está no LGR</b>, então só o ganho resolve (\"o proporcional só desloca os polos sobre o LGR\"). Ângulos: 110,18° + 69,82° = 180° ✓."),
            P("Módulo: K = |s<sub>d</sub>|·|s<sub>d</sub> + 20| = 28,99 · 28,99 = <b>K ≈ 840</b> ✓."),
            fig("lgr_D", 9))
    S += ex("13.13 – P e depois PID para 1/[(s+1)(s+3)(s+5)]",
            "(a) Controlador P com ζ = 0,2. (b) PID (avanço-atraso) para ficar 3,5× mais rápido, com overshoot 2× menor, erro nulo e deslocamento de −2° no polo dominante.",
            P("<b>(a)</b> Na reta ζ = 0,2, a condição de ângulo dá s<sub>d</sub> = −0,702 + j3,44 (85,1° + 56,3° + 38,7° = 180,1° ✓). "
              "K = 3,45·4,14·5,51 = <b>78,7</b> ✓. Então t<sub>s</sub> = 4/0,702 = 5,70 s, sobressinal = 52,6%, e o erro ao degrau é 1/(1 + 78,7/15) = 16% (tipo 0)."),
            P("<b>(b)</b> t<sub>s</sub>' = 5,698/3,5 = 1,628 s ⇒ σ' = 4/1,628 = 2,457. sobressinal' = 26,3% ⇒ ζ' = 0,391 ⇒ ω<sub>d</sub>' = 5,78 ⇒ <b>s<sub>d</sub>' = −2,457 + j5,78</b> ✓."),
            P("Ângulo da planta em s<sub>d</sub>': −255,0° ⇒ faltam <b>75,0°</b>. Como o PI vai \"roubar\" 2°, o PD precisa dar 77,0°: tan 77,0° = 5,78/(z − 2,457) ⇒ <b>z<sub>PD</sub> = 3,79</b>."),
            P("PI: o zero z<sub>PI</sub> e o polo na origem devem somar −2° em s<sub>d</sub>' ⇒ <b>z<sub>PI</sub> = 0,235</b>. Módulo ⇒ <b>K = 37,4</b>:"),
            eq(r"C(s)=37{,}4\,\frac{(s+3{,}79)(s+0{,}235)}{s}\ \Rightarrow\ K_d=37{,}4,\ K_p=150,\ K_i=33{,}2", 13),
            P("Polos de malha fechada: −2,457 ± j5,78 ✓, −3,87 e −0,218. Este último fica colado no zero −0,235 e deixa uma cauda lenta: a saída chega a ~98,7% rápido e só então vai a 100%. O sobressinal simulado é ~19% (abaixo de 26,3% ✓)."),
            fig("ex_pid_E", 12))
    S += ex("13.14 – Avanço de fase: 200/[(s+10)(s+30)] duas vezes mais rápido",
            "A malha fechada atual tem polos em −20 ± j10. Projete um avanço para ficar 2× mais rápido mantendo o overshoot.",
            P("Malha fechada: s<super>2</super> + 40s + 300 + 200 = s<super>2</super> + 40s + 500 ⇒ −20 ± j10. Mesmo ζ (mesmo ângulo) e 2× mais rápido ⇒ <b>s<sub>d</sub> = −40 ± j20</b>."),
            P("Ângulos em s<sub>d</sub>: polo −10 → 180° − arctan(20/30) = 146,31°; polo −30 → 180° − arctan(20/10) = 116,57°. Soma 262,88° ⇒ deficiência <b>82,88°</b>."),
            P("Zero <b>sobre o polo −10</b> (cancela): contribui 146,31°. O polo precisa contribuir 146,31 − 82,88 = 63,43° ⇒ tan 63,43° = 2 = 20/(p − 40) ⇒ <b>p = 50</b> ✓."),
            P("Ganho: |s<sub>d</sub> + 30| = |s<sub>d</sub> + 50| = 22,36 ⇒ 200K<sub>c</sub> = 22,36² = 500 ⇒ <b>K<sub>c</sub> = 2,5</b>. C(s) = 2,5(s+10)/(s+50). "
              "Malha fechada: s<super>2</super> + 80s + 2000 ⇒ −40 ± j20 ✓."),
            P("Efeito colateral: K<sub>p</sub> caiu de 200/300 = 0,67 para 500/1500 = 0,33 e o erro ao degrau subiu de 60% para 75%. "
              "O avanço resolve o transitório, não o erro. Para o erro seria preciso adicionar atraso ou PI."))
    S += ex("13.15 – PID para K/(s²+5s+4) com ζ = 0,8 e t<sub>p</sub> = 1,047 s",
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
    S += [H1("14. Exercícios propostos (gabarito no fim)", "prop")]
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
        "Routh dá estabilidade só para K < 6; com K = 10 a malha fechada é instável e o teorema do valor final nem vale. Daí a necessidade do atraso.",
        "β ≈ 10 (K<sub>v</sub> original = 0,53): por exemplo G<sub>c</sub> = K<sub>c</sub>(s+0,05)/(s+0,005), com K<sub>c</sub> ≈ 0,9–1, reajustado pela condição de módulo no polo dominante (≈ −0,31 ± j0,55). Erro à rampa ≈ 0,2.",
        "O integrador soma um polo na origem: o tipo sobe de 0 para 1 e o erro ao degrau vai a zero (desde que a malha fechada continue estável)."]
    for i, t in enumerate(gab, 1):
        S.append(Paragraph(t, ParagraphStyle("gb", parent=body, leftIndent=20, fontSize=10, leading=13.5), bulletText=f"P{i}."))
    S.append(CondPageBreak(25 * cm))
    
    
    # ================= 9 formulário =================
    S += [H1("15. Formulário de bolso e comandos do MATLAB", "form")]
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
                ["Deficiência angular", "φ = −180° − ∠G(s<sub>d</sub>)  (>0 ⇒ avanço)"],
                ["Nyquist", "Z = N + P; estável ⇔ Z = 0 (não envolver −1 se P = 0)"],
                ["Estados", "polos = autovalores de A; com u = −Kx: autovalores de A − BK"],
                ["Transformada Z", "z = e<super>sT</super>; estável ⇔ |z| &lt; 1; G(z) = (1 − z<super>−1</super>)Z{G(s)/s}"],
                ["Motor CC", "Ω/V<sub>a</sub> = K/[(L<sub>a</sub>s+R<sub>a</sub>)(Js+B)+K²]"]], [4.2, 12.2])
    S += [Paragraph("Comandos do MATLAB usados em aula", h2)]
    S += table([["Comando", "O que faz"],
                ["P=[1]; Q=[1 3 2 0];", "numerador e denominador da FTMA (coeficientes em potências decrescentes de s)"],
                ["roots([1 3 2 1])", "raízes da equação característica (polos de malha fechada)"],
                ["rlocus(P,Q)", "desenha o LGR"],
                ["[K,p]=rlocfind(P,Q)", "clique no LGR: devolve K e os polos naquele ponto"],
                ["step(P,Q)", "resposta ao degrau"],
                ["hold / figure(2)", "sobrepor gráficos / abrir nova janela"],
                ["G=tf(P,Q); T=feedback(G,1)", "cria a FT e fecha a malha unitária"],
                ["sgrid(0.5,[])", "desenha a reta de ζ=0,5 sobre o LGR"]], [6.2, 10.2])
    S += dica("Na prova: escreva sempre a FTMA, a equação característica, o tipo e a entrada antes de calcular qualquer coisa. "
              "Metade da nota costuma estar em montar o problema certo.")
    
    return S

PAGECH = {}
PREV = json.load(open("pages.json")) if os.path.exists("pages.json") else {}
for it in range(2):
    KEYS.clear(); PAGECH.clear(); FN_RESET = True
    make("Teoria_de_Controle_Guia_de_Estudo.pdf").build(story())
    json.dump(KEYS, open("pages.json", "w"))
    if KEYS == PREV: break
    PREV = dict(KEYS)
print("ok", KEYS)

import re
src = open("build.py", encoding="utf-8").read()
exec(open("newsecs.py", encoding="utf-8").read())
exec(open("newsecs2.py", encoding="utf-8").read())

def cut(a, b=None):
    i = src.index(a); j = src.index(b) if b else len(src)
    return src[i:j]
M = lambda t: f"# ================= {t} ================="
head = src[:src.index(M("CAPA"))]
capa = cut(M("CAPA"), 'S += [Paragraph("Sumário", h1)]')
mapa = cut(M("0"), M("A amp-op"))
ampop = cut(M("A amp-op"), M("1 FT"))
ft = cut(M("1 FT"), M("2 polos zeros"))
polos = cut(M("2 polos zeros"), M("3 tipo e erro"))
erro = cut(M("3 tipo e erro"), M("4 LGR"))
lgr = cut(M("4 LGR"), M("5 achar K"))
kk = cut(M("5 achar K"), M("6 compensadores"))
comp = cut(M("6 compensadores"), M("7 exercícios resolvidos"))
ctrl = cut(M("7 exercícios resolvidos"), 'S += [Paragraph("7. Exercícios resolvidos", h1)]')
ex = cut('S += [Paragraph("7. Exercícios resolvidos", h1)]', M("8 propostos"))
prop = cut(M("8 propostos"), M("9 formulário"))
form = cut(M("9 formulário"), M("build"))

def R(s, a, b, n=1):
    assert s.count(a) >= 1, a[:60]
    return s.replace(a, b)

# ---- head: keys, H1, H2k
head += r'''
KEYS = {}
def H1(text, key):
    p = Paragraph(text, h1); p._key = key; return p
def H2k(text, key):
    p = Paragraph(text, h2); p._key = key; return p
'''
capa = CAPA_NOVA
capa += r'''
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
'''
mapa = R(mapa, 'Paragraph("0. Como encarar a matéria (o mapa)", h1)', 'H1("0. Como encarar a matéria (o mapa)", "mapa")')
mapa = mapa.replace('S.append(CondPageBreak(25 * cm))', 'S.append(CondPageBreak(12 * cm))')
ampop = R(ampop, 'Paragraph("A. Amplificador operacional: o controle em forma de circuito", h1)', 'H1("C. Amplificador operacional: o controle em forma de circuito", "ampop")')
for a_, b_ in [('"A.1 O que é"', '"C.1 O que é"'), ('"A.2 As duas regras', '"C.2 As duas regras'), ('"A.3 Inversor', '"C.3 Inversor'), ('"A.4 Não inversor', '"C.4 Não inversor'), ('"A.5 Cada ação', '"C.5 Cada ação')]:
    ampop = ampop.replace(a_, b_)
ampop = ampop.replace("Antes das contas, vale entender", "Com malha e impedância em mãos, vale entender")
ampop = R(ampop, "atraso e avanço de fase (seção 6)", "atraso e avanço de fase (seções 7 e 8)")
ft = R(ft, 'Paragraph("1. Laplace, função de transferência e diagramas de blocos", h1)', 'H1("1. Laplace, função de transferência e diagramas de blocos", "ft")')
ft = R(ft, 'Paragraph("1.4 FTMA, FTMF e equação característica", h2)', 'H2k("1.4 FTMA, FTMF e equação característica", "ftma")')
# ft: remove old 1.3 (moved to A) and renumber
_i = ft.index('S += [CondPageBreak(9 * cm), Paragraph("1.3 Malha aberta × malha fechada: a ideia", h2),')
_j = ft.index('      CondPageBreak(9 * cm), H2k("1.4 FTMA, FTMF e equação característica", "ftma"),')
ft = ft[:_i] + "S += [\n" + ft[_j:]
ft = ft.replace('H2k("1.4 FTMA, FTMF e equação característica", "ftma")', 'H2k("1.3 FTMA, FTMF e equação característica (malha fechada em fórmulas)", "ftma")')
ft = ft.replace('Paragraph("1.5 Diagramas de blocos, redução e Mason", h2)', 'Paragraph("1.4 Diagramas de blocos, redução e Mason", h2)')
polos = R(polos, 'Paragraph("2. Polos, zeros e a resposta do sistema", h1)', 'H1("2. Polos, zeros e a resposta do sistema", "polos")')
polos = R(polos, 'Paragraph("2.1 Sistemas de 2ª ordem: ζ, ω<sub>n</sub>, ω<sub>d</sub>", h2)', 'H2k("2.1 Sistemas de 2ª ordem: ζ, ω<sub>n</sub>, ω<sub>d</sub>", "zeta")')
polos = polos.rstrip()
assert polos.endswith("S.append(CondPageBreak(25 * cm))")
polos = polos[: -len("S.append(CondPageBreak(25 * cm))")] + GLOSS + "\nS.append(CondPageBreak(25 * cm))\n\n"

erro = R(erro, 'S += [Paragraph("3. Tipo do sistema e erro em regime permanente", h1),', 'S += [H1("4. Tipo do sistema e erro em regime permanente", "erro"),')
erro = R(erro, '"3.1 O que é o \\"tipo\\""', '"4.1 O que é o \\"tipo\\""')
erro = R(erro, '"3.2 Constantes de erro e tabela"', '"4.2 Constantes de erro e tabela"')
erro = R(erro, "compensador de atraso da seção 6", "compensador de atraso da seção 8")

lgr = R(lgr, 'S += [Paragraph("4. Lugar das raízes (LGR)", h1),', 'S += [H1("5. Lugar das raízes (LGR)", "lgr"),')
lgr = R(lgr, '      Paragraph("4.1 Regras de construção", h2)]', LGRB)
lgr = R(lgr, 'Paragraph("4.2 Exemplo completo', 'Paragraph("5.3 Exemplo completo')
lgr = R(lgr, "Condição de módulo (seção 5)", "Condição de módulo (seção 6)") if "Condição de módulo (seção 5)" in lgr else lgr
lgr = lgr.replace("condição de módulo (seção 5)", "condição de módulo (seção 6)").replace("Exemplo no Exercício 7.11", "Exemplo no Exercício 13.11")

kk = R(kk, 'S += [Paragraph("5. Como achar o K", h1),', 'S += [H1("6. Como achar o K", "k"),')
kk = kk.replace("Exemplo 5.1", "Exemplo 6.1").replace("Exemplo 5.2", "Exemplo 6.2").replace("pelo Routh da seção 4", "pelo Routh (seções 3.5 e 5.3)")

comp = R(comp, 'S += [Paragraph("6. Compensadores e controladores: avanço, atraso, PID e on-off", h1),', 'S += [H1("8. Compensadores: avanço e atraso de fase", "comp"),')
for i in range(1, 7): comp = comp.replace(f'"6.{i} ', f'"8.{i} ')
comp = comp.replace("Exemplo 6.1", "Exemplo 8.1").replace("Exemplo 6.2", "Exemplo 8.2").replace("Exemplo 6.3", "Exemplo 8.3").replace("do Exemplo 6.2", "do Exemplo 8.2")
comp = comp.rstrip() + "\nS.append(CondPageBreak(25 * cm))\n\n"

ctrl = ctrl.replace(M("7 exercícios resolvidos"), "")
ctrl = R(ctrl, 'Paragraph("6.7 PID: o que é, com exemplos de P, I e D", h2)', 'H2k("7.3 PID: o que é, com exemplos de P, I e D", "pid")')
ctrl = R(ctrl, '"6.8 Ações P, I e D em detalhe"', '"7.4 Ações P, I e D em detalhe"')
ctrl = R(ctrl, '"6.9 Controlador on-off (liga-desliga)"', '"7.5 Controlador on-off (liga-desliga)"')
ctrl = CTRL_HEAD + ctrl.replace("S.append(CondPageBreak(25 * cm))", "").rstrip() + "\nS.append(CondPageBreak(25 * cm))\n\n"

ex = R(ex, 'S += [Paragraph("7. Exercícios resolvidos", h1)]', 'S += [H1("13. Exercícios resolvidos", "ex"), P("Cada resolução termina com um quadro <b>Polos e zeros nesta questão</b>, que diz o que cada polo e cada zero implica no comportamento do sistema.")]')
ex = re.sub(r'ex\("7\.(\d+) –', lambda m: f'ex("13.{m.group(1)} –', ex)
ex = R(ex, "def ex(n, enun, *sol):\n    return [Paragraph(f\"Exercício {n}\", h3), P(f\"<b>Enunciado:</b> {enun}\")] + box(\"Resolução\", list(sol), \"#f6f6f6\", \"#555\")",
       "def ex(n, enun, *sol):\n    out = [Paragraph(f\"Exercício {n}\", h3), P(f\"<b>Enunciado:</b> {enun}\")] + box(\"Resolução\", list(sol), \"#f6f6f6\", \"#555\")\n"
       "    for k, v in PZ.items():\n        if k in n:\n            out += box(\"Polos e zeros nesta questão\", [v], \"#f3eefb\", \"#7d3c98\"); break\n    return out")
ex = ex.replace("o mesmo resultado do Routh do Exercício 13.3", "o mesmo resultado do Routh do Exercício 13.3")

prop = R(prop, 'S += [Paragraph("8. Exercícios propostos (gabarito no fim)", h1)]', 'S += [H1("14. Exercícios propostos (gabarito no fim)", "prop")]')
form = R(form, 'S += [Paragraph("9. Formulário de bolso e comandos do MATLAB", h1)]', 'S += [H1("15. Formulário de bolso e comandos do MATLAB", "form")]')
form = R(form, '["Deficiência angular", "φ = −180° − ∠G(s<sub>d</sub>)  (>0 ⇒ avanço)"]]',
         '["Deficiência angular", "φ = −180° − ∠G(s<sub>d</sub>)  (>0 ⇒ avanço)"],\n            ["Nyquist", "Z = N + P; estável ⇔ Z = 0 (não envolver −1 se P = 0)"],\n            ["Estados", "polos = autovalores de A; com u = −Kx: autovalores de A − BK"],\n            ["Transformada Z", "z = e<super>sT</super>; estável ⇔ |z| &lt; 1; G(z) = (1 − z<super>−1</super>)Z{G(s)/s}"],\n            ["Motor CC", "Ω/V<sub>a</sub> = K/[(L<sub>a</sub>s+R<sub>a</sub>)(Js+B)+K²]"]]')

build = r'''
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
'''

_i = MALHA.index('      Paragraph("A.4 Exemplo numérico: o motor com carga", h2),'); _j = MALHA.index('S += table([["", "Malha aberta", "Malha fechada"],')
MALHA = MALHA[:_i] + A4_RASHID + MALHA[_j:]
MALHA = MALHA.replace('S += dica("A pergunta-chave', REALPOS + '\nS += dica("A pergunta-chave')
mapa = mapa.replace('S += dica("Em toda questão, escreva primeiro a <b>FTMA</b>', SIGLAS + '\nS += dica("Em toda questão, escreva primeiro a <b>FTMA</b>')
ft = ft.replace('Paragraph("1.0 Transformada de Laplace: a ferramenta", h2),', 'Paragraph("1.0 A variável s e a transformada de Laplace", h2),\n' + S_INTRO)
_p = polos.rindex("S.append(CondPageBreak(25 * cm))"); polos = polos[:_p] + TRANSIT + "\n" + polos[_p:]
_p = ctrl.rindex("S.append(CondPageBreak(25 * cm))"); ctrl = ctrl[:_p] + ALOC_ZN + "\n" + ctrl[_p:]
NYQ2 = NYQ.replace('H1("10. Resposta em frequência e critério de Nyquist", "nyq")', 'H1("10. Resposta em frequência: Bode e Nyquist", "nyq")').replace('      Paragraph("10.1 O critério de Nyquist", h2),', BODE).replace('Paragraph("10.2 Margens de ganho e de fase (estabilidade relativa)", h2)', 'Paragraph("10.3 Margens de ganho e de fase (estabilidade relativa)", h2)')
assert NYQ2 != NYQ
body_parts = [mapa, MALHA, IMPED, ampop, ft, polos, ESTAB, erro, lgr, kk, ctrl, comp, ACION_R, NYQ2, SS, ZT, ex, prop, form]
story_fn = "def story():\n    global S\n    S = []\n" + "\n".join("    " + l for l in (capa + "\n".join(body_parts)).splitlines()) + "\n    return S\n"
main = r'''
PAGECH = {}
PREV = json.load(open("pages.json")) if os.path.exists("pages.json") else {}
for it in range(2):
    KEYS.clear(); PAGECH.clear(); FN_RESET = True
    make("Teoria_de_Controle_Guia_de_Estudo.pdf").build(story())
    json.dump(KEYS, open("pages.json", "w"))
    if KEYS == PREV: break
    PREV = dict(KEYS)
print("ok", KEYS)
'''
out = head + "\nPZ = " + repr(PZ) + "\n" + build + story_fn + main
for _a, _b in TEXT_FIX + [("A MF fica estável", "A malha fechada fica estável"), ('P("MF: ', 'P("Malha fechada: '), ('"MF: s<super>2</super> + 80s', '"Malha fechada: s<super>2</super> + 80s')]:
    out = out.replace(_a, _b)
open("build2.py", "w", encoding="utf-8").write(out)
print("written", len(out))

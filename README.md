# Teoria de Controle – guia de estudo

Material de estudo de Teoria de Controle (Engenharia de Controle e Automação, UFOP), montado a partir das aulas e das listas.

- **`Teoria_de_Controle_Guia_de_Estudo.pdf`**: guia para imprimir. Cobre amplificador operacional, Laplace, função de transferência, diagramas de blocos e Mason, polos e zeros, tipo e erro em regime, lugar das raízes, como achar o K, avanço e atraso de fase, PID (com exemplos de P, I e D), controlador on-off e exercícios resolvidos e propostos.
- **`docs/index.html`**: site interativo. Tem polo arrastável no plano s, ζ e ωn, 1ª ordem, ganho K, erro × tipo, PID, on-off, amp-op, avanço/atraso e um **simulador de lugar das raízes passo a passo**. Abra o arquivo no navegador ou ative o GitHub Pages na pasta `docs/`.
- **`src/`**: scripts Python que geram as figuras e o PDF (matplotlib, scipy, reportlab) e conferem as contas numéricas.

Para regenerar o PDF: `cd src && python3 figs.py && python3 figs2.py && python3 figs3.py && python3 build.py` (precisa das fontes DejaVu).

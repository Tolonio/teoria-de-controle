# Teoria de Controle – guia de estudo

Material de estudo de Teoria de Controle (Engenharia de Controle e Automação, UFOP), montado a partir das aulas e das listas.

- **`Teoria_de_Controle_Guia_de_Estudo.pdf`**: guia para imprimir (59 páginas), em ordem lógica: amplificador operacional, Laplace e função de transferência, diagramas de blocos e Mason, polos e zeros, estabilidade e Routh, erro em regime, lugar das raízes, como achar o K, controladores (P, I, D, PD, PI, PID, on-off e outros), avanço e atraso de fase, acionamentos (motor CC), Nyquist, espaço de estados, transformada Z e exercícios resolvidos. Cada página traz no topo as páginas onde estão os conceitos que ela usa.
- **`docs/index.html`**: site interativo. Tem polo arrastável no plano s, ζ e ωn, 1ª ordem, ganho K, erro × tipo, PID, on-off, amp-op, avanço/atraso e um **simulador de lugar das raízes passo a passo**. Abra o arquivo no navegador ou ative o GitHub Pages na pasta `docs/`.
- **`src/`**: scripts Python que geram as figuras e o PDF (matplotlib, scipy, reportlab) e conferem as contas numéricas.

Para regenerar o PDF: `cd src && python3 figs.py && python3 figs2.py && python3 figs3.py && python3 figs4.py && python3 assemble.py && python3 build2.py` (precisa das fontes DejaVu). O `build2.py` roda duas passagens para numerar o sumário e os cabeçalhos de referência.

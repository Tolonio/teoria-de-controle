# Teoria de Controle – guia de estudo

Material de estudo de Teoria de Controle (Engenharia de Controle e Automação, UFOP), montado a partir das aulas, dos slides e das listas resolvidas no caderno. Todas as contas foram conferidas numericamente.

**Site interativo:** https://tolonio.github.io/teoria-de-controle/ (ou abra `docs/index.html` no navegador)

![Lugar das raízes do sistema da aula](figuras/lgr_principal.png)

## O que tem aqui

| Arquivo / pasta | O que é |
|---|---|
| [`Teoria_de_Controle_Guia_de_Estudo.pdf`](Teoria_de_Controle_Guia_de_Estudo.pdf) | Guia para imprimir (59 páginas). No topo de cada página há uma linha "Revise antes" com as páginas onde estão os conceitos que ela usa. |
| [`docs/index.html`](docs/index.html) | Site interativo: cada conceito vira botões e curvas ao vivo, mais o simulador de lugar das raízes passo a passo. |
| [`figuras/`](figuras) | Todas as figuras do guia em PNG (lista abaixo). |
| [`src/`](src) | Scripts Python que fazem as contas, geram as figuras e montam o PDF. |

## Conteúdo do PDF (em ordem lógica)

| Pág. | Capítulo | O que explica |
|---:|---|---|
| 2 | 0. Como encarar a matéria | O mapa: modelar → fechar a malha → analisar → precisão → ajustar K → compensar |
| 4 | A. Amplificador operacional | Regras de ouro (i = 0, v₊ = v₋), fórmula −Zf/Zi, inversor, não inversor, diferencial (= controlador P), integrador, derivador, PI, PD, avanço/atraso com amp-op |
| 6 | 1. Laplace, FT e diagramas de blocos | Transformada de Laplace, tabela, EDO em 4 passos, resposta ao impulso e convolução, RC, massa-mola, tanque, barco, malha aberta × fechada, FTMA/FTMF, redução de blocos, Mason, sensibilidade |
| 12 | 2. Polos, zeros e resposta | Plano s, 1ª e 2ª ordem, ζ, ωn, ωd, sobressinal, tempos, polos dominantes, glossário do que cada coisa representa |
| 16 | 3. Estabilidade e instabilidade | Estável, marginal, instável; por que é o sinal da parte real; onde e por que fica instável; Routh-Hurwitz com casos especiais |
| 18 | 4. Erro em regime | Tipo do sistema, Kp, Kv, Ka, tabela de erros |
| 20 | 5. Lugar das raízes | LGR básico (como polos e zeros moldam a curva), as regras da apostila, exemplo completo da aula |
| 24 | 6. Como achar o K | Condição de módulo, Routh, K pelo erro, K no ponto de saída |
| 25 | 7. Controladores | PD (slide), família completa (P, I, PI, PD, PID, PI-D, cascata, feedforward…), PID com exemplos de P, I e D, ações em detalhe, on-off com histerese |
| 31 | 8. Avanço e atraso de fase | Origem no capacitor, rede RC, projeto por deficiência angular, atraso da aula (Kc = 0,975) |
| 37 | 9. Acionamentos elétricos | Modelo do motor CC, controle P × PI, cascata corrente/velocidade, buck e PWM, o que cada polo implica |
| 40 | 10. Resposta em frequência e Nyquist | Z = N + P, por que o −1, margens de ganho e de fase |
| 42 | 11. Espaço de estados | Da EDO para (A, B, C, D), polos = autovalores, alocação de polos, controlabilidade, observador, LQR |
| 44 | 12. Controle digital e transformada Z | Definição, estabilidade no círculo unitário, discretização com ZOH, PID no Arduino |
| 46 | 13. Exercícios resolvidos | Aula e listas, cada um com o quadro "Polos e zeros nesta questão" |
| 58 | 14. Exercícios propostos | Com gabarito |
| 59 | 15. Formulário e MATLAB | Fórmulas de bolso e comandos usados em aula |

## Site interativo (`docs/index.html`)

- **Polos:** arraste o polo no plano s e veja a resposta ao degrau mudar.
- **2ª ordem e 1ª ordem:** controles de ζ, ωn, τ e K.
- **Ganho K:** polos de malha fechada andando sobre o lugar das raízes, com resposta e estabilidade.
- **Erro em regime:** tipo 0, 1 e 2 contra degrau, rampa e parábola.
- **PID:** controles de Kp, Ki e Kd com as parcelas P, I e D desenhadas e a verificação de Routh.
- **On-off:** aquecedor com histerese e atraso, animado.
- **Amp-op:** circuitos com as ondas de entrada e saída.
- **Avanço/atraso:** ângulo no polo desejado e diagrama de fase.
- **Simulador de lugar das raízes passo a passo:** os 7 passos da apostila. Clique no plano para ver ∠G, K e ζ do ponto, com a tabela de Routh do K atual.

## Figuras (`figuras/`)

| Figura | Mostra |
|---|---|
| `ampop.png` | Amp-op ideal e circuitos de controle (inversor, não inversor, diferencial, PI, avanço/atraso) |
| `malha.png`, `pid.png` | Diagramas de malha fechada e do PID |
| `primeira_ordem.png`, `massa_mola.png` | Resposta de 1ª ordem e o sistema massa-mola-amortecedor |
| `plano_s.png`, `geometria.png`, `degrau_zeta.png` | Polo × forma da resposta, geometria de ζ e ωn, efeito de ζ |
| `maquina_zero.png` | Polo de malha fechada atravessando para a direita (zero em +2) |
| `estab_mapas.png` | Regiões de estabilidade nos planos s e z |
| `regra_eixo.png`, `lgr_basico.png`, `lgr_principal.png` | Regra do eixo real, seis LGRs básicos, LGR completo da aula |
| `lgr_A.png` a `lgr_D.png` | LGRs dos exercícios das listas |
| `pd_zero.png`, `pid_comp.png`, `ex_pid_E.png`, `ex_pid_F.png` | Efeito do zero do PD, comparação P/PI/PD/PID, respostas dos PIDs projetados |
| `onoff.png` | Relé com histerese e oscilação do aquecedor |
| `capacitor.png`, `rede_avanco.png`, `rede_atraso.png`, `fase_avanco.png` | Origem elétrica do avanço de fase e as redes RC |
| `avanco_exemplo.png`, `atraso_exemplo.png` | Projetos de avanço e de atraso (antes × depois) |
| `motor_blocos.png`, `motor_resp.png` | Diagrama de blocos do motor CC e controle P × PI |
| `nyquist.png`, `bode_margens.png` | Critério de Nyquist e margens de ganho e de fase |
| `ss_resp.png` | Alocação de polos por realimentação de estados |
| `z_discreto.png` | Malha fechada digital e limite de K pela amostragem |

## Como regenerar

Precisa de Python 3 com numpy, scipy, matplotlib e reportlab, e das fontes DejaVu.

```bash
cd src
python3 figs.py && python3 figs2.py && python3 figs3.py && python3 figs4.py   # figuras
python3 assemble.py && python3 build2.py                                      # PDF (duas passagens para numerar páginas)
```

`calc*.py` são as conferências numéricas dos exemplos (polos, K, compensadores).

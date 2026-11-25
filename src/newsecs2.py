SIGLAS = r'''
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
'''

S_INTRO = r'''      Paragraph("O que é o s (frequência complexa)", h3),
      P("<b>s</b> é uma variável complexa, s = σ + jω, chamada <b>frequência complexa</b>. Ela representa um sinal do tipo e<super>st</super> = e<super>σt</super>·(cos ωt + j·sen ωt): "
        "a parte real <b>σ</b> diz quanto o sinal cresce (σ &gt; 0) ou decai (σ &lt; 0) por segundo, e a parte imaginária <b>ω</b> diz quão rápido ele oscila (rad/s). "
        "Por isso a unidade de s é 1/s (o mesmo que rad/s)."),
      P("A grande vantagem: derivar e<super>st</super> é só multiplicar por s, porque d(e<super>st</super>)/dt = s·e<super>st</super>. Por isso, no mundo de Laplace, <b>derivar vira multiplicar por s</b> e <b>integrar vira dividir por s</b>. "
        "Quando dizemos que um sistema tem um polo em s = −2, queremos dizer que ele contém um termo e<super>−2t</super> na resposta. Um polo em s = −1 ± j3 dá e<super>−t</super>cos 3t. "
        "O plano s (eixo horizontal σ, vertical jω) é o \"mapa\" onde desenhamos polos, zeros e o lugar das raízes. Fazendo σ = 0 (s = jω), olhamos só senoides puras, e é isso que o diagrama de Bode faz (capítulo 10)."),
'''

A4_RASHID = r'''      Paragraph("A.4 Exemplo real (Acionamentos, Rashid Ex. 14.13): o motor com carga", h2),
      P("Motor CC de 50 kW, 240 V e 1700 rpm, alimentado por conversor de ganho K<sub>2</sub> = 100, com sensor de velocidade de 95 mV/(rad/s) (detalhes no capítulo 9). Torque nominal de 280,9 N·m."),
      ]
S += B(["<b>Malha aberta:</b> regula-se a tensão para 1700 rpm a vazio. Ao entrar o torque nominal, a velocidade cai 17 rad/s, para <b>1537,7 rpm</b>. A regulação é de <b>10,55%</b>, e o controlador nunca percebe.",
        "<b>Malha fechada</b> (a medida da velocidade é comparada com a referência): com a mesma carga, a velocidade cai só 2 rad/s, para <b>1680,5 rpm</b>. A regulação é de <b>1,16%</b>.",
        "<b>Por quê?</b> A queda de velocidade fica dividida por (1 + ganho de malha). Aqui, o termo K<sub>1</sub>K<sub>2</sub>K<sub>v</sub>I<sub>f</sub> = 12,1 é somado ao denominador original 1,65: "
        "(1,65 + 12,1)/1,65 ≈ 8,3 vezes menos queda. É a <b>sensibilidade</b> reduzida pela realimentação."])
S += [fig("rashid_regulacao", 13, "Figura 0 – Velocidade × torque de carga no Exemplo 14.13: a realimentação deixa a reta quase horizontal."),
      P("Note que mesmo em malha fechada sobra uma pequena queda. Esse controlador é só proporcional e o motor é tipo 0 (capítulo 4). Com um PI, a queda iria a zero. É por isso que os acionamentos reais usam PI (capítulo 9).")]
'''

REALPOS = r'''
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
'''

TRANSIT = r'''
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
'''

ALOC_ZN = r'''
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
'''

BODE = r'''      H2k("10.1 Diagrama de Bode: o que é, o que representa fisicamente e como interpretar", "bode"),
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
S += [Paragraph("10.2 O critério de Nyquist", h2),'''

ACION_R = r'''
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
'''

TEXT_FIX = [
    ("Laplace com CI nulas:", "Aplicando Laplace com condições iniciais nulas (sistema parado no instante zero):"),
    ("Polos de MA 0, −3, −1 (duplo)", "Polos de malha aberta 0, −3, −1 (duplo)"),
    ("polos de MF", "polos de malha fechada"), ("polo de MF", "polo de malha fechada"), ("Polos de MF", "Polos de malha fechada"),
    ("os de MF", "os de malha fechada"), ("ganho estático de MF", "ganho estático de malha fechada"),
    ("confira se a MF é estável", "confira se a malha fechada é estável"), ("(A MF é estável:", "(A malha fechada é estável:"),
    ("a MF é instável", "a malha fechada é instável"), ("a MF continue estável", "a malha fechada continue estável"),
    ("Sem compensador: MF = 4/", "Sem compensador, malha fechada = 4/"), ("= 1):</b> MF = 10/", "= 1):</b> malha fechada = 10/"),
    ("<b>Margem de fase (MF):</b>", "<b>Margem de fase:</b>"), ("MG = 60/30 = 2 (6 dB) e MF ≈ 25°", "margem de ganho = 60/30 = 2 (6 dB) e margem de fase ≈ 25°"),
    ("MF de 45° a 60° e MG &gt; 6 dB. A MF se relaciona", "margem de fase de 45° a 60° e margem de ganho &gt; 6 dB. A margem de fase se relaciona"),
    ("ζ ≈ MF/100 para MF &lt; 70°", "ζ ≈ (margem de fase)/100 para margens abaixo de 70°"), ("<b>Margem de ganho (MG):</b>", "<b>Margem de ganho:</b>"),
    ("dos de MA", "dos de malha aberta"), ("s, OS = 52,6%", "s, sobressinal = 52,6%"), ("OS' = 26,3%", "sobressinal' = 26,3%"), ("O OS simulado", "O sobressinal simulado"),
    ("discretize com ZOH", "discretize com segurador de ordem zero"), ("(10.2)", "(10.3)"),
]

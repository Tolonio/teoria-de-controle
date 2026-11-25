# ---------------------------------------------------------------- blocks inserted by assemble.py
GLOSS = r'''
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
'''

ESTAB = r'''
# ================= 3 estabilidade =================
S += [H1("3. Estabilidade e instabilidade: o que é, onde e por quê", "estab"),
      P("<b>Estabilidade</b> é a propriedade de, depois de uma perturbação ou de uma mudança de referência, a saída <b>voltar a se acomodar</b> num valor finito. "
        "<b>Instabilidade</b> é o contrário: a saída cresce sem parar (ou até algo físico saturar, quebrar ou desarmar). Um pêndulo pendurado é estável; um lápis em pé na ponta é instável."),
      Paragraph("3.1 As três situações", h2)]
S += table([["Situação", "Definição", "Onde estão os polos de MF", "Resposta típica"],
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
      P("A malha fechada move os polos: 1 + KG = 0. Com K pequeno, os polos de MF ficam perto dos de MA. Aumentando K, eles andam pelo LGR. "
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
'''

LGRB = r'''      H2k("5.1 O LGR \"normal\": como polos e zeros moldam a curva", "lgrb")]
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
S += [H2k("5.2 Regras de construção", "regras")]'''

CTRL_HEAD = r'''
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
'''

ACION = r'''
# ================= 9 acionamentos =================
S += [H1("9. Acionamentos elétricos com teoria de controle: o motor CC", "acion"),
      P("Acionamento é o conjunto conversor + motor + controle que faz uma máquina elétrica girar na velocidade, posição ou torque desejados. É a aplicação mais direta de tudo o que veio antes: "
        "o motor é a planta, o conversor (buck, ponte H, PWM) é o atuador, o encoder/tacogerador é o sensor e o microcontrolador roda o PI/PID."),
      Paragraph("9.1 Modelo do motor CC com excitação independente", h2)]
S += B(["<b>Armadura (elétrica):</b> V<sub>a</sub> = R<sub>a</sub>i<sub>a</sub> + L<sub>a</sub>di<sub>a</sub>/dt + E<sub>a</sub>, com força contraeletromotriz E<sub>a</sub> = K<sub>b</sub>ω.",
        "<b>Torque:</b> T = K<sub>t</sub>i<sub>a</sub> (no SI, K<sub>t</sub> = K<sub>b</sub> = K).",
        "<b>Mecânica:</b> J dω/dt + Bω = T − T<sub>L</sub> (inércia, atrito viscoso, torque de carga)."])
S += [fig("motor_blocos", 15, "Figura 0 – Diagrama de blocos do motor CC: a fcem K<sub>b</sub>ω é uma realimentação natural."),
      eq(r"\frac{\Omega(s)}{V_a(s)}=\frac{K}{(L_as+R_a)(Js+B)+K^2}"),
      P("É um sistema de <b>2ª ordem</b> com dois polos: um ligado à constante de tempo elétrica τ<sub>e</sub> = L<sub>a</sub>/R<sub>a</sub> e outro à mecânica τ<sub>m</sub> = J/B. Repare que a fcem já funciona como uma malha fechada interna. "
        "Como em geral τ<sub>e</sub> ≪ τ<sub>m</sub>, é comum desprezar L<sub>a</sub> e ficar com um 1ª ordem: Ω/V<sub>a</sub> ≈ [K/(R<sub>a</sub>J)]/[s + (BR<sub>a</sub> + K²)/(R<sub>a</sub>J)]."),
      ]
S += exemplo("Exemplo numérico (valores didáticos)",
             P("R<sub>a</sub> = 1 Ω, L<sub>a</sub> = 0,5 H, K = 0,5 V·s/rad, J = 0,1 kg·m², B = 0,1 N·m·s. Então (0,5s + 1)(0,1s + 0,1) + 0,25 = 0,05s² + 0,15s + 0,35 e"),
             eq(r"\frac{\Omega}{V_a}=\frac{10}{s^2+3s+7}\qquad p=-1{,}5\pm j2{,}18,\ \ \zeta=0{,}57,\ \ \omega_n=2{,}65\ \mathrm{rad/s}", 13),
             P("<b>Polos e zeros:</b> o par complexo dá uma partida com ~11% de sobressinal e t<sub>s</sub> ≈ 4/1,5 = 2,7 s. Não há polo na origem, então o sistema é <b>tipo 0</b> em velocidade. "
               "Ganho estático 10/7 = 1,43 (rad/s)/V."),
             P("<b>Controle P (K<sub>p</sub> = 1):</b> MF = 10/(s² + 3s + 17) ⇒ erro ao degrau 1 − 10/17 = <b>41%</b>, e os polos −1,5 ± j3,84 oscilam mais. Aumentar K<sub>p</sub> reduz o erro, mas a parte real fica presa em −1,5 e só a oscilação cresce."),
             P("<b>Controle PI (0,6 + 1,2/s):</b> o polo na origem torna o sistema tipo 1 ⇒ <b>erro zero</b> em velocidade, mesmo com torque de carga constante. O zero em −2 compensa o atraso do integrador. "
               "Polos de MF: −1,10 e −0,95 ± j3,16. O dominante é o <b>real</b> −1,10, por isso o sobressinal fica em só ~6% (t<sub>s</sub> ≈ 2,7 s)."),
             fig("motor_resp", 12))
S += [Paragraph("9.2 Controle em cascata (corrente dentro da velocidade)", h2),
      P("Acionamentos reais usam <b>duas malhas</b>. A <b>interna, de corrente</b> (rápida, PI), mede i<sub>a</sub> e controla a tensão aplicada. Isso controla diretamente o torque (T = Ki<sub>a</sub>) e permite <b>limitar a corrente</b>, protegendo o motor na partida. "
        "A <b>externa, de velocidade</b> (mais lenta, PI), gera a referência de corrente. Regra prática: a malha interna deve ser 5 a 10 vezes mais rápida que a externa, para que a externa a enxergue como um ganho quase unitário."),
      Paragraph("9.3 O atuador: conversor buck e PWM (o seu trabalho)", h2),
      P("O conversor CC-CC buck chaveado com ciclo de trabalho D entrega, em média, <b>V<sub>o</sub> = D·V<sub>in</sub></b>. Para o controle, ele é um <b>ganho</b> (V<sub>in</sub> por unidade de D) mais um filtro LC de 2ª ordem, "
        "com polos em ω<sub>0</sub> = 1/√(LC), que costumam ser bem mais rápidos que o motor. O Arduino lê a velocidade ou a tensão, calcula o PI digital (seção 12) e ajusta o PWM. Esse é exatamente o \"buck com feedback\": realimentação de tensão ou de velocidade, PI e saturação de D entre 0 e 1."),
      Paragraph("9.4 O que os polos implicam no motor", h2)]
S += B(["<b>Polo mecânico (lento):</b> domina a resposta de velocidade; inércia J maior ⇒ polo mais perto da origem ⇒ motor mais lento.",
        "<b>Polo elétrico (rápido):</b> L<sub>a</sub>/R<sub>a</sub>; importa para a malha de corrente e para o ripple do PWM.",
        "<b>K (fluxo):</b> K² aparece somando no denominador. Fluxo maior ⇒ realimentação de fcem mais forte ⇒ polos mais rápidos e menor velocidade por volt (enfraquecimento de campo faz o contrário).",
        "<b>Torque de carga T<sub>L</sub></b> é um <b>distúrbio</b>. Com P sobra erro de velocidade proporcional a T<sub>L</sub>; com PI (polo na origem antes do ponto de entrada do distúrbio) o erro vai a zero."])
S += [P("<i>Observação:</i> as questões da prova de Acionamentos que você mandou em outro chat não estão acessíveis daqui. Reenvie as fotos que eu resolvo cada uma nesta seção.")]
S.append(CondPageBreak(25 * cm))
'''

NYQ = r'''
# ================= 10 Nyquist =================
S += [H1("10. Resposta em frequência e critério de Nyquist", "nyq"),
      P("Outra forma de olhar o mesmo sistema: aplica-se uma senoide de frequência ω e mede-se quanto ela sai amplificada (|G(jω)|) e atrasada (∠G(jω)). "
        "O <b>Bode</b> desenha módulo (dB) e fase contra log ω. O <b>diagrama de Nyquist</b> desenha G(jω)H(jω) no plano complexo, com ω indo de −∞ a +∞."),
      Paragraph("10.1 O critério de Nyquist", h2),
      eq(r"Z=N+P"),
      P("<b>P</b> = polos de malha <b>aberta</b> no semiplano direito (você sabe pela FTMA). <b>N</b> = número de voltas, no sentido horário, que a curva de Nyquist dá em torno do ponto <b>−1</b>. "
        "<b>Z</b> = polos de malha <b>fechada</b> no semiplano direito. Estável ⇔ Z = 0. Se a malha aberta é estável (P = 0), basta a curva <b>não envolver o −1</b>."),
      P("<b>Por que o −1?</b> Os polos de MF satisfazem 1 + GH = 0, ou seja, GH = −1. O −1 é a mesma condição de módulo 1 e ângulo 180° do LGR. "
        "Se em alguma frequência o sinal volta com ganho ≥ 1 e invertido (180°), a realimentação \"negativa\" vira positiva e a oscilação se sustenta ou cresce."),
      fig("nyquist", 15, "Figura 0 – Nyquist de K/[(s+1)(s+2)(s+3)]: cruza o eixo real em −K/60 (ω = √11). Instável para K &gt; 60, o mesmo resultado do Routh do Exercício 13.3."),
      Paragraph("10.2 Margens de ganho e de fase (estabilidade relativa)", h2),
      P("<b>Margem de ganho (MG):</b> quanto o ganho pode ser multiplicado até instabilizar, medida na frequência em que a fase vale −180°. <b>Margem de fase (MF):</b> quanto atraso extra de fase cabe, medido onde |GH| = 1 (0 dB). "
        "Para K = 30 no exemplo: MG = 60/30 = 2 (6 dB) e MF ≈ 25°. Regra prática de projeto: MF de 45° a 60° e MG &gt; 6 dB. A MF se relaciona com o amortecimento: ζ ≈ MF/100 para MF &lt; 70°."),
      fig("bode_margens", 11),
      ]
S += dica("Nyquist e LGR contam a mesma história: o K em que o Nyquist passa por −1 é o K em que o LGR cruza o eixo jω, e a frequência é a mesma. "
          "O Nyquist tem duas vantagens: funciona com atraso de transporte e<super>−sT</super> (que o LGR não trata bem) e com dados medidos de resposta em frequência.")
S.append(CondPageBreak(25 * cm))
'''

SS = r'''
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
             P("Ganho de referência: o ganho estático de MF é C(−(A−BK))<super>−1</super>B·N = N/25 ⇒ <b>N = 25</b> para seguir r sem erro. "
               "O resultado é ζ = 0,8, ω<sub>n</sub> = 5, sem sobressinal visível e t<sub>s</sub> ≈ 1 s, contra 4 s do sistema solto."),
             fig("ss_resp", 12))
S += B(["<b>Observador (estimador de estados):</b> quando nem todos os estados são medidos, estima-se x com x̂' = Ax̂ + Bu + L(y − Cx̂). Os polos de A − LC devem ser 2 a 5 vezes mais rápidos que os do controle. "
        "Exige <b>observabilidade</b>: posto de [C; CA; …] = n.",
        "<b>Erro zero com estados:</b> acrescente um integrador do erro como estado extra (equivale ao I do PID).",
        "<b>LQR:</b> em vez de escolher polos, minimiza um custo ∫(xᵀQx + uᵀRu)dt; o MATLAB devolve K com <font face='DejaVuSansMono'>lqr(A,B,Q,R)</font>.",
        "<b>MATLAB:</b> <font face='DejaVuSansMono'>sys=ss(A,B,C,D); eig(A); rank(ctrb(A,B)); K=place(A,B,[-4+3i -4-3i]); [num,den]=ss2tf(A,B,C,D)</font>."])
S.append(CondPageBreak(25 * cm))
'''

ZT = r'''
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
S += dica("Transformada Z em prova: (1) discretize com ZOH; (2) monte 1 + KG(z) = 0; (3) estável se |z| &lt; 1; (4) valor final: y(∞) = lim<sub>z→1</sub>(z − 1)Y(z). "
          "Polo em z = 1 é o integrador digital (tipo 1).")
S.append(CondPageBreak(25 * cm))
'''

PZ = {
 "Função de transferência e polos": "Polos −1 e −3, reais e negativos: estável e sem oscilação. O −1 é o <b>dominante</b> (e<super>−t</super> some 3× mais devagar que e<super>−3t</super>) e define t<sub>s</sub> ≈ 4 s. Sem zeros, nenhum efeito extra. Ganho estático 2/3.",
 "Tipo e erros": "Polo na origem ⇒ <b>tipo 1</b>: erro zero ao degrau e finito à rampa. O zero em −2 aumenta K<sub>v</sub> (10·2/5 = 4), acelera a resposta e pode aumentar o sobressinal. Polos de MF −1,52 e −13,5, reais: sem oscilação, com −1,52 dominante.",
 "K máximo por Routh": "Três polos e nenhum zero ⇒ 3 assíntotas (±60°, 180°): dois ramos <b>inevitavelmente</b> cruzam o eixo jω. Por isso existe um K máximo (60). Sem polo na origem ⇒ tipo 0.",
 "K para um ζ desejado": "Dois polos (0 e −4) ⇒ o LGR sai em −2 e sobe na vertical. A parte real fica presa em −2, então t<sub>s</sub> = 2 s para qualquer K complexo e o K só escolhe o ζ. Polo na origem ⇒ tipo 1. Nenhum K instabiliza.",
 "Erro ao degrau em sistema tipo 0": "Sem polo na origem ⇒ tipo 0 ⇒ erro finito ao degrau. Mais K reduz o erro, mas a parte real fica em −2 (t<sub>s</sub> fixo) e ω<sub>d</sub> cresce: mais oscilação.",
 "LGR com zero": "O zero em −3 <b>atrai</b> os ramos: forma o círculo e eles voltam ao eixo real, um indo para o zero e o outro para −∞. Com um zero à esquerda e só 2 polos, o sistema é estável para todo K.",
 "Routh de 4ª ordem": "Polos de MA 0, −3, −1 (duplo), sem zeros ⇒ 4 assíntotas a ±45° e ±135°. O par de ±45° cruza o eixo jω cedo, e o ganho 20 já passou do limite ⇒ 2 polos de MF no semiplano direito.",
 "Faixa de K": "A planta tem um polo de malha aberta no semiplano direito (o termo −3). Só a realimentação com K &gt; 3 o traz para a esquerda; acima de 51 o par complexo atravessa para a direita. A estabilidade existe numa <b>janela</b> de K.",
 "LGR passo a passo de K(s+1)": "O zero −1 fica entre os polos 0 e −2 e prende um ramo no trecho [−1, 0]. Com um zero, 3 assíntotas (em vez de 4) ⇒ K crítico alto (140,8). O polo de MF que vai para o zero −1 tem efeito pequeno (quase cancelado).",
 "Zeros no semiplano direito": "Zero duplo em +2 (fase não mínima) <b>puxa</b> os ramos para a direita, e o polo +1 de malha aberta já é instável. Resultado: nenhum K estabiliza. Seria preciso um compensador que mude polos e zeros, não só o ganho.",
 "Ângulo de partida": "O par −2 ± j3 parte a −142° e curva para as assíntotas de ±135° (fica estável). Quem instabiliza é o ramo saído dos polos 0 e −1, que vai para ±45°. Os polos lentos dominam a estabilidade.",
 "Controlador proporcional": "Polos 0 e −20 ⇒ LGR vertical em σ = −10: a parte real (e o t<sub>s</sub> = 0,4 s) não depende de K; o K só escolhe o ζ (POS). Polo na origem ⇒ tipo 1 (erro à rampa = 20/K).",
 "P e depois PID": "Planta tipo 0 (sem polo em 0) ⇒ o P deixa erro de 16%. O PID adiciona um <b>polo na origem</b> (tipo 1, erro zero) e dois zeros: −3,79 (parte PD, dá o ângulo que puxa o LGR para a esquerda) e −0,235 (parte PI). Esse último forma um <b>dipolo</b> com o polo de MF −0,218 e deixa a cauda lenta.",
 "Avanço de fase: 200": "O zero −10 <b>cancela</b> o polo −10, o que só é seguro porque esse polo é estável e conhecido. O polo novo em −50 é rápido. Os polos de MF dobram de distância à origem com o mesmo ângulo: mesmo ζ, 2× mais rápido. O ganho estático cai e o erro sobe (avanço não cuida de erro).",
 "PID para K/(s²+5s+4)": "Zero do PD em −7 dá +45° para levar o LGR a −4 ± j3. O zero do PI em −0,1 com o polo na origem forma um dipolo: erro zero, mas o polo de MF −0,085 faz a aproximação final ser lenta.",
}

CAPA_NOVA = r'''
# ================= CAPA =================
S += [Paragraph("Teoria de Controle – guia de estudo", ParagraphStyle("t", fontName="DVB", fontSize=24, leading=29, textColor=NAVY)),
      Paragraph("Montado a partir das aulas, slides e listas (UFOP). Todas as contas foram conferidas numericamente. "
                "No topo de cada página, a linha <i>Revise antes</i> mostra onde estão os conceitos que ela usa.",
                ParagraphStyle("st", parent=body, fontSize=10.5, leading=14, textColor=colors.HexColor("#444"))),
      Spacer(1, 6)]
'''

MALHA = r'''
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
S += [P("Cada bloco multiplica o que entra nele. Juntando, chega-se à <b>função de transferência de malha fechada</b>, deduzida com calma no capítulo 1:"),
      eq(r"U=G_aG_c\,E,\quad Y=G_p\,U\ \Rightarrow\ \frac{Y}{E}=G_cG_aG_p=G(s);\qquad E=R-HY\ \Rightarrow\ \frac{Y}{R}=\frac{G}{1+GH}"),
      Paragraph("A.4 Exemplo numérico: o motor com carga", h2),
      P("Um motor tem ganho estático de 1,43 (rad/s)/V: cada volt dá 1,43 rad/s em regime. Queremos velocidade 1 (normalizada)."),
      ]
S += B(["<b>Malha aberta:</b> aplicamos u = 1/1,43 = 0,70 V e pronto. Funciona... até entrar uma carga: a velocidade cai para 0,75 e <b>fica lá</b>. "
        "Se depois o motor esquenta e perde 20% de ganho, cai para 0,55. O controlador nunca percebe.",
        "<b>Malha fechada com P (u = 10·e):</b> a velocidade fica em 0,94 (sobra um pequeno erro, típico do P). Com a carga, cai só para 0,92; com o desgaste, para 0,90. "
        "A realimentação reduziu o efeito das duas perturbações em mais de 10 vezes.",
        "<b>Malha fechada com PI:</b> a parcela integral continua agindo enquanto existir erro, e a velocidade <b>volta exatamente para 1</b> depois de cada perturbação."])
S += [fig("malha_sim", 14.5, "Figura 0 – Mesmo motor nas três estruturas: carga em t = 4 s e perda de 20% de ganho em t = 7 s."),
      P("<b>Por que isso acontece (sensibilidade):</b> em malha fechada, Y/R = KG/(1 + KG). Se KG é grande, Y/R ≈ 1 <b>qualquer que seja G</b>. A planta pode mudar que o resultado quase não muda. "
        "Com K = 10 e G = 1,43, Y/R = 14,3/15,3 = 0,935. Se G cai 20% (1,14), Y/R = 11,4/12,4 = 0,920: só 1,6% de variação, contra 20% em malha aberta.")]
S += table([["", "Malha aberta", "Malha fechada"],
            ["Precisa de sensor?", "não (mais barato e simples)", "sim"],
            ["Corrige perturbações e desgaste?", "não", "sim"],
            ["Precisão", "depende de conhecer bem a planta", "depende de um bom sensor"],
            ["Pode ficar instável?", "não, se a planta for estável", "<b>sim</b>: ganho demais faz oscilar (capítulo 3)"],
            ["Quando usar", "processo previsível, sem perturbação, erro tolerável", "precisão, perturbações, planta que muda ou instável"]], [4.4, 5.8, 6.2])
S += dica("A pergunta-chave para classificar: <b>a saída é medida e comparada com a referência?</b> Se sim, é malha fechada; se não, é aberta. "
          "Um timer, por mais \"inteligente\" que seja, é malha aberta.")
S.append(CondPageBreak(25 * cm))
'''

IMPED = r'''
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
'''

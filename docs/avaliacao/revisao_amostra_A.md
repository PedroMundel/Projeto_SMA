# Revisão independente de fidelidade — amostra A

Arquivos: os 5 de menor concordância entre réplicas (`regra_160` 0,528; `regra_151` 0,539;
`regra_115` 0,604; `regra_032` 0,609; `regra_217` 0,620). Julgamento contra o `.gobr`, com o
manual (§4.6, §5.4, §6.1, §6.2, §6.4, §6.6, §7.4, §7.6) e as premissas P1–P8 como base.

Amostra de `regra_032` (15 de 75): R1, R2, R4, R8, R11 (início); R21, R26, R38, R43, R46 (meio);
R56, R61, R72, R74, R75 (fim).

## 1. Tabela-resumo

| Arquivo | Regras revisadas | Corretas | Imprecisas | Erradas | Resumo ok? | Pontos de atenção ok? |
|---|---|---|---|---|---|---|
| regra_160 | 14 (todas) | 5 | 2 | 7 | Sim, com ressalva (omite a regra final "indefinido") | Não. Seção vazia; lacunas reais ficaram de fora |
| regra_151 | 1 (todas) | 0 | 1 | 0 | Parcial ("todos os clientes" ignora o filtro de segmentação) | Não. Ponto 1 é falso; ponto 2 é impreciso |
| regra_115 | 2 (todas) | 2 | 0 | 0 | Sim | Sim (vazio; nada evidente a apontar) |
| regra_032 | 15 de 75 | 14 | 1 | 0 | Sim, com ressalva (chama de "fixas" carteiras que são `livre`) | Parcial. Os 4 pontos são verdadeiros, mas falta a consequência do erro de sintaxe |
| regra_217 | 2 (todas) | 1 | 1 | 0 | Parcial (omite o piso de 7 dias da 2ª faixa) | Sim |

## 2. Itens imprecisos ou errados

### regra_160

**Erro comum às regras R7–R12 e R14 (redator).** A coluna Observação diz *"Rota nos próximos 1 dia:
nunca visitados, visitados nos últimos 3 dias ou sem visita há mais de 3000 dias"*.
- `.gobr` e pacote: estas regras não filtram por rota. A população efetiva é
  **(sem rota nos próximos 1 dia) OU (com rota, mas fora da janela de visita 4–3000 dias)**. Só a
  segunda parte foi descontada pelas regras R1–R6 de fechamento de rota.
- A descrição perdeu o primeiro termo do OU, que é a maior parte dos clientes. Nas linhas R1–R6, a
  mesma coluna lista condições somadas com "e" ("Rota nos próximos 1 dia; visitados..."). Por esse
  paralelo, o leitor entende que R7–R12 e R14 também só valem para quem tem rota amanhã, o que é falso.
- O pacote traz o OU completo, então a causa é o **redator**. Nas réplicas v3, os agentes 1, 3, 4 e 5
  escreveram isso certo ("exceto os que entram no fechamento de rota", "sem rota em 1 dia ou...").
  O `agente_2`, que foi o escolhido, é o único que errou.

| Regra | Classe | O que a descrição diz | O que o `.gobr` diz | Causa |
|---|---|---|---|---|
| R5 Fechamento de rota: resgate | imprecisa | "inativos para o vendedor **que nunca compraram com ele** ou estão há mais de 90 dias sem comprar" | Quem nunca comprou com o vendedor e cumpre os filtros comuns (PJ, rota, visita 4–3000) já foi tratado por R1 (`sem venda do vendedor`). Pela P4, `inativos para o vendedor` também exclui quem nunca comprou. Sobra: inativo para o vendedor, sem compra há mais de 90 dias. | **Pacote**: `tratados_antes_por` não inclui R1, e a `condicao_efetiva` mantém o termo "nunca compraram", que é vazio. |
| R6 Fechamento de rota: ativos sem compra recente | imprecisa | "ativos para o vendedor **que nunca compraram com ele** ou há mais de 90 dias" | Mesmo caso. R1 já tratou quem nunca comprou, e "ativo" implica ter comprado (P4). Sobra: ativo para o vendedor, sem compra há mais de 90 dias. | **Pacote** |
| R7 Primeira compra (prospects) | errada | Observação: só clientes com rota nos próximos 1 dia, fora da janela de visita | PJ sem venda do vendedor, **menos** os tratados por R1 (rota + visita 4–3000). A maioria entra justamente por não ter rota amanhã. | **Redator** |
| R8 Primeira compra (ativos) | errada | Idem R7 | Idem R7, para o time `vendedores_ativos` | **Redator** |
| R9 Risco de inatividade | errada | Idem R7, com 61–90 dias | PJ, positivação com o vendedor entre 61 e 90 dias, menos os tratados por R3 | **Redator** |
| R10 Estimular regularidade | errada | Idem R7, com 31–60 dias | PJ, positivação com o vendedor entre 31 e 60 dias, menos os tratados por R2 | **Redator** |
| R11 Compra regularmente | errada | Idem R7, com compra nos últimos 30 dias | PJ, `atividade do vendedor de 30 dias`, menos os tratados por R4 | **Redator** |
| R12 Resgate de cliente sem compra | errada | Idem R7. Repete também "inativos... que nunca compraram com ele" | PJ inativo para o vendedor, menos os tratados por R5. Os PJ que nunca compraram já foram tratados por R7/R8 (P6: os dois times cobrem todos). | **Redator** (observação) + **pacote** ("nunca compraram") |
| R14 Pessoa Física/Jurídica (indefinido) | errada | "Clientes **pessoa jurídica** ativos para o vendedor que nunca compraram... ou há mais de 90 dias" + a observação de rota | Sem filtro: pega todo o resto. Isso inclui, e o nome deixa claro que é o objetivo, os clientes **sem tipo de pessoa definido** (nem `pessoa fisica` nem `pessoa juridica`), que nenhuma regra anterior trata. A sobra de PJ é só uma parte. | **Pacote**: trata PF/PJ como partição binária, deduz "PJ" ao descontar R13 e perde o "indefinido". O **redator** repete o erro e soma o da observação. |

Pontos de atenção (vazio). Ficaram de fora:
- R14, com nome de "indefinido", é na prática o pega-tudo final. Ela também recebe os PJ ativos para o
  vendedor sem compra há mais de 90 dias que não entraram no fechamento de rota.
- O fechamento de rota exige `recencia de visita entre 4 e 3000 dias`. Um cliente PJ **nunca
  visitado** com rota amanhã não recebe a frequência de 1 dia. Isso é relevante justamente para
  quem está na primeira compra.
- Clientes PF nunca entram no fechamento de rota (todas as regras R1–R6 exigem PJ).

Resumo: fiel ("seis primeiras regras... 1 dia... depois primeira compra e faixas... PF 14 dias"),
mas omite a regra final sem filtro (14 dias).

### regra_151

| Regra | Classe | O que a descrição diz | O que o `.gobr` diz | Causa |
|---|---|---|---|---|
| R1 Não agendar Ativos de campo com vendas em 60 dias | imprecisa | "Clientes de todos os tipos da carteira televendas fixa com ruptura de campo". O resumo diz que a regra "bloqueia a agenda de **todos** os clientes dessa carteira". | Bloqueia só os clientes da carteira que estão **também** na segmentação `cliente de ruptura` (`contido na segmentacao`): carteira fixa do time de campo com `tem venda em 60 dias`. Na prática, o filtro é quase redundante, porque a carteira só tem clientes com última compra entre 7 e 60 dias. Por isso a classe é imprecisa, não errada. Ainda assim, a descrição esconde uma condição real do código. | **Pacote**: o filtro está reconhecido, mas `condicao_propria` e `condicao_efetiva` = "todos os clientes". |

Pontos de atenção:
- Ponto 1 é **falso**: *"O nome... fala em 60 dias, mas a regra usa outro valor"*. O valor 60 está no
  código: `tem venda em 60 dias` (segmentação usada pela regra) e `de positivacao(entre 7 dias e
  60 dias)` (carteira de origem). Nome e código batem. **Erro do pacote**: o alerta só olha os números
  da própria regra, embora `numeros_permitidos` já contenha 60. As 5 réplicas copiaram o alerta.
- Ponto 2 é impreciso: *"não se enquadram em nenhuma regra de frequência e ficam sem
  parametrização"*. Nas três primeiras semanas do mês, de fato nada se aplica a eles. Na última
  semana, porém, recebem o bloqueio, que é uma parametrização. O ponto deveria dizer que a lacuna é
  temporal (fora da `ultima semana`).

### regra_115

Nada a apontar.

### regra_032

| Regra | Classe | O que a descrição diz | O que o `.gobr` diz | Causa |
|---|---|---|---|---|
| R74 Inativos Curva C (Norte e Nordeste - Corporativo/Consumidor) | imprecisa | Critério: "Clientes que já compraram, de ramos fora das demais faixas; ou do ramo CONS. FINAL, há mais de 180 dias sem comprar, com faturamento até R$ 10000 [não traduzido...]". Frequência vazia; a observação diz "Regra sem ação". | A regra está quebrada: `ramo de atividade igual("CONS. FINAL"` não fecha o parêntese e não há ação. A descrição apresenta uma população tratada por ela, inclusive clientes **de outros ramos** do Norte/Nordeste, porque considera o filtro não reconhecido como ausente. Uma regra sem ação não parametriza ninguém. Logo, não deveria "consumir" clientes, pelo mesmo raciocínio da P3. | **Pacote**: R74 entra em `tratados_antes_por` de R75. O efeito implícito é que os clientes N/NE de ramos fora das faixas escapariam do `nao agendar` final. |

Corretas na amostra: R1, R2, R4, R8 (a observação sobre o escopo de grupo está certa), R11 (o texto é
truncado, mas fiel à efetiva: inclui global 121–150 sem compra no grupo em 150 dias), R21, R26, R38,
R43, R46, R56, R61, R72 e R75.

Resumo e carteiras: fiéis. Única ressalva: falam em "duas carteiras fixas", mas as duas são `carteira
livre` sobre `carteirafixa("televendas")`. Como as listas de UF são disjuntas e cobrem as 27 UFs,
isso não muda a população.

Pontos de atenção: os 4 são verdadeiros (o 4º é um comentário técnico do pacote, sem valor para o
negócio). Ficaram de fora:
- **A consequência do parêntese não fechado.** O parser real pode rejeitar o arquivo inteiro ou
  "engolir" o bloco seguinte, que é justamente a regra final `nao agendar`. Mesmo que só R74 se perca,
  os inativos curva C de CONS. FINAL do N/NE ficam sem frequência. A descrição trata R75 como se
  funcionasse normalmente.
- (Possível, com ressalva.) Pelo manual §6.6, `ramo de atividade igual(...)` filtra por **id**, e o
  arquivo passa nomes ("MATCON", "CONS. FINAL"...). Se os ids desse cliente forem numéricos, nenhuma
  faixa casa e todos, exceto baixados e prospects, caem no `nao agendar` final. O pacote até marca
  "(id)", mas nenhum ponto alerta para isso.
- A mistura de escopo em R8 (`recencia de positivacao em 150 dias` sem `global`, enquanto as outras
  71 faixas usam `global`) tem cara de erro de digitação. O ponto 3 descreve o efeito, mas não diz isso.

### regra_217

| Regra | Classe | O que a descrição diz | O que o `.gobr` diz | Causa |
|---|---|---|---|---|
| R2 Manter a regularidade de compra | imprecisa | Frequência "Pelo histórico, entre 14 e 28 dias"; observação: "Frequência calculada pelo histórico **de compras**; sem histórico, vale o mínimo de 14 e o máximo de 28 dias" | `frequencia do historico ou no minimo de 14 dias e no maximo de 28 dias`. (a) A coluna Frequência diz que o histórico é limitado a 14–28; a observação diz que os limites só valem sem histórico. São duas leituras diferentes na mesma linha, e "sem histórico, vale mínimo 14 e máximo 28" não define que frequência se aplica. (b) O manual §7.4.3 define `do historico` como cálculo pelo histórico **de visitas**, não de compras. | **Pacote** (o `significado` da ação diz "histórico de compras" e "se não houver, limitada a...") + **redator** (juntou as duas leituras) |

Resumo: diz que *"os que compraram nos últimos 30 dias e não são de compra única"* seguem o histórico.
Omite o piso de 7 dias (`entre 7 dias e 30 dias`), que a tabela e os pontos de atenção trazem
corretamente.

## 3. Conclusão

- A concordância baixa **não tem uma causa só**. Em `regra_160`, ela reflete um erro real. Quatro das
  cinco réplicas expressaram corretamente que R7–R12/R14 valem também para quem não tem rota amanhã.
  A seleção escolheu justamente a única réplica errada (`agente_2`). O critério de escolha por
  concordância textual não protege contra isso.
- Em `regra_151`, `regra_115` e `regra_217`, as réplicas são semanticamente equivalentes. Em textos
  tão curtos, diferenças pequenas de redação derrubam a métrica. Os erros que existem nesses arquivos
  (ponto falso dos "60 dias" e filtro de segmentação omitido na 151; "histórico de compras" e leitura
  ambígua do mínimo/máximo na 217) vêm do **pacote** e aparecem nas 5 réplicas. A concordância é cega
  a eles.
- Em `regra_032`, a amostra é quase toda correta. Os problemas são do pacote (R74 quebrada tratada
  como consumidora de clientes) e de pontos de atenção incompletos.
- Os erros mais graves em população efetiva vêm do pacote: PF/PJ tratados como partição binária
  (regra_160 R14), filtro `contido na segmentacao` ignorado (151) e regra sem ação que consome
  clientes (032). Vale corrigi-los na camada determinística antes de gerar novas réplicas.

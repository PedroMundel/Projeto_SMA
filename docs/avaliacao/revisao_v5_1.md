# Revisão de fidelidade após o pacote v5: revisor 1

Arquivos: regra_160, regra_151, regra_217, regra_233 (todas as regras). Fontes: `.gobr` de referência; manual §4.6 e §4.6.1 (funções de carteira, `ruptura ... de positivacao`), §4.7 (ordem das carteiras), §5.4 (`na ultima semana` = últimos 7 dias do mês), §6.1 (ativos/inativos, `sem venda`, `unica compra com o vendedor`, `atividade do vendedor de`), §6.2 (recência de visita/positivação e escopos), §6.3 (`não tem credito`, `com menos de R$ ... de credito disponivel`, `inadimplentes`), §6.5 (`pessoa fisica`/`pessoa juridica`), §6.6 (`tipo de cobranca`), §6.9 (`contido na segmentacao`), §6.12 e §6.13 (`entre ... e ...`, `nos proximos N dias`), §7.4.2 e §7.4.3 (limites e `do historico`), §7.6 (cascata first-match); premissas P2, P4, P6, P7 e P9.

## 1. Tabela-resumo

| Arquivo | Regras revisadas | Corretas | Imprecisas | Erradas | Resumo ok? | Pontos de atenção ok? |
|---|---|---|---|---|---|---|
| regra_160 | 14 | 13 | 1 | 0 | Parcial | Não |
| regra_151 | 1 | 0 | 1 | 0 | Parcial | Não |
| regra_217 | 2 | 1 | 0 | 1 | Parcial | Não |
| regra_233 | 6 | 6 | 0 | 0 | Sim | Parcial |
| **Total** | **23** | **20** | **2** | **1** | **1 sim, 3 parciais** | **0 sim, 1 parcial, 3 não** |

## 2. Itens imprecisos ou errados

### regra_160

As regras R1 a R13 batem com o código e com a condição efetiva do pacote. Conferi a cascata de ponta a ponta: R2 (31 a 60 dias), R3 (61 a 90) e R4 (até 30, `atividade do vendedor de 30 dias`) cobrem 0 a 90 dias de recência de compra com o vendedor. Por isso R5 e R12 (`inativos para o vendedor`) ficam com "há mais de 90 dias sem comprar com ele". R6 fica com o resíduo "ativos para o vendedor e há mais de 90 dias sem comprar" (P4: `sem venda do vendedor`, ativos e inativos formam uma partição). R7 e R8 só perdem o que R1 consumiu (P6: times disjuntos). As observações "visitados nos últimos 3000 dias, mas sem visita há mais de 3 dias" traduzem bem `recencia de visita entre 4 dias e 3000 dias`.

**R14 "Pessoa Física/Jurídica (indefinido)": imprecisa**
- **O que a descrição diz:** segmento "Tipo de pessoa indefinido". O critério é "Clientes sem tipo de pessoa definido ou pessoas jurídicas ativas há mais de 90 dias sem comprar com o vendedor". O resumo diz que "Pessoa física e tipo de pessoa indefinido fecham as regras".
- **O que o `.gobr` diz:** a regra não tem nenhum filtro (`do time(...)` + `frequencia de 14 dias`). É o pega-tudo final. Pela cascata (§7.6), ela recebe os clientes sem tipo de pessoa e também todo PJ ativo para o vendedor com mais de 90 dias sem comprar: os que não têm rota amanhã e os que têm rota mas não foram visitados entre 4 e 3000 dias (por exemplo, nunca visitados). O rótulo "Tipo de pessoa indefinido" e o resumo escondem essa segunda parte da população. Além disso, "ativas há mais de 90 dias sem comprar" é ambíguo: pode ser lido como "ativas há mais de 90 dias". O certo é "ativas para o vendedor, mas há mais de 90 dias sem comprar com ele".
- **Causa:** redator. A condição efetiva do pacote estava certa. O nome da regra ("indefinido") também induz ao erro (**código**), e a descrição deveria apontar isso.

**Resumo (parcial):** em "primeira compra, que tem 7 dias para prospects e 14 dias para ativos", "prospects" e "ativos" são os **times de vendedores** (`vendedores_prospects` e `vendedores_ativos`), não situações do cliente. Lido como situação do cliente, o trecho se contradiz ("primeira compra para ativos"). O resumo também omite o resíduo PJ de R14 (ver acima).

**Pontos de atenção (não):** a lista está vazia, mas há problemas evidentes de modelagem:
1. R1 a R5 têm a mesma ação de R6 (`frequencia de 1 dia`) e as mesmas condições de rota e visita. R6 sozinho produziria o mesmo efeito. A divisão por perfil só muda o nome da regra que parametriza o cliente. A consequência é que R6, a regra genérica "Fechamento de Rota e Sem Atendimento há 3 dias", fica só com "ativos para o vendedor há mais de 90 dias sem comprar". Essa população é vazia se o limite de inatividade do sistema for de 90 dias ou menos (`$diasparainativos$`; o manual não fixa o valor).
2. O fechamento de rota exige visita registrada (`recencia de visita entre 4 dias e 3000 dias`). Clientes nunca visitados, inclusive prospects com rota amanhã, não recebem a frequência de 1 dia e caem em R7, R8 ou R14. O pacote mostra isso na condição efetiva de R7 ("nunca foram visitados ou ..."), e um usuário precisaria saber.
3. R14 é o pega-tudo apesar do nome "(indefinido)" (ver acima).
- **Causa:** pacote. Não gera alerta para resíduo provavelmente vazio nem para nome de regra que não corresponde à população efetiva. O redator também não aproveitou o que a condição efetiva de R7 já mostrava.

### regra_151

**R1 "Não agendar Ativos de campo com vendas em 60 dias": imprecisa**
- **O que a descrição diz:** "Clientes da segmentação 'cliente de ruptura', que compraram nos últimos 60 dias", não agendar, só na última semana do mês.
- **O que o `.gobr` diz:** a fonte é `da carteira("televendas fixa com ruptura de campo")`, definida como `ruptura("de campo" para "televendas") de positivacao(entre 7 dias e 60 dias)`: clientes de campo cuja última compra foi entre 7 e 60 dias atrás (§4.6.1, §6.12). A segmentação é `carteirafixa("de campo")` com `tem venda em 60 dias`. Todo cliente da carteira comprou nos últimos 60 dias e veio da carteira de campo. Logo, o filtro `contido na segmentacao("cliente de ruptura")` é praticamente redundante, e a regra bloqueia a carteira inteira na última semana do mês (`na ultima semana` = últimos 7 dias, §5.4). O critério, sem citar a carteira, sugere que a regra bloqueia todo cliente de campo com compra em 60 dias, inclusive os que compraram há menos de 7 dias, e que só um subconjunto da carteira é afetado. As duas leituras são falsas.
- **Causa:** pacote. A condição efetiva ("na segmentação ...") não cruza a definição da carteira com a da segmentação e não detecta a redundância. O redator também omitiu a fonte. O filtro redundante é um problema do **código**, e a descrição deveria apontá-lo.

**Resumo (parcial):** situa bem a carteira e o filtro temporal, mas repete a leitura de "subconjunto da segmentação" e não diz que, fora da última semana do mês, nenhum cliente da carteira é parametrizado.

**Pontos de atenção (não):** "Todos os clientes da carteira ... não se enquadram em nenhuma regra e ficam sem parametrização" é falso como está escrito. Na última semana do mês, R1 bloqueia praticamente todos eles. O correto é: "fora da última semana do mês, nenhum cliente da carteira é parametrizado; na última semana, todos são bloqueados". Falta também apontar a redundância entre a segmentação e a carteira.
- **Causa:** pacote. `nao_cobertos` registra "todos os clientes" sem a ressalva temporal, embora as premissas digam que uma regra com filtro temporal só consome clientes nos dias em que roda. O redator copiou o texto sem qualificar.

### regra_217

R1 está correta (`unica compra com o vendedor`, `frequencia de 7 dias`).

**R2 "Manter a regularidade de compra": errada**
- **O que a descrição diz:** "Clientes com **mais de uma compra com o vendedor** que compraram nos últimos 30 dias, mas estão há pelo menos 7 dias sem comprar".
- **O que o `.gobr` diz:** `recencia de positivacao entre 7 dias e 30 dias`, menos o que R1 consumiu. A condição efetiva do pacote é "... e sem ser de compra única com o vendedor". O complemento de "uma única compra com o vendedor" inclui quem **nunca comprou com o vendedor**. Como a recência sem escopo é a do grupo (§6.2, P2), um cliente que comprou de outro vendedor do grupo há 7 a 30 dias, e nunca com este, entra em R2. A descrição o exclui. A população descrita é menor que a real. A frequência ("pelo histórico, entre 14 e 28 dias") está certa pela P9 e pelo §7.4.2 e §7.4.3.
- **Causa:** redator. O pacote dizia "sem ser de compra única com o vendedor", e o texto trocou isso por "mais de uma compra com o vendedor".

**Resumo (parcial):** "quem compra com regularidade" repete a intenção do nome da regra, não o código. O resumo omite a janela de 7 a 30 dias e não menciona os clientes que ficam fora de tudo.

**Pontos de atenção (não):** "Clientes com mais de uma compra com o vendedor que nunca compraram, ..." se contradiz: quem tem mais de uma compra não pode nunca ter comprado. O conjunto não coberto do pacote é "(nunca compraram ou compraram nos últimos 6 dias ou há mais de 30 dias) e sem ser de compra única com o vendedor". Esse conjunto inclui todos os inativos e prospects do time, a maior parte da base, e a redação o deforma. Também falta apontar que R1 não tem limite de recência: um cliente que comprou uma única vez há anos continua recebendo ligação semanal.
- **Causa:** redator (a mesma troca de R2). O alerta de R1 sem recência também não vem do pacote.

### regra_233

As seis regras estão corretas. `nao tem credito` = sem crédito disponível (§6.3). `com menos de R$ 199 de credito disponivel` foi transcrito com o valor do código. `inadimplentes` está certo. `ativos`, `inativos` e `sem venda` seguem a P4 ("nunca compraram com o vendedor"). O resumo informa que os três bloqueios vêm antes das frequências, e isso basta para entender que as faixas excluem os bloqueados.

**Pontos de atenção (parcial):**
- O ponto 1 é um alarme falso. O nome "crédito igual ou menor que R$0,00" é equivalente a `nao tem credito` ("Clientes sem crédito disponível", §6.3). Não há divergência entre nome e código, e o ponto induz o usuário a procurar um erro que não existe.
- O ponto 2 procede. O nome diz "menor que R$200,00" e o código usa `com menos de R$ 199`, então clientes BK com crédito entre R$ 199,00 e R$ 199,99 não são bloqueados. Seria mais útil dizer isso do que dizer que o valor "não aparece no código".
- **Causa:** pacote. O alerta de "número citado no nome que não está no código" é heurístico: não reconhece que `nao tem credito` corresponde a R$ 0.

## 3. Conclusão

Das 23 regras, 20 estão corretas, 2 imprecisas e 1 errada. A cascata da regra_160, que é a mais longa, foi reconstruída sem erro de população nas 13 primeiras regras. O único erro de população (regra_217 R2) é do redator: "sem ser de compra única com o vendedor" virou "mais de uma compra com o vendedor", o que exclui os clientes que só compraram com outros vendedores do grupo. O mesmo deslize deixa contraditório o ponto de atenção do arquivo. O ponto mais fraco são os `pontos_de_atencao`: vazios na regra_160, apesar do resíduo provavelmente vazio de R6 e do pega-tudo mal rotulado em R14; falso na regra_151, onde falta a ressalva temporal e a redundância entre segmentação e carteira; e com um alarme falso na regra_233. Esses três problemas vêm do pacote (`nao_cobertos` sem ressalva temporal, nenhum cruzamento entre carteira e segmentação, alerta numérico heurístico). Devem ser corrigidos em `gobr/`, conforme a regra CASCADE-FIRST, e não no prompt.

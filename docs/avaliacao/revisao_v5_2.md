# Revisão de fidelidade após o pacote v5: revisor 2

Arquivos: regra_160, regra_151, regra_217, regra_233 (todas as regras). Fontes: `.gobr` de referência; manual §3.3/3.3.1 (seleção de vendedores, `ativados`, `menos`), §4.2 e §4.6/4.6.1 (carteiras exclusivas, `ruptura ... de positivacao`), §4.7 (padrão automático `carteirafixa`), §5.4 (`na ultima semana` = últimos 7 dias do mês), §6.1 (atividade/inatividade, `unica compra com o vendedor`, `atividade do vendedor de`), §6.2 (recência sem escopo = grupo), §6.3 (`nao tem credito`, `com menos de R$ X de credito disponivel`), §6.5 (pessoa física/jurídica), §6.9 (`contido na segmentacao`), §6.13 (`nos proximos N dias`), §7 (introdução: parametrização persistente), §7.3.4 (`nao agendar`), §7.4.2 (modificadores de limite), §7.6 (cascata sem repetição), §8.4.1 (`tem venda em N dias`); premissas P2, P4, P5, P6, P7, P9.

## 1. Tabela-resumo

| Arquivo | Regras revisadas | Corretas | Imprecisas | Erradas | Resumo ok? | Pontos de atenção ok? |
|---|---|---|---|---|---|---|
| regra_160 | 14 | 14 | 0 | 0 | Sim | Não (vazio; falta a redundância R1–R5 × R6) |
| regra_151 | 1 | 0 | 1 | 0 | Sim | Não (afirma o contrário da própria R1; faltam 2 problemas) |
| regra_217 | 2 | 1 | 0 | 1 | Parcial | Não (frase contraditória) |
| regra_233 | 6 | 6 | 0 | 0 | Sim | Parcial (1 dos 2 alertas é falso) |
| **Total** | **23** | **21** | **1** | **1** | **3 de 4 (1 parcial)** | **0 de 4 (1 parcial)** |

## 2. Itens imprecisos ou errados

### regra_160

As 14 regras estão corretas. As faixas R1–R6 (PJ, `data da rota nos proximos 1 dia`, `recencia de visita entre 4 dias e 3000 dias`) aparecem com os recortes certos: 0–30, 31–60 e 61–90 dias de positivação com o vendedor, inativos com mais de 90 dias e, em R6, "demais ativos há mais de 90 dias". R7 e R8 tiram só R1. R9–R12 tiram o fechamento de rota. R14 inclui as PJ ativas há mais de 90 dias, como manda a cascata (§7.6, P4).

**Pontos de atenção (vazio): incompleto**
- **O que a descrição diz:** nenhum ponto de atenção.
- **O que o `.gobr` diz:** R1–R5 têm a mesma ação de R6 (`frequencia de 1 dia`, linhas 21, 29, 37, 45, 53, 60). R6 tem só as condições comuns (PJ, rota em 1 dia, visita entre 4 e 3000 dias), então pega todo o resto. Tirar R1–R5 não muda nenhuma agenda: a separação "por perfil de compra" que o resumo destaca não tem efeito. É redundância ou sinal de que o autor queria frequências diferentes por perfil. Há ainda um nome enganoso: "Pessoa Física/Jurídica (indefinido)" (R14) também atende PJ ativas para o vendedor sem compra há mais de 90 dias, o que a tabela da R14 mostra mas nenhum ponto destaca. Menor: o time `vendedores_prospects` usa `porid(...)` sem `ativados` (§3.3.1) e pode incluir vendedores desabilitados, ao contrário de `vendedores_ativos`.
- **Causa:** pacote. Não há alerta para regras consecutivas com a mesma ação que se absorvem, nem para nome de catch-all que esconde população. O redator não tinha base para isso.

### regra_151

**R1 "Não agendar Ativos de campo com vendas em 60 dias": imprecisa**
- **O que a descrição diz:** segmento "Bloqueio: ativos de campo com vendas em 60 dias". Critério: "Clientes da segmentação 'cliente de ruptura', que compraram nos últimos 60 dias". Observação: "Executada somente na última semana do mês".
- **O que o `.gobr` diz:** a fonte é a carteira `ruptura("de campo" para "televendas") de positivacao(entre 7 dias e 60 dias)`, ou seja, clientes do campo cuja última compra foi entre 7 e 60 dias atrás (§4.6.1). O filtro `contido na segmentacao("cliente de ruptura")` (§6.9) exige carteira fixa do campo e `tem venda em 60 dias` (§8.4.1: venda nos últimos 60 dias). Todo cliente da carteira já comprou nos últimos 60 dias, então o filtro só pode excluir alguém por diferença de escopo da compra ou de origem (carteira fixa × portfólio do time). Na prática, a regra bloqueia quase toda a carteira na última semana do mês. A descrição não diz isso e deixa parecer um subconjunto. O rótulo "ativos" vem do nome da regra: não há filtro `ativos` no código.
- **Causa:** pacote, por não cruzar a condição da fonte com a da segmentação (`condicao_efetiva` = só "na segmentação"). Também redator, por levar o rótulo "ativos" do nome para o segmento.

**Pontos de atenção: errados e incompletos**
- **O que a descrição diz:** "Todos os clientes da carteira 'televendas fixa com ruptura de campo' não se enquadram em nenhuma regra e ficam sem parametrização."
- **O que o `.gobr` diz:** na última semana do mês (§5.4), R1 aplica `nao agendar` a praticamente todos esses clientes. A frase contradiz a própria linha da R1. Ela só vale nas três primeiras semanas, e mesmo assim com ressalva: a parametrização do GoBR é persistente (§7, introdução) e o arquivo não tem regra de frequência nem `limpar parametros`. Nada reparametriza esses clientes depois da última semana, então o bloqueio provavelmente continua no mês seguinte. Esse é o problema de modelagem mais sério do arquivo, e a descrição não o aponta. Também falta dizer que a carteira se chama "televendas **fixa** com ruptura de campo" mas não tem `clientes carteirafixa("televendas")`: os clientes fixos do vendedor 291 não entram nela.
- **Causa:** pacote. `nao_cobertos` = "todos os clientes" ignora a R1 por ela ter filtro temporal, e não vem o alerta que `docs/premissas.md` promete para esse caso. Também código: há bloqueio temporal sem regra que o desfaça, e o nome da carteira diverge da definição.

### regra_217

**R2 "Manter a regularidade de compra": errada**
- **O que a descrição diz:** "Clientes com mais de uma compra com o vendedor que compraram nos últimos 30 dias, mas estão há pelo menos 7 dias sem comprar".
- **O que o `.gobr` diz:** `recencia de positivacao entre 7 dias e 30 dias`, sem escopo, menos os clientes de R1 (`unica compra com o vendedor`). Sem escopo, a recência é do grupo (§6.2, P2). A população efetiva é então "última compra no grupo entre 7 e 30 dias atrás e **sem ser** de compra única com o vendedor". Isso inclui quem nunca comprou com o próprio vendedor mas comprou com um colega do grupo nesse intervalo. "Mais de uma compra com o vendedor" exclui esses clientes e restringe a população. O pacote estava certo ("sem ser de compra única com o vendedor"), e o redator trocou isso por uma condição que não é equivalente.
- **Causa:** redator. Fator contribuinte do pacote: o significado "compraram nos últimos 30 dias" não diz que a recência é do grupo, o que facilitou ler a compra como "com o vendedor".

**Resumo: parcial**
- **O que a descrição diz:** "quem compra com regularidade segue a frequência calculada pelo histórico de visitas, entre 14 e 28 dias".
- **O que o `.gobr` diz:** não há critério de regularidade. A faixa é só a última compra entre 7 e 30 dias atrás. Uma única compra com outro vendedor do grupo, há 10 dias, já basta. O rótulo vem do nome da regra e esconde a faixa 7–30. A leitura de mínimo e máximo como limites segue P9 e está certa.
- **Causa:** redator.

**Pontos de atenção: errados e incompletos**
- **O que a descrição diz:** "Clientes com mais de uma compra com o vendedor que nunca compraram, compraram nos últimos 6 dias ou estão há mais de 30 dias sem comprar não se enquadram em nenhuma regra".
- **O que o `.gobr` diz:** "mais de uma compra com o vendedor que nunca compraram" é contraditório. O pacote dizia "(nunca compraram ou compraram nos últimos 6 dias ou sem comprar há mais de 30 dias) e sem ser de compra única com o vendedor". O mesmo erro de reescrita da R2 se repete aqui. Faltou também um ponto evidente: R1 vale para quem fez uma única compra com o vendedor **em qualquer época** (§6.1, sem janela de tempo). Um cliente que comprou uma vez há anos fica com ligação semanal por tempo indeterminado, o que não combina com "Fazer relacionamento". Faltou ainda dizer que R1 (escopo do vendedor) e R2 (escopo do grupo) usam escopos diferentes.
- **Causa:** redator, pela contradição. Pacote, pela falta de alerta sobre compra única sem janela e sobre a mistura de escopos (P2 promete alerta quando a cascata mistura escopos).

### regra_233

As 6 regras estão corretas. Os bloqueios R1–R3 (`nao tem credito` + DH, `com menos de R$ 199 de credito disponivel` + BK, `inadimplentes`) estão fiéis, com o número 199 do código. R4–R6 formam uma partição completa (ativos/inativos para o vendedor e `sem venda` = nunca comprou com o vendedor, P4). O resumo diz que os bloqueios vêm antes.

**Pontos de atenção: parcial**
- **O que a descrição diz:** (1) o nome da R1 "cita R$ 0, valor que não aparece no código: nome e código podem estar divergentes"; (2) o mesmo para o R$ 200 da R2.
- **O que o `.gobr` diz:** (1) é falso alarme. `nao tem credito` (§6.3: "sem crédito disponível") é exatamente "crédito igual ou menor que R$ 0,00", então nome e código concordam. (2) é real, mas vago demais. O código bloqueia BK com crédito abaixo de R$ 199, então BK com crédito entre R$ 199,00 e R$ 199,99 continua sendo agendado, embora o nome prometa bloquear abaixo de R$ 200. O ponto deveria dizer isso de forma concreta.
- **Causa:** pacote, pelo alerta de número no nome que não reconhece `nao tem credito` como R$ 0. Também código, pelo limiar 199 × 200.

## 3. Conclusão

Das 23 regras, 21 estão fiéis. Os erros de população se concentram onde o redator reescreveu uma condição negativa do pacote: "sem ser de compra única com o vendedor" virou "mais de uma compra com o vendedor" na `regra_217`, o que é um erro na R2 e uma frase contraditória nos pontos de atenção. A parte mais fraca são os pontos de atenção, que não estão totalmente certos em nenhum dos quatro arquivos. Na `regra_151`, o pacote tratou como "não coberto" o que a única regra bloqueia, não emitiu o alerta de filtro temporal e não percebeu que o filtro de segmentação é praticamente redundante com a fonte. Também ficou sem aviso o risco de o bloqueio persistir depois da última semana. Na `regra_160`, a descrição regra a regra está impecável, mas não diz que as seis faixas de fechamento de rota têm a mesma ação e equivalem a uma só regra. Na `regra_233`, um dos dois alertas de nome × código é falso positivo. As correções prioritárias são no pacote (CASCADE-FIRST): alerta para regras consecutivas com a mesma ação, `nao_cobertos` que considere bloqueios com filtro temporal, interseção entre fonte e segmentação, e equivalência `nao tem credito` = R$ 0. No redator, a prioridade é proibir reescrever negações do pacote como afirmações.

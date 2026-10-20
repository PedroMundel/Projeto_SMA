# Revisão de fidelidade: amostra B

Revisor independente. Amostra: regra_012, regra_021, regra_077, regra_094, regra_233 (22 regras `parametros`).
Fontes: `.gobr` (referência), `docs/manual_gobr.txt` (§3.3.1, §4.2, §6.1, §6.3, §6.5, §6.7, §7.3.4, §7.4, §7.6), `docs/premissas.md` (P1–P8), pacotes `data/contexto/<id>.json`.

## 1. Tabela-resumo

| Arquivo | Regras revisadas | Corretas | Imprecisas | Erradas | Resumo ok? | Pontos de atenção ok? |
|---|---|---|---|---|---|---|
| regra_012 | 3 | 3 | 0 | 0 | sim | sim (vazio, nada a apontar) |
| regra_021 | 3 | 3 | 0 | 0 | sim | sim (vazio, nada a apontar) |
| regra_077 | 6 | 5 | 1 | 0 | sim, com ressalva leve | sim (vazio; ver R6) |
| regra_094 | 4 | 4 | 0 | 0 | sim | sim |
| regra_233 | 6 | 6 | 0 | 0 | sim | **não**: falta a divergência nome × código em R2 |
| **Total** | **22** | **21** | **1** | **0** | 5/5 | 4/5 |

## 2. Itens imprecisos ou errados

### regra_012 e regra_021

Nada a apontar. Os dois `.gobr` são idênticos. As três faixas (inativos, ativos, sem venda, todas "para o vendedor") são disjuntas por P4, então não há desconto de cascata. "Média dos inativos/ativos da empresa" corresponde a `frequencia de inativos/ativos da empresa` (manual §7.4). "Nunca compraram com o vendedor" para `sem venda` segue P4.

### regra_077

**R6 "Freq. de 14d para clientes inativos": imprecisa (leve)**
- **O que a descrição diz:** segmento "Clientes inativos"; critério "Clientes que já compraram na empresa e estão fora do ciclo de vida ativo". O resumo diz "Prospects e inativos seguem frequência de 14 dias".
- **O que o `.gobr` diz:** a regra **não tem filtro** (`do time("televendas")` + `frequencia de 14 dias`). É um "pega-tudo" para quem sobrou depois de R1–R5. O critério efetivo do pacote ("já compraram e fora do ciclo de vida ativo com a empresa") está correto. Só que o manual §6.7 define, além de ativo, inativo e prospect, os estágios **ativado** e **reativado**, e esses clientes também caem aqui, a não ser que tenham comprado nos últimos 30 dias (R3). Um usuário que lê o rótulo "inativos" e o resumo conclui que só os inativos recebem 14 dias.
- **Causa:** redator. O pacote está certo. O redator copiou o rótulo do nome da regra, e um ponto de atenção do tipo "R6 não tem filtro: atende todos os clientes restantes, não apenas os inativos" deixaria isso claro. Não é falha do `.gobr` (pega-tudo final é um padrão comum), por isso não marquei os pontos de atenção como "não".

Demais regras (R1–R5) corretas. R4 (prospect com a empresa, P5) não sofre o bloqueio de R3, e o pacote acerta ao omitir R3 de `bloqueios_anteriores`. Ressalva menor no resumo: o time é `todostelevendas ativados` (só vendedores habilitados a gerar agenda, §3.3.1), e a descrição diz apenas "time de televendas". Isso trata de vendedores, não de clientes, por isso não conta como erro.

### regra_094

Nada a apontar. R3 ("sem venda", televendas) é de fato inalcançável: `adimplentes` e `inadimplentes` são complementares (§6.3), então R1 e R2 já esgotam a carteira televendas. Descrição, observação e ponto de atenção estão corretos. R4 (campo, sem filtro) está descrito corretamente como "todos os clientes".

### regra_233

**Pontos de atenção: falha evidente omitida (as linhas da tabela estão corretas)**
- **O que a descrição diz:** linha R2 "Clientes com tipo de cobrança BK e com menos de R$ 199 de crédito disponível", que é fiel ao código. `pontos_de_atencao` está vazio.
- **O que o `.gobr` diz:** o nome da regra é "Não agendar clientes BK com crédito **menor que R$200,00**", mas o código usa `com menos de R$ 199 de credito disponivel`. Clientes BK com crédito disponível entre R$ 199,00 e R$ 199,99 continuam sendo agendados, ao contrário do que o nome promete. É a mesma classe de problema que o alerta "nome cita número que não está no código", só que com valor monetário.
- **Causa:** principalmente o **pacote**, por uma lacuna de cobertura: o alerta de nome × código só verifica números de dias (`numeros_exigidos` de R2 = `[]`, embora `numeros` = `[199]`), então nada chegou ao redator. O redator também tinha o nome da regra em mãos e poderia ter notado.

Demais pontos ok. R1 (`nao tem credito` = sem crédito disponível, §6.3) é coerente com o nome "≤ R$0,00". O "ativos/adimplentes" do nome de R4 e R5 se confirma porque R3 bloqueia os inadimplentes antes.

## 3. Conclusão

A fidelidade é alta: 21 de 22 regras estão corretas e nenhuma está errada. Critérios, frequências, bloqueios, premissas (P4, P5) e a cascata (incluindo a regra inalcançável da 094) estão representados corretamente. Os dois problemas são de proatividade, não de leitura do código. O primeiro: o rótulo "inativos" de uma regra sem filtro (077-R6) esconde que ela é um pega-tudo. O segundo: a divergência R$200 × R$199 na 233 não foi apontada, porque o pacote só compara números de dias entre nome e código. Uma observação sistêmica: as linhas da tabela não repetem os bloqueios anteriores e dependem do resumo para isso. Lido o arquivo inteiro, funciona. Mas uma linha recuperada isoladamente (num chunk de RAG, por exemplo, "Clientes ativos | 7 dias" na 077) perde que quem comprou nos últimos 30 dias não é agendado. Recomendação: estender o alerta nome × código a valores monetários e percentuais.

# Relatório do lote do redator (nuvem)

Execução do roteiro `redator/LOTE_NUVEM.md`, seções 0 a 3, com a estratégia adaptativa: 3 réplicas por
arquivo e mais 2 onde a concordância ficou abaixo de 0,8 ou houve menos de 2 candidatos válidos.

## Conferência (seção 0)

- `python -m unittest tests.test_gobr`: 27 testes, todos passaram (Python 3.13.16 no contêiner, não 3.11).
- `contexto` e `entrada` regenerados: 246 pacotes em `data/contexto`, 3 em `data/contexto_exemplos` e
  249 entradas em `data/entrada_redator`.
- `git status --short data/` não mostrou nenhuma mudança, então o lote seguiu.

## Números gerais

| Item | Valor |
|---|---|
| Arquivos | 249 (246 regras de `referencias/` + 3 exemplos) |
| Réplicas geradas | 917 (747 de base + 156 extras por concordância + 14 extras para arquivos sem válido) |
| Candidatos válidos | 842 (91,8%) |
| Candidatos inválidos | 75 (8,2%) |
| Descrições consolidadas (`.json` + `.md`) | 246 |
| Falhas (`.falha.json`) | 3 |
| `pendentes` ao final | nenhuma linha (`0 réplicas pendentes`) |

Réplicas por arquivo: 171 arquivos com 3, 71 com 5 e 7 com 7.

Validade por réplica: agente_1 237/249, agente_2 234/249, agente_3 235/249, agente_4 65/78,
agente_5 65/78, agente_6 4/7, agente_7 2/7. As réplicas extras têm taxa menor porque vão justamente
para os arquivos mais difíceis.

Candidatos válidos por arquivo: 0 válidos em 3 arquivos, 1 em 5, 2 em 8, 3 em 171, 4 em 2 e 5 em 60.

Todos os subagentes usaram `model: sonnet`, no máximo 20 ao mesmo tempo, com no máximo 5 arquivos cada,
nunca duas réplicas do mesmo arquivo no mesmo subagente e cada réplica num `agente_<k>.json` próprio.

## Erros mais comuns

| Erro | Ocorrências | Candidatos afetados |
|---|---|---|
| `Rn: faltam os números [...]` | 162 | 70 |
| `o pacote tem alertas, mas pontos_de_atencao está vazio` | 7 | 7 |

Nenhum candidato foi rejeitado por número inventado. Os avisos (que não invalidam) foram
`consulta N: números fora do pacote [...]` (11) e `Rn: critério com mais de N palavras` (9).

Quase todos os números faltantes vêm da parte de `condicao_efetiva` que desconta as regras anteriores
(`não (...)` ou listas de faixas complementares). O redator tende a simplificar essas condições e
deixa de fora números redundantes ou que só delimitam o que as regras anteriores já trataram.

## Distribuição da concordância

Considera os 246 arquivos consolidados. Média 0,842, mediana 0,847, mínima 0,539 e máxima 1,0.

| Faixa | Arquivos |
|---|---|
| [0,5; 0,6) | 1 |
| [0,6; 0,7) | 18 |
| [0,7; 0,8) | 43 |
| [0,8; 0,9) | 118 |
| [0,9; 1,0) | 52 |
| 1,0 | 14 |

78 arquivos receberam réplicas extras. Mesmo assim, 62 terminaram com concordância abaixo de 0,8 depois
de 5 réplicas: `pendentes` deixa de pedir réplicas ao chegar ao máximo de 5, como previsto.

## Arquivos com falha

Os três abaixo continuaram sem candidato válido depois de 5 réplicas e de mais 2 (7 no total), como manda
o roteiro. Ficaram registrados como `.falha.json`.

- **regra_178**: R6 e R7 falham sempre. R6 é `há pelo menos 15 dias e não (há pelo menos 30 dias) e não
  (há pelo menos 60 dias)`; o "não 60" é redundante e o redator escreve "entre 15 e 29 dias", sem o 60.
  R7 traz o mesmo padrão com 8/15/30/60.
- **regra_184**: R13 é a regra de fechamento. Ela enumera as faixas complementares de frequência histórica
  (menos de 7, entre 8 e 13, entre 15 e 27, entre 29 e 55, entre 57 e 83, mais de 84), mais
  `nos últimos 0 dias` e `360 dias`. Nenhuma réplica transcreveu todas as faixas.
- **regra_208**: R8, R9 e R11 exigem 89 e 120 vindos do complemento `frequência histórica de até 89 dias
  ou de mais de 120 dias`, que o redator resume.

## Os 10 arquivos de menor concordância

| Arquivo | Concordância | Válidos | Escolhido |
|---|---|---|---|
| regra_151 | 0,539 | 5/5 | agente_3.json |
| regra_115 | 0,604 | 5/5 | agente_2.json |
| regra_032 | 0,619 | 4/5 | agente_4.json |
| regra_217 | 0,620 | 5/5 | agente_3.json |
| regra_071 | 0,623 | 5/5 | agente_2.json |
| regra_163 | 0,628 | 5/5 | agente_2.json |
| regra_138 | 0,637 | 5/5 | agente_4.json |
| regra_189 | 0,645 | 5/5 | agente_2.json |
| regra_164 | 0,659 | 5/5 | agente_2.json |
| regra_237 | 0,667 | 5/5 | agente_2.json |

## Pontos que parecem errados ou merecem revisão (nada foi editado)

1. **Concordância 1,0 com um único válido.** Em `gobr/consensus.py`, `choose` devolve concordância 1,0
   quando só um candidato é válido. Cinco arquivos ficaram assim e aparecem na faixa 1,0 sem nenhuma
   concordância real: regra_135 (1/7), regra_160 (1/7), regra_171 (1/5), regra_186 (1/5) e
   regra_212 (1/5). Convém revisá-los à mão e talvez marcar esse caso de outro jeito (por exemplo, `null`).
2. **Números redundantes em `condicao_efetiva`.** O pacote não simplifica negações em cascata (por exemplo
   `não (≥30) e não (≥60)`), e o validador exige todos os números da condição. Isso explica as três falhas
   e a maior parte dos 75 inválidos. Uma das duas peças pode merecer ajuste: simplificar a condição em
   `gobr/` ou exigir só os números não redundantes. O prompt (item 2) manda copiar todo número, então o
   validador está coerente com ele.
3. **Campo `modelo` fixo.** `_meta.modelo` vem da constante `MODEL = "claude-sonnet-5-5"` em
   `gobr/__main__.py`, não do modelo que de fato atendeu cada subagente (os subagentes foram pedidos com o
   alias `sonnet`).
4. **Concordância baixa persistente.** 62 arquivos ficaram abaixo de 0,8 mesmo com 5 réplicas válidas,
   quase todos 5/5. A medida é textual (`similarity` sobre segmento, critério, frequência e observação), e
   parte dessa divergência é só de redação, não de significado.
5. **Saídas antigas sobrescritas.** `data/descricoes/` já tinha 20 descrições versionadas de um piloto
   anterior (regra_002, 008, 018, ...). A consolidação regravou todas com as versões deste lote; nenhuma
   delas está entre as falhas, então não sobrou arquivo antigo misturado.
6. **Versão do Python.** O contêiner tem Python 3.13, não 3.11. Os testes passaram mesmo assim.

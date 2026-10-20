# Correções depois do lote na nuvem

Complementa `RELATORIO_LOTE.md`. Pacote de contexto agora na versão 5 (as seções até "Achado novo de
modelagem" descrevem o v4; o v5 está em "Correções da avaliação (v5)").

## O que mudou

| Item do relatório | Correção | Onde |
|---|---|---|
| Falhas por números redundantes | `cadastrado faz N dias` virou dimensão de intervalo (dias desde o cadastro, sempre ≥ 0), e a cascata reduz negações como `≥15 e não ≥30 e não ≥60` para "há pelo menos 15 e menos de 30 dias". O pacote passou a trazer `numeros_exigidos` por regra: numa condição com várias alternativas ("OU"), só são exigidos os limites dos critérios da própria regra que aparecem em todas as alternativas. Exclusões que vêm da cascata continuam permitidas, mas deixam de ser obrigatórias. Números inventados continuam proibidos. | `gobr/catalogue.py`, `gobr/dims.py`, `gobr/context.py`, `gobr/validate.py` |
| Concordância 1,0 com um só candidato válido | A concordância passa a ser `null` ("sem medida"), e `pendentes` pede réplicas extras nesses casos. | `gobr/consensus.py`, `gobr/__main__.py` |
| "compraram nos últimos 0 dias" | Passa a sair como "compraram hoje". | `gobr/dims.py` |

## Regeração

Só 10 arquivos mudaram de significado com as correções: regra_003, 144, 155, 158, 171, 174, 178, 184, 190 e 201. Nos outros, a entrada do redator é idêntica à que o lote na nuvem usou, e os candidatos de `candidatos_v2/` foram reavaliados com o validador novo.

- `candidatos_v3/`: 184, 212 e 160 (+2 réplicas adaptativas). Os demais arquivos de lá foram substituídos pelo v4.
- `candidatos_v4/`: os 9 arquivos com regra de cadastro, com 3 réplicas e mais 2 onde a concordância ficou abaixo de 0,8.
- Consolidação na ordem v2 → v3 → v4: cada versão sobrescreve a anterior nos arquivos que ela cobre.

## Resultado final

| | |
|---|---|
| Descrições | 249 de 249 (nenhuma falha) |
| Concordância | média 0,836, mediana 0,841; 67 arquivos abaixo de 0,8 |
| Concordância sem medida | nenhum arquivo |

## Achado novo de modelagem (regra_178)

Com o cadastro modelado como intervalo, a cascata mostrou que o bloqueio "Clientes que nunca compraram
com a empresa" (`cadastrado faz 7 dias` + `nao agendar`) vem antes da escada de leads (8, 15, 30 e 60
dias). Pelo manual (§6.11), `cadastrado faz N dias` significa cadastrado há **pelo menos** N dias, então o
bloqueio pega todos os leads com 7 dias ou mais. A escada inteira nunca é aplicada, e a descrição
registra isso nos pontos de atenção.

## Correções da avaliação (v5)

A revisão por amostra (`docs/avaliacao/`) achou seis problemas na camada determinística, todos
corrigidos no pacote v5 (`gobr/catalogue.py`, `gobr/dims.py`, `gobr/cascade.py`, `gobr/context.py`):

1. Pessoa física/jurídica deixou de ser binária: há também "sem tipo de pessoa definido".
2. O filtro de segmentação fica visível; só as fontes declaradas são ocultadas.
3. Regra sem ação não consome clientes na cascata.
4. Ativo/inativo para o vendedor implica compra registrada com ele (P4/P5).
5. O alerta nome × código olha as definições de origem e também valores em R$.
6. `do historico` usa o histórico de visitas, e o mínimo/máximo limita a frequência (P9).

As entradas do redator de 51 arquivos mudaram. Eles foram regerados em `candidatos_v5/`: 3 réplicas
cada (153) e mais 2 em 27 arquivos com concordância abaixo de 0,8 ou sem 2 candidatos válidos (54), num
total de 207 réplicas, das quais 203 são válidas. A consolidação passa a ser v2 → v3 → v4 → v5.

| | |
|---|---|
| Descrições | 249 de 249 (nenhuma falha) |
| Candidatos finais | 902 de 911 válidos |
| Concordância | média 0,838, mediana 0,843; 71 arquivos abaixo de 0,8 |
| Concordância nos 51 do v5 | média 0,787; 25 abaixo de 0,8 (menor: regra_032 e 151, 0,56) |
| Concordância sem medida | nenhum arquivo |

Nos 198 arquivos fora do v5 só mudou o `_meta` (versão do pacote); o texto escolhido é o mesmo.

## Arquivos obsoletos

Onze `.falha.json` não valem mais: os 3 do lote na nuvem (regra_178, 184, 208), 3 de consolidações
intermediárias (regra_163, 201, 230) e 5 que a passada do v2 grava com o pacote v5 antes de o v5
sobrescrever o arquivo (regra_153, 166, 176, 177, 233). Todos tinham um `.json` válido ao lado e foram
removidos.

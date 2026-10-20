# Correções depois do lote na nuvem

Complementa `RELATORIO_LOTE.md`. Pacote de contexto agora na versão 4.

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

## Arquivos obsoletos

Seis `.falha.json` não valem mais: os 3 do lote na nuvem (regra_178, 184, 208) e 3 de consolidações
intermediárias (regra_163, 201, 230). Todos têm um `.json` válido ao lado e podem ser apagados.

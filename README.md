# Assistente GoBR: explicações das regras de negócio

Projeto da disciplina de Sistemas Multiagentes (UFG, 2026-2). O objetivo final é um agente de
conversação, com LangGraph e RAG, que ajude o usuário a escrever regras de parametrização do Govendas na
DSL **GoBR** e aponte falhas na modelagem comercial.

Esta etapa gera a **explicação em linguagem de negócio de cada regra GoBR já existente**: 246 arquivos de
`trabalho/trabalho/referencias/` mais os 3 exemplos. Essas explicações formam a base que o RAG vai indexar
para recuperar exemplos parecidos com o que o usuário descrever.

Relatório completo da etapa: [docs/relatorio_explicacoes.md](docs/relatorio_explicacoes.md).

## Como funciona

```
.gobr ──► camada determinística (gobr/) ──► pacote de contexto ──► redator (LLM) ──► validador ──► concordância ──► descrição
          parser + cascata + alertas        significado já resolvido  só redige texto   números e nomes  escolhe a réplica
```

1. **Camada determinística** (`gobr/`, só biblioteca padrão do Python): lê o `.gobr`, traduz cada
   cláusula pelo catálogo do manual e calcula a **cascata**. As regras `parametros` são avaliadas em ordem,
   e quem foi tratado por uma regra não é reprocessado pelas seguintes (manual §7.6). A condição efetiva de
   cada regra já sai descontada, junto com alertas de modelagem: regra que nunca é aplicada, bloqueio fora
   de ordem, nome divergente do código, lacunas.
2. **Redator** (`redator/prompt_redator.md`): um LLM recebe o pacote e só escreve o texto, um JSON por
   arquivo, no estilo das tabelas dos exemplos do professor. Nesta etapa os redatores foram subagentes do
   Claude Code (Sonnet). O contrato aceita outro backend, como Ollama.
3. **Validador** (`gobr/validate.py`): rejeita o texto que omite um limite de dias exigido, inventa um
   número, altera o nome de uma regra ou omite os pontos de atenção.
4. **Concordância** (`gobr/consensus.py`): gera 3 réplicas por arquivo, mais 2 quando a concordância fica
   abaixo de 0,8, e escolhe a réplica válida mais próxima das demais.

As ambiguidades do manual foram resolvidas como premissas explícitas, de P1 a P8, em
[docs/premissas.md](docs/premissas.md).

## Estrutura

| Caminho | Conteúdo |
|---|---|
| `gobr/` | camada determinística, validador, concordância e CLI |
| `tests/test_gobr.py` | 36 testes (`unittest`) |
| `redator/` | prompt congelado, exemplos do prompt e roteiro do lote na nuvem |
| `data/contexto/`, `data/contexto_exemplos/` | pacote de contexto completo por arquivo (v5) |
| `data/entrada_redator/` | visão do pacote que o redator lê |
| `data/candidatos_v2/`, `_v3/`, `_v4/`, `_v5/` | réplicas geradas pelo redator (lote na nuvem e regerações) |
| `data/descricoes/` | **resultado**: `<arquivo>.md` (tabela) e `<arquivo>.json` (com `_meta` de procedência) |
| `docs/` | premissas, avaliação, relatório e texto do manual GoBR |
| `research/` | pesquisas que embasaram as decisões |
| `data/candidatos/`, `data/candidatos_piloto/` | piloto e calibração (experimentos iniciais) |

## Como reproduzir

Requer Python 3.11 ou mais novo. Não há dependências externas.

```bash
python -m unittest tests.test_gobr
```

```bash
python -m gobr contexto trabalho/trabalho/referencias data/contexto
```

```bash
python -m gobr entrada data/contexto data/entrada_redator
```

```bash
python -m gobr pendentes data/candidatos_v2 data/entrada_redator --contexto data/contexto data/contexto_exemplos
```

```bash
python -m gobr consolidar data/candidatos_v2 data/descricoes --contexto data/contexto data/contexto_exemplos --prompt redator/prompt_redator.md
```

Para reproduzir exatamente `data/descricoes/`, consolide `candidatos_v2`, depois `candidatos_v3`,
`candidatos_v4` e por fim `candidatos_v5`: cada versão sobrescreve a anterior nos arquivos que ela cobre (ver
[data/descricoes/RELATORIO_CORRECOES.md](data/descricoes/RELATORIO_CORRECOES.md)). O passo do redator
(gerar as réplicas listadas por `pendentes`) está descrito em [redator/LOTE_NUVEM.md](redator/LOTE_NUVEM.md). `python -m gobr cobertura <dir>` lista as cláusulas que o
parser não reconheceu.

## Resultado

- 249 de 249 arquivos descritos e validados, sem números inventados.
- Nos dois exemplos que servem de teste independente, 9 de 9 itens do gabarito batem em critério, limite
  e frequência ([docs/avaliacao/gabaritos.md](docs/avaliacao/gabaritos.md)).
- Na revisão independente por amostra aleatória, 21 de 22 regras estão corretas e nenhuma errada. Na
  amostra dos arquivos de menor concordância havia erros; as seis causas na camada determinística foram
  corrigidas no pacote v5 e os 51 arquivos afetados foram regerados. Na reavaliação cega desses
  arquivos, as regras erradas caíram de 7 para 1 em 23 (relatório, seções 5.2 e 5.3).
- 77 dos 246 arquivos do corpus têm algum alerta de modelagem: regras que nunca são aplicadas, nomes
  divergentes do código, escopos misturados, lacunas e outros. São esses achados que o agente vai usar
  para ser proativo.

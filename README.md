# Assistente GoBR: explicações das regras de negócio

Projeto da disciplina de Sistemas Multiagentes (UFG, 2026-2). O objetivo final é um agente de
conversação, com LangGraph e RAG, que ajude o usuário a escrever regras de parametrização do Govendas na
DSL **GoBR** e aponte falhas na modelagem comercial.

Esta etapa gera a **explicação em linguagem de negócio de cada regra GoBR já existente**: 246 arquivos de
`trabalho/trabalho/referencias/` mais os 3 exemplos. Essas explicações formam a base que o RAG vai indexar
para recuperar exemplos parecidos com o que o usuário descrever.

Relatório completo da etapa: [docs/relatorio_explicacoes.md](docs/relatorio_explicacoes.md).

A segunda etapa **indexa essas explicações com embeddings** (`gobr/index.py`): dada a descrição de negócio
do usuário, devolve as regras existentes mais parecidas, com o `.gobr` de exemplo. Relatório:
[docs/relatorio_indexacao.md](docs/relatorio_indexacao.md).

A terceira etapa **indexa o manual GoBR**: `gobr/manual.py` extrai do PDF seções, tabelas e exemplos de
código, e `gobr/manual_search.py` busca a seção certa por embeddings, BM25 ou a fusão dos dois. Relatório:
[docs/relatorio_manual.md](docs/relatorio_manual.md).

A quarta etapa é o **fluxo básico do agente** em LangGraph (`gobr/agent.py`):

```
descrição ──► buscar (exemplos + manual) ──► redigir (LLM) ──► validar (parser + cascata) ──► responder
                                                ▲                    │ erro
                                                └────────────────────┘ (até 2 tentativas)
```

O LLM é o Qwen3.6-35B-A3B no llama-server do PC com a RTX 5060, acessado por um túnel SSH. A validação diz
se o `.gobr` serve; os alertas da cascata voltam para o usuário como pontos de atenção da modelagem.

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

As ambiguidades do manual foram resolvidas como premissas explícitas, de P1 a P9, em
[docs/premissas.md](docs/premissas.md).

## Estrutura

| Caminho | Conteúdo |
|---|---|
| `gobr/` | camada determinística, validador, concordância, índices, fluxo do agente (`agent.py`) e CLI |
| `tests/test_gobr.py`, `tests/test_index.py`, `tests/test_manual.py`, `tests/test_agent.py` | 36 + 16 + 22 + 14 testes (`unittest`) |
| `redator/` | prompts congelados (redator e `prompt_agente.md`), exemplos do prompt e roteiro do lote na nuvem |
| `data/contexto/`, `data/contexto_exemplos/` | pacote de contexto completo por arquivo (v5) |
| `data/entrada_redator/` | visão do pacote que o redator lê |
| `data/candidatos_v2/`, `_v3/`, `_v4/`, `_v5/` | réplicas geradas pelo redator (lote na nuvem e regerações) |
| `data/descricoes/` | **resultado**: `<arquivo>.md` (tabela) e `<arquivo>.json` (com `_meta` de procedência) |
| `data/indice/<modelo>/` | **índice de embeddings**: vetores, chunks, manifesto e avaliação, um por modelo |
| `data/consultas_avaliacao/` | consultas rotuladas para avaliar a recuperação (gabaritos do professor, 30 cegas e 48 do manual) |
| `data/manual/` | manual extraído do PDF: `secoes.json` (95 seções) e `chunks.jsonl` (463 chunks) |
| `data/indice_manual/<modelo>/` | índice de embeddings do manual e avaliação |
| `data/agente/` | avaliação do agente nos 3 gabaritos: `avaliacao.md` e o `.gobr` e a resposta de cada um, por modo |
| `docs/` | premissas, avaliação, relatórios e texto do manual GoBR |
| `research/` | pesquisas que embasaram as decisões |
| `data/candidatos/`, `data/candidatos_piloto/` | piloto e calibração (experimentos iniciais) |

## Como reproduzir

Requer Python 3.11 ou mais novo. A camada determinística não tem dependências externas; o índice precisa
de `numpy` e `sentence-transformers` (testado com numpy 2.4.4, sentence-transformers 6.1.0 e torch 2.11 com
CUDA). Os testes do índice usam um embedder falso e não baixam modelo. Extrair o manual do PDF
(`python -m gobr manual`) exige `pdfplumber` 0.11.10 (MIT).

```bash
python -m unittest tests.test_gobr tests.test_index tests.test_manual
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

Índice de embeddings (o modelo padrão é `Qwen/Qwen3-Embedding-0.6B`; troque com `--modelo`):

```bash
python -m gobr indexar data/descricoes data/indice/qwen3-0.6b --contexto data/contexto data/contexto_exemplos --gobr trabalho/trabalho/referencias trabalho/trabalho/exemplos
```

```bash
python -m gobr buscar data/indice/qwen3-0.6b "Ativos: compra nos últimos 30 dias, 14 dias. Inativos: mais de 45 dias, 14 dias"
```

```bash
python -m gobr avaliar-indice data/indice/qwen3-0.6b --consultas data/consultas_avaliacao/ouro.json data/consultas_avaliacao/cegas.json
```

Manual (extração, índice, busca e avaliação):

```bash
python -m gobr manual trabalho/trabalho/govendas-rules.pdf data/manual
```

```bash
python -m gobr indexar-manual data/manual data/indice_manual/qwen3-0.6b
```

```bash
python -m gobr buscar-manual data/indice_manual/qwen3-0.6b "frequencia fixa semanal" -k 3
```

```bash
python -m gobr avaliar-manual data/indice_manual/qwen3-0.6b --consultas data/consultas_avaliacao/manual.json
```

Agente (exige `langgraph` 1.2.20 e `openai` 3.49.0, e o llama-server do PC no ar). Num terminal, suba o
servidor no PC e abra o túnel na mesma conexão (`-c 32768` cabe o manual inteiro; com RAG, 8192 basta):

```bash
ssh -L 8080:127.0.0.1:8080 pc "& D:\tools\llama.cpp-b11770\llama-server.exe -m D:\tools\models\Qwen3.6-35B-A3B-UD-IQ4_XS.gguf -ngl 999 --n-cpu-moe 30 -c 32768 -np 1 --jinja --host 127.0.0.1 --port 8080"
```

O servidor continua vivo no PC depois que a conexão cai; encerre-o com
`ssh pc "Get-Process llama-server | Stop-Process"`.

Em outro, rode o agente ou a avaliação nos 3 gabaritos (a busca tira o próprio gabarito e os de mesma estrutura):

```bash
python -m gobr agente "Ativos: compra nos últimos 30 dias, 14 dias. Inativos: mais de 45 dias, 28 dias"
```

```bash
python -m gobr avaliar-agente data/agente/rag --consultas data/consultas_avaliacao/ouro.json --gabaritos trabalho/trabalho/exemplos
```

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
- Recuperação: os 3 gabaritos do professor voltam em 1º lugar e, das 30 consultas cegas, 28 voltam em 1º
  e todas no top-5. O vetor do arquivo, reordenado pelos números em comum, ganhou do multi-vetor
  ([docs/relatorio_indexacao.md](docs/relatorio_indexacao.md)).
- Manual: em 48 consultas rotuladas, a busca híbrida (embeddings + BM25) põe a seção certa no top-5 em todas
  ([docs/relatorio_manual.md](docs/relatorio_manual.md)).
- Agente: nos 3 exemplos do professor, sem o próprio gabarito na busca, 2 de 3 `.gobr` passam na validação
  com RAG do manual (185 s para os 3) e 2 de 3 com o manual inteiro no prompt (548 s). A validação não pega
  erros de significado, como "agendar inadimplentes autorizados" virar `nao agendar`
  ([docs/relatorio_fluxo.md](docs/relatorio_fluxo.md), [data/agente/avaliacao.md](data/agente/avaliacao.md)).

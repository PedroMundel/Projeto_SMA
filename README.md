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

A quarta etapa foi o fluxo básico em LangGraph (busca fixa, redação e validação; relatório em
[docs/relatorio_fluxo.md](docs/relatorio_fluxo.md)). A quinta é o **fluxo agêntico** (`gobr/agent.py`): o
LLM decide quando buscar mais exemplos ou o manual e quando perguntar ao usuário, e o grafo valida e confere
tudo o que ele entrega ([docs/desenho_agente.md](docs/desenho_agente.md)):

```
pedido ─► triagem (LLM extrai os segmentos; o código vê o que falta) ─(lacunas)─► pergunta ao usuário ─► triagem
   └─► preparar (busca inicial + tabela de segmentos) ─► agente (LLM)
                                                    ┌─ buscar_exemplos / buscar_manual ─► agente
                                                    ├─ perguntar_usuario (pausa e espera a resposta) ─► agente
                                                    └─ entrega ─► validar ─(erro)─► agente
                                                                     └─(ok)─► conferir ─(divergência, 1ª vez)─► agente
                                                                                  └─► responder
```

A sexta etapa dá ao agente **memória de contexto** (`gobr/memory.py`, [docs/desenho_memoria.md](docs/desenho_memoria.md),
[docs/relatorio_memoria.md](docs/relatorio_memoria.md)): a conversa continua depois da primeira resposta e
sobrevive ao fechamento do programa (`SqliteSaver` do LangGraph, um banco local). A cada mensagem, o LLM diz o
que ela é e que linhas do pedido mudam, e o código aplica:

```
mensagem ─► receber ─(1º pedido)─► triagem ─► ... ─► responder ─────────────┐
               └─(já há pedido)─► interpretar ─(mudança, pedido novo)─► triagem  │
                                      ├─(dúvida)─► explicar ───────────────────┤
                                      └─(volta)─► desfazer ────────────────────┴─► lembrar (pedido, versões, turnos)
```

O LLM é o Qwen3.6-35B-A3B num llama-server local, numa RTX 5060. O validador
(parser + cascata) diz se o `.gobr` serve. Na conferência, o código compara a ação e a frequência de cada
regra com o segmento da triagem, e o conferente (LLM) compara com o pedido o que cada regra faz, segundo o
pacote. Os alertas da cascata voltam para o usuário como pontos de atenção da modelagem.

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
| `gobr/` | camada determinística, validador, concordância, índices, fluxo do agente (`agent.py`), memória da conversa (`memory.py`, avaliada por `memory_eval.py`) e CLI |
| `tests/test_gobr.py`, `tests/test_index.py`, `tests/test_manual.py`, `tests/test_agent.py`, `tests/test_memory.py` | 36 + 16 + 22 + 51 + 67 testes (`unittest`) |
| `redator/` | prompts congelados (redator, `prompt_agente.md`, `prompt_conferente.md`, `prompt_triagem.md`, `prompt_interprete.md` e `prompt_explicar.md`), exemplos do prompt e roteiro do lote na nuvem |
| `data/contexto/`, `data/contexto_exemplos/` | pacote de contexto completo por arquivo (v5) |
| `data/entrada_redator/` | visão do pacote que o redator lê |
| `data/candidatos_v2/`, `_v3/`, `_v4/`, `_v5/` | réplicas geradas pelo redator (lote na nuvem e regerações) |
| `data/descricoes/` | **resultado**: `<arquivo>.md` (tabela) e `<arquivo>.json` (com `_meta` de procedência) |
| `data/indice/<modelo>/` | **índice de embeddings**: vetores, chunks, manifesto e avaliação, um por modelo |
| `data/consultas_avaliacao/` | consultas rotuladas para avaliar a recuperação (gabaritos do professor, 30 cegas e 48 do manual) |
| `data/manual/` | manual extraído do PDF: `secoes.json` (95 seções) e `chunks.jsonl` (463 chunks) |
| `data/indice_manual/<modelo>/` | índice de embeddings do manual e avaliação |
| `data/agente/` | avaliação do agente: fluxo fixo (`avaliacao.md`, `rag/`, `manual_inteiro/`) e agêntico (`avaliacao_agentico.md`, `agentico/`, `perguntas/`, com triagem `agentico_triagem/` e `perguntas_triagem/`, `casos_pergunta.json`) e memória (`avaliacao_memoria.md`, `memoria/`, `casos_memoria.json`, `casos_memoria_novos.json`) |
| `docs/` | premissas, avaliação, relatórios e texto do manual GoBR |
| `research/` | pesquisas que embasaram as decisões |
| `data/candidatos/`, `data/candidatos_piloto/` | piloto e calibração (experimentos iniciais) |

## Como reproduzir

Requer Python 3.11 ou mais novo. A camada determinística não tem dependências externas; o índice precisa
de `numpy` e `sentence-transformers` (testado com numpy 2.4.4, sentence-transformers 6.1.0 e torch 2.11 com
CUDA). Os testes do índice usam um embedder falso e não baixam modelo. Extrair o manual do PDF
(`python -m gobr manual`) exige `pdfplumber` 0.11.10 (MIT). O agente exige `langgraph` 1.2.20, `openai` e, para a
memória, `langgraph-checkpoint-sqlite` 3.1.3 (MIT).

```bash
python -m unittest tests.test_gobr tests.test_index tests.test_manual tests.test_agent tests.test_memory
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

Agente (exige `langgraph` 1.2.20, `langgraph-checkpoint-sqlite` 3.1.3 e `openai` 3.49.0, e o llama-server no ar).
Num terminal, suba o servidor (caminhos da máquina em que foi medido):

```bash
E:/tools/llama.cpp-b11770/llama-server.exe -m E:/tools/models/Qwen3.6-35B-A3B-UD-IQ4_XS.gguf -ngl 999 --n-cpu-moe 30 -c 32768 -np 1 --jinja --host 127.0.0.1 --port 8080
```

Com o servidor na mesma GPU de 8 GB, rode o agente com `CUDA_VISIBLE_DEVICES=-1` (os embeddings vão para a CPU).

Em outro, converse com o agente (ele pode fazer até 2 perguntas; responda no terminal):

```bash
python -m gobr agente "Ativos: compra nos últimos 30 dias, 14 dias. Inativos: mais de 45 dias, 28 dias"
```

Avaliação nos 3 gabaritos (a busca tira o próprio gabarito e os de mesma estrutura):

```bash
python -m gobr avaliar-agente data/agente/agentico --consultas data/consultas_avaliacao/ouro.json --gabaritos trabalho/trabalho/exemplos
```

Perguntas, com o usuário simulado de `data/agente/casos_pergunta.json`:

```bash
python -m gobr avaliar-perguntas data/agente/casos_pergunta.json data/agente/perguntas
```

Conversa com memória: cada linha depois da resposta é um novo turno, e o mesmo nome retoma a conversa em outro
processo (`conversas` lista as guardadas):

```bash
python -m gobr agente --conversa minha-empresa "Ativos: compra nos últimos 30 dias, 14 dias"
```

```bash
python -m gobr conversas
```

Conversas roteirizadas, com as saídas esperadas de cada turno (`--modo concatenada` e `--modo nenhuma` são as
linhas de base):

```bash
python -m gobr avaliar-memoria data/agente/casos_memoria.json data/agente/memoria/memoria
```

Qualidade contra o gabarito (decisão por cliente, igualdade por regra e cosseno; os dois últimos exigem `--consultas`):

```bash
python -m gobr comparar data/agente/final/teste --gabaritos trabalho/trabalho/referencias
```

```bash
python -m gobr igualdade data/agente/final/teste --gabaritos trabalho/trabalho/referencias --consultas data/consultas_avaliacao/teste_qualidade.json
```

Só o conferente, em `.gobr` já escritos:

```bash
python -m gobr conferir data/agente/rag/*.gobr --consultas data/consultas_avaliacao/ouro.json
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
- Fluxo fixo: nos 3 exemplos do professor, sem o próprio gabarito na busca, 2 de 3 `.gobr` passam na validação
  com RAG do manual (185 s para os 3) e 2 de 3 com o manual inteiro no prompt (548 s). A validação não pega
  erros de significado, como "agendar inadimplentes autorizados" virar `nao agendar`
  ([docs/relatorio_fluxo.md](docs/relatorio_fluxo.md), [data/agente/avaliacao.md](data/agente/avaliacao.md)).
- Fluxo agêntico: 3 de 3 passam na validação. O conferente acusa a ação invertida do V1Vidros nas entregas
  antigas e não acusa nada nas outras quatro. Sem a triagem, o agente não perguntava quando faltava um dado
  (0 de 3 casos incompletos). Com a triagem, pergunta nos 3, e a triagem não aponta lacuna nos 3 completos;
  num deles, o próprio agente perguntou time e carteira. Os gabaritos seguem 3/3, em 352 s
  ([docs/relatorio_agente.md](docs/relatorio_agente.md), [data/agente/avaliacao_agentico.md](data/agente/avaliacao_agentico.md)).
- Memória: em 7 conversas escritas com o código congelado, o agente com memória acerta 54 de 54 verificações; com as
  mensagens concatenadas num pedido só, 31; sem memória, 27. Nas 10 conversas que guiaram as correções, 87, 58 e 45 de
  87. São poucas conversas, de um autor só e com uma rodada, e parte da diferença é da verificação "regra intacta"; sem
  ela, nas novas, 46, 30 e 27 de 46 ([docs/relatorio_memoria.md](docs/relatorio_memoria.md),
  [data/agente/avaliacao_memoria.md](data/agente/avaliacao_memoria.md)).
- Qualidade: em 12 arquivos sorteados, com regra escrita antes, a versão sem a reescrita final de formas tira 63,5 de 100 em
  mesma decisão por cliente (antes, 58,1) e 34 de 34 verificações nas conversas. Por regra, 25% saem sintática e 44%
  semanticamente iguais ao gabarito com ele fora da busca; nos 3 exemplos do professor (treino), 8 de 20 e 8 de 20 com a
  reescrita aplicada às saídas prontas. Em uso real, com o gabarito entre os exemplos que o agente pode buscar e o código final, 12 de 20 regras saem iguais; no V1Vidros são as 5 regras do gabarito, em outra ordem. A igualdade ignora a ordem e
  parte da ação (ver as ressalvas do relatório). O
  resto, com o que não deu certo, está em [docs/relatorio_qualidade.md](docs/relatorio_qualidade.md).

# Backend de LLM para o fluxo LangGraph (texto ou imagem para regra GoBR)

Pesquisa de 2026-11-10. Escopo: escolher o backend do LLM do agente (LangGraph + RAG) que recebe uma descrição em texto OU uma imagem de regras de negócio e escreve regras na DSL GoBR. O LLM roda no PC (RTX 5060 8 GB, 32 GB RAM, llama.cpp b11770); o agente roda no notebook (Python 3.11) via túnel SSH `-L 8080:127.0.0.1:8080`.

Convenções: **(não verificado)** = não consegui confirmar na fonte primária. **(inferência)** = conclusão minha. Nomes e versões abaixo foram vistos nas páginas citadas na data acima.

NO-REJECTED: da seção `## Rejected` do `CLAUDE.md` do projeto, nada se aplica a este tema. Ligação relevante: "Batch API com créditos: os US$ 250 valem só para sessões na nuvem" (a opção paga abaixo respeita isso: exige chave e saldo próprios, e não usa os créditos). `research/redator_llm.md` §6.3 foi lido (candidatos Ollama).

---

## 1. Tabela comparativa

| Backend | Evidência de qualidade (pt-BR / código) | Velocidade / VRAM | Entrada de imagem | Saída estruturada | Custo | Esforço de setup | Licença |
|---|---|---|---|---|---|---|---|
| **A. llama-server (já no PC) + `Qwen3.6-35B-A3B-UD-IQ4_XS`** + `mmproj-F16.gguf` (899 MB) | Card HF: LiveCodeBench v6 80,4; SWE-bench Multilingual 67,2 (é multilinguagem de *programação*, não pt-BR). Nenhum benchmark de pt-BR verificado | ~30 tok/s medido pelo Pedro (MoE, experts na CPU). O projetor ocupa ~0,9 GB a mais e vai para a GPU por padrão (`--no-mmproj-offload` evita) | Sim, nativo ("Causal Language Model with Vision Encoder"); `image_url` na `/v1/chat/completions`. Combinação com `--n-cpu-moe` e este build: **não testada** | Sim: `response_format` json_schema e `--json-schema`/`--grammar` documentados | Zero (energia) | Baixo: baixar 1 arquivo (899 MB) + adicionar `--mmproj` | Apache-2.0 (card HF) |
| **B. Ollama no PC + `gemma4`** (12b ou e4b) | Card HF do 12b: MMMLU 83,4; LiveCodeBench v6 72,0; "35+ idiomas de fábrica, 140+ no pré-treino". Sem benchmark pt-BR | `gemma4:12b-it-qat` 7,2 GB e `12b` 7,7-8,0 GB: não cabem com KV em 8 GB (inferência), haverá split CPU/GPU. `gemma4:e4b-it-q4_K_M` 6,6 GB cabe melhor. Velocidade: não medida | Sim, todas as 51 tags listam Text e Image | Sim: `format` com JSON Schema (doc Ollama, ver `redator_llm.md` §6.1) | Zero | Alto: instalar Ollama (não existe no PC), baixar ~7-8 GB, segundo servidor para manter | Apache 2.0 (card HF; a página Ollama não informa) |
| **C. Claude API `claude-sonnet-5-5`** | Doc oficial: "top-tier ... multilingual, coding, image processing" (afirmação do fornecedor, sem número); é o modelo do redator do projeto | Nuvem; sem VRAM; contexto 1M, saída máx. 128K | Sim (lista de modelos com visão inclui `claude-sonnet-5-5`) | Sim, GA: `output_config.format` com `type: "json_schema"`; sem `minLength`/`minimum`/recursão | US$ 2 entrada / US$ 10 saída por MTok; Batch API -50% | Médio: **não há chave configurada**; precisa saldo próprio (os US$ 250 não valem) | Proprietária (API paga) |
| **C2. Claude API `claude-haiku-5-5`** (variante barata de C) | Mesma doc; descrito para "classificação, extração, roteamento"; sem benchmark | Nuvem; mais rápido da linha | Sim | Sim, GA | US$ 0,10 / US$ 0,50 por MTok (prompts até 100K); acima disso US$ 0,50 / US$ 2,50 | Igual a C | Proprietária |

Observação sobre tamanho: o repositório unsloth lista `UD-IQ4_XS` com 17,7 GB; o Pedro mediu 16,5 GB no disco. Provavelmente GB versus GiB (inferência, não verificado).

## 2. Recomendação

**A (llama-server + Qwen3.6-35B-A3B já no PC).** Já está medido a ~30 tok/s, custa zero, tem a mesma API OpenAI para texto, imagem e JSON Schema, e o único download é o `mmproj-F16.gguf` de 899 MB, que o próprio repositório do GGUF já fornece. B só ganharia se a imagem falhar em A. C/C2 ficam como plano de reserva ou juiz, sem depender dos créditos rejeitados.

## 3. Justificativa por opção

### A. llama-server + Qwen3.6-35B-A3B
- Existe e o nome é exato: https://huggingface.co/Qwen/Qwen3.6-35B-A3B (Apache-2.0; 35B totais, 3B ativos; 256 experts, 8 roteados + 1 compartilhado; contexto nativo 262.144; classificado como image-text-to-text).
- O repositório `unsloth/Qwen3.6-35B-A3B-GGUF` **tem** `mmproj`: `mmproj-F16.gguf` 899 MB, `mmproj-BF16.gguf` 903 MB, `mmproj-F32.gguf` 1,79 GB (https://huggingface.co/unsloth/Qwen3.6-35B-A3B-GGUF/tree/main). Uma discussão de abril/2026 perguntava onde estava; a Unsloth respondeu que o arquivo existe (https://huggingface.co/unsloth/Qwen3.6-35B-A3B-GGUF/discussions/1). Escolher o F16 (mesmo tamanho do BF16; qual dá melhor qualidade: não verificado).
- llama-server: `-mm, --mmproj FILE`; `--no-mmproj-offload` mantém o projetor fora da GPU (https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md). README: conteúdo `image_url` com `image_url.url` aceitando URL remota, base64 (`data:image/...;base64`) ou arquivo local (este exige `--media-path` e prefixo `file://`). Para o túnel SSH, usar base64 no corpo da requisição (inferência: arquivo local estaria no PC, não no notebook).
- Saída estruturada: o README diz que `response_format` aceita `{"type": "json_object"}` e o formato de esquema `{"type": "json_schema", "json_schema": {"name": ..., "strict": ..., "schema": {...}}}`. Também há `-j/--json-schema`, `--grammar` na linha de comando e `json_schema`/`grammar` em `/completion`.
- Desligar thinking (três caminhos documentados, escolher um e testar):
  1. Por requisição, `chat_template_kwargs: {"enable_thinking": false}`. O card Qwen mostra isso para vLLM/SGLang; o README do llama.cpp documenta `chat_template_kwargs` como parâmetro genérico do template. A *combinação* (chave `enable_thinking` no llama-server com este template) não está escrita em nenhuma das duas páginas: **testar**. O card diz que Qwen3.6 não suporta `/think` e `/nothink`.
  2. Por requisição, `reasoning_effort: "none"` ("If `none`, reasoning/thinking is disabled").
  3. No servidor, `-rea off` / `--reasoning off` ou `--reasoning-budget 0` ("0 for immediate end").
- Parâmetros de amostragem recomendados no card para modo sem thinking: `temperature=0.7, top_p=0.8, top_k=20, min_p=0.0, presence_penalty=1.5`. Para geração de DSL (código) com saída restrita, usar temperatura baixa é inferência minha; o card tem recomendação separada para código em modo thinking (`temperature=0.6`).
- Riscos:
  - O card da Unsloth não menciona mmproj nem desligar thinking para llama.cpp (só o comando `llama serve -hf ...`).
  - A lista de `docs/multimodal.md` do llama.cpp **não cita Qwen3.6** (cita Gemma 4 E2B/E4B/26B-A4B/31B, Qwen2/2.5 VL, Qwen3 Omni). Que Qwen3.6 funciona com `--mmproj` vem de fichas de comunidade, não da doc oficial.
  - Issue #24831 (llama.cpp build 9683): `--mmproj` + `--n-cpu-moe 999` com Qwen3.6-35B-A3B-UD-Q4_K_M em 2x RTX 3090 abortou com erro fatal no kernel MMQ do CUDA; fechada como "not planned" por inatividade em 2026-08-07, nunca confirmada (https://github.com/ggml-org/llama.cpp/issues/24831). Hardware e build diferentes dos seus, mas é exatamente o padrão MoE-na-CPU + projetor. Também houve relato de segfault ao processar imagem em abril (discussão #1 acima, sem resolução visível).
  - O README consultado é o de `master`; o build b11770 do PC pode não ter todas as flags (`--reasoning`, `--reasoning-budget`) ou campos (`reasoning_effort`): não verificado.
  - Interação de grammar/json_schema com thinking ligado: não verificada. Desligar thinking resolve.
  - VRAM com projetor + KV de 8192/slot em 8 GB: não medida.

### B. Ollama + gemma4
- Existe: https://ollama.com/library/gemma4 (51 tags; todas "Text, Image"). Tags até ~8 GB: `gemma4:e2b-it-qat` 4,3 GB; `gemma4:e4b-it-qat` 6,1 GB; `gemma4:e4b-it-q4_K_M` 6,6 GB; `gemma4:12b-it-qat` 7,2 GB; `gemma4:12b` 7,7-8,0 GB; `gemma4:12b-it-q4_K_M` 8,0 GB. O `gemma4:latest` é o e4b (6,6-9,5 GB, contexto 128K). Em 8 GB de VRAM, com KV, o 12b provavelmente extravasa para a CPU (inferência).
- Card HF `google/gemma-4-12b-it`: Apache 2.0; aceita texto, imagem e áudio; MMMLU 83,4%; LiveCodeBench v6 72,0%; para desligar thinking, `enable_thinking=False` no `apply_chat_template` (o 12B ainda emite bloco de pensamento vazio). Como isso se traduz na API do Ollama: não verificado.
- Estruturado: `format` com JSON Schema, conforme `redator_llm.md` §6.1 (https://docs.ollama.com/capabilities/structured-outputs). A página da biblioteca não menciona saída estruturada nem português.
- O llama.cpp do PC também suporta Gemma 4 com visão (doc multimodal lista E2B, E4B, 26B-A4B, 31B; o 12B não aparece na lista, não verificado). Ou seja, se o Qwen falhar em imagem, um GGUF de Gemma 4 no mesmo llama-server evita instalar Ollama (inferência).
- Contra: instalar um segundo runtime, baixar mais ~7 GB, e o ganho em relação ao Qwen que já roda é incerto.

### C. Claude API (Sonnet 5.5) e C2 (Haiku 5.5)
- IDs exatos: `claude-sonnet-5-5` e `claude-haiku-5-5` (https://platform.claude.com/docs/en/models/overview). Contexto 1M, saída 128K, corte de conhecimento Jun/2026; retirada "não antes de" 28/09/2027 (Sonnet) e 07/10/2027 (Haiku).
- Preços (https://platform.claude.com/docs/en/about-claude/pricing): Sonnet 5.5 US$ 2 / US$ 10 por MTok; leitura de cache US$ 0,10. Haiku 5.5 US$ 0,10 / US$ 0,50 (prompts até 100K) e US$ 0,50 / US$ 2,50 (acima de 100K). Batch API: 50% de desconto. Custo de tokens de imagem: não verificado.
- Visão estável para ambos (https://platform.claude.com/docs/en/build-with-claude/vision; lista inclui `claude-sonnet-5-5` e `claude-haiku-5-5`). Limites de formato/tamanho de imagem: não li.
- Estruturado: GA; parâmetro `output_config.format` (`type: "json_schema"`); `output_format` antigo está obsoleto; recursos de schema sem suporte retornam 400 (recursão, `minimum`/`maximum`, `minLength`/`maxLength`, `additionalProperties` diferente de `false`, etc.) (https://platform.claude.com/docs/en/build-with-claude/structured-outputs). O schema de `redator_llm.md` §7.3 já evita esses recursos.
- Thinking: segundo a doc de modelos, para o Sonnet 5.5 a Models API reporta `thinking.types.disabled.supported = false` (não aceita `thinking: {type: "disabled"}`) e `between_tools.supported = true`. Ou seja, no Sonnet 5.5 o thinking é adaptativo e não dá para desligá-lo totalmente; isso afeta latência e custo de saída (inferência). Para o Haiku 5.5 não verificado.
- Pré-requisitos: chave de API própria e saldo; nenhuma chave está configurada; os US$ 250 estão rejeitados no `CLAUDE.md`.
- Pergunta em aberto: enviar imagens e regras de negócio de clientes a um terceiro. Se houver dados confidenciais, o local (A) é preferível (inferência; não é requisito dito pelo Pedro).

## 4. Cliente Python (PyPI, consultado em 2026-11-10)

| Pacote | Versão | Data | Licença | Python | Observação |
|---|---|---|---|---|---|
| `langgraph` | 1.2.20 | 2026-11-05 | MIT | >=3.10 | Dependências: `langchain-core>=1.4.7,<2`, `langgraph-checkpoint`, `langgraph-prebuilt`, `langgraph-sdk`, `pydantic>=2.7.4`, `xxhash` |
| `langchain-core` | 1.7.7 | 2026-11-10 | MIT | >=3.10,<4 | Já vem como dependência do langgraph |
| `openai` | 3.49.0 | 2026-11-10 | Apache-2.0 | >=3.10 | Cliente para a API OpenAI-compatível do llama-server (`base_url="http://127.0.0.1:8080/v1"`, chave qualquer) |
| `langchain-openai` | 1.7.4 | 2026-11-04 | MIT | >=3.10,<4 | Não necessário (ver abaixo) |
| `ollama` | 0.6.3 | 2026-09-29 | MIT | >=3.8 | Só se escolher B |
| `anthropic` | 2.8.0 | 2026-11-10 | Apache-2.0 | >=3.10 | Só se escolher C |

URLs: https://pypi.org/project/langgraph/ , https://pypi.org/project/langchain-core/1.7.7/ , https://pypi.org/project/openai/ , https://pypi.org/project/langchain-openai/ , https://pypi.org/project/ollama/ , https://pypi.org/project/anthropic/ , dependências do langgraph em https://pypi.org/pypi/langgraph/1.2.20/json .

Compatibilidade com Python 3.11: todos exigem `>=3.10` ou `>=3.8` e nenhum fixa teto abaixo de 4.0, então 3.11 satisfaz (leitura do campo `requires_python`; não li a lista de classifiers).

**Conjunto mínimo recomendado para A:** `langgraph` + `openai`. `langchain-core` e `pydantic` chegam como dependência do langgraph. `langchain-openai` é dispensável: o nó do grafo chama `openai.OpenAI(base_url=...).chat.completions.create(...)` com `response_format` e conteúdo `image_url` (base64) diretamente, e o estado do LangGraph pode ser um `TypedDict`/Pydantic, sem mensagens LangChain (SCALE-FIT; inferência). Só adicionar `langchain-openai` se quiser usar `ChatOpenAI` com `bind_tools`/ToolNode prontos. `ollama` e `anthropic` só entram se B ou C forem escolhidos.

Nota: `openai` está na série 3.x (3.49.0); não conferi o changelog da migração de 2.x para 3.x, então as assinaturas de `chat.completions.create` e `chat.completions.parse` devem ser testadas.

## 5. Plano de verificação mínimo (sem instalar nada agora)

1. Baixar `mmproj-F16.gguf` e subir o `llama-server` com `--mmproj`, mantendo as flags atuais de `--n-cpu-moe`/experts na CPU. Se abortar, testar sem `--n-cpu-moe` (workaround sugerido na issue #24831) ou com `--no-mmproj-offload`.
2. Mandar uma imagem real de regras via `image_url` base64; ver se lê a tabela.
3. Testar `response_format` json_schema com o schema de `redator_llm.md` §7.3 e thinking desligado pelos 3 caminhos; medir tok/s e VRAM com projetor.
4. Só se 1-3 falharem: Gemma 4 GGUF no mesmo llama-server, depois Ollama, depois API Claude.

## 6. Não verificado

- Qualidade de geração em pt-BR e de GoBR (DSL sem corpus público) de qualquer modelo: nenhum benchmark encontrado; as notas LiveCodeBench/SWE-bench não medem pt-BR nem DSL própria.
- Qwen3.6 + `--mmproj` + experts na CPU no build b11770 (só relatos de comunidade; uma issue de crash em hardware diferente).
- Chave `enable_thinking` dentro de `chat_template_kwargs` no llama-server; interação de json_schema com thinking.
- Se o build b11770 tem as flags/campos do README de `master`.
- VRAM real e tok/s com projetor, e com Gemma 4 12b/e4b em 8 GB.
- Suporte do Gemma 4 12b em `docs/multimodal.md` do llama.cpp (lista cita E2B, E4B, 26B-A4B, 31B).
- Como desligar thinking do Gemma 4 pela API do Ollama; licença na página Ollama (só no card HF).
- Preço dos tokens de imagem e limites de imagem da API Claude; se `claude-haiku-5-5` aceita `thinking: disabled`.
- Mudanças de API do `openai` 3.x em relação à 2.x.
- Diferença de tamanho 16,5 GB (disco do Pedro) versus 17,7 GB (HF).

## 7. Dead ends

- `docs/multimodal.md` e README do servidor não mostram o formato de imagem no mesmo lugar; o formato `image_url` veio do README do servidor (`raw.githubusercontent.com`).
- Página da biblioteca Ollama do `gemma4` não informa licença, idiomas nem saída estruturada.
- A página do card unsloth não cobre mmproj/visão em llama.cpp.
- PyPI JSON de `openai`, `anthropic`, `langchain-core` vem truncado; datas obtidas pelas páginas `pypi.org/project/...`.

## 8. Fontes

- https://huggingface.co/Qwen/Qwen3.6-35B-A3B
- https://huggingface.co/unsloth/Qwen3.6-35B-A3B-GGUF (e `/tree/main`, `/discussions/1`)
- https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md
- https://github.com/ggml-org/llama.cpp/blob/master/docs/multimodal.md
- https://github.com/ggml-org/llama.cpp/issues/24831
- https://ollama.com/library/gemma4 e `/tags`
- https://huggingface.co/google/gemma-4-12b-it
- https://platform.claude.com/docs/en/models/overview
- https://platform.claude.com/docs/en/about-claude/pricing
- https://platform.claude.com/docs/en/build-with-claude/structured-outputs
- https://platform.claude.com/docs/en/build-with-claude/vision
- PyPI: ver tabela da seção 4

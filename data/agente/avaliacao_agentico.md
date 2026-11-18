# Avaliação do fluxo agêntico (2026-11-17)

Servidor: llama-server b11770, `Qwen3.6-35B-A3B-UD-IQ4_XS.gguf`, `-c 32768 -np 1 --jinja`, `reasoning_effort="none"`,
temperatura 0. Código e prompts do working tree desta data (prompts na versão 1, ver
`docs/relatorio_agente.md` §4.2). Medido antes de o conferente passar a receber as respostas do usuário às
perguntas (correção posterior; só muda a entrada do conferente quando o agente pergunta, aqui só no V1Vidros).

## 1. Gabaritos (`avaliar-agente`, saídas em `agentico/`)

Comando: `python -m gobr avaliar-agente data/agente/agentico --consultas data/consultas_avaliacao/ouro.json --gabaritos trabalho/trabalho/exemplos`.
Perguntas do agente recebem a resposta padrão ("sem resposta: siga com a premissa mais provável").

| gabarito | aprovado | entregas | passos | perguntas | divergências | regras (gerado/gabarito) | assinatura igual | alertas | s |
|---|---|---|---|---|---|---|---|---|---|
| RegraInfinittoDesign | sim | 1 | 1 | 0 | 0 | 4/5 | não | 1 | 56 |
| RegraMaxlub | sim | 3 | 3 | 0 | 1 | 9/10 | não | 3 | 98 |
| V1Vidros-RegraComercial | sim | 2 | 6 | 2 | 2 | 6/5 | não | 1 | 114 |

Total: 3/3 aprovados em 268 s (fluxo fixo, commit `094e6b1`: 2/3 em 185 s). Rodadas anteriores com o mesmo
prompt: 3/3 (312 s e 221 s), com variação de passos, perguntas e divergências entre rodadas.

## 2. Perguntas (`avaliar-perguntas`, saídas em `perguntas/`)

Comando: `python -m gobr avaliar-perguntas data/agente/casos_pergunta.json data/agente/perguntas`.

| caso | faltava algo | perguntou | perguntas | aprovado | divergências | alertas | s |
|---|---|---|---|---|---|---|---|
| completo_basico | não | não | 0 | sim | 0 | 0 | 26 |
| completo_bloqueio | não | não | 0 | sim | 0 | 0 | 23 |
| completo_prospect | não | não | 0 | sim | 0 | 0 | 27 |
| falta_frequencia | sim | não | 0 | sim | 0 | 0 | 22 |
| falta_criterio | sim | não | 0 | sim | 0 | 0 | 20 |
| acao_ambigua | sim | não | 0 | sim | 0 | 0 | 28 |

Não perguntou em nenhum dos 3 casos incompletos; inventou o que faltava (frequência copiada de outro
segmento, critério escolhido, "tratar à parte" lido como `nao agendar`). Também não perguntou nos completos.

## 3. Conferente sozinho (`conferir`)

Comando: `python -m gobr conferir data/agente/rag/*.gobr data/agente/manual_inteiro/*.gobr trabalho/trabalho/exemplos/{RegraInfinittoDesign,RegraMaxlub,V1Vidros-RegraComercial}.gobr --consultas data/consultas_avaliacao/ouro.json`.

| arquivo | erro conhecido | conferente |
|---|---|---|
| rag/RegraInfinittoDesign | nenhum de ação | confere |
| rag/RegraMaxlub | nenhum de ação | confere |
| rag/V1Vidros | "Agendar inadimplentes autorizados" virou `nao agendar` | acusa a ação oposta |
| manual_inteiro/RegraInfinittoDesign | nenhum de ação | confere |
| manual_inteiro/RegraMaxlub | nenhum de ação | confere |
| manual_inteiro/V1Vidros | o mesmo do rag | acusa a ação oposta |
| gabarito InfinittoDesign | regra "Baixados na Receita" que o pedido não pede | acusa |
| gabarito Maxlub | "Baixados na receita" e regra final de bloqueio, ambas fora do pedido | acusa a regra final; os baixados só numa rodada de duas |
| gabarito V1Vidros | sem regra para "Agendar inadimplentes" ("Nao agendar baixados" está no pedido: "Não agendar: Clientes baixados na receita") | acusa o trecho sem regra; não acusa os baixados (certo) |

Diferenças reais entre pedido e gabarito: 4. O conferente acusou 3 na rodada final (os baixados do Maxlub só
numa rodada de duas), sem falso positivo.

O prompt do conferente foi ajustado olhando as 6 entregas antigas (dois falsos positivos no Maxlub, resolvidos
mostrando os filtros e os bloqueios anteriores na tabela); os 3 gabaritos não foram usados no ajuste.

## 4. Com a triagem estruturada (`docs/desenho_agente.md` §9)

Mesmo servidor e comandos; saídas em `perguntas_triagem/` e `agentico_triagem/`. Código depois das correções
do code-auditor (casamento de nome só exato ou "<segmento>:"). Antes da avaliação completa, uma sonda só da
triagem nos 6 casos: o esquema (enum e inteiro) foi respeitado em todos, 4 a 10 s por chamada; o
`falta_frequencia` virava `nao_agendar` e o prompt da triagem ganhou a regra "linha sem frequência nem
bloqueio → `indefinido`" (ajuste feito vendo o caso).

### 4.1 Perguntas

`python -m gobr avaliar-perguntas data/agente/casos_pergunta.json data/agente/perguntas_triagem`

| caso | faltava algo | lacunas | perguntou | perguntas (triagem + agente) | aprovado | divergências (código + LLM) | alertas | s |
|---|---|---|---|---|---|---|---|---|
| completo_basico | não | 0 | sim | 0 + 2 | sim | 0 + 0 | 0 | 72 |
| completo_bloqueio | não | 0 | não | 0 + 0 | sim | 0 + 0 | 0 | 37 |
| completo_prospect | não | 0 | não | 0 + 0 | sim | 0 + 0 | 0 | 38 |
| falta_frequencia | sim | 1 | sim | 1 + 0 | sim | 0 + 0 | 0 | 58 |
| falta_criterio | sim | 2 | sim | 1 + 0 | sim | 0 + 0 | 0 | 77 |
| acao_ambigua | sim | 1 | sim | 1 + 0 | sim | 0 + 0 | 0 | 129 |

A triagem achou lacuna nos 3 incompletos e em nenhum completo. No `completo_basico`, as 2 perguntas são do
agente, não da triagem: qual time e qual carteira usar (nenhum pedido diz). A rodada anterior, com o casamento
de nome por qualquer prefixo, deu a mesma tabela de perguntas.

### 4.2 Gabaritos

`python -m gobr avaliar-agente data/agente/agentico_triagem --consultas data/consultas_avaliacao/ouro.json --gabaritos trabalho/trabalho/exemplos`

| gabarito | aprovado | entregas | passos | lacunas | perguntas (triagem + agente) | divergências (código + LLM) | regras (gerado/gabarito) | assinatura igual | alertas | s |
|---|---|---|---|---|---|---|---|---|---|---|
| RegraInfinittoDesign | sim | 1 | 1 | 0 | 0 + 0 | 0 + 0 | 4/5 | não | 1 | 56 |
| RegraMaxlub | sim | 3 | 3 | 0 | 0 + 0 | 0 + 1 | 8/10 | não | 1 | 115 |
| V1Vidros-RegraComercial | sim | 2 | 8 | 1 | 1 + 2 | 0 + 0 | 6/5 | não | 2 | 181 |

3/3 em 352 s (sem triagem: 268 s). No V1Vidros, a lacuna é real ("Agendar Inadiplentes" sem frequência); sem
resposta (avaliação em lote), o agente perguntou de novo duas vezes, com outras palavras, e a regra agenda a
cada 14 dias, com a lacuna no aviso.

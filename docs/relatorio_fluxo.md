# Relatório da etapa: fluxo básico de busca (RAG) com LangGraph

## 1. Objetivo

Ligar as etapas anteriores num fluxo LangGraph (dica 5 do enunciado): o usuário descreve as regras de negócio
em texto, o agente recupera exemplos parecidos (índice das descrições) e trechos do manual (índice do manual),
redige o `.gobr` e o valida. A entrada por imagem fica para a entrega do agente completo (decisão do Pedro,
2026-11-10).

## 2. O fluxo (`gobr/agent.py`)

```
descrição ──► buscar ──► redigir ──► validar ──► responder
                            ▲           │ erro e tentativas < 2
                            └───────────┘
```

| Nó | O que faz | Usa |
|---|---|---|
| `buscar` | Embute a descrição uma vez e faz as duas buscas com o mesmo vetor: os 3 arquivos mais parecidos (com a descrição e o `.gobr` de cada um) e as 3 seções do manual | `gobr.index.search`, `gobr.manual_search.search` (híbrido) |
| `redigir` | Monta o prompt (`redator/prompt_agente.md` + pedido + exemplos + manual) e pede o arquivo GoBR num bloco ```gobr | LLM |
| `validar` | Grava o rascunho, roda o parser e a cascata. Erro: nenhum bloco, nenhuma regra, trecho não reconhecido, fonte não declarada, regra sem ação ou número do pedido fora das cláusulas. Alerta: os da cascata (regra inalcançável, lacuna, escopos misturados...) | `gobr.parser`, `gobr.context.build` |
| `responder` | Devolve o `.gobr`, as notas do LLM (o que ficou de fora), os erros que sobraram e os pontos de atenção | — |

Com erro, o grafo volta a `redigir` com a tentativa anterior e a lista de erros, até 2 tentativas. O LLM só
redige: quem decide se o `.gobr` serve é o pacote (`CASCADE-FIRST`), e os alertas da cascata são a parte
"proativa" do enunciado (apontar falhas na modelagem comercial).

## 3. Backend do LLM

| Decisão | Alternativas | Por quê |
|---|---|---|
| llama-server (llama.cpp b11770) com `Qwen3.6-35B-A3B-UD-IQ4_XS.gguf` no PC com a RTX 5060 | Ollama + gemma4; API Claude (Sonnet/Haiku 5.5) | Já instalado e medido a ~30 tok/s, custo zero, API compatível com a da OpenAI. O Ollama exigiria instalar e baixar ~7 GB de um modelo menor; a API Claude exige chave e saldo próprio. Comparação em `research/backend_llm_fluxo.md`. |
| Cliente `openai` 3.49.0 + `langgraph` 1.2.20 | `langchain-openai` | O cliente oficial basta para a API do llama-server; `langchain-openai` seria uma camada a mais. |
| Notebook roda o fluxo e os embeddings; o PC roda só o LLM, pelo túnel `ssh -L 8080:127.0.0.1:8080 pc` | Tudo no PC | Os índices e o código estão no notebook; o modelo de 16,5 GB fica onde está a GPU. |
| Temperatura 0, `seed` 0, sem raciocínio (`reasoning_effort: "none"`) | Raciocínio ligado | Saída mais estável e sem gastar tokens de raciocínio no contexto de 8192. |

## 4. Avaliação (`python -m gobr avaliar-agente`)

Entradas: as descrições dos 3 exemplos do professor (`data/consultas_avaliacao/ouro.json`); gabaritos: os
`.gobr` de `trabalho/trabalho/exemplos/`. A busca tira o próprio gabarito **e todos os arquivos de mesma
assinatura estrutural**, senão o agente só copiaria a resposta.

Critério (escolha do Pedro, refinado na revisão de código): **aprovado** = a validação não acha erro. Isso
quer dizer: parse sem trecho não reconhecido, fontes declaradas, toda regra com ação, e cada número do
pedido numa **cláusula** do `.gobr` (número só no nome da regra não conta) ou citado pelo LLM nas notas
como deixado de fora. Os números do pedido não incluem o 0 nem os rótulos "Regra 01", e "1.500,00" é lido
como 1500.

A primeira versão exigia todos os inteiros da descrição e reprovava os próprios gabaritos: faltavam ao
Maxlub o 0 de "entre 0 e 60 dias" e o 35 da capacidade (o GoBR não tem cláusula para isso), e ao V1Vidros
o 1 a 4 de "Regra 01..04". Com o critério refinado, os gabaritos passam contra as próprias descrições. A
exceção é o 35 do Maxlub, que só passa quando o LLM diz nas notas que o deixou de fora.

Só reportados: assinatura igual à do gabarito, número de regras e alertas. Assinatura igual não serve de aprovação porque o gabarito tem regras que a descrição não pede (o
InfinittoDesign bloqueia "Baixados na Receita Federal", que não está na descrição).

### 4.1 Resultados

Tabelas completas e configuração do servidor em `data/agente/avaliacao.md`; o `.gobr` e a resposta de cada
gabarito, em `data/agente/rag/` e `data/agente/manual_inteiro/`.

| Gabarito | RAG do manual (3 seções) | Manual inteiro no prompt |
|---|---|---|
| RegraInfinittoDesign | não: inventa `atividade da empresa em N dias` nas 2 tentativas | sim, na 1ª |
| RegraMaxlub | sim, na 1ª (8 regras; a capacidade de 35 clientes vai para as notas) | não: não declara o 35 nem depois do erro |
| V1Vidros-RegraComercial | sim, na 1ª | sim, na 1ª |
| **Aprovados** | **2 de 3** | **2 de 3** |
| Tempo dos 3 | 185 s | 548 s sem cache de prompt |
| Prompt | 4 a 5 mil tokens | 22 a 23 mil tokens |

Nenhum `.gobr` gerado tem a assinatura do gabarito, como esperado: o gabarito tem regras que a descrição não
pede, e o agente separa ou junta faixas de outro jeito (4 regras contra 5 no InfinittoDesign, 8 contra 10 no
Maxlub). As três rodadas com RAG deram a mesma tabela, e as duas últimas com o manual inteiro também; com
temperatura 0 e seed fixo, a saída se repetiu.

Manual inteiro × RAG: empate em aprovação (2 de 3). O manual inteiro evitou a cláusula inventada do
InfinittoDesign, mas custa 5 vezes mais tokens e 3 vezes mais tempo, e no Maxlub o modelo deixou de seguir a
instrução das notas. Com 3 casos não dá para dizer que um ganha; o RAG fica como padrão pelo custo.

### 4.2 O que a validação não pega

A validação garante sintaxe, fontes, ações, alcance das regras e presença dos números, não o significado:

- **Ação invertida:** no V1Vidros, "Agendar inadimplentes: clientes inadimplentes autorizados para
  agendamento" virou `nao agendar` nos dois modos. Com RAG, o agente avisa nas notas que não achou cláusula
  para "autorizados", mas mantém o bloqueio.
- **Frequência lida como critério:** na primeira rodada (descrição de teste do README), "30 dias, 14 dias" virou
  duas faixas de recência. A cascata acusou filtros contraditórios, e o prompt passou a explicar o formato
  "Segmento: critério, frequência".
- **Escopos misturados:** com RAG, o V1Vidros mistura recência global e de grupo. A cascata avisa (é alerta,
  não erro), mas o agente não corrige.
- **Raciocínio em comentários:** com RAG, o `.gobr` do Maxlub termina com 17 linhas `#` em que o modelo pensa
  alto sobre uma regra final que não escreveu (apêndice A). O parser ignora comentários, então isso passa.

As frequências de agendamento dos 6 arquivos gerados conferem com as dos pedidos.

Esses casos pedem uma checagem de significado que compare o pacote do `.gobr` gerado (`condicao_efetiva` de
cada regra) com a descrição: é o próximo passo natural, junto com a entrada por imagem.

## 5. Limitações

- Só texto; imagem entra com o `mmproj` do Qwen3.6 na próxima entrega.
- Só 3 casos de avaliação: os resultados mostram onde o fluxo erra, não uma taxa de acerto.
- Um número declarado nas notas conta como tratado, sem conferir se o motivo é verdadeiro.
- O servidor roda com 1 slot: o agente atende um pedido por vez.

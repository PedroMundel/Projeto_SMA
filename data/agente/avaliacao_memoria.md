# Avaliação da memória de contexto (2026-11-24)

Servidor local: llama-server b11770, `Qwen3.6-35B-A3B-UD-IQ4_XS.gguf`, `-c 32768 -np 1 --jinja --n-cpu-moe 30`,
`reasoning_effort="none"`, temperatura 0, RTX 5060; embeddings na CPU. Um turno que termina com erro do validador
ou exceção não passa em nenhuma verificação. Cada configuração rodou uma vez. As saídas (`.md`, uma por conversa,
com as verificações) estão em `memoria/`.

Modos: **memória** (o agente desta etapa; cada turno reabre o banco); **concatenada** (todas as mensagens e
respostas até ali viram um pedido só, sem memória); **nenhuma** (cada mensagem é um pedido novo, o comportamento
da etapa anterior).

## 1. Resumo

| Conjunto | Modo | Verificações | Verificações dos turnos depois do 1º | Sem contar "regra intacta" | Tempo médio dos turnos depois do 1º (s) |
|---|---|---|---|---|---|
| original (10 conversas, 30 turnos) | memória | 87/87 | 67/67 | 65/65 | 26 |
| original | concatenada | 58/87 | 38/67 | 52/65 | 67 |
| original | nenhuma | 45/87 | 25/67 | 45/65 | 37 |
| novo (7 conversas, 18 turnos) | memória | 54/54 | 38/38 | 46/46 | 28 |
| novo | concatenada | 31/54 | 15/38 | 30/46 | 69 |
| novo | nenhuma | 27/54 | 11/38 | 27/46 | 41 |

- O 1º turno de cada conversa é igual nos três modos.
- **O conjunto original guiou correções.** Na 1ª rodada, a memória tinha 85/87: dois bloqueios de inadimplentes
  entraram depois das regras de frequência. A verificação `bloqueia_antes` entrou depois dessa rodada, porque a da
  ação não via o defeito. Nas linhas de base ela foi refeita sobre os arquivos já gerados (3/3 nos dois modos).
- **As linhas de base do conjunto original não foram rodadas de novo:** são da 1ª rodada, antes das duas últimas
  correções, que só agem em turnos de mudança e não são executadas nesses modos. As do conjunto novo são do código final.
- **O conjunto novo** foi escrito com as saídas esperadas antes de rodar e com código e prompts congelados (hashes
  conferidos no fim).
- **"Regra intacta" favorece a memória por construção:** as linhas de base redigem o arquivo inteiro a cada turno, e
  uma regra equivalente escrita de outro jeito conta como mudada. Por isso a coluna sem ela.

## 2. Conjunto original (`casos_memoria.json`)

Comando: `python -m gobr avaliar-memoria data/agente/casos_memoria.json data/agente/memoria/<modo> --modo <modo>`.

### 2.1 Memória (2ª rodada, código final; `memoria/memoria/`)

| caso | turnos | verificações certas | turnos todos certos | tipos | perguntas | maior prompt por turno (tokens) | s |
|---|---|---|---|---|---|---|---|
| muda_frequencia | 3 | 8/8 | 3/3 | inicial, alterar, duvida | 2 0 0 | 15382 4990 1828 | 104 |
| inclui_segmentos | 3 | 10/10 | 3/3 | inicial, alterar, alterar | 0 0 0 | 4770 4403 4123 | 83 |
| remove_segmento | 2 | 7/7 | 2/2 | inicial, alterar | 0 0 | 4922 5200 | 58 |
| desfaz | 4 | 10/10 | 4/4 | inicial, alterar, desfazer, alterar | 2 0 0 0 | 15382 4961 1097 5028 | 117 |
| lembra_resposta | 2 | 6/6 | 2/2 | inicial, alterar | 1 0 | 12889 4530 | 114 |
| completa_depois | 2 | 5/5 | 2/2 | inicial, alterar | 2 0 | 6119 5016 | 88 |
| referencia | 3 | 7/7 | 3/3 | inicial, duvida, alterar | 0 0 0 | 6369 1825 5929 | 115 |
| pedido_novo | 2 | 9/9 | 2/2 | inicial, novo | 2 0 | 15382 3977 | 83 |
| muda_criterio | 2 | 5/5 | 2/2 | inicial, alterar | 2 0 | 15382 5451 | 86 |
| conversa_longa | 7 | 20/20 | 7/7 | inicial, alterar, alterar, alterar, alterar, alterar, duvida | 0 0 0 0 1 0 0 | 4770 4833 5307 4531 4374 5264 2303 | 182 |

Total (memoria): 87/87 verificações

### 2.2 Memória (1ª rodada, antes de `bloqueia_antes` e da retirada da numeração; `memoria/memoria_rodada1/`)

| caso | turnos | verificações certas | turnos todos certos | tipos | perguntas | maior prompt por turno (tokens) | s |
|---|---|---|---|---|---|---|---|
| muda_frequencia | 3 | 8/8 | 3/3 | inicial, alterar, duvida | 2 0 0 | 15382 4973 1828 | 88 |
| inclui_segmentos | 3 | 9/9 | 3/3 | inicial, alterar, alterar | 0 0 1 | 4770 4386 7456 | 124 |
| remove_segmento | 2 | 7/7 | 2/2 | inicial, alterar | 0 0 | 4922 5183 | 56 |
| desfaz | 4 | 10/10 | 4/4 | inicial, alterar, desfazer, alterar | 2 0 0 0 | 15382 4944 1097 5011 | 117 |
| lembra_resposta | 2 | 6/6 | 2/2 | inicial, alterar | 1 0 | 12889 15428 | 143 |
| completa_depois | 2 | 5/5 | 2/2 | inicial, alterar | 2 0 | 6119 4999 | 87 |
| referencia | 3 | 7/7 | 3/3 | inicial, duvida, alterar | 0 0 0 | 6369 1825 5912 | 107 |
| pedido_novo | 2 | 8/8 | 2/2 | inicial, novo | 2 0 | 15382 3977 | 78 |
| muda_criterio | 2 | 5/5 | 2/2 | inicial, alterar | 2 0 | 15382 5434 | 81 |
| conversa_longa | 7 | 19/19 | 7/7 | inicial, alterar, alterar, alterar, alterar, alterar, duvida | 0 0 0 0 2 0 0 | 4770 4816 5290 4514 6868 5496 2452 | 205 |

Total (memoria): 84/84 verificações

### 2.3 Concatenada (sem `bloqueia_antes`: +3/3)

| caso | turnos | verificações certas | turnos todos certos | tipos | perguntas | maior prompt por turno (tokens) | s |
|---|---|---|---|---|---|---|---|
| muda_frequencia | 3 | 7/8 | 2/3 | inicial, inicial, inicial | 2 0 3 | 15382 10138 6200 | 235 |
| inclui_segmentos | 3 | 5/9 | 1/3 | inicial, inicial, inicial | 0 0 0 | 4770 4734 4767 | 100 |
| remove_segmento | 2 | 3/7 | 1/2 | inicial, inicial | 0 0 | 4922 4928 | 63 |
| desfaz | 4 | 4/10 | 1/4 | inicial, inicial, inicial, inicial | 2 0 0 2 | 15382 9103 14916 5733 | 280 |
| lembra_resposta | 2 | 3/6 | 1/2 | inicial, inicial | 1 2 | 12889 5006 | 141 |
| completa_depois | 2 | 3/5 | 1/2 | inicial, inicial | 2 1 | 6119 4386 | 94 |
| referencia | 3 | 6/7 | 2/3 | inicial, inicial, inicial | 0 0 0 | 6369 4581 6279 | 154 |
| pedido_novo | 2 | 8/8 | 2/2 | inicial, inicial | 2 0 | 15382 6857 | 188 |
| muda_criterio | 2 | 3/5 | 1/2 | inicial, inicial | 2 0 | 15382 4776 | 86 |
| conversa_longa | 7 | 13/19 | 3/7 | inicial, inicial, inicial, inicial, inicial, inicial, inicial | 0 2 2 2 2 0 1 | 4770 8370 5874 5558 5817 7650 9318 | 517 |

Total (concatenada): 55/84 verificações

### 2.4 Nenhuma (sem `bloqueia_antes`: +3/3)

| caso | turnos | verificações certas | turnos todos certos | tipos | perguntas | maior prompt por turno (tokens) | s |
|---|---|---|---|---|---|---|---|
| muda_frequencia | 3 | 4/8 | 1/3 | inicial, inicial, inicial | 2 1 1 | 15382 3441 4087 | 106 |
| inclui_segmentos | 3 | 4/9 | 1/3 | inicial, inicial, inicial | 0 0 0 | 4770 3955 3802 | 50 |
| remove_segmento | 2 | 4/7 | 1/2 | inicial, inicial | 0 0 | 4922 10250 | 59 |
| desfaz | 4 | 4/10 | 1/4 | inicial, inicial, inicial, inicial | 2 1 2 1 | 15382 3721 24887 4870 | 234 |
| lembra_resposta | 2 | 3/6 | 1/2 | inicial, inicial | 1 1 | 12889 2857 | 105 |
| completa_depois | 2 | 2/5 | 1/2 | inicial, inicial | 2 1 | 6119 3900 | 74 |
| referencia | 3 | 3/7 | 1/3 | inicial, inicial, inicial | 1 1 2 | 15083 4874 8160 | 260 |
| pedido_novo | 2 | 8/8 | 2/2 | inicial, inicial | 2 0 | 15382 3991 | 88 |
| muda_criterio | 2 | 3/5 | 1/2 | inicial, inicial | 2 1 | 15382 4898 | 101 |
| conversa_longa | 7 | 7/19 | 1/7 | inicial, inicial, inicial, inicial, inicial, inicial, inicial | 0 1 1 0 0 1 2 | 4770 4096 3986 3951 4156 4851 8492 | 230 |

Total (nenhuma): 42/84 verificações

## 3. Conjunto novo (`casos_memoria_novos.json`)

Comando: `python -m gobr avaliar-memoria data/agente/casos_memoria_novos.json data/agente/memoria/novos_<modo> --modo <modo>`.

### 3.1 Memória

| caso | turnos | verificações certas | turnos todos certos | tipos | perguntas | maior prompt por turno (tokens) | s |
|---|---|---|---|---|---|---|---|
| duas_mudancas | 2 | 9/9 | 2/2 | inicial, alterar | 0 0 | 4469 4991 | 59 |
| mudanca_global | 2 | 6/6 | 2/2 | inicial, alterar | 0 0 | 4787 4561 | 47 |
| divide_segmento | 2 | 7/7 | 2/2 | inicial, alterar | 0 0 | 4770 6171 | 88 |
| volta_a_versao_1 | 4 | 8/8 | 4/4 | inicial, alterar, alterar, desfazer | 2 0 0 0 | 15382 5005 5289 1156 | 119 |
| duvida_de_cascata | 3 | 7/7 | 3/3 | inicial, duvida, duvida | 0 0 0 | 4736 1596 2262 | 47 |
| muda_a_resposta | 2 | 7/7 | 2/2 | inicial, alterar | 1 0 | 4743 4280 | 54 |
| informal | 3 | 10/10 | 3/3 | inicial, alterar, alterar | 2 0 0 | 15382 4924 6087 | 123 |

Total (memoria): 54/54 verificações

### 3.2 Concatenada

| caso | turnos | verificações certas | turnos todos certos | tipos | perguntas | maior prompt por turno (tokens) | s |
|---|---|---|---|---|---|---|---|
| duas_mudancas | 2 | 5/9 | 1/2 | inicial, inicial | 0 0 | 4469 4488 | 62 |
| mudanca_global | 2 | 2/6 | 1/2 | inicial, inicial | 0 0 | 4787 12794 | 121 |
| divide_segmento | 2 | 2/7 | 1/2 | inicial, inicial | 0 0 | 4770 10978 | 227 |
| volta_a_versao_1 | 4 | 4/8 | 1/4 | inicial, inicial, inicial, inicial | 2 2 1 2 | 15382 5327 4537 5745 | 241 |
| duvida_de_cascata | 3 | 5/7 | 1/3 | inicial, inicial, inicial | 0 0 0 | 4736 4717 4741 | 90 |
| muda_a_resposta | 2 | 6/7 | 1/2 | inicial, inicial | 1 0 | 4743 4655 | 113 |
| informal | 3 | 7/10 | 1/3 | inicial, inicial, inicial | 2 1 0 | 15382 4553 6489 | 157 |

Total (concatenada): 31/54 verificações

### 3.3 Nenhuma

| caso | turnos | verificações certas | turnos todos certos | tipos | perguntas | maior prompt por turno (tokens) | s |
|---|---|---|---|---|---|---|---|
| duas_mudancas | 2 | 6/9 | 1/2 | inicial, inicial | 0 0 | 4469 4690 | 51 |
| mudanca_global | 2 | 4/6 | 1/2 | inicial, inicial | 0 0 | 4787 3148 | 33 |
| divide_segmento | 2 | 2/7 | 1/2 | inicial, inicial | 0 0 | 4770 16332 | 120 |
| volta_a_versao_1 | 4 | 4/8 | 1/4 | inicial, inicial, inicial, inicial | 2 1 1 1 | 15382 3911 5735 18237 | 158 |
| duvida_de_cascata | 3 | 3/7 | 1/3 | inicial, inicial, inicial | 0 0 2 | 4736 4433 11525 | 185 |
| muda_a_resposta | 2 | 4/7 | 1/2 | inicial, inicial | 1 1 | 4743 3804 | 52 |
| informal | 3 | 4/10 | 1/3 | inicial, inicial, inicial | 2 1 0 | 15382 4984 7672 | 102 |

Total (nenhuma): 27/54 verificações

## 4. Regressão: os 3 gabaritos (`avaliar-agente`, saídas em `memoria/gabaritos/`)

Medida antes das duas últimas correções, que só agem em turnos de mudança.

| gabarito | aprovado | entregas | passos | lacunas | perguntas (triagem + agente) | divergências (código + LLM) | regras (gerado/gabarito) | assinatura igual | alertas | s |
|---|---|---|---|---|---|---|---|---|---|---|
| RegraInfinittoDesign | sim | 1 | 1 | 0 | 0 + 0 | 0 + 0 | 4/5 | não | 1 | 48 |
| RegraMaxlub | sim | 3 | 3 | 0 | 0 + 0 | 0 + 1 | 8/10 | não | 1 | 100 |
| V1Vidros-RegraComercial | sim | 2 | 7 | 1 | 1 + 2 | 0 + 1 | 6/5 | não | 2 | 113 |

## 5. Lido nas conversas, fora das verificações

- **`divide_segmento`:** o "há mais de 120 dias" saiu como última regra sem filtro, e pega também quem nunca comprou.
- **`duas_mudancas` e `duvida_de_cascata`:** o "Inativo" do 1º turno também é uma regra sem filtro; é a forma que os
  exemplos usam para os demais, mas inclui prospects.
- **`muda_a_resposta`:** a linha do pedido que guarda a resposta leva o texto inteiro da pergunta, e a mudança mostrada
  ao usuário fica longa.
- **`inclui_segmentos` (1ª rodada):** nas notas, o modelo raciocinou por mais de 20 linhas sobre o "4." da lista.
- Tamanho do banco: 16,5 MB para 30 turnos na 2ª rodada (0,55 MB por turno); 24,6 MB na 1ª (0,82); 7,7 MB para os 18
  turnos novos (0,43).

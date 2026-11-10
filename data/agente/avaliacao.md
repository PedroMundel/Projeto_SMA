# Avaliação do agente nos 3 gabaritos do professor

Comando: `python -m gobr avaliar-agente data/agente/<modo> --consultas data/consultas_avaliacao/ouro.json
--gabaritos trabalho/trabalho/exemplos [--manual-inteiro]`, em 2026-11-10. LLM: Qwen3.6-35B-A3B-UD-IQ4_XS no
llama-server b11770 (`-ngl 999 --n-cpu-moe 30 -c 32768 -np 1 --jinja`), RTX 5060, temperatura 0, seed 0, sem
raciocínio. A busca tira o próprio gabarito e os arquivos de mesma assinatura.

## rag

| gabarito | aprovado | tentativas | regras (gerado/gabarito) | assinatura igual | alertas | exemplos |
|---|---|---|---|---|---|---|
| RegraInfinittoDesign | não | 2 | 4/5 | não | 2 | regra_197, regra_224, regra_149 |
| RegraMaxlub | sim | 1 | 8/10 | não | 1 | regra_239, regra_197, regra_194 |
| V1Vidros-RegraComercial | sim | 1 | 6/5 | não | 1 | regra_192, regra_191, regra_156 |

Tempo: 185 s para os 3 (prompt de 4 a 5 mil tokens).

## manual_inteiro

| gabarito | aprovado | tentativas | regras (gerado/gabarito) | assinatura igual | alertas | exemplos |
|---|---|---|---|---|---|---|
| RegraInfinittoDesign | sim | 1 | 4/5 | não | 0 | regra_197, regra_224, regra_149 |
| RegraMaxlub | não | 2 | 8/10 | não | 0 | regra_239, regra_197, regra_194 |
| V1Vidros-RegraComercial | sim | 1 | 6/5 | não | 0 | regra_192, regra_191, regra_156 |

Tempo: 548 s para os 3 na rodada sem cache (cada prompt de 22 a 23 mil tokens leva cerca de 140 s para ser
lido, a ~160 tok/s); 118 s na rodada seguinte, com o cache de prompt do llama-server.

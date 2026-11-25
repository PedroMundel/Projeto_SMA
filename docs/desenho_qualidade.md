# Qualidade do agente: o que mudou e como se decide se entra

Escrito em 2026-11-24, antes de sortear e rodar o conjunto de teste.

## Conjuntos

| Papel | Conjunto | Já guiou correções? |
|---|---|---|
| treino | 3 gabaritos, 6 casos de pergunta, 17 conversas (`casos_memoria.json`, `casos_memoria_novos.json`) | sim |
| validação | 10 consultas cegas de fonte única (`cegas_fonte_unica.json`) | sim (3 regressões foram lidas) |
| teste | 12 arquivos sorteados do corpus (`teste_qualidade.json`) e 6 conversas (`casos_memoria_teste.json`) | não |

O sorteio usa a semente 20261124 e filtros automáticos (uma só fonte, 3 a 9 regras, sem regra inalcançável nem trecho não
reconhecido, assinatura única, fora das cegas). As 6 conversas foram escritas antes da validação e não foram rodadas; uma
delas (a resposta com a frequência do grupo) nasceu de um achado da auditoria.

## Regra de decisão

O antigo é o commit `620cae6`; o novo é o código congelado antes do sorteio. Cada um roda o teste uma vez.

1. Corpus: média da nota de `comparar` (por regra do gabarito), com 0 para o pedido não aprovado ou com exceção.
2. Conversas: verificações certas.

O novo entra se não perder em nenhum dos dois. Se perder em algum, fica o antigo, e o relatório conta o que houve.
Sem ajustes depois de ver o teste.

## Segundo teste: a versão enxuta (escrito em 2026-11-24, 20:40, antes de sortear e rodar)

O primeiro teste aprovou a versão completa pela regra acima, mas o ganho veio de casos que estouravam o contexto, e
quase todo o resto do código não mostrou ganho. A versão enxuta é o `620cae6` mais: `fit_context`, `cascade.single_day`,
a ruptura global do catálogo e o medidor (`outcomes`, `comparar`). As peças foram escolhidas depois de ver o primeiro
teste, então ele não pode aprová-la.

- Sorteio novo: 12 arquivos, semente 20261125, mesmos filtros, fora das consultas cegas e dos 12 do primeiro teste.
- Antigo (`620cae6`) e enxuta rodam o conjunto novo uma vez cada, no corpus; a enxuta roda também as 6 conversas.
- As 6 conversas já foram vistas e deram 34/34 nos dois lados: só como regressão; o antigo fica com o 34/34 já medido.
- Regra: a mesma de antes. A enxuta entra se não perder do antigo na média do corpus (0 para reprovado ou exceção) nem
  nas conversas. Se perder, fica o `620cae6`. Sem ajustes depois de ver o teste.

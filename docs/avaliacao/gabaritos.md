# Avaliação contra os gabaritos do professor

Os 3 pares de `trabalho/trabalho/exemplos/` (descrição de negócio em PDF ou mapa mental + `.gobr`) servem
de gabarito. Comparo cada item do gabarito com a descrição gerada em `data/descricoes/`.

**Ressalva:** a Maxlub foi usada como exemplo dentro do prompt do redator, então não é teste
independente. As 3 réplicas reproduziram o exemplo (concordância 1,0). Infinitto e V1 Vidros são teste de
verdade: não aparecem no prompt.

Os gabaritos **não são função pura do `.gobr`**. Eles trazem itens que não existem no código e omitem
itens que existem. A comparação conta como acerto omitir o que não está no código e incluir o que está.

## Infinitto Design (teste)

| Item do gabarito | No `.gobr`? | Descrição gerada | Resultado |
|---|---|---|---|
| Ativo: pedidos nos últimos 60 dias, 14 dias | sim | "compraram com qualquer vendedor da empresa nos últimos 60 dias", 14 dias | igual |
| Risco de inatividade: pedidos entre 60 e 90 dias, 7 dias | sim | "há mais de 60 dias sem comprar com qualquer vendedor da empresa, mas compraram no grupo de vendedores nos últimos 90 dias", 7 dias | igual, com escopo explícito |
| Inativo: sem pedidos há mais de 90 dias, 28 dias | sim (regra sem filtro, "todos os demais") | "há mais de 60 dias sem comprar com qualquer vendedor e nunca compraram no grupo ou estão há mais de 90 dias sem comprar nele", 28 dias | igual, com escopo explícito |
| Prospect: ciclo de vida prospect, 7 dias | sim | "nunca compraram com nenhum vendedor da empresa", 7 dias | igual |
| (não consta) bloqueio de baixados na Receita | sim | bloqueio listado | incluído corretamente |

As faixas "Risco" e "Inativo" ficaram mais técnicas que no PDF porque o próprio código mistura escopos:
"Ativo" usa `recencia de positivacao global` (empresa toda) e "Risco" usa `recencia de positivacao`
(grupo de vendedores). O ponto de atenção gerado avisa disso. É uma falha real de modelagem que o
gabarito não mostra.

## V1 Vidros (teste)

| Item do gabarito | No `.gobr`? | Descrição gerada | Resultado |
|---|---|---|---|
| Regra 01 Ativos: pedido nos últimos 30 dias, 14 dias | sim | "compraram nos últimos 30 dias", 14 dias | igual |
| Regra 02 Risco: pedido nos últimos 45 dias, mas 30 dias sem comprar, 7 dias | sim | "compraram nos últimos 45 dias, mas estão há mais de 30 dias sem comprar", 7 dias | igual |
| Regra 03 Inativos: sem pedidos há mais de 45 dias, 14 dias | sim | "estão há mais de 45 dias sem comprar", 14 dias | igual |
| Regra 04 Prospects: ciclo de vida prospect, 7 dias | sim | "nunca compraram com nenhum vendedor da empresa", 7 dias | igual |
| Não agendar: baixados na receita | sim | bloqueio listado | igual |
| Agendar inadimplentes autorizados | **não** | omitido | omitido corretamente |

O ponto de atenção gerado aponta uma lacuna real: quem só comprou com vendedores de outros grupos não cai
em nenhuma faixa. Isso decorre das premissas P1 e P2 (ver `docs/premissas.md`).

## Maxlub (exemplo do prompt, não é teste)

Todos os 8 itens do gabarito que existem no código batem com a descrição: as 5 faixas de recência com
limites e frequências, os prospects, os inadimplentes e a rota do externo na semana. "Capacidade de
atendimento: 35 clientes (dia)" não está no `.gobr` e foi omitida, como devia. O bloqueio de baixados e a
regra final de "não agendar" estão no código e não no gabarito, e foram incluídos.

## Resumo

| Exemplo | Itens do gabarito presentes no código | Iguais | Itens fora do código omitidos | Itens extras do código incluídos |
|---|---|---|---|---|
| Infinitto (teste) | 4 | 4 | 0 | 1 |
| V1 Vidros (teste) | 5 | 5 | 1 de 1 | 0 |
| Maxlub (prompt) | 8 | 8 | 1 de 1 | 2 |

Nos dois testes independentes, **9 de 9** itens batem em critério, limite de dias e frequência. Nenhum
item foi inventado. A única diferença sistemática é o estilo: quando o código mistura escopos de
recência, a descrição explicita "com qualquer vendedor da empresa" / "no grupo de vendedores", e o
gabarito simplifica.

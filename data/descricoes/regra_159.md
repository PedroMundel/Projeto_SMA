# regra_159.gobr

Regra de frequência por faturamento anual do cliente com a empresa, em três curvas (A, B e C), para os times baby e pet, cada um com seus valores de corte. Para todos os vendedores há ainda a regra padrão: clientes ativos a cada 7 dias e os demais a cada 15 dias. Não há bloqueios de agenda.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Curva C (Baby) | Clientes com total faturado no ano com a empresa menor que R$ 10000 ou valor desconhecido | 45 dias | Vale para o time baby |
| Curva A (Baby) | Clientes com total faturado no ano com a empresa maior que R$ 30000 | 15 dias | Vale para o time baby |
| Curva B (Baby) | Clientes com total faturado no ano com a empresa entre R$ 10000 e R$ 30000 | 30 dias | Vale para o time baby |
| Curva C (Pet) | Clientes com total faturado no ano com a empresa menor que R$ 5000 ou valor desconhecido | 45 dias | Vale para o time pet |
| Curva A (Pet) | Clientes com total faturado no ano com a empresa maior que R$ 20000 | 15 dias | Vale para o time pet |
| Curva B (Pet) | Clientes com total faturado no ano com a empresa entre R$ 5000 e R$ 20000 | 30 dias | Vale para o time pet |
| Ativos | Clientes ativos para o vendedor | 7 dias | Regra padrão para todos os vendedores |
| Inativos | Clientes que não estão ativos para o vendedor | 15 dias | Regra padrão para todos os vendedores |

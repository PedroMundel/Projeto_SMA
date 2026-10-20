# regra_163.gobr

Regra de agendamento do time de televendas dividida em duas carteiras fixas por ramo de atividade: construtora (ramos 15, 16, 3 e 6) e matcom (demais ramos). Em cada carteira, as faixas seguem o relacionamento do cliente com o vendedor: cliente novo, novo relacionamento, regularidade de compra, ruptura e perda de relacionamento. Na carteira construtora, clientes que compraram nos últimos 30 dias deixam de ser agendados. As frequências vão de 7 a 30 dias.

## Carteiras

| Carteira | Descrição |
|---|---|
| construtora | Carteira fixa dos vendedores do time televendas, com os ramos de atividade 15, 16, 3 e 6 |
| matcom | Carteira fixa dos vendedores do time televendas, com os ramos de atividade fora de 15, 16, 3 e 6 |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: venda em 30 dias (Construtoras) | Clientes que compraram nos últimos 30 dias | Não agendar | Vale para a carteira construtora |
| Novo cliente (Construtoras) | Clientes que nunca compraram ou estão há mais de 30 dias sem comprar e não têm vendas para o vendedor | 30 dias |  |
| Novo relacionamento (Construtoras) | Clientes com vendas para o vendedor, uma única compra com ele e mais de 60 dias sem comprar | 21 dias |  |
| Regularidade de compra (Construtoras) | Clientes com vendas para o vendedor e mais de 30 dias sem comprar no grupo, que compraram com ele há até 30 dias ou há mais de 60 dias | 28 dias | Quem tem compra única com o vendedor entra só se comprou no grupo entre 30 e 60 dias atrás |
| Ruptura (Construtoras) | Clientes com mais de 30 dias sem comprar no grupo, que compraram com o vendedor nos últimos 60 dias, mas estão há mais de 30 dias sem comprar com ele | 14 dias | Quem tem compra única com o vendedor entra só se comprou no grupo entre 30 e 60 dias atrás |
| Perdendo relacionamento (Construtoras) | Clientes que nunca compraram com o vendedor e nunca compraram no grupo ou estão há mais de 30 dias sem comprar no grupo | 21 dias | Compra única com o vendedor: entra também quem comprou no grupo há mais de 30 e até 60 dias |
| Novo cliente (Matcom) | Clientes sem vendas para o vendedor | 7 dias |  |
| Novo relacionamento (Matcom) | Clientes com vendas para o vendedor, uma única compra com ele e mais de 30 dias sem comprar | 14 dias |  |
| Compra com regularidade (Matcom) | Clientes com vendas para o vendedor que compraram nos últimos 30 dias, mas estão há mais de 6 dias sem comprar | Pelo histórico de compras, entre 7 e 30 dias | Sem histórico de compras, a frequência fica limitada a no mínimo 7 e no máximo 30 dias |
| Regularidade de compra (Matcom) | Clientes com vendas para o vendedor que compraram no grupo nos últimos 6 dias e compraram com ele há até 30 dias ou há mais de 60 dias | 14 dias | Se não for compra única, entra também quem está há mais de 30 dias sem comprar no grupo |
| Ruptura (Matcom) | Clientes que compraram no grupo nos últimos 6 dias e com o vendedor nos últimos 60 dias, mas estão há mais de 30 dias sem comprar com ele | 7 dias | Se não for compra única, entra também quem está há mais de 30 dias sem comprar no grupo |
| Perdendo relacionamento (Matcom) | Clientes que nunca compraram com o vendedor e nunca compraram no grupo ou compraram no grupo nos últimos 6 dias | 7 dias | Se não for compra única, entra também quem está há mais de 30 dias sem comprar no grupo |

## Pontos de atenção

- As regras misturam a recência de compra medida no grupo de vendedores (como 'Não agendar clientes com venda em 30d (Construtoras)' e 'Estabeleça relacionamento com seu novo cliente (Matcom)') e a medida com o próprio vendedor (como 'Cliente entrando em ruptura (Construtoras)'); faixas de escopos diferentes não se excluem automaticamente e podem se sobrepor ou deixar lacunas.

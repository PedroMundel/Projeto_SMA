# regra_126.gobr

Regra padrão de frequência para três grupos: o time ruptura global, a carteira de televendas e a carteira de campo. O ruptura global atende a cada 14 dias quem está há mais de 31 dias sem comprar com a empresa e não agenda os demais. Em televendas, as faixas combinam ativos, inativos e adimplência, com frequências de 14, 21 e 30 dias, e os inativos inadimplentes não são agendados. O campo atende ativos a cada 7 dias e os demais a cada 15 dias, com parametrização fixa.

## Carteiras

| Carteira | Descrição |
|---|---|
| carteira televendas | Carteira fixa dos vendedores do time de televendas |
| carteira campo | Carteira fixa dos vendedores do time de campo |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Mais de 31 dias sem comprar (ruptura global) | Clientes que estão há mais de 31 dias sem comprar com qualquer vendedor da empresa | 14 dias | Preferência de segunda a sexta, demais dias sem atendimento |
| Bloqueio: compraram nos últimos 31 dias | Clientes que nunca compraram na empresa ou compraram nos últimos 31 dias, exceto os já tratados pelas regras anteriores | Não agendar |  |
| Ativos adimplentes (televendas) | Clientes adimplentes e ativos para o vendedor | 14 dias | Preferência de segunda a sexta, demais dias sem atendimento |
| Ativos inadimplentes (televendas) | Clientes inadimplentes e ativos para o vendedor | 21 dias | Preferência de segunda a sexta, demais dias sem atendimento |
| Inativos adimplentes (televendas) | Clientes adimplentes e inativos para o vendedor | 30 dias | Preferência de segunda a sexta, demais dias sem atendimento |
| Bloqueio: inativos inadimplentes (televendas) | Clientes inadimplentes e inativos para o vendedor | Não agendar |  |
| Sem vendas (televendas) | Clientes sem vendas para o vendedor | 30 dias | Preferência de segunda a sexta, demais dias sem atendimento |
| Ativos (campo) | Clientes ativos para o vendedor | 7 dias | Parametrização fixa: restrição rígida de frequência e dias para o gerador de agendas |
| Inativos (campo) | Clientes não ativos para o vendedor, exceto os já tratados pelas regras anteriores | 15 dias | Parametrização fixa: restrição rígida de frequência e dias para o gerador de agendas |

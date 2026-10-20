# regra_116.gobr

Regras de agendamento dos times televendas e campo. Filiais não são agendadas por nenhum dos dois times. O televendas atende todos os clientes a cada 7 dias, enquanto o campo organiza a frequência pela situação do cliente (ativo, inativo ou sem vendas) e pela adimplência, de 7 a 60 dias.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: filiais | Clientes que são filiais | Não agendar | Vale para os times televendas e campo |
| Televendas: todos os clientes | Clientes de todos os clientes atendidos pelo televendas, exceto os já tratados pela regra anterior | 7 dias | Dias de preferência: segunda a sábado; evita coincidir com os dias do time campo |
| Campo: ativos adimplentes | Clientes adimplentes e ativos para o vendedor | 7 dias |  |
| Campo: ativos inadimplentes | Clientes inadimplentes e ativos para o vendedor | 14 dias |  |
| Campo: inativos adimplentes | Clientes adimplentes e inativos para o vendedor | 30 dias |  |
| Campo: inativos inadimplentes | Clientes inadimplentes e inativos para o vendedor | 60 dias |  |
| Campo: sem vendas | Clientes sem vendas para o vendedor | 7 dias |  |

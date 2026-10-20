# regra_068.gobr

Regra de agendamento com duas carteiras fixas: a do time campo e a do time televendas. No campo, não são agendados clientes do ramo de atividade de id 17, pessoas físicas e, ao final, inativos e inadimplentes ativos; os ativos adimplentes têm frequência de 30 dias e os sem venda, de 21 dias. No televendas, inadimplentes não são agendados, e os adimplentes seguem 14 dias (ativos e sem venda) ou 30 dias (inativos).

## Carteiras

| Carteira | Descrição |
|---|---|
| carteira campo | Carteira fixa dos vendedores do time campo |
| carteira televendas | Carteira fixa dos vendedores do time televendas |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: plano veterinário | Clientes com ramo de atividade de id 17 | Não agendar | Carteira campo |
| Bloqueio: pessoa física | Clientes pessoa física | Não agendar | Carteira campo |
| Ativos adimplentes (campo) | Clientes adimplentes e ativos para o vendedor | 30 dias | Carteira campo |
| Sem venda (campo) | Clientes que nunca compraram com o vendedor | 21 dias | Carteira campo |
| Bloqueio: inadimplentes ou inativos | Clientes inativos para o vendedor ou inadimplentes que sejam ativos para o vendedor | Não agendar | Carteira campo; vale para quem não entrou nas regras de 30 e 21 dias |
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar | Carteira televendas |
| Ativos adimplentes (televendas) | Clientes adimplentes e ativos para o vendedor | 14 dias | Carteira televendas |
| Inativos adimplentes (televendas) | Clientes adimplentes e inativos para o vendedor | 30 dias | Carteira televendas |
| Sem venda (televendas) | Clientes adimplentes que nunca compraram com o vendedor | 14 dias | Carteira televendas |

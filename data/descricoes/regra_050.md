# regra_050.gobr

Regra padrão de frequência aplicada à carteira fixa de todos os vendedores da empresa. Clientes adimplentes são atendidos a cada 7 dias; entre os inadimplentes, os ativos têm frequência de 14 dias e os sem vendas, de 7 dias. Os clientes inativos e inadimplentes não são agendados.

## Carteiras

| Carteira | Descrição |
|---|---|
| empresa toda | Carteira fixa de todos os vendedores da empresa |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Adimplentes | Clientes adimplentes | 7 dias |  |
| Ativos inadimplentes | Clientes inadimplentes e ativos para o vendedor | 14 dias |  |
| Bloqueio: inativos inadimplentes | Clientes inadimplentes e inativos para o vendedor | Não agendar |  |
| Sem vendas | Clientes inadimplentes que nunca compraram com o vendedor | 7 dias |  |

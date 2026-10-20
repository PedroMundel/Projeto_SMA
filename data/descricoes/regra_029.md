# regra_029.gobr

Regra de agendamento da carteira fixa de todos os vendedores da empresa. Clientes inadimplentes e inativos para o vendedor não são agendados, e esse bloqueio vem antes da frequência. A regra final aplica 14 dias aos demais clientes.

## Carteiras

| Carteira | Descrição |
|---|---|
| empresa toda | Carteira fixa de todos os vendedores da empresa |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: inativos inadimplentes | Clientes inadimplentes e inativos para o vendedor | Não agendar |  |
| Todos os clientes | Clientes de toda a carteira, sem distinção | 14 dias | Regra final: vale para quem sobrou do bloqueio anterior |

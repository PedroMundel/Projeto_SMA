# regra_058.gobr

Regra de frequência para duas carteiras fixas: a de televendas e a de campo. Em televendas, inadimplentes são atendidos a cada 14 dias e os adimplentes seguem a frequência calculada pelo histórico de compras, limitada a no máximo 14 dias. Em campo, adimplentes são atendidos a cada 7 dias; entre os inadimplentes, ativos têm 14 dias, inativos 60 dias e clientes sem vendas 14 dias. Não há regras de bloqueio.

## Carteiras

| Carteira | Descrição |
|---|---|
| televendas | Carteira fixa dos vendedores do time de televendas |
| campo | Carteira fixa dos vendedores do time de campo |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Inadimplentes (televendas) | Clientes inadimplentes da carteira de televendas | 14 dias |  |
| Adimplentes (televendas) | Clientes adimplentes da carteira de televendas | Pelo histórico de compras, no máximo 14 dias | Se não houver histórico, a frequência fica limitada a no máximo 14 dias |
| Adimplentes (campo) | Clientes adimplentes da carteira de campo | 7 dias |  |
| Ativos inadimplentes (campo) | Clientes inadimplentes e ativos para o vendedor | 14 dias |  |
| Inativos inadimplentes (campo) | Clientes inadimplentes e inativos para o vendedor | 60 dias |  |
| Sem venda inadimplentes (campo) | Clientes inadimplentes que nunca compraram com o vendedor | 14 dias |  |

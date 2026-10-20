# regra_058.gobr

Regra padrão de frequência para duas carteiras fixas, a de televendas e a de campo. No televendas, inadimplentes são atendidos a cada 14 dias e adimplentes seguem o histórico, limitado a 14 dias. No campo, adimplentes são atendidos a cada 7 dias, e os inadimplentes variam: ativos 14 dias, inativos 60 dias e sem vendas 14 dias. Não há regras de bloqueio.

## Carteiras

| Carteira | Descrição |
|---|---|
| televendas | Carteira fixa dos vendedores do time de televendas |
| campo | Carteira fixa dos vendedores do time de campo |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Inadimplentes (televendas) | Clientes inadimplentes | 14 dias | Carteira televendas |
| Adimplentes (televendas) | Clientes adimplentes | Pelo histórico, no máximo 14 dias | Carteira televendas |
| Adimplentes (campo) | Clientes adimplentes | 7 dias | Carteira campo |
| Ativos inadimplentes (campo) | Clientes inadimplentes e ativos para o vendedor | 14 dias | Carteira campo |
| Inativos inadimplentes (campo) | Clientes inadimplentes e inativos para o vendedor | 60 dias | Carteira campo |
| Sem vendas inadimplentes (campo) | Clientes inadimplentes que nunca compraram com o vendedor | 14 dias | Carteira campo |

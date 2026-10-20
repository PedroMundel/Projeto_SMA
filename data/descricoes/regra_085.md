# regra_085.gobr

Regra padrão de frequência aplicada à carteira fixa de todos os vendedores, em quatro faixas por situação de pagamento e de compra. Clientes adimplentes são atendidos a cada 7 dias; inadimplentes ativos a cada 14 dias e inadimplentes inativos a cada 30 dias. A faixa final trata os inadimplentes sem vendas, a cada 7 dias, de segunda a sexta.

## Carteiras

| Carteira | Descrição |
|---|---|
| empresa perola | Carteira fixa de todos os vendedores da empresa |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Adimplentes | Clientes adimplentes | 7 dias |  |
| Ativos inadimplentes | Clientes inadimplentes e ativos para o vendedor | 14 dias |  |
| Inativos inadimplentes | Clientes inadimplentes e inativos para o vendedor | 30 dias |  |
| Sem vendas inadimplentes | Clientes inadimplentes que nunca compraram com o vendedor | 7 dias | Dias de preferência: segunda, terça, quarta, quinta, sexta; demais dias sem atendimento |

# regra_045.gobr

Regras de frequência para duas carteiras fixas: a de todos os vendedores, exceto a vendedora Sandra, e a carteira da Sandra. Todos os clientes da Sandra são atendidos a cada 7 dias. Na carteira da empresa, a frequência depende da situação do cliente: inativos inadimplentes a cada 30 dias, inativos adimplentes a cada 7 dias e os demais a cada 14 dias. Todas as faixas atendem apenas de segunda a sexta, e não há regra de não agendar.

## Carteiras

| Carteira | Descrição |
|---|---|
| empresa toda | Carteira fixa de todos os vendedores, exceto a vendedora Sandra |
| carteira sandra | Carteira fixa da vendedora Sandra |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Clientes da Sandra | Todos os clientes da carteira da Sandra | 7 dias | Atende de segunda a sexta; demais dias sem atendimento |
| Inativos inadimplentes | Clientes inadimplentes e inativos para o vendedor | 30 dias | Atende de segunda a sexta; demais dias sem atendimento |
| Inativos adimplentes | Clientes adimplentes e inativos para o vendedor, exceto os já tratados pelas regras anteriores | 7 dias | Atende de segunda a sexta; demais dias sem atendimento |
| Demais clientes (não inativos) | Clientes que não são inativos para o vendedor, exceto os já tratados pelas regras anteriores | 14 dias | Atende de segunda a sexta; demais dias sem atendimento |

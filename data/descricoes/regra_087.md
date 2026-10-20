# regra_087.gobr

Regra de frequência para dois times, com uma carteira fixa para cada: televendas e campo. Na carteira televendas, as faixas combinam adimplência e situação de compra (14, 30 e 60 dias), mais os clientes sem venda com 30 dias. Na carteira campo, a frequência depende só da adimplência: 14 dias para adimplentes e 30 dias para inadimplentes. A regra final do campo, para clientes sem venda, nunca é aplicada.

## Carteiras

| Carteira | Descrição |
|---|---|
| carteira televendas | Carteira fixa dos vendedores do time televendas |
| carteira campo | Carteira fixa dos vendedores do time campo |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Televendas: ativos adimplentes | Clientes adimplentes e ativos para o vendedor | 14 dias | Dias de preferência: segunda, terça, quarta, quinta, sexta; demais dias sem atendimento |
| Televendas: ativos inadimplentes | Clientes inadimplentes e ativos para o vendedor | 30 dias | Dias de preferência: segunda, terça, quarta, quinta, sexta; demais dias sem atendimento |
| Televendas: inativos adimplentes | Clientes adimplentes e inativos para o vendedor | 30 dias | Dias de preferência: segunda, terça, quarta, quinta, sexta; demais dias sem atendimento |
| Televendas: inativos inadimplentes | Clientes inadimplentes e inativos para o vendedor | 60 dias | Dias de preferência: segunda, terça, quarta, quinta, sexta; demais dias sem atendimento |
| Televendas: sem venda | Clientes que nunca compraram com o vendedor | 30 dias | Dias de preferência: segunda, terça, quarta, quinta, sexta; demais dias sem atendimento |
| Campo: adimplentes | Clientes adimplentes | 14 dias | Dias de preferência: segunda, terça, quarta, quinta, sexta; demais dias sem atendimento |
| Campo: inadimplentes | Clientes inadimplentes | 30 dias | Dias de preferência: segunda, terça, quarta, quinta, sexta; demais dias sem atendimento |
| Campo: sem venda | Clientes que nunca compraram com o vendedor, exceto os já tratados pelas regras anteriores | 30 dias | Nunca é aplicada: todos esses clientes já foram tratados antes |

## Pontos de atenção

- A regra '30 dias para clientes sem venda (campo)' nunca é aplicada: todos os clientes dela já são tratados por regras anteriores.

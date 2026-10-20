# regra_225.gobr

Regra de agendamento do time de televendas em cinco faixas: prospects e quatro combinações de cliente ativo ou inativo para o vendedor com adimplente ou inadimplente. Todas as faixas atendem de segunda a sábado. Não há bloqueios; as frequências vão de 10 a 21 dias.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Prospects | Clientes que nunca compraram com qualquer vendedor da empresa | 10 dias | Dias de preferência: segunda a sábado; demais dias sem atendimento |
| Ativos adimplentes | Clientes que já compraram com a empresa, adimplentes e ativos para o vendedor | 21 dias | Dias de preferência: segunda a sábado; demais dias sem atendimento |
| Ativos inadimplentes | Clientes que já compraram com a empresa, inadimplentes e ativos para o vendedor | 10 dias | Dias de preferência: segunda a sábado; demais dias sem atendimento |
| Inativos adimplentes | Clientes que já compraram com a empresa, adimplentes e inativos para o vendedor | 14 dias | Dias de preferência: segunda a sábado; demais dias sem atendimento |
| Inativos inadimplentes | Clientes que já compraram com a empresa, inadimplentes e inativos para o vendedor | 21 dias | Dias de preferência: segunda a sábado; demais dias sem atendimento |

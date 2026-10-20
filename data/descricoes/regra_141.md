# regra_141.gobr

Regra de frequência para todos os vendedores habilitados, organizada pela curva do cliente com a empresa (A, B e C) e pela situação de atividade para o vendedor. Curva A: 15 dias para ativos e 7 dias para inativos; curva B: 21 e 14 dias; curva C: 30 e 21 dias. Clientes fora das curvas (prospects) têm frequência de 21 dias. Não há bloqueios de agenda.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Ativos curva A | Clientes curva A com a empresa e ativos para o vendedor | 15 dias |  |
| Inativos curva A | Clientes curva A com a empresa e não ativos para o vendedor | 7 dias |  |
| Ativos curva B | Clientes curva B com a empresa e ativos para o vendedor | 21 dias |  |
| Inativos curva B | Clientes curva B com a empresa e não ativos para o vendedor | 14 dias |  |
| Ativos curva C | Clientes curva C com a empresa e ativos para o vendedor | 30 dias |  |
| Inativos curva C | Clientes curva C com a empresa e não ativos para o vendedor | 21 dias |  |
| Prospects | Clientes fora das curvas A, B e C com a empresa | 21 dias | Regra final: vale para quem sobrou das faixas anteriores |

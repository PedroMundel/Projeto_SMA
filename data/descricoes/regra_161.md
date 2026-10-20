# regra_161.gobr

Regra de frequência para todos os vendedores habilitados, organizada pela curva do cliente na empresa (A, B e C) e pela condição de ativo para o vendedor. Clientes ativos das curvas A e C ficam a cada 15 dias e os da curva B a cada 7 dias. A regra final, de 7 dias, trata os clientes não ativos e os ativos fora das curvas. Não há bloqueios de agenda.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Ativos Curva A | Clientes da curva A com a empresa e ativos para o vendedor | 15 dias |  |
| Ativos Curva B | Clientes da curva B com a empresa e ativos para o vendedor | 7 dias |  |
| Ativos Curva C | Clientes da curva C com a empresa e ativos para o vendedor | 15 dias |  |
| Inativos | Clientes não ativos para o vendedor ou ativos fora das curvas A, B e C com a empresa | 7 dias | Regra final: vale para quem sobrou das faixas anteriores |

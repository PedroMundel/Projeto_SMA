```gobr
version 1.0

time "televendas":
    vendedores todostelevendas ativados

parametros "Prospects":
    do time("televendas")
    quando prospects da empresa
    frequencia de 7 dias

parametros "Ativos":
    do time("televendas")
    quando atividade de 90 dias
    frequencia de 14 dias

parametros "Demais clientes":
    do time("televendas")
    frequencia de 30 dias
```

**Premissas e Observações:**

1.  **Ordem das Regras:** A regra "Ativos" vem antes de "Demais clientes" para garantir que quem comprou nos últimos 90 dias seja capturado pela faixa de 14 dias, sobrando apenas para a regra final quem está inativo há mais de 90 dias (ou não se enquadra na atividade recente).
2.  **Critério "Demais clientes":** Como o GoBR processa em ordem e a primeira regra que se aplica vence, a última regra sem cláusula `quando` (ou com condição genérica implícita de "quem sobrou") captura os clientes que não foram prospects e não tiveram atividade nos últimos 90 dias.
3.  **Cláusula de Atividade:** Utilizou-se `atividade de 90 dias` baseada nos exemplos de `recencia de positivacao` e na seção 6.1 do manual (`atividade de <<tempo>>`), que verifica se o cliente comprou no período especificado.
4.  **Segmento Prospects:** Utilizou-se `prospects da empresa` conforme o manual (seção 6.1 e 6.7), já que a premissa indica que prospects são sempre da empresa.

Pontos de atenção na modelagem:
- O pedido não diz o time (premissa P11). O arquivo usa "televendas": todos os vendedores de televendas habilitados no Govendas.
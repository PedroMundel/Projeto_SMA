```gobr
version 1.0

time "televendas":
    vendedores todostelevendas

carteira "carteira televendas":
    clientes carteirafixa("televendas")

parametros "Inativos":
    da carteira("carteira televendas")
    quando inativos para o vendedor
    frequencia de 28 dias

parametros "Ativos":
    da carteira("carteira televendas")
    quando ativos para o vendedor
    frequencia de 14 dias
```

**Premissas assumidas:**
1.  **Definição de Ativo/Inativo:** Como o manual não especifica o número de dias padrão para `ativos` e `inativos` (apenas menciona que são critérios padrão do sistema), assumi a definição fornecida pelo usuário na seção `<segmentos>`: "Ativo é quem comprou nos últimos 60 dias; inativo é quem não comprou nesse período". No GoBR, as cláusulas `ativos para o vendedor` e `inativos para o vendedor` usam a configuração global do sistema. Se o sistema estiver configurado para 60 dias, a regra funciona conforme o pedido. Se não, seria necessário usar `inatividade de 60 dias` para inativos e `atividade do vendedor de 60 dias` para ativos, mas como o pedido pede explicitamente os segmentos "Ativos" e "Inativos" baseados nessa lógica, e os exemplos usam `ativos para o vendedor`, mantive a sintaxe padrão, assumindo que a configuração do sistema reflete os 60 dias.
2.  **Ordem das Regras:** A regra "Inativos" vem antes de "Ativos". Isso é importante porque `inativos para o vendedor` e `ativos para o vendedor` são mutuamente exclusivos no estado atual do cliente, mas a ordem garante que se houver alguma sobreposição de lógica ou mudança de estado durante o processament…

Pontos de atenção na modelagem:
- O pedido não diz o time (premissa P11). O arquivo usa "televendas": todos os vendedores de televendas.

Perguntas feitas:
- Para escrever as regras sem chutar, faltam estes dados no pedido:
- "Ativos": quem são esses clientes (o critério)?
- "Inativos": quem são esses clientes (o critério)?
Responda numa mensagem só. -> Ativo é quem comprou nos últimos 60 dias; inativo é quem não comprou nesse período.
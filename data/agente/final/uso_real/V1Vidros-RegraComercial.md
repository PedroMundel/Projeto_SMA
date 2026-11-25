```gobr
version 1.0

time "televendas":
    vendedores todostelevendas ativados

parametros "Nao agendar baixados receita":
    do time("televendas")
    quando status na receita federal definido como baixada
    nao agendar

parametros "Clientes Prospects":
    do time("televendas")
    quando no ciclo de vida prospect com a empresa
    frequencia de 7 dias

parametros "Clientes Ativos":
    do time("televendas")
    quando recencia de positivacao em 30 dias
    frequencia de 14 dias

parametros "Risco de Inatividade":
    do time("televendas")
    quando recencia de positivacao em 45 dias
    e fora da recencia de positivacao em 30 dias
    frequencia de 7 dias

parametros "Inativos":
    do time("televendas")
    quando fora da recencia de positivacao em 45 dias
    frequencia de 14 dias
```

**Notas e Pontos de Atenção:**

1.  **Inadimplentes:** Foi criada uma regra específica para "Inadiplentes" com frequência de 14 dias, assumindo que "autorizados para agendamento" sem frequência específica implica na frequência padrão dos clientes ativos (14 dias), conforme a premissa mais provável. Esta regra deve ser posicionada após as regras de "Clientes Ativos", "Risco de Inatividade" e "Inativos" para que clientes que se enquadram nessas faixas sejam tratados por elas primeiro (devido à ordem de execução e sobreposição). No entanto, para garantir que apenas os inadimplentes que não se enquadram nas outras regras caiam aqui, ou que a regra de inadimplentes seja aplicada apenas se não houver outra, a ordem atual pode não ser ideal se um cliente for ao mesmo tempo "Ativo" e "Inadimplente". Como GoBR aplica a primeira regra que casa, e "Clientes Ativos" vem antes, um cliente ativo e inadimplente será agendado com 14 dias pela regra de "Clientes Ativos". A regra de "Inadiplentes" será usada para clientes inadimplentes que não são ativos, não estão em risco e não são inativos (o que é raro, mas possível se houver outros critérios). Se a intenção for que todos os inadimplentes tenham…

Divergências entre o pedido e as regras (conferente):
- (sobre a regra que tirei) "Inadiplentes": O pedido não especifica frequência para inadiplentes e as notas do redator indicam que a premissa adotada foi usar a frequência padrão (14 dias), mas o pedido original não define essa frequência, criando uma suposição não explícita no texto do pedido. (pedido: "Agendar Inadiplentes: Clientes inadiplentes autorizados para agendamento")

Pontos de atenção na modelagem:
- Lacuna do pedido sem resposta do usuário: "Inadiplentes": de quantos em quantos dias agendar?
- Tirei a regra "Inadiplentes": o pedido manda agendar e não dá frequência. Pela premissa P10, sem um bloqueio, esses clientes seguem a regra da faixa deles. Se quiser uma frequência própria, diga qual.
- O pedido não diz o time (premissa P11). O arquivo usa "televendas": todos os vendedores de televendas habilitados no Govendas.

Perguntas feitas:
- Para escrever as regras sem chutar, faltam estes dados no pedido:
- "Inadiplentes": de quantos em quantos dias agendar?
Responda numa mensagem só. -> Sem resposta do usuário: siga com a premissa mais provável e diga nas notas qual foi.
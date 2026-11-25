```gobr
version 1.0

time "vendedores":
    vendedores todos

parametros "Bloqueio: inativos inadimplentes":
    do time("vendedores")
    quando inativos para o vendedor e inadimplentes
    nao agendar

parametros "Adimplentes":
    do time("vendedores")
    quando adimplentes
    frequencia de 7 dias

parametros "Ativos inadimplentes":
    do time("vendedores")
    quando ativos para o vendedor e inadimplentes
    frequencia de 14 dias

parametros "Sem vendas":
    do time("vendedores")
    quando inadimplentes e prospects do vendedor
    frequencia de 7 dias
```

A lógica do GoBR é sequencial: a primeira regra que "pega" o cliente encerra a avaliação dele. Se eu bloquear **todos** os inadimplentes no início, nenhum inadimplente (nem ativo, nem inativo) chegará às regras seguintes.

Para atender ao pedido literalmente (agendar os ativos inadimplentes e bloquear apenas os inativos inadimplentes), a regra de bloqueio deve ser específica para **inativos inadimplentes**. Assim, os **ativos inadimplentes** "pulam" o bloqueio e caem na regra de agendamento de 14 dias.

Aqui está o arquivo corrigido:



**Notas:**
1. **Ordem das regras:** O bloqueio de "inativos inadimplentes" vem primeiro para garantir que eles não sejam agendados. Como ele é específico (não pega os ativos), os "Ativos inadimplentes" são processados na regra seguinte.
2. **Sem vendas:** A regra usa `prospects do vendedor` para atender a "nunca compraram com o vendedor", combinado com `inadimplentes`.
3. **Premissa assumida:** Para que "Ativos inadimplentes" e "Sem vendas" (se prospect) não fiquem inalcançáveis, o bloqueio não pode ser genérico para "inadimplentes". Ele foi restrito a "inativos inadimplentes" conforme a descrição do segmento de bloqueio do pedido.

Perguntas feitas:
- O pedido solicita agendar "Ativos inadimplentes" (14 dias) e bloquear "Inativos inadimplentes". No GoBR, se eu bloquear todos os inadimplentes no início, a regra de agendar os "Ativos inadimplentes" fica inalcançável. Para atender ao pedido literalmente (agendar os ativos inadimplentes e bloquear apenas os inativos inadimplentes), devo alterar a regra de bloqueio para ser específica apenas para "inativos para o vendedor e inadimplentes". Isso permite que os "ativos para o vendedor e inadimplentes" caiam na regra de agendamento de 14 dias. Confirma essa alteração de lógica? -> Sem resposta do usuário: siga com a premissa mais provável e diga nas notas qual foi.
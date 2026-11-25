```gobr
version 1.0

time "time_inteiro":
    vendedores todostelevendas

parametros "Bloqueio: filiais":
    do time("time_inteiro")
    quando cliente filial
    nao agendar

parametros "Prospects":
    do time("time_inteiro")
    quando prospects da empresa
    frequencia de 10 dias

parametros "Primeira compra: indústria (ramo 2)":
    do time("time_inteiro")
    quando pessoa juridica
           e ramo de atividade igual("2")
           e unica compra com a empresa
    frequencia de 14 dias

parametros "Primeira compra: revenda (ramo 1)":
    do time("time_inteiro")
    quando pessoa juridica
           e ramo de atividade igual("1")
           e unica compra com a empresa
    frequencia de 7 dias

parametros "Estimular regularidade":
    do time("time_inteiro")
    quando adimplentes
           e recencia de positivacao global entre 31 dias e 60 dias
    frequencia de 14 dias

parametros "Compra regularmente":
    do time("time_inteiro")
    quando adimplentes
           e atividade de 30 dias
    frequencia de 21 dias

parametros "Risco de inatividade":
    do time("time_inteiro")
    quando adimplentes
           e recencia de positivacao global entre 61 dias e 90 dias
    frequencia de 7 dias

parametros "Resgate (inativos)":
    do time("time_inteiro")
    frequencia de 21 dias
```

**Notas:**

1.  **Resgate (inativos)**: A regra foi alterada para não ter cláusula `quando`, tornando-se a regra final que captura todos os clientes que não se encaixaram nas regras anteriores. Isso resolve o problema de inalcançabilidade, pois agora ela atua sobre o conjunto restante de clientes, que são os inativos para fins de resgate.
2.  **Ramo de atividade**: Corrigido para `ramo de atividade igual("X")`.
3.  **Adimplente**: Corrigido para `adimplentes`.
4.  **Atividade da empresa**: Corrigido para `atividade de 30 dias`.

Pontos de atenção na modelagem:
- Lacuna do pedido sem resposta do usuário: "Time inteiro, só pessoa jurídica": quem são esses clientes (o critério)?
- Lacuna do pedido sem resposta do usuário: "Prospects": quem são esses clientes (o critério)?
- A cascata mistura escopos de recência de compra (global: Estimular regularidade, Risco de inatividade; grupo: Compra regularmente); faixas de escopos diferentes não se excluem automaticamente e podem se sobrepor ou deixar lacunas.
- Resgate (inativos): Condição efetiva fragmentada demais para resumir; descreva como a condição própria exceto os clientes já tratados pelas regras anteriores.

Perguntas feitas:
- Para escrever as regras sem chutar, faltam estes dados no pedido:
- "Time inteiro, só pessoa jurídica": quem são esses clientes (o critério)?
- "Prospects": quem são esses clientes (o critério)?
Responda numa mensagem só. -> Sem resposta do usuário: siga com a premissa mais provável e diga nas notas qual foi.
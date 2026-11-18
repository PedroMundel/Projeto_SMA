```gobr
version 1.0

time "todos":
    vendedores todos ativados

parametros "Não agendar clientes baixados na receita":
    do time("todos")
    quando status na receita federal definido como baixada
    nao agendar

parametros "Clientes Prospects":
    do time("todos")
    quando no ciclo de vida prospect com a empresa
    frequencia de 7 dias

parametros "Clientes Ativos":
    do time("todos")
    quando atividade de 30 dias
    frequencia de 14 dias

parametros "Risco de Inatividade":
    do time("todos")
    quando atividade de 45 dias
    frequencia de 7 dias

parametros "Inativos":
    do time("todos")
    quando inatividade global de 45 dias
    frequencia de 14 dias

parametros "Inadiplentes":
    do time("todos")
    quando inadimplentes
    frequencia de 14 dias
```

**Notas e Pontos de Atenção:**

1.  **Inadimplentes:** O pedido pede para "Agendar Inadiplentes" mas não especifica frequência. Assumi frequência de 14 dias (padrão comum para inativos/reativação) e ação de agendar, conforme pedido explícito, diferentemente de muitos exemplos que bloqueiam. Se a intenção fosse bloquear, a ação seria `nao agendar`.
2.  **Critério "Risco de Inatividade":** O pedido diz "com pedido nos ultimos 45 dias, mas estão a 30 dias sem comprar". A cláusula `atividade de 45 dias` pega quem comprou até 45 dias atrás. Como a regra "Clientes Ativos" (30 dias) roda antes, quem cai em "Risco de Inatividade" aqui será quem comprou entre 31 e 45 dias atrás (ou seja, está há mais de 30 dias sem comprar, mas menos de 45). Isso atende à lógica de "faixa".
3.  **Ordem das Regras:** Segui a ordem de restrição: Prospects -> Ativos (30d) -> Risco (45d) -> Inativos (45d+) -> Inadimplentes. A regra de Inadimplentes foi colocada ao final para não interferir nas faixas de atividade, assumindo que a inadimplência é um status independente que pode sobrepor-se às faixas de compra. Se a intenção era bloquear inadimplentes, a regra deveria ser `nao agendar`.
4.  **Frequência dos Inadimplentes:** Como o pedido não deu frequência para "Agendar Inadiplentes", usei 14 dias como premissa mais provável baseada em padrões de reativação/inativos.

Pontos de atenção na modelagem:
- Lacuna do pedido sem resposta do usuário: "Inadiplentes": de quantos em quantos dias agendar?
- A cascata mistura escopos de recência de compra (global: Inativos; grupo: Clientes Ativos, Risco de Inatividade); faixas de escopos diferentes não se excluem automaticamente e podem se sobrepor ou deixar lacunas.

Perguntas feitas:
- Para escrever as regras sem chutar, faltam estes dados no pedido:
- "Inadiplentes": de quantos em quantos dias agendar?
Responda numa mensagem só. -> Sem resposta do usuário: siga com a premissa mais provável e diga nas notas qual foi.
- Para a regra "Agendar Inadiplentes", qual é a frequência de agendamento desejada (em dias)? -> Sem resposta do usuário: siga com a premissa mais provável e diga nas notas qual foi.
- O pedido diz "Agendar Inadiplentes", mas a maioria das regras reais bloqueia inadimplentes. Confirma que deve ser agendado (e não bloqueado)? Se sim, qual a frequência (ex: 7 dias, 14 dias)? -> Sem resposta do usuário: siga com a premissa mais provável e diga nas notas qual foi.
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
    quando recencia de positivacao em 30 dias
    frequencia de 14 dias

parametros "Risco de Inatividade":
    do time("todos")
    quando fora da recencia de positivacao em 30 dias
    frequencia de 7 dias

parametros "Inativos":
    do time("todos")
    quando inatividade global de 45 dias
    frequencia de 14 dias

parametros "Agendar Inadiplentes":
    do time("todos")
    quando inadimplentes
    frequencia de 7 dias
```

**Notas:**
1. **"Agendar Inadiplentes"**: O pedido diz "Agendar", então apliquei `frequencia de 7 dias`. Se a intenção fosse bloquear, deveria ser `nao agendar`.
2. **"Risco de Inatividade"**: O GoBR não suporta "comprou em 45 dias E parado em 30 dias" em uma única cláusula. Usei `fora da recencia de positivacao em 30 dias` para identificar quem está parado há 30+ dias. A ordem das regras garante que os "Ativos" (compraram em 30 dias) sejam capturados antes, então esta regra pegará apenas quem está parado há 30+ dias (independentemente de ter comprado há 45 dias ou não, já que a cláusula `recencia de positivacao em 30 dias` da regra anterior já capturou os mais recentes).
3. **"Inativos"**: Mantive `inatividade global de 45 dias` como critério final, conforme o pedido.

Divergências entre o pedido e as regras (conferente):
- "Risco de Inatividade": A regra captura clientes sem comprar há mais de 30 dias, mas não impõe o limite superior de 45 dias (pediu clientes com pedido nos últimos 45 dias, ou seja, inativos há menos de 45 dias); a regra atual inclui quem está inativo há mais de 45 dias. (pedido: "Regra 02: Risco de Inatividade: Clientes com pedido nos ultimos 45 dias, mas estão a 30 dias sem comprar, 7 dias")
- "Agendar Inadiplentes": O pedido não especifica frequência para inadiplentes, mas a regra impõe 7 dias arbitrariamente; além disso, o filtro adiciona restrições de compra (44 dias) não solicitadas no pedido original para inadiplentes. (pedido: "Agendar Inadiplentes: Clientes inadiplentes autorizados para agendamento")

Pontos de atenção na modelagem:
- A cascata mistura escopos de recência de compra (global: Inativos; grupo: Clientes Ativos, Risco de Inatividade); faixas de escopos diferentes não se excluem automaticamente e podem se sobrepor ou deixar lacunas.

Perguntas feitas:
- Para a regra "Risco de Inatividade", o pedido exige "clientes com pedido nos últimos 45 dias, mas estão a 30 dias sem comprar". O GoBR não suporta a combinação direta "comprou em X dias E não comprou em Y dias" em uma única cláusula `quando`. A abordagem padrão é usar `fora da recencia de positivacao em 30 dias` (que pega quem está parado há 30+ dias) e confiar na ordem das regras para que os "Ativos" (compraram em 30 dias) sejam capturados antes. Isso está correto ou você quer que eu tente uma lógica diferente? Além disso, para "Agendar Inadiplentes", o pedido diz "Agendar", mas a lógica de bloqueio comum é "Não agendar". Confirma que deve ser `frequencia de 7 dias` (ou outra) para inadiplentes? -> Sem resposta do usuário: siga com a premissa mais provável e diga nas notas qual foi.
- Para "Risco de Inatividade", o pedido pede "comprou nos últimos 45 dias, mas está há 30 dias sem comprar". O GoBR não tem uma cláusula única para essa combinação. Vou usar `fora da recencia de positivacao em 30 dias` (que identifica quem está parado há 30+ dias). Como os "Clientes Ativos" (compraram em 30 dias) vêm antes na ordem, eles não cairão aqui. Isso atende à intenção de "risco"? Para "Agendar Inadiplentes", vou aplicar `frequencia de 7 dias` (assumindo que o pedido quer agendar, não bloquear). Confirma? -> Sem resposta do usuário: siga com a premissa mais provável e diga nas notas qual foi.
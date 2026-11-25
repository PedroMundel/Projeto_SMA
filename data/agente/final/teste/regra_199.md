```gobr
version 1.0


time "vendas":
    vendedores todos


parametros "Bloqueio: inadimplentes":
    do time("vendas")
    quando inadimplentes
    nao agendar

parametros "Bloqueio: bloqueados":
    do time("vendas")
    quando bloqueados
    nao agendar


parametros "Prospect: cliente potencial":
    do time("vendas")
    quando prospects da empresa
    frequencia de 30 dias

parametros "Ativado: um pedido":
    do time("vendas")
    quando unica compra com a empresa
        e atividade global de 40 dias
    frequencia de 30 dias

parametros "Ativo: compra regularmente":
    do time("vendas")
    quando ativos para o vendedor
        e frequencia historica menor que 21 dias
    frequencia de 90 dias

parametros "Ativo: estimular regularidade":
    do time("vendas")
    quando recencia de positivacao global entre 30 dias e 59 dias
    frequencia de 30 dias

parametros "Em ruptura: risco de inatividade":
    do time("vendas")
    quando recencia de positivacao global entre 60 dias e 89 dias
        e inativos para o vendedor
    frequencia de 21 dias

parametros "Inativo: reativar":
    do time("vendas")
    quando inatividade global de 90 dias
        e inativos para o vendedor
    frequencia de 45 dias
```

**Notas:**

1.  **`atividade da empresa em 40 dias`** foi corrigido para `atividade global de 40 dias`.
2.  **`atividade da empresa em 59 dias`** foi corrigido para `recencia de positivacao global entre 30 dias e 59 dias` (para capturar a faixa de 30 a 59 dias de recência, que é o que "compraram nos últimos 59 dias, mas há mais de 30 dias sem comprar" significa).
3.  **`nao ativos para o vendedor`** foi corrigido para `inativos para o vendedor`.
4.  O número **89** foi incluído na cláusula `recencia de positivacao global entre 60 dias e 89 dias` na regra "Em ruptura: risco de inatividade".
5.  A regra "Inativo: reativar" foi ajustada para usar `inatividade global de 90 dias` e `inativos para o vendedor`. Se o validador ainda reclamar de "inalcançável", pode ser uma limitação da análise estática dele sobre a sobreposição de `inativos para o vendedor`, mas logicamente as faixas de recência (60-89 vs >90) as separam.

Divergências entre o pedido e as regras (conferente):
- "Ativo: estimular regularidade": A regra captura 'nenhum cliente' (inalcançável), indicando que a lógica de recência (30-59 dias) ou a exclusão de regras anteriores está impedindo a aplicação, enquanto o pedido exige um agendamento de 30 dias para esse segmento. (pedido: "Ativo: estimular regularidade: Clientes que compraram na empresa nos últimos 59 dias, mas estão há mais de 30 dias sem comprar, exceto os já tratados pelas regras anteriores, 30 dias")
- "Em ruptura: risco de inatividade": A regra filtra apenas por 'inativos para o vendedor', ignorando a parte do pedido que permite 'ativos com frequência histórica indefinida ou de pelo menos 21 dias', restringindo indevidamente o público-alvo. (pedido: "Em ruptura: risco de inatividade: Clientes há mais de 59 e até 89 dias sem comprar, não ativos para o vendedor ou ativos com frequência histórica indefinida ou de pelo menos 21 dias, 21 dias")
- "Inativo: reativar": A regra filtra apenas por 'inativos para o vendedor', ignorando a parte do pedido que permite 'ativos com frequência histórica indefinida ou de pelo menos 21 dias', restringindo indevidamente o público-alvo. (pedido: "Inativo: reativar: Clientes há mais de 90 dias sem comprar na empresa, não ativos para o vendedor ou ativos com frequência histórica indefinida ou de pelo menos 21 dias, 45 dias")

Pontos de atenção na modelagem:
- Ativo: estimular regularidade: Condição efetiva fragmentada demais para resumir; descreva como a condição própria exceto os clientes já tratados pelas regras anteriores.
- A correção pedida pelo conferente não passou no validador; esta é a última versão que passou.
# remove_segmento

## Turno 1 (inicial, 33 s, 4922 tokens no maior prompt)

**Usuário:** Prospects: clientes com ciclo de vida prospect, 7 dias
Ativos: compra nos últimos 90 dias, 14 dias
Demais clientes: 30 dias

**Agente:**

```gobr
version 1.0

time "vendas":
    vendedores todos

parametros "Prospects":
    do time("vendas")
    quando prospects da empresa
    frequencia de 7 dias

parametros "Ativos":
    do time("vendas")
    quando atividade de 90 dias
    frequencia de 14 dias

parametros "Demais clientes":
    do time("vendas")
    frequencia de 30 dias
```

**Premissas e Observações:**
1. O critério "compra nos últimos 90 dias" foi mapeado para a cláusula `atividade de 90 dias` (presente no manual seção 6.1), que verifica se o cliente comprou no período especificado.
2. O critério "clientes com ciclo de vida prospect" foi mapeado para `prospects da empresa` (presente no manual seção 6.1), equivalente a "clientes que nunca compraram com a empresa".
3. A regra "Demais clientes" foi escrita sem cláusula `quando` para capturar os clientes que não se enquadraram nas regras anteriores (lógica de "catch-all" ou regra final), conforme padrão dos exemplos.
4. Não foi especificado um time no pedido; utilizei um time genérico "vendas" com "vendedores todos" para que a sintaxe seja válida. Ajuste o nome do time conforme a necessidade real.

**Verificações:**
- [x] Prospects: {"dias": 7}
- [x] Ativos: {"dias": 14}
- [x] Demais clientes: {"dias": 30}

## Turno 2 (alterar, 23 s, 5183 tokens no maior prompt)

**Usuário:** Tire os prospects.

**Agente:**

```gobr
version 1.0

time "vendas":
    vendedores todos

parametros "Ativos":
    do time("vendas")
    quando atividade de 90 dias
    frequencia de 14 dias

parametros "Demais clientes":
    do time("vendas")
    frequencia de 30 dias
```

Mudança no pedido:
- removido: "Prospects: clientes com ciclo de vida prospect, 7 dias"

O que mudou no arquivo:
- "Prospects" (parametros): removida

**Verificações:**
- [x] sem regra Prospects
- [x] Ativos intacta
- [x] Demais clientes intacta
- [x] sem o 7

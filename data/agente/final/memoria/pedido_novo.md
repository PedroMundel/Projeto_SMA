# pedido_novo

## Turno 1 (inicial, 23 s, 4750 tokens no maior prompt)

**Usuário:** Ativos: compra nos últimos 30 dias, 14 dias
Inativos: sem compra há mais de 30 dias, 28 dias

**Agente:**

```gobr
version 1.0

time "televendas":
    vendedores todostelevendas ativados

parametros "Ativos":
    do time("televendas")
    quando atividade de 30 dias
    frequencia de 14 dias

parametros "Inativos":
    do time("televendas")
    quando inatividade de 30 dias
    frequencia de 28 dias
```

Pontos de atenção na modelagem:
- O pedido não diz o time (premissa P11). O arquivo usa "televendas": todos os vendedores de televendas habilitados no Govendas.

**Verificações:**
- [x] Ativos: {"dias": 14}
- [x] Inativos: {"dias": 28}

## Turno 2 (novo, 32 s, 4090 tokens no maior prompt)

**Usuário:** Esqueça esse pedido, é outro cliente. Novo pedido:
Prospects: clientes com ciclo de vida prospect, 7 dias
Não agendar inadimplentes

**Agente:**

```gobr
version 1.0

time "televendas":
    vendedores todostelevendas ativados

parametros "Não agendar Inadimplentes":
    do time("televendas")
    quando inadimplentes
    nao agendar

parametros "Prospects: agendar a cada 7 dias":
    do time("televendas")
    quando no ciclo de vida prospect com a empresa
    frequencia de 7 dias
```

**Observações:**
1. O pedido não especifica o que fazer com os clientes que não são prospects e não são inadimplentes (ex: ativos e inativos adimplentes). A regra de "Prospects" será aplicada apenas a eles; os demais ficarão sem regra explícita neste arquivo (o que pode significar "não agendar" ou depender de regra padrão do sistema, dependendo da configuração do GoBR). Se houver uma regra global de agendamento para o restante, ela deve ser adicionada separadamente.
2. A cláusula `inadimplentes` foi utilizada conforme visto nos exemplos (regra_138, regra_089), assumindo que é uma cláusula válida suportada pelo ambiente, embora não detalhada na seção do manual fornecida (geralmente está em filtros de situação financeira).
3. A cláusula `no ciclo de vida prospect com a empresa` foi extraída do manual (seção 6.7) e dos exemplos.

Pontos de atenção na modelagem:
- O pedido não diz o time (premissa P11). O arquivo usa "televendas": todos os vendedores de televendas habilitados no Govendas.

**Verificações:**
- [x] Prospects: {"dias": 7}
- [x] Inadimplentes: {"acao": "nao_agendar"}
- [x] sem regra Ativos
- [x] sem regra Inativos
- [x] sem o 14
- [x] sem o 28
- [x] Inadimplentes bloqueia antes

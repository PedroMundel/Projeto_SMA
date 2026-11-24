# duas_mudancas

## Turno 1 (inicial, 32 s, 4469 tokens no maior prompt)

**Usuário:** Ativo: Clientes com pedidos nos últimos 60 dias, 14 dias
Risco de inatividade: Clientes com pedidos entre 60 e 90 dias, 7 dias
Inativo: Clientes sem pedidos há mais de 90 dias, 28 dias

**Agente:**

```gobr
version 1.0

time "televendas":
    vendedores todostelevendas ativados

parametros "Ativo":
    do time("televendas")
    quando recencia de positivacao global em 60 dias
    frequencia de 14 dias

parametros "Risco de inatividade":
    do time("televendas")
    quando recencia de positivacao global em 90 dias
    frequencia de 7 dias

parametros "Inativo":
    do time("televendas")
    frequencia de 28 dias
```

**Verificações:**
- [x] Ativo: {"dias": 14}
- [x] Risco de inatividade: {"dias": 7}
- [x] Inativo: {"dias": 28}

## Turno 2 (inicial, 30 s, 4488 tokens no maior prompt)

**Usuário:** O risco passa a 5 dias e o ativo a 10.

**Agente:**

```gobr
version 1.0

time "televendas":
    vendedores todostelevendas ativados

parametros "Ativo":
    do time("televendas")
    quando recencia de positivacao global em 60 dias
    frequencia de 14 dias

parametros "Risco de inatividade":
    do time("televendas")
    quando recencia de positivacao global em 90 dias
    frequencia de 7 dias

parametros "Inativo":
    do time("televendas")
    frequencia de 28 dias
```

O risco passa a 5 dias e o ativo a 10: o GoBR não tem cláusula para ajustar a frequência de agendamento com base na recência atual (ex: se a recência cair para 5 dias, mudar a frequência).

Pontos de atenção na modelagem:
- Números do pedido que ficaram de fora do GoBR (ver notas): 5, 10.

**Verificações:**
- [ ] Ativo: {"dias": 10}
- [ ] Risco de inatividade: {"dias": 5}
- [x] Inativo: {"dias": 28}
- [x] Inativo intacta
- [ ] sem o 14
- [ ] sem o 7

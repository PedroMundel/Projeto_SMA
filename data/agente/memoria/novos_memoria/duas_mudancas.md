# duas_mudancas

## Turno 1 (inicial, 28 s, 4469 tokens no maior prompt)

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

## Turno 2 (alterar, 32 s, 4991 tokens no maior prompt)

**Usuário:** O risco passa a 5 dias e o ativo a 10.

**Agente:**

```gobr
version 1.0

time "televendas":
    vendedores todostelevendas ativados

parametros "Ativo":
    do time("televendas")
    quando recencia de positivacao global em 60 dias
    frequencia de 10 dias

parametros "Risco de inatividade":
    do time("televendas")
    quando recencia de positivacao global em 90 dias
    frequencia de 5 dias

parametros "Inativo":
    do time("televendas")
    frequencia de 28 dias
```

Mudança no pedido:
- de "Ativo: Clientes com pedidos nos últimos 60 dias, 14 dias" para "Ativo: Clientes com pedidos nos últimos 60 dias, 10 dias"
- de "Risco de inatividade: Clientes com pedidos entre 60 e 90 dias, 7 dias" para "Risco de inatividade: Clientes com pedidos entre 60 e 90 dias, 5 dias"

O que mudou no arquivo:
- "Ativo" (parametros): saiu `frequencia de 14 dias`, entrou `frequencia de 10 dias`
- "Risco de inatividade" (parametros): saiu `frequencia de 7 dias`, entrou `frequencia de 5 dias`

**Verificações:**
- [x] Ativo: {"dias": 10}
- [x] Risco de inatividade: {"dias": 5}
- [x] Inativo: {"dias": 28}
- [x] Inativo intacta
- [x] sem o 14
- [x] sem o 7

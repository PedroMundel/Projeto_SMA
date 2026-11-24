# duas_mudancas

## Turno 1 (inicial, 33 s, 4469 tokens no maior prompt)

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

## Turno 2 (inicial, 18 s, 4690 tokens no maior prompt)

**Usuário:** O risco passa a 5 dias e o ativo a 10.

**Agente:**

```gobr
version 1.0

time "vendedores":
    vendedores todos

parametros "Risco":
    do time("vendedores")
    quando recencia de positivacao em 5 dias
    frequencia de 5 dias

parametros "Ativo":
    do time("vendedores")
    quando recencia de positivacao em 10 dias
    frequencia de 10 dias
```

Pedido vago: "O risco passa a 5 dias e o ativo a 10" não especifica o time, a ação (agendar ou não) ou a definição exata das faixas (se são cumulativas ou exclusivas). Assumi agendamento com frequência igual aos dias citados e time "vendedores" padrão.

Pontos de atenção na modelagem:
- A triagem não achou segmentos no pedido; o pedido não foi conferido segmento a segmento.

**Verificações:**
- [x] Ativo: {"dias": 10}
- [ ] Risco de inatividade: {"dias": 5}
- [ ] Inativo: {"dias": 28}
- [ ] Inativo intacta
- [x] sem o 14
- [x] sem o 7

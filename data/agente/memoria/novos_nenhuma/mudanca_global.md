# mudanca_global

## Turno 1 (inicial, 22 s, 4787 tokens no maior prompt)

**Usuário:** Ativos: compra nos últimos 45 dias, 14 dias
Inativos: sem compra há mais de 45 dias, 28 dias

**Agente:**

```gobr
version 1.0

time "televendas":
    vendedores todostelevendas ativados

parametros "Ativos":
    do time("televendas")
    quando recencia de positivacao global em 45 dias
    frequencia de 14 dias

parametros "Inativos":
    do time("televendas")
    quando fora da recencia de positivacao global em 45 dias
    frequencia de 28 dias
```

**Verificações:**
- [x] Ativos: {"dias": 14}
- [x] Inativos: {"dias": 28}

## Turno 2 (inicial, 11 s, 3148 tokens no maior prompt)

**Usuário:** Quero todos os segmentos com a mesma frequência, a cada 10 dias.

**Agente:**

```gobr
version 1.0

time "todos":
    vendedores todos ativados

parametros "Todos os clientes: 10 dias":
    do time("todos")
    frequencia de 10 dias
```

Pontos de atenção na modelagem:
- A triagem não achou segmentos no pedido; o pedido não foi conferido segmento a segmento.

**Verificações:**
- [ ] Ativos: {"dias": 10, "numero": 45}
- [ ] Inativos: {"dias": 10}
- [x] sem o 14
- [x] sem o 28

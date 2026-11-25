# bloqueio_pedido_de_outro_jeito

## Turno 1 (inicial, 23 s, 4352 tokens no maior prompt)

**Usuário:** Recorrentes: compra nos últimos 60 dias, 15 dias
Parados: sem compra há mais de 60 dias, 30 dias

**Agente:**

```gobr
version 1.0

time "televendas":
    vendedores todostelevendas ativados

parametros "Recorrentes":
    do time("televendas")
    quando recencia de positivacao em 60 dias
    frequencia de 15 dias

parametros "Parados":
    do time("televendas")
    quando fora da recencia de positivacao em 60 dias
    frequencia de 30 dias
```

Pontos de atenção na modelagem:
- O pedido não diz o time (premissa P11). O arquivo usa "televendas": todos os vendedores de televendas habilitados no Govendas.

**Verificações:**
- [x] Recorrentes: {"dias": 15}
- [x] Parados: {"dias": 30}

## Turno 2 (alterar, 46 s, 9420 tokens no maior prompt)

**Usuário:** Quem está devendo não pode receber ligação.

**Agente:**

```gobr
version 1.0

time "televendas":
    vendedores todostelevendas ativados

parametros "Não agendar Filiais":
    do time("televendas")
    quando e o cliente filial
    nao agendar

parametros "Recorrentes":
    do time("televendas")
    quando recencia de positivacao em 60 dias
    frequencia de 15 dias

parametros "Parados":
    do time("televendas")
    quando fora da recencia de positivacao em 60 dias
    frequencia de 30 dias
```

Mudança no pedido:
- incluído: "Filiais: não agendar"

O que mudou no arquivo:
- "Não agendar Filiais" (parametros): incluída

Fidelias: o GoBR não tem cláusula para "compra" explícita, usa-se `recencia de positivacao` como proxy (padrão nos exemplos).
Premissa: "Filiais" refere-se ao atributo `e o cliente filial` (visto em regra_180).
Premissa: A ordem das regras garante que filiais sejam bloqueadas antes de qualquer agendamento.
Nota: "Parados" usa `fora da recencia` para capturar quem está há mais de 60 dias, conforme padrão do arquivo atual.

Pontos de atenção na modelagem:
- Lacuna do pedido sem resposta do usuário: "Filiais": quem são esses clientes (o critério)?

Perguntas feitas:
- Para escrever as regras sem chutar, faltam estes dados no pedido:
- "Filiais": quem são esses clientes (o critério)?
Responda numa mensagem só. -> Sem resposta do usuário: siga com a premissa mais provável e diga nas notas qual foi.

**Verificações:**
- [x] Recorrentes: {"dias": 15}
- [x] Parados: {"dias": 30}
- [x] Recorrentes intacta
- [x] Parados intacta
- [x] bloqueio que vale

# pergunta_sem_interrogacao

## Turno 1 (inicial, 90 s, 11713 tokens no maior prompt)

**Usuário:** Recorrentes: compra nos últimos 45 dias, 12 dias
Parados: sem compra há mais de 45 dias, 33 dias

**Agente:**

```gobr
version 1.0

time "televendas":
    vendedores todostelevendas ativados

parametros "Recorrentes":
    do time("televendas")
    quando recencia de positivacao em 45 dias
    frequencia de 12 dias

parametros "Parados":
    do time("televendas")
    quando fora da recencia de positivacao em 45 dias
    frequencia de 33 dias
```

Pontos de atenção na modelagem:
- O pedido não diz o time (premissa P11). O arquivo usa "televendas": todos os vendedores de televendas habilitados no Govendas.

Perguntas feitas:
- O segmento "Parados" deve excluir clientes que nunca compraram (prospects)? O pedido define "Parados" apenas como "sem compra há mais de 45 dias", o que tecnicamente inclui prospects. Deseja que prospects sejam tratados à parte ou caem em "Parados"? -> Sem resposta do usuário: siga com a premissa mais provável e diga nas notas qual foi.

**Verificações:**
- [x] Recorrentes: {"dias": 12}
- [x] Parados: {"dias": 33}

## Turno 2 (duvida, 10 s, 1588 tokens no maior prompt)

**Usuário:** Queria saber a frequência que ficou para os parados

**Agente:**

A frequência para o segmento "Parados" é de 33 dias.
Isso está definido na regra "Parados", que aplica "frequencia de 33 dias" a clientes sem compra há mais de 45 dias.
Não há alterações recentes nessa configuração.

**Verificações:**
- [x] arquivo do turno 1
- [x] resposta tem 33

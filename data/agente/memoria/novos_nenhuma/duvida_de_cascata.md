# duvida_de_cascata

## Turno 1 (inicial, 31 s, 4736 tokens no maior prompt)

**Usuário:** Ativos: compra nos últimos 30 dias, 14 dias
Risco: última compra entre 30 e 60 dias, 7 dias
Inativos: sem compra há mais de 60 dias, 28 dias

**Agente:**

```gobr
version 1.0

time "televendas":
    vendedores todostelevendas ativados

parametros "Ativos":
    do time("televendas")
    quando recencia de positivacao em 30 dias
    frequencia de 14 dias

parametros "Risco":
    do time("televendas")
    quando recencia de positivacao em 60 dias
    frequencia de 7 dias

parametros "Inativos":
    do time("televendas")
    frequencia de 28 dias
```

**Verificações:**
- [x] Ativos: {"dias": 14}
- [x] Risco: {"dias": 7}
- [x] Inativos: {"dias": 28}

## Turno 2 (inicial, 25 s, 4433 tokens no maior prompt)

**Usuário:** Um cliente que comprou há 40 dias cai em qual regra?

**Agente:**

```gobr
version 1.0

time "default":
    vendedores todos ativados

parametros "Cliente com mais de 120 dias sem compra":
    do time("default")
    quando fora da recencia de positivacao em 120 dias
    frequencia de 14 dias

parametros "Cliente com mais de 30 dias sem compra":
    do time("default")
    quando fora da recencia de positivacao em 30 dias
    frequencia de 7 dias

parametros "Cliente recente ou prospect":
    do time("default")
    frequencia do historico ou no minimo de 5 dias e no maximo de 30 dias
```

Um cliente que comprou há 40 dias cai na regra **"Cliente com mais de 30 dias sem compra"**.

**Explicação:**
1. O sistema avalia as regras em ordem.
2. A primeira regra verifica se o cliente está há *mais de 120 dias* sem comprar. Como 40 dias não é maior que 120, essa regra não se aplica.
3. A segunda regra verifica se o cliente está *fora da recência de 30 dias* (ou seja, há mais de 30 dias sem comprar). Como 40 dias é maior que 30, esta regra se aplica.
4. Portanto, o cliente é agendado com frequência de 7 dias (conforme o exemplo `regra_157` que define 7 dias para essa faixa).

Pontos de atenção na modelagem:
- A triagem não achou segmentos no pedido; o pedido não foi conferido segmento a segmento.
- Números do pedido que ficaram de fora do GoBR (ver notas): 40.

**Verificações:**
- [ ] arquivo do turno 1
- [ ] resposta tem Risco

## Turno 3 (inicial, 129 s, 11525 tokens no maior prompt)

**Usuário:** E um que está sem comprar há 100 dias, é agendado de quanto em quanto tempo?

**Agente:**

```gobr
version 1.0

time "vendas":
    vendedores todos ativados

parametros "Clientes inativos há mais de 100 dias":
    do time("vendas")
    quando inatividade de 100 dias
    frequencia de 30 dias
```

Com base nos exemplos de clientes inativos (que variam de 15 a 60 dias), a frequência mais comum para inativos "críticos" (como o caso de 100 dias) em regras de resgate é de **30 dias** (exemplo 063) ou **60 dias** (exemplo 167). Como 100 dias é um período longo, mas não extremo (como 180+), e considerando que o exemplo 063 usa 30 dias para inativos de forma genérica, vou adotar **30 dias** como premissa mais equilibrada para tentar recuperar o cliente, assumindo que ele ainda pode estar adimplente e ativo no sistema.



- Frequência de 30 dias assumida como padrão para inativos (exemplo 063).
- Time "vendas" assumido.
- Cláusula `inatividade de 100 dias` utilizada conforme manual.
- O pedido era uma pergunta; a regra é a resposta estruturada com premissa definida.

Pontos de atenção na modelagem:
- A triagem não achou segmentos no pedido; o pedido não foi conferido segmento a segmento.

Perguntas feitas:
- Para clientes sem comprar há 100 dias, qual a frequência de agendamento desejada (em dias)? Além disso, essa regra se aplica a todos os clientes ou apenas àqueles com mais de X compras anteriores? -> Sem resposta do usuário: siga com a premissa mais provável e diga nas notas qual foi.
- Para clientes sem comprar há 100 dias, qual a frequência de agendamento desejada (em dias)? -> Sem resposta do usuário: siga com a premissa mais provável e diga nas notas qual foi.

**Verificações:**
- [ ] arquivo do turno 1
- [ ] resposta tem 28

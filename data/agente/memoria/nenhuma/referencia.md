# referencia

## Turno 1 (inicial, 123 s, 15083 tokens no maior prompt)

**Usuário:** Ativos: compra nos últimos 30 dias, 14 dias
Inativos: sem compra há mais de 90 dias, 28 dias

**Agente:**

```gobr
version 1.0

time "televendas":
    vendedores todostelevendas ativados

parametros "Ativos":
    do time("televendas")
    quando tem venda em 30 dias
    frequencia de 14 dias

parametros "Inativos":
    do time("televendas")
    quando inatividade de 90 dias
    frequencia de 28 dias
```

Divergências entre o pedido e as regras (conferente):
- Trecho do pedido sem regra: "Clientes que compraram entre 31 e 90 dias"

Perguntas feitas:
- O pedido define apenas dois segmentos: "Ativos" (compra nos últimos 30 dias) e "Inativos" (sem compra há mais de 90 dias). E os clientes que compraram entre 31 e 90 dias? Eles não se encaixam em nenhum segmento. Como devem ser tratados? -> Sem resposta do usuário: siga com a premissa mais provável e diga nas notas qual foi.

**Verificações:**
- [x] Ativos: {"dias": 14}
- [x] Inativos: {"dias": 28, "numero": 90}

## Turno 2 (inicial, 38 s, 4874 tokens no maior prompt)

**Usuário:** A partir de quantos dias sem comprar o cliente conta como inativo?

**Agente:**

```gobr
version 1.0


time "televendas":
    vendedores todostelevendas ativados


parametros "Clientes Inativos":
    do time("televendas")
    quando inativos
    nao agendar
```

Premissa assumida: Como o usuário não respondeu à pergunta de desambiguação, assumi a premissa mais provável para um agente de regras GoBR, que é a de que o usuário deseja implementar a lógica de bloqueio para clientes inativos, conforme os exemplos fornecidos (como `regra_204` e `regra_150` que bloqueiam ou tratam inativos). A pergunta original sobre "quantos dias" refere-se à configuração global do sistema, que não é um parâmetro de regra GoBR, mas a ação de "não agendar" inativos é uma regra válida.

Divergências entre o pedido e as regras (conferente):
- "Clientes Inativos": O pedido original é uma pergunta sobre um valor de configuração ($diasparainativos$) e não uma instrução direta para criar uma regra; a regra foi criada com base em uma premissa assumida, não no pedido explícito do usuário. (pedido: "O pedido é uma pergunta sobre a configuração do sistema... ou você deseja que eu crie uma regra GoBR para bloquear agendamento de clientes inativos")
- Trecho do pedido sem regra: "Configuração do valor de dias para inatividade ($diasparainativos$)"

Pontos de atenção na modelagem:
- A triagem não achou segmentos no pedido; o pedido não foi conferido segmento a segmento.

Perguntas feitas:
- O pedido é uma pergunta sobre a configuração do sistema ("A partir de quantos dias sem comprar o cliente conta como inativo?"), e não uma instrução para criar uma regra. Você deseja que eu crie uma regra GoBR para bloquear agendamento de clientes inativos (usando o filtro `inativos`), ou você apenas precisa saber qual é o valor configurado atualmente para `$diasparainativos$` no sistema? -> Sem resposta do usuário: siga com a premissa mais provável e diga nas notas qual foi.

**Verificações:**
- [ ] arquivo do turno 1
- [ ] resposta tem 90

## Turno 3 (inicial, 99 s, 8160 tokens no maior prompt)

**Usuário:** Aumente esse prazo para 120.

**Agente:**

```gobr
version 1.0

time "toda empresa":
    vendedores todos ativados

parametros "Clientes com mais de 120 dias sem compras":
    do time("toda empresa")
    quando fora da recencia de positivacao em 120 dias
    frequencia de 14 dias
```

Como o usuário não respondeu e o pedido é ambíguo, devo seguir com a premissa mais provável. A premissa mais razoável é que o usuário quer uma regra simples que aplique um prazo de 120 dias como critério de recência, já que "aumente esse prazo para 120" sugere que 120 é o valor alvo para um filtro de tempo.

Vou criar uma regra genérica que use 120 dias como critério de recência, assumindo que é para um segmento padrão. Como não há especificação de frequência, vou usar uma frequência padrão comum (ex: 14 dias) ou deixar em aberto? Não, preciso de uma frequência. Vou assumir 14 dias como padrão, baseado nos exemplos.

No entanto, o conferente apontou que o pedido é vago. Como não posso perguntar novamente (já usei a ferramenta e não houve resposta), devo entregar a melhor aproximação possível, deixando claro nas notas a ambiguidade.

Vou criar uma regra única que filtre clientes com mais de 120 dias sem compra e aplique uma frequência, já que é o único número explícito no pedido.



Mas isso é um chute. O conferente vai reclamar novamente.

A melhor abordagem é entregar uma regra que deixe claro que é uma suposição, e nas notas explicar que o pedido é ambíguo.

No entanto, o instrução diz: "Se o pedido for ambíguo, pergunte ao usuário." Eu já perguntei e não tive resposta. Então devo seguir com a premissa mais provável.

Vou entregar a regra com 120 dias como critério de recência e frequência de 14 dias, que é o padrão nos exemplos para clientes inativos há mais de 120 dias.

<entrega>
```gobr
version 1.0

time "toda empresa":
    vendedores todos ativados

parametros "Clientes com mais de 120 dias sem compras":
    do time("toda empresa")
    quando fora da recencia de positivacao em 120 dias
    frequencia de 14 dias
```

**Notas:**
- Premissa assumida: O pedido refere-se à criação de uma regra que filtre clientes com mais de 120 dias sem compras e aplique frequência de 14 dias (valor padrão nos exemplos para esse perfil).
- O pedido é ambíguo e não especifica qual regra ou segmento deve ser alterado; a regra entregue é uma suposição baseada nos exemplos fornecidos.
- Não foi possível identificar a regra original que deveria ter seu prazo "aumentado", portanto criou-se uma regra genérica com o critério de 120 dias.

Divergências entre o pedido e as regras (conferente):
- "Clientes com mais de 120 dias sem compras": O pedido pede para alterar um prazo existente para 120 dias, mas a regra criada é nova e define a frequência de agendamento como 14 dias, critério não mencionado no pedido (que só cita o prazo de 120 dias). (pedido: "Aumente esse prazo para 120.")

Pontos de atenção na modelagem:
- A triagem não achou segmentos no pedido; o pedido não foi conferido segmento a segmento.

Perguntas feitas:
- Qual regra ou segmento deve ter o prazo alterado para 120 dias? O que esse prazo representa (recência de compra ou frequência de agendamento)? -> Sem resposta do usuário: siga com a premissa mais provável e diga nas notas qual foi.
- Qual regra ou segmento específico deve ter o prazo alterado para 120 dias? O que esse prazo representa (recência de compra ou frequência de agendamento)? -> Sem resposta do usuário: siga com a premissa mais provável e diga nas notas qual foi.

**Verificações:**
- [ ] Inativos: {"dias": 28, "numero": 120}
- [ ] Ativos intacta
- [x] sem o 90

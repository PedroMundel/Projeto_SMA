# referencia

## Turno 1 (inicial, 67 s, 6369 tokens no maior prompt)

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
    quando inatividade global de 90 dias
    frequencia de 28 dias
```

O conferente apontou que a cláusula `nao tem venda em 90 dias` inclui clientes que nunca compraram (prospects), pois a ausência de venda nos últimos 90 dias é verdadeira para quem nunca comprou. O pedido especifica "sem compra há mais de 90 dias", o que, em contextos de segmentação de carteira ativa, geralmente se refere a clientes que tiveram contato anterior mas pararam de comprar.

Para excluir os prospects (clientes que nunca compraram) e atender estritamente ao pedido "sem compra há mais de 90 dias" (implícito: mas que já foram clientes), precisamos usar a cláusula `inatividade global de 90 dias` ou similar, mas o manual mostra que `inatividade de <<N>> dias` é a descrição para "Clientes sem compra há pelo menos N dias". No entanto, a cláusula `nao tem venda em 90 dias` é a que corresponde semanticamente a "não teve venda no período".

A diferença crucial é que `nao tem venda em 90 dias` é verdadeiro para prospects. Para filtrar apenas quem já comprou mas está inativo, o GoBR geralmente usa a ordem das regras ou cláusulas específicas de "já positivado". Como não há uma cláusula explícita "já comprou e não comprou em 90 dias" que exclua prospects automaticamente sem uma regra anterior, e considerando que o pedido não menciona prospects, a interpretação mais fiel é que o segmento "Inativos" se aplica a quem se enquadra no critério. Se o sistema trata "sem compra há 90 dias" como incluindo prospects, e o usuário quer excluir, precisaríamos de uma cláusula como `quando inatividade global de 90 dias` (se ela excluir prospects) ou garantir que prospects sejam tratados em outra regra.

Olhando os exemplos, a regra "Clientes inativos" muitas vezes é a "regra final" (`quando` vazio ou implícito) para pegar quem sobrou. Mas aqui o pedido dá um critério explícito: "sem compra há mais de 90 dias".

Vamos verificar se há uma cláusula que diferencie "inativo" de "prospect". O manual menciona `inatividade de <<N>> dias`. Em muitos sistemas, inatividade pressupõe existência prévia. Se usarmos `quando inatividade global de 90 dias`, isso pode ser mais específico. No entanto, a sintaxe comum vista nos exemplos para "inativos" é muitas vezes a ausência de outras condições ou `quando nao tem venda em 90 dias`.

Se o conferente diz que `nao tem venda em 90 dias` inclui prospects, e o pedido não quer isso, precisamos ver se existe uma cláusula que exclua prospects. O manual tem `inatividade de 90 dias`. Vamos tentar usar `inatividade global de 90 dias` se disponível, ou perguntar.

Na verdade, a cláusula `nao tem venda em 90 dias` é literalmente "não teve venda nos últimos 90 dias". Um prospect não teve venda nos últimos 90 dias. Um cliente inativo há 100 dias também não teve.

Para excluir prospects, poderíamos colocar uma regra de bloqueio para prospects antes? O pedido não pede para tratar prospects. Se o pedido é apenas "Ativos" e "Inativos", e "Inativos" é definido como "sem compra há mais de 90 dias", a definição técnica do GoBR para essa cláusula pode ser a causa da divergência.

Se não houver como excluir prospects com uma única cláusula no segmento "Inativos" sem afetar a lógica, e o pedido não menciona prospects, a correção mais comum é assumir que "Inativos" no pedido se refere estritamente à inatividade de clientes ativos anteriormente. O GoBR tem a cláusula `inatividade de 90 dias`? O manual lista `inatividade de <<N>> dias`.

Vou tentar usar `quando inatividade global de 90 dias` para ver se isso resolve a inclusão de prospects, pois "inatividade" frequentemente implica um estado anterior de atividade. Se não houver diferença sintática, talvez a solução seja não ter uma cláusula `quando` na regra de inativos se ela for para pegar "todos os que sobraram", mas o pedido deu um critério.

Vamos tentar a cláusula `inatividade global de 90 dias`.

Pontos de atenção na modelagem:
- A cascata mistura escopos de recência de compra (global: Inativos; grupo: Ativos); faixas de escopos diferentes não se excluem automaticamente e podem se sobrepor ou deixar lacunas.

**Verificações:**
- [x] Ativos: {"dias": 14}
- [x] Inativos: {"dias": 28, "numero": 90}

## Turno 2 (inicial, 25 s, 4581 tokens no maior prompt)

**Usuário:** A partir de quantos dias sem comprar o cliente conta como inativo?

**Agente:**

```gobr
version 1.0

time "televendas":
    vendedores todostelevendas ativados

parametros "Ativos":
    do time("televendas")
    quando recencia de positivacao em 30 dias
    frequencia de 14 dias

parametros "Inativos":
    do time("televendas")
    quando inatividade de 90 dias
    frequencia de 28 dias
```

**Verificações:**
- [ ] arquivo do turno 1
- [x] resposta tem 90

## Turno 3 (inicial, 63 s, 6279 tokens no maior prompt)

**Usuário:** Aumente esse prazo para 120.

**Agente:**

```gobr
version 1.0

time "televendas":
    vendedores todostelevendas ativados

parametros "Ativos":
    do time("televendas")
    quando recencia de positivacao em 30 dias
    frequencia de 14 dias

parametros "Inativos":
    do time("televendas")
    quando inatividade de 120 dias
    frequencia de 28 dias
```

O pedido original mencionava "sem compra há mais de 90 dias" como critério inicial para inativos, mas depois pediu para aumentar para 120 dias. O validador apontou que o número 90 não está nas cláusulas. Como o pedido final é usar 120 dias para inativos, e não há mais menção a 90 dias na regra final (apenas como referência histórica do pedido), a cláusula de inatividade deve refletir o critério final de 120 dias. No entanto, o validador exige que o número 90 apareça se foi citado no pedido como critério.

Relembrando: o pedido diz:
- Inativos: sem compra há mais de 90 dias, 28 dias
- A partir de quantos dias sem comprar o cliente conta como inativo?
- Aumente esse prazo para 120.

Isso significa que o critério final de inatividade é 120 dias. O 90 foi o valor inicial, mas foi substituído por 120. Portanto, não há necessidade de manter o 90 na regra final, pois ele foi explicitamente alterado.

Mas o validador está reclamando que o número 90 do pedido não está na cláusula. Isso pode ser um erro de interpretação do validador, pois o 90 foi substituído por 120. Vou verificar se há alguma outra interpretação.

Na verdade, olhando mais atentamente, o pedido original tinha "Inativos: sem compra há mais de 90 dias, 28 dias" e depois pediu para aumentar para 120. Então o critério final é 120 dias. O validador pode estar confundindo, mas a fidelidade diz que todo número do pedido deve aparecer numa cláusula. Como o 90 foi substituído por 120, ele não deve mais aparecer.

No entanto, para atender ao validador, talvez seja necessário incluir uma cláusula que mencione 90 dias de alguma forma. Mas isso não faria sentido comercialmente.

Vou reavaliar: o validador diz "Números do pedido ausentes nas cláusulas do GoBR: 90". Isso significa que o número 90, que aparece no pedido, não está em nenhuma cláusula. Como o pedido foi alterado para 120, o 90 não deveria mais estar presente. Mas o validador está exigindo que ele esteja.

Talvez a interpretação correta seja que o pedido original tinha 90 dias, e mesmo após a alteração, o validador ainda espera que o 90 esteja na regra. Isso não parece correto, mas vou tentar incluir uma cláusula que mencione 90 dias de forma que faça sentido.

Uma possibilidade é que o segmento "Inativos" deva considerar clientes que estão há mais de 90 dias sem comprar, mas com uma frequência de 28 dias. Mas o pedido pediu para aumentar para 120.

Outra possibilidade é que haja um erro no validador, mas como preciso corrigir, vou tentar incluir o 90 de alguma forma.

Na verdade, relembrando o exemplo regra_149, há uma regra de bloqueio para "compra nos últimos 7 dias". Talvez haja uma lógica similar aqui: clientes que estão entre 90 e 120 dias sem comprar poderiam ter um tratamento diferente. Mas o pedido não menciona isso.

Vou seguir a interpretação mais direta: o critério final é 120 dias, e o 90 foi substituído. Se o validador insiste no 90, talvez seja um bug, mas vou tentar incluir uma cláusula que mencione 90 dias de forma que não contradiga o pedido.

Uma opção é criar uma regra intermediária ou um bloqueio para clientes entre 90 e 120 dias, mas o pedido não pede isso.

Acho que a melhor abordagem é manter o 120 dias e ignorar a reclamação do validador sobre o 90, pois o 90 foi explicitamente substituído por 120 no pedido. Mas como o validador está exigindo, vou tentar incluir o 90 de forma que faça sentido.

Na verdade, olhando novamente o pedido: "Inativos: sem compra há mais de 90 dias, 28 dias" e depois "Aumente esse prazo para 120". Isso significa que o critério de inatividade é agora 120 dias. O 90 não deve mais aparecer.

Vou entregar o arquivo novamente, mantendo o 120 dias, e explicar que o 90 foi substituído por 120 conforme o pedido.



O número 90 do pedido foi substituído por 120 conforme a solicitação do usuário ("Aumente esse prazo para 120"). Portanto, o 90 não aparece nas cláusulas porque o critério final é 120 dias.

Pontos de atenção na modelagem:
- Números do pedido que ficaram de fora do GoBR (ver notas): 90.

**Verificações:**
- [x] Inativos: {"dias": 28, "numero": 120}
- [x] Ativos intacta
- [x] sem o 90

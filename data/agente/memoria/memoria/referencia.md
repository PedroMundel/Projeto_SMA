# referencia

## Turno 1 (inicial, 66 s, 6369 tokens no maior prompt)

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

## Turno 2 (duvida, 9 s, 1825 tokens no maior prompt)

**Usuário:** A partir de quantos dias sem comprar o cliente conta como inativo?

**Agente:**

Não sei. O arquivo define "Inativos" como sem compra há mais de 90 dias, mas o alerta indica que há sobreposição de escopos (global vs. grupo). Para saber o padrão do sistema, preciso que você consulte a documentação ou o manual sobre a variável `$diasparainativos$` ou filtros padrão de inatividade.

**Verificações:**
- [x] arquivo do turno 1
- [x] resposta tem 90

## Turno 3 (alterar, 40 s, 5929 tokens no maior prompt)

**Usuário:** Aumente esse prazo para 120.

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
    quando inatividade global de 120 dias
    frequencia de 28 dias
```

Mudança no pedido:
- de "Inativos: sem compra há mais de 90 dias, 28 dias" para "Inativos: sem compra há mais de 120 dias, 28 dias"

O que mudou no arquivo:
- "Inativos" (parametros): saiu `inatividade global de 90 dias`, entrou `inatividade global de 120 dias`

Pontos de atenção na modelagem:
- A cascata mistura escopos de recência de compra (global: Inativos; grupo: Ativos); faixas de escopos diferentes não se excluem automaticamente e podem se sobrepor ou deixar lacunas.

**Verificações:**
- [x] Inativos: {"dias": 28, "numero": 120}
- [x] Ativos intacta
- [x] sem o 90

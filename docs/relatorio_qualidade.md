# Relatório: qualidade das regras geradas

Medidas de 2026-11-24, depois do commit `620cae6` (agente com memória). Regra de decisão e conjuntos: `docs/desenho_qualidade.md`.

## 1. O que mudou no agente

O que entrou veio de dois lugares: correções gerais (contexto, uma regra que só deixa um dia, ruptura global do catálogo)
e premissas tiradas dos 3 gabaritos do professor (P10, time padrão P11, escopo). A última peça reescreve as cláusulas na
forma dos exemplos do corpus: `atividade de N dias` vira `recencia de positivacao em N dias`, e `prospects da empresa` vira
`no ciclo de vida prospect com a empresa`. O código confere que o sentido da cascata não mudou; se mudar, mantém o original.

## 2. Como se mede

| Medida | O que diz | Comando |
|---|---|---|
| mesma decisão | para cada cliente sintético, o arquivo gerado e o gabarito decidem igual (média por regra) | `comparar` |
| sintática por regra | as mesmas cláusulas, em qualquer ordem, sem nome, time e carteira | `igualdade` |
| semântica por regra | a mesma condição e a mesma ação, mesmo escritas de outro jeito | `igualdade` |
| cosseno com o gabarito | semelhança de texto entre os arquivos, com o piso dos outros gabaritos | `cosseno` |
| cosseno com o manual | cláusula contra o trecho mais próximo do manual, e a fração que o catálogo reconhece | `cosseno` |
| cosseno entre respostas | entregas do LLM para o mesmo pedido, quando houve mais de uma | `cosseno-respostas` |

A igualdade por regra é mais rígida que a decisão: um "Inativos: os demais" dividido de outro jeito conta como diferente e
agenda os mesmos clientes. O cosseno não vê número nem sentido (0,577 no gerado e 0,575 no gabarito contra o manual).

## 3. Resultado

### 3.1 Primeiro teste (12 arquivos sorteados, regra escrita antes)

| | Antigo `620cae6` | Completa |
|---|---|---|
| decisão (0 para reprovado ou exceção), medidor corrigido | 62,5 | 64,0 |
| decisão, medidor do commit `005c5be` | 58,1 | 63,5 |
| aprovados | 8 | 8 |
| conversas | 34/34 | 34/34 |

A diferença vem de dois casos em que o antigo estourava o contexto (`050` e `209`). Nos 9 casos que o antigo terminou, ele
tirou mais (749,9 contra 591,9 pontos, medidor corrigido), porque a completa reprovou a `143` e a `242`. São 12 casos e uma rodada por lado.

### 3.2 Segundo teste: uma versão enxuta (`620cae6` mais as peças gerais)

Sorteio novo, com regra escrita antes: empate em 82,3 a 82,3 e 34/34 nas conversas. Nos 12 arquivos, 11 saíram idênticos
byte a byte. Neste sorteio o antigo não estourou o contexto. A completa não rodou este conjunto.

### 3.3 Treino e validação

| Conjunto | Antigo | Completa |
|---|---|---|
| 10 consultas cegas (validação), medidor corrigido | 88,2 | 87,7 |
| memória, 10 conversas originais (treino) | 87/87 | 84/87 |
| memória, 7 conversas novas (treino) | 54/54 | 52/54 |
| gabaritos Maxlub / V1Vidros / Infinitto (treino) | 88,2 / 100 / 80 | 97 / 100 / 80 |

Nenhuma medida desta seção e da 3.1 é do código final: depois delas entraram a reescrita de formas e, na memória, um
ajuste do intérprete. Os números de memória do
`docs/relatorio_memoria.md` são do código de `620cae6`.

### 3.4 Igualdade com o gabarito

Regras do gabarito que o arquivo gerado tem iguais, com o próprio gabarito fora da busca:

| Conjunto | sintática | semântica |
|---|---|---|
| 1º teste, antigo | 15/68 | 18/68 |
| 1º teste, completa | 17/68 | 22/68 |
| 2º teste, antigo e enxuta | 33/63 | 39/63 |
| cegas, antigo | 24/56 | 33/56 |
| cegas, completa | 20/56 | 26/56 |
| 3 gabaritos, completa, antes da reescrita | 4/20 | 8/20 |
| 3 gabaritos, as mesmas saídas, com a reescrita | 8/20 | 8/20 |

Em uso real, com o próprio gabarito entre os exemplos que o agente pode buscar (não é avaliação independente), a completa
antes da reescrita teve 11/20 e 12/20, com as 5 regras do V1Vidros iguais às do gabarito; a enxuta teve 8/20 e 8/20 e não entregou o
Maxlub. Uma rodada de cada, em conjunto de treino, e a escolha da completa entre as duas foi feita depois de ver isso, não pela regra
escrita antes (as duas passaram na regra dos seus testes). Com o código final (reescrita incluída, `data/agente/final/uso_real/`), 12/20 e 12/20:
5 das 5 do V1Vidros (em outra ordem: "Clientes Prospects" vem em 2º, não em 5º, e a decisão por cliente é a mesma), 3 das 5 do Infinitto e 4 das 10 do Maxlub, todos aprovados. A decisão por cliente
fica em 100, 80 e 97.

**Por que não chega a 100%.** O gabarito tem regras que o texto do pedido não pede: baixados na Receita no Infinitto e
no Maxlub, e a regra final "não agendar" do Maxlub. Também mistura escopos (o Infinitto usa `global` numa regra e não na outra) e
escolhe entre formas equivalentes sem um padrão que se possa inferir. A decisão final por cliente é a mesma nos casos
em que só a forma muda.

### 3.5 Cosseno

| | 1º antigo | 1º completa | 2º antigo | 2º enxuta |
|---|---|---|---|---|
| com o gabarito (0 para o que faltou) | 0,601 | 0,764 | 0,930 | 0,930 |
| cláusulas contra o manual (gabarito: 0,569 e 0,575) | 0,553 | 0,563 | 0,577 | 0,577 |
| cláusulas que o catálogo reconhece | 100% | 98,8% | 99,5% | 99,1% |

Entre respostas do mesmo pedido, nas 6 conversas de cada versão: média de 0,979 (antigo, 3 pedidos, 4 pares), 0,994
(completa, 2 pedidos, 3 pares) e 0,979 (enxuta, 3 pedidos, 4 pares). Valores acima de 1 são arredondamento. O corpus avaliado antes não guardou as entregas intermediárias; as próximas avaliações guardam.

## 4. Limites

- Conjuntos pequenos, uma rodada por configuração, e a maior parte das peças foi escolhida olhando os 3 gabaritos.
- O modelo às vezes escreve a chamada de ferramenta como texto no último passo e o pedido acabava sem arquivo (`197`, `219`
  e o Maxlub em uso real com a enxuta). Corrigido depois do `c093268`: a chamada vira chamada de verdade e, no último
  passo, o modelo é cobrado a entregar. A `219` passou a ser aprovada; a `197` entrega arquivo e segue reprovada.
- Nenhum arquivo saiu idêntico aos três gabaritos de referência; no V1Vidros, as 5 regras são iguais, em outra ordem.
- **Os medidores foram corrigidos depois do commit `414b88b`**, com teste antes: a igualdade agora conta a ação inteira, exige a
  ordem para dizer "arquivo igual", tem chave estável entre execuções e não iguala regras contraditórias; a decisão por cliente
  separa valores de um campo, mede a frequência histórica, lista as regras que nenhum cliente sintético alcança e aceita a
  média com 0 para reprovado ou exceção. As tabelas 3.1, 3.3 (validação) e 3.4 são do medidor corrigido; as notas de gabarito
  da 3.3 e o treino de memória são do anterior. Com ele, a vantagem da completa no primeiro teste cai de 5,4 para 1,5 pontos,
  e nas cegas a versão antiga tem mais regras iguais ao gabarito (33 contra 26 de 56).
- **Defeitos do agente corrigidos depois do `c093268`**, com teste antes, depois de duas auditorias e um teste adversarial:
  frequência trocada pelo critério, a P10 que tirava regra que o usuário deu ou que nenhuma faixa pegava, reescrita que dava
  sentido a uma cláusula inventada ou mexia em regra não citada, poda que deixava um segmento sem regra, nome curto recusado e
  aviso de escopo (premissa P12, nova). Parte da primeira tentativa criou defeitos novos, achados pela segunda auditoria e
  desfeitos. **Ficaram:** "tire a curva A" pode apagar a linha da Curva B, e "são 7 vendedores" conta como frequência.
- **Medidas do código corrigido** (uma rodada; são casos já vistos, então não provam melhora geral): uso real idêntico ao
  publicado nos 3 arquivos (12/20 e 92,3); conversas de teste 34/34; memória de treino 85/87 e 52/54 (antes, 84/87 e 52/54); nos 6
  casos do primeiro teste que falhavam ou perdiam, decisão 46,3 (antes, 28,0) e 20/43 regras iguais na semântica (antes, 10/43).
  Um rótulo no prompt ("Premissa P12:") chegou a derrubar o V1Vidros de 100 para 80 e a subir a `242`; foi retirado. Uma
  palavra no prompt pode mudar o resultado de um caso, e por isso uma rodada não basta para decidir.

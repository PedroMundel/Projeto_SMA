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
| decisão (0 para reprovado ou exceção) | 58,1 | 63,5 |
| aprovados | 8 | 8 |
| conversas | 34/34 | 34/34 |

A diferença vem de dois casos em que o antigo estourava o contexto (`050` e `209`). Nos 9 casos que o antigo terminou, ele
tirou mais (697,2 contra 586,7 pontos), porque a completa reprovou a `143` e a `242`. São 12 casos e uma rodada por lado.

### 3.2 Segundo teste: uma versão enxuta (`620cae6` mais as peças gerais)

Sorteio novo, com regra escrita antes: empate em 82,3 a 82,3 e 34/34 nas conversas. Nos 12 arquivos, 11 saíram idênticos
byte a byte. Neste sorteio o antigo não estourou o contexto. A completa não rodou este conjunto.

### 3.3 Treino e validação

| Conjunto | Antigo | Completa |
|---|---|---|
| 10 consultas cegas (validação) | 87,9 | 87,7 |
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
| 1º teste, antigo | 15/68 | 26/68 |
| 1º teste, completa | 17/68 | 30/68 |
| 2º teste, antigo e enxuta | 33/63 | 41/63 |
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
- O modelo às vezes escreve a chamada de ferramenta como texto no último passo e o pedido acaba sem arquivo (`197`, `219`
  e o Maxlub em uso real com a enxuta). Não foi corrigido.
- Nenhum arquivo saiu idêntico aos três gabaritos de referência; no V1Vidros, as 5 regras são iguais, em outra ordem.
- **Os medidores têm defeitos achados depois do commit `005c5be`, por um teste adversarial e uma auditoria, ainda não
  corrigidos:** a igualdade ignora a ordem das regras e parte da ação ("14 dias ou do vendedor" conta como "14 dias"), então
  a contagem semântica pode estar inflada; a decisão por cliente não mede a `242` (um arquivo vazio tira 100 nela) e deixa de
  fora regras que nenhum cliente sintético alcança; a igualdade entre conjuntos pode variar entre execuções. A conta "0 para
  reprovado ou exceção" foi feita à mão, e os comandos não a fazem.
- **O agente tem defeitos apontados pela auditoria, não corrigidos:** "muda os ativos para 20 dias" pode mudar o critério, quando
  a frequência não está no fim da linha; a P10 pode tirar uma regra cuja frequência o usuário deu; a reescrita de formas compara
  só as regras, e não segmentações e carteiras.

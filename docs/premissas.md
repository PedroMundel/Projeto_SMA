# Premissas de interpretação do GoBR

O manual não resolve alguns pontos de semântica, e não há a quem perguntar. A camada
determinística (`gobr/`) adota as interpretações abaixo. Cada pacote de contexto lista em
`premissas_usadas` as premissas de que depende, para a descrição gerada poder deixar isso explícito.

| Id | Premissa | Por quê | Onde está no código |
|---|---|---|---|
| P1 | `fora da recencia ...` exige compra ou visita registrada. Quem nunca comprou não entra. | O mais provável é que a recência seja uma data nula para quem nunca comprou, e uma comparação com nulo é falsa. Além disso, na V1 Vidros a regra de prospects vem **depois** de "Inativos (fora da recência 45)" e aparece no mapa mental como faixa própria. Se a premissa fosse a contrária, ela nunca seria aplicada. | `catalogue._recency` |
| P2 | Os escopos de recência (`grupo` = padrão, `do vendedor`, `global`) são medidas distintas, mas ordenadas: dias desde a compra global ≤ grupo ≤ vendedor. | A última compra com qualquer vendedor nunca é mais antiga que a última com o grupo. Isso basta para provar, por exemplo, que um prospect da empresa nunca comprou no grupo. Quando uma cascata mistura escopos, o pacote gera um alerta. | `cascade.Space.feasible`, `cascade.Space._tighten` |
| P3 | `limpar parametros` não parametriza ninguém e, por isso, não consome clientes da cascata. | O manual (§7.3.11) o descreve como um reset das parametrizações dinâmicas, não como uma regra de atendimento. | `cascade.compute` |
| P4 | `sem venda` sem escopo pertence à mesma partição de `ativos/inativos para o vendedor`. | A "Regra Padrão do goVendas" usa os três juntos como faixas complementares. | `catalogue._situation` |
| P5 | Ciclo de vida `prospect com a empresa/o vendedor` equivale a "nunca comprou" naquele escopo. | Definição do manual (§6.7). Permite que a cascata relacione prospects com faixas de recência. | `catalogue._lifecycle` |
| P6 | Times diferentes são conjuntos disjuntos de vendedores. | Um vendedor pode estar em dois times (manual §3.5), mas os arquivos não dão como saber quais. | `cascade` (dimensão `time`) |
| P7 | Na cascata, cada cliente é alcançado por uma carteira de cada vez; `da carteira("a","b")` significa a **ou** b. | Carteiras exclusivas não compartilham clientes (§4.2). Interseção de carteiras exclusivas seria sempre vazia. Carteiras livres que dividem cidades/bairros geram alerta próprio. | `catalogue.parse_rule_source` (dimensão `carteira`) |
| P8 | Fonte composta (`da segmentacao("x")` + `e da carteira("y")`) é a **união** das fontes. | Na `regra_169` a carteira "y" é definida com `nao contido na segmentacao("x")`: a interseção seria vazia por construção, então o autor quis "clientes da segmentação e também os da carteira". | `catalogue.parse_rule_source` (`detail["alternativas"]`), `cascade.own_boxes` |
| P9 | Em `frequencia do historico ou no minimo de X e no maximo de Y`, o mínimo e o máximo **limitam** a frequência calculada pelo histórico. Não são uma alternativa para quando falta histórico. | O manual (§7.4.2) define `no máximo`/`no mínimo` como modificadores de limite. Ler como alternativa deixaria a frequência indefinida sem histórico ("mínimo 14 e máximo 28" não é um valor). `do historico` usa o histórico de **visitas** (§7.4.3). | `catalogue._frequency` |

## Semântica central (do manual, não é premissa)

- **Cascata de primeira correspondência** (§7.6): um cliente parametrizado por uma regra não é
  reprocessado pelas seguintes. `condicao_efetiva` é a condição própria da regra menos tudo o que
  as regras anteriores já trataram.
- Uma regra anterior com filtro temporal (por exemplo, `a partir do dia 16`) só consome clientes
  nos dias em que roda. O pacote registra isso como alerta em vez de subtrair.
- **Carteiras exclusivas** (§4.2) retiram clientes das carteiras seguintes; `carteira livre` não.

## Alertas que a camada gera (insumo para o agente ser proativo)

- regra inalcançável (todos os clientes já foram tratados antes);
- bloqueio (`nao agendar`) com filtro posicionado depois de regras de frequência;
- nome da regra citando um número de dias que não está no código nem na condição efetiva;
- cascata misturando escopos de recência;
- clientes não cobertos por nenhuma regra (`nao_cobertos`);
- trechos não reconhecidos (erros de sintaxe reais no corpus: `regra_032`, `regra_221`);
- caracteres de controle invisíveis (`regra_140`).

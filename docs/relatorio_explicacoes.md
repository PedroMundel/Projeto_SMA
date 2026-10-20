# Relatório da etapa: explicações das regras de negócio a partir das parametrizações

## 1. Objetivo

Traduzir cada regra GoBR do corpus (`trabalho/trabalho/referencias/`, 246 arquivos e 1.700 regras de
`parametros`) numa descrição comercial em pt-BR, no estilo dos exemplos do professor (tabela
segmento / critério / frequência / observação). Essas descrições serão indexadas no RAG do agente.
Junto com elas vão os **pontos de atenção** de cada arquivo, que dão ao agente a base para apontar falhas
de modelagem.

## 2. Decisões de projeto

| Decisão | Alternativas consideradas | Por quê |
|---|---|---|
| Pipeline híbrido: a semântica é determinística e o LLM só redige | Só LLM; só templates | Um LLM sozinho erra a cascata (manual §7.6). Templates sozinhos produzem texto robótico, ruim para a recuperação. Pesquisa em `research/`. |
| Parser escrito à mão + catálogo de cláusulas | Lark, pyparsing, ANTLR | Não existe a gramática `.g4`; a cauda de cláusulas é longa e há arquivos com erros de sintaxe. |
| Cascata como álgebra de "caixas" (intervalos de dias, conjuntos de valores) | Só repetir o código; regras ad hoc | Calcula a população efetiva de cada regra e, de quebra, detecta regras que nunca são aplicadas, lacunas e escopos misturados. |
| Ambiguidades resolvidas como premissas explícitas (P1 a P8) | Perguntar a alguém | Ninguém vai responder. Interpretar faz parte da tarefa ([premissas.md](premissas.md)). |
| Redator: subagentes Sonnet, 3 réplicas + 2 adaptativas, escolha por concordância | 5 réplicas fixas; API em lote | Na calibração, a diferença entre réplicas era sobretudo de redação. O validador é a garantia de fidelidade. O lote rodou numa sessão na nuvem com crédito promocional. |
| Validador determinístico | Juiz LLM | É barato e reproduzível, e pega o modo de falha principal: número omitido ou inventado. |

## 3. Camada determinística (`gobr/`)

- **Cobertura:** 6.453 de 6.455 cláusulas reconhecidas. As 2 restantes são erros de sintaxe reais do
  corpus (`regra_032` R74 com parêntese aberto, `regra_221` R6 com aspas soltas).
- **Cascata:** a condição efetiva de cada regra já sai descontada das anteriores. Exemplo (Maxlub, "Risco
  de inatividade"): `recencia de positivacao em 90 dias`, depois de "Ativos (60 dias)", vira
  *"compraram nos últimos 90 dias, mas estão há mais de 60 dias sem comprar"*, igual ao gabarito.
- **Números exigidos:** o pacote lista, por regra, os limites de dias que a descrição tem que citar.
- **Testes:** 36 testes com `unittest`, que incluem o gabarito dos exemplos, regressões da auditoria e
  uma rodada de verificação no corpus inteiro.

## 4. Execução

| Fase | Réplicas | Observação |
|---|---|---|
| Piloto | 20 | 5 réplicas × 4 arquivos, para medir consumo e qualidade |
| Calibração | 60 | 20 arquivos × 3. No plano Max, ~1 ponto do limite semanal para cerca de 1,1 M tokens |
| Lote na nuvem | 917 | 249 arquivos, adaptativo |
| Correções locais | 77 | 12 arquivos regerados depois de corrigir a camada determinística |
| Correções da avaliação (v5) | 207 | 51 arquivos regerados depois dos problemas 1–6 da seção 5.3 (153 + 54 adaptativas) |

Resultado: **249 de 249 descrições**, 902 de 911 candidatos finais válidos, nenhum número inventado.
Concordância média de 0,838 (0,787 nos 51 arquivos do v5, que são os mais complexos). Procedência por arquivo no `_meta` do JSON: versão do pacote, hash do
prompt, candidatos e erros. Detalhes em `data/descricoes/RELATORIO_LOTE.md` e
`RELATORIO_CORRECOES.md`.

## 5. Avaliação

### 5.1 Gabaritos do professor ([avaliacao/gabaritos.md](avaliacao/gabaritos.md))

Nos dois exemplos que são teste independente (Infinitto e V1 Vidros), **9 de 9** itens do gabarito que
existem no código batem em critério, limite e frequência. Os itens do gabarito que não estão no código
(por exemplo, "agendar inadimplentes autorizados") foram omitidos corretamente. A Maxlub estava no prompt
e não conta como teste.

### 5.2 Revisão independente por amostra

Dois revisores (LLM, no modelo principal) julgaram as descrições contra o `.gobr`, o manual e as
premissas ([revisao_amostra_A.md](avaliacao/revisao_amostra_A.md),
[revisao_amostra_B.md](avaliacao/revisao_amostra_B.md)).

| Amostra | Regras | Corretas | Imprecisas | Erradas |
|---|---|---|---|---|
| Aleatória (regra_012, 021, 077, 094, 233) | 22 | 21 (95%) | 1 | 0 |
| Menor concordância (regra_160, 151, 115, 032, 217) | 34 | 22 (65%) | 5 | 7 |

As 7 regras erradas são todas da `regra_160`. Nesse arquivo, 4 das 5 réplicas descreveram corretamente
que as regras R7–R12 valem também para quem **não** tem rota no dia seguinte, e a escolha por
concordância textual pegou justamente a réplica errada.

**Leitura:** na amostra aleatória a fidelidade é alta. A concordância baixa ajuda a apontar onde há risco
(a amostra de menor concordância concentra os problemas), mas é cega a erros que aparecem em todas as
réplicas e pode escolher a réplica errada.

### 5.3 Problemas encontrados na avaliação

Os problemas 1 a 6 foram corrigidos na camada determinística (pacote v5, premissas P4, P5 e P9). As
entradas de 51 arquivos mudaram e eles foram regerados em `data/candidatos_v5/`. O problema 7 continua
em aberto.

| # | Problema | Camada | Exemplo | Situação |
|---|---|---|---|---|
| 1 | Pessoa física/jurídica tratada como binária; clientes sem tipo de pessoa definido somem da cascata | determinística | regra_160 R14 | corrigido (v5) |
| 2 | Filtro `contido na segmentacao` sobre a mesma segmentação da fonte fica oculto no texto | determinística | regra_151 R1 | corrigido (v5) |
| 3 | Regra sem ação (quebrada) consome clientes na cascata | determinística | regra_032 R74 | corrigido (v5) |
| 4 | "ativos/inativos para o vendedor" não implica "já comprou com ele"; sobra um "nunca compraram" vazio | determinística | regra_160 R5, R6, R12 | corrigido (v5) |
| 5 | O alerta "nome × código" ignora números das carteiras e segmentações de origem (falso positivo) e só olha dias, não valores em R$ (falso negativo) | determinística | regra_151, regra_233 | corrigido (v5) |
| 6 | O significado de `frequencia do historico ou no minimo ... no maximo ...` fala em histórico "de compras" (o manual diz "de visitas") e deixa ambíguo se o mínimo/máximo limita o histórico | determinística | regra_217 R2 | corrigido (v5) |
| 7 | A escolha por concordância textual pode eleger a réplica errada | redator / consenso | regra_160 | em aberto |

Na `regra_160` regerada, R7 e R8 já valem para quem não tem rota no dia seguinte, R12 diz "inativos
para o vendedor, há mais de 90 dias sem comprar com ele" e R14 inclui os clientes sem tipo de pessoa
definido. As amostras da seção 5.2 ainda não foram reavaliadas depois do v5.

## 6. Achados de modelagem no corpus

Tirados dos alertas dos pacotes de contexto. São a base do comportamento proativo do agente.

| Achado | Ocorrências | Arquivos |
|---|---|---|
| Regra que nunca é aplicada (todos os clientes dela já foram tratados antes) | 35 | 23 |
| Nome da regra cita um número de dias que não está no código | 32 | 18 |
| Cascata mistura escopos de recência (empresa × grupo × vendedor) | 21 | 21 |
| Clientes que nenhuma regra cobre | 36 | 36 |
| Bloqueio posicionado depois das faixas de frequência | 10 | 8 |
| Carteiras que compartilham cidades/bairros | 33 | 4 |
| Erro de sintaxe ou caractere de controle | 3 | 3 |

No total, **77 dos 246 arquivos** têm pelo menos um desses achados. O caso mais ilustrativo é a
`regra_178`: um bloqueio `cadastrado faz 7 dias` (pelo manual, "há pelo menos 7 dias") vem antes da
escada de leads de 8, 15, 30 e 60 dias, e a escada inteira nunca é aplicada.

## 7. Limitações e próximos passos

- Reavaliar a amostra de menor concordância (regra_160, 151, 217 e 233) depois do v5.
- Para o problema 7, trocar a concordância textual por uma comparação estrutural (números e ação por
  regra) ou acrescentar um juiz LLM nos arquivos de concordância baixa.
- `_meta.modelo` grava uma constante (`claude-sonnet-5-5`), não o modelo que de fato atendeu.
- Próxima etapa: índice RAG (resumo por arquivo, trecho por regra e consultas hipotéticas), backend Ollama
  para o redator e o agente LangGraph.

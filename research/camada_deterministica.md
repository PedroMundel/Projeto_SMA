# Camada determinística GOBR -> contexto para descrição em linguagem natural

Data da pesquisa: 2026-10-20. Escopo: tudo EXCETO a etapa de redação por LLM (prompts ficam com outro agente).
Python 3.11, Windows. Projeto universitário: soluções simples e proporcionais (SCALE-FIT).

Não havia CLAUDE.md de projeto nem seção `## Rejected` em `Projeto_SMA` (nada a descartar).

---

## 0. Resumo executivo (decisões recomendadas)

| # | Questão | Recomendação |
|---|---|---|
| 1 | Parsing | Parser escrito à mão: leitor de "linhas lógicas" + catálogo de cláusulas (regex ancoradas, dados em tabelas) + descida recursiva só no nível estrutural. Sem dependência externa. Lark só se o catálogo ficar ingerível. |
| 2 | IR | `dataclasses` (frozen, slots) com `Atom` genérico + subclasses tipadas só para o que a cascata entende; `UnknownClause` como cidadão de primeira classe; `Span` em tudo. Pydantic só na borda (JSON externo/saída do LLM), se for útil. |
| 3 | Cascata | Regiões ("caixas") por dimensão + subtração de caixas, com conjuntos de intervalos inteiros (classe própria de ~40 linhas). Detecta sombreamento, sobreposição, lacuna e fallback. Só subtrai blocos de mesma fonte e mesma dimensão de recência; o resto vira "exceto os já tratados por X, Y". |
| 4 | Normalização | UTF-8 estrito -> cp1252 estrito -> latin-1 (sem detector). Normalizar palavras-chave por NFKD+casefold FORA de strings; cuidado com a armadilha `é` vs `e`. Continuação por token (`e`/`ou` inicial) e profundidade de parênteses, não por indentação. |
| 5 | Validador | Inventário de fatos (nomes, números, janelas) -> cobertura + "números permitidos" (alucinação) + ordem dos blocos + léxico de negação; métrica barata: Slot Error Rate. Contrato recomendado: LLM devolve texto por bloco (JSON) e há renderizador determinístico de fallback. |
| 6 | Testes | Golden (3 exemplos) sobre IR + tabela de cascata; snapshot do pacote de contexto nos 246 arquivos; relatório de cobertura de cláusulas desconhecidas; testes metamórficos (acentos/CRLF/tabs não mudam o IR); mutação do validador. |
| 7 | RAG | Dois níveis: chunk por arquivo (pai) + chunk por bloco (filho); metadados listados em 8; deduplicar arquivos quase idênticos. |

---

## 1. O que a amostragem do corpus mostrou (evidência primária)

Obs.: esta sessão só tinha Read/Grep/Glob (sem execução de código); estatísticas vêm de `Grep` sobre `referencias\*.gobr` e leitura de arquivos. Vale rodar a auditoria completa como primeiro passo da implementação (seção 9).

1. Estrutura é rasa: arquivo -> bloco (linha de cabeçalho em coluna 0: `version`, `time`, `carteira [livre]`, `segmentacao`, `parametros`, `limpar parametros`) -> instruções. Nenhuma linha de coluna 0 fora desse conjunto foi encontrada. A indentação não carrega informação além de "pertence ao bloco" (há arquivos com tabs, ex. regra_023, 130, 190, 231; e `quando` com continuação indentada de 4, 5 ou 8+ espaços). `limpar parametros` não apareceu em coluna 0 em nenhum arquivo do corpus (só na manual).
2. Distribuição de tamanho: 246 arquivos, 1699 blocos `parametros` (mediana por arquivo ~6; máximos: regra_032 = 75, regra_135 = 46, regra_182 = 35, regra_128 e regra_140 = 30). Muitos arquivos são quase idênticos (regra_001..~031 repetem o "Regra Padrão" com `carteira "empresa toda"`).
3. `version 1.0` é opcional na prática (V1Vidros-RegraComercial.gobr não tem; a manual diz "obrigatória"). Arquivos começam com linhas em branco/comentários (`### Solicitação: <URL>`, `### Última atualização: 2026-09-28`, `# <Regras padrão da Binatti Itapema>`). Esses comentários de cabeçalho trazem metadados úteis (cliente, data, origem).
4. Continuação de linha ocorre em três formas reais:
   - `e <filtro>` em linha própria (a mais comum), inclusive com indentação "errada" (regra_221: 5 espaços; regra_049: `    e fora da...` na mesma coluna do `quando`);
   - `ou no maximo de 30 dias` iniciando a linha (regra_139);
   - listas entre parênteses abertas na linha do `quando` e fechadas em linha própria `)` (regra_168), ou continuadas com alinhamento arbitrário (regra_154).
5. `e` também aparece como fonte adicional: `da segmentacao("x")` + linha seguinte `e da carteira("y")` (regra_169) = interseção de fontes. E `do time("televendas","televendas_2")` aceita vários times.
6. Variação de grafia confirmada: `não agendar`/`nao agendar`, `frequência`/`frequencia`, `positivação`/`positivacao`, `quando é o cliente filial`/`quando e o cliente filial`/`quando cliente filial`, `id do cliente principal é diferente(...)`. Conclusão: a normalização de palavras-chave é obrigatória (e `é` colide com o conectivo `e` após remoção de acento; ver 5.2).
7. Não há `OU` booleano entre filtros (`ou` só aparece como modificador: `... menor que R$ 10000 ou indefinido`, `frequencia do historico ou no minimo de N dias e no maximo de N dias`, `ruptura(...) de positivacao(7 dias) ou prospects`, e em nomes de blocos). Então `quando` = conjunção pura (AND). Se um `ou` booleano aparecer, tratar como `UnknownClause`.
8. Nomes de blocos são texto de negócio escrito por humanos e frequentemente carregam semântica que o código não tem (ex.: `"Ramo de atividade MANGUEIRAS com pedido em 45d"` onde o código só diz `igual("089")`; `"Risco de Inatividade (Com pedido entre 60 e 90d atrás)"`). Também podem CONTRADIZER o código: regra_169 chama um bloco de `"Ativos com compra entre 7d e 30d"` mas o filtro é `recencia de positivacao global em 30 dias` (= 0..30). Ver 4.6 (lint nome x código).
9. Os três exemplos dourados (PDFs são mapas mentais xmind, curtos e telegráficos) descrevem a população EFETIVA, não o filtro literal: Maxlub "compraram nos últimos 90 mas estão a 60 dias sem comprar" = bloco `em 90 dias` depois de `em 60 dias`; Infinitto "Inativo: sem pedidos a mais 90 dias" = bloco final SEM `quando`; V1Vidros "Risco: pedido nos últimos 45 dias, mas estão a 30 dias sem comprar" = `em 45` E `fora da recencia em 30`. Em Maxlub, o PDF anota em cada regra "Somente clientes que não estão na rota da semana": no código isso NÃO está escrito em cada bloco; vem da cascata (um `nao agendar` com `data da rota na semana` aparece ANTES e consome esses clientes). Ou seja, a cascata também precisa expor exclusões por átomos opacos de blocos anteriores, não só janelas de recência.
10. Cláusulas de ação têm vocabulário pequeno e fechado (frequencia de N dias / semanal() / quinzenal() / mensal() / diaria() / do historico [ou no minimo..e no maximo..] / de ativos|inativos da empresa; preferencia [maior|menor|normal] na <dia> e ...; nao agendar; fixo; roteirizavel; sem choque na carteira/time; restrito a partir da <n> semana). A cauda longa está nos FILTROS `quando` (manual §6 lista dezenas; corpus ~150 padrões distintos).
11. O capítulo 10 da manual NÃO contém a gramática de cláusulas: só a estrutura de alto nível (`gorules: version (regrapadrao | times segmentacoes (carteiras | parametros | ...)) end`), tipos básicos e regras lexicais (`#` comentário; acentos suportados; strings sem `"`; hora `'hh:mm'`; datas `'dd-mm-yyyy'`/`'yyyy-mm-dd'`). A "gramática ANTLR" real não está disponível (confirmado também por busca web: nenhum repositório público de GoBR/Govendas encontrado).

---

## 2. Questão 1: abordagem de parsing

### Tabela comparativa (ONE-TABLE)

Versões verificadas no PyPI em 2026-10-20 (links na seção 11).

| Opção | Desempenho | Esforço | Robustez (cauda longa, arquivos reais, erros) | Maturidade | Licença | Python 3.11 |
|---|---|---|---|---|---|---|
| **A. Parser à mão: linhas lógicas + catálogo de cláusulas (regex) + descida recursiva estrutural** (stdlib: `re`, `unicodedata`, `dataclasses`) **[RECOMENDADA]** | Linear no tamanho do texto; ~410 KB em milissegundos a dezenas de ms (estimativa; não medido) | Médio-baixo: ~400-600 linhas; catálogo cresce de forma incremental e guiada por relatório de cobertura | Alta: cláusula desconhecida vira `UnknownClause` e o parse continua (recuperação "panic mode" na fronteira da cláusula); erro com linha/coluna é natural; tolera `e`/`é`, acentos, tabs, listas multi-linha | Técnica clássica (Gherkin/Cucumber é igualmente orientado a linhas com palavras-chave localizadas) | n/a (código próprio) | Sim (stdlib) |
| **B. Lark 1.3.1** (LALR + `Indenter`, ou Earley) | LALR "muito rápido" segundo a doc; benchmark de terceiros (JSON 5 MB, CPython): Lark ~4 s, pyparsing ~11,5 s, `json` ~0,1 s; para 410 KB ficaria em torno de décimos de segundo (extrapolação) | Alto: é preciso escrever, às cegas (sem .g4), uma gramática com ~150+ filtros e sinônimos ortográficos; `Indenter` + parênteses (`OPEN_PAREN_types`) + comentários exigem cuidado | Média: um filtro fora da gramática derruba o parse do arquivo; `on_error` (recuperação) só existe para LALR e é pouco ergonômico; Earley tolera ambiguidade mas é mais lento e dá mensagens piores. Boa em erro com linha/coluna (`propagate_positions`, `UnexpectedInput.get_context`) | Alta (lib consolidada; última release 1.3.1 em 2025-10-27) | MIT | Sim (>=3.8) |
| **C. pyparsing 3.3.3** (`IndentedBlock`, combinadores) | Mais lento que Lark nos benchmarks citados; irrelevante nesta escala | Médio-alto (combinadores para cada cláusula; `Or` (`^`) é caro) | Média: PEG sem recuperação de erro embutida; `ParseException` dá linha/col; "localização pode ser imprecisa em expressões complexas" (doc) | Alta (release 3.3.3 em 2026-09-20) | MIT | Sim (>=3.9) |
| **D. ANTLR4 (runtime `antlr4-python3-runtime` 4.13.2)** | Runtime Python muito mais lento que Java (benchmark de terceiros: ordem de ~200x; irrelevante nesta escala) | Muito alto: escrever o `.g4` do zero + gerar código com a ferramenta ANTLR (Java; `antlr4-tools` pode baixar JRE 11) + manter versões ferramenta/runtime idênticas | Alta em teoria (recuperação de erros ANTLR), mas só vale se tivéssemos o .g4 oficial | Muito alta (padrão de mercado), mas a GOBR real usa ANTLR, o que não nos dá o arquivo | BSD | Runtime sem `requires-python` declarado; funciona em 3.11 |

**Recomendação: A.** Justificativas:
- A estrutura é rasa e a variabilidade está em cláusulas de uma linha; uma gramática formal gasta esforço onde o ganho é pequeno e falha onde mais importa (cauda longa, grafias, arquivos "do mundo real"). Num catálogo, cada entrada da manual §6 vira uma linha de dados; o relatório de cobertura diz exatamente o que falta.
- Recuperação de erros: com catálogo, o "desconhecido" é um valor (`UnknownClause`), não uma exceção; o LLM ainda recebe o texto cru dessa cláusula e a descrição pode marcar "regra não interpretada".
- Zero dependências, zero toolchain (sem Java), fácil de depurar por colegas do grupo.
- Quando reconsiderar: se o catálogo passar de ~300 padrões ou precisar de expressões aninhadas, adotar Lark SÓ como micro-gramática de condicionais de tempo (`entre <tempo> e <tempo>`, `há N dias atras`, `nos proximos N ...`) dentro do catálogo (arquitetura híbrida).

### Como o parser A funciona (resumo)

1. `lexer`: texto normalizado -> lista de `LogicalLine(text_raw, text_norm, indent, physical_lines=[n...], span)`. Remover comentário `#` com varredura ciente de strings (alternando aspas `"`/`'`; um `'` dentro de `"D'Água"` não abre string). Juntar linhas de continuação: (a) profundidade de parênteses > 0 no fim da linha; (b) primeira palavra da linha seguinte é `e` ou `ou` (nenhuma instrução legítima começa com essas palavras) - independente da indentação.
2. Nível estrutural (descida recursiva trivial): linha em coluna 0 com palavra-chave de bloco abre `Block`; linhas indentadas seguintes são instruções do bloco até o próximo cabeçalho em coluna 0.
3. Instruções por palavra-chave inicial: `do|da|na|no|nos|nas <fonte>(...)` (inclusive `e da carteira(...)` = outra fonte, interseção); temporal (`na segunda`, `nos dias uteis`, `na primeira semana`...); `quando <filtros>`; ações.
4. `quando`: laço "casar UM filtro do catálogo na posição atual (âncora `^`, ordem por especificidade, maior casamento primeiro) -> esperar `e` ou fim". NÃO dividir por ` e ` ingenuamente (colide com `entre 30 dias e 60 dias`, `maior que X e menor que Y`, `no minimo de 3 dias e no maximo de 21 dias`, `preferencia na segunda e na terca`).
5. Filtro sem casamento: consome até o próximo ` e ` cujo restante começa com um filtro conhecido (ressincronização), emite `UnknownClause(raw, span, nearest=[difflib.get_close_matches...])`.
6. Tudo que não é reconhecido como bloco (`alertas`, `tags` etc.) -> `UnknownBlock` com linhas cruas.

---

## 3. Questão 2: desenho da representação intermediária (IR)

### Dataclasses x Pydantic

Recomendação: `dataclasses` (`frozen=True, slots=True, kw_only=True`; `slots` e `kw_only` existem desde 3.10; `asdict()` é recursivo - doc Python 3.11).

- A IR é construída por código próprio e confiável: validação em tempo de execução não agrega; o que importa é imutabilidade, igualdade estrutural (testes golden) e serialização JSON simples.
- Pydantic 2.14.1 (MIT; Python 3.10+) é excelente na BORDA (carregar o JSON do pacote de contexto, validar saída estruturada do LLM, gerar JSON Schema) e tem uniões discriminadas (`Field(discriminator='kind')`). LangGraph aceita TypedDict, dataclass ou Pydantic como esquema de estado, e a documentação do LangGraph observa que "Pydantic é menos performático que TypedDict ou dataclass" (irrelevante nesta escala, mas confirma que não há ganho em usá-lo internamente).
- Regra INTERFACE-TAX: não criar hierarquia de classes com uma só implementação; `kind: str` + dict de parâmetros no caso genérico.

### Esboço

```python
@dataclass(frozen=True, slots=True, kw_only=True)
class Span:
    file: str
    lines: tuple[int, ...]        # linhas físicas (1-based), várias se houve continuação
    raw: str                      # texto original da cláusula (pré-normalização)

@dataclass(frozen=True, slots=True, kw_only=True)
class Atom:                       # um filtro "quando", já normalizado
    id: str                       # chave do catálogo, ex. "recencia", "ciclo_vida", "cidade_igual"
    params: Mapping[str, object]  # ex. {"kind": "positivacao", "scope": "grupo", "lo": 0, "hi": 60, "negated": False}
    span: Span

@dataclass(frozen=True, slots=True, kw_only=True)
class UnknownClause:
    span: Span
    nearest: tuple[str, ...] = () # ids do catálogo mais próximos (difflib)

@dataclass(frozen=True, slots=True, kw_only=True)
class Block:
    kind: Literal["time","carteira","segmentacao","parametros","limpar","unknown"]
    name: str                     # string original, sem normalizar
    exclusive: bool | None        # carteira vs carteira livre
    sources: tuple[Source, ...]   # do time(...), da carteira(...), e da segmentacao(...)
    temporal: tuple[Atom, ...]    # na segunda, nos dias uteis...
    filters: tuple[Atom | UnknownClause, ...]   # conjunção
    actions: tuple[Atom | UnknownClause, ...]   # frequencia, preferencia, nao agendar, fixo...
    index: int                    # posição no arquivo (ORDEM é semântica!)
    span: Span
```

Pontos de desenho:
- Filtros = lista plana (conjunção) porque não existe `OU` booleano no corpus; negação é atributo do átomo (`fora da recencia`, `nao tem venda`, `diferente(...)`), não um nó `Not`. Se surgir OR/NOT arbitrário, promover a `Expr` (And/Or/Not) - só então.
- Desconhecido: `UnknownClause` fica NA MESMA posição da lista, com `span.raw`; o pacote de contexto o repassa literalmente e o validador exige que a descrição o mencione como "condição não interpretada".
- Rastreabilidade: `Span` (arquivo, linhas físicas, texto cru) em todo nó; a descrição pode citar "linha 37" e o chunk RAG guarda o trecho `.gobr` exato.
- Nome do bloco é dado de primeira classe: texto livre do autor (guardar original; nunca normalizar o nome).
- Campos derivados da cascata (população efetiva etc.) NÃO ficam na IR sintática; vivem em `CascadeResult` separado (parse != semântica).

---

## 4. Questão 3: cascata / população efetiva

### 4.1 Semântica a modelar (manual)

- §7.6 (manual_utf8 linhas 1281-1282): "clientes parametrizados em uma regra anterior não são reprocessados por regras subsequentes. A ordem importa."
- §4.2/§4.7 (linhas 250-262, 461-482): carteira exclusiva remove seus clientes do pool das seguintes; `carteira livre` não remove; regras de carteira só adicionam; exclusão é indireta pela ordem.
- §7.3.4 (linha 1143): `nao agendar` é uma parametrização como outra (consome).
- §7.6 (linha 1278): `limpar parametros` é a única forma de "excluir"; efeito exato sobre o estado de consumo NÃO está especificado (tratar como corte de cascata + aviso).
- Filtros temporais (`na segunda`, `nos dias uteis`): bloco só executa naqueles dias; logo só consome clientes naquelas execuções.

Premissas semânticas a CONFIRMAR com o professor/autor (anotar como `SemanticsPolicy` configurável, com avisos no pacote de contexto):
1. `nao agendar` consome cliente (assumido sim; os PDFs dourados são coerentes com isso, ver ponto 9 da seção 1).
2. `recencia de positivacao em N dias` = recência no intervalo [0, N]; `entre a e b` = [a, b] (inclusive); `fora da recencia em N` = [N+1, inf). O cliente que NUNCA comprou (prospect) satisfaz `fora da recencia`? Indefinido na manual. Pista nos exemplos: V1Vidros põe "Inativos: fora da recencia em 45" ANTES de "Prospects: ciclo de vida prospect"; se prospects casassem em `fora da recencia`, o bloco Prospects seria código morto. Default sugerido: prospect NÃO casa; flag `never_bought_matches_outside_recency=False`; emitir aviso se o resultado depender disso.
3. Hierarquia de escopos de recência (inferida da manual §6.2): do vendedor >= do grupo (padrão) >= global (em dias desde o último evento; quanto mais amplo o escopo, mais recente o último evento). Logo `{recencia do vendedor <= N} subconjunto de {recencia do grupo <= N} subconjunto de {recencia global <= N}`. Na v1, só comparar recências de MESMO (tipo, escopo); entre escopos diferentes, tratar como independentes e dizer "pode haver sobreposição".
4. "N meses" em recência: converter 30 dias/mês e 7 dias/semana apenas com aviso (a manual só define 30 dias para `mensal()` de frequência).

### 4.2 Técnicas estudadas e o que aproveitar

- Firewall: política de regras com semântica "primeiro casamento" é exatamente o mesmo problema. Anomalias clássicas (Al-Shaer & Hamed): sombreamento (regra posterior nunca alcançada porque regras anteriores já casam todo o seu espaço), generalização, correlação (sobreposição parcial com ações diferentes) e redundância (remover a regra não muda o resultado). Detecção estática = comparação de conjuntos/intervalos por campo (ex.: arXiv 1102.1237, "Applying static code analysis to firewall policies", menciona MCSI - conjunto mínimo de intervalos). Aproveitar: nomenclatura e a detecção por caixas (hiper-retângulos) por campo.
- DMN, hit policy FIRST: sobreposições são permitidas e ganha a primeira regra; validadores (Sparx EA) verificam lacunas ("gap": nenhuma regra casa) e sobreposições (violação só sob UNIQUE); a especificação não exige tabela completa. Drools: epic DROOLS-3136 lista completude (sem lacunas), consistência, subsunção, "rule masking" e formas normais; a análise de tabelas de decisão do Drools reporta "Overlap detected: Overlap values: [<60, >=30] for rules [3, 1]" (aritmética de intervalos por coluna). O verificador clássico do Drools cobre redundância, subsunção, incoerência e lacunas.
- Enquadramento: cada bloco = uma "regra de tabela de decisão" cuja entrada é o conjunto de átomos; saída = ação; política = FIRST sobre a ordem do arquivo.
- Pesos pesados descartados (proporcionalidade): BDD, SMT (`z3-solver` 5.3.1.0, MIT, existe e funcionaria) - só valeria se aparecessem OR/NOT arbitrários e átomos acoplados; o corpus mostra conjunções de poucas dimensões.

### 4.3 Algoritmo recomendado (simples e exato para o caso dominante)

Modelo: cada bloco k vira uma CAIXA `B_k` = {dimensão -> restrição}, dimensões ausentes = livres.
- Dimensão `fonte`: conjunto de fontes (time/carteira/segmentação) com chave canônica (interseção quando há `e da carteira(...)`).
- Dimensão `recencia[(tipo, escopo)]`: conjunto de intervalos de inteiros (dias) fechados. `em N` = [0,N]; `entre a e b` = [a,b]; `fora ... em N` = [N+1, inf); `fora ... entre a e b` = [0,a-1] união [b+1, inf).
- Dimensão `nunca_comprou[escopo]` (prospect, `sem venda`, `ciclo de vida prospect`): booleano.
- Dimensão `frequencia_historica`: intervalo (mesma classe de intervalos).
- Átomos opacos (cidade, ramo, curva ABC, status receita, `data da rota na semana`...): chave `(id, params)`, com polaridade e pares complementares conhecidos (`adimplentes`/`inadimplentes`, `pessoa fisica`/`pessoa juridica`, `igual(X)`/`diferente(X)`, `cliente filial`/`cliente principal`, `contido`/`nao contido`). Átomos sem complemento conhecido ficam como `Not(atom)` simbólico.
- Filtro temporal: dimensão `quando_roda` (conjunto de dias/semanas/meses; sem filtro = sempre).

Operações (todas sobre caixas):
```
intersect(A, B): por dimensão, interseção; vazio se alguma dimensão fica vazia
subtract(A, B) -> list[Box]:     # A \ B como união de caixas DISJUNTAS
    if disjoint(A, B): return [A]
    out, rest = [], A
    for d in dims(B):
        outside = rest[d] - B[d]          # parte de A fora de B nesta dimensão
        if outside: out.append(rest | {d: outside})
        rest = rest | {d: rest[d] & B[d]}
    return out                            # o que sobra de 'rest' está dentro de B e é descartado
```
Cascata (por GRUPO DE FONTE: blocos com a mesma chave de fonte; fontes diferentes tratadas como independentes + aviso):
```
consumidos = []                          # caixas já parametrizadas
for bloco in ordem_do_arquivo:
    efetiva = [bloco.caixa]
    for c in consumidos:                 # só os que rodam em TODOS os dias do bloco
        efetiva = [r for e in efetiva for r in subtract(e, c)]
    resultado[bloco] = efetiva           # lista de caixas disjuntas
    if bloco consome: consumidos.append(bloco.caixa)
```
Para carteiras: igual, mas só carteiras exclusivas (`carteira` sem `livre`) entram em `consumidos`; `livre` não.

Saídas deterministas por bloco (entram no pacote de contexto):
- `own_condition` (o que o bloco diz literalmente) e `effective_condition` (após a cascata; estruturado: janelas, flags).
- `consumed_by_earlier`: nomes dos blocos anteriores que de fato reduziram a população.
- `shadowed: bool` (efetiva vazia = regra inalcançável, "sombreada"), `shadow_reason` (quais blocos).
- `overlaps_earlier` (interseção não vazia mas não total) - informativo.
- `is_fallback` (sem `quando` e último do grupo): efetiva = universo menos tudo que veio antes. Se a efetiva for descritível com 1-2 janelas (ex.: Infinitto: "recência > 90 dias"), entregar como `effective_condition`; senão, "todos os demais clientes".
- `gap_after_last` (aviso): união das caixas não cobre a fonte e não existe fallback -> "clientes fora destas condições não são parametrizados por este arquivo".
- `name_vs_code` (4.6).
- `global_exclusions`: átomos opacos de blocos `nao agendar` anteriores que valem para TODOS os blocos seguintes do grupo (ex.: baixados na Receita, inadimplentes, rota da semana). Para a prosa, listá-los UMA vez ("antes das regras abaixo, não são agendados: ...") em vez de repetir em cada bloco; o PDF Maxlub, porém, repete "somente clientes que não estão na rota da semana" em cada regra, então o texto por bloco pode citar a exclusão relevante quando o pacote marcar `repeat_exclusion_in_block=True` (decisão de estilo do agente de prompts).

Regra de renderização: se a efetiva é UMA caixa e só uma dimensão difere da condição própria -> prosa simples ("compraram nos últimos 90 dias, mas não nos últimos 60": janela [61,90]). Se há >3 caixas ou termos `Not` opacos -> não calcular texto; entregar condição própria + `exceto os já tratados por <nomes>`.

Complexidade: O(n^2) caixas por grupo, n <= 75 no corpus; trivial.

### 4.4 Aritmética de intervalos: classe própria x biblioteca

- `portion` 2.6.3 (LGPL-3.0-or-later; Python >=3.10) existe e tem união/diferença/complemento, mas o suporte a intervalos DISCRETOS (inteiros contíguos) é uma subclasse marcada experimental; como dias são inteiros, `[0,60]` e `[61,90]` deveriam fundir. Recomenda-se uma classe `IntervalSet` própria (~40 linhas: tuplas ordenadas `(lo, hi)` fechadas, `INF = 10**9`, métodos `&`, `|`, `-`, `complement`, `is_empty`, `__contains__`), pois evita LGPL, dependência e a armadilha aberto/fechado.

### 4.5 Exemplos de teste da cascata (já definidos pelo corpus)

| Arquivo | Blocos (ordem do arquivo) | Efetivo esperado |
|---|---|---|
| Maxlub | `nao agendar` x3 (baixados, inadimplentes, `data da rota na semana`); prospects; ativos `em 60`; risco `em 90`; inativos 90 `em 120`; 120 `em 150`; 150 `em 180`; fallback `nao agendar` | os 3 primeiros consomem; ativos [0,60]; risco [61,90]; inativos(90) [91,120]; (120) [121,150]; (150) [151,180]; todos "exceto rota da semana, inadimplentes, baixados" (bate com o PDF); fallback = demais (>180, não prospects) |
| Infinitto | baixados; prospects; ativo `global em 60`; risco `em 90` (recência do GRUPO, não global); inativo sem `quando` | ativo usa escopo GLOBAL e risco usa escopo do GRUPO -> escopos diferentes; v1 não subtrai entre escopos; avisar. Inativo = demais (>90) |
| V1Vidros | baixados; ativos `em 30`; risco `em 45 e fora em 30`; inativos `fora em 45`; prospects | ativos [0,30]; risco [31,45]; inativos [46,inf); prospects: sombreado SE `fora da recencia` incluir nunca-compraram (ver premissa 2) |
| regra_169 | (fonte segmentação+carteira) prospects; `global em 30`; `global em 60`; `global em 90`; `global entre 90 e 180` | efetivo: [0,30], [31,60], [61,90], [91,180] (o bloco `entre 90 e 180` sobrepõe o dia 90 com o anterior; interseção fechada resolve); o nome do 1o ("entre 7d e 30d") não bate com [0,30] -> aviso `name_vs_code` |

Observação: em Infinitto, o bloco "Inativo" sem `quando` vem depois de prospects; o PDF dourado diz "Clientes sem pedidos a mais 90 dias" - o efetivo calculado ([91,inf) menos prospects) reproduz o texto humano.

### 4.6 Lint nome x código (muito barato, muito valioso)

Extrair números de dias de cada nome de bloco (`\d+\s*d(ias)?`, `entre 60 e 90d`) e comparar com as janelas efetivas/literais. Divergência vira aviso no pacote (`name_conflicts=[...]`) e o validador exige que a descrição descreva o EFETIVO e, se o nome divergir, diga isso. Evita a descrição "repetir o nome enganoso".

---

## 5. Questão 4: normalização

### 5.1 Codificação

Estratégia determinística, sem detector:
1. Ler bytes; remover BOM UTF-8 (`utf-8-sig`).
2. `bytes.decode("utf-8")` estrito. UTF-8 tem estrutura rígida: texto latin-1/cp1252 com acentos quase nunca é UTF-8 válido, então o teste é um detector eficiente para este caso.
3. Se falhar: `decode("cp1252")` estrito (superconjunto do ISO-8859-1 nos caracteres imprimíveis; 5 bytes indefinidos 0x81, 0x8D, 0x8F, 0x90, 0x9D lançam erro).
4. Se falhar: `latin-1` (nunca falha) + aviso. Registrar `encoding_used` nos metadados.
5. Opcional: se o texto contém `Ã£`, `Ã§`, `Ã©`, `â€` (mojibake: UTF-8 lido como cp1252), tentar `s.encode("cp1252").decode("utf-8")`; fazer só quando todos os caracteres são re-codificáveis. A busca no corpus por esses padrões não encontrou ocorrências.

Detectores verificados (não recomendados aqui): `charset-normalizer` 3.5.2 (MIT, >=3.7) e `chardet` 7.7.0 (0BSD, >=3.10). A documentação de benchmark do próprio chardet reporta precisão ~98-99% (chardet) vs ~85% (charset-normalizer) no conjunto dele (fonte do fornecedor) e deixa claro que a distinção latin-1 vs cp1252 é "superconjunto", ou seja, um detector não traz ganho sobre a cascata acima; textos curtos não foram medidos. Para ~246 arquivos conhecidos, a cascata é mais simples e reprodutível. `Unidecode` 1.4.0 existe mas é GPL: usar `unicodedata` da stdlib.

Limitação desta pesquisa: a busca por bytes não-UTF-8 com `Grep` não achou nenhum arquivo em latin-1/cp1252 em `referencias\`, o que contradiz o relato do enunciado; pode ser limitação da ferramenta de busca. A auditoria de codificação (decodificar os 246 arquivos e contar por codec) deve ser o primeiro teste da implementação.

### 5.2 Acentos e ortografia de palavras-chave

- `fold(texto) = casefold(NFKD(texto) sem marcas combinantes)`, aplicado somente FORA de literais entre aspas (nomes, listas de cidades/ramos). Procedimento: substituir cada literal `"..."`/`'...'` por marcador `\x00N\x00`, normalizar o resto, restaurar depois. Nomes de blocos e valores de lista permanecem EXATOS (o LLM e o validador precisam do original).
- Também normalizar: NBSP (U+00A0) e demais espaços Unicode -> espaço; múltiplos espaços -> um; aspas tipográficas “ ” -> `"`; hífens Unicode; `\r\n`/`\r` -> `\n`; tabs só importam para o nível estrutural (que ignora quantidade de indentação).
- Armadilha do `é`: `quando é o cliente filial` e `id do cliente principal é diferente(...)` usam o verbo ser. Após remover acento vira `e`, idêntico ao conectivo. Solução: no catálogo, tratar `(e|é)\s+` opcional (cópula) dentro dos padrões dessas cláusulas; e a regra do laço de `quando`: um `e` na PRIMEIRA posição após `quando` não é conectivo. Alternativa: antes do fold, trocar o token isolado `é` por um marcador `<COP>` que o catálogo ignora.
- Sinônimos de ortografia: aplicar equivalências APÓS o fold (`positivacao`/`positivação` já resolvido; `terca`/`terça`; `sabado`/`sábado`; `semana`/`semanas`; `dia`/`dias`; `quinta-feira`/`quinta`) direto na regex do catálogo (`dias?`, `terca`, etc.).
- Números: `R$ 10000`, `R$0,00`, `3.5`, `100,00` -> parser de número pt-BR com decimal por vírgula; datas `'dd-mm-yyyy'` e `'yyyy-mm-dd'` -> `datetime.date`.
- Palavras desconhecidas "parecidas" com palavras do catálogo (typos): `difflib.get_close_matches` (stdlib) só para SUGERIR no relatório; nunca corrigir automaticamente (`rapidfuzz` 3.14.6, MIT, existe mas é desnecessário).

### 5.3 Continuação de linha

Ver 2 (passos 1 e 4). Regras resumidas: (a) parênteses abertos continuam; (b) linha cuja primeira palavra é `e`/`ou` continua a instrução anterior; (c) fim de linha com vírgula dentro de lista continua (já coberto por (a)); (d) comentários removidos ANTES de juntar linhas; (e) guardar `physical_lines` para spans.
Caso especial: `e da carteira(...)` logo após `da segmentacao(...)` é continuação de FONTE (não de `quando`): decidir pelo contexto (instrução anterior era fonte).

---

## 6. Questão 5: validador determinístico da prosa gerada

### 6.1 Verificações (todas sem LLM)

Entrada: pacote de contexto (fatos) + texto gerado (preferencialmente JSON `{"resumo": "...", "blocos": [{"id": 3, "texto": "..."}]}`, contrato a combinar com o agente de prompts; permite verificar POR BLOCO).

1. Cobertura de nomes: cada nome de bloco `time/carteira/segmentacao/parametros` aparece verbatim (comparação acento/caixa-insensível). Para nomes muito longos, exigir o nome ou um prefixo >= 60%.
2. Cobertura de números: todo número relevante do bloco (limiares, N dias, frequências, janelas efetivas) aparece (dígitos, normalizando `1.000`/`1000`, `7 dias`/`7d`). Listas longas (cidades/ramos): exigir a CONTAGEM e/ou os K primeiros itens, não todos (senão força o LLM a copiar listas de 40 cidades).
3. Alucinação numérica: todo número no texto pertence a `numeros_permitidos` = números da IR + números derivados determinísticos pelo pacote (ex.: 61 e 91 das janelas efetivas, índices/ordinais 1..n, contagens) + anos/datas de metadados. Número fora do conjunto = falha. Mesmo para identificadores (IDs de vendedor, códigos de ramo) citados.
4. Ordem: a primeira menção dos blocos segue a ordem do arquivo (a cascata depende da ordem); permitir agrupamento explícito só quando o pacote marcar o grupo.
5. Léxico por tipo de ação: bloco `nao agendar` -> texto do bloco contém um de {"não agendar", "não será agendado", "não agenda", ...}; bloco com `frequencia` não contém "não agendar" (e vice-versa); `fixo` -> "fixa|fixo"; `roteirizavel` -> "roteiriz". Tabelas pequenas, versionadas.
6. Cascata: bloco com `consumed_by_earlier` não vazio deve conter marcador de exclusão ("exceto", "que não", "demais"); bloco `is_fallback` contém "demais|restantes|todos os outros"; bloco `shadowed` contém "nunca|inalcançável|não terá efeito".
7. Aviso obrigatório: cada `UnknownClause` e cada `name_conflicts`/`warnings` do pacote precisa aparecer sinalizado.
8. Higiene: idioma pt-BR (heurística de stopwords), tamanho mínimo/máximo, ausência de marcação (markdown/JSON vazado), sem citar valores inexistentes (ex.: "R$" quando nenhum valor monetário).

### 6.2 Métricas estabelecidas, baratas e determinísticas

- Slot Error Rate (SER = (p + q) / N: p slots faltantes, q slots redundantes, N slots da entrada), usada em NLG data-to-text desde Wen et al. 2015 e adotada no E2E NLG Challenge (variantes contam substituições, repetições e alucinações; pode passar de 1). É o análogo direto das verificações 2-3: slots = {nomes, números, ações}. Implementar como `ser = (faltantes + extras) / total_slots` por arquivo e por bloco; critério de aceite sugerido: `ser == 0` nos números e nomes, tolerância configurável nos itens opcionais.
- Dušek, Howcroft & Rieser (2019): omissão é o erro mais comum em NLG neural, mais que alucinação -> priorizar a verificação de cobertura.
- PARENT (Dhingra et al., 2019) exige textos de referência e tabela; só teria uso nos 3 exemplos dourados; BLEU/ROUGE não medem fidelidade -> não usar como aceite.
- Wiseman et al. (2017) propõem métricas extrativas (extrair fatos do texto e comparar com os dados), mas com modelo de IE treinado -> pesado. A versão barata aqui é regex de números/nomes.
- Dušek & Kasner (2020) usam NLI nos dois sentidos (dados->texto e texto->dados) para detectar omissão e alucinação; exige modelo NLI (não determinístico, custo): deixar como camada OPCIONAL posterior, não como validador principal.

### 6.3 Política de falha e fallback

1. Reprovou: reenviar ao LLM com a LISTA de violações (máx. 2 tentativas).
2. Persistindo: usar o renderizador determinístico `render.py` (templates por tipo de bloco e de filtro) como descrição de fallback, marcada `source: "template"`. O mesmo renderizador serve de referência para testes e permite medir o LLM (comparar fatos).
3. Todo resultado guarda `validation_report` (violações, SER) junto do chunk.

---

## 7. Questão 6: estratégia de testes

Ferramentas (versões verificadas): `pytest` 9.1.1 (MIT, >=3.10), `syrupy` 6.1.1 (MIT, >=3.10; snapshot como plugin do pytest), `hypothesis` 6.170.5 (MPL-2.0, >=3.11; opcional). Alternativa sem dependência: arquivos JSON golden + flag `--update-golden`.

1. Golden (3 exemplos): para cada `.gobr` em `exemplos\`, arquivo esperado escrito À MÃO com (a) IR essencial (blocos, ações, janelas), (b) tabela de cascata (4.5), (c) fatos transcritos dos PDFs (ex.: Maxlub: frequências 14/14/7/14/21/28 dias na ordem do arquivo [prospects, ativos, risco, inativos 90/120/150], 3 `nao agendar` explícitos + fallback final `nao agendar`, e a exclusão "rota da semana" derivada da cascata, não escrita em cada bloco).
2. Teste do validador com texto humano: transcrever a descrição dos PDFs para texto corrido e verificar que PASSA no validador de cobertura; depois aplicar MUTAÇÕES (trocar um número, remover um bloco, trocar a ordem, inventar valor) e verificar que FALHA. Barato e prova que o validador discrimina.
3. Snapshot (syrupy) do pacote de contexto dos 246 arquivos: qualquer mudança no parser/cascata aparece como diff revisável. Manter snapshots em arquivos separados por regra para diff legível.
4. Relatório de cobertura de cláusulas (script `tools/coverage_report.py`, saída em `research/` ou `out/`): para cada linha de filtro/ação, indica `reconhecida` ou `UnknownClause`; templateiza (`\d+` -> `N`, strings -> `S`, listas -> `L`) para contar padrões distintos; mostra top-N desconhecidos por frequência e por arquivo; métricas: % de linhas reconhecidas, # padrões distintos, # arquivos com 100% de cobertura. Meta de trabalho: >= 98% das linhas; cauda restante tratada como `UnknownClause` e descrita literalmente.
5. Metamórficos: aplicar transformações que NÃO devem mudar a IR (remover acentos de palavras-chave; CRLF; trocar espaços por tabs; adicionar BOM; reindentar; reflowar listas multi-linha) e comparar IR antes/depois (ignorando spans). Pega fragilidades de normalização.
6. Smoke de corpus: todos os 246 arquivos parseiam sem exceção; nenhum bloco perdido (contar cabeçalhos em coluna 0 por regex independente e comparar com `len(blocks)`).
7. Propriedade (opcional, só com `hypothesis`): impressora canônica `render_gobr(ir)` e `parse(render(ir)) == ir`. Só vale se a impressora for útil depois; caso contrário, pular.
8. Cascata: tabelas parametrizadas `(lista de filtros em ordem) -> janelas efetivas esperadas` + casos de sombreamento, lacuna, fallback, `livre` vs exclusiva.

---

## 8. Questão 7: chunking e metadados para o RAG (resumo)

Objetivo no sistema final: dado um pedido de negócio, recuperar regras existentes parecidas (e trechos GOBR) como exemplos.

Recomendação: ambos os níveis, padrão "pequeno para achar, grande para dar contexto" (cf. `ParentDocumentRetriever` do LangChain: embeddings de chunks pequenos, retorno do documento pai).
- Chunk de arquivo (pai): resumo geral + cabeçalho (cliente, data, origem) + lista de blocos.
- Chunk de bloco (filho): descrição do bloco (com condição EFETIVA) + nome + ação; guardar o trecho `.gobr` exato no payload (opcionalmente indexar também o texto GOBR normalizado/BM25 para casar idioma de cláusulas).
- Texto a embutir: descrição em prosa + tokens normalizados de cláusulas (ids do catálogo) em uma linha de prefixo; não embutir listas longas de cidades/códigos.

Metadados úteis (todos determinísticos): `file_id`, `source_path`, `encoding_used`, `content_hash`, `structure_hash` (IR sem nomes/números, para achar quase-duplicatas), `duplicate_of`, `block_index`, `block_kind`, `block_name`, `exclusive`, `team_scope` (times/carteiras citados), `actions` (set: frequencia, nao_agendar, fixo, roteirizavel, preferencia, sem_choque, restrito), `frequency_days` (valor), `clause_ids` (filtros usados: recencia, ciclo_vida, ramo, cidade, rota, inadimplencia...), `recency_windows` (efetivas), `has_fallback`, `has_carteira`, `has_segmentacao`, `n_blocks`, `n_unknown_clauses`, `warnings`, `header_comments` (cliente/data/solicitação), `description_source` (`llm`|`template`), `validation_ser`, `pipeline_version`, `span_lines`.
Observação: o corpus é muito repetitivo (dezenas de arquivos "Regra Padrão"); deduplicar/agrupar por `structure_hash` evita que o top-k do retriever seja preenchido por cópias.

---

## 9. Layout de módulos recomendado e ordem de implementação

```
Projeto_SMA/
  src/gobr_pre/
    textio.py        # read_text_robust(path) -> SourceText(encoding_used, text, warnings)
    lexer.py         # strip comentários (ciente de strings), linhas lógicas, continuação, Span
    fold.py          # mascarar literais, NFKD+casefold, números pt-BR, datas
    catalogue.py     # DADOS: tabelas (id, regex, builder) de fontes, temporais, filtros, ações
    ir.py            # dataclasses: Span, Atom, UnknownClause, Block, GobrFile
    parser.py        # estrutura (blocos) + laço de 'quando' + recuperação (UnknownClause)
    intervals.py     # IntervalSet de inteiros (fechado), INF
    cascade.py       # caixas, subtract, cascata por grupo de fonte, sombreamento/lacuna/fallback, lint nome x código
    context.py       # monta pacote de contexto (JSON): fatos, numeros_permitidos, avisos
    render.py        # renderizador determinístico (templates) = fallback e referência
    validate.py      # cobertura, alucinação numérica, ordem, léxico, SER
    chunks.py        # emite JSONL de chunks + metadados (seção 8)
    cli.py           # python -m gobr_pre <dir_in> <dir_out>
  tools/coverage_report.py
  tests/
    golden/          # esperados escritos à mão (3 exemplos)
    test_lexer.py test_parser.py test_cascade.py test_validate.py test_metamorphic.py test_corpus_smoke.py
  research/camada_deterministica.md
```
SCALE-FIT: sem Docker, banco, cache ou fila - é um batch offline de 246 arquivos; JSON/JSONL em disco bastam. `catalogue.py` é DADOS (lista de tuplas), não hierarquia de classes (INTERFACE-TAX).

Ordem de implementação (cada passo termina com um teste verde):
1. `textio` + auditoria de codificação do corpus (relatório: codec por arquivo).
2. `lexer` + teste de smoke: 246 arquivos -> blocos contados por regex independente.
3. `fold` + `catalogue` v0 a partir das tabelas da manual (§3, §4.6, §5, §6, §7) + `parser` + `coverage_report`; iterar o catálogo até >= 98% de linhas reconhecidas.
4. `ir` fechado + golden dos 3 exemplos.
5. `intervals` + `cascade` (só recência do mesmo tipo/escopo, ciclo de vida/prospect, opacos com complemento) + tabela 4.5 + lint nome x código.
6. `context` (pacote JSON) + snapshot dos 246.
7. `render` (templates) + `validate` + testes de mutação com os PDFs transcritos.
8. `chunks` (JSONL) + deduplicação por `structure_hash`.
9. Refinos opcionais: hierarquia de escopos de recência (vendedor/grupo/global), filtros temporais parciais, `limpar parametros`, carteiras com `ruptura(...)`.

---

## 10. Becos sem saída, riscos e pontos não verificados

- Nenhum .g4/repositório público de GoBR/Govendas encontrado (busca web); "gorules" no mercado refere-se a outro produto (GoRules ZEN), sem relação.
- Estatísticas do corpus por amostragem de `Grep`, não por execução de código; a codificação não-UTF-8 relatada não foi reproduzida.
- Semântica de `fora da recencia` para clientes sem compra, efeito de `limpar parametros` sobre a cascata e hierarquia exata dos escopos de recência vêm de inferência da manual/exemplos: tratar como premissas configuráveis e perguntar ao autor da manual.
- Benchmarks citados de Lark/pyparsing (python-parsing-benchmarks) e ANTLR (AntlrBenchmarks) são de terceiros, obtidos via resumo de busca (fonte primária não reaberta); servem só para ordem de grandeza.
- Slot Error Rate: a fórmula vem de artigos posteriores que a citam (E2E NLG Challenge, arXiv 1901.07931 e 1903.08097); a página do artigo de Wen et al. (1508.01745) consultada não menciona SER no resumo.
- As referências a Al-Shaer & Hamed vêm de fontes secundárias (a nomenclatura de anomalias é padrão; definições formais não foram lidas na fonte primária; o PDF arXiv 1102.1237 não pôde ser lido como texto).
- Drools: detalhes vêm de issues JIRA (DROOLS-3136, DROOLS-4338), não de documentação oficial atual.
- `ftfy` (mojibake) não pôde ser verificado no PyPI e por isso NÃO é recomendado.
- `portion` descartado por: LGPL, intervalos discretos experimentais. `Unidecode` descartado por GPL. Detectores de charset descartados por não agregarem sobre a cascata UTF-8 -> cp1252 -> latin-1. ANTLR e pyparsing descartados por esforço/robustez (seção 2).
- Sugestão (não executada): copiar `manual_utf8.txt` (hoje em `AppData\Local\Temp\sma_ctx`) para dentro do projeto, pois pasta temporária pode ser limpa.

---

## 11. Fontes

Pacotes (PyPI, consultados em 2026-10-20):
- lark 1.3.1 (MIT, >=3.8, 2025-10-27): https://pypi.org/project/lark/
- pyparsing 3.3.3 (MIT, >=3.9, 2026-09-20): https://pypi.org/project/pyparsing/
- antlr4-python3-runtime 4.13.2 (BSD, 2024-08-03): https://pypi.org/project/antlr4-python3-runtime/
- charset-normalizer 3.5.2 (MIT, >=3.7): https://pypi.org/project/charset-normalizer/
- chardet 7.7.0 (0BSD, >=3.10, 2026-10-18): https://pypi.org/project/chardet/
- Unidecode 1.4.0 (GPL, >=3.7): https://pypi.org/project/Unidecode/
- pydantic 2.14.1 (MIT, 3.10+, 2026-10-11): https://pypi.org/project/pydantic/ e licença https://github.com/pydantic/pydantic/blob/main/LICENSE
- portion 2.6.3 (LGPL-3.0-or-later, >=3.10): https://pypi.org/project/portion/ ; https://github.com/AlexandreDecan/portion
- syrupy 6.1.1 (MIT, >=3.10): https://pypi.org/project/syrupy/
- hypothesis 6.170.5 (MPL-2.0, >=3.11): https://pypi.org/project/hypothesis/
- pytest 9.1.1 (MIT, >=3.10): https://pypi.org/project/pytest/
- rapidfuzz 3.14.6 (MIT, >=3.11): https://pypi.org/project/rapidfuzz/
- z3-solver 5.3.1.0 (MIT): https://pypi.org/project/z3-solver/

Documentação:
- Lark, parsers (Earley/LALR/CYK): https://lark-parser.readthedocs.io/en/latest/parsers.html
- Lark, classes (UnexpectedInput, on_error, propagate_positions): https://lark-parser.readthedocs.io/en/latest/classes.html
- Lark, exemplo de indentação (Indenter, %declare _INDENT/_DEDENT): https://lark-parser.readthedocs.io/en/latest/examples/indented_tree.html
- Lark, gramática: https://lark-parser.readthedocs.io/en/latest/grammar.html
- pyparsing HowTo (IndentedBlock, ParseException, packrat): https://pyparsing-docs.readthedocs.io/en/latest/HowToUsePyparsing.html
- ANTLR4, alvo Python: https://github.com/antlr/antlr4/blob/master/doc/python-target.md ; getting started: https://github.com/antlr/antlr4/blob/master/doc/getting-started.md
- Benchmarks de parsers Python: https://github.com/goodmami/python-parsing-benchmarks ; ANTLR por linguagem: https://github.com/KvanTTT/AntlrBenchmarks
- Gherkin (linha a linha, palavras-chave localizadas): https://cucumber.io/docs/gherkin/reference/
- Python 3.11 dataclasses: https://docs.python.org/3.11/library/dataclasses.html
- Pydantic, uniões discriminadas: https://pydantic.dev/docs/validation/latest/concepts/unions/
- LangGraph, esquema de estado: https://docs.langchain.com/oss/python/langgraph/graph-api
- Windows-1252 (bytes indefinidos): https://en.wikipedia.org/wiki/Windows-1252
- chardet, desempenho/FAQ: https://chardet.readthedocs.io/en/latest/performance.html e https://chardet.readthedocs.io/en/latest/faq.html
- LangChain ParentDocumentRetriever: https://python.langchain.com/docs/how_to/parent_document_retriever

Cascata / análise de regras:
- Anomalias de firewall (sombreamento, generalização, correlação, redundância): https://arxiv.org/pdf/1102.1237 ; resumo secundário: https://springerplus.springeropen.com/articles/10.1186/s40064-016-2489-6
- DMN, hit policy FIRST, gaps/overlaps (Sparx EA): https://sparxsystems.com/enterprise_architect_user_guide/16.0/dmn_decisiontable_validation.htm
- Drools DMN decision table analysis: https://lists.jboss.org/pipermail/jboss-jira/2019-July/365369.html (DROOLS-4338) ; epic https://issues.jboss.org/browse/DROOLS-3136
- Drools verifier (redundância, subsunção, incoerência, lacunas): https://docs.jboss.org/drools/release/6.0.0.CR3/drools-guvnor-docs/html/ch06.html

Validação data-to-text:
- PARENT, Dhingra et al. 2019: https://arxiv.org/abs/1906.01081
- Semantic Noise Matters for Neural NLG, Dušek et al. 2019: https://arxiv.org/abs/1911.03905
- Challenges in Data-to-Document Generation, Wiseman et al. 2017: https://arxiv.org/abs/1707.08052
- Evaluating Semantic Accuracy of D2T with NLI, Dušek & Kasner 2020: https://arxiv.org/abs/2011.10819
- Slot Error Rate (Wen et al. 2015, artigo: https://arxiv.org/abs/1508.01745 ; uso/definição citados em https://arxiv.org/pdf/1901.07931 e https://arxiv.org/pdf/1903.08097)

Material do projeto:
- Manual: `...\trabalho\trabalho\govendas-rules.pdf` (dump: `C:\Users\Pedro\AppData\Local\Temp\sma_ctx\manual_utf8.txt`, linhas citadas nas seções 1 e 4).
- Exemplos: `...\trabalho\trabalho\exemplos\` (RegraMaxlub, RegraInfinittoDesign, V1Vidros-RegraComercial).
- Corpus: `...\trabalho\trabalho\referencias\regra_001..246.gobr` (arquivos citados: 023, 032, 049, 101, 128, 130, 135, 139, 140, 154, 168, 169, 182, 190, 201, 209, 221, 231).

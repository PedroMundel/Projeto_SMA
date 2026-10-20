# Etapa REDATOR (LLM): boas práticas e técnicas eficientes

Pesquisa de 2026-10-20. Escopo: etapa que transforma o pacote JSON (já analisado pela camada determinística) em descrição comercial em pt-BR para cada `.gobr`, com foco em fidelidade, recuperação (RAG) e portabilidade para Ollama.

Convenções: **(inferência)** = conclusão minha, sem fonte direta. **(não verificado)** = não consegui confirmar na fonte primária. Nomes de modelos/bibliotecas citados foram conferidos nas páginas oficiais (PyPI, Hugging Face, Ollama, docs Anthropic) na data acima.

Rejeitados: não existe `CLAUDE.md` de projeto em `Projeto_SMA/` (nem seção `## Rejected`), então nenhum candidato foi descartado por NO-REJECTED.

---

## 0. Achados sobre os exemplos-ouro (mudam o desenho)

Li `exemplos/` (3 PDFs + 3 `.gobr`) e alguns de `referencias/` (`regra_001`, `050`, `150`, `230`) e §7.6 do manual.

1. **Os PDFs-ouro não são função pura do `.gobr`.** Há informação nos PDFs que não está no `.gobr` (Maxlub: "Capacidade de atendimento: 35 clientes (Dia)"; V1Vidros: "Agendar Inadimplentes: clientes inadimplentes autorizados") e informação no `.gobr` que não está no PDF (Maxlub: bloqueio "baixados na receita"). Consequência: o redator nunca deve ser avaliado por similaridade textual com o ouro como se fosse gabarito; ver plano de avaliação (§9). Para few-shot, usar versões **adaptadas** do ouro (só conteúdo derivável do pacote).
2. **A cascata já aparece, em linguagem comercial, no ouro.** Maxlub "Risco de Inatividade" (`recencia ... 90` depois de `... 60`) vira "compraram nos últimos 90 mas estão a 60 dias sem comprar"; V1Vidros usa `e fora da recencia ... em 30 dias` e o ouro escreve igual; Infinitto "Risco" vira "entre 60 e 90 dias". O manual confirma a semântica: "Sem repetição: clientes parametrizados em uma regra anterior não são reprocessados por regras subsequentes. A ordem importa" (manual §7.6, linha 1281 do `manual_utf8.txt`).
3. **Regra sem `quando`** (Infinitto "Inativo", `regra_150` "Cliente inativo - Resgate") é *catch-all*: vale para quem sobrou. O ouro Infinitto escreve "Clientes sem pedidos a mais 90 dias". A camada determinística precisa entregar o texto do "restante" já calculado; o redator não deve deduzir. (Ponto em aberto para o agente determinístico: como a engine trata prospects numa regra do tipo "fora da recência" posicionada antes da regra de prospects, caso V1Vidros.)
4. **Observação herdada de bloqueios.** O ouro Maxlub repete "Somente clientes que não estão na rota da semana" em cada linha porque o bloqueio vem antes. Decisão de estilo aberta (Pedro): (a) repetir por linha como no ouro, ou (b) listar bloqueios globais uma vez no resumo + linha própria, e reservar `observacao` para filtros extras da regra (ex.: `e frequencia historica menor que 16 dias` em `regra_230`). Recomendo (b) por gerar chunks de regra mais limpos para o retrieval; (a) fica mais fiel ao ouro. Fica como parâmetro do pacote (`restricoes_herdadas`) e do prompt.
5. **Os 3 ouros são todos "parametros do time televendas".** O corpus também tem tipo `carteira` + "Regra Padrão do goVendas/Duferro Customizável" (`regra_001`, `regra_050`: `quando inativos para o vendedor`, `frequencia de inativos da empresa`, `sem venda`, `adimplentes`), com cláusulas que não aparecem nos ouros. Cobertura de few-shot precisa de pelo menos um exemplo desse tipo, escrito/aprovado à mão.
6. O manual tem cláusulas que o ouro nunca exercita (`frequencia semanal()`, `frequencia do vendedor`, `preferencia na segunda e na terça`, `inatividade de 90 dias`). Isso justifica o campo `clausulas_desconhecidas` e o glossário inline por cláusula.
7. Comentários do `.gobr` podem conter URLs de Basecamp (`regra_150`, `regra_230`). Remover no pacote: ruído e risco de vazar para os embeddings.
8. Nomes de regra carregam empresa/boilerplate ("Regra Padrao da Duferro Customizavel: ..."). Isso é exigido pelo validador (nome literal), mas **não deve** entrar no texto embutido (§3).

---

## 1. Prompting para fidelidade (dados estruturados para prosa)

### 1.1 O que a literatura/documentação sustenta

| Técnica | Evidência | Aplicação aqui |
|---|---|---|
| Dados longos no topo, instruções/exemplos depois; separar com tags XML | Doc Anthropic, "Long context prompting" e "Structure prompts with XML tags" (https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) | Pacote em `<pacote>` primeiro, lembrete curto da tarefa no fim. |
| 3-5 exemplos, relevantes, diversos, em `<example>` | Mesma doc ("Use examples effectively") | Few-shot fixo de 3-4 (§1.3). |
| Permitir "não sei" reduz alucinação | https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations | Campo `clausulas_nao_traduzidas` + marcador `[não traduzido: ...]`. |
| Restringir a conhecimento externo, e "citar" a fonte de cada afirmação; remover afirmação sem suporte | Mesma doc (quotes, citations, external knowledge restriction) | Cada linha ecoa `id` da regra do pacote; sem `id` = descartada. |
| Chain-of-Verification (rascunho, perguntas de checagem, resposta revisada) | Dhuliawala et al., arXiv 2309.11495 (https://arxiv.org/abs/2309.11495) | Não usar para o redator: o verificador determinístico já cumpre esse papel mais barato. |
| Seleção de exemplos por similaridade supera aleatória, inclusive em table-to-text (ToTTo +41,9% relatado) | Liu et al., KATE, arXiv 2101.06804 (https://arxiv.org/abs/2101.06804) | Fase 2 opcional para modelo local (§1.3). |
| Em data-to-text (GEM'24, RDF para texto), um sistema few-shot com *retriever simbólico* de exemplos ficou em 1º lugar nos 4 critérios humanos (No-Omissions, No-Additions, Grammaticality, Fluency) | Jobanputra & Demberg, INLG 2024 (TeamSaarLST) e follow-up 2025 "Symbolic retrieval substantially reduces hallucination in data-to-text generation"; as páginas ACL não abriram para mim, o resultado vem do resumo de busca (não verificado no texto): https://aclanthology.org/2025.inlg-genchal.4 | Apoia: escolher exemplos por *estrutura* (propriedades em comum) e adotar os 4 critérios como rubrica (§4). |

### 1.2 Como apresentar o pacote (ordem, glossário, cascata)

Princípio (inferência, coerente com as fontes acima): **mover todo raciocínio para fora do LLM.** O redator só realiza texto; qualquer coisa que exija "pensar" (cascata, exclusões) já vem pronta.

- **Ordem do JSON = ordem do arquivo** (a ordem é semântica). Cada regra com `posicao`.
- **Por regra, nesta ordem de campos:** `id`, `nome` (literal), `condicao_efetiva` (texto pt-BR determinístico, já com cascata), `acao`, `numeros` (lista que o texto deve conter), `filtros_brutos` (gorules literal, só para referência), `glossario` (uma frase do manual **por cláusula usada naquela regra**, não um glossário global), `clausulas_desconhecidas`, `restricoes_herdadas`.
- **Cascata explícita em duas camadas:** `filtros_brutos` (o que está escrito) e `condicao_efetiva` (o que realmente vale). Instruir: "escreva o critério a partir de `condicao_efetiva`".
- **Glossário inline curto** (1 frase) em vez de despejar o manual (o manual tem ~57 páginas); só o necessário por cláusula.
- **Numeração:** o validador compara dígitos; instruir "números sempre em algarismos".
- **Sem raciocínio livre dentro do JSON de saída** (ver §2). Para Claude, se usar a API (não é o caso dos subagentes), a doc do Sonnet 5.5 diz que respostas JSON para tarefas de múltiplos passos de raciocínio podem errar quando o modelo não pensa antes (https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5). Como a cascata vem pronta, esse risco é pequeno aqui.

### 1.3 Few-shot: fixo vs. dinâmico

- **Fase 1 (agora, Sonnet): fixo e congelado, 3-4 exemplos** no próprio arquivo do subagente: (1) Maxlub adaptado (cascata longa + bloqueios), (2) Infinitto adaptado (catch-all "Inativo"), (3) V1Vidros adaptado (`fora da recencia`), (4) **um exemplo escrito à mão do tipo carteira + "regra padrão"** (`regra_050`). Motivo: Anthropic recomenda 3-5 diversos; Sonnet com instruções explícitas dispensa seleção dinâmica; congelar é o que garante estilo consistente entre agentes paralelos (§5).
- **Fase 2 (opcional, modelo local):** exemplos dinâmicos escolhidos por **assinatura estrutural** (mesmo conjunto de tipos de cláusula, mesmo nº de regras, presença de catch-all) usando só saídas já validadas. Justificativa: KATE + resultado GEM'24 sugerem ganho maior em modelos menores; só entra se o experimento (§9) mostrar erro de estilo.
- Não usar saídas do Sonnet ainda não validadas como exemplo (propaga erro).

### 1.4 Restrições de saída e anti-alucinação (lista usada no prompt de §7)

1. Usar somente o pacote; proibido conhecimento externo e **proibido explicar finalidade/benefício** que não esteja no pacote.
2. Números só copiados do pacote, em algarismos; nunca arredondar/converter semana-mês-dia.
3. Uma linha por regra, mesma ordem, `nome` literal.
4. Cláusula desconhecida: copiar o texto original dentro de `[não traduzido: ...]` e listar em `clausulas_nao_traduzidas`. Nunca "adivinhar".
5. Campo sem informação fica vazio; dúvidas vão para `alertas`.
6. Sem markdown nos campos de texto; sem nomes de empresa no resumo e nas consultas.

---

## 2. Formato de saída

| Opção | Prós | Contras | Veredito |
|---|---|---|---|
| Só Markdown (tabela como o ouro) | Idêntico ao ouro; legível | Validar exige parsear tabela; difícil separar resumo/consultas/metadados; frágil em modelo pequeno | Não |
| **JSON (schema) → renderizar Markdown e textos de embedding por código** | Validação trivial (campos, números, ordem); renderização determinística; chunks por regra de graça; mesmo contrato para Claude e Ollama (`format`) | Estudo mostra que restrição de formato pode piorar *raciocínio* | **Recomendado** |
| Ambos gerados pelo LLM | "Redundância" | Dobra custo e cria divergência entre as duas saídas | Não |

Sobre o risco de formato: Tam et al., "Let Me Speak Freely?" (https://arxiv.org/abs/2408.02442) relatam queda de desempenho em *raciocínio* sob restrições de formato, mais forte quanto mais rígida. Aqui o raciocínio é feito antes (cascata), a tarefa é de realização textual, então o efeito esperado é pequeno **(inferência)**. Mitigação barata: schema plano, campos de texto livre (não enums longos), sem limites de tamanho no schema.

Observação prática: subagentes do Claude Code **não** têm `output_config.format` (isso é da API; ver https://platform.claude.com/docs/en/build-with-claude/structured-outputs). Para eles, o contrato é: gravar um arquivo `.json` e deixar o validador (pydantic/jsonschema) aceitar ou mandar repetir. Já no Ollama, o schema é imposto pelo servidor (§6).

Embedding e recuperação usam o texto **derivado** do JSON (§3), nunca o Markdown cru.

---

## 3. Descrições que recuperam bem

Contexto: consultas serão descrições escritas por usuários no mesmo estilo dos exemplos (texto-para-texto simétrico). Escala pequena: 246 documentos, ~2,5 mil vetores no total; matriz em memória + cosseno em numpy basta, sem banco vetorial (SCALE-FIT).

### 3.1 Multi-representação (recomendado)

Padrão documentado no LangChain "multi-vector retriever": embutir *pedaços menores*, *resumos* e *perguntas hipotéticas*, e devolver o documento original (https://python.langchain.com/docs/how_to/multi_vector, resumo via busca; não verifiquei o texto completo). Para este projeto:

| Vetor | Texto embutido | Quantidade/arquivo | Aponta para |
|---|---|---|---|
| Arquivo | `resumo` + linhas `criterio | frequência` renderizadas em frase corrida | 1 | arquivo |
| Regra | 1 linha de contexto + `criterio` + `frequencia` + `observacao` | 1 por regra | arquivo (+ regra) |
| Consulta hipotética | texto "de usuário" | 3 | arquivo |

- Pontuação do arquivo = **máximo** entre seus vetores (simples; pode-se testar soma ponderada depois).
- **Contexto no chunk de regra:** prefixar 1 linha ("Regra de agendamento do time de televendas; 5 faixas de recência") antes do texto da regra. É a ideia do Contextual Retrieval da Anthropic (35% a 49% menos falhas de recuperação nos testes deles, com BM25 junto): https://www.anthropic.com/news/contextual-retrieval. Aqui o contexto sai de graça da mesma chamada do redator (campo `resumo`).
- Embutir **a descrição**, não o DSL. Guardar o `.gobr` como *payload* devolvido ao agente (é ele que serve de exemplo ao usuário).
- **Mascarar** nomes de empresa/boilerplate no texto embutido (§0.8); manter no metadado.

### 3.2 Consultas hipotéticas (doc2query / HyDE invertido)

- Doc2query original adiciona consultas previstas ao documento antes de indexar (Nogueira et al., https://arxiv.org/abs/1904.08375). Doc2query-- mostra que o modelo **inventa conteúdo** e que filtrar as consultas geradas melhora a recuperação (até 16%) e reduz índice (33%) (https://arxiv.org/abs/2301.03266). HyDE é o inverso, do lado da consulta (https://arxiv.org/abs/2212.10496); a variante do lado do documento ("reverse HyDE", perguntas hipotéticas por documento) é prática de comunidade, sem página oficial que eu tenha conseguido verificar (https://developers.llamaindex.ai/python/framework/optimizing/advanced_retrieval/query_transformations/ cobre só HyDE do lado da consulta).
- **Adaptação:** as consultas reais serão *descrições*, não perguntas. Gerar 3 "descrições de usuário" por arquivo em registros diferentes: (a) telegráfica estilo tabela, (b) narrativa informal ("a gente liga pra quem comprou nos últimos 30 dias a cada 14 dias..."), (c) incompleta (sem nomes de regra, só números e segmentos).
- **Filtro à la doc2query--, barato e determinístico:** todo número presente na consulta hipotética deve existir em `numeros` do pacote; senão, descartar. Sem modelo de relevância (inferência: o filtro numérico cobre o modo de falha principal aqui).
- Query2doc (expansão do lado da consulta, https://arxiv.org/abs/2303.07678) fica como opção futura no agente: reescrever a descrição do usuário na mesma estrutura do índice antes de buscar. Só se o retrieval básico falhar.

### 3.3 Números e hibridização (inferência, testar)

Os documentos do corpus são quase idênticos em estrutura e diferem sobretudo por **números e segmentos** (30/45 dias vs. 60/90/120). Embeddings densos tendem a ser fracos em números **(hipótese, não verificada aqui)**. Opções baratas: (i) BM25 sobre o mesmo texto embutido, fusão simples de scores (`rank-bm25` 0.2.2, Apache-2.0, PyPI; antigo (2022) mas estável: https://pypi.org/project/rank-bm25/); (ii) reordenar usando a sobreposição de `numeros` (extraídos da consulta do usuário). Medir antes de adotar (§9).

Também: muitos arquivos do corpus são duplicatas quase exatas ("Regra Padrão ... Customizável"). Sem tratamento, o top-k devolve 5 cópias do mesmo padrão. Recomendo (inferência) agrupar por **assinatura estrutural** (hash do pacote sem nomes) e devolver no máximo 1-2 por assinatura.

### 3.4 Embeddings em pt-BR

Tabela de modelos de embedding disponíveis no Ollama (verificados nas páginas da biblioteca):

| Modelo (tag Ollama) | Tamanho | Contexto | Idiomas | Licença | Observações |
|---|---|---|---|---|---|
| **`bge-m3`** (567M, 1,2 GB) | 567M | 8K | 100+ | MIT (card HF: https://huggingface.co/BAAI/bge-m3) | **Não exige prefixo de instrução**; artigo CC BY 4.0 (https://arxiv.org/abs/2402.03216). Recomendado. |
| `qwen3-embedding` (0.6b/4b/8b; 639MB/2.5GB/4.7GB) | 0,6-8B | 32K-40K (página inconsistente) | 100+ | Apache-2.0 (card HF do 0.6B: https://huggingface.co/Qwen/Qwen3-Embedding-0.6B) | Consulta precisa de `Instruct: ...\nQuery: ...` (docs recomendam instrução em inglês); 8B no topo do MTEB multilíngue (70,58 em 2025-06-05, segundo a página Ollama). |
| `embeddinggemma` (300m, 622MB) | 300M | 2K | 100+ | não verificado (página Ollama não informa) | Leve; 2K de contexto aperta só se o texto de arquivo for longo. |

Recomendação: **bge-m3** (MIT, sem prefixo, 8K cobre o arquivo inteiro, mesmo modelo para índice e consulta como exige a doc Ollama). Evidência específica de pt-BR: **não encontrei benchmark de recuperação em pt-BR verificável** (o CLARIN-PT-LDB é para português *europeu* e para LLMs, não embeddings: https://arxiv.org/abs/2603.12872). Então: validar localmente com o teste de auto-recuperação de §9.

Uso: `ollama.embed(model=..., input=[...])` aceita lista (lote) e devolve vetores L2-normalizados; usar cosseno (https://docs.ollama.com/capabilities/embeddings). `embeddinggemma-2` aparece na listagem da biblioteca Ollama, mas não o examinei.

---

## 4. Verificação de fidelidade além da cobertura por string

Camadas, da mais barata para a mais cara:

1. **Validador determinístico (já previsto):** nomes de regra literais e na ordem; todo `numeros` aparece (em `criterio`/`frequencia`); **nenhum número extra** em qualquer campo (incluindo resumo/consultas); `acao=nao_agendar` casa com "Não agendar"; `clausulas_nao_traduzidas` ⊇ `clausulas_desconhecidas` do pacote. Cobre Omissões e metade das Adições.
2. **Juiz LLM com rubrica binária por regra** (não nota 1-5): para cada linha, 4 perguntas sim/não: (a) condição equivalente à `condicao_efetiva`? (b) alguma afirmação sem base no pacote (finalidade, segmento inventado)? (c) cascata preservada ("mas não nos últimos N", "restante")? (d) estilo comercial curto sem jargão do DSL? Abordagem parecida com FActScore (decompor em fatos atômicos e checar cada um: https://arxiv.org/abs/2305.14251) e com os critérios humanos do GEM'24 (No-Omissions/No-Additions/Grammaticality/Fluency). G-Eval (https://arxiv.org/abs/2303.16634) usa formulário + CoT; aqui o formulário binário basta. Cuidados do juiz (Zheng et al., https://arxiv.org/abs/2306.05685): viés de posição, verbosidade e **autopreferência**; por isso o juiz deve ser instância *sem* contexto do gerador e, no experimento com Ollama, um modelo diferente (Claude).
3. **Ida-e-volta (round trip) por extração, não por regeneração do GOBR:** um agente "cego" recebe só a descrição JSON (sem pacote) e preenche uma lista estruturada: por regra `{recencia_min, recencia_max, outras_condicoes, acao, frequencia}`. Comparação com o pacote é determinística, **depois** da cascata. Ciclo de consistência é ideia estabelecida em data-to-text (Wang et al., ACL 2023, cycle training: https://arxiv.org/abs/2305.14793), mas ali serve para *treinar*; usá-lo como *verificador* é adaptação minha **(inferência)**.
   - Por que extração e não regenerar o `.gobr`: regenerar exige a gramática do gorules (57 páginas), mistura erro do redator com erro do gerador de DSL, e a comparação estrutural exige normalizar sintaxe. Extração para campos simples pega o que importa (número trocado, "entre 60 e 90" virando "90", catch-all mal descrito) por uma fração do custo.
   - É **vale a pena?** Sim em amostra, não necessariamente em todos. Custo: ~1,5 mil tokens por arquivo. Preços de API (referência): Sonnet 5.5 US$2 entrada / US$10 saída por MTok; Haiku 5.5 a partir de US$0,10 / US$0,50 (https://platform.claude.com/docs/en/models/overview). Para os 246 arquivos, a ordem de grandeza é de centavos a poucos dólares **(estimativa minha)**; via assinatura Claude Code não há cobrança por token. Recomendo rodar nos 3 ouros + amostra de ~25 arquivos + todos os que falharem no passo 2, e em *todos* os arquivos produzidos pelo modelo local.

---

## 5. Gerar com subagentes do Claude Code agora

Fatos verificados em https://code.claude.com/docs/en/sub-agents:

- Subagente = arquivo Markdown com frontmatter YAML; o corpo é o *system prompt*. Campos: `name`, `description` (obrigatórios), `tools` (lista permitida), `model` (aceita `sonnet`, `opus`, `haiku`, `fable`, **ID completo** ou `inherit`), entre outros.
- Cada subagente roda em contexto próprio e **não vê o histórico da conversa**. Até 20 em paralelo por padrão (`CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`).
- A página **não menciona temperature/top-p**; alavancas: modelo, `effort`, `maxTurns`.

Recomendações:

1. **Um arquivo de agente, `redator.md`** (em `.claude/agents/`), com instruções + 3-4 exemplos congelados + schema; `tools: Read, Write` (sem busca na web); `model: claude-sonnet-5-5` (ID completo, fixa o snapshot; "Every Claude model ID is a pinned snapshot", doc de modelos). Isso é o "prompt compartilhado": todos os agentes paralelos lêem o mesmo texto.
2. **Invocação mínima:** o prompt de cada chamada traz só a lista de arquivos de pacote (`ctx/regra_001.json` ...) e o diretório de saída. Nada de instruções extras (qualquer variação vira deriva de estilo).
3. **Lote por agente: 8-12 arquivos** (inferência). Pesa: o prompt fixo (~3-5 mil tokens) amortiza melhor com lote; mas lotes longos aumentam o risco de copiar a redação do arquivo anterior. Com 246 arquivos, 8-12 por agente dá ~21-31 chamadas; cabe no limite de 20 concorrentes em 2 ondas. Instruir: "processe cada arquivo de forma independente; **não leia saídas já geradas**; grave `out/<id>.json` imediatamente".
4. **Piloto antes do lote cheio:** 3 ouros + ~8 arquivos diversos (um por tipo de cláusula), revisão humana, só então congelar `prompt_version`.
5. **Determinismo:** não há botão de temperatura nos subagentes. Reprodutibilidade vem de (a) snapshot fixo, (b) prompt congelado, (c) **gerar uma vez e persistir** (FILE-STATE), regerando só quando `prompt_version` mudar, (d) validador rejeitando e reenviando. Medir variabilidade com a repetição ×3 no teste de ouro (§9).
6. **Proveniência injetada por script, não pelo LLM:** depois que o agente grava o JSON, um script adiciona `_meta` = `{prompt_version (sha256[:12] de redator.md), schema_version, model: "claude-sonnet-5-5", gerador: "claude-code-subagent", gerado_em, sha256_gobr, sha256_pacote, resultado_validador}`. O LLM não deve se autodeclarar modelo/versão (pode errar).
7. **Custo (estimativa minha):** ~6 mil tokens de entrada + ~1 mil de saída por arquivo, ×246 = ~1,5M entrada + ~0,25M saída; a US$2/US$10 por MTok dá ordem de **US$5** sem cache (mais, se `effort` alto gerar muito raciocínio). Via assinatura, sem custo por token.

---

## 6. Portar para Ollama depois

### 6.1 Suporte a saída estruturada (docs oficiais, https://docs.ollama.com/capabilities/structured-outputs)

- Parâmetro `format`: `"json"` ou **um objeto JSON Schema**. Exemplo em Python: `format=Modelo.model_json_schema()` e `Modelo.model_validate_json(resposta)` (Pydantic).
- A doc recomenda: **também colocar o schema no prompt** (para ancorar a resposta) e **temperatura baixa (ex.: 0)** para completions mais determinísticos.
- Limitação listada: o *Ollama Cloud* não suporta saída estruturada (uso local OK). A página não detalha quais recursos de JSON Schema são suportados; testar o schema real (planos, sem `minLength`/`pattern`).
- Cliente Python oficial: pacote `ollama` 0.6.3 (MIT, Python >=3.8), https://pypi.org/project/ollama/. Pydantic 2.14.1 (https://pypi.org/project/pydantic/), `jsonschema` 4.26.0 (MIT, Python >=3.10, https://pypi.org/project/jsonschema/). Todos compatíveis com Python 3.11.
- **Contexto:** a FAQ diz padrão de **4096** tokens (`OLLAMA_CONTEXT_LENGTH` ou `options.num_ctx`); a página do Modelfile ainda lista `num_ctx` padrão **2048**. As docs divergem, e o comportamento ao exceder não está descrito (risco de truncamento silencioso do pacote). **Definir `num_ctx` explicitamente** (ex.: 8192) e testar com o maior pacote. Também `seed` e `temperature` existem como parâmetros do Modelfile/opções (https://docs.ollama.com/modelfile).
- Interação de saída estruturada com modelos "thinking" (Qwen, Gemma): **não documentada** nas páginas que li; testar.

### 6.2 O que muda para modelos menores (inferência, a validar no experimento)

1. **Template-first:** a camada determinística entrega `descricao_base` por regra (frase pt-BR gerada por template a partir de `condicao_efetiva`); o modelo pequeno só *polimenta/escolhe* e escreve resumo/consultas. Ablação obrigatória: mede se o LLM melhora o retrieval em relação ao texto-template puro (baseline B0 em §9). Se não melhorar, **o redator pode ser quase todo determinístico** e o LLM só gera o resumo e as consultas.
2. **Uma tarefa por chamada:** (a) chamada por regra → `{criterio, frequencia, observacao}`; (b) uma chamada final → `{resumo, consultas_hipoteticas}` a partir das descrições das regras já validadas. ~1,4 mil chamadas locais (246 arquivos × ~5-6 regras), viável.
3. **Prompt curto:** só as regras de fidelidade (§1.4) + 2 exemplos do *mesmo tipo de cláusula* (seleção dinâmica por assinatura, §1.3 fase 2) + glossário só das cláusulas daquela regra.
4. **Temperatura 0, `seed` fixo, `num_ctx` explícito, schema no prompt e em `format`.**
5. Validador igual, com repetição automática (até 2 tentativas) por regra, não por arquivo (granularidade menor = retentativa barata).

### 6.3 Candidatos locais (verificados na biblioteca Ollama e nos cards)

| Modelo (tag Ollama) | Tamanho em disco / VRAM | Evidência pt-BR | Licença | Contexto | Recomendação |
|---|---|---|---|---|---|
| **`gemma4:12b`** | 7,7-8,0 GB em disco; VRAM = pesos + KV (estimativa: ~9-10 GB, não verificado) | Card HF: "35+ idiomas de fábrica, pré-treino em 140+"; MMMLU 83,4% (instruction-tuned). Sem benchmark específico de pt-BR verificado | Apache 2.0 (card HF: https://huggingface.co/google/gemma-4-12b-it; a página Ollama não informa licença) | 256K | **Recomendado como primeiro a testar** |
| `granite4.2:8b` | 5,3 GB em disco | Página Ollama lista **Portuguese** entre os idiomas suportados; sem benchmark | Apache 2.0 (página Ollama) | 128K | Alternativa se a VRAM for limitada; página destaca saída JSON/RAG |
| `qwen3.5:9b` | 6,6-7,6 GB em disco | "201 idiomas e dialetos"; card HF cita MMMLU/INCLUDE/WMT24++, sem pt-BR específico | Apache 2.0 (card HF: https://huggingface.co/Qwen/Qwen3.5-9B) | 256K | Modo thinking pode inflar tokens (comportamento com `format` não verificado) |

Páginas: https://ollama.com/library/gemma4 , https://ollama.com/library/granite4.2 , https://ollama.com/library/qwen3.5. Notas: (i) **nenhum** tem evidência de qualidade de *geração* em pt-BR que eu tenha conseguido verificar; a recomendação é para o experimento, não um veredito; (ii) VRAM exata depende de quantização e `num_ctx` (não verificado); (iii) `gemma3` (Gemma Terms of Use, 140+ idiomas, 4b/12b/27b) também existe na biblioteca, mas a licença Gemma 3 é mais restritiva que Apache 2.0, então ficou de fora da tabela; (iv) `mistral-small3.2` existe (24B, 15 GB), mas a página não lista português e é maior que o necessário.

Critério de escolha entre eles: rodar o conjunto de avaliação de §9 (ouros + 20 arquivos) e comparar taxa de aprovação do validador, adições do juiz e tempo por arquivo.

---

## 7. Rascunho do prompt e do schema (pt-BR)

### 7.1 System prompt (arquivo `redator.md`; corpo do subagente)

```text
Você é o REDATOR de um pipeline que documenta regras comerciais do Govendas
(linguagem GoBR/gorules) em português do Brasil, com linguagem de negócio curta.

<papel>
Você recebe um PACOTE JSON já analisado por um programa. Seu único trabalho é
ESCREVER texto comercial a partir dele. Você NÃO interpreta código gorules, NÃO
recalcula a cascata de regras e NÃO decide nada de negócio.
</papel>

<fidelidade>
1. Use SOMENTE o que está no pacote. Nada de conhecimento externo.
2. Não explique finalidade, benefício ou intenção que não esteja escrita no pacote.
3. Todo número (dias, quantidades) deve ser copiado do pacote, em algarismos.
   Nunca arredonde, converta (semana/mês/dia) nem invente limites.
4. Escreva exatamente uma linha por regra, na MESMA ORDEM do pacote, com `nome`
   copiado literalmente e `id` igual ao do pacote.
5. As regras são avaliadas em ordem e a primeira que casa vence. O campo
   `condicao_efetiva` JÁ considera as regras anteriores. Escreva o critério a
   partir de `condicao_efetiva`, nunca de `filtros_brutos`.
6. Se uma regra tiver `clausulas_desconhecidas`, escreva no critério
   "[não traduzido: <texto original>]" e repita o texto em
   `clausulas_nao_traduzidas`. Nunca tente adivinhar o significado.
7. Se não houver informação para um campo, deixe-o vazio (""), sem preencher por
   suposição. Dúvidas e ambiguidades vão em `alertas`.
8. `restricoes_herdadas` e `restricoes_globais` NÃO devem ser repetidas em cada
   linha: cite-as uma vez no `resumo`. Use `observacao` só para condições
   próprias da regra.
</fidelidade>

<estilo>
- Frases curtas, voz comercial, como numa planilha de planejamento:
  "Clientes que compraram nos últimos 90 dias mas estão a 60 dias sem comprar".
- Traduza o jargão do DSL: "recencia de positivacao" vira "compraram/compra nos
  últimos N dias"; "fora da recencia" vira "sem comprar há mais de N dias" etc.,
  conforme o `glossario` da regra.
- `criterio`: até 25 palavras. `observacao`: até 20 palavras.
- `frequencia`: "<N> dias" ou "Não agendar", conforme `acao`.
- `resumo`: 2 a 3 frases, sem nomes de empresa: quem é atendido (time/carteira),
  quantas faixas/regras, o que bloqueia a agenda, e o papel da regra final.
- `consultas_hipoteticas`: 3 descrições que um usuário de negócio poderia
  escrever para pedir ESTA configuração, em registros diferentes:
  (a) telegráfica, (b) narrativa informal, (c) incompleta (sem nomes de regra).
  Use apenas números presentes no pacote.
- Nenhum markdown dentro dos campos.
</estilo>

<exemplos>
(3 a 4 pares pacote -> saída, congelados: Maxlub adaptado, Infinitto adaptado,
V1Vidros adaptado e um de carteira com "regra padrão". Ver 7.4.)
</exemplos>

Responda gravando o JSON no arquivo de saída indicado, e nada além do JSON.
```

### 7.2 Template da mensagem do usuário (uma por arquivo; no lote, uma por arquivo listado)

```text
<pacote>
{pacote_json}
</pacote>

Escreva a descrição deste pacote seguindo as regras do sistema e o schema.
Grave em: {caminho_absoluto_saida}
```

(No lote de subagente: "Para cada arquivo abaixo, leia o pacote, gere a saída e grave `out/<id>.json`; trate cada um de forma independente e não leia saídas anteriores." + lista de caminhos absolutos. Caminhos absolutos sempre, por PATH-DRIFT.)

### 7.3 Schema de saída (JSON Schema; só recursos básicos, portável para Ollama `format`)

```json
{
  "type": "object",
  "properties": {
    "resumo": {"type": "string"},
    "regras": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": {"type": "string"},
          "nome": {"type": "string"},
          "segmento": {"type": "string"},
          "criterio": {"type": "string"},
          "frequencia": {"type": "string"},
          "observacao": {"type": "string"},
          "clausulas_nao_traduzidas": {"type": "array", "items": {"type": "string"}}
        },
        "required": ["id", "nome", "segmento", "criterio", "frequencia",
                     "observacao", "clausulas_nao_traduzidas"],
        "additionalProperties": false
      }
    },
    "consultas_hipoteticas": {"type": "array", "items": {"type": "string"}},
    "alertas": {"type": "array", "items": {"type": "string"}}
  },
  "required": ["resumo", "regras", "consultas_hipoteticas", "alertas"],
  "additionalProperties": false
}
```

Colunas do Markdown renderizado (espelham o ouro): `Segmento | Critério | Frequência | Observação`. `segmento` é o rótulo curto (pode ser igual a `nome`). `_meta` é adicionado por script (§5.6), fora do schema do LLM. Esquema evita `minLength`, `pattern` e limites numéricos (a API de saída estruturada da Anthropic não os suporta; é mais seguro para ambos os backends).

### 7.4 Exemplo adaptado (V1Vidros; o pacote abaixo é ilustrativo, o formato real vem do agente determinístico)

Pacote (resumido):

```json
{
  "arquivo": "V1Vidros-RegraComercial.gobr",
  "escopo": {"times": ["televendas"], "carteiras": []},
  "restricoes_globais": [
    {"id": "B1", "nome": "Nao agendar baixados receita",
     "texto_base": "Clientes com situação 'baixada' na Receita Federal não são agendados",
     "acao": "nao_agendar"}
  ],
  "regras": [
    {"id": "R1", "posicao": 1, "nome": "Clientes Ativos",
     "condicao_efetiva": "compraram nos últimos 30 dias",
     "acao": {"tipo": "frequencia", "valor": 14, "unidade": "dias"},
     "numeros": [30, 14],
     "glossario": {"recencia de positivacao em 30 dias": "Clientes cuja última compra ocorreu nos últimos 30 dias"},
     "clausulas_desconhecidas": []},
    {"id": "R2", "posicao": 2, "nome": "Risco de Inatividade",
     "filtros_brutos": ["recencia de positivacao em 45 dias", "fora da recencia de positivacao em 30 dias"],
     "condicao_efetiva": "compraram nos últimos 45 dias mas não compraram nos últimos 30 dias",
     "acao": {"tipo": "frequencia", "valor": 7, "unidade": "dias"},
     "numeros": [45, 30, 7], "clausulas_desconhecidas": []},
    {"id": "R3", "posicao": 3, "nome": "Inativos",
     "condicao_efetiva": "sem compra há mais de 45 dias",
     "acao": {"tipo": "frequencia", "valor": 14, "unidade": "dias"},
     "numeros": [45, 14], "clausulas_desconhecidas": []},
    {"id": "R4", "posicao": 4, "nome": "Clientes Prospects",
     "condicao_efetiva": "clientes em ciclo de vida prospect com a empresa",
     "acao": {"tipo": "frequencia", "valor": 7, "unidade": "dias"},
     "numeros": [7], "clausulas_desconhecidas": []}
  ]
}
```

Saída esperada (resumida):

```json
{
  "resumo": "Regra comercial do time de televendas com quatro faixas de agendamento por recência de compra (30 e 45 dias) e prospects. Clientes baixados na Receita Federal não são agendados. Frequências de 7 a 14 dias.",
  "regras": [
    {"id": "R1", "nome": "Clientes Ativos", "segmento": "Clientes Ativos",
     "criterio": "Clientes com pedido nos últimos 30 dias", "frequencia": "14 dias",
     "observacao": "", "clausulas_nao_traduzidas": []},
    {"id": "R2", "nome": "Risco de Inatividade", "segmento": "Risco de Inatividade",
     "criterio": "Clientes com pedido nos últimos 45 dias, mas estão a 30 dias sem comprar",
     "frequencia": "7 dias", "observacao": "", "clausulas_nao_traduzidas": []},
    {"id": "R3", "nome": "Inativos", "segmento": "Inativos",
     "criterio": "Clientes sem pedidos há mais de 45 dias", "frequencia": "14 dias",
     "observacao": "", "clausulas_nao_traduzidas": []},
    {"id": "R4", "nome": "Clientes Prospects", "segmento": "Prospects",
     "criterio": "Clientes em ciclo de vida prospect", "frequencia": "7 dias",
     "observacao": "", "clausulas_nao_traduzidas": []}
  ],
  "consultas_hipoteticas": [
    "Ativos 30 dias a cada 14 dias; risco de inatividade 45 dias a cada 7; inativos a cada 14; prospects a cada 7",
    "A gente liga a cada 14 dias para quem comprou no último mês, a cada 7 para quem comprou há mais de 30 e menos de 45 dias, e não liga para cliente baixado na Receita",
    "Quero regra de televendas com 4 faixas por tempo sem comprar e prospects toda semana"
  ],
  "alertas": []
}
```

(Texto do ouro em `V1Vidros-RegraComercial.pdf`; "Agendar Inadimplentes" do mapa mental não existe no `.gobr` e por isso **não** entra na saída.)

---

## 8. Dead ends e não verificado

- Subagentes do Claude Code: sem controle documentado de temperatura/top-p (página oficial não cita).
- Não achei benchmark de embedding ou de geração em pt-BR *brasileiro* para os modelos listados; CLARIN-PT-LDB é português europeu (https://aclanthology.org/2026.propor-1.7/).
- GEM'24/SaarLST: li só resumos de busca; páginas ACL retornaram 404/erro ao buscar. Tratar o resultado "1º lugar" como relato, não como verificado no texto.
- LlamaIndex: não há recurso oficial por documento para "perguntas hipotéticas" (só HyDE de consulta e `DocumentSummaryIndex`, descrito por resposta de comunidade); LangChain multi-vector verificado apenas via resumo de busca.
- Docs Ollama divergem sobre `num_ctx` padrão (4096 vs 2048).
- Licença do `embeddinggemma` e da página Ollama do `gemma4`: não informadas na página Ollama; a do `gemma4` foi confirmada no card HF.
- Preço/custo: estimativas minhas a partir da tabela de preços oficial; não medi tokens reais.

---

## 9. Pipeline recomendado e plano de avaliação

### 9.1 Pipeline recomendado (etapa REDATOR)

1. **Pacote (determinístico)** por `.gobr`: blocos em ordem, `condicao_efetiva` com cascata, `restricoes_globais/herdadas`, `numeros`, glossário por cláusula, `clausulas_desconhecidas`; sem URLs/comentários; `assinatura_estrutural`.
2. **Redator (Sonnet via subagente `redator.md`, `model: claude-sonnet-5-5`)**: lote de 8-12 arquivos, few-shot fixo de 3-4, saída `out/<id>.json` conforme o schema (§7.3). Um agente, um prompt congelado, sem leitura de saídas anteriores.
3. **Validador determinístico**: schema + ordem + nomes literais + números (faltando e sobrando) + ação + cláusulas desconhecidas. Falhou: reenvia só aquele arquivo, no máximo 2 vezes; ainda falhou: fila de revisão manual.
4. **Auditoria por amostra**: juiz LLM binário por regra + round trip por extração (§4) nos 3 ouros, ~25 arquivos aleatórios e todo arquivo com alertas.
5. **Injeção de `_meta`** por script (prompt_version, modelo, hashes, resultado do validador) e gravação final em `corpus/descricoes/<id>.json`.
6. **Renderização determinística**: Markdown (tabela `Segmento | Critério | Frequência | Observação` + resumo) para exibição; textos de embedding: arquivo, regra (com 1 linha de contexto) e 3 consultas hipotéticas, com nomes de empresa/boilerplate mascarados.
7. **Índice**: `bge-m3` via `ollama.embed` (lote), cosseno em numpy, pontuação do arquivo = máximo dos vetores; dedup por assinatura no resultado. BM25 (`rank-bm25`) só se o teste de §9.2 mostrar fraqueza em números.
8. **Backend Ollama (depois)**: mesmo contrato e schema; chamada por regra + chamada de resumo; `format` = schema, schema no prompt, temperatura 0, `seed` fixo, `num_ctx` explícito; mesmos validador, juiz e testes.

### 9.2 Plano de avaliação (3 ouros como conjunto de teste, mais amostra)

Conjunto: Maxlub, Infinitto Design, V1Vidros (+ ~20 arquivos diversos de `referencias/` para o modelo local). Ouro é *referência de estilo e de cascata*, não gabarito exato (§0.1).

| # | Verificação | Como | Critério de aprovação |
|---|---|---|---|
| E1 | Cobertura determinística | Validador de §4.1 | 100% nos 3 ouros; ≥95% de arquivos sem retentativa no corpus |
| E2 | Cascata correta | Linhas-chave: Maxlub "Risco/Inativos (90, 120, 150)" ("compraram nos últimos N mas a M dias sem comprar"); Infinitto "Risco" (entre 60 e 90) e "Inativo" (catch-all, mais de 90); V1Vidros "Risco" (45 e fora de 30) e "Inativos" (mais de 45). Checagem automática por números `{N,M}` + juiz binário | 100% das linhas-chave |
| E3 | Sem adições | Juiz LLM binário (b) + números extras no validador; conferir que **não aparecem** "Capacidade 35/dia" (Maxlub) nem "Agendar Inadimplentes" (V1Vidros), pois não existem no `.gobr` | 0 adições |
| E4 | Equivalência com o ouro, linha a linha | Juiz compara `criterio` gerado com a linha do ouro: equivalente / diferente / omitido, ignorando o que o ouro tem a mais ou a menos que o `.gobr` | ≥90% equivalente nas linhas derivadas do `.gobr` |
| E5 | Round trip | Agente cego extrai campos da descrição; compara com pacote | 100% nos ouros; >=95% na amostra |
| E6 | Estabilidade | Gerar cada ouro 3 vezes; comparar números e `condicao`; medir variação de redação | números idênticos em 3/3; variação de estilo apenas cosmética |
| E7 | Estilo | Regras mecânicas: palavras por `criterio` ≤25, sem jargão do DSL (lista de termos proibidos, ex.: "recencia de positivacao"), sem markdown | 100% |
| E8 | **Retrieval (auto-recuperação)** | Para ~30 arquivos, um agente cego (sem ver a descrição gerada) escreve uma consulta de usuário a partir do `.gobr`; medir Recall@1/@5 do próprio arquivo ou de arquivo com **mesma assinatura estrutural** (duplicatas tornam o arquivo exato injusto). Incluir os 3 PDFs-ouro (texto) como consultas qualitativas | Comparar B0/B1/B2 abaixo; escolher o que maximiza Recall@5 |

Baselines (controle de custo-benefício, justificam ou não o LLM):

- **B0:** texto embutido gerado só por template determinístico (sem LLM).
- **B1:** redator Sonnet (este documento).
- **B2:** redator Ollama (`gemma4:12b`, depois `granite4.2:8b`/`qwen3.5:9b`), mesmo contrato.
- Variações de índice: só vetor de arquivo vs. multi-vetor (arquivo + regra + consultas) vs. + BM25.

Decisão proposta (Pedro decide): adotar B1 se superar B0 em E8 de forma perceptível; se B0 empatar, simplificar (resumo e consultas por LLM, tabela por template).

---

## 10. Fontes

- Anthropic, Prompting best practices: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- Anthropic, Reduce hallucinations: https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations
- Anthropic, Prompting Claude Sonnet 5.5: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5
- Anthropic, Structured outputs: https://platform.claude.com/docs/en/build-with-claude/structured-outputs
- Anthropic, Models overview (IDs e preços): https://platform.claude.com/docs/en/models/overview
- Claude Code, Subagents: https://code.claude.com/docs/en/sub-agents
- Anthropic, Contextual Retrieval: https://www.anthropic.com/news/contextual-retrieval
- Ollama, Structured outputs: https://docs.ollama.com/capabilities/structured-outputs ; Embeddings: https://docs.ollama.com/capabilities/embeddings ; FAQ: https://docs.ollama.com/faq ; Modelfile: https://docs.ollama.com/modelfile
- Ollama library: https://ollama.com/library/bge-m3 , /qwen3-embedding , /embeddinggemma , /gemma4 , /granite4.2 , /qwen3.5 , /gemma3 , /mistral-small3.2
- Hugging Face: https://huggingface.co/BAAI/bge-m3 ; https://huggingface.co/Qwen/Qwen3-Embedding-0.6B ; https://huggingface.co/Qwen/Qwen3.5-9B ; https://huggingface.co/google/gemma-4-12b-it
- PyPI: https://pypi.org/project/ollama/ (0.6.3) ; https://pypi.org/project/pydantic/ (2.14.1) ; https://pypi.org/project/jsonschema/ (4.26.0) ; https://pypi.org/project/rank-bm25/ (0.2.2)
- Papers: doc2query https://arxiv.org/abs/1904.08375 ; doc2query-- https://arxiv.org/abs/2301.03266 ; HyDE https://arxiv.org/abs/2212.10496 ; Query2doc https://arxiv.org/abs/2303.07678 ; KATE https://arxiv.org/abs/2101.06804 ; Let Me Speak Freely https://arxiv.org/abs/2408.02442 ; CoVe https://arxiv.org/abs/2309.11495 ; LLM-as-judge https://arxiv.org/abs/2306.05685 ; G-Eval https://arxiv.org/abs/2303.16634 ; FActScore https://arxiv.org/abs/2305.14251 ; cycle training https://arxiv.org/abs/2305.14793 ; BGE M3-Embedding https://arxiv.org/abs/2402.03216 ; Multilingual E5 https://arxiv.org/abs/2402.05672
- GEM'24 / SaarLST (via busca, não verificado no texto): https://aclanthology.org/2025.inlg-genchal.4
- CLARIN-PT-LDB (português europeu): https://arxiv.org/abs/2603.12872
- Locais: `trabalho/trabalho/exemplos/*` (ouros), `trabalho/trabalho/referencias/regra_001|050|150|230.gobr`, `AppData/Local/Temp/sma_ctx/manual_utf8.txt` (§7.6, §6.2).

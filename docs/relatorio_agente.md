# Relatório da etapa: fluxo agêntico que gera a parametrização GoBR a partir de uma pergunta

## 1. Objetivo

Transformar o fluxo fixo da etapa anterior (`buscar → redigir → validar`, relatório em
`docs/relatorio_fluxo.md`) num agente que decide o que fazer: buscar mais exemplos ou o manual, perguntar
ao usuário quando falta algo no pedido, e só entregar depois que o validador e o conferente aprovam. O
enunciado pede um agente de conversação proativo, que aponte os pontos falhos da modelagem comercial e
devolva as regras em GoBR. O desenho e as alternativas descartadas estão em `docs/desenho_agente.md`.

## 2. O grafo (`gobr/agent.py`)

```
pedido ─► preparar ─► agente ─┬─ buscar_exemplos / buscar_manual ─► ferramentas ─► agente
                              ├─ perguntar_usuario ─► perguntar (interrupt) ─► agente
                              └─ entrega (texto com ```gobr) ─► validar ─(erro, < 3 entregas)─► agente
                                                                   └─(ok)─► conferir ─(divergência, 1ª)─► agente
                                                                               └─► responder
```

- **preparar** (determinístico): a busca da etapa anterior (3 exemplos por embeddings, com leave-out por
  assinatura na avaliação, e 3 seções do manual pela busca híbrida). É o piso: se o agente não chamar nenhuma
  ferramenta, faz o mesmo que o fluxo fixo.
- **agente** (LLM com ferramentas no formato da API OpenAI): `buscar_exemplos(consulta)`,
  `buscar_manual(consulta)` e `perguntar_usuario(pergunta)`. Responder em texto com um bloco ```gobr é
  entregar.
- **ferramentas**: executa as buscas e devolve o resultado como mensagem `role: tool`.
- **perguntar**: `interrupt()` do LangGraph pausa o grafo; `converse()` mostra a pergunta (no terminal, ou ao
  usuário simulado da avaliação) e retoma com `Command(resume=resposta)`. Exige checkpointer
  (`InMemorySaver`) e um `thread_id` por conversa.
- **validar**: o `check` da etapa anterior, sem mudança (parser, fontes, ações, regras inalcançáveis ou
  contraditórias, números do pedido). Antes, tira as linhas `#` depois do cabeçalho: na etapa anterior, o
  Maxlub terminava com 17 linhas de raciocínio do modelo.
- **conferir**: segunda chamada ao LLM, com prompt próprio (`redator/prompt_conferente.md`) e saída JSON
  (`response_format` json_schema). Recebe o pedido, as notas do redator e uma tabela que o pacote
  (`gobr.context.build`) calcula para cada regra: filtros (código), clientes (a `condicao_efetiva`, em
  português), bloqueios anteriores e ação. As respostas do usuário às perguntas entram junto com o pedido.
  Devolve, por regra, se confere com o pedido, e os segmentos do pedido sem regra. Divergência na 1ª
  conferência volta ao agente; na 2ª, vai para a resposta (o motivo, cortado em 300 caracteres).
- **responder**: `.gobr`, notas, erros que sobraram, divergências, alertas da cascata e perguntas feitas.

Limites: 8 chamadas do agente com ferramentas (na 8ª, as ferramentas saem e ele tem de entregar), 3
entregas, 2 perguntas, 1 volta do conferente.

CASCADE-FIRST continua valendo: quem diz o que cada regra faz é a cascata; o conferente só compara dois
textos em português. É o primeiro julgamento do LLM que pode devolver uma entrega, por isso fica limitado a
uma volta e, se ainda divergir, aparece para o usuário em vez de sumir.

## 3. Backend

O mesmo da etapa anterior: llama-server b11770 com `Qwen3.6-35B-A3B-UD-IQ4_XS.gguf` no PC (RTX 5060),
`--jinja`, `-c 32768`, 1 slot, `reasoning_effort="none"`, pelo túnel SSH. Antes de desenhar, um teste com 4
casos confirmou que o servidor devolve `tool_calls` nativos com o template do Qwen3.6 (a doc
`function-calling.md` do llama.cpp não lista Qwen3.x) e aceita a volta com `role: tool`.

## 4. Avaliação

Tabelas completas e comandos em `data/agente/avaliacao_agentico.md`.

### 4.1 Gabaritos: 3/3

Nos 3 exemplos do professor, sem o próprio gabarito na busca, os 3 `.gobr` passam no validador (fluxo fixo:
2/3). Tempo: 268 s para os 3 (fluxo fixo: 185 s). O InfinittoDesign, que no fluxo fixo inventava
`atividade da empresa em N dias`, saiu na 1ª entrega. Em três rodadas com o mesmo prompt, o resultado foi 3/3
em todas, mas o número de passos, perguntas e divergências variou entre elas: o servidor não é
determinístico mesmo com temperatura 0.

No V1Vidros da rodada final, "Agendar inadimplentes autorizados" virou uma regra que agenda (no fluxo fixo,
virava `nao agendar` nos dois modos). O conferente ainda devolveu duas divergências, ambas pertinentes:
- a frequência de 7 dias para os inadimplentes não está no pedido;
- o "Risco de inatividade" não tem o limite de 45 dias.

Sobre o segundo ponto, o agente afirmou nas notas e nas perguntas que o GoBR não combina "comprou em 45 dias
e está há 30 sem comprar". O gabarito do Maxlub faz exatamente isso
(`recencia ... em 90 dias e fora da recencia ... em 60 dias`), então a afirmação do agente é falsa, e a
divergência ficou na resposta para o usuário.

### 4.2 Perguntas: o agente não pergunta quando falta um dado

Nos 6 casos de `data/agente/casos_pergunta.json`, ele não perguntou nos 3 completos (certo) nem nos 3
incompletos (errado). Nos incompletos, inventou o que faltava:
- copiou para os inativos a frequência dos ativos;
- escolheu sozinho o critério de "ativo";
- leu "tratar à parte" como `nao agendar`.

O validador aprova os três, porque os números do pedido estão lá. O conferente também, porque julga
contradição, não ausência.

Nos gabaritos, ele pergunta sobre a modelagem: o V1Vidros perguntou como fazer a faixa de risco, e numa
rodada o Maxlub perguntou se mantinha uma regra final de bloqueio.

Ele também pergunta quando a falta é evidente. No terminal, com o pedido "Ativos: compra nos últimos 30 dias,
14 dias. Inativos: mais de 45 dias", ele perguntou a frequência dos inativos, usou a resposta (28 dias), e
o conferente aprovou. A diferença para o `falta_frequencia` é que lá "sem compra há mais de 30 dias" tem um
"N dias" no fim da linha, que pela convenção do formato pode ser lido como frequência.

Nessa rodada no terminal apareceu um defeito, já corrigido: o conferente não recebia as respostas do
usuário e acusava como inventado o valor que o usuário tinha dado. As tabelas de §4.1 a §4.3 foram medidas
antes dessa correção. Ela só muda a entrada do conferente quando há pergunta, o que nas avaliações aconteceu
só no V1Vidros.

Uma 2ª versão dos prompts tentou corrigir isso:
- no agente: "confira cada segmento; se faltar critério ou frequência, pergunte";
- no conferente: "valor que o pedido não dá é divergência".

Ela fez o agente perguntar no `acao_ambigua`, mas não nos outros dois. Nos gabaritos, o Maxlub passou a
reprovar: o agente gastou os 7 passos com ferramentas e, no 8º, sem ferramentas, escreveu a chamada como
texto em vez de entregar. Os prompts voltaram à versão 1. A abordagem que resolveu está em §4.4.

### 4.3 Conferente

Sozinho, nas 6 entregas da etapa anterior, acusou a ação invertida do V1Vidros nos dois modos e disse
"confere" nas outras quatro.

Nos 3 gabaritos, que não foram usados para ajustar o prompt, acusou 3 das 4 diferenças reais entre o pedido
e o gabarito, sem falso positivo. As diferenças reais são regras que a descrição não pede e um trecho do
pedido sem regra. A que faltou, os baixados do Maxlub, foi acusada numa rodada anterior.

O prompt foi ajustado com as próprias 6 entregas. Na 1ª versão, a tabela tinha só a `condicao_efetiva`, e
ele acusava dois falsos positivos no Maxlub:
- "prospect" aparece no pacote como "nunca compraram" (premissa P5);
- a exclusão da rota feita por um bloqueio não aparece na condição.

A tabela passou a mostrar o código dos filtros e os bloqueios anteriores de cada regra.

### 4.4 Triagem estruturada: agora pergunta quando falta dado

Para resolver §4.2, entrou uma triagem antes de redigir (`docs/desenho_agente.md` §9). Uma chamada ao LLM
com json_schema extrai cada segmento do pedido: nome, trecho, critério, ação (agendar, não agendar ou
indefinido) e frequência em dias. O código decide as lacunas:
- ação indefinida;
- segmento que agenda sem frequência;
- critério vazio fora dos residuais ("os demais").

O código faz uma só pergunta com todas as lacunas, e a resposta volta para a triagem. Os segmentos entram
como tabela na 1ª mensagem do agente. Depois do validador, o código compara a ação e a frequência de cada
regra com o segmento de mesmo nome, antes do conferente LLM.

Resultados (`data/agente/avaliacao_agentico.md` §4):
- **Perguntas:** a triagem achou lacuna nos 3 casos incompletos e em nenhum dos 3 completos, e o agente
  perguntou nos 3 incompletos. Sem triagem, foram 0 de 3. Num caso completo, o próprio agente fez 2
  perguntas sobre qual time e qual carteira usar, informação que nenhum pedido dá.
- **Gabaritos:** 3/3 mantido, em 352 s (sem triagem: 268 s). No V1Vidros, a triagem apontou a lacuna real,
  "Agendar Inadiplentes" sem frequência. Sem resposta na avaliação em lote, a lacuna foi para os avisos, e
  o agente ainda perguntou de novo duas vezes, com outras palavras.
- **Esquema:** numa sonda separada, o llama-server respeitou o json_schema com enum e inteiro nos 6 casos,
  com 4 a 10 s por chamada.

O critério de sucesso do desenho (§9.7) foi atingido em duas de três condições:
- perguntou em pelo menos 2 dos 3 incompletos: **sim, 3 de 3**;
- manteve 3/3 nos gabaritos: **sim**;
- não perguntou em nenhum dos 3 completos: **não, 1 de 3 teve perguntas**. Não vieram da triagem, e sim
  do agente, sobre time e carteira.

Ajustes durante a implementação:
- o prompt da triagem ganhou a regra "linha sem frequência nem bloqueio → indefinido", depois de uma sonda
  em que o `falta_frequencia` virava `nao_agendar`. Foi um ajuste feito vendo um caso da avaliação;
- o code-auditor mostrou falsos positivos no casamento de nomes por prefixo ("Ativos inadimplentes" julgada
  como "Ativos"), e o casamento passou a ser só exato ou "<segmento>:".

A comparação por segmento não achou nenhuma divergência nas avaliações (coluna "código" sempre 0), então a
cobertura dela nos casos reais não está medida. Os testes unitários mostram que ela pega frequência e ação
trocadas.

## 5. Limitações

- **Perguntas repetidas e fora da triagem:** sem resposta, o agente refaz a mesma pergunta com outras
  palavras (no V1Vidros, a frequência dos inadimplentes três vezes, contando a da triagem). A checagem de
  pergunta repetida só pega texto idêntico. As perguntas sobre time e carteira também não passam pela
  triagem.
- **A comparação por segmento não foi exercitada nas avaliações** (§4.4): só os testes unitários a cobrem.
- **Custo da triagem:** uma chamada a mais por pedido e duas quando há pergunta (4 a 10 s cada na sonda).
  Nos gabaritos, o tempo total subiu de 268 s para 352 s, com variação entre rodadas no meio.
- **Entrega forçada não garante entrega:** sem ferramentas, o Qwen3.6 pode escrever a chamada de ferramenta
  como texto. O grafo termina, mas sem arquivo (visto só com o prompt da 2ª versão).
- **Notas longas:** o prompt pede até 5 linhas, e o InfinittoDesign escreveu parágrafos de raciocínio.
  Não afetam a validação.
- **Avaliação pequena:** 3 gabaritos, 6 casos de pergunta e 9 arquivos no conferente. Os números mostram onde
  o agente erra, não uma taxa de acerto. O prompt do conferente foi ajustado com as 6 entregas que também
  servem para medi-lo.
- **Variação entre rodadas** com temperatura 0: passos, perguntas e divergências mudam; a aprovação nos
  gabaritos não mudou em três rodadas.
- **Ordem das mensagens `tool`:** quando o agente pede busca e pergunta na mesma mensagem, a resposta da
  busca vem antes, fora da ordem das chamadas. A API aceita; nenhum caso real teve as duas juntas.
- Só texto; entrada por imagem (`mmproj`) continua para depois.

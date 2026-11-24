# Desenho: agente com memória de contexto

Etapa de 2026-11-24. Parte do fluxo agêntico (`gobr/agent.py`, commit `9b7193a`, relatório em
`docs/relatorio_agente.md`).

## 1. O problema

O agente anterior trata um pedido por execução. `converse` cria um `thread_id` novo por pedido, o
checkpointer fica em RAM e só serve para o `interrupt` das perguntas. Depois da resposta, não há como
dizer "troque os ativos para 15 dias" ou "por que a regra 3 não pega ninguém?", e o que o usuário respondeu
se perde.

## 2. Escolhas (Pedro, 2026-11-24)

| Decisão | Escolhida | Alternativas |
|---|---|---|
| Escopo | **conversa persistente**: vários turnos, retomada depois de fechar, contexto compactado | com memória de longo prazo do usuário (um fato velho pode entrar numa regra sem ninguém notar); só na sessão (nada persiste) |
| Armazenamento | **`SqliteSaver`** (`langgraph-checkpoint-sqlite` 3.1.3, MIT): retoma até uma pergunta pendente | JSON próprio (não retoma o `interrupt`); `InMemorySaver` (nada persiste) |

## 3. O que é a memória

A memória não é o histórico de mensagens reenviado ao LLM. É um estado estruturado, guardado pelo
checkpointer a cada nó:

| Campo | O que guarda | Quem escreve |
|---|---|---|
| `pedido` | o pedido vigente, linha a linha, já com as mudanças e as respostas do usuário | código |
| `versoes`, `versao_atual` | cada `.gobr` aprovado, com o pedido, os segmentos e as notas daquele momento, e a versão de onde veio | código |
| `turnos` | um registro curto por turno: mensagem, tipo, o que aconteceu, perguntas e respostas | código |
| `sem_resposta` | lacunas que a triagem perguntou e ninguém respondeu: não pergunta de novo | código |

Os campos de trabalho (mensagens do agente, contadores, erros) são zerados a cada turno. O diálogo com as
ferramentas não passa de um turno para o outro, e por isso o contexto não cresce com a conversa.

## 4. O grafo

| de | condição | para |
|---|---|---|
| início | | receber (código: zera o trabalho do turno) |
| receber | ainda não há pedido | triagem (igual à etapa anterior) |
| receber | já há pedido | interpretar (LLM, JSON) |
| interpretar | `alterar` ou `novo` | triagem → … → responder |
| interpretar | `duvida` | explicar |
| interpretar | `desfazer` | desfazer (código) |
| interpretar | nada aplicável | lembrar, com um pedido de esclarecimento |
| responder, explicar, desfazer | | lembrar → fim |

- **interpretar**: o LLM classifica a mensagem e, se for mudança, devolve operações sobre as linhas numeradas
  do pedido vigente (`alterar`, `incluir`, `remover`). Quem aplica é o código (`memory.apply_operations`): as
  linhas não citadas ficam idênticas, então os números delas continuam exigidos pelo validador. Um LLM que
  reescrevesse o pedido inteiro poderia perder um número sem ninguém notar. Número novo que não está na
  mensagem vira aviso.
- **preparar**, num turno de mudança, põe na 1ª mensagem do agente o pedido vigente, o arquivo atual, o que
  mudou, o histórico compactado e as notas anteriores. No 1º turno a mensagem é a mesma da etapa anterior.
- **conferir** ganha duas checagens em código: regra que a mudança não cita não pode mudar, sumir nem trocar de
  ordem (`memory.untouched_changes`), e bloqueio novo vem antes das regras de frequência (`late_blocks`, §7).
  Divergência volta ao agente uma vez, pelo canal que já existe.
- **responder** mostra a mudança no pedido e a diferença no arquivo, regra a regra, calculadas pelo código.
- **explicar**: responde dúvidas a partir da tabela de regras do pacote, do pedido, dos alertas da cascata,
  do histórico, das versões e do manual. Não muda o arquivo; bloco de código na resposta é retirado.
- **desfazer**: move `versao_atual` para a versão de origem (ou a pedida) e restaura o pedido e as lacunas dela.
- **lembrar**: grava a versão (só se passou no validador), o pedido e o registro do turno. Se a mudança não
  passou, o pedido e o arquivo da versão anterior continuam valendo.

## 5. Compactação

O histórico entra no prompt do mais novo para o mais velho até um orçamento de caracteres; os turnos que não
cabem ficam só no banco. Não há LLM resumidor: o efeito de todos os turnos já está no pedido vigente e nas
versões, e um resumo livre poderia perder números (CASCADE-FIRST).

## 6. Avaliação

`avaliar-memoria data/agente/casos_memoria.json <saída> --modo memoria|concatenada|nenhuma`. Cada caso é uma
conversa com as saídas esperadas escritas à mão antes de rodar (frequência de cada regra, regras intactas,
regra ausente, números presentes e ausentes, arquivo igual ao de um turno, trecho na resposta, limite de perguntas). No modo `memoria`, o grafo e a conexão são
recriados a cada turno, então todo turno depois do 1º também testa a retomada.

Linhas de base: `nenhuma` (cada mensagem é um pedido novo, o comportamento anterior) e `concatenada` (todas
as mensagens juntas viram o pedido: a memória mais simples possível).

Critério, escrito antes de medir: a memória acerta mais verificações que as duas linhas de base, o tamanho do
prompt não cresce com o número de turnos, e os 3 gabaritos seguem 3/3.

## 7. O que mudou depois da auditoria (2026-11-24)

O `code-auditor` reproduziu 12 defeitos na 1ª versão, com um LLM falso, e a medição que estava rodando foi
descartada. O que mudou no desenho:

- **Números das notas:** num turno de mudança, citar o número nas notas não basta para o validador dispensá-lo;
  só vale a linha que diz "o GoBR não tem cláusula para isso". Antes, "alterei de 14 para 15" dispensava o 15.
- **Segmentos congelados** (`keep_segments`): só congela o segmento completo que a mudança não cita nem pelo
  nome, nem pela linha de onde saiu. Mudança que não cita segmento nenhum ("todos a cada 10 dias") não congela
  nada. Segmento que a triagem esqueceu volta.
- **`untouched_changes`** não julga mudanças que podem valer para todos e passa a olhar também as fontes da
  regra (time, carteira, segmentação).
- **Pedido novo** não herda as lacunas sem resposta do anterior, e cada versão guarda as suas. Número da
  mensagem que não entrou no pedido novo vira aviso (antes, a mensagem inteira virava o pedido; hoje isso só acontece se o LLM não devolve nenhuma linha).
- **Desfazer** depois de uma mudança que não entrou não derruba a versão que tinha passado.
- **CLI:** mensagem nova substitui um turno que sempre falha; pergunta pendente continua sendo retomada.
- **Avaliação:** turno que falhou não passa em nenhuma verificação (antes, o modo com memória herdava o
  arquivo anterior e levava pontos), e caso com exceção fica no denominador.

Depois da 1ª rodada com o LLM real, lendo as conversas:

- **Bloqueio novo** tem de vir antes das regras de frequência (`late_blocks`, pelo alerta da cascata): divergência em
  código. A avaliação ganhou `bloqueia_antes`.
- **Numeração** da lista copiada pelo LLM ("4. Inadimplentes") é retirada pelo código.

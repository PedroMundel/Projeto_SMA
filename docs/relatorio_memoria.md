# Relatório da etapa: agente com memória de contexto

## 1. Objetivo

O agente da etapa anterior (`docs/relatorio_agente.md`) trata um pedido por execução: depois da resposta, esquece
tudo. Esta etapa faz dele um agente de conversação de verdade. O usuário muda o que pediu, pergunta sobre as regras,
volta a uma versão anterior e retoma a conversa depois de fechar o programa, até no meio de uma pergunta do agente.
As escolhas e as alternativas estão em `docs/desenho_memoria.md`.

## 2. O que é a memória

Não é o histórico reenviado ao LLM. É um estado estruturado, que o checkpointer do LangGraph (`SqliteSaver`, um banco
local) guarda a cada nó. Cada conversa é um `thread_id`.

| Memória | O que guarda |
|---|---|
| pedido vigente | as linhas do pedido, com as mudanças e as respostas do usuário |
| versões | cada `.gobr` aprovado, o pedido e os segmentos daquele momento e a versão de onde veio |
| turnos | mensagem, tipo, resultado e perguntas de cada turno, em uma linha |
| lacunas sem resposta | o que a triagem já perguntou e ninguém respondeu |

O resto do estado (mensagens do agente, buscas, contadores) é zerado no começo de cada turno. Por isso o contexto não
cresce com a conversa.

## 3. O grafo (`gobr/agent.py`, `gobr/memory.py`)

| de | condição | para |
|---|---|---|
| início | | receber |
| receber | ainda não há pedido | triagem (o fluxo da etapa anterior, com os mesmos prompts) |
| receber | já há pedido | interpretar |
| interpretar | mudança ou pedido novo | triagem → preparar → agente → validar → conferir → responder |
| interpretar | dúvida | explicar |
| interpretar | voltar a uma versão | desfazer |
| interpretar | nada que dê para aplicar | lembrar, com um pedido de esclarecimento |
| responder, explicar, desfazer | | lembrar → fim |

- **interpretar** (LLM com json_schema, `redator/prompt_interprete.md`): classifica a mensagem e, numa mudança, devolve
  operações sobre as linhas numeradas do pedido (alterar, incluir, remover). **O código aplica**: as linhas não citadas
  ficam idênticas, e os números delas continuam exigidos pelo validador. Número que o usuário não disse, ou que disse
  e não entrou em linha nenhuma, vira aviso.
- **agente**, num turno de mudança, recebe o pedido vigente, o arquivo atual, o que mudou, o histórico compactado e as
  notas anteriores.
- **triagem**, num turno de mudança: segmento completo que a mudança não cita fica como era, mesmo que o LLM o leia
  diferente ou o esqueça (código).
- **conferir** ganhou duas checagens em código: regra que a mudança não cita não pode mudar (nem as fontes dela), sumir
  nem trocar de ordem; bloqueio novo tem de vir antes das regras de frequência. Divergência volta ao agente uma vez.
- **explicar** (LLM, `redator/prompt_explicar.md`): responde com a tabela de regras calculada pela cascata, os alertas,
  o histórico, as versões e o manual. Não muda o arquivo.
- **responder** mostra a mudança no pedido e a diferença do arquivo regra a regra, calculadas pelo código.
- **lembrar**: só grava versão que passou no validador. Se a mudança não passou, o arquivo e o pedido anteriores
  continuam valendo.

**Compactação:** o histórico entra no prompt do turno mais novo para o mais velho até 4.000 caracteres. Não há LLM
resumidor: o efeito de cada turno já está no pedido e nas versões, e um resumo livre poderia perder números
(CASCADE-FIRST).

**CLI:** `python -m gobr agente --conversa NOME` abre ou retoma uma conversa; `conversas` lista as guardadas.

## 4. Avaliação

`avaliar-memoria` roda conversas roteirizadas e confere em código as saídas esperadas de cada turno, escritas à mão
antes de rodar. Três modos: **memória** (o banco é reaberto a cada turno, como um processo novo), **concatenada** (todas
as mensagens viram um pedido só) e **nenhuma** (cada mensagem é um pedido novo, o comportamento anterior). Tabelas
completas em `data/agente/avaliacao_memoria.md`. As linhas de base do conjunto original e os gabaritos são de antes das
duas últimas correções (§4.3), que só agem em turnos de mudança do modo memória; o resto é do código final.

### 4.1 Resultado

| Conjunto | Modo | Verificações certas | Sem contar "regra intacta" |
|---|---|---|---|
| original (10 conversas, 30 turnos) | memória | 87/87 | 65/65 |
| original | concatenada | 58/87 | 52/65 |
| original | nenhuma | 45/87 | 45/65 |
| novo (7 conversas, 18 turnos) | memória | 54/54 | 46/46 |
| novo | concatenada | 31/54 | 30/46 |
| novo | nenhuma | 27/54 | 27/46 |

Como ler estes números:
- **O conjunto original guiou correções.** Na 1ª rodada a memória tinha 85/87. O **novo** foi escrito depois, com código e
  prompts congelados: é a medida mais limpa.
- **"Regra intacta" favorece a memória por construção**: as linhas de base redigem o arquivo inteiro a cada turno, e uma
  regra equivalente escrita de outro jeito conta como mudada. Sem ela, a diferença diminui, mas continua.
- **São 17 conversas curtas, escritas por quem fez o código, e cada configuração rodou uma vez.** 100% aqui quer dizer que
  as verificações não acharam erro, não que o agente não erra (§4.3).

### 4.2 Contexto e tempo

| Conjunto | Modo | Maior prompt dos turnos depois do 1º (tokens, média e máximo) | Tempo médio desses turnos (s) |
|---|---|---|---|
| original | memória | 4.248 / 5.929 | 26 |
| original | concatenada | 6.750 / 14.916 | 67 |
| original | nenhuma | 5.861 / 24.887 | 37 |
| novo | memória | 4.211 / 6.171 | 28 |
| novo | concatenada | 6.275 / 12.794 | 69 |
| novo | nenhuma | 7.679 / 18.237 | 41 |

Na conversa de 7 turnos, o maior prompt ficou entre 2.303 e 5.307 tokens, sem tendência de crescer. O agente com
memória parte do arquivo pronto; as linhas de base recomeçam a cada turno.

### 4.3 O que as verificações não viram

Ler as conversas mostrou o que os números escondiam:
- **1ª rodada, bloqueio inócuo:** "não agende os inadimplentes" entrou como última regra, depois de Ativos e Inativos, e
  quase não bloqueava ninguém. Todas as verificações passavam. As linhas de base acertavam a ordem. Corrigido em código,
  e a verificação `bloqueia_antes` entrou na avaliação.
- **1ª rodada, numeração copiada:** o intérprete escreveu "4. Inadimplentes", e o validador passou a exigir o 4.
  Corrigido em código.
- **Ainda de pé:** no caso em que os inativos são divididos em dois, "há mais de 120 dias" virou a última regra, sem filtro, e pega
  também quem nunca comprou.

### 4.4 Persistência e regressão

- Com o LLM real, um processo morto com a pergunta na tela foi retomado em outro: a mesma pergunta voltou, e a resposta
  concluiu o turno.
- Os 3 gabaritos do professor seguem 3/3 no validador, em 261 s. Como na etapa anterior, isso não é a regra certa em tudo:
  o conferente deixou divergências no Maxlub e no V1Vidros.

### 4.5 Auditoria

Antes das medições relatadas aqui, uma auditoria independente do código reproduziu 12 defeitos com um LLM falso, e a medição que já rodava
foi parada e descartada. Os mais graves: citar um número nas notas ("de 14 para 15") dispensava o validador de exigi-lo; mudança que
valia para todos os segmentos era revertida; a lacuna de um pedido vazava para o seguinte; e **a própria avaliação dava
pontos ao modo com memória quando um turno falhava**, porque ele herdava o arquivo anterior. Todos foram corrigidos,
dez deles com teste automático; a soma de casos com exceção na avaliação e a retomada de turno que falha na CLI não têm
teste próprio. A lista do que mudou está em `docs/desenho_memoria.md` §7.

Testes: 192, dos quais 67 de memória (`tests/test_memory.py`), sem LLM.

## 5. Limitações

- **Avaliação pequena e de um autor só** (§4.1).
- **Perguntas sobre time e carteira** continuam no 1º pedido: nenhum exemplo do professor os dá, e a triagem não os cobre.
- **Nome do segmento:** as checagens em código casam regra e segmento pelo nome. Se o agente muda o nome, a regra não é
  julgada.
- **Mudança que não cita nenhum segmento** ("todos a cada 10 dias") desliga a proteção das outras regras naquele turno.
- **O banco cresce** de 0,4 a 0,8 MB por turno, porque o checkpointer guarda o estado a cada nó; não há limpeza
  (`SqliteSaver.prune` não está implementado na versão 3.1.3).
- **Memória de uma conversa só:** não lembra preferências do usuário entre conversas. Foi escolha: um fato velho poderia
  entrar numa regra sem ninguém notar.
- **Notas longas** do LLM continuam aparecendo, e a resposta a uma pergunta entra no pedido com o texto da pergunta.
- Só texto; a entrada por imagem continua para depois.

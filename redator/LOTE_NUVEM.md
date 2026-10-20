# Lote do redator (sessão na nuvem)

Gera as descrições de todas as regras com a estratégia adaptativa: 3 réplicas por arquivo e mais 2
onde a concordância entre elas fica abaixo de 0,8 (ou há menos de 2 candidatos válidos).
Tudo a partir da raiz do repositório; Python 3.11, só a biblioteca padrão.

## 0. Conferência

```
python -m unittest tests.test_gobr          # deve passar
python -m gobr contexto trabalho/trabalho/referencias data/contexto
python -m gobr contexto trabalho/trabalho/exemplos data/contexto_exemplos
python -m gobr entrada data/contexto data/entrada_redator
python -m gobr entrada data/contexto_exemplos data/entrada_redator
git status --short data/                    # nada deve mudar além de datas; se mudar, pare e relate
```

## 1. Rodadas

Repita até `pendentes` não listar nada:

```
python -m gobr pendentes data/candidatos_v2 data/entrada_redator --contexto data/contexto data/contexto_exemplos
```

Cada linha é `<id> <n>`: o arquivo `<id>` precisa de `n` réplicas novas. Para cada réplica, escolha o
próximo número livre `k` em `data/candidatos_v2/<id>/agente_<k>.json` (crie a pasta se faltar), de
modo que duas réplicas nunca escrevam no mesmo arquivo.

Distribua as réplicas em subagentes (`model: sonnet`), no máximo 20 ao mesmo tempo, 5 arquivos por
subagente, e nunca duas réplicas do mesmo arquivo no mesmo subagente. Prompt de cada subagente,
trocando a lista no item 2:

> Tarefa mecânica de redação. Use apenas as ferramentas Read e Write.
> 1. Leia as instruções completas em `redator/prompt_redator.md` e siga-as à risca.
> 2. Para cada par abaixo, de forma independente (não leia nenhum outro arquivo de saída), leia
>    `data/entrada_redator/<id>.json` e grave somente o objeto JSON de resposta no caminho indicado:
>    - `<id>` -> `data/candidatos_v2/<id>/agente_<k>.json`
> 3. Ao terminar, responda apenas "ok".

Use caminhos absolutos do repositório no prompt dos subagentes.

Se um arquivo continuar sem candidato válido depois de 5 réplicas, rode no máximo mais 2 e depois
siga em frente (ele fica registrado como falha).

## 2. Consolidação

```
python -m gobr consolidar data/candidatos_v2 data/descricoes --contexto data/contexto data/contexto_exemplos --prompt redator/prompt_redator.md
```

## 3. Relatório e entrega

Grave `data/descricoes/RELATORIO_LOTE.md` com: número de arquivos, réplicas geradas, candidatos
válidos/inválidos com os erros mais comuns, distribuição da concordância, arquivos com falha e a
lista dos 10 arquivos de menor concordância. Não edite código do pacote `gobr/`, o prompt ou as
entradas; se algo parecer errado neles, descreva no relatório.

Faça commit de `data/candidatos_v2/` e `data/descricoes/` e envie o branch.

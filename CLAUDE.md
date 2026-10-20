# Projeto SMA: assistente GoBR

Disciplina de Sistemas Multiagentes (UFG, 2026-2): agente LangGraph + RAG que ajuda a escrever regras
na DSL GoBR do Govendas. Etapa atual: explicações em linguagem de negócio de cada `.gobr` do corpus.
Visão geral e comandos: `README.md`. Estado da sessão: `HANDOFF.md`.

## Comandos

- Testes: `python -m unittest tests.test_gobr`
- Pacotes: `python -m gobr contexto|entrada|pendentes|consolidar|cobertura ...` (ver docstring de `gobr/__main__.py`)

## Regras

- **CASCADE-FIRST**: a semântica (cascata, alertas, números exigidos) vive em `gobr/`; o LLM só redige. Bug de significado se corrige no pacote, não no prompt.
- **PREMISE-LOG**: toda ambiguidade de semântica vira uma premissa em `docs/premissas.md`; nunca se pede a alguém para resolvê-la.
- **VERSIONED-CANDIDATES**: ao mudar a entrada do redator, gere candidatos novos em `data/candidatos_vN/` e consolide em ordem; nunca misture candidatos de entradas diferentes.
- **NO-COAUTHOR**: commits e PRs deste repositório vão sem a linha Co-Authored-By.

## Rejected

- Lark / pyparsing / ANTLR para o parser: não existe `.g4`, a cauda de cláusulas é longa e há arquivos com erros de sintaxe.
- `portion` para intervalos: LGPL, e o suporte a intervalos discretos é experimental.
- `Unidecode`: GPL. Detectores de charset: o corpus inteiro é UTF-8.
- Só LLM ou só templates: um erra a cascata, o outro produz texto robótico.
- 5 réplicas fixas por arquivo: na calibração, a divergência era sobretudo de redação; a estratégia adaptativa custa menos.
- Batch API com créditos: os US$ 250 valem só para sessões na nuvem.
- Fonte composta (`da segmentacao(x) e da carteira(y)`) como interseção: vazia por construção na regra_169 (premissa P8).
- Exigir todos os números de condições com "OU": derrubava candidatos certos. Os números exigidos vêm do pacote.

## Domain guides

| Guia | Ler quando... |
|---|---|
| `docs/premissas.md` | for mudar a semântica da cascata ou do catálogo de cláusulas |
| `docs/relatorio_explicacoes.md` | for escrever relatório ou apresentação, ou precisar dos números da etapa |
| `docs/avaliacao/*.md` | for mexer na qualidade das descrições ou reavaliar |
| `research/camada_deterministica.md`, `research/redator_llm.md` | for fazer o índice RAG, o backend Ollama ou mudar o prompt |
| `docs/manual_gobr.txt` | for precisar do significado oficial de uma cláusula GoBR |

# Projeto SMA: assistente GoBR

Disciplina de Sistemas Multiagentes (UFG, 2026-2): agente LangGraph + RAG que ajuda a escrever regras
na DSL GoBR do Govendas. Etapas: explicações de cada `.gobr`, índice delas (`gobr/index.py`) e índice do manual
(`gobr/manual.py` extrai, `gobr/manual_search.py` busca) e fluxo básico LangGraph (`gobr/agent.py`).
Visão geral e comandos: `README.md`. Estado da sessão: `HANDOFF.md`.

## Comandos

- Testes: `python -m unittest tests.test_gobr tests.test_index tests.test_manual tests.test_agent`
- Agente: `python -m gobr agente|avaliar-agente ...`; o LLM é o llama-server do PC (RTX 5060) pelo túnel `ssh -L 8080:127.0.0.1:8080 pc`
- Pacotes: `python -m gobr contexto|entrada|pendentes|consolidar|cobertura ...` (ver docstring de `gobr/__main__.py`)
- Índice: `python -m gobr indexar|buscar|avaliar-indice ...`; rode com `HF_HUB_OFFLINE=1` (modelos em cache)
- Manual: `python -m gobr manual|indexar-manual|buscar-manual|avaliar-manual ...`

## Regras

- **CASCADE-FIRST**: a semântica (cascata, alertas, números exigidos) vive em `gobr/`; o LLM só redige. Bug de significado se corrige no pacote, não no prompt.
- **PREMISE-LOG**: toda ambiguidade de semântica vira uma premissa em `docs/premissas.md`; nunca se pede a alguém para resolvê-la.
- **VERSIONED-CANDIDATES**: ao mudar a entrada do redator, gere candidatos novos em `data/candidatos_vN/` e consolide em ordem; nunca misture candidatos de entradas diferentes.
- **NO-COAUTHOR**: commits e PRs deste repositório vão sem a linha Co-Authored-By.
- **MEASURE-RETRIEVAL**: mudança no índice (chunks, pesos, modelo) só entra com `avaliar-indice` rodado e comparado com a tabela do relatório.

## Rejected

- Lark / pyparsing / ANTLR para o parser: não existe `.g4`, a cauda de cláusulas é longa e há arquivos com erros de sintaxe.
- `portion` para intervalos: LGPL, e o suporte a intervalos discretos é experimental.
- `Unidecode`: GPL. Detectores de charset: o corpus inteiro é UTF-8.
- PyMuPDF para ler o manual: AGPL-3.0; o Pedro escolheu pdfplumber (MIT) em 2026-10-25.
- `docs/manual_gobr.txt` como fonte do índice do manual: a conversão desalinha as tabelas de duas colunas.
- bge-m3 e multilingual-e5-small no índice das descrições: medidos, perdem do Qwen3-0.6B nos gabaritos. Qwen3-Embedding-4B: não cabe nos 8 GB de VRAM.
- Multi-vetor (arquivo + regra + consulta) como busca padrão das descrições: empatou ou perdeu do vetor de arquivo.
- Só LLM ou só templates: um erra a cascata, o outro produz texto robótico.
- 5 réplicas fixas por arquivo: na calibração, a divergência era sobretudo de redação; a estratégia adaptativa custa menos.
- Batch API com créditos: os US$ 250 valem só para sessões na nuvem.
- Fonte composta (`da segmentacao(x) e da carteira(y)`) como interseção: vazia por construção na regra_169 (premissa P8).
- Exigir todos os números de condições com "OU": derrubava candidatos certos. Os números exigidos vêm do pacote.
- Ollama + gemma4 como backend do fluxo: exige instalar e baixar ~7 GB, e o llama-server com o Qwen3.6-35B-A3B já roda no PC (Pedro, 2026-11-10).
- Claude API como backend do fluxo: sem chave e com custo próprio; os créditos valem só para sessões na nuvem (Pedro, 2026-11-10).
- Assinatura igual ao gabarito como critério de aprovação: o gabarito tem regras que a descrição não pede (Baixados na Receita).

## Domain guides

| Guia | Ler quando... |
|---|---|
| `docs/premissas.md` | for mudar a semântica da cascata ou do catálogo de cláusulas |
| `docs/relatorio_explicacoes.md` | for escrever relatório ou apresentação, ou precisar dos números da etapa |
| `docs/relatorio_manual.md` | for mexer na extração do PDF, nos chunks ou na busca do manual (denso, BM25, híbrido) |
| `docs/relatorio_fluxo.md`, `research/backend_llm_fluxo.md` | for mexer no grafo (`gobr/agent.py`), no prompt do agente, no backend do LLM ou na avaliação nos gabaritos |
| `docs/relatorio_indexacao.md` | for mexer no índice de embeddings, no `search` ou no modelo, ou precisar dos números de recuperação |
| `docs/avaliacao/*.md` | for mexer na qualidade das descrições ou reavaliar |
| `research/camada_deterministica.md`, `research/redator_llm.md` | for fazer o índice RAG, o backend Ollama ou mudar o prompt |
| `data/manual/secoes.json` | for precisar do significado oficial de uma cláusula GoBR (o `docs/manual_gobr.txt` desalinha as tabelas) |

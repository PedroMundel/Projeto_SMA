# Projeto SMA: assistente GoBR

Disciplina de Sistemas Multiagentes (UFG, 2026-2): agente LangGraph + RAG que ajuda a escrever regras
na DSL GoBR do Govendas. Etapas: explicações de cada `.gobr`, índice delas (`gobr/index.py`) e índice do manual
(`gobr/manual.py` extrai, `gobr/manual_search.py` busca), fluxo agêntico LangGraph (`gobr/agent.py`: triagem, ferramentas, perguntas com `interrupt`, validador e conferente) e memória da conversa (`gobr/memory.py`, `SqliteSaver`).
Visão geral e comandos: `README.md`. Estado da sessão: `HANDOFF.md`.

## Comandos

- Testes: `python -m unittest tests.test_gobr tests.test_index tests.test_manual tests.test_agent tests.test_memory`
- Agente: `python -m gobr agente|conversas|avaliar-agente|avaliar-perguntas|avaliar-memoria|conferir ...`
- LLM: llama-server local, na RTX 5060 (desde 2026-11-24, sem SSH): `E:\tools\llama.cpp-b11770\llama-server.exe -m E:\tools\models\Qwen3.6-35B-A3B-UD-IQ4_XS.gguf -ngl 999 --n-cpu-moe 30 -c 32768 -np 1 --jinja --host 127.0.0.1 --port 8080`; com ele no ar, rode o agente com `CUDA_VISIBLE_DEVICES=-1` (a VRAM está cheia)
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
- ReAct livre (o LLM poderia pular a validação) e triagem só na frente do pipeline fixo: o Pedro escolheu o agente com guardas e conferente (2026-11-17).
- Prompt para o agente perceber sozinho o dado que falta: 2 versões, 0/3 e 1/3 casos, e a 2ª reprovou o Maxlub. Quem decide é o código, pela triagem.
- Casar regra e segmento por qualquer prefixo do nome: julgava "Ativos inadimplentes" como "Ativos". Só nome igual ou "<segmento>:".
- Memória de longo prazo do usuário entre conversas, e memória só na sessão: o Pedro escolheu a conversa persistente; um fato velho entraria numa regra sem ninguém notar (2026-11-24).
- JSON próprio ou `InMemorySaver` para a memória: não retomam o `interrupt` ou não persistem; o Pedro escolheu o `SqliteSaver` (2026-11-24).

## Domain guides

| Guia | Ler quando... |
|---|---|
| `docs/premissas.md` | for mudar a semântica da cascata ou do catálogo de cláusulas |
| `docs/relatorio_explicacoes.md` | for escrever relatório ou apresentação, ou precisar dos números da etapa |
| `docs/relatorio_manual.md` | for mexer na extração do PDF, nos chunks ou na busca do manual (denso, BM25, híbrido) |
| `docs/desenho_agente.md`, `docs/relatorio_agente.md` | for mexer no grafo (`gobr/agent.py`: ferramentas, `interrupt`, conferente), nos prompts do agente ou do conferente, ou na avaliação do agente |
| `docs/desenho_memoria.md`, `docs/relatorio_memoria.md` | for mexer na memória da conversa (`gobr/memory.py`, nós `receber`, `interpretar`, `explicar`, `desfazer`, `lembrar`), nos turnos ou na retomada |
| `docs/relatorio_fluxo.md`, `research/backend_llm_fluxo.md` | for precisar da linha de base do fluxo fixo (commit `094e6b1`) ou mexer no backend do LLM |
| `docs/relatorio_indexacao.md` | for mexer no índice de embeddings, no `search` ou no modelo, ou precisar dos números de recuperação |
| `docs/avaliacao/*.md` | for mexer na qualidade das descrições ou reavaliar |
| `research/camada_deterministica.md`, `research/redator_llm.md` | for fazer o índice RAG, o backend Ollama ou mudar o prompt |
| `data/manual/secoes.json` | for precisar do significado oficial de uma cláusula GoBR (o `docs/manual_gobr.txt` desalinha as tabelas) |

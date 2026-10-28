# Relatório da etapa: indexação do manual GoBR

## 1. Objetivo

Indexar o manual da linguagem GoBR (`trabalho/trabalho/govendas-rules.pdf`, 62 páginas) para que o agente
consulte a sintaxe e as regras da linguagem ao escrever a resposta (dica 3 do enunciado), com atenção à
quebra dos chunks (dica 4).

## 2. Extração (`gobr/manual.py`, `python -m gobr manual`)

| Decisão | Alternativas consideradas | Por quê |
|---|---|---|
| Ler o **PDF**, não o texto já convertido | `docs/manual_gobr.txt` | Na conversão para texto, as tabelas de duas colunas saem desalinhadas. Na §6.1, por exemplo, a descrição de `ativos` aparece ao lado de `ativos para o vendedor`, e cada linha seguinte fica deslocada. Indexar esse texto daria às cláusulas os significados errados. |
| `pdfplumber` 0.11.10 (MIT) | PyMuPDF (AGPL-3.0, já instalado e testado) | O projeto evita bibliotecas GPL e LGPL. O Pedro escolheu o pdfplumber, que também extrai a tabela da §6.1 alinhada. |
| Classificar pelas fontes do PDF | Heurísticas sobre o texto puro | O PDF é regular. Cabeçalho de página em corpo 6, rodapé com "©" e títulos numerados em Helvetica-Bold (16, 12 ou 9,5 pt); um título que quebra em duas linhas é emendado (2.1, 4 e 6.13). Linha toda em Courier é código. A seta desenhada com o fonte Symbol sai como "fi" e vira "→". |
| Tabelas por `find_tables`, emendadas entre páginas | Tratar cada página isolada | Uma tabela sem cabeçalho logo depois de outra com o mesmo número de colunas é continuação. Uma célula vazia na 1ª coluna continua a linha anterior. Uma coluna quase vazia que o detector inventa é absorvida pela vizinha (caso da §6.11). |

Resultado: 95 seções, incluindo as de 3º nível (4.3.1, 7.3.6 etc.), em `data/manual/secoes.json`. Cada
seção traz o texto completo em Markdown, com tabelas e blocos de código.

A revisão de código derrubou uma regra da primeira versão: tratar como definição a linha que começa em
Courier e continua em Helvetica. Ela disparou 8 vezes, todas em prosa que começava com código no meio
da frase, e colava as palavras. As definições que motivaram a regra eram, na verdade, tabelas com borda
continuadas na página seguinte.

## 3. Chunks

| Tipo | Quantos | Como | Por quê |
|---|---|---|---|
| Linha de tabela | 391 | `Filtro: <cláusula>. Descrição: <significado>`, uma linha por chunk | A maior parte do manual é um catálogo de cláusulas. Uma linha é a unidade que o agente procura ("como escrevo X"). |
| Tabela de uma coluna | (incluída acima) | A lista inteira num chunk ("<<N>> anos; <<N>> meses; …") | Uma linha sozinha seria curta demais para recuperar. |
| Prosa | 72 | O texto da seção com os exemplos de código **inteiros**, partido a cada 1.500 caracteres, só entre blocos | Exemplo de código cortado ao meio não serve como modelo. |

- Todo chunk começa pelo caminho de títulos ("6 Regras para filtros de clientes > 6.2 Filtros de recência …"). É a mesma ideia de contexto usada nos chunks de regra das descrições.
- Tamanho: mediana de 56 tokens e máximo de 437 por chunk; mediana de 170 e máximo de 796 por seção (tokenizador do Qwen3).
- A busca devolve a **seção inteira** a que o chunk pertence ("pequeno para achar, grande para dar contexto").

O manual às vezes usa "..." com o sentido de "mesma condicional da linha de cima" (`recencia de
positivação global ...`). O chunk fica sem esse complemento, mas a seção devolvida tem a tabela inteira.

## 4. Busca (`gobr/manual_search.py`)

- **Denso:** Qwen3-Embedding-0.6B, o mesmo modelo do índice das descrições (`data/indice_manual/qwen3-0.6b/`, 936 KB, 463 vetores).
- **BM25:** implementação própria em numpy (k1 = 1,5, b = 0,75). Os tokens são palavras em minúsculas e sem acento. Não acrescenta dependência.
- **Híbrido:** fusão por posição (RRF, k = 60) das duas listas. Notas iguais dividem a mesma posição, e um chunk sem nenhuma palavra da consulta não ganha a parcela do BM25. Na primeira versão, os empates (centenas de chunks com nota 0) recebiam posições pela ordem no arquivo, o que dava bônus ao começo do manual.
- A nota de uma seção é a do seu melhor chunk; o top-k é de seções distintas.
- O índice guarda o hash de `chunks.jsonl` e `secoes.json` e o caminho do manual relativo a ele mesmo. Se o manual for extraído de novo, `load` recusa um índice velho.

## 5. Avaliação (`python -m gobr avaliar-manual`)

Conjunto: 48 consultas rotuladas em `data/consultas_avaliacao/manual.json`, escritas por um subagente
Sonnet que leu as seções. Cada consulta aceita de 1 a 3 seções esperadas. Conferi os rótulos de 4
consultas no texto das seções, e os 4 estavam certos.

- **necessidade (24):** pedido de negócio sem a sintaxe ("clientes que não compram com ninguém da empresa há mais de 60 dias").
- **sintaxe (12):** fragmento de cláusula meio lembrado ("nao agendar inadimplente").
- **conceito (12):** como a linguagem funciona ("um cliente já parametrizado é processado de novo pelas regras seguintes?").

Recall@1 / Recall@5 / MRR (acerto = uma das seções esperadas no top-k):

| Modo | todas (48) | necessidade (24) | sintaxe (12) | conceito (12) |
|---|---|---|---|---|
| denso | 0,625 / 0,917 / 0,741 | 0,542 / 0,875 / 0,677 | 0,583 / 1,000 / 0,757 | **0,833** / 0,917 / **0,854** |
| BM25 | **0,708** / 0,917 / 0,785 | **0,708 / 1,000 / 0,814** | 0,833 / 0,917 / 0,875 | 0,583 / 0,750 / 0,639 |
| **híbrido (padrão)** | **0,708 / 1,000 / 0,826** | 0,667 / **1,000** / 0,789 | **0,917 / 1,000 / 0,958** | 0,583 / **1,000** / 0,767 |

- O híbrido acha a seção certa no top-5 nas 48 consultas, por isso é o padrão. O agente vai ler 3 a 5 seções, então o Recall@5 pesa mais que o @1.
- Antes das correções da revisão (definições falsas e empates no RRF), o híbrido tinha 0,667 / 0,979 / 0,798.
- O BM25 vai bem em "necessidade" porque quem escreveu as consultas leu o texto do manual: mesmo pedindo paráfrase, as palavras se repetem. Com usuários reais, a vantagem do BM25 nesse tipo tende a ser menor.
- O denso ganha em "conceito", em que a pergunta e o texto usam palavras diferentes.

## 6. O manual cabe no contexto

O texto das 95 seções tem 72.509 caracteres, ou **20.254 tokens** no tokenizador do Qwen3. Isso cabe no
contexto de qualquer LLM atual, de modo que o RAG do manual não é necessário por falta de espaço. Ele se
justifica por outros motivos:

1. Levar ao agente só as 3 a 5 seções relevantes, de 170 tokens em média, em vez de 20 mil tokens por
   chamada. Custa menos e ajuda modelos locais (Ollama) com contexto curto ou que se perdem em texto longo.
2. Citar a seção exata de onde saiu a sintaxe da resposta.

Fica como alternativa medir, no fluxo LangGraph, o agente com o manual inteiro no prompt contra o agente com
RAG.

## 7. Uso

```bash
python -m gobr manual trabalho/trabalho/govendas-rules.pdf data/manual
```

```bash
python -m gobr indexar-manual data/manual data/indice_manual/qwen3-0.6b
```

```bash
python -m gobr buscar-manual data/indice_manual/qwen3-0.6b "como não agendar clientes que já estão na rota do vendedor externo" -k 3
```

```bash
python -m gobr avaliar-manual data/indice_manual/qwen3-0.6b --consultas data/consultas_avaliacao/manual.json
```

## 8. Limitações e próximos passos

1. As 48 consultas foram escritas por um LLM que leu o manual (viés lexical a favor do BM25, §5). Faltam
   consultas reais do agente; o fluxo LangGraph vai gerá-las.
2. A extração depende do layout deste PDF (fontes e corpos). Outra versão do manual pede conferir os testes
   de `tests/test_manual.py`.
3. Não comparei modelos de embedding no manual. O Qwen3-0.6B foi mantido por coerência com o índice das
   descrições.
4. Próximo: o fluxo LangGraph do agente. Ele busca exemplos parecidos (`gobr.index.search`) e a sintaxe
   no manual (`gobr.manual_search.search`), e aponta falhas com os alertas da camada determinística.

# Relatório da etapa: indexação das explicações (RAG de exemplos parecidos)

## 1. Objetivo

Indexar com embeddings as 249 descrições de `data/descricoes/` (246 do corpus e os 3 exemplos), para que
o agente, a partir da descrição de negócio do usuário, recupere as regras GoBR existentes mais parecidas
e as use como exemplo (dica 2 do enunciado). A indexação do manual GoBR (dica 3) fica para a etapa
seguinte.

## 2. Desenho

| Decisão | Alternativas consideradas | Por quê |
|---|---|---|
| Embutir a **descrição**, nunca o DSL; o `.gobr` vai como payload | Embutir o código | A consulta do usuário é texto de negócio; o código volta junto para servir de exemplo. |
| Busca pelo vetor do **arquivo** (resumo + uma linha por regra) | Multi-vetor: arquivo + regra + consulta hipotética, nota = máximo (pesquisa §3.1) | Medido (§4): o multi-vetor empata ou perde. O máximo sobre muitos chunks favorece arquivos longos, e as consultas hipotéticas de arquivos parecidos competem entre si. Os vetores de regra e de consulta continuam no índice para a ablação, e o de regra aponta a linha mais parecida do arquivo recuperado. |
| Nota = cosseno + 0,2 × Jaccard dos números (consulta × descrição) | Só cosseno; BM25 | Os arquivos do corpus quase só diferem nos números (30/45 contra 60/90 dias), e o embedding denso não os separa (pesquisa §3.3). O Jaccard leva os 3 gabaritos de 1/3 para 3/3 no 1º lugar, sem nova dependência. |
| Deduplicação por **assinatura estrutural** (tipo, tipo de fonte, quando, filtros e ações de cada regra, sem nomes) | Devolver todas as cópias | 249 arquivos têm só 189 estruturas; um grupo sozinho tem 53 cópias da "Regra Padrão". Sem deduplicar, o top-5 vira 5 cópias. A busca devolve uma por estrutura e lista as demais em `equivalentes`. O tipo de fonte (time, carteira, segmentação) entra porque muda a quem a regra se aplica; o nome do time ou da carteira não entra. |
| Nome literal da regra fora do texto embutido | Embutir o nome | O nome carrega empresa e boilerplate ("Regra Padrao da Royal Pet - Customizavel: ..."). Fica no metadado do chunk de regra. |
| Matriz em memória + cosseno em numpy | Banco vetorial (Chroma, FAISS, Qdrant) | São 2.716 vetores, 6,6 MB em disco. Um banco vetorial só acrescentaria infraestrutura. |
| `sentence-transformers` local, com modelos em cache | Ollama (`bge-m3`, recomendado na pesquisa) | O Ollama não está instalado nesta máquina, e o `sentence-transformers` 6.1.0 já estava, com GPU. O contrato (`Embedder.documents` / `queries`) aceita outro backend. |

Formato em disco, uma pasta por modelo em `data/indice/<modelo>/`: `vetores.npy` (float16, renormalizados ao carregar),
`chunks.jsonl` (tipo, arquivo, regra e texto embutido), `manifesto.json` (modelo, dimensão, contagens e,
por arquivo, assinatura, números e caminhos da descrição e do `.gobr`, relativos à raiz do repositório) e
`avaliacao.md` (tabela completa). Os caminhos supõem que o agente rode da raiz, como a CLI.

## 3. Conjuntos de avaliação

Acerto é devolver um arquivo com a **mesma assinatura** do esperado, porque duplicatas tornariam injusto
exigir o arquivo exato.

| Conjunto | n | Origem | Viés |
|---|---|---|---|
| `ouro` | 3 | Texto dos 3 PDFs do professor (V1 Vidros transcrito da imagem), sem o título com o nome da empresa (`data/consultas_avaliacao/ouro.json`) | Nenhum: texto humano, escrito antes do código. Mas n = 3. |
| `cegas` | 30 | Subagente Sonnet que leu só os `.gobr` (amostra com semente 7) e o manual, **sem ver as descrições**, em três registros: tabela, narrativa e incompleta (`data/consultas_avaliacao/cegas.json`) | Escrito por LLM a partir do código, como o redator. |
| `consulta_propria` | 747 | Consultas hipotéticas do próprio redator; só a própria sai do índice na hora da busca | Otimista: mesmo autor e mesmo pacote da descrição, e os números da consulta vêm da mesma descrição (favorece o reordenamento). |
| `consulta_estrutura` | 747 | Idem, tirando as consultas de todos os arquivos com a mesma assinatura | Só faz sentido no multi-vetor; mede o quanto as consultas das duplicatas inflam o resultado. |

## 4. Resultados (`python -m gobr avaliar-indice`)

Recall@1 / Recall@5 com o Qwen3-Embedding-0.6B. A tabela completa, com MRR e posições, está em
`data/indice/qwen3-0.6b/avaliacao.md`.

| Chunks | Peso dos números | ouro (3) | cegas (30) | consulta_propria (747) |
|---|---|---|---|---|
| arquivo | 0 | 0,333 / 0,333 | 0,800 / 0,867 | 0,506 / 0,798 |
| **arquivo** | **0,2** | **1,000 / 1,000** | **0,933 / 1,000** | **0,604 / 0,847** |
| arquivo + regra | 0,2 | 1,000 / 1,000 | 0,900 / 1,000 | 0,598 / 0,803 |
| multi-vetor | 0 | 0,000 / 0,333 | 0,667 / 0,933 | 0,434 / 0,631 |
| multi-vetor | 0,2 | 1,000 / 1,000 | 0,900 / 1,000 | 0,573 / 0,767 |

- Sem os números, o Maxlub cai para 7º e o V1 Vidros para 9º. Na frente deles ficam regras de televendas
  com as mesmas faixas (ativos, risco, inativos, prospects) e prazos diferentes.
- O peso 0,2 e o Jaccard (contra a fração dos números da consulta) foram escolhidos **nestes mesmos
  conjuntos**: não houve conjunto separado para validação. Com peso 0,1, o V1 Vidros cai para 3º. Nas
  cegas e nas hipotéticas, a diferença entre 0,1 e 0,2 fica em 0,01. O efeito grande é ligar o
  reordenamento, não o valor exato.
- `consulta_propria` fica bem abaixo de `cegas`, por dois motivos: as consultas hipotéticas são curtas e
  genéricas ("Regra padrão de frequência por situação do cliente"), e muitas estruturas diferentes dividem
  o mesmo texto de negócio. O critério de assinatura exata conta como erro um vizinho que serviria de
  exemplo. No multi-vetor, tirar também as consultas das duplicatas (`consulta_estrutura`) derruba o
  Recall@5 de 0,767 para 0,655: parte do resultado de `consulta_propria` vinha de consultas idênticas
  de arquivos de mesma estrutura.

### 4.1 Modelos de embedding

| Modelo | Licença | Em disco / dimensão / contexto | ouro R@1 | cegas R@1 / R@5 | hipotéticas R@1 / R@5 | Observação |
|---|---|---|---|---|---|---|
| **`Qwen/Qwen3-Embedding-0.6B`** (recomendado) | Apache-2.0 | 1,2 GB / 1024 / 32K | **1,000** | **0,933 / 1,000** | **0,604 / 0,847** | Já estava em cache. Indexar leva 2 min 44 s na RTX 5060. A instrução de consulta padrão (inglês, "web search") ficou melhor que uma específica do domínio (testado). |
| `intfloat/multilingual-e5-small` | MIT | 0,47 GB / 384 / 512 | 0,667 | 0,800 / 0,967 | 0,518 / 0,738 | Indexa em 22 s, mas 28 dos 249 textos de arquivo passam de 512 tokens e são truncados. No multi-vetor com números, chega a 0,967 / 1,000 nas cegas e 0,667 no ouro. |
| `BAAI/bge-m3` | MIT | 2,27 GB (`pytorch_model.bin`) / 1024 / 8K | 0,333 | 0,933 / 1,000 | 0,614 / 0,814 | Era a escolha da pesquisa (via Ollama). Indexa em 1 min 7 s. Nos gabaritos fica em 1º, 2º e 4º; só com o embedding, nenhum dos 3 entra no top-5. |

Recomendação: **Qwen3-Embedding-0.6B**. Só ele acerta os 3 gabaritos humanos. Nas cegas empata com o
bge-m3, e nas hipotéticas a diferença fica dentro de 0,04. O Qwen3-Embedding-4B (8,04 GB em fp16) não foi
testado: não cabe nos 8 GB de VRAM da RTX 5060, e os conjuntos atuais não teriam resolução para medir um
ganho.

## 5. Uso

```bash
python -m gobr indexar data/descricoes data/indice/qwen3-0.6b --contexto data/contexto data/contexto_exemplos --gobr trabalho/trabalho/referencias trabalho/trabalho/exemplos
```

```bash
python -m gobr buscar data/indice/qwen3-0.6b "Ativos: pedido nos últimos 30 dias, 14 dias. Risco: 45 dias, 7 dias. Inativos: mais de 45 dias, 14 dias" -k 3
```

```bash
python -m gobr avaliar-indice data/indice/qwen3-0.6b --consultas data/consultas_avaliacao/ouro.json data/consultas_avaliacao/cegas.json
```

No agente, `gobr.index.search` devolve, por resultado: arquivo, nota, assinatura, `regra_mais_parecida`
(chunk da regra mais próxima da consulta), `equivalentes` (arquivos de mesma estrutura) e os caminhos da
descrição e do `.gobr`.

## 6. Limitações e próximos passos

1. O conjunto humano tem só 3 consultas. As 30 cegas são de LLM; um lote de descrições escritas por
   pessoas daria uma medida mais confiável.
2. O peso dos números foi ajustado nos próprios conjuntos de teste (§4).
3. Números por extenso ("trinta dias") e unidades diferentes de dias (semanal, mensal) não entram no
   Jaccard.
4. A relevância por assinatura exata é rígida; uma medida graduada (por exemplo, distância entre
   assinaturas) premiaria vizinhos úteis.
5. Próximo: indexar o manual GoBR com atenção à quebra dos chunks (dica 3) e montar o fluxo LangGraph que
   usa `search` para buscar exemplos.

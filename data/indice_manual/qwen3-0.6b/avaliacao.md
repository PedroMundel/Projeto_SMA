modelo: Qwen/Qwen3-Embedding-0.6B

| modo | consultas | n | recall@1 | recall@5 | MRR |
|---|---|---|---|---|---|
| denso | todas | 48 | 0.625 | 0.917 | 0.741 |
| denso | conceito | 12 | 0.833 | 0.917 | 0.854 |
| denso | necessidade | 24 | 0.542 | 0.875 | 0.677 |
| denso | sintaxe | 12 | 0.583 | 1.000 | 0.757 |
| bm25 | todas | 48 | 0.708 | 0.917 | 0.785 |
| bm25 | conceito | 12 | 0.583 | 0.750 | 0.639 |
| bm25 | necessidade | 24 | 0.708 | 1.000 | 0.814 |
| bm25 | sintaxe | 12 | 0.833 | 0.917 | 0.875 |
| hibrido | todas | 48 | 0.708 | 1.000 | 0.826 |
| hibrido | conceito | 12 | 0.583 | 1.000 | 0.767 |
| hibrido | necessidade | 24 | 0.667 | 1.000 | 0.789 |
| hibrido | sintaxe | 12 | 0.917 | 1.000 | 0.958 |

modelo: Qwen/Qwen3-Embedding-0.6B

| chunks | peso dos números | consultas | n | recall@1 | recall@5 | MRR | posições |
|---|---|---|---|---|---|---|---|
| arquivo | 0.0 | ouro | 3 | 0.333 | 0.333 | 0.333 | 1 - - |
| arquivo | 0.0 | cegas | 30 | 0.800 | 0.867 | 0.828 | 1 1 1 1 1 1 1 1 1 1 1 - 1 - 1 1 1 - 1 1 1 2 1 1 1 - 1 1 3 1 |
| arquivo | 0.0 | consulta_propria | 747 | 0.506 | 0.798 | 0.606 |  |
| arquivo | 0.2 | ouro | 3 | 1.000 | 1.000 | 1.000 | 1 1 1 |
| arquivo | 0.2 | cegas | 30 | 0.933 | 1.000 | 0.967 | 1 1 1 1 1 1 1 1 1 1 1 2 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2 1 |
| arquivo | 0.2 | consulta_propria | 747 | 0.604 | 0.847 | 0.689 |  |
| arquivo+regra | 0.0 | ouro | 3 | 0.000 | 0.333 | 0.167 | 2 - - |
| arquivo+regra | 0.0 | cegas | 30 | 0.700 | 0.867 | 0.756 | 1 1 1 1 4 1 1 1 1 1 1 - 1 - 1 1 3 - 1 1 1 2 1 1 1 - 1 4 3 1 |
| arquivo+regra | 0.0 | consulta_propria | 747 | 0.490 | 0.724 | 0.576 |  |
| arquivo+regra | 0.2 | ouro | 3 | 1.000 | 1.000 | 1.000 | 1 1 1 |
| arquivo+regra | 0.2 | cegas | 30 | 0.900 | 1.000 | 0.942 | 1 1 1 1 4 1 1 1 1 1 1 2 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2 1 |
| arquivo+regra | 0.2 | consulta_propria | 747 | 0.598 | 0.803 | 0.676 |  |
| multi-vetor | 0.0 | ouro | 3 | 0.000 | 0.333 | 0.167 | 2 - - |
| multi-vetor | 0.0 | cegas | 30 | 0.667 | 0.933 | 0.779 | 1 1 1 1 3 1 1 1 2 1 1 - 1 1 1 3 1 2 1 1 2 1 1 2 1 - 1 5 2 1 |
| multi-vetor | 0.0 | consulta_propria | 747 | 0.434 | 0.631 | 0.506 |  |
| multi-vetor | 0.0 | consulta_estrutura | 747 | 0.285 | 0.503 | 0.365 |  |
| multi-vetor | 0.2 | ouro | 3 | 1.000 | 1.000 | 1.000 | 1 1 1 |
| multi-vetor | 0.2 | cegas | 30 | 0.900 | 1.000 | 0.944 | 1 1 1 1 3 1 1 1 2 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2 1 |
| multi-vetor | 0.2 | consulta_propria | 747 | 0.573 | 0.767 | 0.647 |  |
| multi-vetor | 0.2 | consulta_estrutura | 747 | 0.426 | 0.655 | 0.510 |  |

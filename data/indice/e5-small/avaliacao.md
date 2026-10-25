modelo: intfloat/multilingual-e5-small

| chunks | peso dos números | consultas | n | recall@1 | recall@5 | MRR | posições |
|---|---|---|---|---|---|---|---|
| arquivo | 0.0 | ouro | 3 | 0.000 | 0.333 | 0.083 | - 4 - |
| arquivo | 0.0 | cegas | 30 | 0.533 | 0.767 | 0.631 | 1 1 1 1 - 2 2 1 1 1 2 2 - - 1 3 - 1 1 1 1 - - 1 1 - 1 4 3 1 |
| arquivo | 0.0 | consulta_propria | 747 | 0.436 | 0.681 | 0.523 |  |
| arquivo | 0.2 | ouro | 3 | 0.667 | 1.000 | 0.750 | 1 1 4 |
| arquivo | 0.2 | cegas | 30 | 0.800 | 0.967 | 0.878 | 1 1 1 1 - 2 1 1 1 1 2 1 1 2 1 1 3 1 1 1 1 1 1 1 1 1 1 1 2 1 |
| arquivo | 0.2 | consulta_propria | 747 | 0.518 | 0.738 | 0.596 |  |
| arquivo+regra | 0.0 | ouro | 3 | 0.000 | 0.333 | 0.083 | - 4 - |
| arquivo+regra | 0.0 | cegas | 30 | 0.500 | 0.767 | 0.614 | 1 1 1 2 - 1 2 1 1 1 2 2 - - 1 4 - 1 1 2 1 - - 1 1 - 1 3 3 1 |
| arquivo+regra | 0.0 | consulta_propria | 747 | 0.436 | 0.720 | 0.547 |  |
| arquivo+regra | 0.2 | ouro | 3 | 0.667 | 1.000 | 0.750 | 1 1 4 |
| arquivo+regra | 0.2 | cegas | 30 | 0.767 | 0.967 | 0.861 | 1 1 1 2 - 1 1 1 1 1 2 1 1 2 1 1 3 1 1 2 1 1 1 1 1 1 1 1 2 1 |
| arquivo+regra | 0.2 | consulta_propria | 747 | 0.515 | 0.767 | 0.613 |  |
| multi-vetor | 0.0 | ouro | 3 | 0.000 | 0.333 | 0.083 | - 4 - |
| multi-vetor | 0.0 | cegas | 30 | 0.700 | 0.867 | 0.772 | 1 1 1 1 1 1 1 1 1 1 1 3 - 1 1 - 1 2 1 1 2 1 - 1 1 3 1 - 2 1 |
| multi-vetor | 0.0 | consulta_propria | 747 | 0.304 | 0.391 | 0.337 |  |
| multi-vetor | 0.0 | consulta_estrutura | 747 | 0.054 | 0.126 | 0.080 |  |
| multi-vetor | 0.2 | ouro | 3 | 0.667 | 1.000 | 0.750 | 1 1 4 |
| multi-vetor | 0.2 | cegas | 30 | 0.967 | 1.000 | 0.983 | 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2 1 |
| multi-vetor | 0.2 | consulta_propria | 747 | 0.479 | 0.628 | 0.536 |  |
| multi-vetor | 0.2 | consulta_estrutura | 747 | 0.249 | 0.396 | 0.304 |  |

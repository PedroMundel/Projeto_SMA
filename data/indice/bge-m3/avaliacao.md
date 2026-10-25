modelo: BAAI/bge-m3

| chunks | peso dos números | consultas | n | recall@1 | recall@5 | MRR | posições |
|---|---|---|---|---|---|---|---|
| arquivo | 0.0 | ouro | 3 | 0.000 | 0.000 | 0.000 | - - - |
| arquivo | 0.0 | cegas | 30 | 0.600 | 0.800 | 0.686 | 1 1 1 1 1 1 - 1 1 - 1 2 2 4 1 1 2 - 1 1 3 - - - 1 1 1 1 2 1 |
| arquivo | 0.0 | consulta_propria | 747 | 0.467 | 0.710 | 0.562 |  |
| arquivo | 0.2 | ouro | 3 | 0.333 | 1.000 | 0.583 | 1 2 4 |
| arquivo | 0.2 | cegas | 30 | 0.933 | 1.000 | 0.967 | 1 1 1 1 1 1 1 1 1 1 1 1 1 2 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2 1 |
| arquivo | 0.2 | consulta_propria | 747 | 0.614 | 0.814 | 0.693 |  |
| arquivo+regra | 0.0 | ouro | 3 | 0.000 | 0.000 | 0.000 | - - - |
| arquivo+regra | 0.0 | cegas | 30 | 0.533 | 0.867 | 0.666 | 1 1 1 1 2 1 5 1 1 2 1 2 2 4 1 1 5 - 1 1 - - - 2 1 3 1 1 2 1 |
| arquivo+regra | 0.0 | consulta_propria | 747 | 0.427 | 0.699 | 0.524 |  |
| arquivo+regra | 0.2 | ouro | 3 | 0.667 | 0.667 | 0.667 | 1 1 - |
| arquivo+regra | 0.2 | cegas | 30 | 0.867 | 1.000 | 0.933 | 1 1 1 1 2 1 1 1 1 1 1 1 1 2 1 1 2 1 1 1 1 1 1 1 1 1 1 1 2 1 |
| arquivo+regra | 0.2 | consulta_propria | 747 | 0.600 | 0.811 | 0.679 |  |
| multi-vetor | 0.0 | ouro | 3 | 0.000 | 0.000 | 0.000 | - - - |
| multi-vetor | 0.0 | cegas | 30 | 0.633 | 0.933 | 0.758 | 1 1 1 1 3 1 1 1 1 2 1 2 1 1 1 1 2 - 1 1 4 1 - 3 3 2 1 1 2 1 |
| multi-vetor | 0.0 | consulta_propria | 747 | 0.316 | 0.415 | 0.349 |  |
| multi-vetor | 0.0 | consulta_estrutura | 747 | 0.159 | 0.261 | 0.194 |  |
| multi-vetor | 0.2 | ouro | 3 | 0.667 | 0.667 | 0.667 | 1 1 - |
| multi-vetor | 0.2 | cegas | 30 | 0.933 | 1.000 | 0.961 | 1 1 1 1 3 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2 1 |
| multi-vetor | 0.2 | consulta_propria | 747 | 0.434 | 0.586 | 0.489 |  |
| multi-vetor | 0.2 | consulta_estrutura | 747 | 0.269 | 0.424 | 0.325 |  |

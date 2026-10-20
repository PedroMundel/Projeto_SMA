# regra_142.gobr

Regra de agendamento por curva do cliente com a empresa para três times individuais (Yara, Lúcia e Wanderson), cada um com frequências próprias para as curvas A, B, C e para clientes sem curva. Os demais vendedores seguem regras por ramo de atividade (hospitais e clínicas, distribuidoras, farmácias) e, para os outros ramos, por clientes ativos e inativos. Bloqueiam a agenda os inadimplentes e os ramos de atividade 005, 006 e 100. A regra final atende os clientes inativos dos demais ramos.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Curva A (Yara) | Clientes curva A com a empresa | 3 dias | Time Yara |
| Curva B (Yara) | Clientes curva B com a empresa | 7 dias | Time Yara |
| Curva C (Yara) | Clientes curva C com a empresa | 14 dias | Time Yara |
| Sem curva (Yara) | Clientes fora das curvas A, B e C com a empresa | 14 dias | Time Yara |
| Curva A (Lúcia) | Clientes curva A com a empresa | 2 dias | Time Lúcia |
| Curva B (Lúcia) | Clientes curva B com a empresa | 7 dias | Time Lúcia |
| Curva C (Lúcia) | Clientes curva C com a empresa | 14 dias | Time Lúcia |
| Sem curva (Lúcia) | Clientes fora das curvas A, B e C com a empresa | 7 dias | Time Lúcia |
| Curva A (Wanderson) | Clientes curva A com a empresa | 4 dias | Time Wanderson |
| Curva B (Wanderson) | Clientes curva B com a empresa | 7 dias | Time Wanderson |
| Curva C (Wanderson) | Clientes curva C com a empresa | 9 dias | Time Wanderson |
| Sem curva (Wanderson) | Clientes fora das curvas A, B e C com a empresa | 14 dias | Time Wanderson |
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar | Time todos, exceto Yara, Lúcia e Wanderson |
| Hospitais e Clínicas | Clientes dos ramos de atividade 001 e 002 | 14 dias |  |
| Distribuidoras | Clientes do ramo de atividade 003 | 7 dias |  |
| Farmácias | Clientes do ramo de atividade 004 | 21 dias |  |
| Bloqueio: fornecedores, órgãos públicos e representantes | Clientes dos ramos de atividade 005, 006 e 100 | Não agendar |  |
| Demais ramos: ativos | Clientes de ramos de atividade fora de 001, 002, 003, 004, 005, 006 e mais 1, ativos para o vendedor | 7 dias |  |
| Demais ramos: inativos | Clientes de ramos de atividade fora de 001, 002, 003, 004, 005, 006 e mais 1, não ativos para o vendedor | 15 dias | Regra final: vale para quem sobrou das anteriores |

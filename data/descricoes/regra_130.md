# regra_130.gobr

Regra padrão de frequência para dois times: o interno (televendas) e o externo (campo). No time interno, pessoas físicas e inativos inadimplentes não são agendados; pessoas jurídicas ativas seguem a cada 7 dias, inativas adimplentes a cada 15 dias e sem compra a cada 20 dias. No time externo, ativos são visitados a cada 7 dias e os demais a cada 15 dias, com parametrização fixa.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: pessoa física | Clientes pessoa física | Não agendar |  |
| Ativos (interno) | Clientes pessoa jurídica ou sem tipo de pessoa definido, ativos para o vendedor | 7 dias |  |
| Inativos adimplentes (interno) | Clientes adimplentes, pessoa jurídica ou sem tipo de pessoa definido, inativos para o vendedor | 15 dias |  |
| Bloqueio: inativos inadimplentes | Clientes inadimplentes, pessoa jurídica ou sem tipo de pessoa definido, inativos para o vendedor | Não agendar |  |
| Bloqueio: sem compra e pessoa física | Clientes pessoa física sem vendas para o vendedor | Não agendar | Nunca é aplicada: todos esses clientes já foram tratados antes |
| Sem compra, pessoa jurídica (interno) | Clientes pessoa jurídica sem vendas para o vendedor | 20 dias |  |
| Ativos (externo) | Clientes ativos para o vendedor | 7 dias | Parametrização fixa: frequência e dias rígidos para o gerador de agendas |
| Inativos (externo) | Clientes não ativos para o vendedor | 15 dias | Parametrização fixa: frequência e dias rígidos para o gerador de agendas |

## Pontos de atenção

- A regra 'Não agendar clientes sem compra e CPF (Televendas)' nunca é aplicada: todos os clientes dela já são tratados pela regra 'Não agendar clientes CPF (Televendas)'.
- O nome da regra 'Frequencia de 14 dias para clientes inativos (campo)' fala em 14 dias, mas a regra usa outro valor (15 dias).
- Todos os clientes do time interno não se enquadram em nenhuma regra e ficam sem parametrização.

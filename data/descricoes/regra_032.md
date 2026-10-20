# regra_032.gobr

Regra de agendamento do time de televendas, dividida em duas carteiras fixas por UF: sul_sudeste_centrooeste e norte_nordeste. Dentro de cada carteira, os clientes são separados por ramo (Matcon, Ferragista, Agropecuária e Home Center; EPI e Licitação; Atacado; Corporativo/Consumidor), por situação de compra (ativos, pré-inativos e inativos) e por curva A, B e C, conforme o faturamento médio mensal no ano com a empresa. No Sul, Sudeste e Centro-Oeste os ativos compraram nos últimos 120 dias e os inativos estão há mais de 150 dias sem comprar; no Norte e Nordeste esses limites são 150 e 180 dias. Prospects têm frequência de 14 dias. Não são agendados os baixados na Receita e, na regra final, os clientes que não se enquadram nas faixas.

## Carteiras

| Carteira | Descrição |
|---|---|
| sul_sudeste_centrooeste | Carteira fixa dos vendedores de televendas, filtrada por UF (DF, ES, GO, MG, MS, MT e mais 5) |
| norte_nordeste | Carteira fixa dos vendedores de televendas, filtrada por UF (AC, AL, AM, AP, BA, CE e mais 10) |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: baixados na Receita | Clientes com situação baixada na Receita Federal | Não agendar | Vale para todo o time televendas |
| Prospects | Clientes que nunca compraram com qualquer vendedor da empresa | 14 dias | Carteiras sul_sudeste_centrooeste e norte_nordeste |
| Ativos A - Matcon/Ferragista/Agro/Home Center (S/SE/CO) | Clientes de Matcon, Ferragista, Agropecuária e Home Center que compraram nos últimos 120 dias, com faturamento médio mensal acima de R$ 25000 | 14 dias | Carteira sul_sudeste_centrooeste |
| Ativos B - Matcon/Ferragista/Agro/Home Center (S/SE/CO) | Clientes de Matcon, Ferragista, Agropecuária e Home Center que compraram nos últimos 120 dias, com faturamento médio mensal entre R$ 10000 e R$ 25000 | 21 dias | Carteira sul_sudeste_centrooeste |
| Ativos C - Matcon/Ferragista/Agro/Home Center (S/SE/CO) | Clientes de Matcon, Ferragista, Agropecuária e Home Center que compraram nos últimos 120 dias, com faturamento médio mensal até R$ 10000 | 28 dias | Carteira sul_sudeste_centrooeste |
| Pré-inativos A - Matcon/Ferragista/Agro/Home Center (S/SE/CO) | Clientes de Matcon, Ferragista, Agropecuária e Home Center que compraram nos últimos 150 dias, mas estão há mais de 120 dias sem comprar, com faturamento médio mensal acima de R$ 25000 | 14 dias | Carteira sul_sudeste_centrooeste |
| Pré-inativos B - Matcon/Ferragista/Agro/Home Center (S/SE/CO) | Clientes de Matcon, Ferragista, Agropecuária e Home Center que compraram nos últimos 150 dias, mas estão há mais de 120 dias sem comprar, com faturamento médio mensal entre R$ 10000 e R$ 25000 | 14 dias | Carteira sul_sudeste_centrooeste |
| Pré-inativos C - Matcon/Ferragista/Agro/Home Center (S/SE/CO) | Clientes de Matcon, Ferragista, Agropecuária e Home Center que compraram nos últimos 150 dias, mas estão há mais de 120 dias sem comprar, com faturamento médio mensal até R$ 10000 | 14 dias | Carteira sul_sudeste_centrooeste. Exige também compra no grupo de vendedores nos últimos 150 dias |
| Inativos A - Matcon/Ferragista/Agro/Home Center (S/SE/CO) | Clientes de Matcon, Ferragista, Agropecuária e Home Center que estão há mais de 150 dias sem comprar, com faturamento médio mensal acima de R$ 25000 | 14 dias | Carteira sul_sudeste_centrooeste |
| Inativos B - Matcon/Ferragista/Agro/Home Center (S/SE/CO) | Clientes de Matcon, Ferragista, Agropecuária e Home Center que estão há mais de 150 dias sem comprar, com faturamento médio mensal entre R$ 10000 e R$ 25000 | 14 dias | Carteira sul_sudeste_centrooeste |
| Inativos C - Matcon/Ferragista/Agro/Home Center (S/SE/CO) | Clientes de Matcon, Ferragista, Agropecuária e Home Center com faturamento médio mensal até R$ 10000 que estão há mais de 150 dias sem comprar | 14 dias | Também entram os que estão entre 120 e 150 dias sem comprar e nunca compraram, ou não compram há mais de 150 dias, no grupo de vendedores |
| Ativos A - EPI/Licitação (S/SE/CO) | Clientes de EPI e Licitação que compraram nos últimos 120 dias, com faturamento médio mensal acima de R$ 25000 | 14 dias | Carteira sul_sudeste_centrooeste |
| Ativos B - EPI/Licitação (S/SE/CO) | Clientes de EPI e Licitação que compraram nos últimos 120 dias, com faturamento médio mensal entre R$ 10000 e R$ 25000 | 21 dias | Carteira sul_sudeste_centrooeste |
| Ativos C - EPI/Licitação (S/SE/CO) | Clientes de EPI e Licitação que compraram nos últimos 120 dias, com faturamento médio mensal até R$ 10000 | 28 dias | Carteira sul_sudeste_centrooeste |
| Pré-inativos A - EPI/Licitação (S/SE/CO) | Clientes de EPI e Licitação que compraram nos últimos 150 dias, mas estão há mais de 120 dias sem comprar, com faturamento médio mensal acima de R$ 25000 | 14 dias | Carteira sul_sudeste_centrooeste |
| Pré-inativos B - EPI/Licitação (S/SE/CO) | Clientes de EPI e Licitação que compraram nos últimos 150 dias, mas estão há mais de 120 dias sem comprar, com faturamento médio mensal entre R$ 10000 e R$ 25000 | 14 dias | Carteira sul_sudeste_centrooeste |
| Pré-inativos C - EPI/Licitação (S/SE/CO) | Clientes de EPI e Licitação que compraram nos últimos 150 dias, mas estão há mais de 120 dias sem comprar, com faturamento médio mensal até R$ 10000 | 14 dias | Carteira sul_sudeste_centrooeste |
| Inativos A - EPI/Licitação (S/SE/CO) | Clientes de EPI e Licitação que estão há mais de 150 dias sem comprar, com faturamento médio mensal acima de R$ 25000 | 14 dias | Carteira sul_sudeste_centrooeste |
| Inativos B - EPI/Licitação (S/SE/CO) | Clientes de EPI e Licitação que estão há mais de 150 dias sem comprar, com faturamento médio mensal entre R$ 10000 e R$ 25000 | 14 dias | Carteira sul_sudeste_centrooeste |
| Inativos C - EPI/Licitação (S/SE/CO) | Clientes de EPI e Licitação que estão há mais de 150 dias sem comprar, com faturamento médio mensal até R$ 10000 | 14 dias | Carteira sul_sudeste_centrooeste |
| Ativos A - Atacado/Distribuidores (S/SE/CO) | Clientes do ramo Atacado que compraram nos últimos 120 dias, com faturamento médio mensal acima de R$ 50000 | 10 dias | Carteira sul_sudeste_centrooeste |
| Ativos B - Atacado/Distribuidores (S/SE/CO) | Clientes do ramo Atacado que compraram nos últimos 120 dias, com faturamento médio mensal entre R$ 25000 e R$ 50000 | 14 dias | Carteira sul_sudeste_centrooeste |
| Ativos C - Atacado/Distribuidores (S/SE/CO) | Clientes do ramo Atacado que compraram nos últimos 120 dias, com faturamento médio mensal até R$ 25000 | 21 dias | Carteira sul_sudeste_centrooeste |
| Pré-inativos A - Atacado/Distribuidores (S/SE/CO) | Clientes do ramo Atacado que compraram nos últimos 150 dias, mas estão há mais de 120 dias sem comprar, com faturamento médio mensal acima de R$ 50000 | 7 dias | Carteira sul_sudeste_centrooeste |
| Pré-inativos B - Atacado/Distribuidores (S/SE/CO) | Clientes do ramo Atacado que compraram nos últimos 150 dias, mas estão há mais de 120 dias sem comprar, com faturamento médio mensal entre R$ 25000 e R$ 50000 | 10 dias | Carteira sul_sudeste_centrooeste |
| Pré-inativos C - Atacado/Distribuidores (S/SE/CO) | Clientes do ramo Atacado que compraram nos últimos 150 dias, mas estão há mais de 120 dias sem comprar, com faturamento médio mensal até R$ 25000 | 14 dias | Carteira sul_sudeste_centrooeste |
| Inativos A - Atacado/Distribuidores (S/SE/CO) | Clientes do ramo Atacado que estão há mais de 150 dias sem comprar, com faturamento médio mensal acima de R$ 50000 | 10 dias | Carteira sul_sudeste_centrooeste |
| Inativos B - Atacado/Distribuidores (S/SE/CO) | Clientes do ramo Atacado que estão há mais de 150 dias sem comprar, com faturamento médio mensal entre R$ 25000 e R$ 50000 | 10 dias | Carteira sul_sudeste_centrooeste |
| Inativos C - Atacado/Distribuidores (S/SE/CO) | Clientes do ramo Atacado que estão há mais de 150 dias sem comprar, com faturamento médio mensal até R$ 25000 | 21 dias | Carteira sul_sudeste_centrooeste |
| Ativos A - Corporativo/Consumidor (S/SE/CO) | Clientes do ramo CONS. FINAL que compraram nos últimos 120 dias, com faturamento médio mensal acima de R$ 15000 | 28 dias | Carteira sul_sudeste_centrooeste |
| Ativos B - Corporativo/Consumidor (S/SE/CO) | Clientes do ramo CONS. FINAL que compraram nos últimos 120 dias, com faturamento médio mensal entre R$ 10000 e R$ 15000 | 28 dias | Carteira sul_sudeste_centrooeste |
| Ativos C - Corporativo/Consumidor (S/SE/CO) | Clientes do ramo CONS. FINAL que compraram nos últimos 120 dias, com faturamento médio mensal até R$ 10000 | 28 dias | Carteira sul_sudeste_centrooeste |
| Pré-inativos A - Corporativo/Consumidor (S/SE/CO) | Clientes do ramo CONS. FINAL que compraram nos últimos 150 dias, mas estão há mais de 120 dias sem comprar, com faturamento médio mensal acima de R$ 15000 | 14 dias | Carteira sul_sudeste_centrooeste |
| Pré-inativos B - Corporativo/Consumidor (S/SE/CO) | Clientes do ramo CONS. FINAL que compraram nos últimos 150 dias, mas estão há mais de 120 dias sem comprar, com faturamento médio mensal entre R$ 10000 e R$ 15000 | 14 dias | Carteira sul_sudeste_centrooeste |
| Pré-inativos C - Corporativo/Consumidor (S/SE/CO) | Clientes do ramo CONS. FINAL que compraram nos últimos 150 dias, mas estão há mais de 120 dias sem comprar, com faturamento médio mensal até R$ 10000 | 14 dias | Carteira sul_sudeste_centrooeste |
| Inativos A - Corporativo/Consumidor (S/SE/CO) | Clientes do ramo CONS. FINAL que estão há mais de 150 dias sem comprar, com faturamento médio mensal acima de R$ 15000 | 28 dias | Carteira sul_sudeste_centrooeste |
| Inativos B - Corporativo/Consumidor (S/SE/CO) | Clientes do ramo CONS. FINAL que estão há mais de 150 dias sem comprar, com faturamento médio mensal entre R$ 10000 e R$ 15000 | 28 dias | Carteira sul_sudeste_centrooeste |
| Inativos C - Corporativo/Consumidor (S/SE/CO) | Clientes do ramo CONS. FINAL que estão há mais de 150 dias sem comprar, com faturamento médio mensal até R$ 10000 | 28 dias | Carteira sul_sudeste_centrooeste |
| Ativos A - Matcon/Ferragista/Agro/Home Center (N/NE) | Clientes de Matcon, Ferragista, Agropecuária e Home Center que compraram nos últimos 150 dias, com faturamento médio mensal acima de R$ 25000 | 14 dias | Carteira norte_nordeste |
| Ativos B - Matcon/Ferragista/Agro/Home Center (N/NE) | Clientes de Matcon, Ferragista, Agropecuária e Home Center que compraram nos últimos 150 dias, com faturamento médio mensal entre R$ 10000 e R$ 25000 | 21 dias | Carteira norte_nordeste |
| Ativos C - Matcon/Ferragista/Agro/Home Center (N/NE) | Clientes de Matcon, Ferragista, Agropecuária e Home Center que compraram nos últimos 150 dias, com faturamento médio mensal até R$ 10000 | 28 dias | Carteira norte_nordeste |
| Pré-inativos A - Matcon/Ferragista/Agro/Home Center (N/NE) | Clientes de Matcon, Ferragista, Agropecuária e Home Center que compraram nos últimos 180 dias, mas estão há mais de 150 dias sem comprar, com faturamento médio mensal acima de R$ 25000 | 14 dias | Carteira norte_nordeste |
| Pré-inativos B - Matcon/Ferragista/Agro/Home Center (N/NE) | Clientes de Matcon, Ferragista, Agropecuária e Home Center que compraram nos últimos 180 dias, mas estão há mais de 150 dias sem comprar, com faturamento médio mensal entre R$ 10000 e R$ 25000 | 14 dias | Carteira norte_nordeste |
| Pré-inativos C - Matcon/Ferragista/Agro/Home Center (N/NE) | Clientes de Matcon, Ferragista, Agropecuária e Home Center que compraram nos últimos 180 dias, mas estão há mais de 150 dias sem comprar, com faturamento médio mensal até R$ 10000 | 14 dias | Carteira norte_nordeste |
| Inativos A - Matcon/Ferragista/Agro/Home Center (N/NE) | Clientes de Matcon, Ferragista, Agropecuária e Home Center que estão há mais de 180 dias sem comprar, com faturamento médio mensal acima de R$ 25000 | 14 dias | Carteira norte_nordeste |
| Inativos B - Matcon/Ferragista/Agro/Home Center (N/NE) | Clientes de Matcon, Ferragista, Agropecuária e Home Center que estão há mais de 180 dias sem comprar, com faturamento médio mensal entre R$ 10000 e R$ 25000 | 14 dias | Carteira norte_nordeste |
| Inativos C - Matcon/Ferragista/Agro/Home Center (N/NE) | Clientes de Matcon, Ferragista, Agropecuária e Home Center que estão há mais de 180 dias sem comprar, com faturamento médio mensal até R$ 10000 | 14 dias | Carteira norte_nordeste |
| Ativos A - EPI/Licitação (N/NE) | Clientes de EPI e Licitação que compraram nos últimos 150 dias, com faturamento médio mensal acima de R$ 25000 | 14 dias | Carteira norte_nordeste |
| Ativos B - EPI/Licitação (N/NE) | Clientes de EPI e Licitação que compraram nos últimos 150 dias, com faturamento médio mensal entre R$ 10000 e R$ 25000 | 21 dias | Carteira norte_nordeste |
| Ativos C - EPI/Licitação (N/NE) | Clientes de EPI e Licitação que compraram nos últimos 150 dias, com faturamento médio mensal até R$ 10000 | 28 dias | Carteira norte_nordeste |
| Pré-inativos A - EPI/Licitação (N/NE) | Clientes de EPI e Licitação que compraram nos últimos 180 dias, mas estão há mais de 150 dias sem comprar, com faturamento médio mensal acima de R$ 25000 | 14 dias | Carteira norte_nordeste |
| Pré-inativos B - EPI/Licitação (N/NE) | Clientes de EPI e Licitação que compraram nos últimos 180 dias, mas estão há mais de 150 dias sem comprar, com faturamento médio mensal entre R$ 10000 e R$ 25000 | 14 dias | Carteira norte_nordeste |
| Pré-inativos C - EPI/Licitação (N/NE) | Clientes de EPI e Licitação que compraram nos últimos 180 dias, mas estão há mais de 150 dias sem comprar, com faturamento médio mensal até R$ 10000 | 14 dias | Carteira norte_nordeste |
| Inativos A - EPI/Licitação (N/NE) | Clientes de EPI e Licitação que estão há mais de 180 dias sem comprar, com faturamento médio mensal acima de R$ 25000 | 14 dias | Carteira norte_nordeste |
| Inativos B - EPI/Licitação (N/NE) | Clientes de EPI e Licitação que estão há mais de 180 dias sem comprar, com faturamento médio mensal entre R$ 10000 e R$ 25000 | 14 dias | Carteira norte_nordeste |
| Inativos C - EPI/Licitação (N/NE) | Clientes de EPI e Licitação que estão há mais de 180 dias sem comprar, com faturamento médio mensal até R$ 10000 | 14 dias | Carteira norte_nordeste |
| Ativos A - Atacado/Distribuidores (N/NE) | Clientes do ramo Atacado que compraram nos últimos 150 dias, com faturamento médio mensal acima de R$ 50000 | 10 dias | Carteira norte_nordeste |
| Ativos B - Atacado/Distribuidores (N/NE) | Clientes do ramo Atacado que compraram nos últimos 150 dias, com faturamento médio mensal entre R$ 25000 e R$ 50000 | 14 dias | Carteira norte_nordeste |
| Ativos C - Atacado/Distribuidores (N/NE) | Clientes do ramo Atacado que compraram nos últimos 150 dias, com faturamento médio mensal até R$ 25000 | 21 dias | Carteira norte_nordeste |
| Pré-inativos A - Atacado/Distribuidores (N/NE) | Clientes do ramo Atacado que compraram nos últimos 180 dias, mas estão há mais de 150 dias sem comprar, com faturamento médio mensal acima de R$ 50000 | 7 dias | Carteira norte_nordeste |
| Pré-inativos B - Atacado/Distribuidores (N/NE) | Clientes do ramo Atacado que compraram nos últimos 180 dias, mas estão há mais de 150 dias sem comprar, com faturamento médio mensal entre R$ 25000 e R$ 50000 | 10 dias | Carteira norte_nordeste |
| Pré-inativos C - Atacado/Distribuidores (N/NE) | Clientes do ramo Atacado que compraram nos últimos 180 dias, mas estão há mais de 150 dias sem comprar, com faturamento médio mensal até R$ 25000 | 14 dias | Carteira norte_nordeste |
| Inativos A - Atacado/Distribuidores (N/NE) | Clientes do ramo Atacado que estão há mais de 180 dias sem comprar, com faturamento médio mensal acima de R$ 50000 | 10 dias | Carteira norte_nordeste |
| Inativos B - Atacado/Distribuidores (N/NE) | Clientes do ramo Atacado que estão há mais de 180 dias sem comprar, com faturamento médio mensal entre R$ 25000 e R$ 50000 | 10 dias | Carteira norte_nordeste |
| Inativos C - Atacado/Distribuidores (N/NE) | Clientes do ramo Atacado que estão há mais de 180 dias sem comprar, com faturamento médio mensal até R$ 25000 | 21 dias | Carteira norte_nordeste |
| Ativos A - Corporativo/Consumidor (N/NE) | Clientes do ramo CONS. FINAL que compraram nos últimos 150 dias, com faturamento médio mensal acima de R$ 15000 | 28 dias | Carteira norte_nordeste |
| Ativos B - Corporativo/Consumidor (N/NE) | Clientes do ramo CONS. FINAL que compraram nos últimos 150 dias, com faturamento médio mensal entre R$ 10000 e R$ 15000 | 28 dias | Carteira norte_nordeste |
| Ativos C - Corporativo/Consumidor (N/NE) | Clientes do ramo CONS. FINAL que compraram nos últimos 150 dias, com faturamento médio mensal até R$ 10000 | 28 dias | Carteira norte_nordeste |
| Pré-inativos A - Corporativo/Consumidor (N/NE) | Clientes do ramo CONS. FINAL que compraram nos últimos 180 dias, mas estão há mais de 150 dias sem comprar, com faturamento médio mensal acima de R$ 15000 | 14 dias | Carteira norte_nordeste |
| Pré-inativos B - Corporativo/Consumidor (N/NE) | Clientes do ramo CONS. FINAL que compraram nos últimos 180 dias, mas estão há mais de 150 dias sem comprar, com faturamento médio mensal entre R$ 10000 e R$ 15000 | 14 dias | Carteira norte_nordeste |
| Pré-inativos C - Corporativo/Consumidor (N/NE) | Clientes do ramo CONS. FINAL que compraram nos últimos 180 dias, mas estão há mais de 150 dias sem comprar, com faturamento médio mensal até R$ 10000 | 14 dias | Carteira norte_nordeste |
| Inativos A - Corporativo/Consumidor (N/NE) | Clientes do ramo CONS. FINAL que estão há mais de 180 dias sem comprar, com faturamento médio mensal acima de R$ 15000 | 28 dias | Carteira norte_nordeste |
| Inativos B - Corporativo/Consumidor (N/NE) | Clientes do ramo CONS. FINAL que estão há mais de 180 dias sem comprar, com faturamento médio mensal entre R$ 10000 e R$ 15000 | 28 dias | Carteira norte_nordeste |
| Inativos C - Corporativo/Consumidor (N/NE) | Clientes que já compraram, de ramos fora das demais faixas; ou do ramo CONS. FINAL, há mais de 180 dias sem comprar, com faturamento até R$ 10000 [não traduzido: ramo de atividade igual("CONS. FINAL"] |  | Carteira norte_nordeste. Regra sem ação: não define frequência, preferência nem bloqueio |
| Demais clientes | Clientes do time televendas, exceto os já tratados pelas regras anteriores | Não agendar | Regra final: vale para quem sobrou das faixas anteriores |

## Pontos de atenção

- A regra 'Inativos Curva C (Norte e Nordeste - Corporativo/ Consumidor)' tem um trecho não reconhecido, possível erro de sintaxe: ramo de atividade igual("CONS. FINAL".
- A regra 'Inativos Curva C (Norte e Nordeste - Corporativo/ Consumidor)' não tem ação: não define frequência, preferência nem bloqueio.
- As faixas misturam escopos de recência de compra: as faixas Ativos Curva A, B e C (Sul, Sudeste e Centro-Oeste - Matcon, Ferragista, Agropecuária e Home Center) usam compra na empresa, e a regra 'Pré-inativos Curva C' dessa mesma região e ramo usa também compra no grupo de vendedores. Faixas de escopos diferentes não se excluem automaticamente e podem se sobrepor ou deixar lacunas.
- A regra 'Clientes que hoje não se enquadraram nas regras padrão' tem condição fragmentada demais para resumir: vale para todos os clientes, exceto os já tratados pelas regras anteriores.

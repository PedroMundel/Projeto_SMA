# regra_164.gobr

Regras de agendamento por rótulo de cliente (condomínio para o time da vendedora Bruna, construtora e um grupo de segmentos como shopping, supermercado e indústria) para o time todos e o time bruna. Prospects e novos cadastros entram primeiro, com 7 ou 14 dias; depois vêm as faixas de construtora e as de novos cadastros dos demais segmentos, com frequências de 7 a 45 dias. A regra final bloqueia a agenda de todo cliente não coberto por regra comercial.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Novos cadastros: Condomínio (Bruna) | Clientes com rótulo condominio cadastrados a partir de 2024-10-03 | 14 dias | Vale para o time bruna |
| Condomínio com compra recente (Bruna) | Clientes com rótulo condominio, cadastrados antes de 2024-10-03, que compraram com qualquer vendedor da empresa nos últimos 30 dias | 7 dias | Vale para o time bruna |
| Condomínio sem compra (Bruna) | Clientes com rótulo condominio, cadastrados antes de 2024-10-03, que estão há mais de 90 dias sem comprar com qualquer vendedor da empresa | 30 dias | Vale para o time bruna |
| Prospects | Clientes cadastrados a partir de 2024-08-01 e sem vendas para o vendedor | 7 dias | Vale para o time todos |
| Boas-vindas: construtora | Clientes com rótulo construtora, uma única compra na empresa e mais de 60 dias sem comprar | 14 dias |  |
| Construtora RJ, curva A | Clientes de construtora no RJ, curva A, com frequência histórica de compra de menos de 30 dias e mais de 14 dias sem comprar, exceto os já tratados pelas regras anteriores | 7 dias |  |
| Construtora RJ, curva B | Clientes de construtora no RJ, curva B, com frequência histórica de compra de menos de 30 dias e mais de 14 dias sem comprar, exceto os já tratados pelas regras anteriores | 10 dias |  |
| Construtora RJ, curva C | Clientes de construtora no RJ, curva C, com frequência histórica de compra de menos de 30 dias e mais de 14 dias sem comprar, exceto os já tratados pelas regras anteriores | 14 dias |  |
| Construtora com regularidade | Clientes de construtora com frequência histórica de compra de menos de 30 dias e mais de 14 dias sem comprar, exceto os já tratados pelas regras anteriores | 14 dias |  |
| Construtora: estimular regularidade | Clientes de construtora ativos com a empresa e mais de 45 dias sem comprar com qualquer vendedor da empresa, exceto os já tratados pelas regras anteriores | 10 dias |  |
| Construtora: risco de inatividade | Clientes de construtora com mais de 60 dias sem comprar, exceto os já tratados pelas regras anteriores | 14 dias |  |
| Construtora: novos clientes | Clientes de construtora cadastrados a partir de 2024-10-03, exceto os já tratados pelas regras anteriores | 7 dias |  |
| Construtora: resgate de inativos | Clientes de construtora, exceto os já tratados pelas regras anteriores | 45 dias | Última faixa das construtoras: vale para quem sobrou das anteriores |
| Novos cadastros: shopping, supermercado e outros | Clientes com rótulo shopping, supermercado, industria, estaleiro, clube, escolas e mais 7, sem rótulo construtora, cadastrados a partir de 2024-10-03 | 14 dias |  |
| Compra recente: shopping, supermercado e outros | Clientes com rótulo shopping, supermercado, industria, estaleiro, clube, escolas e mais 7, sem rótulo construtora, cadastrados antes de 2024-10-03, que compraram com a empresa nos últimos 30 dias | 7 dias |  |
| Compra recente: shopping, supermercado e outros (30 dias) | Clientes que compraram com qualquer vendedor da empresa nos últimos 30 dias e têm rótulo shopping, supermercado, industria, estaleiro, clube, escolas e mais 7 | 30 dias | Nunca é aplicada: todos esses clientes já foram tratados antes |
| Bloqueio: cliente não coberto por regra comercial | Clientes de todo o time todos, exceto os já tratados pelas regras anteriores | Não agendar | Regra final: vale para quem sobrou das faixas anteriores |

## Pontos de atenção

- A recência de compra é medida em escopos diferentes ao longo das regras (empresa toda e grupo de vendedores); faixas de escopos diferentes não se excluem automaticamente e podem se sobrepor ou deixar lacunas.
- A regra 'Compra com regularidade no RJ - Curva A' tem condição complexa demais para resumir: vale para o critério dela exceto os clientes já tratados pelas regras anteriores.
- A regra 'Compra com regularidade no RJ - Curva B' tem condição complexa demais para resumir: vale para o critério dela exceto os clientes já tratados pelas regras anteriores.
- A regra 'Compra com regularidade no RJ - Curva C' tem condição complexa demais para resumir: vale para o critério dela exceto os clientes já tratados pelas regras anteriores.
- A regra 'Compra com regularidade' tem condição complexa demais para resumir: vale para o critério dela exceto os clientes já tratados pelas regras anteriores.
- A regra 'Estimular regularidade' tem condição complexa demais para resumir: vale para o critério dela exceto os clientes já tratados pelas regras anteriores.
- A regra 'Risco de ficar inativo' tem condição complexa demais para resumir: vale para o critério dela exceto os clientes já tratados pelas regras anteriores.
- A regra 'Ativar novos clientes' tem condição complexa demais para resumir: vale para o critério dela exceto os clientes já tratados pelas regras anteriores.
- A regra 'Resgate de inativos' tem condição complexa demais para resumir: vale para o critério dela exceto os clientes já tratados pelas regras anteriores.
- A regra 'Freq. de 30 dias para Novos cadastros shopping, supermercado e outros' nunca é aplicada: todos os clientes dela já são tratados por regras anteriores.
- A regra 'Isocom: Não agendar' tem condição complexa demais para resumir: vale para todos os clientes exceto os já tratados pelas regras anteriores.
- Clientes do time bruna que não têm rótulo condominio, ou que têm rótulo condominio, foram cadastrados antes de 2024-10-03 e nunca compraram com a empresa ou compraram nos últimos 90 dias, mas estão há mais de 30 dias sem comprar, não se enquadram em nenhuma regra e ficam sem parametrização.

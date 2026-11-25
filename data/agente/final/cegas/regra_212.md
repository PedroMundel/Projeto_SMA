```gobr
version 1.0


time "televendas":
    vendedores todostelevendas ativados


parametros "Bloqueio - Rota nos próximos 7 dias":
    do time("televendas")
    quando data da rota futura nos proximos 7 dias
    nao agendar

parametros "Bloqueio - Compra nos últimos 14 dias":
    do time("televendas")
    quando tem venda da empresa em 14 dias
    nao agendar

parametros "Rota há 7 dias, visita semana anterior, compra 14-30 dias":
    do time("televendas")
    quando data da rota ha 7 dias atras
        e tem visita da empresa na semana anterior
        e tem venda da empresa entre 14 dias e 30 dias
    frequencia de 7 dias

parametros "Compra entre 31 e 60 dias atrás":
    do time("televendas")
    quando tem venda da empresa entre 31 dias e 60 dias
    frequencia de 20 dias

parametros "Nunca comprou":
    do time("televendas")
    quando sem venda da empresa
    frequencia de 14 dias

parametros "Compra no ano passado entre 180 e 360 dias":
    do time("televendas")
    quando tem venda no ano passado
        e recencia de positivacao entre 180 dias e 360 dias
    frequencia de 14 dias

parametros "Última compra entre 61 e 90 dias":
    do time("televendas")
    quando recencia de positivacao entre 61 dias e 90 dias
    frequencia de 7 dias

parametros "Última compra entre 91 e 180 dias":
    do time("televendas")
    quando recencia de positivacao entre 91 dias e 180 dias
    frequencia de 7 dias

parametros "Demais clientes":
    do time("televendas")
    frequencia de 7 dias
```

**O que ficou de fora / Premissas / Pontos falhos:**

1.  **"Teve rota há 7 dias"**: Utilizei a cláusula `data da rota ha 7 dias atras` (encontrada no exemplo 186). O manual não detalha essa sintaxe específica, mas o exemplo a valida.
2.  **Ordem das regras**: Segui a ordem de precedência do pedido (bloqueios primeiro, depois faixas específicas, depois gerais). Note que a regra "Compra entre 31 e 60 dias" vem antes de "Nunca comprou" e "Compra no ano passado". Como "Nunca comprou" é `sem venda da empresa`, ele não conflita com clientes que têm compra entre 31-60 dias. A regra "Compra no ano passado entre 180 e 360 dias" usa `recencia de positivacao` para garantir que não pegamos clientes com compra mais recente (que seriam capturados pelas faixas de 14-30, 31-60, 61-90, 91-180).
3.  **Escopo**: Todas as regras aplicam-se ao time "televendas" como um todo, sem filtrar por vendedor específico ou segmento de carteira, conforme a premissa aceita.
4.  **Sobreposição de faixas**: As faixas de recência (14-30, 31-60, 61-90, 91-180) são mutuamente exclusivas entre si. A regra "Nunca comprou" captura quem tem 0 dias de compra (ou nunca comprou). A regra "Compra no ano passado entre 180 e 36…

Pontos de atenção na modelagem:
- A cascata mistura escopos de recência de compra (global: Bloqueio - Compra nos últimos 14 dias; grupo: Compra no ano passado entre 180 e 360 dias, Última compra entre 61 e 90 dias, Última compra entre 91 e 180 dias); faixas de escopos diferentes não se excluem automaticamente e podem se sobrepor ou deixar lacunas.
- Última compra entre 91 e 180 dias: Condição efetiva fragmentada demais para resumir; descreva como a condição própria exceto os clientes já tratados pelas regras anteriores.
- Demais clientes: Condição efetiva fragmentada demais para resumir; descreva como a condição própria exceto os clientes já tratados pelas regras anteriores.
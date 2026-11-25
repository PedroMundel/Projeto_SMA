```gobr
version 1.0

time "televendas":
    vendedores todostelevendas ativados

parametros "Não agendar inadimplentes":
    do time("televendas")
    quando inadimplentes
    nao agendar

parametros "Prospect 7 dias":
    do time("televendas")
    quando prospects da empresa
    frequencia de 7 dias

parametros "Construtora unica compra 21 dias":
    do time("televendas")
    quando ramo de atividade igual("37")
        e unica compra com a empresa
    frequencia de 21 dias

parametros "Cliente unica compra 7 dias":
    do time("televendas")
    quando unica compra com a empresa
    frequencia de 7 dias

parametros "Frequencia historica menor que 11 dias 7 dias":
    do time("televendas")
    quando frequencia historica menor que 11 dias ou indefinida
    frequencia de 7 dias

parametros "Construtora recencia 60-89 dias 14 dias":
    do time("televendas")
    quando ramo de atividade igual("37")
        e recencia de positivacao entre 60 dias e 89 dias
    frequencia de 14 dias

parametros "Construtora recencia 11-59 dias 21 dias":
    do time("televendas")
    quando ramo de atividade igual("37")
        e recencia de positivacao entre 11 dias e 59 dias
    frequencia de 21 dias

parametros "Inativo 21 dias":
    do time("televendas")
    quando inatividade global de 90 dias
    frequencia de 21 dias

parametros "Demais clientes 7 dias":
    do time("televendas")
    frequencia de 7 dias
```

**Notas:**
1.  **Ramo de Atividade:** Utilizou-se `ramo de atividade igual("37")` para identificar as construtoras, conforme a sintaxe padrão de filtros de ID do manual (seção 6.6). Assumi que "37" é o ID correto, já que o usuário não respondeu à pergunta.
2.  **Ordem das Regras:** A regra "Construtora unica compra 21 dias" foi posicionada antes de "Cliente unica compra 7 dias" para garantir que as construtoras com uma única compra sejam tratadas pela regra de 21 dias, e não pela de 7 dias.
3.  **Inativos:** Utilizou-se `inatividade global de 90 dias` para o critério de inatividade.
4.  **Demais Clientes:** A última regra sem `quando` captura os clientes restantes.

Pontos de atenção na modelagem:
- A cascata mistura escopos de recência de compra (global: Inativo 21 dias; grupo: Construtora recencia 60-89 dias 14 dias, Construtora recencia 11-59 dias 21 dias); faixas de escopos diferentes não se excluem automaticamente e podem se sobrepor ou deixar lacunas.

Perguntas feitas:
- Qual é o ID do ramo de atividade "Construtora" no seu cadastro do Govendas? (Ex: "37", "10207004", etc.) -> Sem resposta do usuário: siga com a premissa mais provável e diga nas notas qual foi.
- O ID do ramo "Construtora" é "37"? -> Sem resposta do usuário: siga com a premissa mais provável e diga nas notas qual foi.
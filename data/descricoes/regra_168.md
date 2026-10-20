# regra_168.gobr

Regra de agendamento do time de televendas organizada em cinco carteiras fixas de rotas por cidade: uma de rota todo dia e quatro de rota de terça a sexta. Todas as rotas têm frequência de 1 dia e entram na roteirização de visitas presenciais; a rota todo dia é atendida de segunda a sexta e as demais são agendadas no dia anterior ao da rota. Antes das rotas, deixam de ser agendados os clientes baixados na Receita Federal e os bloqueados. A regra final não agenda os clientes que não se enquadraram nas regras.

## Carteiras

| Carteira | Descrição |
|---|---|
| rota_todo_dia | Carteira fixa dos vendedores de televendas com clientes de BALNEARIO CAMBORIU, BOMBINHAS, CAMBORIU, ITAJAI, ITAPEMA e PORTO BELO |
| rota_terca | Carteira fixa dos vendedores de televendas com clientes de BIGUACU, BLUMENAU, BOM RETIRO, BOTUVERA, BRUSQUE, CASCAVEL e mais 16 cidades |
| rota_quarta | Carteira fixa dos vendedores de televendas com clientes de ARAUCARIA, BALNEARIO BARRA DO SUL, BALNEARIO PICARRAS, BARRA VELHA, CAMPO ALEGRE, CAMPO LARGO e mais 20 cidades |
| rota_quinta | Carteira fixa dos vendedores de televendas com clientes de BENTO GONCALVES, BIGUACU, BLUMENAU, BOTUVERA, BRUSQUE, CACHOEIRINHA e mais 33 cidades |
| rota_sexta | Carteira fixa dos vendedores de televendas com clientes de ARAUCARIA, BALNEARIO BARRA DO SUL, BALNEARIO PICARRAS, BARRA VELHA, BIGUACU, CAMPO ALEGRE e mais 25 cidades |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: baixados na Receita | Clientes com situação baixada na Receita Federal | Não agendar |  |
| Bloqueio: bloqueados para atendimento | Clientes bloqueados para atendimento | Não agendar |  |
| Rota todo dia | Clientes da carteira rota_todo_dia | 1 dia | Atendimento de segunda a sexta; roteirizável para visitas presenciais; parametrização fixa |
| Rota de terça | Clientes da carteira rota_terca | 1 dia | Preferência na segunda, demais dias sem atendimento; executada somente na segunda; roteirizável; parametrização fixa |
| Rota de quarta | Clientes da carteira rota_quarta | 1 dia | Preferência na terça, demais dias sem atendimento; executada somente na terça; roteirizável; parametrização fixa |
| Rota de quinta | Clientes da carteira rota_quinta | 1 dia | Preferência na quarta, demais dias sem atendimento; executada somente na quarta; roteirizável; parametrização fixa |
| Rota de sexta | Clientes da carteira rota_sexta | 1 dia | Preferência na quinta, demais dias sem atendimento; executada somente na quinta; roteirizável; parametrização fixa |
| Demais clientes | Clientes fora da carteira rota_todo_dia, exceto os já tratados pelas regras anteriores | Não agendar | Regra final: vale para quem sobrou das regras anteriores |

## Pontos de atenção

- Nos dias em que a regra 'Rota de terça -> Agendamento segunda' é executada (somente na segunda), os clientes dela são tratados por ela antes da regra final 'Não agendar clientes que não se enquadraram nas regras hoje'.
- Nos dias em que a regra 'Rota de quarta -> Agendamento terça' é executada (somente na terça), os clientes dela são tratados por ela antes da regra final 'Não agendar clientes que não se enquadraram nas regras hoje'.
- Nos dias em que a regra 'Rota de quinta -> Agendamento quarta' é executada (somente na quarta), os clientes dela são tratados por ela antes da regra final 'Não agendar clientes que não se enquadraram nas regras hoje'.
- Nos dias em que a regra 'Rota de sexta -> Agendamento quinta' é executada (somente na quinta), os clientes dela são tratados por ela antes da regra final 'Não agendar clientes que não se enquadraram nas regras hoje'.
- As carteiras rota_terca e rota_quinta compartilham 18 cidades (BIGUACU, BLUMENAU, BOTUVERA, BRUSQUE, FLORIANOPOLIS e outras): esses clientes aparecem nas duas.
- As carteiras rota_terca e rota_sexta compartilham 6 cidades (BIGUACU, FLORIANOPOLIS, GOVERNADOR CELSO RAMOS, PALHOCA, SAO JOSE e outras): esses clientes aparecem nas duas.
- As carteiras rota_quarta e rota_sexta compartilham 19 cidades (ARAUCARIA, BALNEARIO BARRA DO SUL, BALNEARIO PICARRAS, BARRA VELHA, CAMPO ALEGRE e outras): esses clientes aparecem nas duas.
- As carteiras rota_quinta e rota_sexta compartilham 6 cidades (BIGUACU, FLORIANOPOLIS, GOVERNADOR CELSO RAMOS, PALHOCA, SAO JOSE e outras): esses clientes aparecem nas duas.

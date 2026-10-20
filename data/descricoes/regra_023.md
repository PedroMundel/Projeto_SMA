# regra_023.gobr

Regra de agendamento com três grupos: televendas de Goiânia (carteira fixa), televendas do Distrito Federal (carteira fixa) e vendedores de campo do Distrito Federal. Em Goiânia há duas faixas, de 7 e 14 dias. No Distrito Federal, o televendas varia conforme adimplência e situação de compra, e o campo usa 7 e 15 dias com parametrização fixa. O único bloqueio de agenda são os inativos inadimplentes do televendas do Distrito Federal.

## Carteiras

| Carteira | Descrição |
|---|---|
| carteira televendas gyn | Carteira fixa dos vendedores de televendas de Goiânia |
| carteira televendas df | Carteira fixa dos vendedores de televendas do Distrito Federal |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| GYN: sem venda | Clientes que nunca compraram com o vendedor | 7 dias | Carteira televendas gyn |
| GYN: demais clientes | Clientes que já compraram com o vendedor, sejam ativos ou inativos | 14 dias | Carteira televendas gyn |
| DF: adimplentes | Clientes adimplentes | 7 dias | Carteira televendas df |
| DF: ativos inadimplentes | Clientes inadimplentes e ativos para o vendedor | 14 dias | Carteira televendas df |
| Bloqueio: inativos inadimplentes | Clientes inadimplentes e inativos para o vendedor | Não agendar | Carteira televendas df |
| DF: sem venda inadimplentes | Clientes inadimplentes que nunca compraram com o vendedor | 7 dias | Carteira televendas df |
| Campo DF: ativos | Clientes ativos para o vendedor de campo | 7 dias | Fixo: frequência e dias rígidos para o gerador de agendas |
| Campo DF: inativos | Clientes não ativos para o vendedor de campo | 15 dias | Fixo: frequência e dias rígidos para o gerador de agendas |

# duas_mudancas

## Turno 1 (inicial, 63 s, 8001 tokens no maior prompt)

**Usuário:** Ativo: Clientes com pedidos nos últimos 60 dias, 14 dias
Risco de inatividade: Clientes com pedidos entre 60 e 90 dias, 7 dias
Inativo: Clientes sem pedidos há mais de 90 dias, 28 dias

**Agente:**

```gobr
version 1.0

time "televendas":
    vendedores todostelevendas ativados

parametros "Ativo":
    do time("televendas")
    quando recencia de positivacao global em 60 dias
    frequencia de 14 dias

parametros "Risco de inatividade":
    do time("televendas")
    quando recencia de positivacao global em 90 dias
    frequencia de 7 dias

parametros "Inativo":
    do time("televendas")
    frequencia de 28 dias
```

O erro "inalcançável" ocorre porque a cláusula `inatividade global de 60 dias` é um superconjunto de `inatividade global de 90 dias`. Ou seja, se o cliente está há mais de 90 dias sem comprar, ele automaticamente está há mais de 60 dias sem comprar. Como a regra "Risco de inatividade" (60-90 dias) foi escrita com `inatividade global de 60 dias`, ela capturaria também os clientes com mais de 90 dias, sobrando nada para a regra "Inativo".

Para corrigir, devemos usar a mesma lógica dos exemplos:
1. **Ativo**: `recencia de positivacao global em 60 dias` (última compra em até 60 dias).
2. **Risco de inatividade**: `recencia de positivacao global em 90 dias` (última compra em até 90 dias). Como as regras rodam em ordem e "Ativo" já pegou os de até 60 dias, esta regra pegará os que compraram entre 60 e 90 dias.
3. **Inativo**: Sem cláusula `quando` (ou regra final), pois pegará todos os clientes que sobraram (ou seja, aqueles que não compraram há mais de 90 dias).

Aqui está o arquivo corrigido:

Pontos de atenção na modelagem:
- O pedido não diz o time (premissa P11). O arquivo usa "televendas": todos os vendedores de televendas habilitados no Govendas.

**Verificações:**
- [x] Ativo: {"dias": 14}
- [x] Risco de inatividade: {"dias": 7}
- [x] Inativo: {"dias": 28}

## Turno 2 (alterar, 40 s, 5282 tokens no maior prompt)

**Usuário:** O risco passa a 5 dias e o ativo a 10.

**Agente:**

```gobr
version 1.0

time "televendas":
    vendedores todostelevendas ativados

parametros "Ativo":
    do time("televendas")
    quando recencia de positivacao global em 60 dias
    frequencia de 10 dias

parametros "Risco de inatividade":
    do time("televendas")
    quando recencia de positivacao global em 90 dias
    frequencia de 5 dias

parametros "Inativo":
    do time("televendas")
    frequencia de 28 dias
```

Mudança no pedido:
- de "Ativo: Clientes com pedidos nos últimos 60 dias, 14 dias" para "Ativo: Clientes com pedidos nos últimos 60 dias, 10 dias"
- de "Risco de inatividade: Clientes com pedidos entre 60 e 90 dias, 7 dias" para "Risco de inatividade: Clientes com pedidos entre 60 e 90 dias, 5 dias"

O que mudou no arquivo:
- "Ativo" (parametros): saiu `frequencia de 14 dias`, entrou `frequencia de 10 dias`
- "Risco de inatividade" (parametros): saiu `frequencia de 7 dias`, entrou `frequencia de 5 dias`

**Verificações:**
- [x] Ativo: {"dias": 10}
- [x] Risco de inatividade: {"dias": 5}
- [x] Inativo: {"dias": 28}
- [x] Inativo intacta
- [x] sem o 14
- [x] sem o 7

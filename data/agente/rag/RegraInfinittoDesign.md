```gobr
version 1.0

## Definição de times

time "televendas":
    vendedores todostelevendas ativados

## Regras de planejamento

parametros "Prospect":
    do time("televendas")
    quando prospects da empresa
    frequencia de 7 dias

parametros "Ativo":
    do time("televendas")
    quando atividade da empresa em 60 dias
    frequencia de 14 dias

parametros "Risco de inatividade":
    do time("televendas")
    quando atividade da empresa em 90 dias
    frequencia de 7 dias

parametros "Inativo":
    do time("televendas")
    quando inatividade global de 90 dias
    frequencia de 28 dias
```

Erros que ficaram depois de 2 tentativas:
- R2: trecho não reconhecido: atividade da empresa em 60 dias
- R3: trecho não reconhecido: atividade da empresa em 90 dias

Pontos de atenção na modelagem:
- Ativo: Trecho não reconhecido (possível erro de sintaxe): atividade da empresa em 60 dias
- Risco de inatividade: Trecho não reconhecido (possível erro de sintaxe): atividade da empresa em 90 dias
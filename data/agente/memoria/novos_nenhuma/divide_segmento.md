# divide_segmento

## Turno 1 (inicial, 23 s, 4770 tokens no maior prompt)

**Usuário:** Ativos: compra nos últimos 60 dias, 14 dias
Inativos: sem compra há mais de 60 dias, 28 dias

**Agente:**

```gobr
version 1.0


time "televendas":
    vendedores todostelevendas ativados


parametros "Ativos":
    do time("televendas")
    quando recencia de positivacao em 60 dias
    frequencia de 14 dias

parametros "Inativos":
    do time("televendas")
    quando fora da recencia de positivacao em 60 dias
    frequencia de 28 dias
```

**Verificações:**
- [x] Ativos: {"dias": 14}
- [x] Inativos: {"dias": 28}

## Turno 2 (inicial, 97 s, 16332 tokens no maior prompt)

**Usuário:** Separe os inativos em dois: sem compra entre 60 e 120 dias, a cada 21 dias, e sem compra há mais de 120 dias, a cada 45 dias.

**Agente:**

<tool_call>
<function=buscar_exemplos>
<parameter=consulta>
faixa de inatividade entre dois valores quando
</parameter>
</function>
</tool_call>

Erros que ficaram depois de 3 entregas:
- A resposta não trouxe um bloco ```gobr com o arquivo.

**Verificações:**
- [ ] Ativos intacta
- [ ] sem o 28
- [ ] com o 120
- [ ] com o 21
- [ ] com o 45

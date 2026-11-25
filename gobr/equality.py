"""Igualdade exata com o gabarito, regra por regra, sem LLM nem embedding.

- sintática: as mesmas cláusulas (quando roda, filtros e ações), no texto normalizado do parser, em qualquer ordem;
- semântica: as mesmas condições e a mesma ação, mesmo escritas de outro jeito ("inatividade de 60 dias" e "fora da
  recencia de positivacao em 60 dias" são iguais se geram a mesma condição). Vale a condição da própria regra, sem a
  cascata: a ordem entra em `outcomes`.
Nome da regra, time e carteira não contam: o pedido não os dá. A situação ou o escopo diferente conta.
"""
from gobr import agent, cascade
from gobr.ir import Block, GobrFile
from gobr.text import fold


def _action(block: Block) -> str:
    days = agent._frequency_days(block)
    if block.schedules_nothing:
        return "não agendado"
    return f"{days[0]} dias" if len(days) == 1 else "; ".join(sorted(fold(c.text) for c in block.actions))


def syntactic_key(block: Block) -> tuple:
    return tuple(sorted(fold(c.text) for c in block.temporal + block.filters + block.actions)) + tuple(sorted(block.unclassified))


def semantic_key(effective: cascade.Effective) -> tuple:
    boxes = {tuple(sorted((k, repr(v)) for k, v in box.items() if not k.startswith(cascade.SOURCE_PREFIXES)))
             for box in effective.own}
    when = tuple(sorted(fold(c.text) for c in effective.block.temporal))
    return tuple(sorted(boxes)), when, _action(effective.block)


def _matched(gold: list, made: list) -> list[bool]:
    """Para cada regra do gabarito, se há uma regra gerada igual; cada gerada vale uma vez."""
    left, found = list(made), []
    for key in gold:
        found.append(key in left)
        if found[-1]:
            left.remove(key)
    return found


def compare(made: GobrFile, gold: GobrFile) -> dict:
    def rules(file: GobrFile) -> list[cascade.Effective]:
        return [e for e in cascade.compute(file) if e.block.kind == "parametros"]

    ours, theirs = rules(made), rules(gold)
    syntactic = _matched([syntactic_key(e.block) for e in theirs], [syntactic_key(e.block) for e in ours])
    semantic = _matched([semantic_key(e) for e in theirs], [semantic_key(e) for e in ours])
    total = len(theirs)
    return {"regras": total, "geradas": len(ours), "sintatica": sum(syntactic), "semantica": sum(semantic),
            "arquivo_sintatico": total == len(ours) == sum(syntactic),
            "arquivo_semantico": total == len(ours) == sum(semantic),
            "faltam_semantica": [e.block.name for e, ok in zip(theirs, semantic) if not ok]}

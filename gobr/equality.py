"""Igualdade com o gabarito, regra por regra e do arquivo inteiro, sem LLM nem embedding.

- sintática: as mesmas cláusulas (quando roda, filtros e ações), no texto normalizado do parser, em qualquer ordem;
- semântica: as mesmas condições e a mesma ação, mesmo escritas de outro jeito ("atividade de 60 dias" e "recencia de
  positivacao em 60 dias" geram a mesma condição). Vale a condição da própria regra, sem a
  cascata: a ordem entra em `outcomes`.
Nome da regra, time e carteira não contam: o pedido não os dá. A situação ou o escopo diferente conta. O arquivo só é
igual se as regras também vierem na mesma ordem.
"""
from gobr import cascade, dims
from gobr.ir import Block, GobrFile
from gobr.text import fold


def _action(block: Block) -> str:
    """Toda a ação: "14 dias ou do vendedor" e "14 dias, na segunda" não são "14 dias"."""
    return "não agendado" if block.schedules_nothing else "; ".join(sorted(fold(c.text) for c in block.actions))


def _frozen(value) -> str:
    """Texto estável do valor de uma condição: o `repr` de um conjunto muda a cada execução."""
    if isinstance(value, dims.ValueSet):
        return f"{value.excluding}:{sorted(value.values)}"
    if isinstance(value, frozenset):
        return str(sorted(map(str, value)))
    return repr(value)


def syntactic_key(block: Block) -> tuple:
    return tuple(sorted(fold(c.text) for c in block.temporal + block.filters + block.actions)) + tuple(sorted(block.unclassified))


def semantic_key(effective: cascade.Effective) -> tuple:
    boxes = {tuple(sorted((k, _frozen(v)) for k, v in box.items() if not k.startswith(cascade.SOURCE_PREFIXES)))
             for box in effective.own}
    if not boxes:  # os filtros se contradizem: sem condição, só é igual à mesma regra escrita igual
        return ("contraditória",), syntactic_key(effective.block), _action(effective.block)
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
            "arquivo_sintatico": [syntactic_key(e.block) for e in ours] == [syntactic_key(e.block) for e in theirs],
            "arquivo_semantico": [semantic_key(e) for e in ours] == [semantic_key(e) for e in theirs],
            "faltam_semantica": [e.block.name for e, ok in zip(theirs, semantic) if not ok]}

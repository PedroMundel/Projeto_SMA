"""O que um arquivo decide para cada cliente: a medida de significado, que o validador não dá.

Dois arquivos são comparados cliente a cliente numa grade de clientes sintéticos: dias desde a última compra e os
atributos que aparecem em qualquer um dos dois (inadimplente, baixado na Receita, curva, situação...), um a um e aos
pares. O resultado de um cliente é a ação da primeira regra que o pega; "não agendar" e nenhuma regra contam como não
agendado. A nota é a média, por regra do gabarito, dos clientes dela com o mesmo resultado: sem isso, uma regra só
("todos a cada 14 dias") acertaria 92% dos clientes do V1Vidros. Ignora as fontes (time, carteira, segmentação), os filtros
de data e a diferença entre os escopos de compra (o cliente sintético compra só com o grupo).
"""
from itertools import combinations

from gobr import agent, cascade, dims
from gobr.intervals import INF, NEVER, IntervalSet
from gobr.ir import GobrFile
from gobr.text import fold

NOT_SCHEDULED = "não agendado"
DAYS = tuple(range(0, 201)) + (270, 365, 730, NEVER)
MAX_ATTRIBUTES = 8  # acima disso, só um atributo por vez (os pares cresceriam demais)
UNSEEN = "nenhuma regra"


def _default(key: str):
    family = key.split(":")[0]
    return {"receita": "ativa", "situacao": "ativo", "pessoa": "juridica"}.get(family, dims.OTHER)


def _holds(key: str, allowed, group: int, company: int, attributes: dict) -> bool:
    if key.startswith(cascade.SOURCE_PREFIXES):
        return True
    if key.startswith("rec:compra:"):
        day = company if key.endswith(":global") else group
        return bool(allowed & IntervalSet.of(day, day))
    if key.startswith("rec:visita:") or key == "freqhist":
        return bool(allowed & IntervalSet.of(NEVER, NEVER))
    if key == "cadastro":
        return bool(allowed & IntervalSet.of(INF, INF))
    family = key.split(":")[0]
    if family == "situacao" and (company if key.endswith(":empresa") else group) == NEVER:
        return "sem_venda" in allowed
    if family in dims.CATEGORICAL_DOMAINS:
        return attributes.get(key, _default(key)) in allowed
    if isinstance(allowed, dims.ValueSet):
        return allowed.excluding != (key in attributes)
    return attributes.get(key, False) in allowed


def _rules(file: GobrFile) -> list[tuple[cascade.Effective, str]]:
    found = []
    for e in cascade.compute(file):
        if e.block.kind == "parametros" and e.block.actions:
            days = agent._frequency_days(e.block)
            action = f"{days[0]} dias" if days else "; ".join(fold(c.text) for c in e.block.actions)
            found.append((e, NOT_SCHEDULED if e.block.schedules_nothing else action))
    return found


def _match(rules, group: int, company: int, attributes: dict) -> int | None:
    return next((n for n, (e, _) in enumerate(rules)
                 if any(all(_holds(k, v, group, company, attributes) for k, v in box.items()) for box in e.own)), None)


def outcomes(file: GobrFile, clients: list[tuple[int, int]], attributes: dict) -> list[str]:
    """A ação que cada cliente (dias no grupo, dias na empresa) recebe."""
    rules = _rules(file)
    matches = [_match(rules, group, company, attributes) for group, company in clients]
    return [NOT_SCHEDULED if n is None else rules[n][1] for n in matches]


def profiles(files: list[GobrFile]) -> list[dict]:
    """Combinações de atributos a testar: nenhum, cada valor citado nos arquivos e os pares de atributos diferentes."""
    values = set()
    for file in files:
        for e, _ in _rules(file):
            for box in e.own:
                for key, allowed in box.items():
                    family = key.split(":")[0]
                    if key.startswith(cascade.SOURCE_PREFIXES) or family in ("rec", "freqhist", "cadastro"):
                        continue
                    if family in dims.CATEGORICAL_DOMAINS:
                        values |= {(key, v) for v in allowed if v not in (_default(key), dims.OTHER, "sem_venda")}
                    else:
                        values.add((key, True))
    singles = sorted(values, key=str)
    pairs = [p for p in combinations(singles, 2) if p[0][0] != p[1][0]] if len(singles) <= MAX_ATTRIBUTES else []
    return [{}] + [dict([v]) for v in singles] + [dict(p) for p in pairs]


def agreement(made: GobrFile, gold: GobrFile) -> dict:
    """`regras`: por regra do gabarito, a fração dos clientes dela com o mesmo resultado; `media`: a média delas.

    Os clientes que o gabarito não pega com regra nenhuma entram como mais uma linha, se existirem.
    """
    made_rules, gold_rules = _rules(made), _rules(gold)
    hits: dict[str, list[int]] = {}
    for attributes in profiles([made, gold]):
        for day in DAYS:
            g, m = _match(gold_rules, day, day, attributes), _match(made_rules, day, day, attributes)
            wanted = NOT_SCHEDULED if g is None else gold_rules[g][1]
            got = NOT_SCHEDULED if m is None else made_rules[m][1]
            count = hits.setdefault(UNSEEN if g is None else gold_rules[g][0].block.name, [0, 0])
            count[0] += wanted == got
            count[1] += 1
    order = [e.block.name for e, _ in gold_rules if e.block.name in hits] + [UNSEEN] * (UNSEEN in hits)
    shares = {name: hits[name][0] / hits[name][1] for name in order}
    return {"media": sum(shares.values()) / len(shares), "regras": shares}


def baselines(gold: GobrFile) -> dict[str, float]:
    """A nota de um arquivo vazio e a de uma regra só com a ação mais comum do gabarito: o piso da métrica."""
    actions = [action for e, action in _rules(gold) if not e.block.schedules_nothing and action.endswith(" dias")]
    common = max(sorted(set(actions)), key=actions.count) if actions else "14 dias"
    team = 'Version 1.0\n\ntime "t":\n    vendedores todos\n\n'
    one = f'{team}parametros "Todos":\n    do time("t")\n    frequencia de {common}\n'
    return {"vazio": agreement(agent._package(team)[0], gold)["media"],
            "uma regra": agreement(agent._package(one)[0], gold)["media"]}

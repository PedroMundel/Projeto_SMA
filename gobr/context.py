"""Context package: everything the redator needs about one .gobr file, as a JSON-ready dict.

The package carries meaning that is already resolved (glosses, effective cascade conditions)
plus deterministic warnings ('alertas') about modelling flaws, so the LLM only writes prose.
"""
import hashlib
import re
from pathlib import Path

from gobr import cascade, dims
from gobr.cascade import Effective
from gobr.ir import Block, Clause, GobrFile
from gobr.parser import parse_file, read_source
from gobr.text import CONTROL_CHARS_RE

PACKAGE_VERSION = "4"  # 2: composite sources as unions (P8); 3: registration age as interval; 4: required numbers
MAX_CODE_CHARS = 160  # long id/city lists are summarized in 'significado'; the full list stays in the .gobr
DAY_NUMBER_RE = re.compile(r"(\d+)\s*dias?\b")
NAME_DAY_NUMBER_RE = re.compile(r"(\d+)\s*(?:d\b|dias?\b)|\bdia (\d+)", re.IGNORECASE)
PREMISES = {
    "P1": "'fora da recencia' exige compra/visita registrada: quem nunca comprou não entra.",
    "P2": "Escopos de recência (grupo, vendedor, global) são medidas distintas, ordenadas: global <= grupo <= vendedor.",
    "P3": "'limpar parametros' não parametriza ninguém, portanto não consome clientes da cascata.",
    "P4": "'sem venda' sem escopo pertence à mesma partição de 'ativos/inativos para o vendedor'.",
    "P5": "Ciclo de vida 'prospect' equivale a 'nunca comprou' no escopo indicado.",
    "P6": "Times diferentes são tratados como conjuntos disjuntos de vendedores.",
    "P7": "Na cascata, cada cliente é alcançado por uma carteira de cada vez; 'da carteira(a, b)' = a ou b.",
    "P8": "Fonte composta ('da segmentacao(x) e da carteira(y)') é a união das fontes: a regra vale para as duas.",
}


def build(path: Path) -> dict:
    file = parse_file(path)
    effectives = cascade.compute(file)
    numbers = _file_numbers(file)
    exclusion_keys = {k for e in effectives if e.block.schedules_nothing and not cascade.temporal_key(e.block)
                      for box in e.own for k in box}
    frequency_keys = {k for e in effectives if not e.block.schedules_nothing for box in e.own for k in box}
    rules = [_rule(e, numbers, exclusion_keys - frequency_keys) for e in effectives]
    uncovered = _uncovered_text(effectives, numbers, exclusion_keys)
    package = {
        "versao_pacote": PACKAGE_VERSION,
        "arquivo": path.name,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "comentarios": [c for c in file.header_comments if "http" not in c],
        "times": [_simple_block(b) for b in file.of_kind("time")],
        "carteiras": [_portfolio(b, file) for b in file.of_kind("carteira", "carteira livre")],
        "segmentacoes": [_simple_block(b) for b in file.of_kind("segmentacao")],
        "bloqueios": [r["nome"] for r in rules if r["acao_principal"] == "nao_agendar"],
        "regras": rules,
        "nao_cobertos": uncovered,
        "alertas": _file_alerts(file, effectives, path),
        "numeros_obrigatorios": sorted({n for r in rules for n in r["numeros"]}),
        "numeros_permitidos": sorted(numbers),
    }
    package["premissas_usadas"] = _premises_used(package)
    return package


def _rule(e: Effective, numbers: set[int], hidden_keys: set[str]) -> dict:
    block = e.block
    own_text = cascade.render_boxes(e.own, e.own, numbers, set()) if e.own else None
    hidden = hidden_keys - {k for box in e.own for k in box}
    effective_text = cascade.render_boxes(e.boxes, e.own, numbers, hidden) if e.boxes else None
    if e.own and not block.filters:
        own_text = "todos os clientes da fonte (sem filtro)"
    rule = {
        "id": block.id,
        "posicao": int(block.id[1:]),
        "nome": block.name,
        "tipo_bloco": block.kind,
        "fonte": " e ".join(c.gloss or c.text for c in block.sources) or "(sem fonte declarada)",
        "quando_executa": [_clause(c) for c in block.temporal],
        "filtros": [_clause(c) for c in block.filters],
        "acoes": [_clause(c) for c in block.actions],
        "acao_principal": _main_action(block),
        "condicao_propria": own_text,
        "condicao_efetiva": effective_text,
        "tratados_antes_por": [b.id for b in e.treated_before if not b.schedules_nothing],
        "bloqueios_anteriores": [b.id for b in e.treated_before if b.schedules_nothing],
        "inalcancavel": e.unreachable,
        "numeros": sorted({n for c in block.filters + block.actions + block.temporal for n in c.numbers}),
        "numeros_exigidos": _required_numbers(e, effective_text, numbers, hidden),
        "alertas": _rule_alerts(e, effective_text, own_text),
    }
    return rule


def _required_numbers(e: Effective, effective_text: str | None, numbers: set[int], hidden: set[str]) -> list[int]:
    """Day thresholds the description must carry. A single effective box: all of them. A union of boxes:
    only the thresholds of the rule's own dimensions shared by every box; the others are cascade exclusions
    that the redator may summarize as "exceto os já tratados". Fragmented or unreachable rules: their own
    condition. Action days (frequency limits) are always required."""
    boxes = e.boxes if effective_text is not None else e.own
    own_keys = {k for box in e.own for k in box}
    per_box = []
    for box in boxes:
        keys = [k for k in box if k not in hidden and (len(boxes) == 1 or k in own_keys)]
        rendered = " ".join(dims.render(k, box[k], numbers) for k in keys)
        per_box.append({int(n) for n in DAY_NUMBER_RE.findall(rendered)})
    shared = set.intersection(*per_box) if per_box else set()
    action_days = {int(n) for c in e.block.actions for n in DAY_NUMBER_RE.findall(c.gloss)}
    return sorted(shared | action_days)


def _clause(c: Clause) -> dict:
    code = c.text if len(c.text) <= MAX_CODE_CHARS else c.text[:MAX_CODE_CHARS] + "…"
    return {"codigo": code, "significado": c.gloss or None, "reconhecida": c.recognized}


def _main_action(block: Block) -> str:
    if block.kind == "limpar parametros":
        return "limpar_parametros"
    if block.schedules_nothing:
        return "nao_agendar"
    kinds = [a.detail.get("tipo") for a in block.actions]
    return "frequencia" if "frequencia" in kinds else (kinds[0] if kinds else "nenhuma")


def _simple_block(block: Block) -> dict:
    return {"id": block.id, "nome": block.name,
            "definicao": "; ".join(c.gloss or f"[não traduzido: {c.text}]" for c in block.sources),
            "filtros": [_clause(c) for c in block.filters]}


def _portfolio(block: Block, file: GobrFile) -> dict:
    data = _simple_block(block)
    data["livre"] = block.kind == "carteira livre"
    if block.kind == "carteira":
        mine = file.teams.get(block.name, frozenset())
        earlier = []
        for other in file.of_kind("carteira"):
            if other is block:
                break
            if file.teams.get(other.name, frozenset()) & mine:
                earlier.append(other.name)
        data["exceto_alocados_em"] = earlier
    return data


def _file_numbers(file: GobrFile) -> set[int]:
    """Numbers written anywhere in the code or in block names; the renderer prefers these when phrasing bounds."""
    found = set()
    for block in file.blocks:
        found |= {int(a or b) for a, b in NAME_DAY_NUMBER_RE.findall(block.name)}
        for clause in block.all_clauses():
            found |= set(clause.numbers)
            found |= {int(n) for n in re.findall(r"\d+", clause.text)}
    return found


def _rule_alerts(e: Effective, effective_text: str | None, own_text: str | None) -> list[str]:
    block, alerts = e.block, []
    if not e.own:
        alerts.append("Os filtros desta regra se contradizem: nenhum cliente pode atendê-los ao mesmo tempo.")
    elif e.unreachable:
        names = ", ".join(f'"{b.name}"' for b in e.treated_before)
        alerts.append(f"Regra inalcançável: todos os clientes dela já foram tratados antes por {names}.")
    if block.schedules_nothing and block.filters and any(not b.schedules_nothing for b in e.treated_before):
        names = ", ".join(f'"{b.name}"' for b in e.treated_before if not b.schedules_nothing)
        alerts.append(f"Bloqueio depois de regras de frequência: clientes já parametrizados por {names} "
                      "não serão bloqueados por esta regra.")
    for earlier in e.partial_before:
        when = "; ".join(c.gloss for c in earlier.temporal)
        alerts.append(f'Nos dias em que "{earlier.name}" é executada ({when}), os clientes dela são tratados '
                      "por ela antes desta regra.")
    if e.boxes and effective_text is None:
        alerts.append("Condição efetiva fragmentada demais para resumir; descreva como a condição própria "
                      "exceto os clientes já tratados pelas regras anteriores.")
    alerts += _name_mismatch(block, f"{own_text} {effective_text}")
    undeclared = sorted({n for c in block.sources for n in c.detail.get("fontes_nao_declaradas", [])})
    if undeclared:
        alerts.append(f"Fonte não declarada no arquivo: {', '.join(undeclared)} (time/carteira/segmentação inexistente "
                      "ou declarada com outro nome).")
    unknown = [c.text for c in block.all_clauses() if not c.recognized] + block.unclassified
    alerts += [f"Trecho não reconhecido (possível erro de sintaxe): {u}" for u in unknown]
    if not block.actions and block.kind == "parametros":
        alerts.append("Regra sem ação (nenhuma frequência, preferência ou bloqueio).")
    return alerts


def _name_mismatch(block: Block, condition_text: str) -> list[str]:
    in_name = {int(a or b) for a, b in NAME_DAY_NUMBER_RE.findall(block.name)}
    in_code = {n for c in block.all_clauses() for n in c.numbers + c.detail.get("dias_equivalentes", [])}
    boundaries = {int(n) for n in re.findall(r"\d+", condition_text)}
    # A name saying "sem venda em 8 dias" matches the boundary "há mais de 7 dias": off-by-one wording is
    # tolerated for cascade boundaries only, never for the code's own values (14 vs 15 days stays a mismatch).
    missing = sorted(n for n in in_name if n not in in_code and not {n - 1, n, n + 1} & boundaries)
    if not missing:
        return []
    return [f"O nome da regra cita {', '.join(map(str, missing))} dia(s), valor que não aparece no código "
            "nem na condição efetiva: nome e código podem estar divergentes."]


def _file_alerts(file: GobrFile, effectives: list[Effective], path: Path) -> list[str]:
    alerts = []
    scopes: dict[str, list[str]] = {}
    for e in effectives:
        for box in e.own:
            for key, value in box.items():
                if key.startswith("rec:compra:") and value.spans != ((-1, -1),):
                    scopes.setdefault(key.split(":")[2], []).append(e.block.name)
    if len(scopes) > 1:
        detail = "; ".join(f"{scope}: {', '.join(names[:3])}" for scope, names in sorted(scopes.items()))
        alerts.append(f"A cascata mistura escopos de recência de compra ({detail}); faixas de escopos diferentes "
                      "não se excluem automaticamente e podem se sobrepor ou deixar lacunas.")
    if CONTROL_CHARS_RE.search(read_source(path)):
        alerts.append("O arquivo contém caracteres de controle invisíveis (possível erro de digitação).")
    alerts += _shared_portfolio_values(file)
    if file.of_kind("limpar parametros"):
        alerts.append("O arquivo usa 'limpar parametros': parametrizações dinâmicas anteriores do GoBR são removidas.")
    return alerts


def _shared_portfolio_values(file: GobrFile) -> list[str]:
    """Portfolios filtered on the same field with overlapping values put the same client in both."""
    alerts = []
    portfolios = file.of_kind("carteira", "carteira livre")
    for index, first in enumerate(portfolios):
        for second in portfolios[index + 1:]:
            if not file.teams.get(first.name, frozenset()) & file.teams.get(second.name, frozenset()):
                continue
            for key, value in _field_values(first).items():
                other = _field_values(second).get(key)
                shared = sorted(value.values & other.values) if other else []
                if shared:
                    alerts.append(f'As carteiras "{first.name}" e "{second.name}" compartilham {len(shared)} valor(es) '
                                  f"de {key.split(':', 1)[1]} ({', '.join(shared[:5])}{'...' if len(shared) > 5 else ''}): "
                                  "esses clientes aparecem nas duas.")
    return alerts


def _field_values(block: Block) -> dict:
    return {k: v for c in block.filters for k, v in c.constraint.items()
            if k.startswith("campo:") and k.count(":") == 1 and not v.excluding}


def _uncovered_text(effectives: list[Effective], numbers: set[int],
                    exclusion_keys: set[str]) -> dict[str, str]:
    texts = {}
    for first, boxes in cascade.uncovered(effectives):
        text = cascade.render_boxes(boxes, cascade.sources_of(first.own), numbers, exclusion_keys)
        source = " e ".join(c.gloss or c.text for c in first.block.sources) or "(sem fonte declarada)"
        texts[source] = text or "várias combinações de clientes não são cobertas por nenhuma regra"
    return texts


def _premises_used(package: dict) -> list[str]:
    blob = str(package["regras"])
    used = {"P2"} if any("escopos de recência" in a for a in package["alertas"]) else set()
    if "da carteira" in blob:
        used.add("P7")
    if any(" e da " in r["fonte"] or " e do " in r["fonte"] for r in package["regras"]):
        used.add("P8")
    if "fora da recencia" in blob:
        used.add("P1")
    if "limpar parametros" in blob:
        used.add("P3")
    if "sem venda" in blob:
        used.add("P4")
    if "prospect" in blob:
        used.add("P5")
    if len(package["times"]) > 1:
        used.add("P6")
    return [f"{p}: {PREMISES[p]}" for p in sorted(used)]

"""Deterministic checks of a redator answer against its context package.

Errors make a candidate unusable; warnings are kept for review.
"""
import json
import re
from dataclasses import dataclass, field

from gobr.redator import view

RULE_KEYS = ("id", "nome", "segmento", "criterio", "frequencia", "observacao", "clausulas_nao_traduzidas")
TOP_KEYS = ("resumo", "carteiras", "regras", "pontos_de_atencao", "consultas_hipoteticas")
DAY_NUMBER_RE = re.compile(r"(\d+)\s*dias?\b")
NUMBER_RE = re.compile(r"(?<![\w.,])\d+(?![\w])")
MAX_COUNT = 20  # small counts ("5 faixas") are allowed in the summary and in the attention points
MAX_CRITERION_WORDS = 40


@dataclass
class Report:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def check(answer: dict, package: dict) -> Report:
    report = Report()
    missing = [k for k in TOP_KEYS if k not in answer]
    if missing:
        report.errors.append(f"campos ausentes: {missing}")
        return report
    allowed = _allowed_numbers(package)
    _check_rules(answer, package, allowed, report)
    _check_portfolios(answer, package, report)
    _check_free_text(answer, allowed, report)
    if package["alertas"] or package["nao_cobertos"] or any(r["alertas"] for r in package["regras"]):
        if not answer["pontos_de_atencao"]:
            report.errors.append("o pacote tem alertas, mas pontos_de_atencao está vazio")
    return report


def _allowed_numbers(package: dict) -> set[int]:
    text = json.dumps(view(package), ensure_ascii=False)
    return set(package["numeros_permitidos"]) | {int(n) for n in NUMBER_RE.findall(text)}


def _check_rules(answer: dict, package: dict, allowed: set[int], report: Report) -> None:
    expected = view(package)["regras"]
    got = answer["regras"]
    if [r.get("id") for r in got] != [r["id"] for r in expected]:
        report.errors.append(f"ids/ordem das regras divergem: {[r.get('id') for r in got]}")
        return
    for rule, source in zip(got, expected):
        absent = [k for k in RULE_KEYS if k not in rule]
        if absent:
            report.errors.append(f"{source['id']}: campos ausentes {absent}")
            continue
        if rule["nome"] != source["nome"]:
            report.errors.append(f"{source['id']}: nome alterado ({rule['nome']!r})")
        text = " ".join(rule[k] for k in ("segmento", "criterio", "frequencia", "observacao"))
        condition = source["condicao_efetiva"] or source.get("condicao_propria") or ""
        required = {int(n) for n in DAY_NUMBER_RE.findall(condition + " " + " ".join(source["acoes"]))}
        written = {int(n) for n in NUMBER_RE.findall(text)}
        if required - written:
            report.errors.append(f"{source['id']}: faltam os números {sorted(required - written)}")
        invented = written - allowed
        if invented:
            report.errors.append(f"{source['id']}: números que não existem no pacote {sorted(invented)}")
        if source["acao_principal"] == "nao_agendar" and "não agendar" not in rule["frequencia"].lower():
            report.errors.append(f"{source['id']}: bloqueio sem 'Não agendar' na frequência")
        if source.get("clausulas_desconhecidas") and not rule["clausulas_nao_traduzidas"]:
            report.errors.append(f"{source['id']}: cláusula desconhecida não declarada")
        if len(rule["criterio"].split()) > MAX_CRITERION_WORDS:
            report.warnings.append(f"{source['id']}: critério com mais de {MAX_CRITERION_WORDS} palavras")


def _check_portfolios(answer: dict, package: dict, report: Report) -> None:
    expected = [c["id"] for c in package["carteiras"]]
    got = [c.get("id") for c in answer["carteiras"]]
    if got != expected:
        report.errors.append(f"ids das carteiras divergem: {got} (esperado {expected})")


def _check_free_text(answer: dict, allowed: set[int], report: Report) -> None:
    counts = set(range(1, MAX_COUNT + 1))
    for field_name in ("resumo", "pontos_de_atencao"):
        value = answer[field_name]
        text = value if isinstance(value, str) else " ".join(value)
        invented = {int(n) for n in NUMBER_RE.findall(text)} - allowed - counts
        if invented:
            report.errors.append(f"{field_name}: números que não existem no pacote {sorted(invented)}")
    queries = answer["consultas_hipoteticas"]
    if len(queries) != 3:
        report.errors.append(f"consultas_hipoteticas deve ter 3 itens, tem {len(queries)}")
    for index, query in enumerate(queries):
        invented = {int(n) for n in NUMBER_RE.findall(query)} - allowed
        if invented:
            report.warnings.append(f"consulta {index + 1}: números fora do pacote {sorted(invented)}")

"""Dimensions of the client space and their pt-BR rendering.

A constraint is a mapping {dimension key: allowed values}. Day-based dimensions hold an
IntervalSet; categorical and boolean dimensions hold a frozenset. Key conventions:

  rec:<compra|visita>:<grupo|vendedor|global>   IntervalSet of days since the last event (-1 = never)
  freqhist                                      IntervalSet of historical purchase frequency (-1 = undefined)
  situacao:<padrao|vendedor|empresa>            {ativo, inativo, sem_venda}
  curva:<empresa|vendedor>                      {A, B, C}
  ciclo:<empresa|vendedor>                      {ativo, inativo, ativado, reativado}
  receita                                       {ativa, suspensa, inapta, baixada}
  time                                          ValueSet of team names
  carteira                                      ValueSet of carteira names (the one the client is reached through)
  segmentacao:<nome>                            {True, False}
  campo:<campo>                                 ValueSet of ids/names ('igual' / 'diferente' filters)
  campo:<campo>:<op>:<v1|v2...>                 {True, False}  ('contem' / 'inicia com' filters)
  <boolean key in BOOLEAN_GLOSS>                {True, False}
  fato:<gloss><US><texto>                       {True, False}  (recognized clause without cascade model)
  opaco:<texto>                                 {True, False}  (unrecognized clause)
"""
from dataclasses import dataclass

from gobr.intervals import INF, NEVER, IntervalSet


@dataclass(frozen=True)
class ValueSet:
    """A finite set of values, or (excluding=True) everything except them. The universe is open:
    an 'igual(...)' filter never needs to know every id that exists in the ERP."""

    values: frozenset = frozenset()
    excluding: bool = False

    def __and__(self, other: "ValueSet") -> "ValueSet":
        if not self.excluding and not other.excluding:
            return ValueSet(self.values & other.values)
        if self.excluding and other.excluding:
            return ValueSet(self.values | other.values, True)
        included, excluded = (self, other) if other.excluding else (other, self)
        return ValueSet(included.values - excluded.values)

    def __or__(self, other: "ValueSet") -> "ValueSet":
        return (self.complement() & other.complement()).complement()

    def __sub__(self, other: "ValueSet") -> "ValueSet":
        return self & other.complement()

    def complement(self) -> "ValueSet":
        return ValueSet(self.values, not self.excluding)

    def __bool__(self) -> bool:
        return self.excluding or bool(self.values)

BOOL = frozenset({True, False})
OTHER = "outro"  # any value the filters do not name (no ABC curve, prospect lifecycle, unknown status...)
CATEGORICAL_DOMAINS = {
    "situacao": frozenset({"ativo", "inativo", "sem_venda"}),
    "curva": frozenset({"A", "B", "C", OTHER}),
    "ciclo": frozenset({"ativo", "inativo", "ativado", "reativado", OTHER}),
    "receita": frozenset({"ativa", "suspensa", "inapta", "baixada", OTHER}),
}
FACT_SOURCE_SEPARATOR = "\x1f"
BOOLEAN_GLOSS = {
    "inadimplente": ("inadimplentes", "adimplentes"),
    "pessoa_juridica": ("pessoa jurídica", "pessoa física"),
    "filial": ("filiais", "clientes principais (não filiais)"),
    "bloqueado": ("bloqueados para atendimento", "não bloqueados"),
    "excluido": ("excluídos do sistema", "não excluídos"),
    "credito": ("com crédito disponível", "sem crédito disponível"),
    "coordenada": ("com geolocalização confiável", "sem geolocalização confiável"),
    "agendavel": ("marcados como agendáveis", "marcados como não agendáveis"),
    "unica_compra:empresa": ("com uma única compra na empresa", "sem ser de compra única na empresa"),
    "unica_compra:vendedor": ("com uma única compra com o vendedor", "sem ser de compra única com o vendedor"),
    "rota_semana": ("com data de rota (vendedor externo) nesta semana", "sem data de rota nesta semana"),
}
EXPLICIT_GROUP_SUFFIX = " no grupo de vendedores"
SCOPE_SUFFIX = {"grupo": "", "vendedor": " com o próprio vendedor", "global": " com qualquer vendedor da empresa"}
SITUACAO_WORDS = {"ativo": "ativos", "inativo": "inativos", "sem_venda": "sem vendas"}
SITUACAO_SCOPE = {"padrao": "", "vendedor": " para o vendedor", "empresa": " para a empresa"}
FIELD_LABELS = {
    "nome da cidade": "cidade",
    "nome do bairro": "bairro",
    "uf do estado": "UF",
    "nome da rota": "nome da rota",
    "codigo da rota": "código da rota",
    "ramo de atividade": "ramo de atividade (id)",
    "cnae": "CNAE (id)",
    "cnae da receita": "CNAE da Receita (id)",
    "cnae do erp": "CNAE do ERP",
    "nome do cnae da receita": "nome do CNAE da Receita",
    "o rotulo": "rótulo",
    "conteudo da nota": "conteúdo da nota",
    "nome da nota": "nome da nota",
    "id do cliente": "id do cliente",
    "id do cliente principal": "id do cliente principal",
    "tipo de pagamento": "tipo de pagamento (id)",
    "tipo de cobranca": "tipo de cobrança (id)",
}
FIELD_OPS = {"igual": ("é", "não é"), "diferente": ("não é", "é"), "contem": ("contém", "não contém"),
             "inicia com": ("começa com", "não começa com")}
MAX_LISTED_VALUES = 6


def domain(key: str):
    if key.startswith("rec:") or key == "freqhist":
        return IntervalSet.full()
    if key in ("time", "carteira") or (key.startswith("campo:") and key.count(":") == 1):
        return ValueSet(excluding=True)
    return CATEGORICAL_DOMAINS.get(key.split(":")[0], BOOL)


def render(key: str, value, numbers: set[int], explicit_group: bool = False) -> str:
    """pt-BR phrase for 'the client's <key> is within <value>'. explicit_group names the seller-group
    scope, needed when the same phrase also mentions another recency scope."""
    family = key.split(":")[0]
    if family == "rec":
        _, event, scope = key.split(":")
        suffix = EXPLICIT_GROUP_SUFFIX if explicit_group and scope == "grupo" else SCOPE_SUFFIX[scope]
        return _render_recency(value, event, suffix, numbers)
    if key == "freqhist":
        return _render_freqhist(value, numbers)
    if family in CATEGORICAL_DOMAINS and (OTHER in value or len(CATEGORICAL_DOMAINS[family] - value) == 1):
        return _render_categorical_negation(key, sorted(CATEGORICAL_DOMAINS[family] - value))
    if family == "situacao":
        words = " ou ".join(SITUACAO_WORDS[v] for v in sorted(value))
        return f"{words}{SITUACAO_SCOPE[key.split(':')[1]]}"
    if family == "curva":
        return f"curva {' ou '.join(sorted(value))} com {'a empresa' if key.endswith('empresa') else 'o vendedor'}"
    if family == "ciclo":
        target = "a empresa" if key.endswith("empresa") else "o vendedor"
        return f"no ciclo de vida {' ou '.join(sorted(value))} com {target}"
    if family == "receita":
        return f"com situação {' ou '.join(sorted(value))} na Receita Federal"
    if key in ("time", "carteira"):
        names = ", ".join(sorted(value.values))
        return f"{'fora d' if value.excluding else 'd'}{'o time' if key == 'time' else 'a carteira'} {names}"
    if isinstance(value, ValueSet):
        return _render_value_set(key.split(":", 1)[1], value)
    return _render_boolean(key, True in value)


def _list_values(listed: list[str]) -> str:
    shown = ", ".join(listed[:MAX_LISTED_VALUES])
    return shown + (f" e mais {len(listed) - MAX_LISTED_VALUES}" if len(listed) > MAX_LISTED_VALUES else "")


def _render_value_set(field: str, value: ValueSet) -> str:
    listed = sorted(value.values)
    shown = _list_values(listed)
    label = FIELD_LABELS.get(field, field)
    if len(listed) == 1:
        return f"{label} {'diferente de' if value.excluding else 'igual a'} {shown}"
    return f"{label} {'fora de' if value.excluding else 'em'}: {shown}"


def _render_categorical_negation(key: str, excluded: list[str]) -> str:
    family = key.split(":")[0]
    if family == "situacao":
        scope = SITUACAO_SCOPE[key.split(":")[1]]
        if excluded == ["sem_venda"]:
            return f"com alguma venda (ativos ou inativos){scope}"
        return f"não {' nem '.join(SITUACAO_WORDS[e] for e in excluded)}{scope}"
    listed = " nem ".join(excluded)
    if family == "receita":
        return f"não estão com situação {listed} na Receita Federal"
    target = "a empresa" if key.endswith("empresa") else "o vendedor"
    if family == "curva":
        return f"fora da curva {listed} com {target}"
    return f"fora do ciclo de vida {listed} com {target}"


def _render_boolean(key: str, positive: bool) -> str:
    family, _, rest = key.partition(":")
    if key in BOOLEAN_GLOSS:
        return BOOLEAN_GLOSS[key][0 if positive else 1]
    if family == "segmentacao":
        return f"{'na' if positive else 'fora da'} segmentação \"{rest}\""
    if family == "campo":
        field, op, values = rest.split(":", 2)
        listed = values.split("|")
        shown = _list_values(listed)
        verb = FIELD_OPS[op][0 if positive else 1]
        return f"{FIELD_LABELS.get(field, field)} {verb} {'um de ' if len(listed) > 1 and op in ('igual', 'diferente') else ''}{shown}"
    if family == "fato":
        gloss = rest.split(FACT_SOURCE_SEPARATOR)[0]
        return gloss if positive else f"não ({gloss})"
    if family == "opaco":
        return f"[não traduzido: {rest}]" if positive else f"não [não traduzido: {rest}]"
    raise KeyError(f"dimensão sem renderização: {key}")


def _lower(lo: int, numbers: set[int]) -> str:
    """Phrase for 'days >= lo', printing a number that exists in the source file when possible."""
    if lo in numbers and (lo - 1) not in numbers:
        return f"pelo menos {lo}"
    return f"mais de {lo - 1}"


def _upper(hi: int, numbers: set[int]) -> str:
    if (hi + 1) in numbers and hi not in numbers:
        return f"menos de {hi + 1}"
    return f"até {hi}"


def _render_recency(value: IntervalSet, event: str, suffix: str, numbers: set[int]) -> str:
    verb, noun = ("compraram", "comprar") if event == "compra" else ("foram visitados", "receber visita")
    parts = []
    for lo, hi in value.spans:
        if lo == NEVER:
            parts.append(f"nunca {verb}{suffix}")
            lo = 0
            if hi == NEVER:
                continue
        if lo == 0 and hi == INF:
            parts.append(f"já {verb}{suffix}")
        elif lo == 0:
            parts.append(f"{verb}{suffix} nos últimos {hi} dias")
        elif hi == INF:
            parts.append(f"sem {noun}{suffix} há {_lower(lo, numbers)} dias")
        else:
            parts.append(f"{verb}{suffix} nos últimos {hi} dias, mas estão há {_lower(lo, numbers)} dias sem {noun}")
    return " ou ".join(parts) if len(parts) == 1 else "(" + " ou ".join(parts) + ")"


def _render_freqhist(value: IntervalSet, numbers: set[int]) -> str:
    parts = []
    for lo, hi in value.spans:
        if lo == NEVER:
            parts.append("frequência histórica indefinida")
            lo = 0
            if hi == NEVER:
                continue
        if hi == INF:
            parts.append(f"frequência histórica de compra de {_lower(lo, numbers)} dias")
        elif lo == 0:
            parts.append(f"frequência histórica de compra de {_upper(hi, numbers)} dias")
        elif lo == hi:
            parts.append(f"frequência histórica de compra de {lo} dias")
        else:
            parts.append(f"frequência histórica de compra entre {lo} e {hi} dias")
    return " ou ".join(parts)

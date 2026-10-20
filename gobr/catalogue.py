"""Clause catalogue: folded statement text -> Clause (gloss, cascade constraint, thresholds).

Every matcher receives text that is folded (lowercase, no accents) with literals masked as
<sN>/<dN>. Matchers are tried in order; the first that returns a Clause wins. Anything no
matcher accepts becomes an unrecognized Clause with an 'opaco:' constraint, so the cascade
still treats it as an unknown condition instead of ignoring it.
"""
import re
from collections.abc import Callable

from gobr import dims
from gobr.intervals import NEVER, IntervalSet
from gobr.ir import Clause
from gobr.text import Literals

DAYS = r"(\d+) dias?"
WEEKDAYS = {"segunda": "segunda", "terca": "terça", "quarta": "quarta", "quinta": "quinta",
            "sexta": "sexta", "sabado": "sábado", "domingo": "domingo"}
WORKDAYS = ["segunda", "terca", "quarta", "quinta", "sexta"]
FIXED_FREQUENCIES = {"diaria": 1, "semanal": 7, "quinzenal": 15, "mensal": 30, "bimestral": 60,
                     "trimestral": 90, "semestral": 180, "anual": 365}
ORDINAL_WEEKS = {"primeira": "1ª", "segunda": "2ª", "terceira": "3ª", "quarta": "4ª", "ultima": "última"}
PERIODS = {
    "na semana": "na semana atual", "no mes": "no mês atual", "no ano": "no ano atual",
    "no bimestre": "no bimestre atual", "no trimestre": "no trimestre atual", "no semestre": "no semestre atual",
    "na quinzena": "na quinzena atual", "do dia": "hoje", "no dia": "hoje", "hoje": "hoje", "ontem": "ontem",
    "de ontem": "ontem", "na semana anterior": "na semana anterior", "no mes anterior": "no mês anterior",
    "no ano anterior": "no ano anterior", "no ano passado": "no ano anterior",
}


class Context:
    """What a matcher may need besides the text: literals and the file's source -> teams map."""

    def __init__(self, literals: Literals, teams: dict[str, frozenset[str]]):
        self.literals = literals
        self.teams = teams

    def unmask(self, text: str) -> str:
        return self.literals.unmask(text)


Matcher = Callable[[str, Context], Clause | None]


def ints(text: str) -> list[int]:
    return [int(n) for n in re.findall(r"(?<![<\w])\d+(?![\w>])", text)]


def describe_period(cond: str) -> str | None:
    """Translate a time conditional ('em 30 dias', 'entre 10 dias e 90 dias', 'na semana') to pt-BR."""
    cond = cond.strip()
    if cond in PERIODS:
        return PERIODS[cond]
    if m := re.fullmatch(r"em (\d+) (dias?|semanas?|meses|mes|anos?|horas?)", cond):
        return f"nos últimos {m.group(1)} {m.group(2)}"
    if m := re.fullmatch(r"entre (\d+) (?:dias? )?e (\d+) dias?", cond):
        return f"entre {m.group(1)} e {m.group(2)} dias atrás"
    if m := re.fullmatch(r"ha (\d+) (dias?|semanas?|meses|anos?) atras", cond):
        return f"há {m.group(1)} {m.group(2)}"
    if m := re.fullmatch(r"nos proximos (\d+) (dias?|semanas?|meses)", cond):
        return f"nos próximos {m.group(1)} {m.group(2)}"
    if m := re.fullmatch(r"(?:futura )?em (\d+) (dias?|semanas?) a frente", cond):
        return f"daqui a {m.group(1)} {m.group(2)} ou mais"
    if m := re.fullmatch(r"entre <d\d+> e <d\d+>", cond):
        return f"no intervalo {cond}"
    return None


# ---------------------------------------------------------------- filters (quando)

def _recency(text: str, ctx: Context) -> Clause | None:
    m = re.fullmatch(r"(fora da )?recencia de (positivacao|visita|venda)( do vendedor| global)? (.+)", text)
    if not m:
        return None
    outside, event_raw, scope_raw, cond = m.groups()
    event = "visita" if event_raw == "visita" else "compra"
    scope = {None: "grupo", " do vendedor": "vendedor", " global": "global"}[scope_raw]
    window = None
    if w := re.fullmatch(f"em {DAYS}", cond):
        window = IntervalSet.of(0, int(w.group(1)))
    elif w := re.fullmatch(f"entre {DAYS} e {DAYS}", cond):
        window = IntervalSet.of(int(w.group(1)), int(w.group(2)))
    if window is None:
        period = describe_period(cond)
        if period is None:
            return None
        gloss = f"{'sem' if outside else 'com'} {event} {period}{dims.SCOPE_SUFFIX[scope]}"
        return _fact(text, gloss)
    # P1: 'fora da recencia' requires a recorded event; never-bought clients do not match it.
    value = (IntervalSet.of(0) - window) if outside else window
    key = f"rec:{event}:{scope}"
    numbers = ints(cond)
    return Clause(text, dims.render(key, value, set(numbers)), constraint={key: value}, numbers=numbers)


def _activity(text: str, ctx: Context) -> Clause | None:
    """'inatividade de N dias', 'atividade global de N dias', 'tem venda ... em N dias', 'nao tem venda ...'."""
    scope_of = {None: "grupo", "global": "global", "do vendedor": "vendedor", "da empresa": "global"}
    if m := re.fullmatch(rf"inatividade(?: (global))?( de| maior que) {DAYS}", text):
        key, n = f"rec:compra:{scope_of[m.group(1)]}", int(m.group(3))
        value = IntervalSet.of(n + 1 if m.group(2) == " maior que" else n)
    elif m := re.fullmatch(rf"atividade(?: (global|do vendedor))? de {DAYS}", text):
        key, n = f"rec:compra:{scope_of[m.group(1)]}", int(m.group(2))
        value = IntervalSet.of(0, n)
    elif m := re.fullmatch(rf"(nao )?tem venda(?: (do vendedor|da empresa))? em {DAYS}", text):
        key, n = f"rec:compra:{scope_of[m.group(2)]}", int(m.group(3))
        value = IntervalSet.of(0, n)
        if m.group(1):
            value = IntervalSet.full() - value
    elif m := re.fullmatch(r"(nao )?tem venda(?: (do vendedor|da empresa))? (.+)", text):
        period = describe_period(m.group(3))
        if period is None:
            return None
        who = {None: "", "do vendedor": " com o vendedor", "da empresa": " com a empresa"}[m.group(2)]
        return _fact(text, f"{'sem' if m.group(1) else 'com'} compra{who} {period}")
    else:
        return None
    return Clause(text, dims.render(key, value, {n}), constraint={key: value}, numbers=[n])


def _situation(text: str, ctx: Context) -> Clause | None:
    if m := re.fullmatch(r"(ativos|inativos)(?: para (o vendedor|a empresa))?", text):
        scope = {None: "padrao", "o vendedor": "vendedor", "a empresa": "empresa"}[m.group(2)]
        value = frozenset({m.group(1)[:-1]})
    elif m := re.fullmatch(r"sem vendas?(?: (do vendedor|da empresa))?(?: ou prospects)?", text):
        # P4: 'sem venda' without scope belongs to the same partition as 'ativos/inativos para o vendedor'.
        scope = {None: "vendedor", "do vendedor": "vendedor", "da empresa": "empresa"}[m.group(1)]
        value = frozenset({"sem_venda"})
    else:
        return None
    key = f"situacao:{scope}"
    return Clause(text, dims.render(key, value, set()), constraint={key: value})


def _lifecycle(text: str, ctx: Context) -> Clause | None:
    m = re.fullmatch(r"(?:no )?ciclo de vida (prospect|ativo|inativo|ativado|reativado) com (a empresa|o vendedor)", text)
    if m is None:
        if text in ("prospect", "prospects", "prospects da empresa", "prospects do vendedor"):
            scope = "vendedor" if text.endswith("vendedor") else "global"
            return _never_bought(text, scope)
        return None
    stage, target = m.groups()
    if stage == "prospect":
        # P5: lifecycle 'prospect' = never bought in that scope, so it shares the recency dimension.
        return _never_bought(text, "global" if target == "a empresa" else "vendedor")
    key = f"ciclo:{'empresa' if target == 'a empresa' else 'vendedor'}"
    value = frozenset({stage})
    return Clause(text, dims.render(key, value, set()), constraint={key: value})


def _never_bought(text: str, scope: str) -> Clause:
    key, value = f"rec:compra:{scope}", IntervalSet.of(NEVER, NEVER)
    gloss = f"prospects (nunca compraram{dims.SCOPE_SUFFIX[scope]})"
    return Clause(text, gloss, constraint={key: value})


def _curve(text: str, ctx: Context) -> Clause | None:
    m = re.fullmatch(r"curva ([abc]) com (a empresa|o vendedor)", text)
    if not m:
        return None
    key = f"curva:{'empresa' if m.group(2) == 'a empresa' else 'vendedor'}"
    value = frozenset({m.group(1).upper()})
    return Clause(text, dims.render(key, value, set()), constraint={key: value})


def _revenue_status(text: str, ctx: Context) -> Clause | None:
    m = re.fullmatch(r"status na receita federal definido como (ativa|suspensa|inapta|baixada)", text)
    if not m:
        return None
    value = frozenset({m.group(1)})
    return Clause(text, dims.render("receita", value, set()), constraint={"receita": value})


BOOLEAN_FILTERS = {
    "adimplentes": ("inadimplente", False), "inadimplentes": ("inadimplente", True),
    "cliente filial": ("filial", True), "o cliente filial": ("filial", True),
    "eh o cliente filial": ("filial", True), "e o cliente filial": ("filial", True),
    "cliente principal": ("filial", False), "o cliente principal": ("filial", False),
    "bloqueados": ("bloqueado", True), "nao bloqueados": ("bloqueado", False),
    "excluidos": ("excluido", True), "nao excluidos": ("excluido", False),
    "tem credito": ("credito", True), "nao tem credito": ("credito", False),
    "tem coordenada confiavel": ("coordenada", True), "nao tem coordenada confiavel": ("coordenada", False),
    "agendavel": ("agendavel", True), "nao agendavel": ("agendavel", False),
    "unica compra com a empresa": ("unica_compra:empresa", True),
    "unica compra com o vendedor": ("unica_compra:vendedor", True),
    "data da rota na semana": ("rota_semana", True),
}


def _person_type(text: str, ctx: Context) -> Clause | None:
    m = re.fullmatch(r"pessoa (fisica|juridica)", text)
    if not m:
        return None
    value = frozenset({m.group(1)})
    return Clause(text, dims.render("pessoa", value, set()), constraint={"pessoa": value})


def _boolean(text: str, ctx: Context) -> Clause | None:
    if text not in BOOLEAN_FILTERS:
        return None
    key, positive = BOOLEAN_FILTERS[text]
    value = frozenset({positive})
    return Clause(text, dims.render(key, value, set()), constraint={key: value})


def _field(text: str, ctx: Context) -> Clause | None:
    fields = "|".join(sorted(map(re.escape, dims.FIELD_LABELS), key=len, reverse=True))
    m = re.fullmatch(rf"({fields})(?: eh)? (igual|diferente|contem|inicia com)\(([^)]*)\)", text)
    if not m:
        return None
    field, op, args = m.groups()
    values = ctx.literals.strings_in(args) or [a.strip() for a in args.split(",") if a.strip()]
    if op in ("igual", "diferente"):
        key, value = f"campo:{field}", dims.ValueSet(frozenset(values), excluding=op == "diferente")
    else:
        key, value = f"campo:{field}:{op}:{'|'.join(values)}", frozenset({True})
    return Clause(ctx.unmask(text), dims.render(key, value, set()), constraint={key: value})


def _segment_membership(text: str, ctx: Context) -> Clause | None:
    m = re.fullmatch(r"(nao )?contido na segmentacao\(([^)]*)\)", text)
    if not m:
        return None
    names = ctx.literals.strings_in(m.group(2))
    constraint = {f"segmentacao:{name}": frozenset({not m.group(1)}) for name in names}
    gloss = " e ".join(dims.render(k, v, set()) for k, v in constraint.items())
    return Clause(ctx.unmask(text), gloss, constraint=constraint)


def _registration_age(text: str, ctx: Context) -> Clause | None:
    m = re.fullmatch(rf"cadastrado (?:faz|ha) {DAYS}", text)
    if not m:
        return None
    n = int(m.group(1))
    value = IntervalSet.of(n)
    return Clause(text, dims.render("cadastro", value, {n}), constraint={"cadastro": value}, numbers=[n])


def _historical_frequency(text: str, ctx: Context) -> Clause | None:
    if m := re.fullmatch(rf"frequencia historica menor que {DAYS}( ou indefinida)?", text):
        n = int(m.group(1))
        value = IntervalSet.of(0, n - 1) | (IntervalSet.of(NEVER, NEVER) if m.group(2) else IntervalSet())
    elif m := re.fullmatch(rf"frequencia historica maior que {DAYS}", text):
        n = int(m.group(1))
        value = IntervalSet.of(n + 1)
    elif m := re.fullmatch(rf"frequencia historica entre {DAYS} e {DAYS}", text):
        value = IntervalSet.of(int(m.group(1)), int(m.group(2)))
    elif m := re.fullmatch(rf"frequencia historica de {DAYS}", text):
        value = IntervalSet.of(int(m.group(1)), int(m.group(1)))
    else:
        return None
    numbers = ints(text)
    return Clause(text, dims.render("freqhist", value, set(numbers)), constraint={"freqhist": value}, numbers=numbers)


FACT_PATTERNS: list[tuple[str, Callable[[re.Match], str]]] = [
    (r"(media faturada|total faturado) no (mes|bimestre|trimestre|semestre|ano) com a empresa (.+)",
     lambda m: f"{'faturamento médio mensal' if m.group(1) == 'media faturada' else 'total faturado'} "
               f"no {m.group(2)} com a empresa {_money(m.group(3))}"),
    (r"com ticket medio (maior que|menor que|igual a) r\$ ?([\d.,]+)(.*)",
     lambda m: f"ticket médio {m.group(1)} R$ {m.group(2)}{_money(m.group(3))}"),
    (r"com (\d+)% de credito", lambda m: f"com pelo menos {m.group(1)}% do limite de crédito disponível"),
    (r"com menos de r\$ ?([\d.,]+) de credito disponivel", lambda m: f"com menos de R$ {m.group(1)} de crédito disponível"),
    (r"com limite de r\$ ?([\d.,]+) de credito", lambda m: f"com limite de crédito de pelo menos R$ {m.group(1)}"),
    (r"queda de faturamento (maior|menor) que (\d+)%", lambda m: f"queda de faturamento {m.group(1)} que {m.group(2)}%"),
    (r"cadastrado a partir do dia (<d\d+>)", lambda m: f"cadastrados a partir de {m.group(1)}"),
    (r"(nao )?tem (\d+)% de visita (remota|incerta) (.+)",
     lambda m: f"{'sem ' if m.group(1) else ''}pelo menos {m.group(2)}% de visitas {m.group(3)}s {describe_period(m.group(4)) or m.group(4)}"),
    (r"(tem|nao tem) visita(?: da empresa| do vendedor)? (.+)",
     lambda m: f"{'com' if m.group(1) == 'tem' else 'sem'} visita {describe_period(m.group(2)) or m.group(2)}"),
    (r"data da rota (futura )?(do vendedor )?(.+)",
     lambda m: f"com data de rota{' futura' if m.group(1) else ''}{' do vendedor' if m.group(2) else ''} "
               f"{describe_period(m.group(3)) or m.group(3)}"),
    (r"data da (proxima|ultima) visita do representante (.+)",
     lambda m: f"com {m.group(1)} visita do representante externo {describe_period(m.group(2)) or m.group(2)}"),
    (r"(fora da |na )agenda( do vendedor| global)?( de ruptura| complementar)? (.+)",
     lambda m: f"{'fora' if m.group(1).startswith('fora') else 'presentes'} da agenda{m.group(3) or ''} {describe_period(m.group(4)) or m.group(4)}"),
    (r"(sem|com) contato no ultimo agendamento(?: para (o vendedor|a empresa))?",
     lambda m: f"{m.group(1)} contato no último agendamento"),
    (r"total de compras com (o vendedor|a empresa) (.+)", lambda m: f"total de compras com {m.group(1)} {m.group(2)}"),
    (r"positivado (?:de )?hoje", lambda m: "positivados hoje"),
    (r"elegivel( incluindo roteirizavel)?", lambda m: "elegíveis (não excluídos, ativos e agendáveis)"),
    (r"sem perfil com (o vendedor|a empresa)", lambda m: f"sem perfil de não agendamento com {m.group(1)}"),
    (r"(?:nao )?tem parametro(?: manual)?", lambda m: m.group(0).replace("nao ", "sem ").replace("tem ", "com ")),
    (r"em ruptura global do (bimestre|trimestre|semestre|ano)", lambda m: f"em ruptura global de compra do {m.group(1)}"),
]


def _money(rest: str) -> str:
    rest = rest.strip()
    rest = re.sub(r"r\$ ?", "R$ ", rest)
    return rest.replace("ou indefinido", "(ou valor desconhecido)")


def _fact_catalogue(text: str, ctx: Context) -> Clause | None:
    for pattern, gloss in FACT_PATTERNS:
        if m := re.fullmatch(pattern, text):
            return _fact(ctx.unmask(text), ctx.unmask(gloss(m)))
    return None


def _fact(text: str, gloss: str) -> Clause:
    """The key carries the source text so two clauses with similar glosses stay distinct facts."""
    key = f"fato:{gloss}{dims.FACT_SOURCE_SEPARATOR}{text}"
    return Clause(text, gloss, constraint={key: frozenset({True})}, numbers=ints(text))


FILTER_MATCHERS: list[Matcher] = [
    _recency, _activity, _situation, _lifecycle, _curve, _revenue_status, _person_type, _boolean, _field,
    _segment_membership, _historical_frequency, _registration_age, _fact_catalogue,
]


def parse_filter(text: str, ctx: Context) -> Clause:
    for matcher in FILTER_MATCHERS:
        if clause := matcher(text, ctx):
            return clause
    shown = ctx.unmask(text)
    return Clause(shown, "", recognized=False, constraint={f"opaco:{shown}": frozenset({True})})


def split_conjunction(text: str) -> list[str]:
    """Split on top-level ' e ', re-joining the halves of 'entre X e Y', 'maior que ... e menor que'
    and 'no minimo ... e no maximo'."""
    pieces, depth, current = [], 0, ""
    tokens = re.split(r"(\(|\)| e )", text)
    for token in tokens:
        if token == "(":
            depth += 1
        elif token == ")":
            depth -= 1
        if token == " e " and depth == 0:
            pieces.append(current.strip())
            current = ""
        else:
            current += token
    pieces.append(current.strip())
    merged: list[str] = []
    for piece in pieces:
        if merged and re.match(r"^(\d|<d\d+>|menor que|maior que|igual a|no maximo|r\$)", piece):
            merged[-1] = f"{merged[-1]} e {piece}"
        elif piece:
            merged.append(piece)
    return merged


# ---------------------------------------------------------------- temporal filters (when the rule runs)

def parse_temporal(text: str, ctx: Context) -> Clause:
    gloss = _temporal_gloss(text)
    if gloss is None:
        return Clause(ctx.unmask(text), "", recognized=False)
    return Clause(ctx.unmask(text), gloss, numbers=ints(text))


def _temporal_gloss(text: str) -> str | None:
    if m := re.fullmatch(r"n[oa] (segunda|terca|quarta|quinta|sexta|sabado|domingo)(?:-feira)?", text):
        return f"somente quando executada {'no' if m.group(1) in ('sabado', 'domingo') else 'na'} {WEEKDAYS[m.group(1)]}"
    simple = {
        "nos dias uteis": "somente quando executada em dias úteis",
        "no fim de semana": "somente quando executada no fim de semana",
        "todos os dias": "todos os dias",
        "no ultimo dia do mes": "somente no último dia do mês",
        "na primeira quinzena": "somente na primeira quinzena do mês (dias 1 a 15)",
        "na segunda quinzena": "somente na segunda quinzena do mês (dia 16 em diante)",
    }
    if text in simple:
        return simple[text]
    if m := re.fullmatch(r"no dia (\d+)", text):
        return f"somente no dia {m.group(1)} de cada mês"
    if m := re.fullmatch(r"(antes|depois|a partir) do dia (\d+)", text):
        word = {"antes": "antes do", "depois": "depois do", "a partir": "a partir do"}[m.group(1)]
        return f"somente {word} dia {m.group(2)} de cada mês"
    if m := re.fullmatch(r"entre os dias (\d+) e (\d+)", text):
        return f"somente entre os dias {m.group(1)} e {m.group(2)} de cada mês"
    if m := re.fullmatch(r"na (primeira|segunda|terceira|quarta|ultima) semana", text):
        return f"somente na {ORDINAL_WEEKS[m.group(1)]} semana do mês"
    if m := re.fullmatch(r"(?:em|no) (janeiro|fevereiro|marco|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro)", text):
        return f"somente em {m.group(1)}"
    if m := re.fullmatch(r"no (primeiro|segundo|terceiro|quarto|quinto|sexto) (bimestre|trimestre|semestre)", text):
        return f"somente no {m.group(1)} {m.group(2)} do ano"
    return None


# ---------------------------------------------------------------- actions

def parse_action(text: str, ctx: Context) -> Clause:
    for matcher in (_schedule_block, _frequency, _preference, _flags, _no_clash, _restricted):
        if clause := matcher(text, ctx):
            return clause
    return Clause(ctx.unmask(text), "", recognized=False)


def _schedule_block(text: str, ctx: Context) -> Clause | None:
    if text == "nao agendar":
        return Clause(text, "não agendar", detail={"tipo": "nao_agendar"})
    return None


def _frequency(text: str, ctx: Context) -> Clause | None:
    m = re.fullmatch(r"frequencia (.+)", text)
    if not m:
        return None
    options = [opt.strip() for opt in re.split(r" ou ", m.group(1))]
    alternatives = [_frequency_option(opt) for opt in options]
    if any(a is None for a in alternatives):
        return None
    gloss = "frequência " + alternatives[0]
    for option, phrase in zip(options[1:], alternatives[1:]):
        # P9: "ou no minimo/no maximo" bounds the frequency computed so far; any other "ou" is a fallback.
        gloss += f", {phrase}" if option.startswith(("no minimo", "no maximo")) else f"; se não houver, {phrase}"
    numbers = ints(text)
    days = [FIXED_FREQUENCIES[k] for k in re.findall(r"(\w+)\(", text) if k in FIXED_FREQUENCIES]
    return Clause(ctx.unmask(text), gloss, numbers=numbers,
                  detail={"tipo": "frequencia", "dias_equivalentes": days})


def _frequency_option(option: str) -> str | None:
    if m := re.fullmatch(f"de {DAYS}", option):
        return f"de {m.group(1)} dias"
    if m := re.fullmatch(r"(\w+)\((<d\d+>)?\)", option):
        if m.group(1) in FIXED_FREQUENCIES:
            pivot = f" a partir da data {m.group(2)}" if m.group(2) else ""
            return f"{m.group(1)} ({FIXED_FREQUENCIES[m.group(1)]} dias){pivot}"
    if m := re.fullmatch(r"de (ativos|inativos) (da empresa|do vendedor)", option):
        return f"média dos clientes {m.group(1)} {m.group(2)}"
    if m := re.fullmatch(r"do (vendedor|govendas|historico)(?: (mais|menos) (\d+) dias?)?", option):
        base = {"vendedor": "configurada pelo vendedor", "govendas": "padrão do Govendas",
                "historico": "calculada pelo histórico de visitas"}[m.group(1)]
        return f"{base}{f' {m.group(2)} {m.group(3)} dias' if m.group(2) else ''}"
    if option == "de qualquer vendedor":
        return "configurada por qualquer vendedor"
    if option == "remover":
        return "remover a frequência existente"
    if m := re.fullmatch(r"(do historico(?: mais \d+ dias?)?) (no (?:minimo|maximo) .+)", option):
        head = _frequency_option(m.group(1))
        return f"{head}, {_frequency_limits(m.group(2))}" if head else None
    if option.startswith("no minimo") or option.startswith("no maximo"):
        return _frequency_limits(option)
    return None


def _frequency_limits(text: str) -> str:
    text = re.sub(r"no minimo de (\d+) dias?", r"no mínimo \1 dias", text)
    text = re.sub(r"no maximo de (\d+) dias?", r"no máximo \1 dias", text)
    text = re.sub(r"no (minimo|maximo) (\w+)\(\)", lambda m: f"no {'mínimo' if m.group(1) == 'minimo' else 'máximo'} "
                  f"{FIXED_FREQUENCIES.get(m.group(2), m.group(2))} dias", text)
    return f"limitada a {text}"


INTENSITY = {"maior": 3, "normal": 2, "menor": 1}


def _preference(text: str, ctx: Context) -> Clause | None:
    m = re.fullmatch(r"preferencia ?(.*)", text)
    if not m:
        return None
    spec = m.group(1).strip()
    dynamic = {"do vendedor": "preferência de dias configurada pelo vendedor",
               "do historico": "preferência de dias calculada pelo histórico de visitas",
               "do historico ou remover": "preferência pelo histórico de visitas; sem histórico, remove a preferência",
               "do historico ou nos dias uteis": "preferência pelo histórico de visitas; sem histórico, dias úteis"}
    if spec in dynamic:
        return Clause(text, dynamic[spec], detail={"tipo": "preferencia"})
    weights: dict[str, int] = {}
    for item in split_conjunction(spec):
        im = re.fullmatch(r"(?:(maior|normal|menor) )?(?:nos dias uteis|n[oa] (\w+?)(?:-feira)?|todos os dias|no fim de semana)", item)
        if not im:
            return None
        intensity = INTENSITY[im.group(1) or "normal"]
        if "dias uteis" in item:
            days = WORKDAYS
        elif "todos os dias" in item:
            days = list(WEEKDAYS)
        elif "fim de semana" in item:
            days = ["sabado", "domingo"]
        elif im.group(2) in WEEKDAYS:
            days = [im.group(2)]
        else:
            return None
        for day in days:
            weights[day] = intensity
    label = {3: "maior preferência", 2: "preferência", 1: "menor preferência"}
    groups = []
    for level in (3, 2, 1):
        chosen = [WEEKDAYS[d] for d in WEEKDAYS if weights.get(d) == level]
        if chosen:
            groups.append(f"{label[level]}: {', '.join(chosen)}")
    gloss = "dias de atendimento - " + "; ".join(groups) + "; demais dias sem atendimento"
    return Clause(text, gloss, detail={"tipo": "preferencia"})


def _flags(text: str, ctx: Context) -> Clause | None:
    flags = {"fixo": "parametrização fixa (restrição rígida de frequência e dias para o gerador de agendas)",
             "roteirizavel": "cliente incluído na roteirização de visitas presenciais",
             "nao roteirizavel": "cliente fora da roteirização de visitas presenciais"}
    return Clause(text, flags[text], detail={"tipo": text}) if text in flags else None


def _no_clash(text: str, ctx: Context) -> Clause | None:
    m = re.fullmatch(r"sem choque( na rota| fora da rota)?( e na pasta)? (?:com |n[oa] )?(time|carteira)\(([^)]*)\)", text)
    if not m:
        return None
    target = ", ".join(ctx.literals.strings_in(m.group(4)))
    scope = {" na rota": " (apenas clientes roteirizáveis)", " fora da rota": " (apenas clientes não roteirizáveis)"}.get(m.group(1) or "", "")
    gloss = f"evitar que os dias de atendimento coincidam com os do {m.group(3)} {target}{scope}"
    return Clause(ctx.unmask(text), gloss, detail={"tipo": "sem_choque"})


def _restricted(text: str, ctx: Context) -> Clause | None:
    m = re.fullmatch(r"restrito (a partir da|ate a) (primeira|segunda|terceira|quarta) semana", text)
    if not m:
        return None
    week = ORDINAL_WEEKS[m.group(2)]
    gloss = f"só pode entrar na agenda {'a partir da' if m.group(1) == 'a partir da' else 'até a'} {week} semana do mês"
    return Clause(text, gloss, detail={"tipo": "restrito"})


# ---------------------------------------------------------------- sources

def parse_rule_source(text: str, ctx: Context) -> Clause:
    """'do time("a","b")', 'da carteira("x")', 'da segmentacao("s")', joined by ' e '."""
    alternatives, glosses, undeclared = [], [], []
    for part in split_conjunction(text):
        m = re.fullmatch(r"d[oa]s? (time|carteira|segmentacao)\(([^)]*)\)", part)
        if not m:
            return Clause(ctx.unmask(text), "", recognized=False)
        kind, names = m.group(1), ctx.literals.strings_in(m.group(2))
        undeclared += [n for n in names if n not in ctx.teams]
        fallback = (lambda n: frozenset({n})) if kind == "time" else (lambda n: frozenset())
        teams = frozenset().union(*(ctx.teams.get(n, fallback(n)) for n in names))
        constraint: dict = {"time": dims.ValueSet(teams)} if teams else {}
        if kind == "carteira":
            # P7: a client is reached through one carteira at a time, so listing several means "any of them".
            constraint["carteira"] = dims.ValueSet(frozenset(names))
        elif kind == "segmentacao":
            for name in names:
                constraint[f"segmentacao:{name}"] = frozenset({True})
        alternatives.append(constraint)
        glosses.append(f"{'do time' if kind == 'time' else 'da ' + kind} {', '.join(names)}")
    detail = {"fontes_nao_declaradas": undeclared, "fontes": ctx.literals.strings_in(text)}
    if len(alternatives) > 1:
        # P8: 'da segmentacao("x") e da carteira("y")' lists two client sources; the rule covers both (a union).
        detail["alternativas"] = alternatives
    return Clause(ctx.unmask(text), " e ".join(glosses), constraint=alternatives[0] if len(alternatives) == 1 else {},
                  detail=detail)


def parse_seller_selection(text: str, ctx: Context) -> Clause:
    m = re.fullmatch(r"vendedores (todostelevendas|todosdecampo|todos|porid\([^)]*\))(.*)", text)
    if not m:
        return Clause(ctx.unmask(text), "", recognized=False)
    base, modifiers = m.groups()
    kinds = {"todostelevendas": "todos os vendedores de televendas", "todosdecampo": "todos os vendedores de campo",
             "todos": "todos os vendedores"}
    gloss = kinds.get(base) or f"os vendedores de id {', '.join(ctx.literals.strings_in(base))}"
    for mod in re.finditer(r"(ativados|inativados|menos\([^)]*\)|dos supervisores\([^)]*\)|do supervisor\([^)]*\))", modifiers):
        token = mod.group(1)
        if token == "ativados":
            gloss += " habilitados no Govendas"
        elif token == "inativados":
            gloss += " desabilitados no Govendas"
        elif token.startswith("menos"):
            gloss += f", exceto os de id {', '.join(ctx.literals.strings_in(token))}"
        else:
            gloss += f" dos supervisores de id {', '.join(ctx.literals.strings_in(token))}"
    return Clause(ctx.unmask(text), gloss)


def parse_client_source(text: str, ctx: Context) -> Clause:
    """'clientes <função>' of carteira/segmentacao blocks."""
    names = ctx.literals.strings_in(text)
    patterns = [
        (r"clientes carteirafixa\(([^)]*)\)", lambda: f"carteira fixa dos vendedores do time {', '.join(names)}"),
        (r"clientes carteiraacessivel\(([^)]*)\)", lambda: f"carteira acessível do time {', '.join(names)}"),
        (r"clientes carteiraruptura\(([^)]*)\)", lambda: f"carteira de ruptura pré-calculada do time {', '.join(names)}"),
        (r"clientes portfolio\(([^)]*)\)", lambda: f"portfólio completo do time {', '.join(names)}"),
        (r"clientes todos\(([^)]*)\)", lambda: f"todos os clientes do sistema, para o time {', '.join(names)}"),
        (r"clientes segmentados\(([^)]*)\)", lambda: f"clientes da segmentação {', '.join(names)}"),
        (r"clientes inativos\((.*)\)", lambda: f"clientes inativos do time {names[0] if names else ''} há pelo menos {_tail(text)}"),
        (r"clientes ruptura(?: da segmentacao)?\(<s\d+> para <s\d+>\)(.*)",
         lambda: f"clientes de {names[0]} em ruptura{_rupture(text)}, transferidos para {names[1]}"),
    ]
    for pattern, gloss in patterns:
        if re.fullmatch(pattern, text):
            return Clause(ctx.unmask(text), gloss(), numbers=ints(text))
    return Clause(ctx.unmask(text), "", recognized=False)


def _tail(text: str) -> str:
    m = re.search(r",\s*(.+)\)$", text)
    return m.group(1) if m else ""


def _rupture(text: str) -> str:
    parts = []
    for kind, arg, prospects in re.findall(r"de (positivacao|visita|inativos)\(([^)]*)\)( ou prospects)?", text):
        noun = {"positivacao": "sem compra", "visita": "sem visita", "inativos": "inativos"}[kind]
        arg = re.sub(r"entre (\d+) dias? e (\d+) dias?", r"entre \1 e \2 dias", arg)
        parts.append(f"{noun} há {arg}{' (incluindo prospects)' if prospects else ''}")
    return (" de " + " e ".join(parts)) if parts else ""

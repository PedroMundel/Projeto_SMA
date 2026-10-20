"""Lexing of .gobr sources: comments, string masking, accent folding and logical lines.

Literals are masked before folding so that keywords can be matched without accents
while the content of strings ("Cordeirópolis") is preserved verbatim.
"""
import re
import unicodedata
from dataclasses import dataclass, field

STRING_RE = re.compile(r'"[^"]*"|\'[^\']*\'')
CONTROL_CHARS_RE = re.compile(r"[\x00-\x08\x0b-\x1f\x7f]")
PLACEHOLDER_RE = re.compile(r"<([sd])(\d+)>")
HEADER_RE = re.compile(
    r"^(?P<kind>limpar parametros|parametros|time|carteira livre|carteira|segmentacao|alerta|tag)"
    r"\s*(?P<name><s\d+>.*?)\s*:\s*$"
)
CONTINUATION_START_RE = re.compile(
    r"^(e |ou |\)|,|<s\d+>|de (positivacao|visita|inativos)|dos supervisores|do supervisor|"
    r"ativados|inativados|menos)"
)
OPEN_ENDING_RE = re.compile(r"(\be|\bou|,|\(|^preferencia|^quando)$")


@dataclass
class Literals:
    """Original text of every masked literal, indexed by placeholder number."""

    strings: list[str] = field(default_factory=list)
    dates: list[str] = field(default_factory=list)

    def mask(self, line: str) -> str:
        def replace(match: re.Match) -> str:
            token = match.group(0)
            bucket, tag = (self.strings, "s") if token[0] == '"' else (self.dates, "d")
            bucket.append(token[1:-1])
            return f"<{tag}{len(bucket) - 1}>"

        return STRING_RE.sub(replace, line)

    def strings_in(self, text: str) -> list[str]:
        return [self.strings[int(n)] for tag, n in PLACEHOLDER_RE.findall(text) if tag == "s"]

    def unmask(self, text: str) -> str:
        def replace(match: re.Match) -> str:
            tag, index = match.group(1), int(match.group(2))
            return f'"{self.strings[index]}"' if tag == "s" else f"'{self.dates[index]}'"

        return PLACEHOLDER_RE.sub(replace, text)


@dataclass
class LogicalLine:
    text: str  # folded, literals masked
    line_no: int
    indented: bool


def fold(text: str) -> str:
    """Lowercase and strip accents; the verb 'é' becomes 'eh' so it never reads as the connective 'e'."""
    text = CONTROL_CHARS_RE.sub("", unicodedata.normalize("NFC", text))
    text = re.sub(r"(?<!\w)[éÉ](?!\w)", "eh", text)
    decomposed = unicodedata.normalize("NFKD", text)
    stripped = "".join(ch for ch in decomposed if not unicodedata.combining(ch))
    return re.sub(r"\s+", " ", stripped.lower()).strip()


def strip_comment(line: str) -> str:
    in_quote = None
    for index, ch in enumerate(line):
        if ch in "\"'" and in_quote in (None, ch):
            in_quote = None if in_quote else ch
        elif ch == "#" and in_quote is None:
            return line[:index]
    return line


def logical_lines(source: str, literals: Literals) -> list[LogicalLine]:
    """Join physical lines into statements: a line continues the previous one when it starts with a
    connective/modifier, or when the previous one is left open (trailing 'e', comma, unbalanced paren)."""
    lines: list[LogicalLine] = []
    for line_no, raw in enumerate(source.splitlines(), start=1):
        code = strip_comment(raw)
        if not code.strip():
            continue
        text = fold(literals.mask(code))
        indented = code[:1] in (" ", "\t")
        previous = lines[-1] if lines else None
        if previous and indented and previous.indented and _continues(previous.text, text):
            separator = "" if previous.text.endswith("(") or text.startswith(")") else " "
            previous.text = f"{previous.text}{separator}{text}"
            continue
        lines.append(LogicalLine(text, line_no, indented))
    for line in lines:
        line.text = re.sub(r"\s*\(\s*", "(", line.text)
        line.text = re.sub(r"\s*,\s*", ",", line.text)
        line.text = re.sub(r"\s*\)", ")", line.text)
    return lines


def _continues(previous: str, current: str) -> bool:
    return (
        previous.count("(") > previous.count(")")
        or bool(OPEN_ENDING_RE.search(previous))
        or bool(CONTINUATION_START_RE.match(current))
    )

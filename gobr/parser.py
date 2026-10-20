"""Structural parser: logical lines -> blocks -> classified clauses."""
import re
from pathlib import Path

from gobr import catalogue
from gobr.catalogue import Context
from gobr.ir import Block, Clause, GobrFile
from gobr.text import HEADER_RE, Literals, LogicalLine, logical_lines

ACTION_START_RE = re.compile(
    r"^(frequencia|preferencia|nao agendar|fixo|roteirizavel|nao roteirizavel|sem choque|restrito)\b"
)
SOURCE_START_RE = re.compile(r"^d[oa]s? (time|carteira|segmentacao)\(")
BLOCK_PREFIX = {"time": "T", "carteira": "C", "carteira livre": "C", "segmentacao": "S",
                "parametros": "R", "limpar parametros": "L", "alerta": "A", "tag": "G"}


def read_source(path: Path) -> str:
    raw = path.read_bytes()
    for encoding in ("utf-8-sig", "cp1252"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    return raw.decode("latin-1")


def parse_file(path: Path) -> GobrFile:
    source = read_source(path)
    literals = Literals()
    lines = logical_lines(source, literals)
    header_comments = [l.strip("# ").strip() for l in source.splitlines()
                       if l.strip().startswith("#") and l.strip("# ").strip()]
    raw_blocks = _group_blocks(lines, literals)
    teams = _resolve_teams(raw_blocks, literals)
    ctx = Context(literals, teams)
    blocks = [_build_block(kind, name, line_no, body, ctx) for kind, name, line_no, body in raw_blocks]
    _number_blocks(blocks)
    return GobrFile(header_comments, blocks, teams)


def _group_blocks(lines: list[LogicalLine], literals: Literals) -> list[tuple[str, str, int, list[str]]]:
    blocks: list[tuple[str, str, int, list[str]]] = []
    for line in lines:
        header = HEADER_RE.match(line.text)
        if header:
            name = literals.unmask(header.group("name"))[1:-1]
            blocks.append((header.group("kind"), name, line.line_no, []))
        elif blocks:
            blocks[-1][3].append(line.text)
    return blocks


def _resolve_teams(raw_blocks, literals: Literals) -> dict[str, frozenset[str]]:
    """Map every time/carteira/segmentacao name to the root teams whose clients it holds."""
    teams = {name: frozenset({name}) for kind, name, _, _ in raw_blocks if kind == "time"}
    derived = [(name, body) for kind, name, _, body in raw_blocks if kind in ("carteira", "carteira livre", "segmentacao")]
    for _ in range(2):  # the second pass resolves references to blocks declared later in the file
        for name, body in derived:
            roots: set[str] = set()
            for statement in body:
                if statement.startswith("clientes "):
                    names = literals.strings_in(statement)
                    if " para " in statement:
                        names = names[1:2]
                    for ref in names:
                        roots |= teams.get(ref, frozenset())
            teams[name] = frozenset(roots)
    return teams


def _build_block(kind: str, name: str, line_no: int, body: list[str], ctx: Context) -> Block:
    block = Block(id="", kind=kind, name=name, line_no=line_no)
    for statement in body:
        _classify(statement, block, ctx)
    return block


def _classify(statement: str, block: Block, ctx: Context) -> None:
    if statement.startswith("vendedores "):
        block.sources.append(catalogue.parse_seller_selection(statement, ctx))
    elif statement.startswith("clientes "):
        block.sources.append(catalogue.parse_client_source(statement, ctx))
    elif SOURCE_START_RE.match(statement):
        block.sources.append(catalogue.parse_rule_source(statement, ctx))
    elif statement.startswith("quando"):
        filters = re.sub(r"^quando\s*(?:e |eh (?=o cliente))?", "", statement)
        block.filters += [catalogue.parse_filter(piece, ctx) for piece in catalogue.split_conjunction(filters)]
    elif ACTION_START_RE.match(statement):
        block.actions.append(catalogue.parse_action(statement, ctx))
    elif block.kind in ("parametros", "alerta") and not block.filters and not block.actions:
        block.temporal += [catalogue.parse_temporal(p, ctx) for p in catalogue.split_conjunction(statement)]
    else:
        block.unclassified.append(ctx.unmask(statement))


def _number_blocks(blocks: list[Block]) -> None:
    counters: dict[str, int] = {}
    for block in blocks:
        prefix = BLOCK_PREFIX[block.kind]
        counters[prefix] = counters.get(prefix, 0) + 1
        block.id = f"{prefix}{counters[prefix]}"


def unrecognized(file: GobrFile) -> list[tuple[str, Clause | str]]:
    found: list[tuple[str, Clause | str]] = []
    for block in file.blocks:
        found += [(block.id, c) for c in block.all_clauses() if not c.recognized]
        found += [(block.id, s) for s in block.unclassified]
    return found

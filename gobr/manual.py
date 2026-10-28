"""Extração do manual GoBR (PDF) em seções e chunks para o índice.

O texto já convertido (docs/manual_gobr.txt) desalinha as tabelas de duas colunas: a descrição de uma
linha aparece ao lado da cláusula seguinte. Por isso a fonte aqui é o PDF, lido com pdfplumber.

- Fora: cabeçalho (corpo 6) e rodapé (©) de página, réguas pontilhadas e as páginas antes do capítulo 1.
- Título: negrito numerado ("6.2 Filtros de recência ..."). Se ele quebra em duas linhas, a linha seguinte
  em negrito do mesmo corpo, antes de qualquer conteúdo, continua o título.
- Código: linha toda em Courier.
- A seta desenhada com o fonte Symbol sai do PDF como "ﬁ"; vira "→".
- Tabelas: `find_tables`. Uma tabela sem cabeçalho logo depois de outra com o mesmo número de colunas é
  continuação (quebra de página); célula da 1ª coluna vazia continua a linha anterior.

Chunks: uma linha de tabela por chunk e a prosa (com os exemplos de código inteiros) por seção, sempre
com o caminho de títulos como contexto. Cada chunk aponta para a seção, que guarda o texto completo.
"""
import re
from dataclasses import dataclass, field
from pathlib import Path

HEADING = re.compile(r"(\d+(?:\.\d+)*)\.?\s+(\S.*)")
CODE_FONT = "Courier"
MAX_PROSE = 1500  # caracteres por chunk de prosa; acima disso, quebra entre blocos, nunca dentro de código


@dataclass
class Section:
    number: str
    title: str
    page: int
    path: list[str]
    blocks: list[tuple[str, object]] = field(default_factory=list)  # ("texto"|"codigo", str) ou ("tabela", rows)
    code_x: float = 0.0  # margem do bloco de código aberto, base da indentação


def _font(char: dict) -> str:
    return char["fontname"].split("+")[-1]


def _is_noise(line: dict, page_height: float) -> bool:
    text = line["text"].strip()
    return (line["chars"][0]["size"] < 7 or text.startswith("©") or not text.strip(". ")
            or line["top"] > page_height - 60)


def _line_text(line: dict) -> str:
    text = line["text"].strip()
    if any("Symbol" in _font(c) for c in line["chars"]):  # o pdfplumber já expandiu a ligadura "ﬁ" para "fi"
        text = re.sub(r"(?<!\w)(?:fi)+(?!\w)", "→", text)
    return text


def _code_line(line: dict, base_x: float) -> str:
    width = line["chars"][0]["width"] or 6.0
    return " " * max(round((line["x0"] - base_x) / width), 0) + line["text"].rstrip()


def _clean(cell: str | None) -> str:
    return re.sub(r"\s+", " ", cell or "").strip()


def _table_rows(table, page) -> tuple[bool, list[list[str]]]:
    rows = [[_clean(c) for c in row] for row in table.extract()]
    for col in reversed(range(1, len(rows[0]) if rows else 0)):
        if sum(bool(r[col]) for r in rows) <= len(rows) // 10:  # coluna fantasma: o texto vai para a vizinha
            rows = [r[:col - 1] + [f"{r[col - 1]} {r[col]}".strip()] + r[col + 1:] for r in rows]
    first = page.crop(table.rows[0].bbox).chars if table.rows else []
    has_header = bool(first) and all("Bold" in _font(c) for c in first if c["text"].strip())
    return has_header, rows


def _page_items(page) -> list[tuple[float, str, object]]:
    """(topo, tipo, conteúdo) em ordem de leitura: linhas fora das tabelas e as tabelas."""
    tables = page.find_tables()
    boxes = [t.bbox for t in tables]
    items = [(t.bbox[1], "tabela", _table_rows(t, page)) for t in tables]
    for line in page.extract_text_lines():
        middle = (line["top"] + line["bottom"]) / 2
        if _is_noise(line, page.height) or any(b[1] <= middle <= b[3] for b in boxes):
            continue
        items.append((line["top"], "linha", line))
    return sorted(items, key=lambda item: item[0])


def extract(pdf_path: Path) -> list[Section]:
    import pdfplumber  # import tardio: o resto do pacote roda só com a biblioteca padrão

    sections: list[Section] = []  # vazio até o capítulo 1: capa e índice ficam de fora
    heading_size = 0.0
    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, 1):
            for _, kind, item in _page_items(page):
                if kind == "linha":
                    first = item["chars"][0]
                    bold = "Bold" in _font(first) and CODE_FONT not in _font(first)
                    match = HEADING.fullmatch(item["text"].strip())
                    if match and bold and first["size"] >= 9.5:
                        number, title = match.groups()
                        if sections or number == "1":
                            parents = [s for s in sections if number.startswith(s.number + ".")]
                            path = (parents[-1].path if parents else []) + [f"{number} {title}"]
                            sections.append(Section(number, title, page_number, path))
                            heading_size = first["size"]
                        continue
                    if bold and sections and not sections[-1].blocks and first["size"] == heading_size:
                        current = sections[-1]  # título quebrado em duas linhas
                        current.title += " " + item["text"].strip()
                        current.path[-1] += " " + item["text"].strip()
                        continue
                if not sections:
                    continue
                _add(sections[-1], kind, item)
    return sections


def _add(section: Section, kind: str, item) -> None:
    blocks = section.blocks
    last = blocks[-1] if blocks else (None, None)
    if kind == "tabela":
        has_header, rows = item
        if not has_header and last[0] == "tabela" and rows and len(rows[0]) == len(last[1][0]):
            _extend_table(last[1], rows)  # continuação depois da quebra de página
        else:
            blocks.append(("tabela", rows if has_header else [[""] * len(rows[0])] + rows))
        return
    if all(CODE_FONT in _font(c) for c in item["chars"] if c["text"].strip()):
        if last[0] == "codigo":
            blocks[-1] = ("codigo", last[1] + "\n" + _code_line(item, section.code_x))
        else:
            section.code_x = item["x0"]
            blocks.append(("codigo", _code_line(item, item["x0"])))
    elif last[0] == "texto":
        blocks[-1] = ("texto", last[1] + "\n" + _line_text(item))
    else:
        blocks.append(("texto", _line_text(item)))


def _extend_table(rows: list[list[str]], more: list[list[str]]) -> None:
    for row in more:
        if not row[0] and rows:
            rows[-1] = [f"{a} {b}".strip() for a, b in zip(rows[-1], row)]
        else:
            rows.append(row)


def render(section: Section) -> str:
    """Texto completo da seção (Markdown), devolvido ao agente quando um chunk dela é recuperado."""
    out = [f"{'#' * min(section.number.count('.') + 2, 4)} {section.number} {section.title}"]
    for kind, content in section.blocks:
        if kind == "tabela":
            header, *rows = content
            out.append("\n".join(["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
                                 + ["| " + " | ".join(c.replace("|", "\\|") for c in r) + " |" for r in rows]))
        elif kind == "codigo":
            out.append(f"```\n{content}\n```")
        else:
            out.append(_join_lines(content))
    return "\n\n".join(out)


def _join_lines(text: str) -> str:
    """Junta linhas quebradas pelo PDF, preservando itens de lista."""
    return re.sub(r"\n(?!\s*(?:•|\d+\.\s|-\s))", " ", text)


def chunks(sections: list[Section]) -> list[dict]:
    out = []
    for section in sections:
        context = " > ".join(section.path)
        prose, size = [], 0
        for kind, content in section.blocks:
            if kind == "tabela":
                header, *rows = content
                if len(header) == 1:  # lista de opções: um chunk só, linhas soltas seriam curtas demais
                    out.append(_chunk(section, "tabela", f"{context}\n{header[0]}: " + "; ".join(r[0] for r in rows)))
                    continue
                for row in rows:
                    cells = [f"{h}: {c}" if h else c for h, c in zip(header, row) if c]
                    out.append(_chunk(section, "tabela", f"{context}\n" + ". ".join(cells)))
                continue
            piece = f"```\n{content}\n```" if kind == "codigo" else _join_lines(content)
            if prose and size + len(piece) > MAX_PROSE:
                out.append(_chunk(section, "prosa", f"{context}\n" + "\n\n".join(prose)))
                prose, size = [], 0
            prose.append(piece)
            size += len(piece)
        if prose:
            out.append(_chunk(section, "prosa", f"{context}\n" + "\n\n".join(prose)))
    return out


def _chunk(section: Section, kind: str, text: str) -> dict:
    return {"secao": section.number, "titulo": section.title, "pagina": section.page, "tipo": kind, "texto": text}

"""Memória da conversa: as regras, em código, do que passa de um turno para o outro.

O LLM só diz quais linhas do pedido mudam; quem aplica, compara o arquivo novo com o anterior e decide o que
do histórico cabe no prompt é este módulo (CASCADE-FIRST). O estado em si fica no grafo (`gobr.agent.State`) e
é guardado pelo checkpointer.
"""
import json
import re

from gobr.index import numbers
from gobr.text import fold

KINDS = ("alterar", "duvida", "novo", "desfazer")
RULE_LABEL = re.compile(r"\bregra\s+\d+", re.IGNORECASE)  # "Regra 01:" numera o pedido, não é um limite
LEFT_OUT = re.compile(r"gobr nao (tem|expressa|possui|permite|suporta|oferece)")  # a forma que o prompt pede nas notas
FUNCTION_WORDS = {"a", "o", "e", "as", "os", "de", "do", "da", "dos", "das", "um", "uma", "em", "no", "na", "nos", "nas", "para", "por", "que",
                  "com", "dias", "dia", "nao", "sem", "ate", "ou", "se", "so", "mais", "menos", "todos", "todas", "outros", "outras", "cliente", "clientes"}
NUMBERING = re.compile(r"^\d+[.)]\s+")  # o pedido vai ao LLM com as linhas numeradas, e ele às vezes copia o número
QUOTED = re.compile(r'"([^"]+)"')
REFERENCE = re.compile(r"\b(ess[ae]s?|iss[oa]|est[ae]s?|mesm[oa]s?|tod[oa]s?|tudo|outr[oa]s?|anterior|ultim[oa]s?|primeir[oa]s?|"
                       r"ambos|dois|duas|linha|resto|demais|corte)\b")  # a mensagem aponta para linhas sem as citar
CRITERION = re.compile(r"\b(compr\w*|venda\w*|pedidos?|recencia|inatividade|atividade|corte|criterio|prazo|ultimos|faixa|entre)\b")
CRITERION_BEFORE = re.compile(r"\b(ultim\w*|ha|mais de|menos de|ate|entre|sem|compr\w*|pedido\w*|inatividade|atividade|recencia|faz)\W+(\w+\W+){0,2}$")  # "nos últimos 30 dias" não é a frequência
FREQUENCY_TAIL = re.compile(r"\b(\d+)( dias?)\W*$")  # "..., 14 dias": o último "N dias" da linha é a frequência
QUESTION = re.compile(r"\?|^\W*(qual|quais|quant\w*|como|por ?que|quem|onde|quando|o que)\b|\b(explic\w*|me (diz|fala|mostra)|"
                      r"duvida|entend\w*|lembr\w*)\b")
ANSWER_PREFIX = "Resposta do usuário ("
CHANGED_ANSWER_PREFIX = "Pedido do usuário ("
HISTORY_CHARS = 4000  # ~1.000 tokens: o efeito dos turnos já está no pedido e no arquivo
MESSAGE_CHARS = 500


def one_line(text: str) -> str:
    return " ".join(text.split())


def short(text: str, limit: int = 300) -> str:
    return text if len(text) <= limit else text[:limit].rstrip() + "…"


def requested_numbers(text: str) -> set[int]:
    """Inteiros do pedido que o .gobr tem de ter: sem o 0, sem "Regra NN" e com 1.500,00 lido como 1500."""
    text = RULE_LABEL.sub(" ", text)
    text = re.sub(r"(?<=\d)\.(?=\d{3}\b)", "", text)
    text = re.sub(r"(?<=\d),\d+", "", text)
    return set(numbers(text)) - {0}


def declared_left_out(notes: str) -> set[int]:
    """Números das linhas das notas que dizem que o GoBR não expressa aquele trecho do pedido."""
    return {n for line in notes.splitlines() if LEFT_OUT.search(fold(line)) for n in requested_numbers(line)}


# --- pedido vigente ---

def request_lines(text: str) -> list[str]:
    return [line.strip() for line in text.splitlines() if line.strip()]


def answer_line(question: str, answer: str) -> str:
    """O que o usuário respondeu vira linha do pedido, e uma mudança posterior pode alterá-la ou removê-la."""
    return f"{ANSWER_PREFIX}{one_line(question)}): {one_line(answer)}"


def binding_text(request: str) -> str:
    """As linhas cujos números o arquivo tem de ter; a resposta a uma pergunta informa, mas não obriga."""
    return "\n".join(line for line in request.splitlines() if not line.startswith(ANSWER_PREFIX))


def parse_interpretation(content: str) -> dict:
    """Tipo da mensagem e operações; JSON ruim não trava, vira tipo vazio."""
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        data = None
    if not isinstance(data, dict):
        data = {}
    version, operations = data.get("versao"), data.get("operacoes")
    return {"tipo": data.get("tipo") if data.get("tipo") in KINDS else "",
            "versao": version if isinstance(version, int) and version > 0 else 0,
            "operacoes": operations if isinstance(operations, list) else []}


def _stems(text: str) -> set[str]:
    return {w.removesuffix("s") for w in re.findall(r"[a-z]{4,}", fold(text))} - {"dia", "dias", "cliente", "para", "agora", "mais"}


def _label_words(line: str) -> set[str]:
    """Palavras do nome do segmento ("MEI: ..."), até as curtas, que `_stems` não vê; a linha de resposta não é um nome."""
    if ":" not in line or line.startswith((ANSWER_PREFIX, CHANGED_ANSWER_PREFIX)):
        return set()
    return {w for w in re.findall(r"\w+", fold(line.split(":")[0])) if not w.isdigit()} - FUNCTION_WORDS


def related(change: dict, message: str) -> bool:
    """A mudança tem a ver com a mensagem: uma palavra em comum, um número dela, ou a mensagem aponta sem citar."""
    if REFERENCE.search(fold(message)) or _stems(message) & _stems(f'{change["antes"]} {change["depois"]}'):
        return True
    said_words = set(re.findall(r"\w+", fold(message)))
    for label in (_label_words(change["antes"]), _label_words(change["depois"])):
        if label and label <= said_words and all(len(w) > 1 for w in label):  # o nome inteiro, não uma palavra dele
            return True
    said = requested_numbers(message)
    return bool(said & (requested_numbers(change["depois"]) | requested_numbers(change["antes"])))


def _criterion_tail(line: str) -> bool:
    """O último "N dias" da linha é o critério ("quem comprou nos últimos 30 dias"), e não a frequência."""
    tail = fold(re.split(r"[,:;(]| - ", line)[-1])
    number = re.search(r"\d+ dias?\W*$", tail)
    return bool(number) and CRITERION_BEFORE.search(tail[:number.start()]) is not None


def _frequency_not_criterion(before: str, after: str, message: str) -> str:
    """"Muda os ativos para 20 dias" é a frequência; o critério só muda se a mensagem fala dele."""
    old, new = FREQUENCY_TAIL.search(before), FREQUENCY_TAIL.search(after)
    said = requested_numbers(message)
    if not old or not new or _criterion_tail(before) or old.group(1) != new.group(1) or len(said) != 1 or CRITERION.search(fold(message)):
        return after
    number = said.pop()
    if number not in requested_numbers(after) - requested_numbers(before):
        return after
    return f"{before[:old.start(1)]}{number}{before[old.end(1):]}"


def left_behind(segments: list[dict], changes: list[dict], message: str) -> list[str]:
    """Segmentos que a mensagem cita e a mudança não toca, quando ela cita mais de um e toca só alguns."""
    words = _stems(message)
    cited = [s for s in segments if _stems(s["segmento"]) and _stems(s["segmento"]) <= words]
    missed = [s["segmento"] for s in cited if not touched(s, changes)]
    return missed if len(cited) > 1 and len(missed) < len(cited) else []


def is_question(message: str) -> bool:
    return QUESTION.search(fold(message)) is not None


def apply_operations(lines: list[str], operations: list, message: str) -> tuple[list[str], list[dict], list[str]]:
    """Linhas novas do pedido, mudanças ({antes, depois}) e avisos. As linhas não citadas ficam idênticas."""
    kept: list[str | None] = list(lines)
    added, changes, warnings, touched = [], [], [], set()
    said = requested_numbers(message)
    for op in operations or []:
        kind, number, text = (op.get("op"), op.get("linha"), one_line(str(op.get("texto") or ""))) if isinstance(op, dict) \
            else (None, None, "")
        before = ""
        if kind in ("alterar", "remover"):
            valid = isinstance(number, int) and not isinstance(number, bool) and 1 <= number <= len(lines)
            if not valid or number in touched:
                reason = f"a linha {number} já tinha mudado" if valid else f"o pedido não tem a linha {number}"
                warnings.append(f"Mudança ignorada: {reason}.")
                continue
            before = lines[number - 1]
        elif kind != "incluir":
            warnings.append("Mudança ignorada: operação desconhecida.")
            continue
        if not NUMBERING.match(before):
            text = NUMBERING.sub("", text)
        after = "" if kind == "remover" else text
        if after != before and after.startswith(ANSWER_PREFIX):  # o usuário mudou o valor: agora é exigido
            after = CHANGED_ANSWER_PREFIX + after[len(ANSWER_PREFIX):]
        if kind == "alterar":
            after = _frequency_not_criterion(before, after, message)
        if kind != "remover" and (not after or after == before):
            warnings.append(f"Mudança ignorada: {'o texto novo é igual ao atual' if after else 'o texto novo está vazio'}.")
            continue
        if kind != "incluir" and not related({"antes": before, "depois": after}, message):
            warnings.append(f'Mudança ignorada: a mensagem não fala da linha "{before}".')
            continue
        if kind == "incluir":
            added.append(after)
        else:
            touched.add(number)
            kept[number - 1] = after or None
        changes.append({"antes": before, "depois": after})
        invented = requested_numbers(after) - requested_numbers(before) - said
        if invented:
            warnings.append(f'Números que não estão na sua mensagem entraram no pedido ("{after}"): '
                            f"{', '.join(map(str, sorted(invented)))}. Confira.")
    lost = said - {n for c in changes for n in requested_numbers(c["antes"]) | requested_numbers(c["depois"])}
    if changes and lost:
        warnings.append(f"Números da sua mensagem que não entraram em nenhuma linha do pedido: "
                        f"{', '.join(map(str, sorted(lost)))}. Confira.")
    return [line for line in kept if line is not None] + added, changes, warnings


def change_text(change: dict) -> str:
    if not change["antes"]:
        return f'incluído: "{change["depois"]}"'
    if not change["depois"]:
        return f'removido: "{change["antes"]}"'
    return f'de "{change["antes"]}" para "{change["depois"]}"'


# --- segmentos e regras ---

def segment_of(rule_name: str, segments: list[dict]) -> dict | None:
    """Segmento de nome igual ao da regra, ou cujo nome vem antes dos dois-pontos ("Ativos: compra ..." é Ativos)."""
    name = fold(rule_name)
    named = sorted(((fold(s["segmento"]), s) for s in segments), key=lambda pair: -len(pair[0]))
    return next((s for key, s in named if name == key or name.startswith(key + ":")), None)


def mentioned(name: str, changes: list[dict], message: str = "") -> bool:
    """O nome aparece, como palavra inteira, na mensagem ou nas linhas que mudaram ("ativo" não está em "inativo")."""
    text = fold("\n".join([message] + [c["antes"] + "\n" + c["depois"] for c in changes]))
    return re.search(rf"(?<!\w){re.escape(fold(name))}(?!\w)", text) is not None


def touched(segment: dict, changes: list[dict], message: str = "") -> bool:
    """A mudança cita o segmento pelo nome ou mexe na linha do pedido de onde ele saiu."""
    if mentioned(segment["segmento"], changes, message):
        return True
    origin = fold(segment["trecho"])
    return bool(origin) and any(origin in fold(c[side]) or (c[side] and fold(c[side]) in origin)
                                for c in changes for side in ("antes", "depois"))


def is_global(changes: list[dict], segments: list[dict]) -> bool:
    """Alguma mudança não cita segmento nenhum ("todos a cada 10 dias", "o time agora é..."): pode valer para todos."""
    return any(not any(touched(s, [c]) for s in segments) for c in changes)


def _complete(segment: dict) -> bool:
    return bool(segment["criterio"]) and (segment["acao"] == "nao_agendar"
                                          or (segment["acao"] == "agendar" and segment["frequencia_dias"] > 0))


def keep_segments(old: list[dict], new: list[dict], changes: list[dict], message: str) -> list[dict]:
    """Segmento completo que a mudança não cita fica como era, mesmo se a triagem o leu diferente ou o esqueceu.

    A triagem relê o pedido todo a cada turno e pode variar. Mudança que não cita segmento nenhum não congela nada.
    """
    if is_global(changes, old + new):
        return new
    frozen = {fold(s["segmento"]): s for s in old if _complete(s) and not touched(s, changes, message)}
    read = {fold(s["segmento"]) for s in new}
    return [frozen.get(fold(s["segmento"]), s) for s in new] + [s for name, s in frozen.items() if name not in read]


def _clauses(block) -> list[str]:
    return [c.text for c in block.all_clauses()] + list(block.unclassified)


def clauses_with_sources(block, blocks) -> list[str]:
    """Cláusulas da regra e das fontes (time, carteira, segmentação) que ela usa, direta ou indiretamente."""
    sources = {b.name: b for b in blocks if b.kind != "parametros"}
    found, pending, seen = [], [block], set()
    while pending:
        current_block = pending.pop()
        found += _clauses(current_block)
        names = [n for text in _clauses(current_block) for n in QUOTED.findall(text) if n in sources and n not in seen]
        seen.update(names)
        pending += [sources[n] for n in names]
    return found


def _keyed(blocks) -> dict:
    found: dict = {}
    for block in blocks:
        repeat = sum(key[:2] == (block.kind, fold(block.name)) for key in found)
        found[block.kind, fold(block.name), repeat] = block
    return found


def diff_blocks(old_blocks, new_blocks) -> list[str]:
    """O que mudou de um arquivo para o outro, regra a regra."""
    old, new = _keyed(old_blocks), _keyed(new_blocks)
    lines = []
    for key, block in new.items():
        if key not in old:
            lines.append(f'"{block.name}" ({block.kind}): incluída')
            continue
        before, after = _clauses(old[key]), _clauses(block)
        if before != after:
            gone = [c for c in before if c not in after]
            came = [c for c in after if c not in before]
            detail = [f"saiu {'; '.join(f'`{c}`' for c in gone)}"] * bool(gone) \
                + [f"entrou {'; '.join(f'`{c}`' for c in came)}"] * bool(came)
            lines.append(f'"{block.name}" ({block.kind}): {", ".join(detail) or "mudou a ordem das cláusulas"}')
    lines += [f'"{block.name}" ({block.kind}): removida' for key, block in old.items() if key not in new]
    if [k for k in old if k in new] != [k for k in new if k in old]:
        lines.append("a ordem das regras mudou")
    return lines


def untouched_changes(old_blocks, new_blocks, old_segments: list[dict], new_segments: list[dict],
                      changes: list[dict], message: str) -> list[str]:
    """Regra que a mudança não cita não pode mudar (nem as fontes dela), sumir nem trocar de ordem.

    Só julga a regra cujo segmento existe antes e depois, com a mesma ação e frequência, e nada quando alguma
    mudança pode valer para todos; o código não chuta.
    """
    if is_global(changes, old_segments + new_segments):
        return []
    old, new = _keyed(old_blocks), _keyed(new_blocks)
    found, stable = [], []
    for key, block in old.items():
        before = segment_of(block.name, old_segments)
        after = before and next((s for s in new_segments if fold(s["segmento"]) == fold(before["segmento"])), None)
        if block.kind != "parametros" or not after or touched(before, changes, message) \
                or (before["acao"], before["frequencia_dias"]) != (after["acao"], after["frequencia_dias"]):
            continue
        if key not in new:
            found.append(f'"{block.name}": a regra sumiu do arquivo, mas a mudança pedida não fala dela.')
        else:
            was, now = clauses_with_sources(block, old_blocks), clauses_with_sources(new[key], new_blocks)
            if was != now:
                found.append(f'"{block.name}": a regra (ou uma fonte dela) mudou, mas a mudança pedida não fala dela. '
                             f'Antes: {"; ".join(was)}. Agora: {"; ".join(now)}.')
        stable += [key] * (key in new)
    if stable != [key for key in new if key in stable]:
        found.append("A ordem das regras que a mudança pedida não cita mudou: "
                     f'antes, {", ".join(old[k].name for k in stable)}.')
    return found


# --- versões e histórico ---

def version(state: dict, number: int) -> dict | None:
    return next((v for v in state.get("versoes") or [] if v["n"] == number), None)


def current(state: dict) -> dict | None:
    return version(state, state.get("versao_atual") or 0)


def _newest(texts: list[str], limit: int, omitted: str) -> str:
    """Os textos mais novos que cabem no orçamento, em ordem; o último entra sempre."""
    kept, size = [], 0
    for text in reversed(texts):
        size += len(text)
        if kept and size > limit:
            break
        kept.insert(0, text)
    missing = len(texts) - len(kept)
    return "\n".join([f"({missing} {omitted})"] * bool(missing) + kept)


def history_text(turns: list[dict], limit: int = HISTORY_CHARS) -> str:
    texts = []
    for turn in turns:
        text = f'Turno {turn["n"]} ({turn["tipo"]}). Usuário: "{short(one_line(turn["mensagem"]), MESSAGE_CHARS)}". ' \
               f'Resultado: {turn["resumo"]}'
        text += "".join(f" Pergunta do agente: {one_line(q)} Resposta: {one_line(a)}" for q, a in turn["perguntas"])
        texts.append(text)
    return _newest(texts, limit, "turnos anteriores omitidos")


def versions_text(state: dict) -> str:
    """O pedido de cada versão, para responder sobre as anteriores."""
    texts = [f'- versão {v["n"]}{" (atual)" if v["n"] == state.get("versao_atual") else ""}: {"; ".join(v["pedido"])}'
             for v in state.get("versoes", [])]
    return _newest(texts, HISTORY_CHARS, "versões anteriores omitidas")


def summary(state: dict) -> str:
    """O que a conversa guarda, para o usuário ver (/memoria)."""
    lines = ["Pedido vigente:"] + [f"- {line}" for line in state.get("pedido") or ["(nenhum)"]]
    lines += ["Versões:"] + [f'- {v["n"]}{" (atual)" if v["n"] == state.get("versao_atual") else ""}, '
                             f'a partir da {v["pai"] or "estaca zero"}' for v in state.get("versoes") or []]
    return "\n".join(lines + ["Turnos:", history_text(state.get("turnos") or [])])

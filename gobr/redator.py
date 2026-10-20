"""Redator contract: the trimmed package the LLM reads and the Markdown rendered from its JSON answer.

The LLM never sees hashes or number inventories (those feed the validator); it sees meanings
already resolved by the deterministic layer.
"""


def view(package: dict) -> dict:
    return {
        "arquivo": package["arquivo"],
        "comentarios": package["comentarios"],
        "times": [{"nome": t["nome"], "definicao": t["definicao"]} for t in package["times"]],
        "carteiras": [_portfolio_view(c) for c in package["carteiras"]],
        "segmentacoes": [_portfolio_view(s) for s in package["segmentacoes"]],
        "bloqueios": package["bloqueios"],
        "regras": [_rule_view(r) for r in package["regras"]],
        "nao_cobertos": package["nao_cobertos"],
        "alertas_do_arquivo": package["alertas"],
        "premissas_usadas": package["premissas_usadas"],
    }


def _portfolio_view(portfolio: dict) -> dict:
    data = {"id": portfolio["id"], "nome": portfolio["nome"], "definicao": portfolio["definicao"],
            "filtros": [_meaning(f) for f in portfolio["filtros"]]}
    if portfolio.get("livre"):
        data["livre"] = True
    if portfolio.get("exceto_alocados_em"):
        data["exceto_alocados_em"] = portfolio["exceto_alocados_em"]
    return data


def _rule_view(rule: dict) -> dict:
    data = {
        "id": rule["id"],
        "nome": rule["nome"],
        "fonte": rule["fonte"],
        "acao_principal": rule["acao_principal"],
        "acoes": [_meaning(a) for a in rule["acoes"]],
        "condicao_efetiva": rule["condicao_efetiva"],
    }
    if rule["quando_executa"]:
        data["quando_executa"] = [_meaning(t) for t in rule["quando_executa"]]
    if rule["condicao_efetiva"] is None or rule["inalcancavel"]:
        data["condicao_propria"] = rule["condicao_propria"]
    if rule["tratados_antes_por"]:
        data["tratados_antes_por"] = rule["tratados_antes_por"]
    if rule["inalcancavel"]:
        data["inalcancavel"] = True
    unknown = [f["codigo"] for f in rule["filtros"] + rule["acoes"] + rule["quando_executa"] if not f["reconhecida"]]
    if unknown:
        data["clausulas_desconhecidas"] = unknown
    if rule["alertas"]:
        data["alertas"] = rule["alertas"]
    return data


def _meaning(clause: dict) -> str:
    return clause["significado"] or f"[não traduzido: {clause['codigo']}]"


def render_markdown(answer: dict, package: dict) -> str:
    lines = [f"# {package['arquivo']}", "", answer["resumo"], ""]
    if answer.get("carteiras"):
        lines += ["## Carteiras", "", "| Carteira | Descrição |", "|---|---|"]
        lines += [f"| {_cell(c['nome'])} | {_cell(c['descricao'])} |" for c in answer["carteiras"]]
        lines.append("")
    lines += ["## Regras", "", "| Segmento | Critério | Frequência | Observação |", "|---|---|---|---|"]
    lines += [f"| {_cell(r['segmento'])} | {_cell(r['criterio'])} | {_cell(r['frequencia'])} | {_cell(r['observacao'])} |"
              for r in answer["regras"]]
    if answer.get("pontos_de_atencao"):
        lines += ["", "## Pontos de atenção", ""] + [f"- {p}" for p in answer["pontos_de_atencao"]]
    return "\n".join(lines) + "\n"


def _cell(text: str) -> str:
    return text.replace("|", "/").replace("\n", " ")

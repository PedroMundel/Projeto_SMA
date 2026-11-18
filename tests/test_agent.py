import json
import tempfile
import unittest
from pathlib import Path

from gobr import agent, index, manual_search
from tests.test_index import WordHashEmbedder

HEADER = 'Version 1.0\n\ntime "televendas":\n    vendedores todostelevendas ativados\n\n'
VALID = HEADER + (
    'parametros "Ativo":\n    do time("televendas")\n    quando recencia de positivacao global em 60 dias\n'
    '    frequencia de 14 dias\n\n'
    'parametros "Inativo":\n    do time("televendas")\n    frequencia de 28 dias\n'
)
UNKNOWN_CLAUSE = HEADER + 'parametros "Ativo":\n    do time("televendas")\n    quando o cliente sorrir\n    frequencia de 14 dias\n'
UNREACHABLE = HEADER + (
    'parametros "Ativo":\n    do time("televendas")\n    quando recencia de positivacao global em 60 dias\n'
    '    frequencia de 14 dias\n\n'
    'parametros "Ativo recente":\n    do time("televendas")\n    quando recencia de positivacao global em 30 dias\n'
    '    frequencia de 28 dias\n'
)
LATE_BLOCK = VALID.replace('parametros "Inativo"', (
    'parametros "Baixados":\n    do time("televendas")\n    quando status na receita federal definido como baixada\n'
    '    nao agendar\n\nparametros "Inativo"'))
WITH_BLOCK = VALID.replace('parametros "Ativo"', (
    'parametros "Inadimplentes":\n    do time("televendas")\n    quando inadimplentes\n    nao agendar\n\n'
    'parametros "Ativo"'))
REQUEST = "Ativo: clientes com pedido nos últimos 60 dias, 14 dias. Inativo: os demais, 28 dias."
AGREES = {"regras": [{"regra": "Ativo", "trecho_do_pedido": "Ativo", "confere": True, "motivo": "confere"}],
          "sem_regra": []}
DISAGREES = {"regras": [{"regra": "Ativo", "trecho_do_pedido": "Ativo: ..., 14 dias", "confere": False,
                         "motivo": "o pedido manda agendar"}], "sem_regra": ["Prospect: 7 dias"]}


def fenced(text: str, notes: str = "Sem dúvidas.") -> str:
    return f"Segue a regra:\n```gobr\n{text}```\n{notes}"


def call(name: str, args, call_id: str = "c1") -> dict:
    arguments = args if isinstance(args, str) else json.dumps(args)
    return {"role": "assistant", "content": "",
            "tool_calls": [{"id": call_id, "type": "function", "function": {"name": name, "arguments": arguments}}]}


TRIAGED = {"segmentos": [
    {"segmento": "Ativo", "trecho": "Ativo: ...", "criterio": "pedido nos últimos 60 dias", "acao": "agendar",
     "frequencia_dias": 14},
    {"segmento": "Inativo", "trecho": "Inativo: ...", "criterio": "os demais", "acao": "agendar", "frequencia_dias": 28}]}


def _json_list(items, default) -> list[str]:
    return [i if isinstance(i, str) else json.dumps(i) for i in items] or [json.dumps(default)]


class ScriptedChat:
    """LLM falso: agente, triagem e conferente recebem as suas respostas em ordem (repetem a última).

    Padrões: a triagem devolve os segmentos do REQUEST, sem lacunas; o conferente diz que confere.
    """

    def __init__(self, *replies, conference=(), triage=()):
        self.replies = [{"role": "assistant", "content": r} if isinstance(r, str) else r for r in replies]
        self.conference = _json_list(conference, AGREES)
        self.triage = _json_list(triage, TRIAGED)
        self.received, self.tools, self.conferred, self.triaged = [], [], [], []

    def __call__(self, messages: list[dict], tools=None, schema=None) -> dict:
        if schema is agent.TRIAGE_SCHEMA:
            self.triaged.append(messages)
            return {"role": "assistant", "content": self.triage[min(len(self.triaged), len(self.triage)) - 1]}
        if schema is not None:
            self.conferred.append(messages)
            return {"role": "assistant", "content": self.conference[min(len(self.conferred), len(self.conference)) - 1]}
        self.received.append(messages)
        self.tools.append(tools)
        return self.replies[min(len(self.received), len(self.replies)) - 1]


class AgentTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.embedder = WordHashEmbedder()
        files, chunks = {}, []
        entries = [("ativos_a", "s1", "Ativo: clientes com pedido nos últimos 60 dias, 14 dias", VALID),
                   ("ativos_b", "s1", "Ativo: clientes com pedido nos últimos 60 dias, 14 dias, cópia", VALID),
                   ("prospects", "s2", "Prospect: clientes com ciclo de vida prospect, 7 dias", HEADER + "# prospect\n")]
        for name, sig, text, source in entries:
            path = Path(self.tmp.name) / f"{name}.gobr"
            path.write_text(source, encoding="utf-8")
            files[name] = {"assinatura": sig, "descricao": "", "gobr": path.as_posix(),
                           "numeros": sorted(index.numbers(text))}
            chunks.append({"arquivo": name, "tipo": "arquivo", "regra": None, "texto": text})
        self.examples = index.Index(self.embedder.model, chunks, self.embedder.documents([c["texto"] for c in chunks]), files)
        texts = ["SECAO-RECENCIA: recencia de positivacao", "SECAO-BLOQUEIO: nao agendar",
                 "SECAO-CARTEIRA: carteira livre", "SECAO-EVENTOS: eventos complexos"]
        sections = {str(n): {"secao": str(n), "titulo": t.split(":")[0], "pagina": n, "texto": t}
                    for n, t in enumerate(texts, 1)}
        manual_chunks = [{"secao": n, "texto": s["texto"]} for n, s in sections.items()]
        self.manual = manual_search.ManualIndex(
            self.embedder.model, manual_chunks, self.embedder.documents([c["texto"] for c in manual_chunks]), sections,
            manual_search.BM25([manual_search.tokens(c["texto"]) for c in manual_chunks]))
        self.asked = []

    def tearDown(self):
        self.tmp.cleanup()

    def run_graph(self, chat, answers=(), **state) -> dict:
        res = agent.Resources(self.examples, self.manual, self.embedder, chat, whole_manual=state.pop("inteiro", False))
        pending = list(answers)

        def answer(question: str) -> str:
            self.asked.append(question)
            return pending.pop(0) if pending else ""

        return agent.converse(agent.build_graph(res), {"descricao": REQUEST, **state}, answer)

    # preparar: busca inicial

    def test_first_message_has_examples_and_manual(self):
        chat = ScriptedChat(fenced(VALID))
        out = self.run_graph(chat)
        self.assertEqual(out["exemplos"][0]["arquivo"], "ativos_a")
        first = chat.received[0][1]["content"]
        self.assertIn('parametros "Inativo"', first)
        self.assertIn("SECAO-RECENCIA", first)
        self.assertEqual(first.count("<secao "), agent.MANUAL_K)
        self.assertEqual(chat.received[0][0]["content"], agent.PROMPT.read_text(encoding="utf-8"))
        self.assertEqual(chat.tools[0], agent.TOOLS)

    def test_excluded_file_takes_its_signature_out_of_the_search(self):
        out = self.run_graph(ScriptedChat(fenced(VALID)), excluir=["ativos_a"])
        self.assertEqual([e["arquivo"] for e in out["exemplos"]], ["prospects"])

    def test_excluding_an_unknown_file_fails_instead_of_excluding_nothing(self):
        with self.assertRaises(ValueError):
            self.run_graph(ScriptedChat(fenced(VALID)), excluir=["ativos_c"])

    def test_whole_manual_sends_every_section(self):
        chat = ScriptedChat(fenced(VALID))
        self.run_graph(chat, inteiro=True)
        self.assertEqual(chat.received[0][1]["content"].count("<secao "), 4)

    # ferramentas

    def test_manual_search_result_goes_back_as_a_tool_message(self):
        chat = ScriptedChat(call("buscar_manual", {"consulta": "bloqueio nao agendar"}), fenced(VALID))
        out = self.run_graph(chat)
        result = chat.received[1][-1]
        self.assertEqual((result["role"], result["tool_call_id"]), ("tool", "c1"))
        self.assertIn("SECAO-BLOQUEIO", result["content"])
        self.assertEqual((out["passos"], out["entregas"], out["erros"]), (2, 1, []))

    def test_example_search_keeps_the_leave_out(self):
        chat = ScriptedChat(call("buscar_exemplos", {"consulta": "Ativo: pedido nos últimos 60 dias"}), fenced(VALID))
        self.run_graph(chat, excluir=["ativos_a"])
        self.assertNotIn("ativos_", chat.received[1][-1]["content"])

    def test_unknown_tool_and_bad_arguments_are_reported_to_the_llm(self):
        chat = ScriptedChat(call("apagar_tudo", {}), call("buscar_manual", "{não é json"), fenced(VALID))
        self.run_graph(chat)
        self.assertEqual(chat.received[1][-1]["content"], "Ferramenta desconhecida: apagar_tudo.")
        self.assertIn("`consulta` vazio", chat.received[2][-1]["content"])

    # perguntar: interrupt e retomada

    def test_question_pauses_and_the_answer_reaches_the_llm(self):
        chat = ScriptedChat(call(agent.ASK, {"pergunta": "Qual a frequência dos inativos?"}), fenced(VALID))
        out = self.run_graph(chat, answers=["28 dias"])
        self.assertEqual(self.asked, ["Qual a frequência dos inativos?"])
        self.assertEqual(chat.received[1][-1], {"role": "tool", "tool_call_id": "c1", "content": "28 dias"})
        self.assertEqual(out["perguntas"], [{"pergunta": "Qual a frequência dos inativos?", "resposta": "28 dias"}])
        self.assertIn("Perguntas feitas:\n- Qual a frequência dos inativos? -> 28 dias", out["resposta"])

    def test_empty_answer_tells_the_llm_to_assume(self):
        chat = ScriptedChat(call(agent.ASK, {"pergunta": "Agendar inadimplentes?"}), fenced(VALID))
        self.run_graph(chat, answers=[""])
        self.assertEqual(chat.received[1][-1]["content"], agent.NO_ANSWER)

    def test_questions_stop_at_the_limit(self):
        chat = ScriptedChat(*[call(agent.ASK, {"pergunta": f"P{n}?"}, f"c{n}") for n in range(1, agent.MAX_QUESTIONS + 2)],
                            fenced(VALID))
        out = self.run_graph(chat, answers=["sim"] * 5)
        self.assertEqual(self.asked, [f"P{n}?" for n in range(1, agent.MAX_QUESTIONS + 1)])
        self.assertEqual(chat.received[agent.MAX_QUESTIONS + 1][-1]["content"], agent.QUESTION_LIMIT)
        self.assertEqual(len(out["perguntas"]), agent.MAX_QUESTIONS)

    # limites

    def test_step_limit_takes_the_tools_away(self):
        chat = ScriptedChat(call("buscar_manual", {"consulta": "recencia"}))
        out = self.run_graph(chat)
        self.assertEqual(chat.tools[agent.MAX_STEPS - 2], agent.TOOLS)
        self.assertIsNone(chat.tools[agent.MAX_STEPS - 1])
        self.assertEqual(chat.received[agent.MAX_STEPS - 1][-1]["content"], agent.LAST_STEP)
        self.assertEqual(out["entregas"], agent.MAX_DELIVERIES)
        self.assertEqual(len(chat.received), agent.MAX_STEPS + agent.MAX_DELIVERIES - 1)

    # validar

    def test_valid_answer_ends_after_one_delivery(self):
        out = self.run_graph(ScriptedChat(fenced(VALID)))
        self.assertEqual((out["passos"], out["entregas"], out["conferencias"], out["erros"]), (1, 1, 1, []))
        self.assertTrue(out["resposta"].startswith("```gobr\nVersion 1.0"))

    def test_crlf_and_untagged_fence_are_read(self):
        reply = "```\r\n" + VALID.replace("\n", "\r\n") + "```"
        out = self.run_graph(ScriptedChat(reply))
        self.assertEqual((out["erros"], out["alertas"]), ([], []))

    def test_error_goes_back_to_the_llm_and_is_fixed(self):
        chat = ScriptedChat(fenced(UNKNOWN_CLAUSE), fenced(VALID))
        out = self.run_graph(chat)
        self.assertEqual((out["entregas"], out["erros"]), (2, []))
        self.assertIn("o cliente sorrir", chat.received[1][-1]["content"])

    def test_gives_up_after_max_deliveries(self):
        chat = ScriptedChat("Não sei escrever isso.")
        out = self.run_graph(chat)
        self.assertEqual(len(chat.received), agent.MAX_DELIVERIES)
        self.assertEqual((out["gobr"], out["conferencias"]), ("", 0))
        self.assertIn(f"Erros que ficaram depois de {agent.MAX_DELIVERIES} entregas", out["resposta"])

    def test_cascade_alert_reaches_the_answer(self):
        out = self.run_graph(ScriptedChat(fenced(LATE_BLOCK)))
        self.assertEqual(out["erros"], [])
        self.assertIn("Baixados: Bloqueio depois de regras de frequência", out["resposta"])

    def test_unreachable_rule_goes_back_to_the_llm(self):
        chat = ScriptedChat(fenced(UNREACHABLE), fenced(VALID))
        out = self.run_graph(chat)
        self.assertEqual((out["entregas"], out["erros"]), (2, []))
        self.assertIn('"Ativo recente": inalcançável', chat.received[1][-1]["content"])

    def test_comments_in_the_delivery_are_removed_before_validating(self):
        out = self.run_graph(ScriptedChat(fenced(VALID + "\n# pensando alto sobre 999 clientes\n")))
        self.assertNotIn("#", out["gobr"])
        self.assertEqual(out["erros"], [])

    def test_strip_comments_keeps_the_header_and_drops_the_rest(self):
        text = "# cabeçalho\nVersion 1.0\n# nota\nparametros \"A\":\n    # pensa alto\n    frequencia de 7 dias\n"
        self.assertEqual(agent.strip_comments(text), "# cabeçalho\nVersion 1.0\nparametros \"A\":\n    frequencia de 7 dias\n")
        self.assertEqual(agent.strip_comments(VALID), VALID)
        self.assertEqual(agent.strip_comments(""), "")

    def test_contradictory_filters_are_an_error(self):
        contradiction = VALID.replace("frequencia de 28 dias", "quando recencia de positivacao global em 30 dias\n"
                                      "    e fora da recencia de positivacao global em 60 dias\n    frequencia de 28 dias")
        errors, _ = agent.check(contradiction, REQUEST)
        self.assertIn('"Inativo": os filtros se contradizem, nenhum cliente atende a todos.', errors)

    def test_number_only_in_a_rule_name_does_not_count(self):
        wrong = VALID.replace('"Inativo"', '"Inativo 28 dias"').replace("frequencia de 28", "frequencia de 7")
        errors, _ = agent.check(wrong, REQUEST)
        self.assertEqual(len(errors), 1)
        self.assertTrue(errors[0].startswith("Números do pedido ausentes nas cláusulas do GoBR: 28."))

    def test_number_left_out_in_the_notes_is_an_alert_not_an_error(self):
        notes = "Capacidade de 35 clientes por dia: o GoBR não tem cláusula para isso."
        out = self.run_graph(ScriptedChat(fenced(VALID, notes)), descricao=REQUEST + " Capacidade: 35 clientes.")
        self.assertEqual(out["erros"], [])
        self.assertIn("ficaram de fora do GoBR (ver notas): 35", out["resposta"])
        self.assertIn(notes, out["resposta"])

    def test_requested_numbers_skip_zero_labels_and_read_money(self):
        text = "Regra 01: compra entre 0 e 60 dias, 14 dias. Regra 02: acima de R$ 1.500,00, 7 dias"
        self.assertEqual(agent.requested_numbers(text), {60, 14, 1500, 7})

    def test_undeclared_source_and_rule_without_action_are_errors(self):
        broken = HEADER + 'parametros "Ativo":\n    do time("vendas")\n    quando recencia de positivacao global em 60 dias\n'
        errors, _ = agent.check(broken, "60 dias")
        self.assertEqual(errors, ['"Ativo": fonte não declarada no arquivo: vendas.',
                                  '"Ativo": regra sem ação (frequência, preferência ou nao agendar).'])

    def test_empty_file_is_an_error(self):
        self.assertEqual(agent.check("isto não é gobr", "")[0], ["O arquivo não tem nenhuma regra `parametros`."])

    # conferir

    def test_rule_table_shows_what_each_rule_does(self):
        table = agent.rule_table(WITH_BLOCK).splitlines()
        self.assertTrue(table[0].startswith('- "Inadimplentes"') and table[0].endswith("ação: não agendar"), table[0])
        self.assertIn("clientes: compraram com qualquer vendedor da empresa nos últimos 60 dias", table[1])
        self.assertIn("ação: frequencia de 14 dias (frequência de 14 dias)", table[1])

    def test_conferente_reads_the_rule_table_and_the_notes(self):
        chat = ScriptedChat(fenced(VALID, "Nada ficou de fora."))
        self.run_graph(chat)
        system, user = chat.conferred[0]
        self.assertEqual(system["content"], agent.CONFERENCE_PROMPT.read_text(encoding="utf-8"))
        self.assertIn(agent.rule_table(VALID), user["content"])
        self.assertIn("Nada ficou de fora.", user["content"])
        self.assertIn(REQUEST, user["content"])

    def test_conferente_sees_the_users_answers_as_part_of_the_request(self):
        chat = ScriptedChat(call(agent.ASK, {"pergunta": "Frequência dos inativos?"}), fenced(VALID))
        self.run_graph(chat, answers=["28 dias"])
        self.assertIn("Respostas do usuário às perguntas do agente:\n- Frequência dos inativos? -> 28 dias",
                      chat.conferred[0][1]["content"])

    def test_long_reason_is_cut_in_the_answer(self):
        rambling = {"regras": [{"regra": "Ativo", "trecho_do_pedido": "Ativo", "confere": False, "motivo": "x" * 1000}],
                    "sem_regra": []}
        out = self.run_graph(ScriptedChat(fenced(VALID), conference=[rambling]))
        self.assertEqual(out["divergencias"][0], '"Ativo": ' + "x" * 300 + '… (pedido: "Ativo")')

    def test_divergence_goes_back_to_the_llm_once(self):
        chat = ScriptedChat(fenced(VALID), fenced(VALID), conference=[DISAGREES, AGREES])
        out = self.run_graph(chat)
        self.assertEqual((out["entregas"], out["conferencias"], out["divergencias"]), (2, 2, []))
        feedback = chat.received[1][-1]["content"]
        self.assertIn('"Ativo": o pedido manda agendar (pedido: "Ativo: ..., 14 dias")', feedback)
        self.assertIn('Trecho do pedido sem regra: "Prospect: 7 dias"', feedback)

    def test_divergence_in_the_second_conference_reaches_the_answer(self):
        out = self.run_graph(ScriptedChat(fenced(VALID), conference=[DISAGREES]))
        self.assertEqual((out["entregas"], out["conferencias"], len(out["divergencias"])), (2, 2, 2))
        self.assertIn("Divergências entre o pedido e as regras (conferente):", out["resposta"])

    def test_conferente_without_json_is_an_alert_and_does_not_block(self):
        out = self.run_graph(ScriptedChat(fenced(VALID), conference=["isto não é json"]))
        self.assertEqual((out["entregas"], out["divergencias"]), (1, []))
        self.assertIn("O conferente não respondeu em JSON", out["resposta"])

    def test_failed_fix_brings_back_the_last_valid_file(self):
        out = self.run_graph(ScriptedChat(fenced(VALID), fenced(UNKNOWN_CLAUSE), conference=[DISAGREES]))
        self.assertEqual((out["entregas"], out["conferencias"], out["erros"]), (agent.MAX_DELIVERIES, 1, []))
        self.assertEqual(out["gobr"], VALID.strip())
        self.assertEqual(len(out["divergencias"]), 2)
        self.assertIn("esta é a última versão que passou", out["resposta"])

    def test_divergence_after_the_last_delivery_goes_to_the_answer(self):
        chat = ScriptedChat(fenced(UNKNOWN_CLAUSE), fenced(UNKNOWN_CLAUSE), fenced(VALID), conference=[DISAGREES])
        out = self.run_graph(chat)
        self.assertEqual((out["entregas"], out["conferencias"], len(chat.received)), (agent.MAX_DELIVERIES, 1, 3))
        self.assertIn("Divergências entre o pedido e as regras (conferente):", out["resposta"])

    # triagem

    def test_triage_reads_its_prompt_and_its_segments_reach_the_agent(self):
        chat = ScriptedChat(fenced(VALID))
        out = self.run_graph(chat)
        system, user = chat.triaged[0]
        self.assertEqual(system["content"], agent.TRIAGE_PROMPT.read_text(encoding="utf-8"))
        self.assertEqual(user["content"], REQUEST)
        self.assertEqual((out["lacunas_iniciais"], self.asked), ([], []))
        self.assertIn('- "Inativo" | critério: os demais | ação: agendar a cada 28 dias', chat.received[0][1]["content"])

    def test_gap_is_asked_once_and_the_answer_goes_back_to_the_triage(self):
        missing = {"segmentos": [TRIAGED["segmentos"][0], {**TRIAGED["segmentos"][1], "frequencia_dias": 0}]}
        chat = ScriptedChat(fenced(VALID), triage=[missing, TRIAGED])
        out = self.run_graph(chat, answers=["28 dias"])
        self.assertEqual(len(self.asked), 1)
        self.assertIn('- "Inativo": de quantos em quantos dias agendar?', self.asked[0])
        self.assertIn("-> 28 dias", chat.triaged[1][1]["content"])
        self.assertEqual((out["lacunas_iniciais"], out["lacunas"], out["avisos"]),
                         (['"Inativo": de quantos em quantos dias agendar?'], [], []))
        self.assertIn("Perguntas feitas:\n- Para escrever as regras sem chutar", out["resposta"])

    def test_unanswered_gap_becomes_a_warning_without_a_second_triage(self):
        missing = {"segmentos": [{**TRIAGED["segmentos"][0], "acao": "inventado"}]}
        chat = ScriptedChat(fenced(VALID), triage=[missing])
        out = self.run_graph(chat, answers=[""])
        self.assertEqual(len(chat.triaged), 1)
        self.assertIn('Lacuna do pedido sem resposta do usuário: "Ativo": agendar ou não agendar?', out["resposta"])

    def test_gap_left_after_the_answer_says_the_answer_did_not_solve_it(self):
        missing = {"segmentos": [{**TRIAGED["segmentos"][0], "frequencia_dias": 0}]}
        chat = ScriptedChat(fenced(VALID), triage=[missing])
        out = self.run_graph(chat, answers=["não sei"])
        self.assertEqual(len(chat.triaged), 2)
        self.assertIn('Lacuna que a resposta do usuário não resolveu: "Ativo": de quantos em quantos dias agendar?',
                      out["resposta"])

    def test_triage_without_json_does_not_block(self):
        out = self.run_graph(ScriptedChat(fenced(VALID), triage=["não é json"]))
        self.assertEqual((out["segmentos"], out["erros"]), ([], []))
        self.assertIn("A triagem não respondeu em JSON", out["resposta"])

    def test_frequency_other_than_the_segment_goes_back_to_the_agent(self):
        # o validador não pega: o pedido não tem o 7 (veio da resposta do usuário) e os números dele estão no arquivo
        answered = {"segmentos": [TRIAGED["segmentos"][0], {**TRIAGED["segmentos"][1], "frequencia_dias": 7}]}
        fixed = VALID.replace("frequencia de 28 dias", "frequencia de 7 dias")
        chat = ScriptedChat(fenced(VALID), fenced(fixed), triage=[answered])
        out = self.run_graph(chat, descricao="Ativo: clientes com pedido nos últimos 60 dias, 14 dias. Inativo: os demais.")
        self.assertIn('"Inativo": a regra agenda a cada 28 dias; o pedido dá 7.', chat.received[1][-1]["content"])
        self.assertEqual((out["entregas"], out["divergencias"]), (2, []))

    # mais de uma ferramenta e o cliente

    def test_repeated_question_reuses_the_answer(self):
        chat = ScriptedChat(call(agent.ASK, {"pergunta": "P?"}), call(agent.ASK, {"pergunta": "P?"}, "c2"), fenced(VALID))
        out = self.run_graph(chat, answers=["sim"])
        self.assertEqual(self.asked, ["P?"])
        self.assertEqual(chat.received[2][-1]["content"], "Você já fez esta pergunta. Resposta: sim")
        self.assertEqual(len(out["perguntas"]), 1)

    def test_question_and_search_in_one_message_both_get_a_reply(self):
        both = call("buscar_manual", {"consulta": "recencia"})
        both["tool_calls"] += call(agent.ASK, {"pergunta": "Frequência?"}, "c2")["tool_calls"]
        chat = ScriptedChat(both, fenced(VALID))
        self.run_graph(chat, answers=["7 dias"])
        replies = {m["tool_call_id"]: m["content"] for m in chat.received[1] if m["role"] == "tool"}
        self.assertEqual(replies["c2"], "7 dias")
        self.assertIn("SECAO-RECENCIA", replies["c1"])

    def test_openai_chat_sends_tools_and_schema_and_reads_tool_calls(self):
        from types import SimpleNamespace
        from unittest import mock

        tool_call = SimpleNamespace(id="x1", function=SimpleNamespace(name="buscar_manual", arguments='{"consulta": "a"}'))
        reply = SimpleNamespace(choices=[SimpleNamespace(finish_reason="tool_calls",
                                                         message=SimpleNamespace(content=None, tool_calls=[tool_call]))])
        with mock.patch("openai.OpenAI") as client_class:
            create = client_class.return_value.chat.completions.create
            create.return_value = reply
            chat = agent.openai_chat("http://servidor/v1")
            message = chat([{"role": "user", "content": "oi"}], tools=agent.TOOLS)
            self.assertEqual(message, {"role": "assistant", "content": "", "tool_calls": [
                {"id": "x1", "type": "function", "function": {"name": "buscar_manual", "arguments": '{"consulta": "a"}'}}]})
            self.assertEqual(create.call_args.kwargs["tools"], agent.TOOLS)
            chat([{"role": "user", "content": "oi"}], schema=agent.CONFERENCE_SCHEMA)
            sent = create.call_args.kwargs
            self.assertNotIn("tools", sent)
            self.assertEqual(sent["response_format"]["json_schema"]["schema"], agent.CONFERENCE_SCHEMA)


def segment(name: str, action: str = "agendar", days: int = 0, criterion: str = "critério") -> dict:
    return {"segmento": name, "trecho": name, "criterio": criterion, "acao": action, "frequencia_dias": days}


def rule(name: str, action: str) -> str:
    return f'parametros "{name}":\n    do time("televendas")\n    quando recencia de positivacao global em 60 dias\n    {action}\n\n'


class TriageRulesTest(unittest.TestCase):
    """Saídas escritas à mão no ledger (#33 e #36) antes do código."""

    def test_gaps_missing_frequency_criterion_and_action(self):
        self.assertEqual(agent.gaps([segment("Inativos", days=0, criterion="sem compra há mais de 30 dias")]),
                         ['"Inativos": de quantos em quantos dias agendar?'])
        self.assertEqual(agent.gaps([segment("Ativos", days=14, criterion="")]),
                         ['"Ativos": quem são esses clientes (o critério)?'])
        self.assertEqual(agent.gaps([segment("Inadimplentes", action="indefinido", criterion="inadimplentes")]),
                         ['"Inadimplentes": agendar ou não agendar?'])

    def test_gaps_skip_residual_blocks_and_empty(self):
        self.assertEqual(agent.gaps([segment("Demais clientes", days=30, criterion="")]), [])
        self.assertEqual(agent.gaps([segment("Bloqueio", action="nao_agendar", criterion="inadimplentes")]), [])
        self.assertEqual(agent.gaps([]), [])

    def test_match_segments_flags_frequency_and_action(self):
        gobr = HEADER + rule("Inativos", "frequencia de 14 dias")
        self.assertEqual(agent.match_segments(gobr, [segment("Inativos", days=28)]),
                         ['"Inativos": a regra agenda a cada 14 dias; o pedido dá 28.'])
        gobr = HEADER + rule("Inadimplentes", "nao agendar")
        self.assertEqual(agent.match_segments(gobr, [segment("Inadimplentes", days=7)]),
                         ['"Inadimplentes": o pedido manda agendar; a regra é não agendar.'])

    def test_match_segments_by_prefix_longest_name_and_never_by_guess(self):
        gobr = HEADER + rule("Ativos: compra nos últimos 30 dias", "frequencia de 14 dias")
        self.assertEqual(agent.match_segments(gobr, [segment("Ativos", days=14)]), [])
        gobr = HEADER + rule("Clientes VIP", "frequencia de 7 dias")
        self.assertEqual(agent.match_segments(gobr, [segment("Ativos", days=14)]), [])
        gobr = HEADER + rule("Inativos (90 dias)", "frequencia de 14 dias")
        self.assertEqual(agent.match_segments(gobr, [segment("Inativos", days=28), segment("Inativos (90 dias)", days=14)]), [])
        gobr = HEADER + rule("Inativos", "frequencia de 14 dias")
        self.assertEqual(agent.match_segments(gobr, [segment("Inativos", days=0)]), [])

    # achados do code-auditor (2026-11-17)

    def test_match_segments_does_not_take_a_longer_name_as_the_same_segment(self):
        gobr = HEADER + rule("Ativos inadimplentes", "nao agendar") + rule("Inativos recentes", "frequencia de 7 dias")
        self.assertEqual(agent.match_segments(gobr, [segment("Ativos", days=14), segment("Inativos", days=14)]), [])

    def test_match_segments_flags_a_block_that_schedules_and_reads_fixed_frequencies(self):
        gobr = HEADER + rule("Inadimplentes", "frequencia de 7 dias")
        self.assertEqual(agent.match_segments(gobr, [segment("Inadimplentes", action="nao_agendar")]),
                         ['"Inadimplentes": o pedido manda não agendar; a regra agenda.'])
        gobr = HEADER + rule("Ativos", "frequencia semanal()")
        self.assertEqual(agent.match_segments(gobr, [segment("Ativos", days=14)]),
                         ['"Ativos": a regra agenda a cada 7 dias; o pedido dá 14.'])

    def test_residual_word_counts_only_in_the_segment_name(self):
        self.assertEqual(agent.gaps([segment("Outros distribuidores", days=7, criterion="")]),
                         ['"Outros distribuidores": quem são esses clientes (o critério)?'])
        self.assertEqual(agent.gaps([{**segment("Ativos", days=14, criterion=""), "trecho": "Ativos: 14 dias, como os demais"}]),
                         ['"Ativos": quem são esses clientes (o critério)?'])

    def test_parse_segments_forces_the_schema(self):
        content = json.dumps({"segmentos": [
            {"segmento": "A", "acao": "agendar", "frequencia_dias": "14"},
            {"segmento": "B", "acao": "agendar", "frequencia_dias": -3},
            {"segmento": "C", "acao": "agendar", "frequencia_dias": 1e400},
            {"segmento": "́"}, {"acao": "agendar"}, "texto solto"]})
        segments, warnings = agent.parse_segments(content.replace("Infinity", "1e400"))
        self.assertEqual([(s["segmento"], s["frequencia_dias"], s["criterio"]) for s in segments],
                         [("A", 14, ""), ("B", 0, ""), ("C", 0, "")])
        self.assertEqual(warnings, [])
        self.assertEqual(agent.parse_segments('{"segmentos": []}')[1],
                         ["A triagem não achou segmentos no pedido; o pedido não foi conferido segmento a segmento."])


if __name__ == "__main__":
    unittest.main()

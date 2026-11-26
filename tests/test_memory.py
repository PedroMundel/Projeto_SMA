import json
import unittest
from pathlib import Path

from gobr import agent, memory, memory_eval
from tests.test_agent import (DISAGREES, REQUEST, TRIAGED, UNKNOWN_CLAUSE, VALID, AgentFixture, ScriptedChat, call,
                              fenced)

LINES = "Ativo: clientes com pedido nos últimos 60 dias, 14 dias\nInativo: os demais, 28 dias"
ACTIVE_15 = VALID.replace("frequencia de 14 dias", "frequencia de 15 dias")
BOTH_CHANGED = ACTIVE_15.replace("frequencia de 28 dias", "frequencia de 30 dias")
INACTIVE_TOO = ACTIVE_15.replace("    frequencia de 28 dias", "    quando inadimplentes\n    frequencia de 28 dias")
TRIAGED_15 = {"segmentos": [{**TRIAGED["segmentos"][0], "frequencia_dias": 15}, TRIAGED["segmentos"][1]]}


def change(line: int, text: str) -> dict:
    return {"tipo": "alterar", "versao": 0, "operacoes": [{"op": "alterar", "linha": line, "texto": text}]}


TO_15 = change(1, "Ativo: clientes com pedido nos últimos 60 dias, 15 dias")
UNDO = {"tipo": "desfazer", "versao": 0, "operacoes": []}
DOUBT = {"tipo": "duvida", "versao": 0, "operacoes": []}


class ApplyOperationsTest(unittest.TestCase):
    LINES = ["Ativos: 30, 14 dias", "Inativos: 28 dias"]

    def apply(self, *ops, message="troque os ativos para 15 dias"):
        return memory.apply_operations(self.LINES, list(ops), message)

    def test_change_one_line_keeps_the_others(self):
        lines, changes, warnings = self.apply({"op": "alterar", "linha": 1, "texto": "Ativos: 30, 15 dias"})
        self.assertEqual(lines, ["Ativos: 30, 15 dias", "Inativos: 28 dias"])
        self.assertEqual(changes, [{"antes": "Ativos: 30, 14 dias", "depois": "Ativos: 30, 15 dias"}])
        self.assertEqual(warnings, [])

    def test_remove_and_add(self):
        lines, changes, warnings = self.apply({"op": "remover", "linha": 2}, message="tire os inativos")
        self.assertEqual((lines, changes, warnings),
                         (["Ativos: 30, 14 dias"], [{"antes": "Inativos: 28 dias", "depois": ""}], []))
        lines, changes, warnings = self.apply({"op": "incluir", "linha": 0, "texto": "Prospects: 7 dias"},
                                              message="inclua os prospects a cada 7 dias")
        self.assertEqual((lines, changes, warnings),
                         (self.LINES + ["Prospects: 7 dias"], [{"antes": "", "depois": "Prospects: 7 dias"}], []))

    def test_bad_operations_are_refused_with_a_warning(self):
        bad = [{"op": "alterar", "linha": 0, "texto": "x"}, {"op": "alterar", "linha": 9, "texto": "x"},
               {"op": "remover", "linha": True}, {"op": "alterar", "linha": 1, "texto": "  "},
               {"op": "alterar", "linha": 1, "texto": "Ativos: 30, 14 dias"}, {"op": "incluir", "texto": ""},
               {"op": "trocar", "linha": 1, "texto": "x"}, "alterar"]
        for op in bad:
            with self.subTest(op=op):
                lines, changes, warnings = self.apply(op, message="mude")
                self.assertEqual((lines, changes, len(warnings)), (self.LINES, [], 1))

    def test_second_operation_on_the_same_line_is_refused(self):
        lines, changes, warnings = self.apply({"op": "alterar", "linha": 1, "texto": "Ativos: 30, 15 dias"},
                                              {"op": "remover", "linha": 1})
        self.assertEqual(lines[0], "Ativos: 30, 15 dias")
        self.assertEqual((len(changes), len(warnings)), (1, 1))

    def test_number_the_user_did_not_say_is_a_warning(self):
        lines, _, warnings = self.apply({"op": "alterar", "linha": 1, "texto": "Ativos: 30, 21 dias"},
                                        message="troque a frequência dos ativos")
        self.assertEqual(lines[0], "Ativos: 30, 21 dias")
        self.assertEqual(len(warnings), 1)
        self.assertIn("21", warnings[0])

    def test_number_of_the_message_that_reached_no_line_is_a_warning(self):
        _, _, warnings = self.apply({"op": "alterar", "linha": 1, "texto": "Ativos: 30 dias"},
                                    message="troque os ativos para 15 dias")
        self.assertEqual(len(warnings), 1)
        self.assertIn("15", warnings[0])

    def test_numbers_are_read_as_the_validator_reads_them(self):
        _, _, warnings = self.apply({"op": "alterar", "linha": 1, "texto": "Ativos: 30, valor acima de 2.000"},
                                    message="na regra 3, mude os ativos para 2000 de valor")
        self.assertEqual(warnings, [])

    def test_changed_answer_line_becomes_binding(self):
        line = memory.answer_line("qual prazo?", "90 dias")
        lines, _, _ = memory.apply_operations([line], [{"op": "alterar", "linha": 1, "texto": line.replace("90", "120")}],
                                              "o prazo passa a 120")
        self.assertIn("120", memory.binding_text(lines[0]))

    def test_list_numbering_copied_by_the_llm_is_dropped(self):
        lines, _, warnings = self.apply({"op": "incluir", "linha": 0, "texto": "3. Inadimplentes: não agendar"},
                                        message="não agende os inadimplentes")
        self.assertEqual((lines[2], warnings), ("Inadimplentes: não agendar", []))
        lines, _, _ = self.apply({"op": "alterar", "linha": 1, "texto": "1) Ativos: 30, 15 dias"})
        self.assertEqual(lines[0], "Ativos: 30, 15 dias")
        _, changes, _ = self.apply({"op": "alterar", "linha": 1, "texto": "1. Ativos: 30, 14 dias"})
        self.assertEqual(changes, [])
        own = memory.apply_operations(["1. Ativos: 14 dias"], [{"op": "alterar", "linha": 1, "texto": "1. Ativos: 15 dias"}],
                                      "troque para 15")[0]
        self.assertEqual(own, ["1. Ativos: 15 dias"])

    def test_change_that_the_message_does_not_touch_is_refused(self):
        lines, changes, warnings = self.apply({"op": "remover", "linha": 2}, message="agora não agende os inadimplentes")
        self.assertEqual((lines, changes, len(warnings)), (self.LINES, [], 1))
        for message in ("tire os inativos", "tire o último", "remova essa linha", "tire o de 28 dias", "junte tudo num só"):
            with self.subTest(message=message):
                self.assertEqual(len(self.apply({"op": "remover", "linha": 2}, message=message)[1]), 1)
        kept = self.apply({"op": "alterar", "linha": 2, "texto": "Inativos: 40 dias"}, message="o resto passa a 40")[1]
        self.assertEqual(len(kept), 1)  # o número da mensagem entrou na linha

    def test_bare_days_are_the_frequency_not_the_criterion(self):
        lines = ["Ativos: compra nos últimos 30 dias, 14 dias"]

        def change_(text, message):
            return memory.apply_operations(lines, [{"op": "alterar", "linha": 1, "texto": text}], message)[0][0]
        wrong, right = "Ativos: compra nos últimos 20 dias, 14 dias", "Ativos: compra nos últimos 30 dias, 20 dias"
        self.assertEqual(change_(wrong, "muda os ativo p 20 dias blz"), right)
        self.assertEqual(change_(right, "muda os ativo p 20 dias blz"), right)
        for message in ("o corte dos ativos passa a 20 dias", "ativos agora é quem comprou nos últimos 20 dias",
                        "aumente o prazo dos ativos para 20", "ativos: recência de 20 dias"):
            with self.subTest(message=message):
                self.assertEqual(change_(wrong, message), wrong)
        self.assertEqual(memory.apply_operations(["Ativos: compra nos últimos 30 dias"], [
            {"op": "alterar", "linha": 1, "texto": "Ativos: compra nos últimos 20 dias"}], "ativos 20 dias")[0],
            ["Ativos: compra nos últimos 20 dias"])  # sem frequência na linha, não há para onde mover

    def test_operations_that_are_not_a_list(self):
        self.assertEqual(memory.apply_operations(self.LINES, None, "x")[:2], (self.LINES, []))


class TextTest(unittest.TestCase):
    def test_history_fits_is_cut_and_is_empty(self):
        turns = [{"n": n, "mensagem": f"mensagem {n}", "tipo": "alterar", "resumo": "r" * 50, "perguntas": []}
                 for n in range(1, 5)]
        self.assertEqual(memory.history_text([]), "")
        whole = memory.history_text(turns)
        self.assertLess(whole.index("mensagem 1"), whole.index("mensagem 4"))
        self.assertNotIn("omitidos", whole)
        cut = memory.history_text(turns, limit=220)
        self.assertIn("(2 turnos anteriores omitidos)", cut)
        self.assertNotIn("mensagem 2", cut)
        self.assertLess(cut.index("mensagem 3"), cut.index("mensagem 4"))
        self.assertIn("mensagem 4", memory.history_text(turns, limit=1))

    def test_answers_are_request_lines_whose_numbers_are_not_required(self):
        line = memory.answer_line('"Inativos": de quantos\nem quantos dias?', "a cada\n28 dias")
        self.assertNotIn("\n", line)
        self.assertIn("28", line)
        self.assertEqual(memory.binding_text(f"Ativos: 14 dias\n{line}"), "Ativos: 14 dias")

    def test_bad_interpretation_does_not_break(self):
        for content in ("", "não é json", "[]", '{"tipo": "outra"}', '{"tipo": "desfazer", "versao": "x", "operacoes": 3}'):
            with self.subTest(content=content):
                read = memory.parse_interpretation(content)
                self.assertIn(read["tipo"], ("", "desfazer"))
                self.assertEqual((read["versao"], read["operacoes"]), (0, []))


def seg(name: str, days: int, line: str = "", action: str = "agendar") -> dict:
    return {"segmento": name, "trecho": line or f"{name}: critério, {days} dias", "criterio": "critério", "acao": action,
            "frequencia_dias": days}


class KeepSegmentsTest(unittest.TestCase):
    OLD = [seg("Ativo", 14), seg("Inativo", 28)]

    def keep(self, new, changes, message="", old=None):
        return {s["segmento"]: s["frequencia_dias"] for s in memory.keep_segments(old or self.OLD, new, changes, message)}

    def test_untouched_stays_and_touched_follows_the_triage(self):
        change_ = [{"antes": "Ativo: critério, 14 dias", "depois": "Ativo: critério, 15 dias"}]
        self.assertEqual(self.keep([seg("Ativo", 15), seg("Inativo", 0)], change_), {"Ativo": 15, "Inativo": 28})

    def test_one_line_with_two_segments(self):
        line = "Curva A e B: critério, 14 dias"
        old = [seg("Curva A", 14, line), seg("Curva B", 14, line)]
        new = [seg("Curva A", 15, line.replace("14", "15")), seg("Curva B", 15, line.replace("14", "15"))]
        self.assertEqual(self.keep(new, [{"antes": line, "depois": line.replace("14", "15")}], old=old),
                         {"Curva A": 15, "Curva B": 15})

    def test_change_that_names_no_segment_freezes_nothing(self):
        new = [seg("Ativo", 10), seg("Inativo", 10)]
        self.assertEqual(self.keep(new, [{"antes": "", "depois": "Todos os grupos a cada 10 dias"}]),
                         {"Ativo": 10, "Inativo": 10})

    def test_name_only_in_the_message_is_touched(self):
        new = [seg("Ativo", 15), seg("Inativo", 28)]
        self.assertEqual(self.keep(new, [{"antes": "Frequencia: 14", "depois": "Frequencia: 15"}],
                                   message="troque o ativo para 15")["Ativo"], 15)

    def test_incomplete_segment_follows_the_triage(self):
        change_ = [{"antes": "Ativo: critério, 14 dias", "depois": "Ativo: critério, 15 dias"}]
        self.assertEqual(self.keep([seg("Ativo", 15), seg("Inativo", 21)], change_, old=[seg("Ativo", 14), seg("Inativo", 0)]),
                         {"Ativo": 15, "Inativo": 21})

    def test_segment_the_triage_forgot_comes_back_and_a_removed_one_does_not(self):
        change_ = [{"antes": "Ativo: critério, 14 dias", "depois": "Ativo: critério, 15 dias"}]
        self.assertEqual(self.keep([seg("Ativo", 15)], change_), {"Ativo": 15, "Inativo": 28})
        self.assertEqual(self.keep([], change_), {"Inativo": 28})
        self.assertEqual(self.keep([seg("Ativo", 14)], [{"antes": "Inativo: critério, 28 dias", "depois": ""}]), {"Ativo": 14})


def blocks(source: str):
    return agent._package(source)[0].blocks


class AuditFixesTest(unittest.TestCase):
    def test_days_in_the_criterion_are_not_the_frequency(self):
        before = "Ativos: agendar a cada 14 dias quem comprou nos ultimos 30 dias"
        edit = "Ativos: agendar a cada 20 dias quem comprou nos ultimos 30 dias"
        self.assertEqual(memory._frequency_not_criterion(before, edit, "muda os ativos para 20 dias"), edit)
        kept = memory._frequency_not_criterion("Ativos: compra nos últimos 30 dias, 14 dias", "Ativos: compra nos últimos 20 dias, 14 dias", "muda os ativos para 20 dias")
        self.assertEqual(kept, "Ativos: compra nos últimos 30 dias, 20 dias")

    def test_short_names_are_related_to_the_message(self):
        self.assertTrue(memory.related({"antes": "MEI: não agendar", "depois": ""}, "tire os MEI"))
        self.assertFalse(memory.related({"antes": "Ativos: 30, 14 dias", "depois": ""}, "tire os MEI"))
        for line, message in (("Não compradores: 90, 28 dias", "não agendar os MEI"), ("Sem pedido: 28 dias", "deixe os MEI sem visita"),
                              ("Até 30 dias: 14 dias", "os MEI podem ir até 40"), ("Resposta do usuário (os MEI ou os outros?): 21 dias", "os MEI sem ou com visita")):
            self.assertFalse(memory.related({"antes": line, "depois": ""}, message), line)

    def test_the_tail_with_a_cada_is_still_the_frequency(self):
        for tail in ("agendar a cada 14 dias", "visitar a cada 14 dias", "com frequência de 14 dias", "14 dias", "(14 dias)"):
            before, edit = f"Ativos: compra nos últimos 30 dias, {tail}", f"Ativos: compra nos últimos 20 dias, {tail}"
            expected = before.replace("14", "20")
            self.assertEqual(memory._frequency_not_criterion(before, edit, "muda os ativos para 20 dias"), expected, tail)
        line = "Inativos: sem pedidos a mais de 45 dias"
        self.assertEqual(memory._frequency_not_criterion(line, line.replace("45", "60"), "inativos para 60 dias"), line.replace("45", "60"))


class UntouchedChangesTest(unittest.TestCase):
    SEGMENTS = TRIAGED["segmentos"]
    CHANGE = [{"antes": "Ativo: 60 dias, 14 dias", "depois": "Ativo: 60 dias, 15 dias"}]

    def check(self, new: str, new_segments=None, changes=None, message="troque o ativo para 15 dias", old=VALID, old_segments=None):
        return memory.untouched_changes(blocks(old), blocks(new), old_segments or self.SEGMENTS,
                                        new_segments or self.SEGMENTS, self.CHANGE if changes is None else changes, message)

    def test_only_the_mentioned_rule_changed(self):
        self.assertEqual(self.check(ACTIVE_15), [])

    def test_ativo_does_not_match_inside_inativo(self):
        found = self.check(BOTH_CHANGED)
        self.assertEqual(len(found), 1)
        self.assertIn('"Inativo"', found[0])

    def test_rule_that_disappeared(self):
        found = self.check(ACTIVE_15.split('parametros "Inativo"')[0])
        self.assertEqual(len(found), 1)
        self.assertIn('"Inativo"', found[0])

    def test_order_of_the_rules_not_mentioned(self):
        head, body = VALID.split('parametros "Ativo"')
        active, inactive = body.split('parametros "Inativo"')
        swapped = f'{head}parametros "Inativo"{inactive}\nparametros "Ativo"{active}'
        found = self.check(swapped, new_segments=self.SEGMENTS + [seg("Prospect", 7)], changes=[{"antes": "", "depois": "Prospect: 7 dias"}],
                           message="inclua prospect, 7 dias")
        self.assertEqual(len(found), 1)
        self.assertIn("ordem", found[0])

    def test_segment_that_changed_in_the_triage_is_not_judged(self):
        changed = [self.SEGMENTS[0], {**self.SEGMENTS[1], "frequencia_dias": 30}]
        self.assertEqual(self.check(BOTH_CHANGED, new_segments=changed), [])

    def test_rule_without_a_segment_is_not_judged(self):
        self.assertEqual(self.check(BOTH_CHANGED, old_segments=self.SEGMENTS[:1]), [])

    def test_change_that_names_no_segment_is_not_judged(self):
        team = VALID.replace("todostelevendas ativados", "todosexternos ativados")
        changes = [{"antes": "Time: televendas", "depois": "Time: externos"}]
        self.assertEqual(self.check(team, changes=changes, message="o time agora é o externo"), [])

    def test_source_used_by_an_untouched_rule_is_judged(self):
        team = ACTIVE_15.replace("todostelevendas ativados", "todostelevendas inativados")
        found = self.check(team)
        self.assertEqual(len(found), 1)
        self.assertIn('"Inativo"', found[0])

    def test_diff_lists_what_changed_rule_by_rule(self):
        diff = "\n".join(memory.diff_blocks(blocks(VALID), blocks(ACTIVE_15)))
        self.assertIn('"Ativo"', diff)
        self.assertIn("frequencia de 14 dias", diff)
        self.assertIn("frequencia de 15 dias", diff)
        self.assertNotIn('"Inativo"', diff)
        self.assertEqual(memory.diff_blocks(blocks(VALID), blocks(VALID)), [])


class ConversationTest(AgentFixture):
    """Vários turnos na mesma conversa; cada turno reabre o banco, como um processo novo."""

    def setUp(self):
        super().setUp()
        self.db = Path(self.tmp.name) / "memoria" / "conversas.db"

    def turn(self, chat, message: str | None, answers=(), thread: str = "t") -> dict:
        res = agent.Resources(self.examples, self.manual, self.embedder, chat)
        pending = list(answers)

        def answer(question: str) -> str:
            self.asked.append(question)
            return pending.pop(0) if pending else ""

        with agent.open_memory(self.db) as saver:
            graph = agent.build_graph(res, saver)
            return agent.converse(graph, None if message is None else {"mensagem": message}, answer, thread)

    def started(self) -> dict:
        return self.turn(ScriptedChat(fenced(VALID)), LINES)

    def test_first_turn_sends_the_same_message_as_without_memory(self):
        chat = ScriptedChat(fenced(VALID))
        self.turn(chat, REQUEST)
        first = chat.received[0][1]["content"]
        self.assertTrue(first.startswith(f"<pedido>\n{REQUEST}\n</pedido>\n<premissas>\n{agent.P11}\n{agent.SAME_SCOPE}\n</premissas>\n<segmentos>\n"))
        for tag in ("<conversa>", "<arquivo_atual", "<mudanca>"):
            self.assertNotIn(tag, first)
        self.assertEqual(chat.interpreted, [])

    def test_change_reaches_the_agent_with_the_current_file_after_reopening(self):
        self.started()
        chat = ScriptedChat(fenced(ACTIVE_15), interpret=[TO_15], triage=[TRIAGED_15])
        out = self.turn(chat, "troque o ativo para 15 dias")
        first = chat.received[0][1]["content"]
        self.assertIn(VALID.strip(), first)
        self.assertIn("60 dias, 15 dias", first)
        self.assertIn("troque o ativo para 15 dias", first)
        self.assertNotIn("60 dias, 14 dias", first.split("</pedido>")[0])
        self.assertEqual((out["erros"], out["divergencias"], out["versao_atual"]), ([], [], 2))
        self.assertEqual(out["pedido"], ["Ativo: clientes com pedido nos últimos 60 dias, 15 dias",
                                         "Inativo: os demais, 28 dias"])
        self.assertIn("frequencia de 15 dias", out["resposta"])
        self.assertIn('"Ativo"', out["resposta"])

    def test_working_state_starts_clean_every_turn(self):
        self.turn(ScriptedChat(fenced(VALID), conference=[DISAGREES, DISAGREES]), LINES)
        out = self.turn(ScriptedChat(fenced(ACTIVE_15), interpret=[TO_15], triage=[TRIAGED_15]), "troque o ativo para 15 dias")
        self.assertEqual((out["entregas"], out["conferencias"], out["passos"], out["divergencias"], out["perguntas"]),
                         (1, 1, 1, [], []))

    def test_change_outside_the_request_goes_back_to_the_agent(self):
        self.started()
        chat = ScriptedChat(fenced(INACTIVE_TOO), fenced(ACTIVE_15), interpret=[TO_15], triage=[TRIAGED_15])
        out = self.turn(chat, "troque o ativo para 15 dias")
        self.assertIn('"Inativo"', chat.received[1][-1]["content"])
        self.assertEqual((out["entregas"], out["divergencias"]), (2, []))

    def test_old_number_is_no_longer_required_and_the_untouched_one_still_is(self):
        self.started()
        no_28 = ACTIVE_15.replace("frequencia de 28 dias", "frequencia de 30 dias")
        out = self.turn(ScriptedChat(fenced(no_28), interpret=[TO_15], triage=[TRIAGED_15]), "troque o ativo para 15 dias")
        self.assertTrue(any("28" in e for e in out["erros"]))
        self.assertFalse(any("14" in e for e in out["erros"]))

    def test_failed_change_keeps_the_previous_version_and_request(self):
        self.started()
        out = self.turn(ScriptedChat(fenced(UNKNOWN_CLAUSE), interpret=[TO_15], triage=[TRIAGED_15]),
                        "troque o ativo para 15 dias")
        self.assertTrue(out["erros"])
        self.assertEqual(out["versao_atual"], 1)
        self.assertIn("60 dias, 14 dias", out["pedido"][0])
        self.assertEqual(memory.current(out)["gobr"], VALID.strip())
        self.assertIn("versão 1", out["resposta"])

    def test_doubt_answers_from_memory_and_changes_nothing(self):
        self.started()
        chat = ScriptedChat("A cada 28 dias.\n```gobr\nVersion 1.0\n```", interpret=[DOUBT])
        out = self.turn(chat, "de quantos em quantos dias ficaram os inativos?")
        sent = chat.received[0][1]["content"]
        for expected in ("frequencia de 28 dias", "Inativo: os demais, 28 dias", "de quantos em quantos dias"):
            self.assertIn(expected, sent)
        self.assertIn("A cada 28 dias.", out["resposta"])
        self.assertNotIn("```", out["resposta"])
        self.assertEqual((out["versao_atual"], len(out["versoes"]), len(out["turnos"])), (1, 1, 2))

    def test_undo_returns_to_the_origin_and_the_next_change_starts_from_it(self):
        self.started()
        self.turn(ScriptedChat(fenced(ACTIVE_15), interpret=[TO_15], triage=[TRIAGED_15]), "troque o ativo para 15 dias")
        out = self.turn(ScriptedChat("não usado", interpret=[UNDO]), "volte para a versão anterior")
        self.assertEqual((out["versao_atual"], memory.current(out)["gobr"]), (1, VALID.strip()))
        self.assertIn("60 dias, 14 dias", out["pedido"][0])
        chat = ScriptedChat(fenced(ACTIVE_15), interpret=[TO_15], triage=[TRIAGED_15])
        out = self.turn(chat, "troque o ativo para 15 dias")
        self.assertIn(VALID.strip(), chat.received[0][1]["content"])
        self.assertEqual((out["versao_atual"], memory.current(out)["pai"]), (3, 1))

    def test_undo_without_a_previous_version_or_to_an_unknown_one_changes_nothing(self):
        self.started()
        for request in (UNDO, {**UNDO, "versao": 7}):
            out = self.turn(ScriptedChat("não usado", interpret=[request]), "volte")
            self.assertEqual((out["versao_atual"], out["tipo"]), (1, "sem_mudanca"))

    def test_change_that_cannot_be_applied_asks_to_rephrase(self):
        self.started()
        for read in (change(9, "x"), "não é json", {"tipo": "alterar", "versao": 0, "operacoes": [
                {"op": "remover", "linha": 1}, {"op": "remover", "linha": 2}]}):
            out = self.turn(ScriptedChat("não usado", interpret=[read]), "mude aquilo")
            self.assertEqual((out["tipo"], out["versao_atual"], len(out["pedido"])), ("sem_mudanca", 1, 2))
            self.assertTrue(out["resposta"])

    def test_unrelated_change_gets_a_second_chance_with_the_reason(self):
        self.started()
        wrong = {"tipo": "alterar", "versao": 0, "operacoes": [{"op": "remover", "linha": 2, "texto": ""}]}
        chat = ScriptedChat(fenced(ACTIVE_15), interpret=[wrong, TO_15], triage=[TRIAGED_15])
        out = self.turn(chat, "troque o ativo para 15 dias")
        self.assertEqual((len(chat.interpreted), out["tipo"], out["versao_atual"]), (2, "alterar", 2))
        self.assertIn("não fala", chat.interpreted[1][-1]["content"])

    def test_message_that_cites_two_segments_and_changes_one_is_read_again(self):
        self.started()
        both = {"tipo": "alterar", "versao": 0, "operacoes": TO_15["operacoes"] + [
            {"op": "alterar", "linha": 2, "texto": "Inativo: os demais, 30 dias"}]}
        triaged = {"segmentos": [TRIAGED_15["segmentos"][0], {**TRIAGED["segmentos"][1], "frequencia_dias": 30}]}
        chat = ScriptedChat(fenced(BOTH_CHANGED), interpret=[TO_15, both], triage=[triaged])
        out = self.turn(chat, "o ativo passa a 15 dias e o inativo a 30 dias")
        self.assertEqual((len(chat.interpreted), len(out["mudancas"])), (2, 2))
        self.assertIn('"Inativo"', chat.interpreted[1][-1]["content"])
        stays = ScriptedChat(fenced(ACTIVE_15), interpret=[change(1, "Ativo: clientes com pedido nos últimos 60 dias, 30 dias")])
        self.turn(stays, "o ativo com a mesma frequência do inativo")  # insistiu: vale a 2ª leitura
        self.assertEqual(len(stays.interpreted), 2)
        one = ScriptedChat(fenced(BOTH_CHANGED), interpret=[change(1, "Ativo: clientes com pedido nos últimos 60 dias, 16 dias")])
        self.turn(one, "o ativo passa a 16 dias")
        self.assertEqual(len(one.interpreted), 1)

    def test_doubt_without_a_question_gets_a_second_chance(self):
        self.started()
        chat = ScriptedChat(fenced(ACTIVE_15), interpret=[DOUBT, TO_15], triage=[TRIAGED_15])
        out = self.turn(chat, "troque o ativo para 15 dias")
        self.assertEqual((len(chat.interpreted), out["tipo"]), (2, "alterar"))
        insists = ScriptedChat("resposta", interpret=[DOUBT])
        self.assertEqual(self.turn(insists, "me explica a regra do ativo")["tipo"], "duvida")
        self.assertEqual(len(insists.interpreted), 1)  # pede explicação: não precisa de "?"
        stays = ScriptedChat("resposta", interpret=[DOUBT])
        self.assertEqual(self.turn(stays, "troque o ativo")["tipo"], "duvida")  # insistiu: vale a 2ª leitura
        self.assertEqual(len(stays.interpreted), 2)

    def test_new_request_starts_from_scratch_but_keeps_the_versions(self):
        self.started()
        read = {"tipo": "novo", "versao": 0, "operacoes": [{"op": "incluir", "linha": 0, "texto": "Ativo: 60 dias, 15 dias"}]}
        chat = ScriptedChat(fenced(ACTIVE_15), interpret=[read], triage=[TRIAGED_15])
        out = self.turn(chat, "esqueça. Ativo: 60 dias, 15 dias")
        self.assertNotIn("<arquivo_atual", chat.received[0][1]["content"])
        self.assertEqual((out["pedido"], out["versao_atual"], len(out["versoes"])), (["Ativo: 60 dias, 15 dias"], 2, 2))

    def test_new_request_that_loses_a_number_warns(self):
        self.started()
        read = {"tipo": "novo", "versao": 0, "operacoes": [{"op": "incluir", "linha": 0, "texto": "Ativo: 60 dias"}]}
        out = self.turn(ScriptedChat(fenced(ACTIVE_15), interpret=[read], triage=[TRIAGED_15]), "Ativo: 60 dias, 15 dias")
        self.assertTrue(any("15" in w for w in out["avisos_memoria"]))

    def test_number_in_the_farewell_to_the_old_request_is_not_required(self):
        self.started()
        read = {"tipo": "novo", "versao": 0, "operacoes": [{"op": "incluir", "linha": 0, "texto": "Ativo: 60 dias, 15 dias"}]}
        out = self.turn(ScriptedChat(fenced(ACTIVE_15), interpret=[read], triage=[TRIAGED_15]),
                        "Esqueça a versão 1. Novo pedido: Ativo: 60 dias, 15 dias")
        self.assertEqual((out["erros"], out["versao_atual"], out["pedido"]), ([], 2, ["Ativo: 60 dias, 15 dias"]))

    def test_gap_of_the_old_request_is_asked_again_in_a_new_one_and_undo_restores_the_list(self):
        gap = {"segmentos": [TRIAGED["segmentos"][0], {**TRIAGED["segmentos"][1], "frequencia_dias": 0}]}
        self.turn(ScriptedChat(fenced(VALID), triage=[gap]), "Ativo: 60 dias, 14 dias\nInativo: os demais")
        read = {"tipo": "novo", "versao": 0, "operacoes": [{"op": "incluir", "linha": 0, "texto": "Inativo: os demais"}]}
        out = self.turn(ScriptedChat(fenced(VALID), interpret=[read], triage=[gap, TRIAGED]), "novo pedido: inativo: os demais",
                        answers=["28"])
        self.assertEqual((len(self.asked), out["sem_resposta"]), (2, []))
        out = self.turn(ScriptedChat("não usado", interpret=[UNDO]), "volte")
        self.assertEqual(len(out["sem_resposta"]), 1)

    def test_number_only_mentioned_in_the_notes_does_not_count_in_a_change(self):
        self.started()
        out = self.turn(ScriptedChat(fenced(VALID, "Alterei a frequência de 14 para 15 dias."), interpret=[TO_15],
                                     triage=[TRIAGED_15]), "troque o ativo para 15 dias")
        self.assertTrue(any("15" in e for e in out["erros"]))
        self.assertEqual(out["versao_atual"], 1)

    def test_number_declared_out_of_gobr_counts_in_a_change(self):
        self.started()
        read = {"tipo": "alterar", "versao": 0, "operacoes": [{"op": "incluir", "linha": 0, "texto": "Capacidade: 35 por dia"}]}
        out = self.turn(ScriptedChat(fenced(VALID, "Capacidade 35: o GoBR não tem cláusula para isso."), interpret=[read]),
                        "capacidade de 35 por dia")
        self.assertEqual((out["erros"], memory.current(out)["fora"]), ([], [35]))

    def test_unanswered_gap_warning_says_there_was_no_answer(self):
        gap = {"segmentos": [TRIAGED["segmentos"][0], {**TRIAGED["segmentos"][1], "frequencia_dias": 0}]}
        self.turn(ScriptedChat(fenced(VALID), triage=[gap]), "Ativo: 60 dias, 14 dias\nInativo: os demais")
        gap_15 = {"segmentos": [TRIAGED_15["segmentos"][0], gap["segmentos"][1]]}
        out = self.turn(ScriptedChat(fenced(ACTIVE_15), interpret=[change(1, "Ativo: 60 dias, 15 dias")], triage=[gap_15]),
                        "troque o ativo para 15 dias")
        self.assertTrue(any("sem resposta" in w for w in out["avisos"]))

    def test_undo_after_a_failed_change_does_not_drop_the_version_that_passed(self):
        self.started()
        self.turn(ScriptedChat(fenced(ACTIVE_15), interpret=[TO_15], triage=[TRIAGED_15]), "troque o ativo para 15 dias")
        to_20 = change(1, "Ativo: clientes com pedido nos últimos 60 dias, 20 dias")
        self.turn(ScriptedChat(fenced(UNKNOWN_CLAUSE), interpret=[to_20]), "troque o ativo para 20 dias")
        out = self.turn(ScriptedChat("não usado", interpret=[UNDO]), "desfaça isso")
        self.assertEqual((out["tipo"], out["versao_atual"]), ("sem_mudanca", 2))
        self.assertIn("versão 1", out["resposta"])
        out = self.turn(ScriptedChat("não usado", interpret=[{**UNDO, "versao": 1}]), "volte para a versão 1")
        self.assertEqual((out["tipo"], out["versao_atual"]), ("desfazer", 1))

    def test_forgotten_segment_and_dropped_rule_go_back_to_the_agent(self):
        block = {"segmento": "Inadimplentes", "trecho": "Nao agendar inadimplentes", "criterio": "inadimplentes",
                 "acao": "nao_agendar", "frequencia_dias": 0}
        with_block = VALID.replace('parametros "Ativo"', (
            'parametros "Inadimplentes":\n    do time("televendas")\n    quando inadimplentes\n    nao agendar\n\n'
            'parametros "Ativo"'))
        self.turn(ScriptedChat(fenced(with_block), triage=[{"segmentos": [block] + TRIAGED["segmentos"]}]),
                  "Nao agendar inadimplentes\n" + LINES)
        read = change(2, "Ativo: clientes com pedido nos últimos 60 dias, 15 dias")
        fixed = with_block.replace("frequencia de 14 dias", "frequencia de 15 dias")
        chat = ScriptedChat(fenced(ACTIVE_15), fenced(fixed), interpret=[read], triage=[TRIAGED_15])
        out = self.turn(chat, "troque o ativo para 15 dias")
        self.assertIn('"Inadimplentes"', chat.received[1][-1]["content"])
        self.assertEqual((out["divergencias"], len(out["segmentos"])), ([], 3))

    def test_new_block_after_the_frequency_rules_goes_back_to_the_agent(self):
        base = VALID.replace("    frequencia de 28", "    quando no ciclo de vida prospect com a empresa\n    frequencia de 28")
        self.turn(ScriptedChat(fenced(base)), LINES)  # sobram clientes: o bloqueio no fim não é inalcançável
        block = 'parametros "Inadimplentes":\n    do time("televendas")\n    quando inadimplentes\n    nao agendar\n'
        late = base + "\n" + block
        early = base.replace('parametros "Ativo"', block + '\nparametros "Ativo"')
        segments = {"segmentos": TRIAGED["segmentos"] + [
            {"segmento": "Inadimplentes", "trecho": "Inadimplentes: não agendar", "criterio": "inadimplentes",
             "acao": "nao_agendar", "frequencia_dias": 0}]}
        read = {"tipo": "alterar", "versao": 0, "operacoes": [{"op": "incluir", "linha": 0, "texto": "Inadimplentes: não agendar"}]}
        chat = ScriptedChat(fenced(late), fenced(early), interpret=[read], triage=[segments])
        out = self.turn(chat, "não agende os inadimplentes")
        self.assertIn("antes das regras de frequência", chat.received[1][-1]["content"])
        self.assertEqual((out["entregas"], out["divergencias"]), (2, []))

    def test_new_message_replaces_a_turn_that_failed(self):
        def broken(*_args, **_kwargs):
            raise ConnectionError("servidor fora do ar")
        with self.assertRaises(ConnectionError):
            self.turn(broken, "pedido que sempre falha")
        out = self.turn(ScriptedChat(fenced(VALID)), LINES)
        self.assertEqual((out["erros"], out["pedido"]), ([], LINES.split("\n")))

    def test_versions_in_the_doubt_are_cut_from_the_oldest(self):
        versions = [{"n": n, "pedido": [f"pedido {n} " + "x" * 900]} for n in range(1, 7)]
        text = memory.versions_text({"versoes": versions, "versao_atual": 6})
        self.assertIn("versão 6 (atual)", text)
        self.assertNotIn("versão 1", text)
        self.assertIn("omitidas", text)

    def test_pending_question_survives_reopening(self):
        gap = {"segmentos": [TRIAGED["segmentos"][0], {**TRIAGED["segmentos"][1], "frequencia_dias": 0}]}
        res = agent.Resources(self.examples, self.manual, self.embedder, ScriptedChat("x", triage=[gap]))
        with agent.open_memory(self.db) as saver:  # o processo morre com a pergunta na tela
            graph = agent.build_graph(res, saver)
            graph.invoke({"mensagem": "Ativo: 60 dias, 14 dias\nInativo: os demais"}, agent.thread_config("t"))
        chat = ScriptedChat(fenced(VALID), triage=[TRIAGED])
        out = self.turn(chat, None, answers=["a cada 28 dias"])
        self.assertEqual(len(self.asked), 1)
        self.assertIn('"Inativo"', self.asked[0])
        self.assertEqual((out["erros"], out["versao_atual"]), ([], 1))
        self.assertTrue(out["pedido"][-1].startswith(memory.ANSWER_PREFIX))
        self.assertIn("a cada 28 dias", out["pedido"][-1])

    def test_turn_cut_by_an_error_is_resumed_without_a_new_message(self):
        def broken(*_args, **_kwargs):
            raise ConnectionError("servidor fora do ar")
        with self.assertRaises(ConnectionError):
            self.turn(broken, LINES)
        out = self.turn(ScriptedChat(fenced(VALID)), None)
        self.assertEqual((out["erros"], out["versao_atual"]), ([], 1))

    def test_nothing_pending_returns_none(self):
        self.assertIsNone(self.turn(ScriptedChat("x"), None))
        self.started()
        self.assertIsNone(self.turn(ScriptedChat("x"), None))

    def test_unanswered_gap_is_not_asked_again(self):
        gap = {"segmentos": [TRIAGED["segmentos"][0], {**TRIAGED["segmentos"][1], "frequencia_dias": 0}]}
        self.turn(ScriptedChat(fenced(VALID), triage=[gap]), "Ativo: 60 dias, 14 dias\nInativo: os demais")
        self.assertEqual(len(self.asked), 1)
        gap_15 = {"segmentos": [TRIAGED_15["segmentos"][0], gap["segmentos"][1]]}
        out = self.turn(ScriptedChat(fenced(ACTIVE_15), interpret=[change(1, "Ativo: 60 dias, 15 dias")], triage=[gap_15]),
                        "troque o ativo para 15 dias")
        self.assertEqual(len(self.asked), 1)
        self.assertTrue(any('"Inativo"' in w for w in out["avisos"]))

    def test_number_left_out_before_does_not_block_the_next_turn(self):
        request = LINES + "\nCapacidade: 35 clientes por dia"
        self.turn(ScriptedChat(fenced(VALID, "Capacidade 35: o GoBR não tem cláusula para isso.")), request)
        out = self.turn(ScriptedChat(fenced(ACTIVE_15, ""), interpret=[TO_15], triage=[TRIAGED_15]), "troque o ativo para 15 dias")
        self.assertEqual((out["erros"], out["entregas"]), ([], 1))
        read = change(3, "Capacidade: 35 clientes por semana")
        out = self.turn(ScriptedChat(fenced(ACTIVE_15, ""), interpret=[read], triage=[TRIAGED_15]), "capacidade de 35 por semana")
        self.assertTrue(any("35" in e for e in out["erros"]))  # o usuário voltou a pedir o 35: tem de ser tratado de novo

    def test_triage_noise_on_untouched_segments_is_ignored(self):
        self.started()
        noisy = {"segmentos": [TRIAGED_15["segmentos"][0], {**TRIAGED["segmentos"][1], "frequencia_dias": 0, "acao": "indefinido"}]}
        out = self.turn(ScriptedChat(fenced(ACTIVE_15), interpret=[TO_15], triage=[noisy]), "troque o ativo para 15 dias")
        self.assertEqual((self.asked, out["segmentos"][1]["frequencia_dias"]), ([], 28))

    def test_answers_to_the_agent_become_request_lines(self):
        chat = ScriptedChat(call(agent.ASK, {"pergunta": "Quem comprou hoje entra?"}), fenced(VALID))
        out = self.turn(chat, LINES, answers=["sim"])
        self.assertEqual(out["pedido"][2:], [memory.answer_line("Quem comprou hoje entra?", "sim")])

    def test_prompt_does_not_grow_with_the_conversation(self):
        self.started()
        sizes = []
        for n in range(30):
            days, source = (15, ACTIVE_15) if n % 2 == 0 else (14, VALID)
            read = change(1, f"Ativo: clientes com pedido nos últimos 60 dias, {days} dias")
            triaged = TRIAGED_15 if n % 2 == 0 else TRIAGED
            chat = ScriptedChat(fenced(source), interpret=[read], triage=[triaged])
            self.turn(chat, f"troque o ativo para {days} dias")
            sizes.append(len(json.dumps(chat.received[0])))
        self.assertLess(max(sizes) - sizes[0], memory.HISTORY_CHARS * 2)
        self.assertLess(abs(sizes[-1] - sizes[-3]), 200)

    def test_conversations_do_not_mix(self):
        self.started()
        chat = ScriptedChat(fenced(VALID))
        self.turn(chat, LINES, thread="outra")
        self.assertEqual(chat.interpreted, [])
        with agent.open_memory(self.db) as saver:
            self.assertEqual({c["nome"]: c["turnos"] for c in agent.conversations(saver)}, {"t": 1, "outra": 1})


class CheckTurnTest(unittest.TestCase):
    """A avaliação: cada verificação passa e falha pelo motivo certo."""

    def check(self, expected, gobr, previous=(), answer="", questions=0, failed=False):
        return [ok for _, ok in memory_eval.check_turn(expected, gobr, answer, questions, list(previous), failed)]

    def test_right_and_wrong(self):
        expected = {"regras": {"Ativos": {"dias": 15}, "Inativos": {"dias": 28}}, "intactas": ["Inativos"],
                    "numero_ausente": [14], "sem_regra": ["Prospects"], "resposta_tem": ["28"], "perguntas_max": 0}
        self.assertEqual(self.check(expected, ACTIVE_15, [VALID], "são 28 dias"), [True] * 7)
        self.assertEqual(self.check(expected, VALID, [BOTH_CHANGED], "são 128 dias", 1),
                         [False, True, True, False, False, False, False])

    def test_failed_turn_passes_nothing(self):
        expected = {"regras": {"Ativos": {"dias": 14}}, "intactas": ["Inativos"], "perguntas_max": 0, "arquivo_do_turno": 1}
        self.assertEqual(self.check(expected, VALID, [VALID]), [True] * 4)
        self.assertEqual(self.check(expected, VALID, [VALID], failed=True), [False] * 4)

    def test_file_equal_and_different(self):
        expected = {"arquivo_do_turno": 1, "arquivo_difere_do_turno": 2}
        self.assertEqual(self.check(expected, VALID, [VALID, ACTIVE_15]), [True, True])
        self.assertEqual(self.check(expected, VALID, [VALID, VALID]), [True, False])

    def test_names(self):
        rename = VALID.replace('"Inativo"', '"Demais clientes exceto prospects"').replace('"Ativo"', '"Regra 01: Clientes Ativos"')
        expected = {"sem_regra": ["Prospects"], "regras": {"Ativos": {"dias": 14}, "Demais clientes": {"dias": 28}}}
        self.assertEqual(self.check(expected, rename), [True, True, True])
        extra = VALID + '\nparametros "Ativos inadimplentes":\n    do time("televendas")\n    nao agendar\n'
        self.assertEqual(self.check({"regras": {"Ativos": {"dias": 14}}}, extra), [True])

    def test_numbers_and_clauses_include_the_sources_of_the_rule(self):
        def with_segmentation(days: int) -> str:
            return VALID.replace('parametros "Ativo":\n    do time("televendas")', (
                f'segmentacao "base":\n    do time("televendas")\n    recencia de positivacao global em {days} dias\n\n'
                'parametros "Ativo":\n    da segmentacao("base")'))
        self.assertEqual(self.check({"intactas": ["Ativos"], "numero_ausente": [30], "regras": {"Ativos": {"numero": 45}}},
                                    with_segmentation(45), [with_segmentation(30)]), [True, False, True])

    def test_block_has_to_come_before_the_frequency_rules(self):
        block = 'parametros "Inadimplentes":\n    do time("televendas")\n    quando inadimplentes\n    nao agendar\n'
        early = VALID.replace('parametros "Ativo"', block + '\nparametros "Ativo"')
        for source, ok in ((early, True), (VALID + "\n" + block, False), (VALID, False)):
            self.assertEqual(self.check({"bloqueia_antes": ["Inadimplentes"]}, source), [ok])

    def test_number_present_in_some_rule(self):
        self.assertEqual(self.check({"numero_presente": [28, 99]}, VALID), [True, False])

    def test_some_block_that_works(self):
        block = 'parametros "Devedores":@N    do time("televendas")@N    quando inadimplentes@N    nao agendar@N'.replace("@N", chr(10))
        early = VALID.replace('parametros "Ativo"', block + chr(10) + 'parametros "Ativo"')
        for source, ok in ((early, True), (VALID + chr(10) + block, False), (VALID, False)):
            self.assertEqual(self.check({"tem_bloqueio": True}, source), [ok])

    def test_unknown_check_is_an_error(self):
        with self.assertRaises(ValueError):
            self.check({"regra": {}}, VALID)


if __name__ == "__main__":
    unittest.main()

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
REQUEST = "Ativo: clientes com pedido nos últimos 60 dias, 14 dias. Inativo: os demais, 28 dias."


def fenced(text: str, notes: str = "Sem dúvidas.") -> str:
    return f"Segue a regra:\n```gobr\n{text}```\n{notes}"


def between(text: str, start: str, end: str) -> str:
    return text[text.index(start) + len(start):text.index(end)]


class ScriptedChat:
    """LLM falso: devolve as respostas em ordem (repete a última) e guarda as mensagens recebidas."""

    def __init__(self, *replies: str):
        self.replies, self.received = list(replies), []

    def __call__(self, messages: list[dict]) -> str:
        self.received.append(messages)
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

    def tearDown(self):
        self.tmp.cleanup()

    def run_graph(self, chat, **state) -> dict:
        res = agent.Resources(self.examples, self.manual, self.embedder, chat, whole_manual=state.pop("inteiro", False))
        return agent.build_graph(res).invoke({"descricao": REQUEST, **state})

    def test_retrieval_puts_examples_and_manual_in_prompt(self):
        chat = ScriptedChat(fenced(VALID))
        out = self.run_graph(chat)
        self.assertEqual(out["exemplos"][0]["arquivo"], "ativos_a")
        prompt = chat.received[0][1]["content"]
        self.assertIn('parametros "Inativo"', prompt)
        self.assertIn("SECAO-RECENCIA", prompt)
        self.assertEqual(prompt.count("<secao "), agent.MANUAL_K)
        self.assertEqual(chat.received[0][0]["content"], agent.PROMPT.read_text(encoding="utf-8"))

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

    def test_valid_answer_ends_after_one_attempt(self):
        out = self.run_graph(ScriptedChat(fenced(VALID)))
        self.assertEqual((out["tentativas"], out["erros"]), (1, []))
        self.assertTrue(out["resposta"].startswith("```gobr\nVersion 1.0"))

    def test_crlf_and_untagged_fence_are_read(self):
        reply = "```\r\n" + VALID.replace("\n", "\r\n") + "```"
        out = self.run_graph(ScriptedChat(reply))
        self.assertEqual((out["erros"], out["alertas"]), ([], []))

    def test_error_goes_back_to_the_llm_and_is_fixed(self):
        chat = ScriptedChat(fenced(UNKNOWN_CLAUSE), fenced(VALID))
        out = self.run_graph(chat)
        self.assertEqual((out["tentativas"], out["erros"]), (2, []))
        self.assertIn("o cliente sorrir", between(chat.received[1][1]["content"], "<erros>", "</erros>"))

    def test_gives_up_after_max_attempts(self):
        chat = ScriptedChat("Não sei escrever isso.")
        out = self.run_graph(chat)
        self.assertEqual(len(chat.received), agent.MAX_ATTEMPTS)
        self.assertEqual(out["gobr"], "")
        self.assertIn(f"Erros que ficaram depois de {agent.MAX_ATTEMPTS} tentativas", out["resposta"])

    def test_cascade_alert_reaches_the_answer(self):
        out = self.run_graph(ScriptedChat(fenced(LATE_BLOCK)))
        self.assertEqual(out["erros"], [])
        self.assertIn("Baixados: Bloqueio depois de regras de frequência", out["resposta"])

    def test_unreachable_rule_goes_back_to_the_llm(self):
        chat = ScriptedChat(fenced(UNREACHABLE), fenced(VALID))
        out = self.run_graph(chat)
        self.assertEqual((out["tentativas"], out["erros"]), (2, []))
        self.assertIn('"Ativo recente": inalcançável', between(chat.received[1][1]["content"], "<erros>", "</erros>"))

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


if __name__ == "__main__":
    unittest.main()

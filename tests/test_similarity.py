import unittest

import numpy as np

from gobr import agent, similarity
from tests.test_index import WordHashEmbedder

A = 'version 1.0\n# comentário\n\nparametros "Ativo":\n    quando atividade de 30 dias\n    frequencia de 14 dias  # nota\n'
B = 'version 1.0\n\nparametros "Inadimplentes":\n    quando inadimplentes\n    nao agendar\n'


class SimilarityTest(unittest.TestCase):
    def test_comments_and_blank_lines_do_not_count(self):
        text = similarity.code_text(A)
        self.assertNotIn("comentário", text)
        self.assertNotIn("nota", text)
        self.assertNotIn("\n\n", text)
        self.assertIn("frequencia de 14 dias", text)

    def test_equal_files_score_one_and_the_right_gold_is_the_closest(self):
        rows = similarity.cosine_rows({"a": A, "b": B}, {"a": A, "b": B}, WordHashEmbedder())
        self.assertEqual([r["nome"] for r in rows], ["a", "b"])
        for row in rows:
            self.assertAlmostEqual(row["cosseno"], 1.0, places=5)
            self.assertLess(row["piso"], row["cosseno"])
            self.assertTrue(row["mais_proximo"])

    def test_swapped_files_are_not_the_closest(self):
        rows = similarity.cosine_rows({"a": B, "b": A}, {"a": A, "b": B}, WordHashEmbedder())
        self.assertFalse(any(r["mais_proximo"] for r in rows))

    def test_missing_or_empty_output_counts_zero(self):
        rows = similarity.cosine_rows({"b": ""}, {"a": A, "b": B, "c": A}, WordHashEmbedder())
        self.assertEqual([r["cosseno"] for r in rows], [0.0, 0.0, 0.0])
        self.assertFalse(any(r["mais_proximo"] for r in rows))

    def test_single_gold_has_no_floor(self):
        row = similarity.cosine_rows({"a": A}, {"a": A}, WordHashEmbedder())[0]
        self.assertIsNone(row["piso"])

    def test_the_embedder_is_called_once_per_text(self):
        calls = []

        class Counting(WordHashEmbedder):
            def documents(self, texts):
                calls.append(len(texts))
                return super().documents(texts)

        similarity.cosine_rows({"a": A, "b": B}, {"a": A, "b": B}, Counting())
        self.assertEqual(calls, [4])
        self.assertTrue(np.isfinite(calls).all())


class ManualAndResponsesTest(unittest.TestCase):
    def parsed(self, text):
        return agent._package(text)[0]

    def test_clauses_are_the_rules_not_the_teams_and_are_not_repeated(self):
        clauses = similarity.rule_clauses(self.parsed(A))
        self.assertEqual(len(clauses), len(set(clauses)))
        self.assertTrue(any("atividade" in c for c in clauses))
        self.assertFalse(any("version" in c for c in clauses))

    def test_manual_row_has_the_closest_passage_and_the_recognized_fraction(self):
        embedder = WordHashEmbedder()
        manual = embedder.documents(["quando atividade de 30 dias", "frequencia de 14 dias"])
        good = similarity.manual_rows({"a": self.parsed(A)}, manual, embedder)[0]
        self.assertEqual(good["reconhecidas"], 1.0)
        odd = A.replace("quando atividade de 30 dias", "quando o cliente sorrir")
        bad = similarity.manual_rows({"a": self.parsed(odd)}, manual, embedder)[0]
        self.assertLess(bad["reconhecidas"], 1.0)
        self.assertLess(bad["cosseno"], good["cosseno"])

    def test_deliveries_are_the_blocks_the_llm_sent(self):
        fence = "`" * 3
        messages = [{"role": "user", "content": "x"}, {"role": "assistant", "content": f"{fence}gobr\n{A}{fence}"},
                    {"role": "tool", "content": f"{fence}gobr\nx{fence}"}, {"role": "assistant", "content": "sem bloco"},
                    {"role": "assistant", "content": f"{fence}gobr\n{B}{fence}"}]
        self.assertEqual(len(similarity.deliveries(messages, agent.GOBR_BLOCK)), 2)

    def test_responses_need_two_and_equal_ones_score_one(self):
        embedder = WordHashEmbedder()
        self.assertIsNone(similarity.between_responses([A], embedder))
        same = similarity.between_responses([A, A, A], embedder)
        self.assertEqual((same["respostas"], len(same["seguidas"]), same["iguais"]), (3, 2, True))
        self.assertAlmostEqual(same["primeira_ultima"], 1.0, places=5)
        self.assertLess(similarity.between_responses([A, B], embedder)["primeira_ultima"], 0.9)


if __name__ == "__main__":
    unittest.main()

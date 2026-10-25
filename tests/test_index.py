import json
import tempfile
import unittest
import zlib
from pathlib import Path
from unittest import mock

import numpy as np

from gobr import index


class WordHashEmbedder:
    """Bolsa de palavras com hash: determinística e sem modelo, para testar o índice sem torch."""

    model = "teste/hash"

    def _encode(self, texts: list[str]) -> np.ndarray:
        out = np.zeros((len(texts), 256), dtype=np.float32)
        for row, text in enumerate(texts):
            for word in text.lower().replace(";", " ").replace(":", " ").split():
                out[row, zlib.crc32(word.encode()) % 256] += 1
        return out / np.linalg.norm(out, axis=1, keepdims=True)

    documents = queries = _encode


def description(summary: str, rules: list[tuple[str, str, str]], queries: list[str]) -> dict:
    return {
        "resumo": summary,
        "regras": [
            {"id": f"R{n}", "nome": f"Regra Padrao da Pet Exemplo - Customizavel: {seg}", "segmento": seg,
             "criterio": crit, "frequencia": freq, "observacao": ""}
            for n, (seg, crit, freq) in enumerate(rules, 1)
        ],
        "consultas_hipoteticas": queries,
    }


def package(filters: list[str]) -> dict:
    return {"regras": [
        {"tipo_bloco": "parametros", "fonte": "do time televendas", "quando_executa": [], "filtros": [{"codigo": f}], "acoes": [{"codigo": "frequencia 14"}]}
        for f in filters
    ]}


TELEVENDAS = description(
    "Agenda do televendas por recência. Duas faixas.",
    [("Ativos", "compraram nos últimos 60 dias", "14 dias"), ("Inativos", "sem comprar há mais de 60 dias", "28 dias")],
    ["ativos 60 dias a cada 14 dias", "ligar para inativos a cada 28 dias"],
)
PROSPECTS = description(
    "Agenda de prospects da carteira.",
    [("Prospects", "nunca compraram", "7 dias")],
    ["prospects toda semana"],
)


class ChunkTest(unittest.TestCase):
    def test_one_file_chunk_one_per_rule_and_one_per_query(self):
        kinds = [c["tipo"] for c in index.chunks("x", TELEVENDAS)]
        self.assertEqual(kinds, ["arquivo", "regra", "regra", "consulta", "consulta"])

    def test_rule_chunk_has_summary_context_but_not_the_literal_name(self):
        rule = index.chunks("x", TELEVENDAS)[1]
        self.assertEqual(rule["texto"], "Agenda do televendas por recência.\nAtivos: compraram nos últimos 60 dias; 14 dias")
        self.assertNotIn("Pet Exemplo", rule["texto"])
        self.assertIn("Pet Exemplo", rule["nome"])

    def test_file_chunk_lists_every_rule(self):
        self.assertEqual(index.chunks("x", TELEVENDAS)[0]["texto"].count("\n"), 2)


class SignatureTest(unittest.TestCase):
    def test_rule_names_do_not_change_the_signature(self):
        a, b = package(["recencia em 60 dias"]), package(["recencia em 60 dias"])
        b["regras"][0]["nome"] = "outro nome"
        self.assertEqual(index.signature(a), index.signature(b))

    def test_a_different_window_changes_the_signature(self):
        self.assertNotEqual(index.signature(package(["recencia em 60 dias"])), index.signature(package(["recencia em 90 dias"])))


    def test_source_kind_counts_but_the_team_name_does_not(self):
        team, other_team, portfolio = (package(["recencia em 60 dias"]) for _ in range(3))
        other_team["regras"][0]["fonte"] = "do time externo"
        portfolio["regras"][0]["fonte"] = "da carteira carteira televendas"
        self.assertEqual(index.signature(team), index.signature(other_team))
        self.assertNotEqual(index.signature(team), index.signature(portfolio))


class SearchTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.tmp = Path(tmp.name)
        descriptions, contexts, gobr = (self.tmp / d for d in ("descricoes", "contexto", "gobr"))
        for d in (descriptions, contexts, gobr):
            d.mkdir()
        files = {"tele_a": (TELEVENDAS, ["recencia em 60 dias"]), "tele_b": (TELEVENDAS, ["recencia em 60 dias"]),
                 "prospects": (PROSPECTS, ["prospect"])}
        for name, (desc, filters) in files.items():
            (descriptions / f"{name}.json").write_text(json.dumps(desc), encoding="utf-8")
            (contexts / f"{name}.json").write_text(json.dumps(package(filters)), encoding="utf-8")
            (gobr / f"{name}.gobr").write_text("", encoding="utf-8")
        (descriptions / "quebrado.falha.json").write_text("{}", encoding="utf-8")
        self.embedder = WordHashEmbedder()
        self.index = index.build(descriptions, [contexts], [gobr], self.embedder)

    def query(self, text: str) -> np.ndarray:
        return self.embedder.queries([text])[0]

    def test_failed_consolidations_are_not_indexed(self):
        self.assertEqual(sorted(self.index.files), ["prospects", "tele_a", "tele_b"])

    def test_same_structure_is_one_hit_with_the_other_as_equivalent(self):
        hits = index.search(self.index, self.query("inativos 60 dias a cada 28 dias"))
        self.assertEqual([h["arquivo"] for h in hits], ["tele_a", "prospects"])
        self.assertEqual(hits[0]["equivalentes"], ["tele_b"])
        self.assertTrue(hits[0]["gobr"].endswith("tele_a.gobr"))

    def test_hit_points_to_the_closest_rule_of_the_file(self):
        hit = index.search(self.index, self.query("inativos sem comprar há mais de 60 dias"))[0]
        self.assertEqual(hit["regra_mais_parecida"]["regra"], "R2")

    def test_file_score_is_its_best_chunk_among_the_requested_kinds(self):
        query = self.query("prospects toda semana")
        everything = index.search(self.index, query, kinds=index.KINDS)[0]
        self.assertEqual(everything["arquivo"], "prospects")
        self.assertAlmostEqual(everything["nota"], 1.0, places=3)
        own = next(i for i, c in enumerate(self.index.chunks) if c["texto"] == "prospects toda semana")
        self.assertLess(index.search(self.index, query, kinds=index.KINDS, exclude={own})[0]["nota"], 0.99)
        self.assertLess(index.search(self.index, query)[0]["nota"], 0.99)

    def test_shared_numbers_add_weight_times_jaccard(self):
        text = "agenda 60 14 28"
        query, query_numbers = self.query(text), index.numbers(text)
        self.assertEqual(query_numbers, {60, 14, 28})
        plain = index.search(self.index, query, query_numbers, weight=0.0)
        boosted = index.search(self.index, query, query_numbers, weight=1.0)
        self.assertEqual(boosted[0]["arquivo"], "tele_a")
        plain_score = next(h["nota"] for h in plain if h["arquivo"] == "tele_a")
        self.assertAlmostEqual(boosted[0]["nota"] - plain_score, 1.0, places=3)

    def test_save_and_load_keep_chunks_and_vectors(self):
        index.save(self.index, self.tmp / "indice")
        loaded = index.load(self.tmp / "indice")
        self.assertEqual(loaded.chunks, self.index.chunks)
        self.assertEqual(loaded.files, self.index.files)
        np.testing.assert_allclose(loaded.vectors, self.index.vectors, atol=1e-3)

    def test_evaluate_reports_every_variant_and_query_group(self):
        table = index.evaluate(self.index, self.embedder, {"ouro": {"prospects": "prospects que nunca compraram"}})
        self.assertEqual(table[("arquivo", 0.0, "ouro")]["posicoes"], [1])
        self.assertNotIn(("arquivo", 0.0, "consulta_estrutura"), table)
        self.assertEqual(table[("multi-vetor", index.NUMBER_WEIGHT, "consulta_propria")]["n"], 5)

    def test_structure_leave_out_hides_the_queries_of_duplicates_too(self):
        tele = frozenset(i for i, c in enumerate(self.index.chunks)
                         if c["tipo"] == "consulta" and c["arquivo"] in ("tele_a", "tele_b"))
        with mock.patch.object(index, "search", wraps=index.search) as spy:
            index.evaluate(self.index, self.embedder, {})
        self.assertIn(tele, {call.args[5] for call in spy.call_args_list})

    def test_unknown_expected_file_stops_the_evaluation(self):
        with self.assertRaises(SystemExit):
            index.evaluate(self.index, self.embedder, {"ouro": {"nao_existe": "x"}})

    def test_empty_descriptions_folder_stops_before_writing(self):
        with self.assertRaises(SystemExit):
            index.build(self.tmp / "nao_existe", [self.tmp / "contexto"], [], self.embedder)


if __name__ == "__main__":
    unittest.main()

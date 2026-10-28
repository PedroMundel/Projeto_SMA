import json
import tempfile
import unittest
from pathlib import Path

import numpy as np

from gobr import manual, manual_search
from tests.test_index import WordHashEmbedder

OUT = Path(__file__).resolve().parents[1] / "data" / "manual"


def section(blocks: list) -> manual.Section:
    return manual.Section("6.1", "Filtros de atividade", 26, ["6 Filtros de clientes", "6.1 Filtros de atividade"], blocks)


class ChunkTest(unittest.TestCase):
    def test_each_table_row_is_a_chunk_with_the_heading_path(self):
        found = manual.chunks([section([("tabela", [["Filtro", "Descrição"], ["ativos", "Clientes ativos"],
                                                     ["inativos", "Clientes inativos"]])])])
        self.assertEqual([c["texto"] for c in found], [
            "6 Filtros de clientes > 6.1 Filtros de atividade\nFiltro: ativos. Descrição: Clientes ativos",
            "6 Filtros de clientes > 6.1 Filtros de atividade\nFiltro: inativos. Descrição: Clientes inativos",
        ])

    def test_single_column_table_is_one_chunk(self):
        found = manual.chunks([section([("tabela", [["Condicional"], ["<<N>> dias"], ["<<N>> meses"]])])])
        self.assertEqual(len(found), 1)
        self.assertTrue(found[0]["texto"].endswith("Condicional: <<N>> dias; <<N>> meses"))

    def test_prose_is_split_between_blocks_never_inside_code(self):
        code = "parametros \"x\":\n" + "    frequencia de 7 dias\n" * 40
        found = manual.chunks([section([("texto", "a" * 1000), ("codigo", code), ("texto", "fim")])])
        self.assertEqual(len(found), 2)
        self.assertIn(code, found[1]["texto"])

    def test_row_with_empty_first_cell_continues_the_previous_row(self):
        rows = [["Filtro", "Descrição"], ["ativos", "Clientes considerados"]]
        manual._extend_table(rows, [["", "ativos pelo sistema"], ["inativos", "Clientes inativos"]])
        self.assertEqual(rows[1:], [["ativos", "Clientes considerados ativos pelo sistema"], ["inativos", "Clientes inativos"]])


class ExtractedManualTest(unittest.TestCase):
    """Regressões sobre data/manual/, gerado por `python -m gobr manual`."""

    @classmethod
    def setUpClass(cls):
        cls.sections = {s["secao"]: s for s in json.loads((OUT / "secoes.json").read_text(encoding="utf-8"))}
        cls.chunks = [json.loads(line) for line in (OUT / "chunks.jsonl").read_text(encoding="utf-8").splitlines()]

    def test_two_column_table_rows_stay_aligned(self):
        self.assertIn("| ativos | Clientes considerados ativos pelos critérios padrão do sistema |",
                      self.sections["6.1"]["texto"])

    def test_table_split_by_a_page_break_is_one_table(self):
        text = self.sections["6.1"]["texto"]
        self.assertEqual(text.count("|---|"), 1)
        self.assertIn("| atividade de <<tempo>> |", text)

    def test_page_headers_footers_and_rules_are_gone(self):
        noise = [c for c in self.chunks if "©" in c["texto"] or "ALL RIGHTS" in c["texto"] or "....." in c["texto"]]
        self.assertEqual(noise, [])

    def test_third_level_headings_are_sections(self):
        self.assertIn("7.3.6", self.sections)
        self.assertIn("frequencia do vendedor ou de qualquer vendedor ou de 35 dias", self.sections["7.3.6"]["texto"])

    def test_table_continued_on_the_next_page_keeps_its_rows(self):
        self.assertIn("| para o gestor | O alerta é entregue ao gestor |", self.sections["8.7"]["texto"])

    def test_headings_wrapped_in_two_lines_keep_the_whole_title(self):
        self.assertEqual(self.sections["4"]["titulo"], "Regras para carteiras e segmentações de clientes")
        self.assertTrue(self.sections["6.13"]["titulo"].endswith("intervalo no passado"))

    def test_prose_starting_with_inline_code_is_not_turned_into_a_table(self):
        self.assertEqual([c["secao"] for c in self.chunks if "Termo:" in c["texto"]], [])

    def test_symbol_font_arrow_becomes_an_arrow(self):
        self.assertIn("(1) dia do mês → (2) dia da semana", self.sections["5.1"]["texto"])


class SearchTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.dir = Path(tmp.name)
        chunks = [
            {"secao": "6.1", "titulo": "Atividade", "pagina": 26, "tipo": "tabela", "texto": "inativos para a empresa: sem compra com nenhum vendedor"},
            {"secao": "6.1", "titulo": "Atividade", "pagina": 26, "tipo": "tabela", "texto": "ativos para o vendedor: compraram com o vendedor"},
            {"secao": "7.4.1", "titulo": "Frequência fixa", "pagina": 46, "tipo": "tabela", "texto": "frequencia semanal: visita toda semana"},
            {"secao": "8.7", "titulo": "Alvos", "pagina": 57, "tipo": "tabela", "texto": "para o gestor: o alerta é entregue ao gestor"},
        ]
        sections = [{"secao": n, "titulo": t, "pagina": p, "caminho": [], "texto": f"## {n} {t}"}
                    for n, t, p in (("6.1", "Atividade", 26), ("7.4.1", "Frequência fixa", 46), ("8.7", "Alvos", 57))]
        lines = "".join(json.dumps(c, ensure_ascii=False) + "\n" for c in chunks)
        (self.dir / "chunks.jsonl").write_text(lines, encoding="utf-8")
        (self.dir / "secoes.json").write_text(json.dumps(sections, ensure_ascii=False), encoding="utf-8")
        self.embedder = WordHashEmbedder()
        self.index, self.manifest = manual_search.build(self.dir, self.embedder)

    def find(self, text: str, mode: str, k: int = 3) -> list[str]:
        vector = self.embedder.queries([text])[0]
        return [h["secao"] for h in manual_search.search(self.index, text, vector, k, mode)]

    def test_tokens_ignore_case_and_accents(self):
        self.assertEqual(manual_search.tokens("Frequência SEMANAL, à vista"), ["frequencia", "semanal", "a", "vista"])

    def test_bm25_ranks_the_document_with_the_rare_term_first(self):
        scores = self.index.bm25.scores(manual_search.tokens("gestor"))
        self.assertEqual(int(np.argmax(scores)), 3)
        self.assertEqual(scores[0], 0.0)

    def test_every_mode_finds_the_section_and_returns_each_section_once(self):
        for mode in manual_search.MODES:
            found = self.find("frequencia semanal", mode)
            self.assertEqual(found[0], "7.4.1", mode)
            self.assertEqual(len(found), len(set(found)))

    def test_hit_carries_the_whole_section_text(self):
        vector = self.embedder.queries(["alerta para o gestor"])[0]
        hit = manual_search.search(self.index, "alerta para o gestor", vector, 1)[0]
        self.assertEqual((hit["secao"], hit["texto"]), ("8.7", "## 8.7 Alvos"))

    def test_tied_scores_share_a_rank(self):
        ranks = manual_search._ranks(np.array([0.0, 2.0, 0.0, 1.0], dtype=np.float32))
        self.assertEqual(ranks.tolist(), [3.0, 1.0, 3.0, 2.0])

    def test_chunks_without_query_terms_get_no_lexical_share_in_the_fusion(self):
        vector = self.embedder.queries(["gestor"])[0]
        fused = manual_search.chunk_scores(self.index, "gestor", vector, "hibrido")
        dense = manual_search.chunk_scores(self.index, "gestor", vector, "denso")
        only_dense = 1 / (manual_search.RRF_K + manual_search._ranks(dense))
        np.testing.assert_allclose(fused[:3], only_dense[:3])
        self.assertGreater(fused[3], only_dense[3])

    def test_unknown_mode_is_rejected(self):
        with self.assertRaises(ValueError):
            self.find("x", "semantico")

    def test_load_refuses_an_index_built_from_other_chunks(self):
        manual_search.save(self.index, self.manifest, self.dir / "indice")
        saved = json.loads((self.dir / "indice" / "manifesto.json").read_text(encoding="utf-8"))
        self.assertEqual(saved["manual"], "..")  # relativo ao índice: carrega de qualquer pasta
        self.assertEqual(len(manual_search.load(self.dir / "indice").chunks), 4)
        with open(self.dir / "chunks.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps({"secao": "8.7", "titulo": "Alvos", "pagina": 57, "tipo": "prosa", "texto": "novo"}) + "\n")
        with self.assertRaises(SystemExit):
            manual_search.load(self.dir / "indice")

    def test_evaluate_counts_any_expected_section_as_a_hit(self):
        queries = [{"consulta": "frequencia semanal", "tipo": "sintaxe", "esperadas": ["6.1", "7.4.1"]},
                   {"consulta": "alerta gestor", "tipo": "necessidade", "esperadas": ["8.7"]}]
        table = manual_search.evaluate(self.index, self.embedder, queries, k=2)
        self.assertEqual(table[("bm25", "todas")]["recall@1"], 1.0)
        self.assertEqual(table[("hibrido", "sintaxe")]["n"], 1)

    def test_evaluate_rejects_expected_sections_without_chunks_and_empty_sets(self):
        for queries in ([{"consulta": "x", "tipo": "conceito", "esperadas": ["99"]}], []):
            with self.assertRaises(SystemExit):
                manual_search.evaluate(self.index, self.embedder, queries)


if __name__ == "__main__":
    unittest.main()

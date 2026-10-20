import copy
import json
import tempfile
import unittest
from pathlib import Path

from gobr.consensus import Candidate, choose
from gobr.context import build
from gobr.validate import Report, check
from gobr.intervals import INF, NEVER, IntervalSet
from gobr.parser import parse_file, unrecognized
from gobr.text import Literals, fold, logical_lines

ROOT = Path(__file__).resolve().parents[1] / "trabalho" / "trabalho"
EXAMPLES = ROOT / "exemplos"
CORPUS = ROOT / "referencias"


def rule(package: dict, name: str) -> dict:
    return next(r for r in package["regras"] if r["nome"] == name)


class IntervalSetTest(unittest.TestCase):
    def test_subtracting_a_shorter_window_leaves_the_older_band(self):
        self.assertEqual(IntervalSet.of(0, 90) - IntervalSet.of(0, 60), IntervalSet.of(61, 90))

    def test_complement_of_window_includes_never(self):
        self.assertEqual(IntervalSet.of(0, 45).complement(), IntervalSet(((NEVER, NEVER), (46, INF))))

    def test_adjacent_spans_merge(self):
        self.assertEqual(IntervalSet.of(0, 60) | IntervalSet.of(61, 90), IntervalSet.of(0, 90))


class LexerTest(unittest.TestCase):
    def test_accented_verb_e_is_not_read_as_connective(self):
        self.assertEqual(fold("cnae é igual"), "cnae eh igual")

    def test_continuation_lines_join_into_one_statement(self):
        source = 'parametros "x":\n    quando ativos\n        e adimplentes\n    nao agendar\n'
        texts = [line.text for line in logical_lines(source, Literals())]
        self.assertEqual(texts, ["parametros <s0>:", "quando ativos e adimplentes", "nao agendar"])

    def test_string_contents_keep_accents(self):
        literals = Literals()
        logical_lines('    quando nome da cidade igual("Cordeirópolis")\n', literals)
        self.assertEqual(literals.strings, ["Cordeirópolis"])


class GoldenExamplesTest(unittest.TestCase):
    """Effective conditions must read like the business descriptions in exemplos/*.pdf."""

    @classmethod
    def setUpClass(cls):
        cls.maxlub = build(EXAMPLES / "RegraMaxlub.gobr")
        cls.infinitto = build(EXAMPLES / "RegraInfinittoDesign.gobr")
        cls.v1 = build(EXAMPLES / "V1Vidros-RegraComercial.gobr")

    def test_maxlub_risk_band_excludes_active_clients(self):
        self.assertEqual(rule(self.maxlub, "Risco de inatividade")["condicao_efetiva"],
                         "compraram nos últimos 90 dias, mas estão há mais de 60 dias sem comprar")

    def test_maxlub_blocks_are_listed_once_not_repeated_per_rule(self):
        self.assertEqual(rule(self.maxlub, "Clientes ativos")["condicao_efetiva"], "compraram nos últimos 60 dias")

    def test_infinitto_fallback_describes_the_remaining_clients(self):
        text = rule(self.infinitto, "Inativo (Com último pedido há mais de 90d atrás)")["condicao_efetiva"]
        self.assertIn("há mais de 90 dias", text)

    def test_infinitto_flags_mixed_recency_scopes(self):
        self.assertTrue(any("escopos de recência" in a for a in self.infinitto["alertas"]))

    def test_v1_prospects_are_not_absorbed_by_outside_recency_rule(self):
        self.assertEqual(rule(self.v1, "Clientes Prospects")["condicao_efetiva"],
                         "nunca compraram com qualquer vendedor da empresa")

    def test_v1_reports_clients_left_without_rule(self):
        self.assertEqual(self.v1["nao_cobertos"]["do time televendas"],
                         "já compraram com qualquer vendedor da empresa e nunca compraram no grupo de vendedores")

    def test_rules_over_whole_carteira_partition_leave_no_gap(self):
        self.assertEqual(build(CORPUS / "regra_001.gobr")["nao_cobertos"], {})


class AlertsTest(unittest.TestCase):
    def test_name_citing_other_frequency_than_code_is_flagged(self):
        package = build(CORPUS / "regra_060.gobr")
        self.assertTrue(any("cita 14" in a for r in package["regras"] for a in r["alertas"]))


def build_source(body: str) -> dict:
    source = 'version 1.0\n\ntime "tv":\n    vendedores todostelevendas\n\n' + body
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "caso.gobr"
        path.write_text(source, encoding="utf-8")
        return build(path)


def params(name: str, *lines: str, source: str = 'do time("tv")') -> str:
    return f'parametros "{name}":\n    {source}\n' + "".join(f"    {line}\n" for line in lines) + "\n"


class CascadeRegressionTest(unittest.TestCase):
    def test_facts_with_different_scope_stay_distinct(self):
        package = build_source(params("a", "quando na agenda global de hoje", "nao agendar")
                               + params("b", "quando na agenda do vendedor de hoje", "frequencia de 7 dias"))
        self.assertFalse(rule(package, "b")["inalcancavel"])

    def test_inactivity_greater_than_excludes_the_boundary_day(self):
        package = build_source(params("a", "quando inatividade maior que 31 dias", "frequencia de 7 dias"))
        self.assertIn("mais de 31", rule(package, "a")["condicao_efetiva"])

    def test_every_day_filter_still_consumes_clients(self):
        package = build_source(params("a", "todos os dias", "quando ativos", "frequencia de 7 dias")
                               + params("b", "quando ativos", "frequencia de 14 dias"))
        self.assertTrue(rule(package, "b")["inalcancavel"])

    def test_closed_lifecycle_list_does_not_shadow_prospects(self):
        stages = "".join(params(f"c{i}", f"quando no ciclo de vida {s} com a empresa", "frequencia de 7 dias")
                         for i, s in enumerate(["ativo", "inativo", "ativado", "reativado"]))
        package = build_source(stages + params("p", "quando no ciclo de vida prospect com a empresa", "frequencia de 7 dias"))
        self.assertFalse(rule(package, "p")["inalcancavel"])

    def test_several_carteiras_in_one_source_mean_any_of_them(self):
        body = ('carteira "a":\n    clientes carteirafixa("tv")\n    quando ativos\n\n'
                'carteira "b":\n    clientes carteirafixa("tv")\n\n'
                + params("ab", "frequencia de 7 dias", source='da carteira("a","b")')
                + params("b", "frequencia de 14 dias", source='da carteira("b")'))
        self.assertTrue(rule(build_source(body), "b")["inalcancavel"])

    def test_registration_age_ladder_collapses_to_bands(self):
        package = build_source(params("a", "quando cadastrado faz 30 dias", "frequencia de 20 dias")
                               + params("b", "quando cadastrado faz 15 dias", "frequencia de 15 dias"))
        self.assertEqual(rule(package, "b")["condicao_efetiva"], "cadastrados no ERP há pelo menos 15 e menos de 30 dias")

    def test_cascade_exclusions_in_a_union_are_not_required_numbers(self):
        package = build_source(params("a", "quando cadastrado faz 60 dias", "e unica compra com o vendedor", "nao agendar")
                               + params("b", "quando recencia de positivacao em 30 dias", "frequencia de 14 dias"))
        self.assertEqual(rule(package, "b")["numeros_exigidos"], [14, 30])

    def test_contradictory_recency_scopes_make_rule_unreachable(self):
        package = build_source(params("x", "quando recencia de positivacao do vendedor em 30 dias",
                                      "e fora da recencia de positivacao global em 60 dias", "frequencia de 7 dias"))
        self.assertTrue(rule(package, "x")["inalcancavel"])


class CorpusSmokeTest(unittest.TestCase):
    def test_every_reference_file_builds(self):
        for path in sorted(CORPUS.glob("*.gobr")):
            with self.subTest(path=path.name):
                package = build(path)
                self.assertTrue(package["regras"] or package["carteiras"])

    def test_only_known_syntax_errors_remain_unrecognized(self):
        leftovers = {(p.name, bid) for p in sorted(CORPUS.glob("*.gobr")) for bid, _ in unrecognized(parse_file(p))}
        self.assertEqual(leftovers, {("regra_032.gobr", "R74"), ("regra_221.gobr", "R6")})


class RedatorContractTest(unittest.TestCase):
    """The frozen few-shot answers must satisfy the validator; corrupted copies must not."""

    @classmethod
    def setUpClass(cls):
        project = Path(__file__).resolve().parents[1]
        cls.package = build(EXAMPLES / "RegraMaxlub.gobr")
        cls.answer = json.loads((project / "redator/exemplos/RegraMaxlub.saida.json").read_text(encoding="utf-8"))

    def corrupted(self, rule_index: int, field: str, value: str) -> dict:
        answer = copy.deepcopy(self.answer)
        answer["regras"][rule_index][field] = value
        return answer

    def test_frozen_example_answer_is_valid(self):
        self.assertEqual(check(self.answer, self.package).errors, [])

    def test_missing_threshold_is_an_error(self):
        answer = self.corrupted(5, "criterio", "Clientes que compraram nos últimos 90 dias")
        self.assertTrue(any("faltam os números [60]" in e for e in check(answer, self.package).errors))

    def test_invented_number_is_an_error(self):
        answer = self.corrupted(4, "frequencia", "15 dias")
        self.assertTrue(any("não existem no pacote [15]" in e for e in check(answer, self.package).errors))

    def test_renamed_rule_is_an_error(self):
        answer = self.corrupted(0, "nome", "Bloqueio Receita")
        self.assertTrue(any("nome alterado" in e for e in check(answer, self.package).errors))

    def test_single_valid_candidate_has_no_measured_agreement(self):
        _, agreement = choose([Candidate(Path("agente_1.json"), self.answer, Report())])
        self.assertIsNone(agreement)

    def test_consensus_picks_the_candidate_closest_to_the_others(self):
        outlier = self.corrupted(5, "criterio", "Texto completamente diferente sobre outra coisa, 90 e 60 dias")
        candidates = [Candidate(Path(f"agente_{i}.json"), answer, Report())
                      for i, answer in enumerate([outlier, self.answer, copy.deepcopy(self.answer)])]
        chosen, _ = choose(candidates)
        self.assertNotEqual(chosen.path.name, "agente_0.json")


if __name__ == "__main__":
    unittest.main()

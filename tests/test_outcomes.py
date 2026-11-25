import unittest

from gobr import agent, outcomes
from gobr.intervals import NEVER
from tests.test_agent import HEADER, VALID, one_rule

EARLY = VALID.replace('parametros "Ativo"', one_rule("inadimplentes", action="nao agendar", name="Inadimplentes") + 'parametros "Ativo"')
LATE = VALID + "\n" + one_rule("inadimplentes", action="nao agendar", name="Inadimplentes")


def parsed(text: str):
    return agent._package(text)[0]


class OutcomesTest(unittest.TestCase):
    def test_each_client_gets_the_first_rule_that_takes_it(self):
        got = outcomes.outcomes(parsed(VALID), [(0, 0), (60, 60), (61, 61), (NEVER, NEVER), (90, 10)], {})
        # o filtro do VALID é global: quem comprou há 10 dias com outro vendedor da empresa é ativo
        self.assertEqual(got, ["14 dias", "14 dias", "28 dias", "28 dias", "14 dias"])

    def test_no_rule_and_block_are_not_scheduled(self):
        only = HEADER + one_rule("atividade de 30 dias")
        self.assertEqual(outcomes.outcomes(parsed(only), [(30, 30), (31, 31), (90, 10)], {}),
                         ["14 dias", outcomes.NOT_SCHEDULED, outcomes.NOT_SCHEDULED])
        overdue = {"inadimplente": True}
        self.assertEqual(outcomes.outcomes(parsed(EARLY), [(5, 5)], overdue), [outcomes.NOT_SCHEDULED])
        self.assertEqual(outcomes.outcomes(parsed(LATE), [(5, 5)], overdue), ["14 dias"])
        self.assertEqual(outcomes.outcomes(parsed(EARLY), [(5, 5)], {}), ["14 dias"])

    def test_prospects(self):
        rules = HEADER + one_rule("no ciclo de vida prospect com a empresa", action="frequencia de 7 dias", name="Prospects")
        self.assertEqual(outcomes.outcomes(parsed(rules), [(NEVER, NEVER), (NEVER, 30), (30, 30)], {}),
                         ["7 dias", outcomes.NOT_SCHEDULED, outcomes.NOT_SCHEDULED])

    def test_global_rupture_is_the_band_the_manual_defines(self):
        for period, (low, high) in {"bimestre": (30, 60), "trimestre": (61, 90), "semestre": (91, 180), "ano": (181, 365)}.items():
            rules = parsed(HEADER + one_rule(f"em ruptura global do {period}"))
            clients = [(d, d) for d in (low - 1, low, high, high + 1, NEVER)]
            self.assertEqual(outcomes.outcomes(rules, clients, {}),
                             [outcomes.NOT_SCHEDULED, "14 dias", "14 dias", outcomes.NOT_SCHEDULED, outcomes.NOT_SCHEDULED])

    def score(self, made: str, gold: str) -> dict:
        return outcomes.agreement(parsed(made), parsed(gold))

    def test_agreement_is_the_mean_over_the_gold_rules(self):
        self.assertEqual(self.score(VALID, VALID)["media"], 1.0)
        changed = self.score(VALID.replace("de 14 dias", "de 15 dias"), VALID)
        self.assertEqual((changed["media"], changed["regras"]), (0.5, {"Ativo": 0.0, "Inativo": 1.0}))

    def test_late_block_and_missing_rules_are_seen(self):
        self.assertEqual(self.score(LATE, EARLY)["regras"], {"Inadimplentes": 0.0, "Ativo": 1.0, "Inativo": 1.0})
        self.assertEqual(self.score(VALID, EARLY)["regras"]["Inadimplentes"], 0.0)
        prospects = VALID.replace('parametros "Ativo"', one_rule("no ciclo de vida prospect com a empresa", action="frequencia de 7 dias",
                                                                 name="Prospects") + 'parametros "Ativo"')
        self.assertEqual(self.score(VALID, prospects)["regras"]["Prospects"], 0.0)
        revenue = VALID.replace('parametros "Ativo"', one_rule("status na receita federal definido como baixada", action="nao agendar",
                                                               name="Baixados") + 'parametros "Ativo"')
        self.assertEqual(self.score(VALID, revenue)["regras"]["Baixados"], 0.0)

    def test_attributes_of_the_files_are_exercised(self):
        for clause in ("inativos para o vendedor", "elegivel", "curva A com a empresa"):
            with self.subTest(clause=clause):
                gold = HEADER + one_rule(clause, action="frequencia de 7 dias", name="X") + one_rule("atividade de 60 dias")
                made = gold.replace("frequencia de 7 dias", "frequencia de 90 dias")
                self.assertEqual(self.score(made, gold)["regras"]["X"], 0.0)

    def test_frequencies_not_in_days_are_compared_by_their_text(self):
        gold = HEADER + one_rule("atividade de 60 dias", action="frequencia do historico")
        self.assertEqual(self.score(gold.replace("frequencia do historico", "frequencia fixa semanal"), gold)["regras"],
                         {"Ativos": 0.0, outcomes.UNSEEN: 1.0})

    def test_empty_and_catch_all_score_low(self):
        gold = agent.ROOT / "trabalho" / "trabalho" / "exemplos" / "V1Vidros-RegraComercial.gobr"
        base = outcomes.baselines(agent._package(agent.read_source(gold))[0])
        self.assertLess(base["vazio"], 0.35)
        self.assertLess(base["uma regra"], 0.65)

    def test_single_day_rule_of_the_maxlub_is_seen(self):
        gold = HEADER + one_rule("atividade de 60 dias")
        made = HEADER + one_rule("atividade de 60 dias", "inatividade de 60 dias")
        self.assertAlmostEqual(self.score(made, gold)["regras"]["Ativos"], 1 / 61)


if __name__ == "__main__":
    unittest.main()

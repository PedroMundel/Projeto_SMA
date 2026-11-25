import unittest

from gobr import agent, cascade, equality

TIME = 'Version 1.0\n\ntime "televendas":\n    vendedores todostelevendas ativados\n\n'


def rule(name, filters, action="frequencia de 14 dias", team="televendas"):
    when = "".join(f"    {'quando' if n == 0 else 'e'} {f}\n" for n, f in enumerate(filters))
    return f'parametros "{name}":\n    do time("{team}")\n{when}    {action}\n\n'


def parsed(*rules):
    return agent._package(TIME + "".join(rules))[0]


ACTIVE = rule("Ativo", ["atividade de 30 dias"])


class EqualityTest(unittest.TestCase):
    def test_same_rules_are_equal_both_ways_whatever_the_name_or_order(self):
        other = rule("Prospects", ["no ciclo de vida prospect com a empresa"], "frequencia de 30 dias")
        result = equality.compare(parsed(other, ACTIVE.replace('"Ativo"', '"Cliente ativo"')), parsed(ACTIVE, other))
        self.assertEqual((result["sintatica"], result["semantica"], result["regras"]), (2, 2, 2))
        same = equality.compare(parsed(ACTIVE, other), parsed(ACTIVE, other))
        self.assertTrue(same["arquivo_sintatico"] and same["arquivo_semantico"])

    def test_same_meaning_written_differently_is_semantic_only(self):
        made = parsed(rule("Ativo", ["recencia de positivacao em 30 dias"]))
        result = equality.compare(made, parsed(ACTIVE))
        self.assertEqual(result["sintatica"], 0)
        self.assertEqual(result["semantica"], 1)

    def test_other_days_or_other_action_are_different(self):
        for changed in (rule("Ativo", ["atividade de 45 dias"]), rule("Ativo", ["atividade de 30 dias"], "frequencia de 7 dias"),
                        rule("Ativo", ["atividade de 30 dias"], "nao agendar")):
            result = equality.compare(parsed(changed), parsed(ACTIVE))
            self.assertEqual((result["sintatica"], result["semantica"]), (0, 0))
            self.assertEqual(result["faltam_semantica"], ["Ativo"])

    def test_each_generated_rule_counts_once_and_extra_rules_break_the_file(self):
        result = equality.compare(parsed(ACTIVE), parsed(ACTIVE, ACTIVE.replace('"Ativo"', '"Ativo 2"')))
        self.assertEqual((result["sintatica"], result["regras"]), (1, 2))
        extra = equality.compare(parsed(ACTIVE, rule("Outra", ["inadimplentes"], "nao agendar")), parsed(ACTIVE))
        self.assertEqual((extra["sintatica"], extra["semantica"]), (1, 1))
        self.assertFalse(extra["arquivo_sintatico"])

    def test_another_order_is_not_the_same_file(self):
        a, b = rule("A", ["recencia de positivacao em 30 dias"]), rule("B", ["recencia de positivacao em 60 dias"], "frequencia de 7 dias")
        result = equality.compare(parsed(b, a), parsed(a, b))
        self.assertEqual((result["sintatica"], result["semantica"]), (2, 2))
        self.assertFalse(result["arquivo_sintatico"] or result["arquivo_semantico"])

    def test_the_whole_action_counts(self):
        for action in ("frequencia de 14 dias ou do vendedor", "frequencia de 14 dias\n    preferencia na segunda"):
            result = equality.compare(parsed(rule("Ativo", ["atividade de 30 dias"], action)), parsed(ACTIVE))
            self.assertEqual(result["semantica"], 0, action)

    def test_order_of_listed_values_does_not_change_the_key(self):
        one = rule("A", ['ramo de atividade igual("1","2","3","4","5")'])
        two = rule("A", ['ramo de atividade igual("5","4","3","2","1")'])
        self.assertEqual(equality.semantic_key(cascade.compute(parsed(one))[-1]), equality.semantic_key(cascade.compute(parsed(two))[-1]))

    def test_contradictory_rules_are_only_equal_to_the_same_rule(self):
        one = rule("A", ["atividade de 10 dias", "inatividade de 90 dias"])
        two = rule("A", ["atividade de 20 dias", "inatividade de 95 dias"])
        self.assertEqual(equality.compare(parsed(one), parsed(two))["semantica"], 0)
        self.assertEqual(equality.compare(parsed(one), parsed(one))["semantica"], 1)

    def test_scope_is_part_of_the_meaning(self):
        result = equality.compare(parsed(rule("Ativo", ["atividade global de 30 dias"])), parsed(ACTIVE))
        self.assertEqual(result["semantica"], 0)


if __name__ == "__main__":
    unittest.main()

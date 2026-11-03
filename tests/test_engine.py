import unittest
from engine import ForwardChainingEngine, Rule

class TestForwardChainingEngine(unittest.TestCase):
    def test_can_fire_when_all_antecedents_exist(self):
        rule = Rule(["budget_high", "portable"],
                    "recommend:premium_ultrabook", 5, "Premium Ultrabook")
        engine = ForwardChainingEngine([rule])
        engine.assert_facts(["budget_high", "portable"])
        self.assertTrue(engine.can_fire(rule))

    def test_cannot_fire_when_an_antecedent_is_missing(self):
        rule = Rule(["budget_high", "portable"],
                    "recommend:premium_ultrabook")
        engine = ForwardChainingEngine([rule])
        engine.assert_facts(["budget_high"])
        self.assertFalse(engine.can_fire(rule))

    def test_consequent_is_not_added_twice(self):
        rule = Rule(["budget_high"], "recommend:premium_ultrabook")
        engine = ForwardChainingEngine([rule])
        engine.assert_facts(["budget_high", "recommend:premium_ultrabook"])
        self.assertFalse(engine.can_fire(rule))

    def test_higher_priority_rule_fires_first(self):
        rules = [
            Rule(["gaming"], "spec:gaming_features", 2, "Gaming specification"),
            Rule(["gaming"], "recommend:high_end_gaming_laptop", 5, "Pro gaming"),
        ]
        engine = ForwardChainingEngine(rules)
        engine.assert_facts(["gaming"])
        engine.run()
        self.assertEqual(engine.trace[0]["rule"], "Pro gaming")

    def test_conclusions_separate_fact_types(self):
        engine = ForwardChainingEngine([])
        engine.assert_facts([
            "budget_high", "recommend:premium_ultrabook", "spec:ram_16_plus"
        ])
        result = engine.conclusions()
        self.assertIn("premium_ultrabook", result["recommendations"])
        self.assertIn("ram_16_plus", result["specs"])
        self.assertIn("budget_high", result["other_facts"])
        
if __name__ == "__main__":
    unittest.main()

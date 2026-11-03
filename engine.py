from dataclasses import dataclass
from typing import List, Set, Dict, Any

@dataclass
class Rule:
    antecedents: list[str]
    consequent: str
    priority: int = 0
    name: str = ""


class ForwardChainingEngine:
    def __init__(self, rules: list[Rule]):
        self.rules = rules
        self.facts: set[str] = set()
        self.trace: list[dict[str, Any]] = []

    def assert_facts(self, initial: list[str]) -> None:
        self.facts.update(initial)

    def can_fire(self, rule: Rule) -> bool:
        for antecedent in rule.antecedents:
            if antecedent not in self.facts:
                return False
        if rule.consequent in self.facts:
            return False
        return True

    def run(self) -> None:
        while True:
            firable = [rule for rule in self.rules if self.can_fire(rule)]
            if not firable:
                break
            firable.sort(key=lambda rule: (-rule.priority, rule.name))
            chosen = firable[0]
            self.facts.add(chosen.consequent)
            self.trace.append({
                "rule": chosen.name,
                "consequent": chosen.consequent,
                "antecedents": chosen.antecedents.copy(),
                "priority": chosen.priority,
            })

    def conclusions(self) -> dict[str, list[str]]:
        recommendations = []
        specs = []
        others = []
        for fact in sorted(self.facts):
            if fact.startswith("recommend:"):
                recommendations.append(fact.split(":", 1)[1])
            elif fact.startswith("spec:"):
                specs.append(fact.split(":", 1)[1])
            else:
                others.append(fact)
        return {
            "recommendations": recommendations,
            "specs": specs,
            "other_facts": others,
        }

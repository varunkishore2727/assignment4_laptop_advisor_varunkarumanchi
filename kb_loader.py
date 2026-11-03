import json
from pathlib import Path
from engine import Rule


def load_rules(file_path: str | Path) -> list[Rule]:
    """Load IF-THEN rules from the JSON knowledge base."""
    with Path(file_path).open("r", encoding="utf-8") as file:
        rule_data = json.load(file)

    rules = []
    for item in rule_data:
        rules.append(Rule(
            antecedents=item["if"],
            consequent=item["then"],
            priority=item.get("priority", 0),
            name=item.get("name", ""),
        ))
    return rules

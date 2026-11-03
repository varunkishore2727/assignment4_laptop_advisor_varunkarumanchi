from pathlib import Path
from engine import ForwardChainingEngine
from kb_loader import load_rules

BASE_DIR = Path(__file__).resolve().parent
RULES_FILE = BASE_DIR / "kb" / "laptop_rules.json"


def ask_yes_no(question):
    while True:
        answer = input(question + " (y/n): ").strip().lower()

        if answer == "y":
            return True
        elif answer == "n":
            return False
        else:
            print("Please enter y or n.")


def ask_word(question, options):
    while True:
        answer = input(question).strip().lower()

        if answer in options:
            return answer
        else:
            print("Please enter one of:", ", ".join(options))


def collect_initial_facts():
    facts = []

    budget = ask_word(
        "What is your budget? (low/medium/high): ",
        ["low", "medium", "high"]
    )
    facts.append("budget_" + budget)

    if ask_yes_no("Is portability important?"):
        facts.append("portable")

    if ask_yes_no("Do you need long battery life?"):
        facts.append("long_battery")

    if ask_yes_no("Will you use the laptop for gaming?"):
        facts.append("gaming")

    if ask_yes_no("Will you do creative work (photo/video editing, 3D)?"):
        facts.append("creative_work")

    if ask_yes_no("Is the laptop only for office tasks (documents, email)?"):
        facts.append("office_only")

    if ask_yes_no("Do you travel often?"):
        facts.append("travel_often")

    if ask_yes_no("Do you need a large screen (15+ inches)?"):
        facts.append("large_screen")

    os_preference = ask_word(
        "Preferred OS (windows/macos/linux): ",
        ["windows", "macos", "linux"]
    )

    if os_preference == "macos":
        facts.append("pref_os_macos")
    elif os_preference == "linux":
        facts.append("pref_os_linux")
    else:
        facts.append("pref_os_windows")

    if ask_yes_no("Do you need AI acceleration (e.g., for ML)?"):
        facts.append("needs_ai_accel")

    return facts


def display_results(engine):
    results = engine.conclusions()

    if results["recommendations"]:
        for recommendation in results["recommendations"]:
            print("> Recommendation:", recommendation)

            for item in engine.trace:
                if item["consequent"] == "recommend:" + recommendation:
                    print("> Explanation: derived from rule '" + item["rule"] + "'")
                    break
    else:
        print("> No matching laptop recommendation.")

    if results["specs"]:
        print("\n> Recommended specifications:")
        for spec in results["specs"]:
            print("-", spec.replace("_", " ").title())
    print("\nFacts collected:")
    for fact in sorted(engine.facts):
        print("-", fact)

    print("\nRules fired:")

    for number, item in enumerate(engine.trace, start=1):
        print(str(number) + ". " + item["rule"])
        print("   IF:", ", ".join(item["antecedents"]))
        print("   THEN:", item["consequent"])
        print("   Priority:", item["priority"])

    if not engine.trace:
        print("No rules fired.")

    print("=" * 50)


def main():
    print("LAPTOP ADVISOR - FORWARD CHAINING EXPERT SYSTEM")
    print("-" * 50)

    rules = load_rules(RULES_FILE)
    print("Loaded", len(rules), "rules.")

    initial_facts = collect_initial_facts()

    print("\nFacts collected:", initial_facts)

    engine = ForwardChainingEngine(rules)
    engine.assert_facts(initial_facts)

    engine.run()

    display_results(engine)


if __name__ == "__main__":
    main()
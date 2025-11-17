from src.agent import run_panoptes_scout


CASES: dict[str, dict] = {
    "balanced": {
        "csv_path": "eval_data/balanced_sample.csv",
        "target_column": "label",
    },
    "imbalanced": {
        "csv_path": "eval_data/imbalanced_sample.csv",
        "target_column": "label",
    },
    "missing_values": {
        "csv_path": "eval_data/missing_values_sample.csv",
        "target_column": "label",
    },
}


def run_case(name: str) -> None:
    case = CASES[name]
    print(f"=== {name} ({case['csv_path']}) ===")
    briefing = run_panoptes_scout(
        csv_path=case["csv_path"],
        target_column=case["target_column"],
    )
    print(briefing)
    print()


def run_all() -> None:
    for name in CASES:
        run_case(name)


if __name__ == "__main__":
    run_all()

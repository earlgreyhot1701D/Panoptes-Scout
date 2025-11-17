import argparse

from .agent import run_panoptes_scout


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run Panoptes Scout on a CSV file."
    )
    parser.add_argument("csv_path", help="Path to the CSV file.")
    parser.add_argument(
        "--target_column",
        dest="target_column",
        default=None,
        help="Optional name of the target column.",
    )
    args = parser.parse_args()

    briefing = run_panoptes_scout(
        csv_path=args.csv_path,
        target_column=args.target_column,
    )
    print(briefing)


if __name__ == "__main__":
    main()

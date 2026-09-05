from __future__ import annotations

import argparse
from pathlib import Path

from scripts.modules import analyze_and_decide, clean_and_categorize
from scripts.modules import engagement_priority, visualize_priority, visualize_report

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = PROJECT_ROOT / "data" / "Connections.csv"
DEFAULT_OUTPUT = PROJECT_ROOT / "output"

STEPS = (
    "categorize",
    "recommend",
    "report",
    "prioritize",
    "priority-report",
    "all",
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="linkedin-network-analyzer",
        description=(
            "Analyze a local LinkedIn Connections.csv export with explainable, "
            "deterministic heuristics."
        ),
    )
    parser.add_argument(
        "--input",
        default=str(DEFAULT_INPUT),
        help="Path to a LinkedIn Connections.csv export.",
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT),
        help="Directory for generated CSV, Excel, and report files.",
    )
    parser.add_argument(
        "--step",
        choices=STEPS,
        default="all",
        help="Pipeline stage to run. Default: all.",
    )
    return parser


def run_pipeline(input_file: str | Path, output_dir: str | Path, step: str = "all") -> None:
    input_path = Path(input_file)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    categorized_file = output_path / "all_connections_categorized.csv"
    actions_file = output_path / "final_linkedin_actions.xlsx"
    priority_file = output_path / "linkedin_priority.xlsx"
    reports_dir = output_path / "reports"
    priority_reports_dir = output_path / "priority_reports"

    if step in {"categorize", "all"}:
        clean_and_categorize.clean_and_categorize(input_path, output_path)

    if step in {"recommend", "all"}:
        if not categorized_file.exists():
            clean_and_categorize.clean_and_categorize(input_path, output_path)
        analyze_and_decide.analyze_and_decide(categorized_file, actions_file)

    if step in {"prioritize", "all"}:
        if not actions_file.exists():
            if not categorized_file.exists():
                clean_and_categorize.clean_and_categorize(input_path, output_path)
            analyze_and_decide.analyze_and_decide(categorized_file, actions_file)
        engagement_priority.add_priority_score(actions_file, priority_file)

    if step in {"report", "all"}:
        if not actions_file.exists():
            if not categorized_file.exists():
                clean_and_categorize.clean_and_categorize(input_path, output_path)
            analyze_and_decide.analyze_and_decide(categorized_file, actions_file)
        visualize_report.visualize_report(actions_file, reports_dir)

    if step in {"priority-report", "all"}:
        if not priority_file.exists():
            if not actions_file.exists():
                if not categorized_file.exists():
                    clean_and_categorize.clean_and_categorize(input_path, output_path)
                analyze_and_decide.analyze_and_decide(categorized_file, actions_file)
            engagement_priority.add_priority_score(actions_file, priority_file)
        visualize_priority.visualize_priority(priority_file, priority_reports_dir)

    print(f"Completed '{step}' workflow. Outputs: {output_path}")


def main() -> None:
    args = build_parser().parse_args()
    run_pipeline(args.input, args.output_dir, args.step)


if __name__ == "__main__":
    main()

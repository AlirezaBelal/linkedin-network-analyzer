from __future__ import annotations

import argparse
from contextlib import contextmanager
import os
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


@contextmanager
def _private_creation_permissions():
    # For this single-process CLI, avoid world-readable files on POSIX.
    # Existing files, folder parents, remote backups and Windows ACLs still
    # require independent owner review.
    old_mask = os.umask(0o077)
    try:
        yield
    finally:
        os.umask(old_mask)


def run_pipeline(input_file: str | Path, output_dir: str | Path, step: str = "all") -> None:
    if step not in STEPS:
        raise ValueError("Invalid pipeline step")
    input_path, output_path = Path(input_file), Path(output_dir)
    with _private_creation_permissions():
        output_path.mkdir(parents=True, exist_ok=True, mode=0o700)
        categorized_file = output_path / "all_connections_categorized.csv"
        actions_file = output_path / "final_linkedin_actions.xlsx"
        priority_file = output_path / "linkedin_priority.xlsx"

        # Always derive prerequisites from the requested source CSV. Reusing
        # intermediate files from a previous run silently analyzed stale people.
        clean_and_categorize.clean_and_categorize(input_path, output_path)
        if step in {"recommend", "report", "prioritize", "priority-report", "all"}:
            analyze_and_decide.analyze_and_decide(categorized_file, actions_file)
        if step in {"prioritize", "priority-report", "all"}:
            engagement_priority.add_priority_score(actions_file, priority_file)
        if step in {"report", "all"}:
            visualize_report.visualize_report(actions_file, output_path / "reports")
        if step in {"priority-report", "all"}:
            visualize_priority.visualize_priority(priority_file, output_path / "priority_reports")

    print(f"Completed '{step}' workflow. Outputs: {output_path}")


def main() -> None:
    args = build_parser().parse_args()
    run_pipeline(args.input, args.output_dir, args.step)


if __name__ == "__main__":
    main()

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def visualize_report(input_file: str | Path, output_dir: str | Path) -> str:
    """Generate category and recommendation reports from the review workbook."""
    dataframe = pd.read_excel(input_file)
    required = {"Category", "Action Recommendation"}
    missing = required.difference(dataframe.columns)
    if missing:
        raise ValueError(f"Recommendation workbook is missing columns: {sorted(missing)}")

    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(8, 6))
    dataframe["Category"].value_counts().plot.pie(autopct="%1.1f%%", startangle=140)
    plt.title("Distribution of LinkedIn Connections by Category")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig(destination / "category_distribution_pie.png")
    plt.close()

    plt.figure(figsize=(10, 6))
    dataframe["Action Recommendation"].value_counts().plot.bar()
    plt.title("Action Recommendations Count")
    plt.xlabel("Action Recommendation")
    plt.ylabel("Connections")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(destination / "action_recommendation_count.png")
    plt.close()

    cross_table = pd.crosstab(dataframe["Category"], dataframe["Action Recommendation"])
    axis = cross_table.plot.bar(figsize=(10, 6))
    axis.set_title("Category vs Action Recommendation")
    axis.set_xlabel("Category")
    axis.set_ylabel("Connections")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(destination / "category_vs_action.png")
    plt.close()

    print("Visualization & report completed")
    return str(destination)

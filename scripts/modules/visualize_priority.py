from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def visualize_priority(input_file: str | Path, output_dir: str | Path) -> str:
    """Generate visual reports for deterministic priority scores."""
    dataframe = pd.read_excel(input_file)
    required = {"Category", "Priority", "Priority Score"}
    missing = required.difference(dataframe.columns)
    if missing:
        raise ValueError(f"Priority workbook is missing columns: {sorted(missing)}")

    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(8, 6))
    dataframe["Priority"].value_counts().plot.pie(autopct="%1.1f%%", startangle=140)
    plt.title("LinkedIn Connections Priority Distribution")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig(destination / "priority_distribution_pie.png")
    plt.close()

    cross_table = pd.crosstab(dataframe["Category"], dataframe["Priority"])
    axis = cross_table.plot.bar(figsize=(10, 6))
    axis.set_title("Category vs Priority")
    axis.set_xlabel("Category")
    axis.set_ylabel("Connections")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(destination / "category_vs_priority.png")
    plt.close()

    groups = [
        group["Priority Score"].dropna().to_numpy()
        for _, group in dataframe.groupby("Category", sort=True)
    ]
    labels = [name for name, _ in dataframe.groupby("Category", sort=True)]
    plt.figure(figsize=(10, 6))
    plt.boxplot(groups, tick_labels=labels)
    plt.title("Priority Score Distribution by Category")
    plt.xlabel("Category")
    plt.ylabel("Priority Score")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(destination / "priority_score_boxplot.png")
    plt.close()

    print("Priority visualization completed")
    return str(destination)

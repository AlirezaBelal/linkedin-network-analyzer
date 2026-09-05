import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def visualize_priority(input_file, output_dir):
    """
    Generate visual reports for Engagement Score & Priority.
    """
    df = pd.read_excel(input_file)
    os.makedirs(output_dir, exist_ok=True)

    # Pie chart: Priority distribution
    plt.figure(figsize=(8, 6))
    df['Priority'].value_counts().plot.pie(autopct='%1.1f%%', startangle=140, shadow=True)
    plt.title('LinkedIn Connections Priority Distribution')
    plt.ylabel('')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'priority_distribution_pie.png'))
    plt.close()

    # Count plot: Priority vs Category
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x='Category', hue='Priority', order=df['Category'].unique())
    plt.title('Category vs Priority')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'category_vs_priority.png'))
    plt.close()

    # Scatter plot: Engagement Score by Category
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x='Category', y='Engagement Score')
    plt.title('Engagement Score Distribution by Category')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'engagement_score_boxplot.png'))
    plt.close()

    print("✅ Engagement & Priority Visualization Completed")
    return output_dir

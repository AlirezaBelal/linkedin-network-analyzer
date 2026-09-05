import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def visualize_report(input_file, output_dir):
    """
    Generate visual reports (pie chart, count plots) of connections and action recommendations.
    """
    df = pd.read_excel(input_file)
    os.makedirs(output_dir, exist_ok=True)

    # Pie chart - Category distribution
    plt.figure(figsize=(8, 6))
    df['Category'].value_counts().plot.pie(autopct='%1.1f%%', startangle=140, shadow=True)
    plt.title('Distribution of LinkedIn Connections by Category')
    plt.ylabel('')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'category_distribution_pie.png'))
    plt.close()

    # Count plot - Action Recommendation
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x='Action Recommendation', order=df['Action Recommendation'].value_counts().index)
    plt.title('Action Recommendations Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'action_recommendation_count.png'))
    plt.close()

    # Count plot - Category vs Action
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x='Category', hue='Action Recommendation')
    plt.title('Category vs Action Recommendation')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'category_vs_action.png'))
    plt.close()

    print("✅ Visualization & Report Completed")
    return output_dir

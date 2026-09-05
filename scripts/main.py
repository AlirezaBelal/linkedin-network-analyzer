import os

from scripts.modules import clean_and_categorize, analyze_and_decide, visualize_report
from scripts.modules import engagement_priority, visualize_priority

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "Connections.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

os.makedirs(OUTPUT_DIR, exist_ok=True)


def main():
    print("Welcome to LinkedIn Network Analyzer")
    print("Select the script to run:")
    print("1: Clean & Categorize Connections")
    print("2: Analyze & Decide Actions")
    print("3: Visualize & Generate Report")
    print("4: Run All Steps")
    print("5: Add Engagement Score & Priority")
    print("6: Visualize Engagement & Priority")

    choice = input("Enter your choice (1-6): ").strip()

    categorized_file = os.path.join(OUTPUT_DIR, "all_connections_categorized.csv")
    excel_file = os.path.join(OUTPUT_DIR, "final_linkedin_actions.xlsx")
    engagement_file = os.path.join(OUTPUT_DIR, "linkedin_engagement_priority.xlsx")
    priority_report_dir = os.path.join(OUTPUT_DIR, "priority_reports")

    if choice == "1":
        clean_and_categorize.clean_and_categorize(DATA_FILE, OUTPUT_DIR)
    elif choice == "2":
        analyze_and_decide.analyze_and_decide(categorized_file, excel_file)
    elif choice == "3":
        visualize_report.visualize_report(excel_file, os.path.join(OUTPUT_DIR, "reports"))
    elif choice == "4":
        clean_and_categorize.clean_and_categorize(DATA_FILE, OUTPUT_DIR)
        analyze_and_decide.analyze_and_decide(categorized_file, excel_file)
        visualize_report.visualize_report(excel_file, os.path.join(OUTPUT_DIR, "reports"))
    elif choice == "5":
        engagement_priority.add_engagement_score(excel_file, engagement_file)
    elif choice == "6":
        visualize_priority.visualize_priority(engagement_file, priority_report_dir)
    else:
        print("Invalid choice. Exiting.")


if __name__ == "__main__":
    main()

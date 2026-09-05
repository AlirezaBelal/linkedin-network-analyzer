# LinkedIn Network Analyzer

**A complete Python project to analyze your LinkedIn connections, categorize them, provide action recommendations, compute engagement scores, assign priority, and generate visual reports.**

---

## 📂 Project Structure

```

linkedin_network_analyzer/
│
├── data/
│   └── Connections.csv        # CSV file downloaded from LinkedIn
│
├── output/
│   └── (all generated outputs here)
│
├── scripts/
│   ├── main.py                # Main script to run the project
│   └── modules/
│       ├── clean_and_categorize.py
│       ├── analyze_and_decide.py
│       ├── visualize_report.py
│       ├── engagement_priority.py
│       └── visualize_priority.py
│
└── README.md

````

---

## 🛠 Installation

1. Clone the repository:

```bash
git clone <repository_url>
cd linkedin_network_analyzer
````

2. Install dependencies:

```bash
pip install pandas openpyxl matplotlib seaborn
```

---

## 📝 Usage

### Step 1: Download your LinkedIn connections CSV

1. Go to: [LinkedIn Data Download](https://www.linkedin.com/mypreferences/d/download-my-data)
2. Select **Connections** and request archive.
3. Save the CSV as `data/Connections.csv`.

---

### Step 2: Run the main script

```bash
python scripts/main.py
```

You will see the menu:

```
1: Clean & Categorize Connections
2: Analyze & Decide Actions
3: Visualize & Generate Report
4: Run All Steps
5: Add Engagement Score & Priority
6: Visualize Engagement & Priority
```

* **Option 1:** Categorizes connections by role and saves CSVs.
* **Option 2:** Adds action recommendations and saves Excel.
* **Option 3:** Generates charts for categories and action recommendations.
* **Option 4:** Runs steps 1–3 in sequence.
* **Option 5:** Adds Engagement Score & Priority to Excel file.
* **Option 6:** Generates visual reports for Engagement & Priority.

---

### Step 3: Outputs

* `output/all_connections_categorized.csv` → categorized CSV
* `output/final_linkedin_actions.xlsx` → with action recommendations
* `output/linkedin_engagement_priority.xlsx` → with engagement score & priority
* `output/reports/` → charts for categories & actions
* `output/priority_reports/` → charts for engagement & priority

---

## 📊 Visualization

* **Category distribution:** pie chart
* **Action recommendation count:** count plot
* **Category vs Action:** grouped count plot
* **Priority distribution:** pie chart
* **Category vs Priority:** grouped count plot
* **Engagement Score distribution:** box plot

---

## ⚡ Notes

* All scripts are written in English.
* You can run any step individually or all steps sequentially.
* Engagement Score is based on category and simulated activity.
* Priority: High / Medium / Low for actionable connections.

---

## 🎯 Goal

* Quickly understand your LinkedIn network.
* Identify valuable connections for collaboration, product work, or HR opportunities.
* Make data-driven decisions for engagement and follow/unfollow actions.

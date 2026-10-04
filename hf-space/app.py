from pathlib import Path
import tempfile

import gradio as gr
import pandas as pd
import spaces


# ZeroGPU requires at least one registered @spaces.GPU function during startup.
# This demo is CPU-only, so this no-op is intentionally never called.
@spaces.GPU(duration=10)
def _zerogpu_requirement():
    return None


CATEGORY_SCORE = {
    "Product": 5,
    "Developer": 4,
    "AI / Data": 4,
    "HR / Recruiter": 3,
    "Other": 1,
}

RECOMMENDATIONS = {
    "Product": "Prioritize outreach",
    "AI / Data": "Prioritize outreach",
    "Developer": "Explore collaboration",
    "HR / Recruiter": "Keep warm",
    "Other": "Review manually",
}

SAMPLE = pd.DataFrame([
    {
        "First Name": "Ava",
        "Last Name": "Example",
        "URL": "https://www.linkedin.com/in/example-product-lead/",
        "Company": "Example Labs",
        "Position": "Senior Product Manager",
    },
    {
        "First Name": "Noah",
        "Last Name": "Example",
        "URL": "https://www.linkedin.com/in/example-ml-engineer/",
        "Company": "Example AI",
        "Position": "Machine Learning Engineer",
    },
    {
        "First Name": "Mina",
        "Last Name": "Example",
        "URL": "https://www.linkedin.com/in/example-recruiter/",
        "Company": "Example Talent",
        "Position": "Technical Recruiter",
    },
    {
        "First Name": "Omid",
        "Last Name": "Example",
        "URL": "https://www.linkedin.com/in/example-software-engineer/",
        "Company": "Example Systems",
        "Position": "Backend Software Engineer",
    },
    {
        "First Name": "Sara",
        "Last Name": "Example",
        "URL": "https://www.linkedin.com/in/example-founder/",
        "Company": "Example Studio",
        "Position": "Founder",
    },
])


def categorize_title(title):
    if pd.isna(title):
        return "Other"

    normalized = str(title).strip().lower()
    if not normalized:
        return "Other"

    if any(
        keyword in normalized
        for keyword in ("hr", "recruiter", "talent", "people", "human resources")
    ):
        return "HR / Recruiter"

    if any(
        keyword in normalized
        for keyword in (
            "machine learning",
            "deep learning",
            "data scientist",
            "data analyst",
            "data engineer",
            "ai engineer",
            "ml engineer",
            "artificial intelligence",
        )
    ) or normalized.startswith(("ai ", "ml ", "data ")):
        return "AI / Data"

    if any(
        keyword in normalized
        for keyword in (
            "product manager",
            "head of product",
            "product owner",
            "product lead",
            "product",
        )
    ) or normalized == "pm":
        return "Product"

    if any(
        keyword in normalized
        for keyword in (
            "developer",
            "engineer",
            "cto",
            "backend",
            "frontend",
            "fullstack",
            "full stack",
            "software",
            "programmer",
        )
    ):
        return "Developer"

    return "Other"


def has_value(value):
    return not pd.isna(value) and bool(str(value).strip())


def compute_priority_score(row):
    category_points = CATEGORY_SCORE.get(str(row.get("Category", "Other")), 1)
    completeness_points = sum(
        1
        for field in ("Company", "Position", "URL")
        if field in row and has_value(row.get(field))
    )
    return int(category_points + completeness_points)


def assign_priority(score):
    if score >= 7:
        return "High"
    if score >= 5:
        return "Medium"
    return "Low"


def analyze(df):
    if df is None:
        raise gr.Error("Upload a CSV or use the synthetic example.")

    if isinstance(df, str):
        df = pd.read_csv(df, encoding="utf-8-sig")

    if "Position" not in df.columns:
        raise gr.Error('CSV must contain a "Position" column.')

    out = df.copy()
    out["Category"] = out["Position"].apply(categorize_title)
    out["Action Recommendation"] = out["Category"].map(RECOMMENDATIONS)
    out["Recommendation Basis"] = (
        "Role-title heuristic only; review context before taking account actions."
    )
    out["Priority Score"] = out.apply(compute_priority_score, axis=1)
    out["Priority"] = out["Priority Score"].apply(assign_priority)
    out["Priority Basis"] = (
        "Category relevance (1-5) + presence of Company/Position/URL (0-3)."
    )

    category_counts = out["Category"].value_counts().to_dict()
    priority_counts = out["Priority"].value_counts().to_dict()

    summary = f"""### Analysis summary

**Rows analyzed:** {len(out)}

**Categories**
- Product: {category_counts.get("Product", 0)}
- AI / Data: {category_counts.get("AI / Data", 0)}
- Developer: {category_counts.get("Developer", 0)}
- HR / Recruiter: {category_counts.get("HR / Recruiter", 0)}
- Other: {category_counts.get("Other", 0)}

**Priority**
- High: {priority_counts.get("High", 0)}
- Medium: {priority_counts.get("Medium", 0)}
- Low: {priority_counts.get("Low", 0)}

> Deterministic review heuristic only — not a behavioral or engagement score.
"""

    path = Path(tempfile.gettempdir()) / "linkedin_network_analysis.csv"
    out.to_csv(path, index=False, encoding="utf-8-sig")
    return out, summary, str(path)


with gr.Blocks(title="LinkedIn Network Analyzer") as demo:
    gr.Markdown(
        "# 🧭 LinkedIn Network Analyzer\n"
        "Privacy-aware, deterministic portfolio demo. No LinkedIn login and no account actions."
    )

    with gr.Row():
        upload = gr.File(label="Upload CSV", file_types=[".csv"], type="filepath")
        sample_btn = gr.Button("Load synthetic example", variant="secondary")

    preview = gr.Dataframe(
        headers=list(SAMPLE.columns),
        value=SAMPLE,
        interactive=True,
        label="Input preview",
        wrap=True,
    )

    run_btn = gr.Button("Analyze", variant="primary")

    output_columns = [
        "First Name",
        "Last Name",
        "URL",
        "Company",
        "Position",
        "Category",
        "Action Recommendation",
        "Recommendation Basis",
        "Priority Score",
        "Priority",
        "Priority Basis",
    ]
    output = gr.Dataframe(
        headers=output_columns,
        value=pd.DataFrame(columns=output_columns),
        label="Analysis output",
        interactive=False,
        wrap=True,
    )
    summary = gr.Markdown(
        "### Ready to analyze\n"
        "Upload a CSV or use the synthetic example, then select **Analyze**."
    )
    download = gr.DownloadButton(
        "Download analyzed CSV",
        value=None,
        variant="secondary",
    )

    sample_btn.click(lambda: SAMPLE, outputs=preview)

    def load_uploaded(path):
        if not path:
            return SAMPLE
        return pd.read_csv(path, encoding="utf-8-sig")

    upload.change(load_uploaded, inputs=upload, outputs=preview)
    run_btn.click(analyze, inputs=preview, outputs=[output, summary, download])


if __name__ == "__main__":
    demo.launch(ssr_mode=False)

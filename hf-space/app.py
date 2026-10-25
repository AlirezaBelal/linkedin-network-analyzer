"""Public, fictional, read-only illustration; never process uploaded contacts."""
import gradio as gr
import pandas as pd

SAMPLE = pd.DataFrame([
    {"First Name":"Ava","Last Name":"Example","Company":"Example Labs","Position":"Senior Product Manager","URL":"https://example.invalid/product"},
    {"First Name":"Noah","Last Name":"Example","Company":"Example AI","Position":"Machine Learning Engineer","URL":"https://example.invalid/ml"},
    {"First Name":"Mina","Last Name":"Example","Company":"Example Talent","Position":"Technical Recruiter","URL":"https://example.invalid/hr"},
    {"First Name":"Omid","Last Name":"Example","Company":"Example Systems","Position":"Backend Software Engineer","URL":"https://example.invalid/dev"},
    {"First Name":"Sara","Last Name":"Example","Company":"Example Studio","Position":"Founder","URL":"https://example.invalid/other"},
])
# Static example only. The separate local CLI is authoritative for real exports.
EXAMPLE_RESULTS = pd.DataFrame([
    {"Name":"Ava Example","Category":"Product","Recommendation":"Prioritize outreach","Priority Score":8,"Priority":"High"},
    {"Name":"Noah Example","Category":"AI / Data","Recommendation":"Prioritize outreach","Priority Score":7,"Priority":"High"},
    {"Name":"Mina Example","Category":"HR / Recruiter","Recommendation":"Keep warm","Priority Score":6,"Priority":"Medium"},
    {"Name":"Omid Example","Category":"Developer","Recommendation":"Explore collaboration","Priority Score":7,"Priority":"High"},
    {"Name":"Sara Example","Category":"Other","Recommendation":"Review manually","Priority Score":4,"Priority":"Low"},
])
with gr.Blocks(title="LinkedIn Network Analyzer — Synthetic Preview") as demo:
    gr.Markdown("# LinkedIn Network Analyzer — Synthetic Preview\n"
                "**No uploads, text entry, downloads, logins or account actions.** "
                "Only fictional data is displayed. Run the "
                "[local open-source CLI](https://github.com/AlirezaBelal/linkedin-network-analyzer) "
                "privately for real contact analysis.")
    gr.Dataframe(value=SAMPLE, interactive=False, label="Fictional input", wrap=True)
    gr.Dataframe(value=EXAMPLE_RESULTS, interactive=False,
                 label="Illustrative deterministic analysis", wrap=True)
    gr.Markdown("Role-title heuristics are not engagement metrics; review every recommendation.")
if __name__ == "__main__":
    demo.launch(ssr_mode=False)

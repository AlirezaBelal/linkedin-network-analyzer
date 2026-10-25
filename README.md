# LinkedIn Network Analyzer

[![CI](https://github.com/AlirezaBelal/linkedin-network-analyzer/actions/workflows/ci.yml/badge.svg)](https://github.com/AlirezaBelal/linkedin-network-analyzer/actions/workflows/ci.yml)

> A privacy-aware Python CLI for turning a LinkedIn connections export into a reviewable network map with role categories, explainable recommendations, deterministic priority scores, and visual reports.

This project addresses a practical network-management problem:

**How can a large LinkedIn network be converted from a flat contact export into a structured, reviewable dataset without pretending that a CSV export can reveal real engagement or make destructive account decisions automatically?**

## Product / data context

LinkedIn exports are useful raw data, but they are not a decision system. Titles are inconsistent, the export does not contain reliable engagement history, and a broad category such as `Other` is not evidence that a connection has low value.

The product goal is therefore to make network review more systematic while preserving:

**explainability · deterministic output · human review · data privacy**

The analyzer works only on a local CSV export. It does not require LinkedIn credentials, does not log in to LinkedIn, and does not perform follow/unfollow/removal actions.

## What the application does

```text
LinkedIn Connections.csv
        |
        v
input/header validation
        |
        v
role-title categorization
        |
        v
explainable action recommendation
        |
        v
deterministic priority score
        |
        +-------------------+
        |                   |
        v                   v
CSV / Excel outputs     visual reports
        |
        v
human review / optional downstream workflow
```

## Core capabilities

- **Bounded LinkedIn export ingestion** (20 MiB, 50,000 rows, 64 columns) with support for a short preamble before the CSV header and rejection of duplicate headers
- **Role-title categorization** into Product, Developer, AI / Data, HR / Recruiter, and Other
- **Explainable recommendations** that intentionally send uncertain records to manual review
- **Deterministic priority scoring** with no simulated/random activity values
- **Per-category CSV outputs** plus combined CSV and Excel review files
- **Visual reports** for category, recommendation, and priority distributions
- **Installable CLI command** for repeatable runs
- **Synthetic example data** for safe demonstration
- **Offline unit tests and GitHub Actions CI**
- **Privacy-focused repository defaults** that ignore real exports and generated outputs

## Decision semantics

The analyzer uses transparent heuristics, not behavioral truth.

### Role categories

Categories are inferred from the `Position` text using explicit keyword rules. These rules are intentionally simple and inspectable. They can produce false positives or miss unusual titles.

### Recommendations

Recommendations describe a review posture, not an automatic account action:

| Category | Recommendation |
|---|---|
| Product | Prioritize outreach |
| AI / Data | Prioritize outreach |
| Developer | Explore collaboration |
| HR / Recruiter | Keep warm |
| Other | Review manually |

`Other` is deliberately **not** mapped to automatic unfollow/removal.

### Priority score

The score is deterministic and auditable:

```text
priority score = category relevance (1-5) + profile completeness (0-3)
```

Profile completeness adds one point for each available field among `Company`, `Position`, and `URL`.

Priority bands:

- `High`: score >= 7
- `Medium`: score >= 5
- `Low`: score < 5

This is a portfolio-review heuristic. It is **not an engagement score** and does not claim to measure relationship strength, message history, content interaction, or business value.

## Complementary downstream workflow

For a separately scoped, safety-first workflow that can review a bounded list of profile URLs before connection removal, see **[linkedin-connection-remover](https://github.com/AlirezaBelal/linkedin-connection-remover)**.

```text
LinkedIn export
      |
      v
LinkedIn Network Analyzer
categorize · recommend · prioritize · report
      |
      v
human-reviewed shortlist
      |
      v
LinkedIn Connection Remover (optional, separate repository)
dry-run · explicit confirmation · bounded execution
```

The repositories are intentionally independent. This analyzer never invokes the remover.

## Input schema

The only required column is:

- `Position`

Typical LinkedIn exports also contain fields such as:

- `First Name`
- `Last Name`
- `URL`
- `Email Address`
- `Company`
- `Connected On`

A synthetic example is included at:

```text
examples/Connections.example.csv
```

Real LinkedIn exports should not be committed to the repository.

## Output contract

A full run writes to `output/` by default:

```text
output/
├── all_connections_categorized.csv
├── HR _ Recruiter.csv
├── Developer.csv
├── Product.csv
├── AI _ Data.csv
├── Other.csv
├── final_linkedin_actions.xlsx
├── linkedin_priority.xlsx
├── reports/
│   ├── category_distribution_pie.png
│   ├── action_recommendation_count.png
│   └── category_vs_action.png
└── priority_reports/
    ├── priority_distribution_pie.png
    ├── category_vs_priority.png
    └── priority_score_boxplot.png
```

The Excel outputs preserve the export columns and add analysis fields such as `Category`, `Action Recommendation`, `Priority Score`, and `Priority`. **Potential spreadsheet formulas in untrusted text are prefixed with an apostrophe in Excel exports**, so displayed text can differ from original CSV data. Raw CSV files are not formula-sanitized; import them as text when using spreadsheet software. Runs always recompute intermediate stages from the current input, rather than trusting stale outputs.

## Repository structure

```text
.
├── README.md
├── SECURITY.md
├── LICENSE
├── VERSION
├── CHANGELOG.md
├── pyproject.toml
├── requirements.txt
├── examples/
│   └── Connections.example.csv
├── scripts/
│   ├── __init__.py
│   ├── main.py
│   └── modules/
│       ├── __init__.py
│       ├── clean_and_categorize.py
│       ├── analyze_and_decide.py
│       ├── engagement_priority.py
│       ├── visualize_report.py
│       └── visualize_priority.py
├── tests/
│   └── test_analysis.py
└── .github/workflows/
    └── ci.yml
```

The unsafe historical browser-based connection-removal script is **removed from the current source tree**. It may remain in past Git revisions. This repository performs analysis only; use the independent `linkedin-connection-remover` project for any separately reviewed account-management workflow.

## Quick start

Requires **Python 3.10+**.

```bash
git clone https://github.com/AlirezaBelal/linkedin-network-analyzer.git
cd linkedin-network-analyzer
python -m venv .venv
```

Linux / macOS:

```bash
source .venv/bin/activate
```

Windows PowerShell:

```powershell
.venv\Scripts\activate
```

Install the project:

```bash
python -m pip install -e .
```

Run the safe synthetic example:

```bash
linkedin-network-analyzer \
  --input examples/Connections.example.csv \
  --output-dir demo-output \
  --step all
```

Or run your local export:

```bash
linkedin-network-analyzer \
  --input data/Connections.csv \
  --output-dir output \
  --step all
```

## CLI reference

```text
--input PATH
--output-dir PATH
--step {categorize,recommend,report,prioritize,priority-report,all}
```

`all` is the default and executes the full analysis pipeline in dependency order.

Individual stages can be useful while tuning rules:

```bash
linkedin-network-analyzer --input data/Connections.csv --step categorize
linkedin-network-analyzer --input data/Connections.csv --step recommend
linkedin-network-analyzer --input data/Connections.csv --step prioritize
```

## Public demo and deployment safeguards

The public Hugging Face Space source is now **Static HTML/CSS with fictional records only**: no CSV upload, editable contact table, JavaScript, Python backend, Gradio or generated download. Earlier versions accepted contact exports and used a shared temporary download path. These are removed from **source**, not necessarily the running hosted service. **A GitHub commit does not deploy a new Space, purge old caches/logs, or prove historical data deletion.** The operator must authorize and verify the replacement and review hosted SDK/hardware settings separately.

Hugging Face publication is **manual-only**, restricted to `master` and explicit owner approval. GitHub PRs and pushes cannot publish new hosted code. Do not upload real contacts to an unverified hosted service.

## Tests

Run locally:

```bash
python -m unittest discover -s tests -v
```

The test suite covers:

- role-title categorization
- safe recommendation semantics
- deterministic priority scoring
- missing-column validation
- LinkedIn-style CSV preamble detection

Tests are offline and never connect to LinkedIn.

## Continuous Integration

GitHub Actions runs on pushes and pull requests. CI checks the project across supported Python versions by running:

- editable package installation
- dependency consistency with `pip check`
- Python source compilation
- unit tests
- a full CLI smoke test against synthetic example data
- dependency vulnerability auditing

CI does not access LinkedIn, use credentials, or process real connection data.

## Data safety

LinkedIn exports contain personal data. The repository therefore ignores local `data/`, generated `output/`, CSV/Excel outputs, browser profiles, and common secret-file formats while explicitly allowing only the synthetic example dataset.

For real workflows:

- process files in a private directory; on POSIX the CLI uses a restrictive creation umask for new output, but cannot correct the permissions of existing files or remote sync/backup destinations
- reject files larger than 20 MiB, more than 50,000 rows, or more than 64 columns; very large, adversarial inputs are outside this CLI's supported scope

- do not commit LinkedIn exports or generated review files
- do not publish email addresses, profile URLs, or connection lists
- keep analysis outputs only as long as needed
- avoid pasting raw connection records into issues or bug reports
- treat recommendations as heuristics requiring human review

See [SECURITY.md](SECURITY.md) for data-handling and vulnerability-reporting guidance.

## Current scope and limitations

This repository is a focused local analysis tool. It does not claim to provide:

- real LinkedIn engagement metrics
- message or interaction history
- semantic/LLM title classification
- relationship-strength prediction
- automatic follow/unfollow/removal decisions
- direct LinkedIn API integration
- scraping, CAPTCHA solving, challenge bypass, or stealth automation
- a hosted dashboard or multi-user service

These are explicit product boundaries rather than missing claims hidden behind the README.

## Release

Current source release: **1.0.1** (security and data-processing hardening). Changes are documented in [CHANGELOG.md](CHANGELOG.md). This release tag describes repository source, **not** approval or verification of the deployed Hugging Face Space.

## License

Released under the [MIT License](LICENSE).

## Portfolio

For broader project context and other product/data work, see **[alirezabelal.github.io](https://alirezabelal.github.io/)**.

# Security and Data Handling

## Supported version

Security fixes are applied to the current productized baseline on the default branch.

## Reporting a vulnerability

Please report security issues privately rather than opening a public issue when the report could expose personal data, credentials, session artifacts, or an exploitable weakness.

Include only the minimum information needed to reproduce the issue. Do not attach a real LinkedIn export, browser profile, credential, cookie, token, or generated file containing connection data.

## Data sensitivity

A LinkedIn connections export can contain personally identifiable information, including names, email addresses, employers, job titles, profile URLs, and relationship metadata.

For real use:

- keep source exports outside version control
- keep generated CSV, Excel, and chart outputs private
- remove analysis artifacts when they are no longer needed
- do not paste real connection rows into public issues or logs
- use synthetic records when reporting bugs
- review local filesystem permissions and backup/sync behavior before processing sensitive exports

The repository `.gitignore` excludes common export/output paths and secret-file patterns, but ignore rules are not a substitute for operational care. The local CLI bounds CSV files to 20 MiB, 50,000 rows and 64 columns; it rejects duplicate headers. New outputs use a restrictive creation umask on POSIX, but previously existing files and synchronized folders require operator review. When writing Excel, formula-like contact fields are quoted to avoid creating executable spreadsheet formulas; raw CSV must be imported as text.

## Application boundary

The supported LinkedIn Network Analyzer workflow is local data analysis only. It does not require LinkedIn credentials and does not log in to LinkedIn.

The historical destructive connection-removal script was removed from the active tree; old Git revisions may still contain it. The supported code performs analysis only.

An older Space revision allowed CSV uploads and wrote all download outputs to a shared temporary path. The reviewed replacement is a static HTML/CSS preview with no user input, processing, user download, Gradio or image/Pillow dependency. The owner-approved static publication succeeded on 2026-10-25; the current remote tree and static SDK were rechecked on 2026-10-26. **This does not certify deletion of historical uploads, caches, logs, backups or revisions.** Future hosted publications still require separate, explicit owner approval.

## Dependency security

GitHub Actions installs the package, checks dependency consistency, runs offline tests, executes a synthetic smoke test, and audits CLI runtime dependencies. The public static preview has **no Python dependency set to audit**. A previously tested Gradio 6 stack pulled Pillow 12.3.0, which failed dependency auditing with advisories fixed in Pillow 13; removing this unnecessary dynamic stack is intentional, not an audit suppression. Passing checks do not certify the live Hugging Face instance or purge historical files.

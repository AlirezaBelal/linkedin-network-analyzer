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

The repository `.gitignore` excludes common export/output paths and secret-file patterns, but ignore rules are not a substitute for operational care.

## Application boundary

The supported LinkedIn Network Analyzer workflow is local data analysis only. It does not require LinkedIn credentials and does not log in to LinkedIn.

A historical browser-automation file remains in the repository for provenance and is outside the supported analyzer workflow. For maintained connection-removal behavior, use the separate `linkedin-connection-remover` repository and review its safeguards before any live action.

## Dependency security

GitHub Actions installs the package, checks dependency consistency, runs offline tests, executes a synthetic smoke test, and audits runtime dependencies for known vulnerabilities.

# Changelog

## 1.0.1 - 2026-10-25

### Security and correctness

- Replace uploaded-contact public Space functionality with synthetic-only, read-only preview source; publication now requires explicit owner approval on `master` (running hosted instance not yet verified).
- Remove obsolete runnable connection-removal script from current tree; old Git history is unchanged.
- Bound private local CSV input to 20 MiB, 50,000 rows and 64 columns; reject empty exports and duplicate headers.
- Recompute analysis prerequisites from the supplied CSV to avoid reusing stale results; protect Excel exports from formula injection and restrict newly created POSIX files.
- Add synthetic regression, full visualization smoke and hosted-data policy tests, with measured 92% Python source coverage on the reviewed baseline.
- Replace the unnecessary Gradio/Pillow dependency tree with static HTML/CSS after the independent demo audit exposed vulnerabilities; no security audit was suppressed. Update Actions to Node 24 capable versions.


All notable changes to the productized public baseline are documented here.

## 1.0.0 - 2026-09-05

### Added

- installable `linkedin-network-analyzer` CLI
- synthetic LinkedIn connections example dataset
- offline unit tests
- GitHub Actions test matrix and dependency audit
- `SECURITY.md`, `LICENSE`, and explicit version tracking
- product/data context, output contract, limitations, and portfolio links in the README

### Changed

- converted the interactive menu into a repeatable command-line workflow
- made CSV ingestion tolerant of a short LinkedIn-style preamble before the header
- replaced automatic `Other -> Unfollow / Remove` behavior with `Review manually`
- replaced simulated/random activity scoring with deterministic priority scoring
- renamed priority visualization semantics so the project no longer claims to measure real engagement
- clarified that browser-based connection removal is a separate downstream product boundary

### Data and safety

- real exports and generated analysis artifacts remain excluded from version control
- only synthetic example data is intentionally tracked
- tests and CI do not connect to LinkedIn

# Changelog

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

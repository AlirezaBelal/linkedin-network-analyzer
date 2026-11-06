# Network Atlas 1.1 release review

## Initial audit
The 1.0.1 CLI already supplied bounded local CSV processing, human-review recommendations, deterministic scoring, two Excel workbooks and six reports. Pages exposed five fictional records only. PRs 4–6 deliberately removed shared hosted contact processing and destructive account automation; PRs 7–9 added an independently constrained static Pages explorer. This release preserves those historical Hugging Face decisions.

Confirmed defects: substring rules matched Director (cto) and Production (product); pandas ingestion could silently reinterpret ragged rows; literal NA/NULL disappeared in later stages; reruns left obsolete category CSVs; output destinations could follow symlinks; the Matplotlib minimum predated the existing tick_labels API.

## Browser-local file security decision
Accept only an explicit, user-authorized selection. No upload endpoint exists. CSP blocks connections; no remote runtime assets, telemetry, persistent storage, profile links, credentials, or account actions exist. Render text via textContent. Replace state only after complete validation; clear restores a separate fictional sample. Never log raw input or put search/contact data in the URL.

Limits: 2 MiB, 2,000 rows, 32 columns, 2,048 characters per field. Pagination renders at most twenty rows. Fatal UTF-8 decoding and bounded strict parsing reject malformed files without echoing content. Browser CSV is a fixed, formula-quoted nine-column review schema, omitting email, profile URL and extra columns. It is not the full Python output set. LF normalization and stricter unquoted-quote rejection are intentional browser ingestion differences.

Local Node upper-bound testing processed a near-2-MiB 2,000-row synthetic fixture in approximately 150 ms, below a 5-second / 100-MiB heap-growth guard. Real Chromium QA repeats file-picker processing and downloads at seven sizes, records elapsed time and coarse browser heap estimates, and applies a 10-second interaction budget. These are regression budgets, not universal device-performance guarantees.

Reset/leave discards app references and DOM records. No forensic memory erasure or removal of original files/downloads/backups/extensions is claimed. A compromised host, browser extension, device or browser remains outside this static app's assurance. No contact content belongs in issues, screenshots or public artifacts.

## Design skills applied
Pinned design and web-ui-audit skills at 5e85045d96662605f33e12150cdc6d00cb04dc0a remain unchanged. Design used the brand and product registers, restrained typesetting and hardening: a navy instrument-like hero, original role-group SVG, native system typography, compact light review workspace, consistent 44px controls, text/count-backed meters, semantic table and native disclosures. This avoids implying a relationship graph or behavioral measurements.

Implementation findings addressed: oversized hero (72px) reduced to 34–54px; input outline suppression replaced with visible focus; count-only chips replaced with labeled distributions; empty-state recovery and file-error focus added; tables scroll within a labeled keyboard region; results paginate; raw strings use text nodes; no animation is required. Private search/filter state deliberately stays out of URLs.

## Verification contract
Python tests cover original CLI reports and protections plus CSV, stale-file, overlap/symlink and NA/NULL regressions. A 288-case synthetic Python/JavaScript parity suite checks categories, scoring, priority and recommendations. Node tests cover rules, quotes, malformed/oversized input, prototype keys, CSV safety and runtime privacy.

The browser workflow checks 320, 375, 390, 768, 1024, 1440 and 1920px; uses genuine file-chooser and download events with fictional CSVs; tests malformed files, injection text, clear/reset, filters and pagination; scans sample/imported states with axe; checks assets, overflow, keyboard focus, empty states, browser errors, storage and unexpected network requests. Master-only verification waits for the exact published static release, then repeats the matrix. Artifacts contain only synthetic data.

CI retains Python 3.10–3.14, package installation, installed CLI smoke, all six charts, coverage, dependency auditing and historical hosted-demo tests. No Hugging Face source/workflow changes or publication are included.


Formula-like CLI Excel column headers are quoted as text as of 1.1.1, alongside cell values. If quoting would produce duplicate headers, workbook creation rejects the ambiguity; rename those source columns and rerun. Standard schemas and raw CLI CSV values/headers are unchanged.

JavaScript title/completeness normalization explicitly follows Python Unicode whitespace, including NEL and control separators; BOM inside a field remains a present value. The 288-case fixture cross-check includes these boundaries. File-level UTF-8 BOM handling remains separate.

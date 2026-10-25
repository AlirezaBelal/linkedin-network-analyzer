---
title: LinkedIn Network Analyzer — Synthetic Preview
emoji: 🧭
colorFrom: blue
colorTo: indigo
sdk: static
app_file: index.html
pinned: false
license: mit
---

# LinkedIn Network Analyzer — Synthetic Preview

This **static HTML/CSS-only** Space shows five fictional LinkedIn-style contact
records and deterministic category/recommendation/priority illustrations.
It offers **no file uploads, forms, text input, user-generated downloads,
JavaScript, Gradio, Pillow, Python backend or external asset requests**.

No actual LinkedIn account is accessed. Its numbers and human review labels
are illustration-only, not relationship-quality or engagement measurements.
For real exports, use the [private local CLI](https://github.com/AlirezaBelal/linkedin-network-analyzer)
without sharing personal contacts with public hosted services.

## Publishing boundary

The GitHub sync workflow is **manual only**, restricted to the approved
`master` revision and explicit owner confirmation. Before authorizing
publication, review the currently hosted Space and its hardware/SDK settings,
and ensure the static runtime is supported. Its exact old root-level
`app.py` and `requirements.txt` are deleted by the approved upload command;
no unrelated files or old Git revisions are intentionally removed.

This source change does not itself update the hosted service. Deleting files
from the current tree **does not certify removal from historical revisions,
caches, logs, backups or the prior Gradio execution environment**.

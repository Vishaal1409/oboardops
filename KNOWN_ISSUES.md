# Known Issues — OnboardOps

Tracking minor issues found during testing. None of these are blocking — just things to be aware of or polish if time allows before Sep 14.

## 1. HR Q&A tool can match vague questions to overly specific policies

**Found:** Sep 5, 2026 (edge-case testing)

**Details:** Asking a vague question like "tell them about our leave policy" matched to the paternity leave entry instead of the more commonly relevant 21-day annual paid leave policy. Caused by fuzzy text-matching (SequenceMatcher) finding the closest wording match rather than the most contextually relevant one.

**Owner:** Ishitha

**Priority:** Low — not blocking, nice-to-fix if time allows

**Possible fix:** Weight matches toward higher-priority/more common policies when the question is vague, or add default keywords that route generic "leave policy" questions to the main entry.

## 2. Class-based tools need a wrapper for Strands

**Found:** Aug 30, 2026 (integration testing)

**Details:** Strands requires plain `@tool`-decorated functions, not classes. Ishitha's original HR Q&A tool (`HRQATool`) was a class, so a wrapper (`tools/hr_qa_wrapper.py`) was created to expose it as a simple function.

**Status:** Resolved — pattern documented here in case any future tool runs into the same issue.

## 3. Checklist items are unsuitable as tracker Task values verbatim

**Found:** Sep 6, 2026 (checklist→tracker format-compatibility testing, `e2e/test_checklist_tracker_bridge.py`)

**Details:** `generate_checklist()` items are long, punctuation-heavy, LLM-generated sentences (100–362 characters observed in live testing) — grounded in the Indian HR compliance skill, so they legitimately need that detail for a human-readable checklist. But `tracker_tool.py`'s `update_task_status()`/`_update_task_status_in_sheet()` match a task by **exact** (case-insensitive) string equality with no task-ID concept, and there's no length cap on `log_status()`'s `task` argument. Logging a raw checklist item verbatim as a Task cell is both a poor spreadsheet fit and, because `generate_checklist()` is non-deterministic across calls, impossible to reliably reference again later (a regenerated checklist won't reproduce the exact same sentence).

**Owner:** Arun (checklist tool) / Ishitha (tracker tool) — touches both

**Priority:** Low — not blocking; a real fix (task IDs) is a shared-Sheet schema change, out of scope before Sep 14

**Fix applied today:** `tools/checklist_tool.py` gained two pure-Python helpers — `parse_checklist_items()` and `short_task_label()` — that derive a short (≤60 char), deterministic label per checklist item without an extra LLM call. `tools/tracker_tool.py`'s `log_status`/`update_task_status` docstrings now explicitly tell the agent to use a short label, not a full sentence. This does **not** solve the deeper non-determinism/no-task-ID limitation — that's still open, and is why `short_task_label()` output from one generation can't be used to update a task logged from a later regeneration of "the same" checklist.

**Possible future fix:** Add a `Task ID` column to the tracker sheet and switch lookups to ID-based instead of exact-text matching.

## 4. Live Google Sheets verification is machine-specific

**Found:** Sep 6, 2026

**Details:** `credentials.json` has never been committed to the repo (correctly gitignored — it's a service-account secret) and isn't present on every contributor's machine. `e2e/test_checklist_tracker_bridge.py` and `e2e/test_agent_full_integration.py` verify the checklist→tracker format fix against a **mocked** Google Sheet, which is sufficient to confirm the format/shape issue and fix, but not a live write/read against the real shared sheet.

**Owner:** Whoever has `credentials.json` locally (Ishitha has verified live tracker functions separately in `test_tracker_functions.py`)

**Priority:** Low — mocked verification covers the actual bug found; live confirmation is a nice-to-have, not blocking

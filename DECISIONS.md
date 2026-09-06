# Decisions Log

Notable engineering decisions made during this project, and why — kept here
so the reasoning isn't lost once the working context that produced it is gone.

---

## 2026-09-03 — Merged team's `tools/` restructure into the checklist tool work

One important thing that happened along the way: while I was working, your team pushed 9 commits restructuring the repo (`tools/` directory, `agent.py`, other tools). Their `tools/checklist_tool.py` had a placeholder stub — `# TODO: Arun implements this` — which is the actual file the rest of the codebase expects, not the root-level `checklist_tool.py` I'd built earlier. I merged their history in, then moved my implementation into that file and adapted it to match: function renamed `generate_checklist`, returns a plain string (not a Pydantic object) to match `tracker_tool.py`/`hr_qa_tool.py` convention, path resolution uses their `PROJECT_ROOT` pattern, and I added `test_checklist.py` at root matching their `test_scheduling.py`/`test_hr_qa.py` script style. `requirements.txt` now includes `pydantic` (used internally for output validation).

---

## 2026-09-06 — Fixed checklist→tracker format mismatch with string truncation, not a task-ID schema change

Testing `generate_checklist()` output against `tracker_tool.py` for the first time (nobody had — the existing integration tests hardcoded a short literal task string instead of using real checklist output) surfaced a real problem: checklist items are 100–362 character LLM-generated sentences, while the tracker's `update_task_status()` requires **exact** (case-insensitive) string matching with no task-ID concept.

**Why not fix this properly with task IDs**: that would mean adding a `Task ID` column to the live shared Google Sheet, changing every lookup in `tracker_tool.py` to be ID-based, and migrating already-logged rows — a shared-schema change touching a spreadsheet other people are actively using, eight days before the Sep 14 deadline. Too large and too risky for what this actually needs today.

**What I did instead**: added two pure-Python, no-LLM-call helpers to `tools/checklist_tool.py` — `parse_checklist_items()` (splits a checklist's Markdown into raw item strings) and `short_task_label()` (derives a short, deterministic label per item by cutting at the first clause-boundary separator, or hard-truncating at a word boundary). Neither is exposed as an `@tool` — the actual bridging decision belongs to the agent when it calls `log_status`, so the fix that reaches that decision is a **docstring change** on `log_status`/`update_task_status` in `tools/tracker_tool.py`, telling the agent to pass a short label instead of a full sentence. `generate_checklist()`'s own return type and contract are untouched.

**What this does not fix**: `generate_checklist()` is non-deterministic across calls, so a label derived from one generation still can't be used to reliably `update_task_status()` against a later regeneration of "the same" checklist. That's a real, pre-existing limitation of the tracker's exact-match design, not something string truncation can solve — documented in `KNOWN_ISSUES.md` #3 as still open, deliberately not disguised as fixed.

**Verification**: `e2e/test_checklist_tracker_bridge.py` — two live `generate_checklist()` calls confirmed items regularly exceed 80 characters (up to 362 observed), `short_task_label()` produced valid ≤61-char labels for all of them, and a mocked `log_status()` call showed the label — not the raw sentence — landing in the tracker's Task cell. `e2e/test_agent_full_integration.py` confirmed the full 7-tool agent still behaves correctly end-to-end (checklist+HR+schedule+log in one turn, unusual role/department combos, blank-department handling, and MD role disambiguation) after these changes.

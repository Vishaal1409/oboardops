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

---

## 2026-09-10 — Added a 60s client-side timeout around `generate_checklist`'s Bedrock call

A team dry-run of the demo flow (playing "the new hire" through a real multi-turn conversation with the full agent) went cleanly, but it's the kind of live-in-front-of-an-audience moment where the previously-observed 195s outlier (from the 50-case stress test, `FEATURES.md` gap #5) would be genuinely bad — several minutes of dead silence mid-demo, with no feedback that anything is even happening.

**Why 60s**: the observed latency range across dozens of live calls is ~10-25s median, with the one outlier at 195s. 60s comfortably covers normal variance without falsely killing a legitimately-slow-but-successful call very often, while still failing in well under a minute with a clean message instead of leaving the room waiting. This is a judgment call, not a measured optimum — there wasn't time to gather enough outlier samples to fit a real distribution before Sep 14.

**Implementation**: wraps the existing `agent(prompt, structured_output_model=...)` call in a `ThreadPoolExecutor(max_workers=1)` and calls `future.result(timeout=60)`. On `TimeoutError`, returns `"Error: checklist generation timed out after 60s. ..."` — consistent with the tool's existing `"Error: ..."`/`"Unexpected error: ..."` string convention, not a raised exception.

**Important limitation, deliberately accepted**: this bounds how long the *caller* waits — it does not cancel the underlying Bedrock call. Neither `boto3`/Bedrock nor Strands' synchronous `Agent.__call__` expose real mid-flight cancellation, so the orphaned call keeps running in its background thread until it eventually finishes (its result is just discarded) or the process exits. A first attempt at this used `with ThreadPoolExecutor(...)`, which is wrong: `__exit__` calls `shutdown(wait=True)`, which would block the caller until the orphaned call actually finishes anyway — silently defeating the entire timeout. Fixed by managing the executor manually and calling `shutdown(wait=False)` in a `finally` block instead. Caught this by writing a test that mocks a 5s-sleeping agent under a 1s timeout and asserting the function actually returns in ~1s, not ~5s — worth being suspicious of any timeout implementation that hasn't been proven to return promptly, since the naive version *looks* correct and only fails under real latency.

**Verification**: `test_checklist.py` and `e2e/test_checklist_tracker_bridge.py` re-run clean (no regression on normal-latency calls, which stay well under 60s); a scratch test with a mocked 5s-sleeping agent under a 1s timeout confirmed the function returns in ~1s with the expected error string, not after the full simulated delay.

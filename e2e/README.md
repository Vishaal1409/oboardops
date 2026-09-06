# OnboardOps — End-to-End Test Suite

How to verify the whole system, in order, and what to expect from each step. Individual tools have their own unit tests at the project root (owned by whoever built that tool); this folder holds the **cross-tool** checks — does output from one tool actually work as input to another, and does the full agent (not just standalone functions) behave sanely on realistic and edge-case prompts.

## Prerequisites

| Requirement | Needed for |
|---|---|
| AWS credentials with Bedrock access to `us.anthropic.claude-sonnet-4-6` | Every test that calls `generate_checklist()` or the full agent (they all do, live) |
| `credentials.json` (Google service account — see [`SETUP_GOOGLE_SHEETS.md`](../SETUP_GOOGLE_SHEETS.md)) | Only `test_tracker_functions.py` and `test_tracker_integration.py`. Everything else — including both tests in this folder — mocks the Google Sheet, so it runs without this file. |

Run everything from the **project root**, not from inside `e2e/`.

## Run sequence

### 1. Per-tool checks (no live Google credentials needed)

```bash
python test_checklist.py       # generate_checklist: 3 roles + edge cases (blank/unusual input)
python test_hr_qa.py            # HR Q&A: direct-phrasing questions
python test_hr_qa_stress.py     # HR Q&A: paraphrased/casual questions
python test_scheduling.py       # generate_schedule: 5 start dates incl. weekend rollover
python test_tracker.py          # tracker: all 4 functions, mocked Google Sheet
```

### 2. Live-credential tracker checks (skip these if you don't have `credentials.json`)

```bash
python test_tracker_functions.py     # get_employee_tasks / update_task_status / get_all_tasks, live sheet
python test_tracker_integration.py   # simulated multi-tool -> tracker logging, live sheet
```

### 3. Cross-tool end-to-end (this folder)

```bash
python e2e/test_checklist_tracker_bridge.py   # does checklist output feed cleanly into the tracker?
python e2e/test_agent_full_integration.py     # unusual/edge-case prompts through the FULL agent
```

Run the bridge test before the full-agent test — it isolates the checklist→tracker question with 2 live calls, before the agent test spends several more live calls exercising the full tool-calling loop.

## What each e2e test actually checks

### `test_checklist_tracker_bridge.py`

Calls the **real** `generate_checklist()` (live Bedrock, 2 calls total), parses out individual items, and feeds them through a **mocked** `log_status()` to inspect exactly what would land in the Task column. Confirms:
- Real checklist items are often >80 characters, full sentences with commas/parentheses/₹ symbols — fine for a human-readable checklist, a poor fit as a spreadsheet Task label verbatim.
- `short_task_label()` (in `tools/checklist_tool.py`) derives a short (≤61 char), non-empty label per item, and that label — not the raw sentence — is what gets written to the mocked sheet's Task cell.
- A second live generation call demonstrates that `generate_checklist()` is non-deterministic — proving why a label from one generation can't be used later to `update_task_status()` against a regenerated checklist. This is a documented tracker limitation (exact-string task matching, no task IDs — see [`KNOWN_ISSUES.md`](../KNOWN_ISSUES.md)), not something this test or the label helper fixes.

### `test_agent_full_integration.py`

Builds the same 7-tool `Agent` as `agent.py` (doesn't import `agent.py` directly, since that module fires a live call on import) against a mocked Google Sheet, and runs 4 scenarios:

- **A** — the original compound scenario (checklist + leave-days question + schedule + log a task) that used to be `agent.py`'s embedded test before the tracker query tools were wired in. Prints whatever Task-cell text the agent actually chose to write, so you can see whether the `log_status`/`update_task_status` docstring guidance (added alongside `short_task_label()`) is enough to get the agent to log a short label instead of a full sentence.
- **B** — "Intern, Legal": an unusual role/department combo, through the full agent, not the standalone function.
- **C** — a blank/unspecified department. **Observational, not pass/fail** — the agent might ask a clarifying question, surface the tool's `"Error: ..."` message, or guess a department; all three are acceptable, only an unhandled exception is a hard failure. The classification is printed for manual review.
- **D** — "MD, Healthcare": re-confirms the role-disambiguation behavior (Managing Director vs. Medical Doctor) already verified at the standalone-function level, this time through the agent's tool-calling loop.

## Runtime expectations

Both tests here make multiple live Bedrock calls (checklist generation, and — for the agent test — however many tool-calling turns the LLM decides it needs per scenario). Expect several minutes total, and occasional single-call latency spikes (one call in prior standalone stress testing took ~195s under concurrent load — these tests run sequentially, so that specific risk is lower, but budget for it).

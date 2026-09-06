"""
Full-agent integration test - unusual role/department combos and the
reconstructed compound scenario, run through the actual Strands Agent
(tool-calling loop), not standalone tool functions.

Does NOT `import agent` directly - agent.py runs a live call at import time
as a side effect. Instead builds its own Agent here mirroring agent.py's
current 7-tool wiring, against a mocked Google Sheet.

Run from project root: python e2e/test_agent_full_integration.py
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from strands import Agent  # noqa: E402

from tools.checklist_tool import generate_checklist  # noqa: E402
from tools.hr_qa_wrapper import answer_hr_question  # noqa: E402
from tools.scheduling_tool import generate_schedule  # noqa: E402
from tools.tracker_tool import (  # noqa: E402
    HEADERS,
    get_all_tasks,
    get_employee_tasks,
    log_status,
    reset_sheet_client,
    update_task_status,
)

TASK_COLUMN_INDEX = HEADERS.index("Task")


def _print_section(title: str) -> None:
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def _build_agent() -> Agent:
    """Mirrors agent.py's current tool wiring exactly."""
    return Agent(
        tools=[
            answer_hr_question,
            generate_checklist,
            generate_schedule,
            log_status,
            get_employee_tasks,
            update_task_status,
            get_all_tasks,
        ]
    )


def _mocked_sheet():
    mock_worksheet = MagicMock()
    mock_worksheet.row_values.return_value = HEADERS
    mock_worksheet.get_all_records.return_value = []
    mock_sheet = MagicMock()
    mock_sheet.worksheet.return_value = mock_worksheet
    mock_client = MagicMock()
    mock_client.open_by_key.return_value = mock_sheet
    return mock_worksheet, mock_client


def _logged_task_cells(mock_worksheet) -> list[str]:
    cells = []
    for call in mock_worksheet.append_row.call_args_list:
        row = call[0][0]
        if len(row) > TASK_COLUMN_INDEX:
            cells.append(row[TASK_COLUMN_INDEX])
    return cells


def scenario_a_compound(agent: Agent, mock_worksheet) -> bool:
    """Reconstructed commit 2884804 compound scenario: checklist + leave Q&A +
    schedule + log a task, in one turn, through the full agent."""
    _print_section("Scenario A - Reconstructed compound scenario (checklist+HR+schedule+log)")
    prompt = (
        "A new hire named Rajesh Kumar is joining as a Software Engineer in Engineering, "
        "starting 2026-09-08. Please generate his onboarding checklist, tell him how many "
        "paid leave days he gets, create his first-week schedule, and log that his "
        "'Laptop provisioned' task is In Progress, owned by IT."
    )
    print(f"Prompt: {prompt}\n")
    response = agent(prompt)
    print(f"\nAgent response:\n{response}")

    non_empty = len(str(response).strip()) > 0
    logged = mock_worksheet.append_row.called
    task_cells = _logged_task_cells(mock_worksheet)

    print(f"\nNon-empty response: {non_empty}")
    print(f"log_status invoked: {logged}")
    print(f"Task cell(s) written: {task_cells}")
    for cell in task_cells:
        flag = "WARN: long/sentence-like" if len(cell) > 80 else "OK: short label"
        print(f"  -> {flag} ({len(cell)} chars): {cell!r}")

    ok = non_empty and logged
    print(f"\nResult: {'PASS' if ok else 'FAIL'}")
    return ok


def scenario_b_intern_legal(agent: Agent) -> bool:
    _print_section('Scenario B - "Intern, Legal"')
    prompt = (
        "Generate an onboarding checklist for a new Legal Intern joining the Legal "
        "department, and log that their 'NDA signed' task is Completed, owned by Legal."
    )
    print(f"Prompt: {prompt}\n")
    try:
        response = agent(prompt)
        print(f"\nAgent response:\n{response}")
        ok = len(str(response).strip()) > 0
        print(f"\nResult: {'PASS' if ok else 'FAIL'} (non-empty response, no exception)")
        return ok
    except Exception as exc:
        print(f"\nUnhandled exception: {type(exc).__name__}: {exc}")
        print("Result: FAIL")
        return False


def scenario_c_blank_department(agent: Agent) -> str:
    """Observational, not pass/fail on content - only hard-fails on an unhandled
    exception. Classifies the agent's behavior for manual/judge review."""
    _print_section("Scenario C - Blank/unspecified department (observational)")
    prompt = "Generate an onboarding checklist for a new Software Engineer. I don't know the department yet."
    print(f"Prompt: {prompt}\n")
    try:
        response = agent(prompt)
        text = str(response)
        print(f"\nAgent response:\n{text}")

        if text.strip().endswith("?"):
            classification = "asked a clarifying question"
        elif "error" in text.lower() or "required" in text.lower():
            classification = "surfaced the tool's validation error"
        else:
            classification = "guessed/assumed a department"

        print(f"\nClassification: {classification}")
        print("Result: PASS (no unhandled exception - see classification above)")
        return classification
    except Exception as exc:
        print(f"\nUnhandled exception: {type(exc).__name__}: {exc}")
        print("Result: FAIL")
        return "EXCEPTION"


def scenario_d_md_healthcare(agent: Agent) -> bool:
    """Time-permitting: confirm role disambiguation (verified standalone in the
    earlier 50-case stress test) still holds through the agent's tool-calling loop."""
    _print_section('Scenario D - "MD, Healthcare" (role disambiguation, agent-mediated)')
    prompt = "Generate an onboarding checklist for our new MD in the Healthcare department."
    print(f"Prompt: {prompt}\n")
    try:
        response = agent(prompt)
        text = str(response)
        print(f"\nAgent response:\n{text}")
        # Soft check: healthcare-appropriate disambiguation should mention clinical/medical
        # terms rather than board/governance terms.
        medical_signal = any(
            kw in text.lower() for kw in ("clinical", "medical", "patient", "ehr", "credential")
        )
        print(f"\nMedical-context signal present: {medical_signal}")
        ok = len(text.strip()) > 0
        print(f"Result: {'PASS' if ok else 'FAIL'} (non-empty response, no exception)")
        return ok
    except Exception as exc:
        print(f"\nUnhandled exception: {type(exc).__name__}: {exc}")
        print("Result: FAIL")
        return False


def main() -> int:
    print("\n" + "=" * 70)
    print("Full-Agent Integration Test (7-tool agent, mocked Google Sheet)")
    print("=" * 70)

    mock_worksheet, mock_client = _mocked_sheet()
    with patch("tools.tracker_tool.gspread.authorize", return_value=mock_client), patch(
        "tools.tracker_tool.Credentials.from_service_account_file", return_value=MagicMock()
    ), patch("tools.tracker_tool.DEFAULT_CREDENTIALS_PATH", Path("/tmp/fake-credentials.json")), patch(
        "pathlib.Path.exists", return_value=True
    ):
        reset_sheet_client()
        agent = _build_agent()

        results: dict[str, object] = {}
        results["A"] = scenario_a_compound(agent, mock_worksheet)
        results["B"] = scenario_b_intern_legal(agent)
        results["C"] = scenario_c_blank_department(agent)
        results["D"] = scenario_d_md_healthcare(agent)

    _print_section("Summary")
    hard_fail = False
    for name, result in results.items():
        if name == "C":
            print(f"  Scenario {name}: INFO - {result}")
            if result == "EXCEPTION":
                hard_fail = True
        else:
            print(f"  Scenario {name}: {'PASS' if result else 'FAIL'}")
            if not result:
                hard_fail = True

    print(f"\nOverall: {'FAIL (unhandled exception occurred)' if hard_fail else 'PASS'}")
    return 1 if hard_fail else 0


if __name__ == "__main__":
    sys.exit(main())

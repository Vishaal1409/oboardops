"""
Tracker integration test — simulates other OnboardOps tools feeding the tracker.

Run from project root:
    python test_tracker_integration.py
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tools.tracker_tool import (  # noqa: E402
    get_employee_tasks,
    log_status,
    reset_sheet_client,
)

EMPLOYEE = "Rajesh Kumar"
ROLE = "Software Engineer"


def simulate_checklist_tool(employee: str, role: str) -> dict[str, str]:
    """Simulate generate_checklist() output for a Software Engineer."""
    return {
        "employee": employee,
        "role": role,
        "task": "Laptop provisioning",
        "status": "In Progress",
        "owner": "IT",
        "source": "checklist_tool",
    }


def simulate_scheduling_tool(employee: str, role: str) -> dict[str, str]:
    """Simulate generate_schedule() output for first-week meetings."""
    return {
        "employee": employee,
        "role": role,
        "task": "First week meeting scheduled Monday 10am",
        "status": "Completed",
        "owner": "HR",
        "source": "scheduling_tool",
    }


def simulate_it_tool(employee: str, role: str) -> dict[str, str]:
    """Simulate IT setup tool output after granting Bedrock access."""
    return {
        "employee": employee,
        "role": role,
        "task": "Bedrock API access granted",
        "status": "Completed",
        "owner": "IT",
        "source": "it_tool",
    }


def simulate_hr_tool(employee: str, role: str) -> dict[str, str]:
    """Simulate HR tool output after sending benefits enrollment."""
    return {
        "employee": employee,
        "role": role,
        "task": "Benefits enrollment sent",
        "status": "Completed",
        "owner": "HR",
        "source": "hr_tool",
    }


def _task_is_logged(lookup: str, task: str) -> bool:
    """Return True if get_employee_tasks output contains this task."""
    return task.lower() in lookup.lower() and "error" not in lookup.lower()[:40]


def run_scenario(number: int, title: str, payload: dict[str, str]) -> bool:
    """Log a simulated tool output and verify it appears in the tracker."""
    print(f"\n{'=' * 70}")
    print(f"Scenario {number} — {title}")
    print(f"Source tool: {payload['source']}")
    print("=" * 70)

    print("Simulated tool output:")
    print(f"  Employee: {payload['employee']}")
    print(f"  Role:     {payload['role']}")
    print(f"  Task:     {payload['task']}")
    print(f"  Status:   {payload['status']}")
    print(f"  Owner:    {payload['owner']}")

    logged = log_status(
        payload["employee"],
        payload["role"],
        payload["task"],
        payload["status"],
        payload["owner"],
    )
    print(f"\nLogged: {logged}")

    lookup = get_employee_tasks(payload["employee"])
    found = _task_is_logged(lookup, payload["task"]) and logged.lower().startswith("logged:")
    result = "PASS" if found else "FAIL"

    print("\nVerification (get_employee_tasks):")
    print(lookup if lookup.strip() else "  (empty)")
    print(f"\nResult: {result}")
    return found


def main() -> int:
    print("\n" + "=" * 70)
    print("OnboardOps Tracker Integration Tests")
    print("Simulated outputs from checklist, scheduler, IT, and HR tools")
    print("=" * 70)

    reset_sheet_client()

    scenarios: list[tuple[int, str, dict[str, Any]]] = [
        (1, "Checklist Tool Output", simulate_checklist_tool(EMPLOYEE, ROLE)),
        (2, "Scheduling Tool Output", simulate_scheduling_tool(EMPLOYEE, ROLE)),
        (3, "IT Tool Output", simulate_it_tool(EMPLOYEE, ROLE)),
        (4, "HR Tool Output", simulate_hr_tool(EMPLOYEE, ROLE)),
    ]

    results: list[bool] = []
    for number, title, payload in scenarios:
        results.append(run_scenario(number, title, payload))

    passed = sum(1 for ok in results if ok)
    total = len(results)

    print("\n" + "=" * 70)
    if passed == total:
        print(f"Summary: {passed}/{total} integration tests passed ✅")
    else:
        print(f"Summary: {passed}/{total} integration tests passed")
        print("Check credentials.json and SETUP_GOOGLE_SHEETS.md if tests failed.")
    print("=" * 70 + "\n")

    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())

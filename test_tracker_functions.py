"""
Standalone tracker function tests against the live Google Sheet.

Proves get_employee_tasks, update_task_status, and get_all_tasks work
independently before the agent is wired up.

Run from project root:
    python test_tracker_functions.py
"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tools.tracker_tool import (  # noqa: E402
    HEADERS,
    _get_all_records,
    get_all_tasks,
    get_employee_tasks,
    reset_sheet_client,
    update_task_status,
)

EMPLOYEE = "Rajesh Kumar"
NEW_STATUS = "Completed"


def _print_section(title: str) -> None:
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def _pass_fail(ok: bool) -> str:
    return "PASS" if ok else "FAIL"


def test_get_employee_tasks() -> bool:
    _print_section("1. get_employee_tasks(\"Rajesh Kumar\")")
    print("What it does: Retrieve all tracker rows for one employee.")
    print(f"Input: employee={EMPLOYEE!r}")

    result = get_employee_tasks(EMPLOYEE)
    print("\nResult:")
    print(result)

    ok = (
        EMPLOYEE.lower() in result.lower()
        and "error" not in result.lower()[:40]
        and "no tasks found" not in result.lower()
    )
    print(f"\nResult: {_pass_fail(ok)}")
    return ok


def _pick_task_to_complete() -> tuple[str, int] | None:
    """Pick a Rajesh Kumar row that is not already Completed. Returns (task, sheet_row)."""
    records = _get_all_records()
    for idx, record in enumerate(records):
        employee = str(record.get("Employee", "")).strip()
        task = str(record.get("Task", "")).strip()
        status = str(record.get("Status", "")).strip()
        if employee.lower() == EMPLOYEE.lower() and task and status != NEW_STATUS:
            return task, idx + 2  # header is row 1
    return None


def test_update_task_status() -> bool:
    _print_section('2. update_task_status(..., "Completed")')
    print("What it does: Change one task's Status column in the Google Sheet.")
    print("API: update_task_status(employee, task_name, new_status)")
    print("(Sheet row number is resolved from employee + task, then column D is updated.)")

    picked = _pick_task_to_complete()
    if picked is None:
        print("\nNo in-progress/not-started task found for Rajesh Kumar.")
        print("Falling back to re-completing 'Laptop provisioning' if it exists.")
        task_name = "Laptop provisioning"
        row_number = None
        for idx, record in enumerate(_get_all_records()):
            if (
                str(record.get("Employee", "")).strip().lower() == EMPLOYEE.lower()
                and str(record.get("Task", "")).strip().lower() == task_name.lower()
            ):
                row_number = idx + 2
                break
        if row_number is None:
            print("Result: FAIL")
            return False
    else:
        task_name, row_number = picked

    print(f"\nTarget employee: {EMPLOYEE}")
    print(f"Target task:     {task_name}")
    print(f"Sheet row:       {row_number}")
    print(f"New status:      {NEW_STATUS}")
    print(f"Status column:   {HEADERS.index('Status') + 1} (D)")

    result = update_task_status(EMPLOYEE, task_name, NEW_STATUS)
    print("\nResult:")
    print(f"  {result}")

    lookup = get_employee_tasks(EMPLOYEE)
    verified = (
        result.lower().startswith("updated")
        and task_name.lower() in lookup.lower()
        and "error" not in result.lower()
    )
    print("\nPost-update lookup:")
    print(lookup)
    print(f"\nResult: {_pass_fail(verified)}")
    return verified


def test_get_all_tasks() -> bool:
    _print_section("3. get_all_tasks()")
    print("What it does: Retrieve the entire OnboardOps tracker.")
    print("Input: none")

    result = get_all_tasks()
    print("\nResult:")
    print(result)

    ok = (
        "OnboardOps Tracker" in result
        and EMPLOYEE in result
        and "error" not in result.lower()[:40]
        and "no tasks logged" not in result.lower()
    )
    print(f"\nResult: {_pass_fail(ok)}")
    return ok


def main() -> int:
    print("\n" + "=" * 70)
    print("Standalone Tracker Function Tests (live Google Sheet)")
    print("Sample employee: Rajesh Kumar, Software Engineer")
    print("=" * 70)

    reset_sheet_client()

    results = [
        ("get_employee_tasks", test_get_employee_tasks()),
        ("update_task_status", test_update_task_status()),
        ("get_all_tasks", test_get_all_tasks()),
    ]

    passed = sum(1 for _, ok in results if ok)
    total = len(results)

    _print_section("Summary")
    for name, ok in results:
        print(f"  {name}: {_pass_fail(ok)}")
    print(f"\n{passed}/{total} standalone tracker functions passed")
    if passed != total:
        print("If tests failed, check credentials.json and SETUP_GOOGLE_SHEETS.md.")
    print("=" * 70 + "\n")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())

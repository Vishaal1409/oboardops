"""
Checklist -> Tracker format-compatibility test.

Confirms (or disproves) that generate_checklist()'s real output can be bridged
cleanly into tracker_tool.py's Task column: parses real checklist items, shows
their raw lengths, derives short_task_label()s for them, and inspects exactly
what a mocked log_status() call would write to the sheet. Also demonstrates
generate_checklist()'s non-determinism concretely, to explain why a label
derived from one generation can't be reused to look up a task from a later
regeneration (see KNOWN_ISSUES.md).

Run from project root: python e2e/test_checklist_tracker_bridge.py
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tools.checklist_tool import (  # noqa: E402
    generate_checklist,
    parse_checklist_items,
    short_task_label,
)
from tools.tracker_tool import HEADERS, log_status, reset_sheet_client  # noqa: E402

ROLE = "Software Engineer"
DEPARTMENT = "Engineering"
TASK_COLUMN_INDEX = HEADERS.index("Task")


def _print_section(title: str) -> None:
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def _pass_fail(ok: bool) -> str:
    return "PASS" if ok else "FAIL"


def _mocked_sheet():
    """Context-manager-free mock setup mirroring test_tracker.py's pattern."""
    mock_worksheet = MagicMock()
    mock_worksheet.row_values.return_value = HEADERS
    mock_sheet = MagicMock()
    mock_sheet.worksheet.return_value = mock_worksheet
    mock_client = MagicMock()
    mock_client.open_by_key.return_value = mock_sheet
    return mock_worksheet, mock_client


def main() -> int:
    print("\n" + "=" * 70)
    print("Checklist -> Tracker Bridge Test (live checklist generation)")
    print(f"Role: {ROLE!r}  Department: {DEPARTMENT!r}")
    print("=" * 70)

    results: list[bool] = []

    # --- Step 1: real, live checklist generation -----------------------
    _print_section("1. generate_checklist() - live call #1")
    checklist_1 = generate_checklist(ROLE, DEPARTMENT)
    items_1 = parse_checklist_items(checklist_1)
    print(f"Parsed {len(items_1)} items.")
    ok_count = 5 <= len(items_1) <= 7
    results.append(ok_count)
    print(f"Result (5-7 items): {_pass_fail(ok_count)}")

    # --- Step 2: surface the raw-length problem with real data ----------
    _print_section("2. Raw item lengths (surfacing the format problem)")
    long_items = 0
    for i, item in enumerate(items_1, 1):
        length = len(item)
        flag = " <- long" if length > 80 else ""
        print(f"  [{i}] {length:3d} chars{flag}")
        if length > 80:
            long_items += 1
    print(f"\n{long_items}/{len(items_1)} items exceed 80 characters.")
    print("(This is expected and fine for a human-readable checklist - the")
    print(" problem is only when this text is used verbatim as a tracker Task.)")

    # --- Step 3: derive short labels, demonstrate the fix ----------------
    _print_section("3. short_task_label() applied to each item")
    labels = [short_task_label(item) for item in items_1]
    labels_ok = all(0 < len(label) <= 61 for label in labels)
    for i, (item, label) in enumerate(zip(items_1, labels), 1):
        print(f"  [{i}] ({len(item)} -> {len(label)} chars) {label!r}")
    results.append(labels_ok)
    print(f"\nResult (all labels non-empty, <=61 chars): {_pass_fail(labels_ok)}")

    # --- Step 4: feed a label through a MOCKED log_status ----------------
    _print_section("4. Mocked log_status() - inspect the actual row written")
    mock_worksheet, mock_client = _mocked_sheet()
    sample_label = labels[0]
    with patch("tools.tracker_tool.gspread.authorize", return_value=mock_client), patch(
        "tools.tracker_tool.Credentials.from_service_account_file", return_value=MagicMock()
    ), patch("tools.tracker_tool.DEFAULT_CREDENTIALS_PATH", Path("/tmp/fake-credentials.json")), patch(
        "pathlib.Path.exists", return_value=True
    ):
        reset_sheet_client()
        result = log_status(
            employee="Rajesh Kumar",
            role=ROLE,
            task=sample_label,
            status="Not Started",
            owner="HR",
        )

    print(f"log_status() returned: {result!r}")
    mock_worksheet.append_row.assert_called_once()
    written_row = mock_worksheet.append_row.call_args[0][0]
    written_task = written_row[TASK_COLUMN_INDEX]
    print(f"Row written to sheet: {written_row}")
    print(f"Task cell contains:   {written_task!r}")

    bridge_ok = (
        result.lower().startswith("logged:")
        and written_task == sample_label
        and len(written_task) <= 61
    )
    results.append(bridge_ok)
    print(f"\nResult (short label written cleanly to Task cell): {_pass_fail(bridge_ok)}")

    # --- Step 5: demonstrate non-determinism concretely -------------------
    _print_section("5. generate_checklist() - live call #2 (determinism check)")
    checklist_2 = generate_checklist(ROLE, DEPARTMENT)
    items_2 = parse_checklist_items(checklist_2)
    print(f"Call #1 items: {len(items_1)} | Call #2 items: {len(items_2)}")

    identical = set(items_1) == set(items_2)
    print(f"Item sets identical across calls: {identical}")
    if not identical:
        print("\nAs expected: the two generations differ in wording. This is why a")
        print("short_task_label() derived from call #1's items cannot be used to")
        print("update_task_status() against call #2's regenerated checklist - the")
        print("exact-match lookup in tracker_tool.py has no concept of \"the same")
        print("logical task across two generations,\" only literal string equality.")
        print("This is a pre-existing tracker limitation, tracked in KNOWN_ISSUES.md,")
        print("not something this test fixes.")
    # Informational only - does not affect pass/fail, since determinism/non-determinism
    # is a property of the LLM, not something this test enforces either way.

    # --- Summary -----------------------------------------------------------
    _print_section("Summary")
    total = len(results)
    passed = sum(results)
    print(f"{passed}/{total} core checks passed")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())

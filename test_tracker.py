"""
Test script for Tracker Tool
Run live against Google Sheets: python test_tracker.py --live
Run mocked unit tests:       python test_tracker.py
"""

from __future__ import annotations

import argparse
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tools.tracker_tool import (  # noqa: E402
    HEADERS,
    get_all_tasks,
    get_employee_tasks,
    log_status,
    reset_sheet_client,
    update_task_status,
)

# Sample data for Rajesh Kumar and Priya Sharma
SAMPLE_TASKS = [
    {
        "Employee": "Rajesh Kumar",
        "Role": "Software Engineer",
        "Task": "Laptop provisioned",
        "Status": "Completed",
        "Owner": "IT",
    },
    {
        "Employee": "Rajesh Kumar",
        "Role": "Software Engineer",
        "Task": "HR orientation scheduled",
        "Status": "In Progress",
        "Owner": "HR",
    },
    {
        "Employee": "Priya Sharma",
        "Role": "Product Manager",
        "Task": "Badge issued",
        "Status": "Not Started",
        "Owner": "Admin",
    },
]

LIVE_SAMPLE_ROWS = [
    ("Rajesh Kumar", "Software Engineer", "Laptop provisioned", "Completed", "IT"),
    ("Rajesh Kumar", "Software Engineer", "HR orientation scheduled", "In Progress", "HR"),
    ("Priya Sharma", "Product Manager", "Badge issued", "Not Started", "Admin"),
]


class TrackerToolTests(unittest.TestCase):
    """Unit tests for all 4 tracker functions (mocked Google Sheets)."""

    def setUp(self) -> None:
        reset_sheet_client()
        self.mock_worksheet = MagicMock()
        self.mock_worksheet.row_values.return_value = HEADERS
        self.mock_worksheet.get_all_records.return_value = list(SAMPLE_TASKS)

        self.mock_sheet = MagicMock()
        self.mock_sheet.worksheet.return_value = self.mock_worksheet

        self.mock_client = MagicMock()
        self.mock_client.open_by_key.return_value = self.mock_sheet

        patcher = patch(
            "tools.tracker_tool.gspread.authorize",
            return_value=self.mock_client,
        )
        patcher.start()
        self.addCleanup(patcher.stop)

        creds_patcher = patch(
            "tools.tracker_tool.Credentials.from_service_account_file",
            return_value=MagicMock(),
        )
        creds_patcher.start()
        self.addCleanup(creds_patcher.stop)

        exists_patcher = patch(
            "tools.tracker_tool.DEFAULT_CREDENTIALS_PATH",
            Path("/tmp/fake-credentials.json"),
        )
        exists_patcher.start()
        self.addCleanup(exists_patcher.stop)

        path_exists_patcher = patch("pathlib.Path.exists", return_value=True)
        path_exists_patcher.start()
        self.addCleanup(path_exists_patcher.stop)

    def test_log_status(self) -> None:
        result = log_status(
            employee="Rajesh Kumar",
            role="Software Engineer",
            task="Email account created",
            status="Completed",
            owner="IT",
        )
        self.assertIn("Logged:", result)
        self.mock_worksheet.append_row.assert_called_once()

    def test_get_employee_tasks(self) -> None:
        result = get_employee_tasks("Rajesh Kumar")
        self.assertIn("Tasks for Rajesh Kumar", result)
        self.assertIn("Laptop provisioned", result)
        self.assertIn("HR orientation scheduled", result)
        self.assertNotIn("Priya Sharma", result)

    def test_get_all_tasks(self) -> None:
        result = get_all_tasks()
        self.assertIn("OnboardOps Tracker - All Tasks", result)
        self.assertIn("Rajesh Kumar", result)
        self.assertIn("Priya Sharma", result)

    def test_update_task_status(self) -> None:
        result = update_task_status(
            "Rajesh Kumar",
            "HR orientation scheduled",
            "Completed",
        )
        self.assertIn("Updated Rajesh Kumar", result)
        self.mock_worksheet.update_cell.assert_called_once_with(3, 4, "Completed")


def run_live_tests() -> None:
    """Live integration test — calls all 4 tracker functions against Google Sheets."""
    print("\n" + "=" * 60)
    print("Live Tracker Tool Test (Google Sheets)")
    print("=" * 60)

    reset_sheet_client()

    # 1. log_status — write sample tasks for Rajesh Kumar and Priya Sharma
    print("\n[1/4] log_status")
    for employee, role, task, status, owner in LIVE_SAMPLE_ROWS:
        print(f"  Logging: {employee} | {task} | {status}")
        print(f"  → {log_status(employee, role, task, status, owner)}")

    # 2. get_employee_tasks — fetch Rajesh Kumar's tasks
    print("\n[2/4] get_employee_tasks")
    print(get_employee_tasks("Rajesh Kumar"))

    # 3. update_task_status — mark one task completed
    print("\n[3/4] update_task_status")
    print(
        update_task_status(
            "Rajesh Kumar",
            "HR orientation scheduled",
            "Completed",
        )
    )

    # 4. get_all_tasks — full tracker overview
    print("\n[4/4] get_all_tasks")
    print(get_all_tasks())

    print("\n" + "=" * 60)
    print("Live test complete.")
    print("=" * 60)


def main() -> None:
    parser = argparse.ArgumentParser(description="Test the OnboardOps tracker tool.")
    parser.add_argument(
        "--live",
        action="store_true",
        help="Run live tests against Google Sheets (requires credentials.json).",
    )
    args = parser.parse_args()

    if args.live:
        run_live_tests()
        return

    print("\n" + "=" * 60)
    print("Tracker Tool Tests (mocked Google Sheets)")
    print("=" * 60)
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TrackerToolTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        sys.exit(1)


if __name__ == "__main__":
    main()

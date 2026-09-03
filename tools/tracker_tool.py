"""
Tracker Tool for OnboardOps - Strands Agent Integration
Logs onboarding task updates to a shared Google Sheet.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Optional

import gspread
from google.oauth2.service_account import Credentials
from strands import tool

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SHEET_ID = "1X_0-I8tuDK11ic35iv4HEUInCytviuFd0wQb-BBono0"
DEFAULT_CREDENTIALS_PATH = PROJECT_ROOT / "credentials.json"
WORKSHEET_NAME = "Sheet1"

HEADERS = ["Employee", "Role", "Task", "Status", "Owner"]
VALID_STATUSES = {"Not Started", "In Progress", "Completed", "Blocked"}
STATUS_COLUMN = "Status"

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


class GoogleSheetClient:
    """Manages a lazy, singleton Google Sheet connection."""

    _instance: Optional["GoogleSheetClient"] = None

    def __new__(cls, sheet_id: str, credentials_path: Path = DEFAULT_CREDENTIALS_PATH):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.sheet_id = sheet_id
            cls._instance.credentials_path = Path(credentials_path)
            cls._instance.client: Optional[gspread.Client] = None
            cls._instance.worksheet: Optional[gspread.Worksheet] = None
        return cls._instance

    @classmethod
    def reset(cls) -> None:
        """Reset singleton (useful for tests)."""
        cls._instance = None

    def _connect(self) -> None:
        """Authenticate and connect to Google Sheet."""
        if not self.credentials_path.exists():
            raise FileNotFoundError(
                f"Credentials not found at {self.credentials_path}. "
                "Follow SETUP_GOOGLE_SHEETS.md to create credentials.json."
            )

        try:
            creds = Credentials.from_service_account_file(
                str(self.credentials_path),
                scopes=SCOPES,
            )
            self.client = gspread.authorize(creds)
            sheet = self.client.open_by_key(self.sheet_id)
            self.worksheet = sheet.worksheet(WORKSHEET_NAME)
            self._ensure_headers()
        except FileNotFoundError:
            raise
        except gspread.exceptions.SpreadsheetNotFound as exc:
            raise ConnectionError(
                f"Spreadsheet not found. Verify SHEET_ID and sharing permissions: {exc}"
            ) from exc
        except gspread.exceptions.WorksheetNotFound as exc:
            raise ConnectionError(
                f"Worksheet '{WORKSHEET_NAME}' not found in spreadsheet: {exc}"
            ) from exc
        except Exception as exc:
            raise ConnectionError(f"Failed to connect to Google Sheet: {exc}") from exc

    def get_worksheet(self) -> gspread.Worksheet:
        """Return worksheet, connecting on first use."""
        if self.worksheet is None:
            self._connect()
        return self.worksheet  # type: ignore[return-value]

    def _ensure_headers(self) -> None:
        """Ensure the sheet has the expected header row."""
        worksheet = self.worksheet
        if worksheet is None:
            return

        first_row = worksheet.row_values(1)
        if not first_row:
            worksheet.append_row(HEADERS, value_input_option="USER_ENTERED")
            return

        normalized = [cell.strip() for cell in first_row]
        if normalized[: len(HEADERS)] != HEADERS:
            raise ValueError(
                "Sheet headers do not match expected format. "
                f"Expected: {HEADERS}. Found: {first_row}"
            )

    def append_row(self, row: list[Any]) -> bool:
        """Append a row to the sheet."""
        try:
            self.get_worksheet().append_row(row, value_input_option="USER_ENTERED")
            return True
        except Exception as exc:
            logger.exception("Error appending row to Google Sheet")
            raise RuntimeError(f"Failed to append row: {exc}") from exc


_sheet_client: Optional[GoogleSheetClient] = None


def reset_sheet_client() -> None:
    """Reset cached sheet client (useful for tests)."""
    global _sheet_client
    _sheet_client = None
    GoogleSheetClient.reset()


def get_sheet_client(
    credentials_path: Path = DEFAULT_CREDENTIALS_PATH,
) -> GoogleSheetClient:
    """Get or create the sheet client."""
    global _sheet_client
    if _sheet_client is None:
        _sheet_client = GoogleSheetClient(SHEET_ID, credentials_path)
    return _sheet_client


def _validate_required_field(value: str, field_name: str) -> str:
    """Validate that a required string field is non-empty."""
    if not value or not str(value).strip():
        raise ValueError(f"{field_name} is required and cannot be empty.")
    return str(value).strip()


def _validate_status(status: str) -> str:
    """Validate and normalize task status."""
    cleaned = _validate_required_field(status, "status")
    if cleaned not in VALID_STATUSES:
        allowed = ", ".join(sorted(VALID_STATUSES))
        raise ValueError(f"Invalid status '{cleaned}'. Must be one of: {allowed}")
    return cleaned


def _get_all_records() -> list[dict[str, Any]]:
    """Fetch all task records from the sheet."""
    worksheet = get_sheet_client().get_worksheet()
    return worksheet.get_all_records(expected_headers=HEADERS)


def _format_employee_tasks(employee_name: str, records: list[dict[str, Any]]) -> str:
    """Format task records for a single employee."""
    employee_tasks = [
        record
        for record in records
        if str(record.get("Employee", "")).strip().lower() == employee_name.lower()
    ]

    if not employee_tasks:
        return f"No tasks found for {employee_name}"

    lines = [f"\nTasks for {employee_name}:"]
    for record in employee_tasks:
        lines.append(
            f"  - {record.get('Task')} [{record.get('Status')}] "
            f"(Owner: {record.get('Owner')})"
        )
    return "\n".join(lines)


def _format_all_tasks(records: list[dict[str, Any]]) -> str:
    """Format all task records for display."""
    if not records:
        return "No tasks logged yet."

    lines = [
        "",
        "=" * 80,
        "OnboardOps Tracker - All Tasks",
        "=" * 80,
    ]
    for index, record in enumerate(records, 1):
        lines.extend(
            [
                "",
                f"{index}. {record.get('Employee')} ({record.get('Role')})",
                f"   Task: {record.get('Task')}",
                f"   Status: {record.get('Status')} | Owner: {record.get('Owner')}",
            ]
        )
    lines.append("\n" + "=" * 80)
    return "\n".join(lines)


def _update_task_status_in_sheet(employee_name: str, task: str, status: str) -> str:
    """Update a task row in the sheet and return a result message."""
    worksheet = get_sheet_client().get_worksheet()
    records = worksheet.get_all_records(expected_headers=HEADERS)

    for idx, record in enumerate(records):
        record_employee = str(record.get("Employee", "")).strip().lower()
        record_task = str(record.get("Task", "")).strip().lower()
        if record_employee == employee_name.lower() and record_task == task.lower():
            row_number = idx + 2  # account for header row
            status_col = HEADERS.index(STATUS_COLUMN) + 1
            worksheet.update_cell(row_number, status_col, status)
            return f"Updated {employee_name}'s '{task}' to {status}"

    return f"Task not found for {employee_name}: {task}"


@tool
def log_status(employee: str, role: str, task: str, status: str, owner: str) -> str:
    """
    Log an onboarding task status update to the shared Google Sheet tracker.

    Called by the Strands agent whenever a task is completed or updated.
    Writes to the OnboardOps Tracker sheet so managers can see real-time status.

    Args:
        employee: New hire's name (e.g., "Rajesh Kumar").
        role: Job role (e.g., "Software Engineer").
        task: Task description (e.g., "Laptop provisioned").
        status: Task status (Not Started / In Progress / Completed / Blocked).
        owner: Who is responsible (e.g., "IT", "HR", "Manager").

    Returns:
        Success or error message.
    """
    try:
        row = [
            _validate_required_field(employee, "employee"),
            _validate_required_field(role, "role"),
            _validate_required_field(task, "task"),
            _validate_status(status),
            _validate_required_field(owner, "owner"),
        ]
        get_sheet_client().append_row(row)
        return f"Logged: {row[0]} | {row[2]} | {row[3]}"
    except FileNotFoundError as exc:
        return f"Setup Error: {exc}"
    except (ConnectionError, ValueError, RuntimeError) as exc:
        return f"Error: {exc}"
    except Exception as exc:
        logger.exception("Unexpected error in log_status")
        return f"Unexpected error: {exc}"


@tool
def get_employee_tasks(employee: str) -> str:
    """
    Retrieve all onboarding tasks for a specific employee.

    Args:
        employee: Employee name to look up.

    Returns:
        Formatted list of tasks for the employee.
    """
    try:
        employee_name = _validate_required_field(employee, "employee")
        return _format_employee_tasks(employee_name, _get_all_records())
    except (FileNotFoundError, ConnectionError, ValueError, RuntimeError) as exc:
        return f"Error retrieving tasks: {exc}"
    except Exception as exc:
        logger.exception("Unexpected error in get_employee_tasks")
        return f"Unexpected error: {exc}"


@tool
def update_task_status(employee: str, task_name: str, new_status: str) -> str:
    """
    Update the status of a specific onboarding task.

    Args:
        employee: Employee name.
        task_name: Task to update.
        new_status: New status (Not Started / In Progress / Completed / Blocked).

    Returns:
        Success or error message.
    """
    try:
        employee_name = _validate_required_field(employee, "employee")
        task = _validate_required_field(task_name, "task_name")
        status = _validate_status(new_status)
        return _update_task_status_in_sheet(employee_name, task, status)
    except (FileNotFoundError, ConnectionError, ValueError, RuntimeError) as exc:
        return f"Error updating task: {exc}"
    except Exception as exc:
        logger.exception("Unexpected error in update_task_status")
        return f"Unexpected error: {exc}"


@tool
def get_all_tasks() -> str:
    """
    Get an overview of all onboarding tasks in the tracker.

    Returns:
        Formatted table of all tasks.
    """
    try:
        return _format_all_tasks(_get_all_records())
    except (FileNotFoundError, ConnectionError, ValueError, RuntimeError) as exc:
        return f"Error retrieving tasks: {exc}"
    except Exception as exc:
        logger.exception("Unexpected error in get_all_tasks")
        return f"Unexpected error: {exc}"

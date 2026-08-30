# OnboardOps Google Sheets Setup Guide

This guide walks you through connecting the OnboardOps tracker tool to Google Sheets using a service account.

## Overview

The tracker tool writes onboarding task updates to this shared spreadsheet:

- **Sheet ID:** `1X_0-I8tuDK11ic35iv4HEUInCytviuFd0wQb-BBono0`
- **Worksheet:** `Sheet1`
- **Columns:** `Employee | Role | Task | Status | Owner`

Valid status values:

- `Not Started`
- `In Progress`
- `Completed`
- `Blocked`

---

## Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Click **Select a project** → **New Project**.
3. Name it (e.g., `onboardops-tracker`) and click **Create**.
4. Select the new project from the project dropdown.

---

## Step 2: Enable the Google Sheets API

1. In Cloud Console, open **APIs & Services** → **Library**.
2. Search for **Google Sheets API**.
3. Click it and press **Enable**.

---

## Step 3: Create a Service Account

1. Go to **APIs & Services** → **Credentials**.
2. Click **Create Credentials** → **Service account**.
3. Name it (e.g., `onboardops-sheets-bot`) and click **Create and Continue**.
4. Skip optional role/permission steps and click **Done**.
5. Open the service account you just created.
6. Go to the **Keys** tab → **Add Key** → **Create new key** → **JSON**.
7. Download the JSON file and save it as:

```text
oboardops/credentials.json
```

**Important:** Never commit `credentials.json` to git. It is already listed in `.gitignore`.

---

## Step 4: Share the Spreadsheet with the Service Account

1. Open the downloaded JSON file and copy the `client_email` value.
   It looks like: `onboardops-sheets-bot@your-project.iam.gserviceaccount.com`
2. Open the [OnboardOps Tracker Sheet](https://docs.google.com/spreadsheets/d/1X_0-I8tuDK11ic35iv4HEUInCytviuFd0wQb-BBono0/edit).
3. Click **Share**.
4. Paste the service account email and grant **Editor** access.
5. Uncheck **Notify people** and click **Share**.

Without this step, the API will return permission errors even with valid credentials.

---

## Step 5: Prepare the Sheet Headers

Row 1 of `Sheet1` must contain these exact headers:

```text
Employee | Role | Task | Status | Owner
```

The tracker tool will create this header row automatically if the sheet is empty. If you already have data, make sure the headers match exactly.

---

## Step 6: Install Python Dependencies

From the project root:

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

---

## Step 7: Test the Integration

### Mocked tests (no credentials required)

```bash
python test_tracker.py
```

This runs unit tests with a mocked Google Sheets client.

### Live test (requires credentials.json)

```bash
python test_tracker.py --live
```

This will:

1. Log sample onboarding tasks for two employees
2. Fetch tasks for one employee
3. Update a task status
4. Print all tasks from the sheet

---

## Step 8: Use in the Strands Agent

Import the tracker tools in your agent:

```python
from strands import Agent
from tools.tracker_tool import (
    log_status,
    get_employee_tasks,
    update_task_status,
    get_all_tasks,
)

agent = Agent(tools=[log_status, get_employee_tasks, update_task_status, get_all_tasks])
```

Example agent prompt:

```text
Log that Rajesh Kumar (Software Engineer) has completed laptop provisioning. Owner is IT.
```

---

## Troubleshooting

### `credentials.json not found`

- Ensure the file is at the project root: `oboardops/credentials.json`
- Run commands from the project root directory

### `Spreadsheet not found`

- Verify the sheet ID in `tools/tracker_tool.py`
- Confirm the service account email has **Editor** access to the sheet

### `Worksheet 'Sheet1' not found`

- Rename your tab to `Sheet1`, or update `WORKSHEET_NAME` in `tools/tracker_tool.py`

### `Sheet headers do not match expected format`

- Row 1 must be exactly: `Employee, Role, Task, Status, Owner`
- Remove extra columns from row 1 or move them to a different sheet

### `Invalid status`

- Status must be one of: `Not Started`, `In Progress`, `Completed`, `Blocked`
- Status values are case-sensitive

### API quota / rate limits

- Google Sheets API has generous free quotas for hackathon/demo use
- If you hit limits, wait a minute and retry

---

## Security Checklist

- [ ] `credentials.json` is in `.gitignore`
- [ ] Service account has access only to the tracker spreadsheet
- [ ] Credentials are not shared in Slack, email, or demo recordings
- [ ] Rotate keys if credentials are ever exposed

---

## File Reference

| File | Purpose |
|------|---------|
| `credentials.json` | Service account key (local only, not in git) |
| `tools/tracker_tool.py` | Tracker tool with Strands `@tool` functions |
| `test_tracker.py` | Mocked and live integration tests |
| `requirements.txt` | Python dependencies |

---

## Quick Verification Checklist

```bash
# 1. Dependencies installed
pip install -r requirements.txt

# 2. Credentials in place
test -f credentials.json && echo "credentials.json found"

# 3. Mocked tests pass
python test_tracker.py

# 4. Live test (optional)
python test_tracker.py --live
```

If all steps pass, your Google Sheets integration is ready for the hackathon demo.

from strands import tool

@tool
def log_status(employee: str, role: str, task: str, status: str, owner: str) -> str:
    """Logs an onboarding task's status update to the shared Google Sheet tracker."""
    # TODO: Ishitha implements this — writes to the shared Google Sheet
    return f"Logged: {employee} | {task} | {status}"
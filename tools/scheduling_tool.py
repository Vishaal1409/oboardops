from datetime import datetime, timedelta
from strands import tool


# First-week onboarding schedule from first_week_schedule.md
FIRST_WEEK_SCHEDULE = [
    {
        "day": "Day 1",
        "title": "Welcome & Setup",
        "meetings": [
            "Welcome and HR introduction",
            "Complete onboarding paperwork and essential policies",
            "IT setup: device, accounts, and required software",
            "Meet the manager and immediate team",
        ],
    },
    {
        "day": "Day 2",
        "title": "Role & Tools",
        "meetings": [
            "Introduction to role and responsibilities",
            "Review expectations and initial goals",
            "Introduction to team tools and workflows",
            "Check-in with manager",
        ],
    },
    {
        "day": "Day 3",
        "title": "Team & Processes",
        "meetings": [
            "Cross-functional team introductions",
            "Understand key team responsibilities and collaboration",
            "Walk through important business and team processes",
            "Q&A session",
        ],
    },
    {
        "day": "Day 4",
        "title": "Role-Specific Training",
        "meetings": [
            "Role-specific training and resources",
            "Practice key workflows and tools",
            "Review questions and blockers",
            "Manager check-in",
        ],
    },
    {
        "day": "Day 5",
        "title": "Review & Next Steps",
        "meetings": [
            "Review first-week progress",
            "Address outstanding questions",
            "Gather onboarding feedback",
            "Set priorities and goals for Week 2",
        ],
    },
]


@tool
def generate_schedule(start_date: str) -> list:
    """
    Generate the first five working days of the onboarding schedule.

    Args:
        start_date: Employee start date in YYYY-MM-DD format.

    Returns:
        A list containing the date, weekday, onboarding day,
        title, and meetings for each onboarding day.
    """

    # Validate and convert the start date
    try:
        current_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError(
            "Invalid start_date. Please use YYYY-MM-DD format."
        )

    # If the employee starts on a weekend,
    # begin onboarding on the following Monday.
    if current_date.weekday() == 5:  # Saturday
        current_date += timedelta(days=2)
    elif current_date.weekday() == 6:  # Sunday
        current_date += timedelta(days=1)

    schedule = []

    for onboarding_day in FIRST_WEEK_SCHEDULE:
        # Add the current working day to the schedule
        schedule.append(
            {
                "date": current_date.isoformat(),
                "weekday": current_date.strftime("%A"),
                "day": onboarding_day["day"],
                "title": onboarding_day["title"],
                "meetings": onboarding_day["meetings"],
            }
        )

        # Move to the next working day
        current_date += timedelta(days=1)

        # Skip Saturday and Sunday
        if current_date.weekday() == 5:  # Saturday
            current_date += timedelta(days=2)
        elif current_date.weekday() == 6:  # Sunday
            current_date += timedelta(days=1)

    return schedule
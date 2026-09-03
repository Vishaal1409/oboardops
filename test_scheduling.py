from tools.scheduling_tool import generate_schedule


test_dates = [
    "2026-08-31",  # Monday
    "2026-09-02",  # Wednesday
    "2026-09-04",  # Friday
    "2026-09-05",  # Saturday
    "2026-09-06",  # Sunday
]


for start_date in test_dates:
    print("\n" + "=" * 60)
    print(f"START DATE: {start_date}")
    print("=" * 60)

    schedule = generate_schedule(start_date)

    for day in schedule:
        print(f"{day['day']} - {day['date']} ({day['weekday']})")
        print(f"  {day['title']}")

        for meeting in day["meetings"]:
            print(f"  - {meeting}")
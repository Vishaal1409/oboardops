"""
Test script for Checklist Tool
Confirms checklist items differ meaningfully by role/department, and that
trickier inputs (blank fields, unusual titles) are handled without crashing.
"""

from tools.checklist_tool import generate_checklist


def test_checklist():
    """Test the checklist tool"""

    print("\n" + "=" * 60)
    print("Testing Checklist Tool")
    print("=" * 60)

    # Standard roles - output should differ meaningfully between each
    test_cases = [
        {"role": "Software Engineer", "department": "Engineering"},
        {"role": "Sales Representative", "department": "Sales"},
        {"role": "HR Manager", "department": "Human Resources"},
    ]

    # Trickier inputs: an unusual-but-real title should still produce a
    # tailored checklist; blank/whitespace-only role or department should be
    # rejected with a clear "Error: ..." string rather than crashing or
    # silently guessing.
    edge_cases = [
        {"role": "Chief Vibes Officer", "department": "Culture & Vibes"},
        {"role": "Software Engineer", "department": ""},
        {"role": "", "department": "Engineering"},
        {"role": "   ", "department": "   "},
    ]

    for case in test_cases + edge_cases:
        print(f"\nROLE: {case['role']!r} | DEPARTMENT: {case['department']!r}")
        print("-" * 60)
        result = generate_checklist(**case)
        print(result)


if __name__ == "__main__":
    test_checklist()

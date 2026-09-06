"""
HR Q&A stress test — paraphrased, casual, and abbreviated questions.
Run from project root: python test_hr_qa_stress.py
"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tools.hr_qa_tool import HRQATool  # noqa: E402

PASS_THRESHOLD = 0.5

STRESS_QUESTIONS = [
    "how much PTO do we get?",
    "what if i want to leave the company?",
    "do i get paid if i don't come to office?",
    "health coverage details please",
    "can i work from my couch?",
    "notice period for quitting?",
    "i need time off - what's the policy?",
    "maternity leave for men?",
    "professional courses - will company pay?",
    "flexible hours available?",
]


def run_stress_test() -> int:
    print("\n" + "=" * 70)
    print("HR Q&A Stress Test (varied real-world wording)")
    print("=" * 70)

    try:
        hr_qa = HRQATool()
    except (FileNotFoundError, ValueError) as exc:
        print(f"Failed to load HR Q&A tool: {exc}")
        return 1

    print(f"Loaded {len(hr_qa.policies)} policies | PASS if confidence > {PASS_THRESHOLD}\n")

    passed = 0
    failed = 0

    for index, question in enumerate(STRESS_QUESTIONS, 1):
        result = hr_qa.search(question)
        print(f"{index}. Q: {question}")

        if not result:
            failed += 1
            print("   Confidence: n/a | Category: n/a")
            print("   Result: FAIL (no match)\n")
            continue

        confidence = float(result.get("confidence") or 0)
        category = result.get("category") or "unknown"
        matched = result.get("question") or ""
        is_pass = confidence > PASS_THRESHOLD

        if is_pass:
            passed += 1
            outcome = "PASS"
        else:
            failed += 1
            outcome = "FAIL"

        print(f"   Confidence: {confidence:.2f} | Category: {category}")
        print(f"   Matched: {matched}")
        print(f"   Result: {outcome}\n")

    total = len(STRESS_QUESTIONS)
    print("=" * 70)
    print(f"Summary: {passed}/{total} PASS  |  {failed}/{total} FAIL")
    print("=" * 70 + "\n")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(run_stress_test())

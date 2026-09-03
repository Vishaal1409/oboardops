"""
Test script for HR Q&A Tool
Run this to verify the tool works before Week 2 integration
"""

from tools.hr_qa_tool import HRQATool


def test_hr_qa():
    """Test the HR Q&A tool"""
    
    print("\n" + "="*60)
    print("Testing HR Q&A Tool")
    print("="*60)
    
    # Initialize
    try:
        hr_qa = HRQATool()
        print(f"✓ Loaded {len(hr_qa.policies)} HR policies\n")
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return
    
    # Test questions
    test_questions = [
        "How many leave days do I get?",
        "What's the notice period?",
        "Can I work from home?",
        "What health insurance?",
        "How do I get reimbursed?",
        "When is my bonus?",
        "What if I have a problem at work?"
    ]
    
    # Run tests
    for q in test_questions:
        print(f"Q: {q}")
        result = hr_qa.search(q)
        if result:
            print(f"   Confidence: {result['confidence']} | Category: {result['category']}")
            print(f"   A: {result['answer'][:80]}...\n")
        else:
            print("   A: No match found\n")
    
    # Show categories
    print("="*60)
    print("Available Categories:")
    print("="*60)
    categories = hr_qa.get_all_categories()
    print(", ".join(categories))


if __name__ == "__main__":
    test_hr_qa()

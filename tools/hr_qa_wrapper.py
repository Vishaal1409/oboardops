from strands import tool
from tools.hr_qa_tool import HRQATool

# Initialize once so the knowledge base loads only one time
_hr_qa = HRQATool(knowledge_base_path="hr_qa_knowledge_base.json")

@tool
def answer_hr_question(question: str) -> str:
    """Answers an employee's HR policy question using the HR knowledge base."""
    return _hr_qa.answer_question(question)
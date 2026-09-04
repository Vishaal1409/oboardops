"""
HR Q&A Tool for OnboardOps
Loads HR policy knowledge base and answers employee policy questions.
Part of the Strands Agents orchestrator.
"""

from __future__ import annotations

import json
import logging
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Dict, List, Optional

from strands import tool

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_KNOWLEDGE_BASE_PATH = PROJECT_ROOT / "hr_qa_knowledge_base.json"


class HRQATool:
    """HR Policy Question & Answer Tool."""

    def __init__(self, knowledge_base_path: Path | str = DEFAULT_KNOWLEDGE_BASE_PATH):
        """
        Initialize the HR Q&A tool by loading the knowledge base.

        Args:
            knowledge_base_path: Path to the HR policy JSON file.
        """
        self.knowledge_base_path = Path(knowledge_base_path)
        self.policies: List[Dict[str, Any]] = []
        self.load_knowledge_base()

    def load_knowledge_base(self) -> None:
        """Load HR policies from JSON file."""
        if not self.knowledge_base_path.exists():
            raise FileNotFoundError(
                f"Knowledge base not found: {self.knowledge_base_path}"
            )

        try:
            with open(self.knowledge_base_path, "r", encoding="utf-8") as handle:
                data = json.load(handle)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON in knowledge base: {exc}") from exc

        policies = data.get("hr_policies")
        if not isinstance(policies, list):
            raise ValueError(
                "Knowledge base must contain an 'hr_policies' list at the top level."
            )

        self.policies = policies

    def _similarity_score(self, query: str, target: str) -> float:
        """Calculate similarity between two strings (0.0 to 1.0)."""
        query_lower = query.lower().strip()
        target_lower = target.lower().strip()
        return SequenceMatcher(None, query_lower, target_lower).ratio()

    def _keyword_boost(self, query: str, policy: Dict[str, Any]) -> float:
        """Add a small boost when query words appear in the policy question."""
        query_words = {word for word in query.lower().split() if len(word) > 3}
        if not query_words:
            return 0.0

        policy_text = policy.get("question", "").lower()
        matches = sum(1 for word in query_words if word in policy_text)
        return min(0.15, matches * 0.05)

    def search(self, question: str, threshold: float = 0.4) -> Optional[Dict[str, Any]]:
        """
        Search for the best matching HR policy answer.

        Args:
            question: Employee's question.
            threshold: Minimum similarity score (0.0-1.0).

        Returns:
            Best matching policy with confidence score, or None if no match.
        """
        if not question or not isinstance(question, str):
            return None

        best_match: Optional[Dict[str, Any]] = None
        best_score = threshold

        for policy in self.policies:
            policy_question = policy.get("question", "")
            score = self._similarity_score(question, policy_question)
            score += self._keyword_boost(question, policy)

            if score > best_score:
                best_score = score
                best_match = policy

        if best_match:
            return {
                "question": best_match.get("question"),
                "answer": best_match.get("answer"),
                "category": best_match.get("category"),
                "priority": best_match.get("priority"),
                "confidence": round(min(best_score, 1.0), 2),
            }

        return None

    def search_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get all policies in a specific category."""
        if not category or not isinstance(category, str):
            return []

        return [
            {
                "question": policy.get("question"),
                "answer": policy.get("answer"),
                "category": policy.get("category"),
                "priority": policy.get("priority"),
            }
            for policy in self.policies
            if str(policy.get("category", "")).lower() == category.lower()
        ]

    def get_all_categories(self) -> List[str]:
        """Get all available policy categories."""
        categories = {
            policy.get("category")
            for policy in self.policies
            if policy.get("category")
        }
        return sorted(categories)

    def answer_question(self, question: str) -> str:
        """
        Answer a question and return formatted response.

        For use in the Strands agent and test scripts.
        """
        result = self.search(question)
        if not result:
            return (
                "I couldn't find an answer to that question. "
                "Please contact HR at hr@company.com."
            )

        answer = str(result["answer"])
        confidence = float(result["confidence"])

        if confidence < 0.6:
            answer += (
                f"\n\n[Confidence: {int(confidence * 100)}%. "
                "Verify with HR if needed.]"
            )

        return answer


_hr_qa_instance: Optional[HRQATool] = None


def get_hr_qa_tool() -> HRQATool:
    """Get or create the shared HR Q&A tool instance."""
    global _hr_qa_instance
    if _hr_qa_instance is None:
        _hr_qa_instance = HRQATool()
    return _hr_qa_instance


@tool
def answer_hr_question(question: str) -> str:
    """
    Answer an employee's HR policy question using the knowledge base.

    Use this tool when employees ask about leave, benefits, reimbursement,
    notice period, work arrangements, or other HR policies.

    Args:
        question: The employee's HR policy question.

    Returns:
        Policy answer or guidance to contact HR.
    """
    try:
        return get_hr_qa_tool().answer_question(question)
    except FileNotFoundError as exc:
        return f"Setup Error: {exc}"
    except ValueError as exc:
        return f"Configuration Error: {exc}"
    except Exception as exc:
        logger.exception("Unexpected error in answer_hr_question")
        return f"Unexpected error: {exc}"


@tool
def list_hr_policy_categories() -> str:
    """
    List all HR policy categories available in the knowledge base.

    Returns:
        Comma-separated list of policy categories.
    """
    try:
        categories = get_hr_qa_tool().get_all_categories()
        if not categories:
            return "No HR policy categories found."
        return "Available HR policy categories: " + ", ".join(categories)
    except Exception as exc:
        logger.exception("Unexpected error in list_hr_policy_categories")
        return f"Error listing categories: {exc}"

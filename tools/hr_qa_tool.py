"""
HR Q&A Tool for OnboardOps
Loads HR policy knowledge base and answers employee policy questions.
Part of the Strands Agents orchestrator.
"""

import json
import os
from difflib import SequenceMatcher
from typing import Optional, Dict, List


class HRQATool:
    """HR Policy Question & Answer Tool"""
    
    def __init__(self, knowledge_base_path: str = "hr_qa_knowledge_base.json"):
        """
        Initialize the HR Q&A tool by loading the knowledge base.
        
        Args:
            knowledge_base_path (str): Path to the HR policy JSON file
        """
        self.knowledge_base_path = knowledge_base_path
        self.policies = []
        self.load_knowledge_base()
    
    def load_knowledge_base(self):
        """Load HR policies from JSON file."""
        if not os.path.exists(self.knowledge_base_path):
            raise FileNotFoundError(
                f"Knowledge base not found: {self.knowledge_base_path}"
            )
        
        try:
            with open(self.knowledge_base_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.policies = data.get("hr_policies", [])
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in knowledge base: {e}")
    
    def _similarity_score(self, query: str, target: str) -> float:
        """
        Calculate similarity between two strings (0.0 to 1.0).
        Uses SequenceMatcher for fuzzy matching.
        """
        query_lower = query.lower().strip()
        target_lower = target.lower().strip()
        matcher = SequenceMatcher(None, query_lower, target_lower)
        return matcher.ratio()
    
    def search(self, question: str, threshold: float = 0.4) -> Optional[Dict]:
        """
        Search for the best matching HR policy answer.
        
        Args:
            question (str): Employee's question
            threshold (float): Minimum similarity score (0.0-1.0)
                              Lower = more lenient. Default 0.4
        
        Returns:
            Dict: Best matching policy with confidence score
            None: If no match found above threshold
        """
        if not question or not isinstance(question, str):
            return None
        
        best_match = None
        best_score = threshold
        
        for policy in self.policies:
            policy_question = policy.get("question", "")
            score = self._similarity_score(question, policy_question)
            
            if score > best_score:
                best_score = score
                best_match = policy
        
        if best_match:
            return {
                "question": best_match.get("question"),
                "answer": best_match.get("answer"),
                "category": best_match.get("category"),
                "priority": best_match.get("priority"),
                "confidence": round(best_score, 2)
            }
        
        return None
    
    def search_by_category(self, category: str) -> List[Dict]:
        """Get all policies in a specific category."""
        matching = [
            {
                "question": p.get("question"),
                "answer": p.get("answer"),
                "category": p.get("category"),
                "priority": p.get("priority")
            }
            for p in self.policies 
            if p.get("category", "").lower() == category.lower()
        ]
        return matching
    
    def get_all_categories(self) -> List[str]:
        """Get all available policy categories."""
        categories = set(p.get("category") for p in self.policies if p.get("category"))
        return sorted(list(categories))
    
    def answer_question(self, question: str) -> str:
        """
        Answer a question and return formatted response.
        For use in the Strands agent.
        """
        result = self.search(question)
        
        if not result:
            return "I couldn't find an answer to that question. Please contact HR."
        
        answer = result["answer"]
        confidence = result["confidence"]
        
        if confidence < 0.6:
            answer += f"\n\n[Confidence: {int(confidence*100)}%. Verify with HR if needed.]"
        
        return answer

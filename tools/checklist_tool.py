"""
Checklist Tool for OnboardOps - Strands Agent Integration
Generates a personalized onboarding checklist for a new hire's role and department.
"""

import logging
from pathlib import Path

from pydantic import BaseModel, Field
from strands import Agent, tool
from strands.models import BedrockModel

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Domain skill: Indian HR & labour-law compliance
#
# Loaded from the project's Claude Code skill at .claude/skills/ so statutory
# content (Labour Codes, POSH, PF/ESI, gratuity, Shops & Establishments Act,
# etc.) has one source of truth shared between this tool and anything else in
# the repo that reads the same skill.
# ---------------------------------------------------------------------------
COMPLIANCE_SKILL_PATH = PROJECT_ROOT / ".claude" / "skills" / "indian-hr-compliance" / "SKILL.md"


def _load_compliance_reference() -> str:
    """Read the compliance skill file and strip its YAML frontmatter."""
    if not COMPLIANCE_SKILL_PATH.exists():
        logger.warning(
            "compliance skill not found at %s - statutory checklist items will rely "
            "on model recall instead of the verified reference",
            COMPLIANCE_SKILL_PATH,
        )
        return ""
    text = COMPLIANCE_SKILL_PATH.read_text(encoding="utf-8")
    if text.startswith("---"):
        _, _, text = text.partition("---\n")
        _, _, text = text.partition("\n---\n")
    return text.strip()


COMPLIANCE_REFERENCE = _load_compliance_reference()

# ---------------------------------------------------------------------------
# Prompt template
#
# Design choices:
#   - Role/department are injected into both the system prompt (framing the
#     model as an onboarding specialist for that exact context) and the user
#     turn (the concrete request), keeping it anchored to the specific pairing
#     instead of drifting into generic onboarding advice.
#   - Instructions explicitly ask for responsibilities/tools/goals UNIQUE to
#     the role+department combo, and forbid boilerplate items ("get an ID
#     badge") unless department-specific - this is what makes e.g. Software
#     Engineer/Engineering diverge visibly from Sales Rep/Sales.
#   - Item count is bounded (5-7) and each item must be a single actionable
#     step (starts with a verb) so the checklist is usable as-is, not prose.
#   - The compliance reference is appended so statutory/regulatory items (PF,
#     ESI, POSH, gratuity, appointment letters, etc.) reflect the actual
#     Indian Labour Codes and named forms instead of the model's own recall,
#     phrased as "verify current figure" rather than an asserted fact.
# ---------------------------------------------------------------------------
_BASE_SYSTEM_PROMPT = """You are an onboarding specialist who writes highly \
specific, actionable new-hire checklists. You tailor every item to the exact \
role and department you are given - naming the actual tools, systems, \
stakeholders, and early deliverables that someone in that job would \
realistically encounter in their first two weeks. Avoid generic filler steps \
(e.g. "get your ID badge", "read the employee handbook") unless they are \
genuinely specific to this department. Every item must be a concrete action \
starting with a verb."""

_COMPLIANCE_INSTRUCTIONS = """

Unless told otherwise, assume the new hire is India-based. When a checklist \
item touches a statutory or compliance matter (provident fund, ESI, POSH, \
gratuity, appointment letters, Shops & Establishments Act, professional tax, \
TDS, etc.), ground it strictly in the reference below - use its named forms \
(e.g. EPF Form 11, gratuity Form F) and thresholds, phrasing any number as \
"commonly X - verify current figure" rather than asserting it as fixed. Do \
not invent statutory details that aren't in this reference.

<indian_hr_compliance_reference>
{reference}
</indian_hr_compliance_reference>"""

CHECKLIST_SYSTEM_PROMPT = _BASE_SYSTEM_PROMPT + (
    _COMPLIANCE_INSTRUCTIONS.format(reference=COMPLIANCE_REFERENCE) if COMPLIANCE_REFERENCE else ""
)

CHECKLIST_PROMPT_TEMPLATE = """Generate a 5-7 item onboarding checklist for a new \
hire in the following position:

Role: {role}
Department: {department}

Requirements:
- Each item must be a single, actionable step (start with a verb).
- Items must reflect the specific tools, responsibilities, and goals of a \
{role} in {department} - not generic company-wide onboarding steps.
- Order items roughly in the sequence a new hire would complete them.
- Return between 5 and 7 items, no more, no less."""


class _OnboardingChecklist(BaseModel):
    """Structured, validated checklist output (internal - the tool returns a formatted string)."""

    role: str = Field(description="The role the checklist was generated for.")
    department: str = Field(description="The department the checklist was generated for.")
    items: list[str] = Field(
        description="5-7 actionable onboarding checklist items, each starting with a verb.",
        min_length=5,
        max_length=7,
    )

    def to_markdown(self) -> str:
        header = f"### Onboarding Checklist: {self.role} ({self.department})\n"
        bullets = "\n".join(f"- {item}" for item in self.items)
        return f"{header}\n{bullets}"


def _validate_required_field(value: str, field_name: str) -> str:
    """Validate that a required string field is non-empty."""
    if not value or not str(value).strip():
        raise ValueError(f"{field_name} is required and cannot be empty.")
    return str(value).strip()


def _build_agent() -> Agent:
    # Uses the caller's default AWS credentials/region (env vars, ~/.aws/credentials,
    # or an assumed role) - no separate Anthropic API key needed.
    model = BedrockModel(
        model_id="us.anthropic.claude-sonnet-4-6",
        max_tokens=2048,
    )
    # callback_handler=None silences the default per-step console logging (tool-call
    # traces, streamed tokens) so only the final formatted checklist is returned.
    return Agent(model=model, system_prompt=CHECKLIST_SYSTEM_PROMPT, callback_handler=None)


@tool
def generate_checklist(role: str, department: str) -> str:
    """Generate a personalized onboarding checklist based on role and department.

    Args:
        role: The new hire's job title, e.g. "Software Engineer".
        department: The department the new hire is joining, e.g. "Engineering".

    Returns:
        A Markdown-formatted 5-7 item onboarding checklist tailored to the role
        and department, or an "Error: ..." message if generation failed.
    """
    try:
        role = _validate_required_field(role, "role")
        department = _validate_required_field(department, "department")

        agent = _build_agent()
        prompt = CHECKLIST_PROMPT_TEMPLATE.format(role=role, department=department)
        result = agent(prompt, structured_output_model=_OnboardingChecklist)
        return result.structured_output.to_markdown()
    except ValueError as exc:
        return f"Error: {exc}"
    except Exception as exc:
        logger.exception("Unexpected error in generate_checklist")
        return f"Unexpected error: {exc}"

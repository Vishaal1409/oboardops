"""
checklist_tool.py

A personalized onboarding checklist generator built as a Strands tool.

Two-stage build history (kept as comments below, since the reviewer asked for
the design trail):

  Phase 1 - defined generate_onboarding_checklist(role, department), wrote the
  prompt template, and returned a hard-coded OnboardingChecklist so the
  function shape and call sites could be validated before wiring up the LLM.

  Phase 2 - replaced the dummy return with a real strands.Agent call against
  Claude on Amazon Bedrock (via BedrockModel, using the caller's existing AWS
  credentials), using structured output so the result is a validated, typed
  object instead of free-form text.
"""

from pathlib import Path

from pydantic import BaseModel, Field
from strands import Agent, tool
from strands.models import BedrockModel

# ---------------------------------------------------------------------------
# Domain skill: Indian HR & labour-law compliance
#
# Loaded from the project-local Claude Code skill at .claude/skills/ so the
# statutory content (Labour Codes, POSH, PF/ESI, gratuity, Shops &
# Establishments Act, etc.) has one source of truth shared between this tool
# and anything else in the repo that reads the same skill.
# ---------------------------------------------------------------------------
COMPLIANCE_SKILL_PATH = (
    Path(__file__).parent / ".claude" / "skills" / "indian-hr-compliance" / "SKILL.md"
)


def _load_compliance_reference() -> str:
    """Read the compliance skill file and strip its YAML frontmatter."""
    if not COMPLIANCE_SKILL_PATH.exists():
        raise FileNotFoundError(
            f"Indian HR compliance skill not found at {COMPLIANCE_SKILL_PATH}. "
            "This tool relies on it for statutory accuracy - restore the file "
            "before generating checklists."
        )
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
#   - The role/department are injected into both the system prompt (framing
#     Claude as an onboarding specialist for that exact context) and the user
#     turn (the concrete request), which keeps the model anchored to the
#     specific pairing instead of drifting to generic onboarding advice.
#   - The instructions explicitly ask for responsibilities/tools/goals that
#     are UNIQUE to the role+department combo, and forbid boilerplate items
#     ("get an ID badge", "read the handbook") unless department-specific -
#     this is what makes Software Engineer/Engineering diverge visibly from
#     Sales Representative/Sales in the output.
#   - Item count is bounded (5-7) and each item must be a single actionable
#     step (starts with a verb) so the checklist is usable as-is, not prose.
#   - The compliance reference is appended so any statutory/regulatory item
#     (PF, ESI, POSH, gratuity, appointment letters, etc.) reflects the actual
#     Indian Labour Codes and named forms instead of the model's own recall,
#     and is phrased as "verify current figure" rather than an asserted fact.
# ---------------------------------------------------------------------------
CHECKLIST_SYSTEM_PROMPT = f"""You are an onboarding specialist who writes highly \
specific, actionable new-hire checklists. You tailor every item to the exact \
role and department you are given - naming the actual tools, systems, \
stakeholders, and early deliverables that someone in that job would \
realistically encounter in their first two weeks. Avoid generic filler steps \
(e.g. "get your ID badge", "read the employee handbook") unless they are \
genuinely specific to this department. Every item must be a concrete action \
starting with a verb.

Unless told otherwise, assume the new hire is India-based. When a checklist \
item touches a statutory or compliance matter (provident fund, ESI, POSH, \
gratuity, appointment letters, Shops & Establishments Act, professional tax, \
TDS, etc.), ground it strictly in the reference below - use its named forms \
(e.g. EPF Form 11, gratuity Form F) and thresholds, phrasing any number as \
"commonly X - verify current figure" rather than asserting it as fixed. Do \
not invent statutory details that aren't in this reference.

<indian_hr_compliance_reference>
{COMPLIANCE_REFERENCE}
</indian_hr_compliance_reference>"""

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


class OnboardingChecklist(BaseModel):
    """Structured, validated checklist output."""

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


def _build_agent() -> Agent:
    # Uses the caller's default AWS credentials/region (env vars, ~/.aws/credentials,
    # or an assumed role) - no separate Anthropic API key needed.
    # Model ID: claude-sonnet-4-6 - this AWS account currently has Bedrock model
    # access granted for Sonnet 4.6 and Haiku 4.5 but not yet for the Opus/Sonnet 5
    # tier. Request model access in the Bedrock console and swap the ID below
    # to "us.anthropic.claude-opus-5" once granted.
    model = BedrockModel(
        model_id="us.anthropic.claude-sonnet-4-6",
        max_tokens=2048,
    )
    # callback_handler=None silences the default per-step console logging (tool-call
    # traces, streamed tokens) so only our own formatted checklist prints below.
    return Agent(model=model, system_prompt=CHECKLIST_SYSTEM_PROMPT, callback_handler=None)


@tool
def generate_onboarding_checklist(role: str, department: str) -> OnboardingChecklist:
    """Generate a personalized 5-7 item onboarding checklist for a new hire.

    Args:
        role: The new hire's job title, e.g. "Software Engineer".
        department: The department the new hire is joining, e.g. "Engineering".

    Returns:
        An OnboardingChecklist with items tailored to the given role and department.

    Raises:
        ValueError: If role or department is blank/whitespace-only. Both are required -
            without a real department in particular, the model silently guesses one
            (or falls back to a "please provide this info" non-checklist), which is
            worse than failing clearly at the boundary.
    """
    role = role.strip()
    department = department.strip()
    if not role or not department:
        raise ValueError(
            f"Both 'role' and 'department' are required and cannot be blank "
            f"(got role={role!r}, department={department!r})."
        )

    agent = _build_agent()
    prompt = CHECKLIST_PROMPT_TEMPLATE.format(role=role, department=department)
    result = agent(prompt, structured_output_model=OnboardingChecklist)
    return result.structured_output


if __name__ == "__main__":
    test_cases = [
        {"role": "Software Engineer", "department": "Engineering"},
        {"role": "Sales Representative", "department": "Sales"},
        {"role": "HR Manager", "department": "Human Resources"},
    ]

    # Trickier inputs: an unusual-but-real title should still produce a tailored
    # checklist; blank/whitespace-only role or department should be rejected
    # outright rather than silently degrading into a guessed or non-checklist
    # response (see the ValueError raised in generate_onboarding_checklist).
    edge_cases = [
        {"role": "Chief Vibes Officer", "department": "Culture & Vibes"},
        {"role": "Software Engineer", "department": ""},
        {"role": "", "department": "Engineering"},
        {"role": "   ", "department": "   "},
    ]

    for case in test_cases + edge_cases:
        print("=" * 70)
        print(f"CASE: role={case['role']!r}, department={case['department']!r}")
        print("=" * 70)
        try:
            result = generate_onboarding_checklist(**case)
            print(result.to_markdown())
        except ValueError as e:
            print(f"[REJECTED] {e}")
        print()

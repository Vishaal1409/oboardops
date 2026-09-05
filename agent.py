from strands import Agent
from tools.hr_qa_wrapper import answer_hr_question
from tools.checklist_tool import generate_checklist
from tools.scheduling_tool import generate_schedule
from tools.tracker_tool import log_status

agent = Agent(tools=[answer_hr_question, generate_checklist, generate_schedule, log_status])

print("=== Edge Case Test: Vague Role + Missing Info ===")
response = agent(
    "We have a new hire starting soon — just tell them about our leave policy, "
    "give them a basic onboarding checklist for a general Marketing role, "
    "and log that their 'Account setup' task is Not Started, owner unclear."
)
print(response)
from strands import Agent
from tools.hr_qa_wrapper import answer_hr_question
from tools.checklist_tool import generate_checklist
from tools.scheduling_tool import generate_schedule
from tools.tracker_tool import log_status

agent = Agent(tools=[answer_hr_question, generate_checklist, generate_schedule, log_status])

print("=== Full End-to-End Test ===")
response = agent(
    "A new hire named Rajesh Kumar is joining as a Software Engineer in Engineering, "
    "starting 2026-09-08. Please generate his onboarding checklist, tell him how many "
    "paid leave days he gets, create his first-week schedule, and log that his "
    "'Laptop provisioned' task is In Progress, owned by IT."
)
print(response)
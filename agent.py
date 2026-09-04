from strands import Agent
from tools.hr_qa_wrapper import answer_hr_question
from tools.checklist_tool import generate_checklist
from tools.scheduling_tool import generate_schedule

agent = Agent(tools=[answer_hr_question, generate_checklist, generate_schedule])

# Test 1: HR question
print("=== Test 1: HR Question ===")
response1 = agent("How many paid leave days do I get per year?")
print(response1)

# Test 2: Checklist request
print("\n=== Test 2: Checklist Request ===")
response2 = agent("Generate an onboarding checklist for a Software Engineer in the Engineering department")
print(response2)

# Test 3: Scheduling request
print("\n=== Test 3: Scheduling Request ===")
response3 = agent("Create a first-week schedule for someone starting on 2026-09-01")
print(response3)
from strands import Agent
from tools.hr_qa_wrapper import answer_hr_question
from tools.checklist_tool import generate_checklist
from tools.scheduling_tool import generate_schedule
from tools.tracker_tool import log_status, get_employee_tasks, update_task_status, get_all_tasks

agent = Agent(tools=[
    answer_hr_question,
    generate_checklist,
    generate_schedule,
    log_status,
    get_employee_tasks,
    update_task_status,
    get_all_tasks,
])

print("=== Test: Query existing tasks ===")
response = agent("What tasks does Rajesh Kumar have so far?")
print(response)
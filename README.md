# oboardops

> **AI agent for employee onboarding automation**
> *Agents for Humans Hackathon*

## 🎯 Problem Statement

Employee onboarding is often fragmented across HR paperwork, IT setup, meeting schedules, team introductions, company policies, and role-specific tasks.

For a new employee, this can make it difficult to understand **what needs to be done, when it needs to be done, and who is responsible for it**. At the same time, HR teams and managers spend valuable time coordinating onboarding activities and answering repetitive questions.

This fragmented process can lead to missed tasks, unclear ownership, scattered information, and a less consistent first-week experience.

**oboardops aims to make employee onboarding organized, transparent, and easier to navigate by bringing essential onboarding tasks, responsibilities, schedules, and information into one experience.**

---

## 💡 Our Approach

oboardops is being developed as an AI-assisted onboarding experience that helps organize the information and activities involved in bringing a new employee into a team.

The project brings together key onboarding areas such as:

* 📄 **Paperwork & HR requirements**
* 💻 **IT and account setup**
* 📅 **First-week schedules**
* 👋 **Team and cross-functional introductions**
* 📋 **Onboarding tasks and ownership**
* ❓ **HR policy questions and answers**

The goal is to reduce the friction between **"I don't know what I need to do"** and **"I know exactly what my next onboarding step is."**

---

## 👥 Who It's For

### 👩‍💼 HR Teams

HR teams can use oboardops to organize onboarding information, policies, tasks, and responsibilities in a centralized experience.

### 🧑‍💻 New Employees

New employees get a clearer understanding of their onboarding journey, including what they need to complete, what happens during their first week, and where to find important information.

### 👨‍💼 Managers & Team Leads

Managers and team leads can gain better visibility into onboarding activities, assigned responsibilities, progress, and upcoming tasks for new team members.

---

## 📅 First-Week Onboarding

A structured first week helps new employees understand the organization, their role, and the people and processes around them.

| Day       | Focus                                                                |
| --------- | -------------------------------------------------------------------- |
| **Day 1** | Welcome, HR introduction, paperwork, IT setup, and team introduction |
| **Day 2** | Role responsibilities, expectations, goals, and team tools           |
| **Day 3** | Cross-functional introductions and key team processes                |
| **Day 4** | Role-specific training, workflows, and manager check-in              |
| **Day 5** | First-week review, feedback, and Week 2 priorities                   |

See [`first_week_schedule.md`](first_week_schedule.md) for the detailed first-week schedule.

---

## 📋 Onboarding Task Tracking

A core part of the onboarding experience is making responsibilities visible and easy to track.

The onboarding tracker is structured around:

| Employee     | Role | Task            | Status                           | Owner              |
| ------------ | ---- | --------------- | -------------------------------- | ------------------ |
| New employee | Role | Onboarding task | Pending / In Progress / Complete | Responsible person |

This structure helps answer three important questions:

1. **What needs to be done?**
2. **What is the current status?**
3. **Who owns the task?**

---

## ❓ HR Policy Q&A

New employees often have questions about company policies during their first days and weeks.

oboardops includes an HR knowledge base that can be used to organize policy-related questions and answers, helping employees find relevant information without repeatedly relying on HR for common questions.

The current knowledge base is maintained in:

`hr_qa_knowledge_base.json`

The HR Q&A functionality and its tests are located in the `tools/` and test files within this repository.

---

## 🏗️ Project Structure

```text
oboardops/
│
├── tools/
│   └── HR Q&A tools
│
├── first_week_schedule.md
│   └── Day 1–Day 5 onboarding schedule
│
├── hr_qa_knowledge_base.json
│   └── HR policy knowledge base
│
├── test_hr_qa.py
│   └── HR Q&A tests
│
├── README.md
│   └── Project documentation
│
└── LICENSE
```
---

## 🏗️ Design / Architecture

oboardops uses a modular AI-agent architecture where a Strands Agent orchestrates four specialized onboarding tools. Each tool is responsible for a specific part of the onboarding workflow, making the system easier to test, maintain, and extend.

See the [**architecture diagram**](docs/oboardops_architecture.svg) for a visual overview of the system.

### Core Components

#### 1. **Strands Agent (Orchestration Layer)**
Routes onboarding requests to the appropriate specialized tools. All 7 tool functions (HR Q&A, Checklist, Scheduling, and all 4 Tracker functions) are wired into `agent.py`'s `Agent(tools=[...])` — the LLM decides which tool(s) to call for a given request, including chaining multiple tools in a single turn (e.g. generating a checklist, then logging a task from it).

#### 2. **Four Specialized Tools**

- **HR Q&A Tool** — Answers common HR policy questions using fuzzy matching against `hr_qa_knowledge_base.json`. Covers leave, benefits, reimbursement, employment terms, and more.

- **Checklist Tool** — Generates a personalized, 5–7 item onboarding checklist based on the employee's role and department, via a live call to Claude (Amazon Bedrock) with Pydantic-validated structured output and a grounded Indian HR compliance reference. See [Technical Implementation](#-technical-implementation-the-checklist-tool) below for how this works.

- **Scheduling Tool** — Generates a structured first-week onboarding schedule based on the employee's start date. Provides a day-by-day agenda (Days 1–5) with meetings, activities, and milestones.

- **Tracker Tool** — Records, updates, and retrieves onboarding tasks with four core functions:
  - `log_status()` — Log a new onboarding task with employee name, role, task, status, and owner
  - `get_employee_tasks()` — Retrieve all tasks assigned to a specific employee
  - `update_task_status()` — Update the status of an existing task (Not Started, In Progress, Completed, Blocked)
  - `get_all_tasks()` — View all onboarding tasks across all employees
  
  **Status:** Mocked tests pass 4/4 (`test_tracker.py`). Live Google Sheets testing has also been verified (`test_tracker_functions.py`, 3/3 PASS) — `credentials.json` itself is a per-developer service-account secret and intentionally not committed to the repo (see [SETUP_GOOGLE_SHEETS.md](SETUP_GOOGLE_SHEETS.md)).

#### 3. **Google Sheets**
Shared task tracking sheet with columns:
- Employee
- Role
- Task
- Status (Pending / In Progress / Completed)
- Owner (IT, HR, Manager, Admin, etc.)

**Note:** Live integration requires a per-developer `credentials.json` — see [SETUP_GOOGLE_SHEETS.md](SETUP_GOOGLE_SHEETS.md) for setup instructions. Both mocked (`test_tracker.py`) and live (`test_tracker_functions.py`) test evidence exist; the credentials file itself is gitignored by design, so a fresh clone runs mocked-only until that file is added locally.

#### 4. **HR / Manager Visibility**
Task status dashboard showing:
- Pending tasks
- In-progress work
- Completed milestones
- Task ownership and accountability

### Tool Flow

```text
          Employee Request
               |
               v
       Strands Agent
    (Orchestration Layer)
               |
    +----------+---------+---------+
    |          |         |         |
    v          v         v         v
  HR Q&A    Checklist  Scheduling  Tracker
   Tool      Tool       Tool       Tool
    |          |         |         |
    +----------+---------+---------+
               |
               v
         Google Sheets
      (Task & Status Backend)
               |
               v
    HR/Manager Visibility
```

---

## 🔧 Technical Implementation: The Checklist Tool

*This section explains **how** the Checklist Tool works under the hood, since it does the most "AI reasoning" work of the four tools.*

### The flow

1. A caller (the agent, or a test script) provides a `role` and `department` — e.g. `"Software Engineer"`, `"Engineering"`.
2. These get filled into a prompt template. Separately, a system prompt frames the model as an onboarding specialist and forbids generic filler items ("get an ID badge") unless genuinely department-specific.
3. That system prompt also carries the full text of a maintained reference on Indian labour law (see "Compliance skill reference" below).
4. Both are sent to Claude, running on Amazon Bedrock, via the [Strands Agents](https://github.com/strands-agents) framework — the same framework powering every other tool in OnboardOps.
5. Instead of just asking for free text and hoping it comes back as a clean list, the call uses **Pydantic structured output** so the result is validated before it's ever turned into a checklist.

### Why Pydantic structured output, in plain terms

A plain LLM call just returns text — if you ask for "5 to 7 checklist items," nothing stops the model from returning 3, or 12, or a paragraph of prose instead of a list. That's tolerable for a chatbot, but risky for a tool whose output other tools (like the Tracker) might need to consume.

**Structured output** fixes this by giving the model a schema to fill in, instead of free text:

```python
class _OnboardingChecklist(BaseModel):
    role: str
    department: str
    items: list[str] = Field(min_length=5, max_length=7)
```

The model's response has to fit this shape — `role`, `department`, and an `items` list with *between 5 and 7* entries — or the call fails validation instead of silently shipping something malformed (the tool then returns a clear `"Unexpected error: ..."` string, rather than a broken checklist). In practice, every successful call to `generate_checklist()` returns exactly 5–7 items, every time, without the calling code needing to sanity-check the model's output itself. That reliability is also why it was safe to build the checklist→tracker bridging work on top of it (see `KNOWN_ISSUES.md` and `e2e/test_checklist_tracker_bridge.py`) — the *shape* of the output was never in question, only how long each item's text turned out to be.

### Compliance skill reference, in plain terms

Ask an LLM "what form does an Indian employee fill out for provident fund enrollment?" and it might answer confidently — and be wrong, or out of date. The Checklist Tool doesn't rely on the model's own memory for anything statutory.

Instead, the system prompt includes the full text of [`.claude/skills/indian-hr-compliance/SKILL.md`](.claude/skills/indian-hr-compliance/SKILL.md) — a maintained reference covering the Indian Labour Codes, the POSH Act, EPF/ESI, gratuity, and the Shops & Establishments Act, complete with real form names and current-as-of-writing thresholds. The model is instructed to ground any compliance-related item in *this* text, and to phrase numeric thresholds as "commonly ₹X — verify current figure" rather than asserting them as immutable fact, since those numbers legitimately change over time.

**Example of what this actually produces** (real generated output, not illustrative):

> *"Submit PAN, Aadhaar, and EPF Form 11 (declaration of prior PF membership/UAN) to HR, and complete ESI KYC if your gross monthly wage falls within the notified ceiling (commonly ₹21,000/month — verify current figure), so statutory enrollments are processed before your first payroll cycle."*

That names a real form ("EPF Form 11"), a real scheme ("ESI KYC"), and hedges the one number in it — that specificity comes directly from the injected reference, not from the model improvising.

### It generalizes beyond Engineering

Every example above happens to be Engineering-flavored, so it's worth showing the tool actually adapts rather than reusing one template. Here's the same tool, same prompt template, same compliance reference — just a different `role`/`department` — for **Sales Manager, Sales**:

> *"Meet with the VP of Sales and your direct reports within the first week to align on current quota attainment, territory/account mapping, deal-review cadence, and the Q-end forecast commitments you are inheriting."*
>
> *"Audit the active pipeline in the CRM for your assigned territory — flagging deals lacking next steps, close-date hygiene issues, or stalled stages — and present a prioritized action plan to the VP of Sales by end of Week 2."*

There's no repo cloning, no CI/CD access request, no code review here — a Software Engineer checklist is full of exactly that, and none of it. Instead this one is pitched at a *manager* (direct reports, VP alignment, quota inheritance) rather than an individual contributor. The statutory items (PAN/Aadhaar/EPF/POSH) still show up, correctly, regardless of role — but everything else about the checklist is genuinely role- and seniority-specific, not a reskinned template.

---

## 📚 Documentation

- **[Architecture Diagram](docs/oboardops_architecture.svg)** — Visual overview of the OnboardOps system components and data flow
- **[Demo Video Script](docs/demo_video_script.md)** — Full hackathon demo script (3:30–3:45) with speaker notes, visual cues, and calibrated timing
- **[Final Recording Plan](docs/recording_plan.md)** — Master video recording timeline, checklist, and quality control plan for Shruthika
- **[First-Week Schedule](first_week_schedule.md)** — Structured Day 1–5 onboarding agenda
- **[Google Sheets Setup](SETUP_GOOGLE_SHEETS.md)** — Instructions for configuring Google Sheets integration (optional)
- **[End-to-End Test Suite](e2e/README.md)** — Cross-tool checks: does checklist output feed cleanly into the tracker, and how the full agent handles unusual/edge-case prompts

---

## 🚀 Current Progress

### Hackathon Deliverables

* [x] Define the onboarding problem and target users
* [x] Design modular tool architecture with Strands Agent orchestration
* [x] Implement HR Q&A Tool with knowledge base
* [x] Implement Scheduling Tool with first-week schedule
* [x] Implement Tracker Tool with 4 core functions
* [x] Implement Checklist Tool (live Claude call via Amazon Bedrock, Pydantic structured output, Indian HR compliance grounding)
* [x] Wire all 7 tools into the Strands Agent orchestrator (`agent.py`)
* [x] Write and verify mocked unit tests (4/4 tracker tests passing)
* [x] Write and verify cross-tool end-to-end tests (`e2e/`) — checklist output feeding into the tracker, and unusual role/department combos through the full agent
* [x] Create polished architecture diagram
* [x] Write demo video script with live walkthrough
* [x] Document all components and setup instructions

### Known Limitations

- **Tracker task matching**: `update_task_status()` matches tasks by exact (case-insensitive) string equality — there's no task-ID concept, so a checklist-derived task label logged in one turn must be reproduced character-for-character to update it later. See `KNOWN_ISSUES.md` and `e2e/test_checklist_tracker_bridge.py`.
- **Google Sheets credentials**: `credentials.json` is a per-developer secret, intentionally gitignored — a fresh clone runs the Tracker Tool's mocked tests only until that file is added locally (see `SETUP_GOOGLE_SHEETS.md`).
- **Checklist Tool model access**: the team's AWS account currently has Bedrock access to `claude-sonnet-4-6`; the newer Claude Opus/Sonnet 5 tier isn't enabled on this account yet.

---

## 🎯 Vision

**Make onboarding feel less like a pile of tasks and more like a guided journey.**

oboardops is designed to help employees know **what to do, when to do it, and where to find the information they need**, while giving HR teams and managers better visibility into the onboarding process.

---

## 🛠️ Hackathon

Built for the **Agents for Humans Hackathon** with a focus on using AI to make employee onboarding more organized, accessible, and human-friendly.

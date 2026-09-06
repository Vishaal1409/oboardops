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
Routes onboarding requests to the appropriate specialized tools. Currently a bare-bones orchestrator — tools are not yet wired into agent.py but the integration points are ready.

#### 2. **Four Specialized Tools**

- **HR Q&A Tool** — Answers common HR policy questions using fuzzy matching against `hr_qa_knowledge_base.json`. Covers leave, benefits, reimbursement, employment terms, and more.

- **Checklist Tool** — Generates a personalized onboarding checklist based on the employee's role and department. *Currently a placeholder implementation ("coming soon").*

- **Scheduling Tool** — Generates a structured first-week onboarding schedule based on the employee's start date. Provides a day-by-day agenda (Days 1–5) with meetings, activities, and milestones.

- **Tracker Tool** — Records, updates, and retrieves onboarding tasks with four core functions:
  - `log_status()` — Log a new onboarding task with employee name, role, task, status, and owner
  - `get_employee_tasks()` — Retrieve all tasks assigned to a specific employee
  - `update_task_status()` — Update the status of an existing task (Not Started, In Progress, Completed, Blocked)
  - `get_all_tasks()` — View all onboarding tasks across all employees
  
  **Status:** Mocked tests pass 4/4. Backend is Google Sheets (credentials.json not configured for live testing).

#### 3. **Google Sheets**
Shared task tracking sheet with columns:
- Employee
- Role
- Task
- Status (Pending / In Progress / Completed)
- Owner (IT, HR, Manager, Admin, etc.)

**Note:** Live integration test requires `credentials.json` — see [SETUP_GOOGLE_SHEETS.md](SETUP_GOOGLE_SHEETS.md) for setup instructions. Current test evidence uses mocked Google Sheets.

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

## � Documentation

- **[Architecture Diagram](docs/oboardops_architecture.svg)** — Visual overview of the OnboardOps system components and data flow
- **[Demo Video Script](docs/demo_video_script.md)** — Full hackathon demo script (3–5 minutes) with speaker notes and screen cues
- **[First-Week Schedule](first_week_schedule.md)** — Structured Day 1–5 onboarding agenda
- **[Google Sheets Setup](SETUP_GOOGLE_SHEETS.md)** — Instructions for configuring Google Sheets integration (optional)

---

## 🚀 Current Progress

### Hackathon Deliverables

* [x] Define the onboarding problem and target users
* [x] Design modular tool architecture with Strands Agent orchestration
* [x] Implement HR Q&A Tool with knowledge base
* [x] Implement Scheduling Tool with first-week schedule
* [x] Implement Tracker Tool with 4 core functions
* [x] Add Checklist Tool (placeholder implementation)
* [x] Write and verify mocked unit tests (4/4 tracker tests passing)
* [x] Create polished architecture diagram
* [x] Write demo video script with live walkthrough
* [x] Document all components and setup instructions

### Known Limitations

- **Checklist Tool**: Currently placeholder ("coming soon"). Full personalization by role/department not yet implemented.
- **Google Sheets Integration**: Live testing requires `credentials.json` — not configured for this hackathon. Mocked tests verify all 4 Tracker functions work correctly.
- **Agent Orchestration**: Strands Agent is bare-bones. Tool integration points are ready but tools are not yet wired into agent.py.

---

## 🎯 Vision

**Make onboarding feel less like a pile of tasks and more like a guided journey.**

oboardops is designed to help employees know **what to do, when to do it, and where to find the information they need**, while giving HR teams and managers better visibility into the onboarding process.

---

## 🛠️ Hackathon

Built for the **Agents for Humans Hackathon** with a focus on using AI to make employee onboarding more organized, accessible, and human-friendly.

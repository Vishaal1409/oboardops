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

oboardops uses a modular AI-agent architecture where a central agent orchestrates specialized onboarding tools. Each tool is responsible for a specific part of the onboarding workflow, making the system easier to test, maintain, and extend.

### Core Components

- **Agent Orchestrator** — Receives the employee's request and determines which onboarding tool should handle it.
- **HR Q&A Tool** — Answers common HR policy questions using the HR knowledge base.
- **Checklist Tool** — Generates a personalized onboarding checklist based on the employee's role and department.
- **Scheduling Tool** — Generates a structured first-week onboarding schedule based on the employee's start date.
- **Tracker Tool** — Records onboarding tasks and their status in the shared tracking system.

### Tool Flow

```text
                         Employee Request
                                |
                                v
                       Agent Orchestrator
                                |
              +-----------------+-----------------+
              |                 |                 |
              v                 v                 v
         HR Q&A Tool      Checklist Tool    Scheduling Tool
              |                 |                 |
              v                 v                 v
       HR Knowledge Base    Role + Department   Start Date
                                |                 |
                                v                 v
                           Personalized      First-Week
                            Checklist         Schedule
                                |
                                +--------+--------+
                                         |
                                         v
                                  Onboarding Output
                                         |
                                         v
                                  Tracker Tool
---

## 🚀 Current Progress

### Week 1

* [x] Define the onboarding problem
* [x] Identify primary users
* [x] Structure the first-week onboarding schedule
* [x] Establish HR policy Q&A knowledge base
* [x] Set up initial HR Q&A tooling and tests
* [ ] Continue integrating onboarding workflow components

### Week 2

Planned focus includes:

* Connecting onboarding information into a unified workflow
* Improving the employee onboarding experience
* Integrating task tracking and ownership
* Expanding HR policy Q&A
* Testing the end-to-end onboarding flow

---

## 🎯 Vision

**Make onboarding feel less like a pile of tasks and more like a guided journey.**

oboardops is designed to help employees know **what to do, when to do it, and where to find the information they need**, while giving HR teams and managers better visibility into the onboarding process.

---

## 🛠️ Hackathon

Built for the **Agents for Humans Hackathon** with a focus on using AI to make employee onboarding more organized, accessible, and human-friendly.

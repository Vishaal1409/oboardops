# OnboardOps Demo Video Script
## AI-Assisted Employee Onboarding — Hackathon Demo (3–5 minutes)

---

## 1. OPENING / PROBLEM (30 seconds)

[SCREEN: Show fragmented onboarding documents — emails, spreadsheets, forms, calendar invites]

**Speaker:**

"Onboarding a new employee is a critical moment — but it's usually broken into fragments. New employees juggle HR paperwork, IT setup, meeting schedules, policy questions, and role-specific tasks. Meanwhile, HR teams and managers spend hours coordinating handoffs and answering repetitive questions.

The result? Missed tasks. Unclear ownership. Scattered information. And a frustrating experience for everyone involved."

[SCREEN: Fade to title]

"What if onboarding could be organized, transparent, and simple? That's OnboardOps."

---

## 2. WHO IT'S FOR (20 seconds)

[SCREEN: Three personas appear — Employee, HR, Manager]

**Speaker:**

"OnboardOps is built for three groups:

**New employees** — who need clarity on what to do, when to do it, and who to ask for help.

**HR teams** — who manage policies, tasks, and coordination across the entire onboarding journey.

And **managers and team leads** — who need visibility into progress and when their new direct report will be ready to contribute."

---

## 3. SOLUTION — THE FOUR TOOLS (45 seconds)

[SCREEN: Show the four tool icons/boxes from the architecture diagram]

**Speaker:**

"OnboardOps brings together four specialized tools:

**First, the HR Q&A Tool.** New employees often have questions about company policies, benefits, leave, or reimbursement. Instead of asking HR repeatedly, they can search a knowledge base that answers common questions instantly.

**Second, the Checklist Tool.** Onboarding isn't one-size-fits-all. Different roles and departments need different checklists. This tool generates a personalized checklist so employees know exactly what they need to complete.

**Third, the Scheduling Tool.** We've structured the first week into a five-day agenda — welcome, role intro, team meetings, training, and a review. This gives new employees a clear roadmap of their first week.

**And finally, the Tracker Tool.** Every onboarding task has an owner, a status, and a deadline. The Tracker logs, updates, and displays tasks in real time so everyone knows what's happening."

---

## 4. ARCHITECTURE (30 seconds)

[SCREEN: Show the architecture diagram]

**Speaker:**

"Under the hood, these four tools are orchestrated by a Strands Agent. Think of the Agent as the traffic controller — it routes onboarding requests to the right tool, integrates the responses, and makes sure nothing falls through the cracks.

Each tool is modular and independent. If you need to add a tool, update a tool, or swap a tool, you can do it without affecting the others.

All task data flows into a shared Google Sheet — giving HR and managers a live view of who's doing what and when."

---

## 5. LIVE DEMO WALKTHROUGH (90 seconds)

[SCREEN: Show the Tracker Tool demo data on screen]

**Speaker:**

"Let me show you how this works. Meet Rajesh Kumar — a new Software Engineer joining our team today.

[SCREEN: Display Rajesh's task table]

In our tracker, we have two tasks logged for Rajesh:

**Task 1:** 'Laptop provisioned'
- Status: Completed ✅
- Owner: IT

**Task 2:** 'HR orientation scheduled'
- Status: In Progress 🔵
- Owner: HR

Here's what our tracker can do:

**[1] Log a new task** — When IT finishes provisioning Rajesh's laptop, they log it into the tracker with a status and owner.

**[2] Retrieve tasks** — If Rajesh needs to know what he's got to do today, we can pull up all his tasks at once.

**[3] Update a task status** — As Rajesh completes onboarding activities, we update the status from 'In Progress' to 'Completed'.

**[4] View all tasks** — HR and managers can see the entire onboarding pipeline — across all new employees.

The mocked tests in our repository verify all four of these functions work correctly. We've demonstrated this with Rajesh's data.

[SCREEN: Show the test results — 4/4 passing]

The tracker is designed to use a shared Google Sheet as its backend, making it easy for HR and managers to stay in sync without needing a separate app."

---

## 6. WHY IT MATTERS (20 seconds)

[SCREEN: Show the benefits checklist]

**Speaker:**

"Why does this matter?

**Clear ownership** — Everyone knows who's responsible for each task.

**Easier progress visibility** — No more 'Is the new hire ready?' — just check the tracker.

**Less manual coordination** — HR isn't chasing IT or Finance to find out status updates.

**A better experience** — New employees feel organized, supported, and ready to contribute.

That's the power of a centralized, modular onboarding workflow."

---

## 7. CLOSING (20 seconds)

[SCREEN: Back to title slide with logo]

**Speaker:**

"OnboardOps shows how AI agents can simplify the messy, fragmented parts of running a business. Instead of scattered spreadsheets and emails, you get a organized, intelligent workflow.

It's modular. It scales. And it puts the focus back on what matters — helping new people succeed.

This is OnboardOps. Let's bring onboarding into the 21st century.

Thanks."

[SCREEN: Fade out]

---

## TIMING NOTES

- **Opening**: 30 seconds
- **Who it's for**: 20 seconds
- **Solution**: 45 seconds
- **Architecture**: 30 seconds
- **Demo walkthrough**: 90 seconds
- **Why it matters**: 20 seconds
- **Closing**: 20 seconds

**Total: ~255 seconds (4 minutes 15 seconds)**

Feel free to add pauses, emphasis, or ad-libs during the spoken demo. The script is designed to be natural and conversational.
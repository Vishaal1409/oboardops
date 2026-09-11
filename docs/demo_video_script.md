# OnboardOps Final Demo Video Script
## AI-Assisted Employee Onboarding — Hackathon Final Video Script

**Target Duration:** 3:30 – 3:45 (210s – 225s)  
**Maximum Limit:** 4:15 – 5:00  
**Safety Buffer:** 40 – 85 seconds  
**Speaker:** Shruthika  
**Status:** LOCKED (Calibrated against Sept 10 Rough Trial Recording)

---

## TIMING & SECTION OVERVIEW

| Section | Target Duration | Cumulative Timestamp | Screen / Visual Cue |
| :--- | :--- | :--- | :--- |
| **1. Opening / Problem** | 25s | `00:00 – 00:25` | Title slide & fragmented onboarding artifacts |
| **2. Who It's For** | 20s | `00:25 – 00:45` | Three Persona Cards (Employee, HR, Manager) |
| **3. Solution (The Four Tools)** | 40s | `00:45 – 01:25` | Architecture tool overview (4 core modules) |
| **4. Architecture & Agent** | 25s | `01:25 – 01:50` | `oboardops_architecture.svg` diagram |
| **5. Live Demo Walkthrough** | 70s | `01:50 – 03:00` | Terminal running `python test_tracker.py` + Rajesh Kumar data |
| **6. Why It Matters (Value)** | 20s | `03:00 – 03:20` | Key Benefits visual checklist |
| **7. Closing & Next Steps** | 15s | `03:20 – 03:35` | Final slide with repo & logo |

---

## FULL SPOKEN SCRIPT & DEMO CUES

### 1. OPENING / PROBLEM (25 seconds)

**Timestamp:** `00:00 – 00:25`  
**Visual Cue:** [SCREEN: Start on Title Slide with OnboardOps logo, then transition to a split screen showing scattered onboarding documents — email drafts, messy spreadsheets, forms, and calendar invites.]

**Speaker:**
> "Onboarding a new employee is a critical milestone — but in most companies, it's fragmented across emails, spreadsheets, and scattered forms.
>
> New hires struggle to know what to do next, while HR teams and managers waste hours answering repetitive questions and tracking down task updates.
>
> What if employee onboarding was organized, transparent, and intelligent from day one? That's **OnboardOps**."

---

### 2. WHO IT'S FOR (20 seconds)

**Timestamp:** `00:25 – 00:45`  
**Visual Cue:** [SCREEN: Display three clean persona cards: **New Employee** 🧑‍💻, **HR Teams** 👩‍💼, and **Managers** 👨‍💼.]

**Speaker:**
> "OnboardOps connects the three key stakeholders in any onboarding journey:
>
> First, **New Employees** — who get total clarity on their first-week roadmap and daily tasks.
>
> Second, **HR Teams** — who automate policy Q&A and manage compliance effortlessly.
>
> And third, **Managers** — who get real-time visibility into when their direct hire is ready to contribute."

---

### 3. SOLUTION — THE FOUR TOOLS (40 seconds)

**Timestamp:** `00:45 – 01:25`  
**Visual Cue:** [SCREEN: Show the four core tool modules from the system architecture.]

**Speaker:**
> "OnboardOps brings together four specialized AI tools:
>
> **1. HR Q&A Tool:** Answers company policy, leave, and benefit questions instantly using grounded fuzzy matching.
>
> **2. Checklist Tool:** Generates role-tailored checklists validated with Pydantic and grounded in Indian HR compliance.
>
> **3. Scheduling Tool:** Structures the first week into a five-day agenda with clear daily milestones.
>
> **4. Tracker Tool:** Logs, updates, and retrieves task statuses in real time, assigning clear owners and deadlines."

---

### 4. ARCHITECTURE & STRANDS AGENT (25 seconds)

**Timestamp:** `01:25 – 01:50`  
**Visual Cue:** [SCREEN: Display `docs/oboardops_architecture.svg` highlighting the central Strands Agent.]

**Speaker:**
> "Under the hood, these four tools are orchestrated by a central **Strands Agent**. The agent acts as an intelligent controller, routing requests and chaining tools seamlessly when an employee needs multiple actions at once.
>
> All task state is structured to synchronize with a shared Google Sheet backend — keeping HR, IT, and managers updated without building a complex custom app."

---

### 5. LIVE DEMO WALKTHROUGH (70 seconds)

**Timestamp:** `01:50 – 03:00`  
**Visual Cue:** [SCREEN: Switch to VS Code terminal positioned at repo root. Run `python test_tracker.py`.]

**Speaker:**
> "Let's see this in action with a real onboarding profile — meet **Rajesh Kumar**, a new Software Engineer.
>
> I'll run our tracker test suite to demonstrate all four core tracker operations:
>
> [ACTION: Execute `python test_tracker.py` in terminal. Show 4 passing tests.]
>
> As you can see, all 4 tracker functions execute and pass in under 0.01 seconds:
>
> **1. Log Task:** IT logs Rajesh's 'Laptop provisioned' task as *Completed*.  
> **2. Retrieve Employee Tasks:** Pulls Rajesh's full onboarding pipeline.  
> **3. View All Tasks:** Gives HR a consolidated view across all active new hires.  
> **4. Update Task Status:** Updates 'HR Orientation' from *In Progress* to *Completed*.
>
> [SCREEN: Bring up the simple summary table of Rajesh's sample tasks.]
>
> These verified unit tests prove the core tracker logic is ready to sync live with our Google Sheets backend structure."

---

### 6. WHY IT MATTERS (20 seconds)

**Timestamp:** `03:00 – 03:20`  
**Visual Cue:** [SCREEN: Show slide with 4 value-add checkmarks: **Clear Ownership**, **Real-Time Visibility**, **Less Manual Coordination**, **Elevated Hire Experience**.]

**Speaker:**
> "Why does OnboardOps matter?
>
> **Clear Ownership:** Every single task has a named owner — HR, IT, or Manager.  
> **Real-Time Visibility:** Managers check progress in seconds without bothering HR.  
> **Less Friction:** New hires feel supported, empowered, and productive from Day 1."

---

### 7. CLOSING & CALL TO ACTION (15 seconds)

**Timestamp:** `03:20 – 03:35`  
**Visual Cue:** [SCREEN: Return to OnboardOps title slide with GitHub link and 'Agents for Humans Hackathon 2026'.]

**Speaker:**
> "OnboardOps shows how AI agents transform fragmented administrative overhead into a unified, human-centric onboarding journey.
>
> Built for the Agents for Humans Hackathon. Thank you!"

[SCREEN: Fade out to black]

---

## TIMING CALIBRATION & TRIAL RECORDING LESSONS

1. **Eliminated Overruns:** The trial take ran ~4:15–4:40 due to repetitive dialogue during the demo section. We tightened the demo section from 90s to 70s by pointing directly at test outputs instead of re-reading raw data line by line.
2. **Terminal Preparation:** Always pre-type `python test_tracker.py` or clear the terminal prior to recording so there is zero command-line lag.
3. **Pacing Guardrails:** Keep spoken speed between 130–145 words per minute. Pauses between sections should be strictly 1 second.
4. **Emergency Trim Options (If Spoken Slow):**
   - Skip Section 3 detailed sub-descriptions (saves 12s).
   - Combine Section 6 benefits into two quick phrases (saves 8s).
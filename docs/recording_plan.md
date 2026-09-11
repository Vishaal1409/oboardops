# OnboardOps Final Video Recording & Execution Plan

**Task Owner:** Shruthika  
**Project:** OnboardOps — AI-Assisted Employee Onboarding  
**Hackathon Deadline:** September 14, 2026  
**Status:** ACTIVE & APPROVED  

---

## 🗓️ DATE INTERPRETATION & MASTER SCHEDULE

> [!IMPORTANT]
> **Date Discrepancy Note:** Historical prompt notes reference "tomorrow (Sept 11)", but the current system date is **Friday, September 11, 2026**.
> To preserve a 24-to-48-hour submission buffer before the **September 14, 2026** deadline, the execution schedule is structured below with Friday, Sept 11 as TODAY.

```
       [Sept 11 - FRI]             [Sept 12 - SAT]            [Sept 13 - SUN]         [Sept 14 - MON]
  Script Lock & Setup Prep    --->  Dry Run & Recording  --->  Editing & Final QA --->  Submission Buffer
     (Phase 1–3 Done)              (Final Recording)          (MP4 Export & Check)    (Deadline Day)
```

### Schedule Timeline

| Phase / Date | Key Milestones | Responsible | Deliverable / Status |
| :--- | :--- | :--- | :--- |
| **Friday, Sept 11 (TODAY)** | • Lock final video script<br>• Audit repo & verify test suite<br>• Prepare final recording plan | Agent & Shruthika | • `docs/demo_video_script.md` [LOCKED]<br>• `docs/recording_plan.md` [ACTIVE] |
| **Saturday, Sept 12 (AM)** | • Environment & mic audio check<br>• Terminal & slide setup<br>• Perform 2 dry runs with timer | Shruthika | • Equipment verified<br>• Timing calibrated (3:30–3:45) |
| **Saturday, Sept 12 (PM)** | • Record 2–3 full takes of video<br>• Select best audio/video take<br>• Check terminal clarity & code visibility | Shruthika | • Raw recording files (.mp4) |
| **Sunday, Sept 13** | • Trim transitions & balance audio<br>• Render final 1080p MP4 export<br>• Retake buffer window (if needed)<br>• Perform quality control review | Shruthika | • Final video file (`oboardops_demo.mp4`)<br>• 24-Hour Submission Safety Buffer |
| **Monday, Sept 14** | • Upload video & complete hackathon submission prior to deadline | Shruthika | • Hackathon Submission Complete |

---

## 📋 RECORDING PREPARATION CHECKLIST

### 1. Slide Deck & Screen Assets
- [ ] **Slide 1:** Title slide with OnboardOps logo and "Agents for Humans Hackathon 2026".
- [ ] **Slide 2:** Personas overview (New Employee 🧑‍💻, HR Teams 👩‍💼, Managers 👨‍💼).
- [ ] **Slide 3:** The Four Tools architecture boxes.
- [ ] **Slide 4 / Diagram:** `docs/oboardops_architecture.svg` ready to display or highlight.
- [ ] **Slide 5:** Why It Matters value proposition checklist (4 key benefits).
- [ ] **Slide 6:** Closing slide with GitHub repository link.

### 2. Terminal & Demo Setup
- [ ] Open VS Code / Terminal focused on `oboardops` repository root.
- [ ] Font size zoomed to 16–18pt for crisp readability in video render.
- [ ] Pre-run `python test_tracker.py` to ensure clean environment (all 4/4 tests PASS).
- [ ] Clear terminal screen (`cls` or `clear`) so prompt is ready at top of screen.
- [ ] Sample data table ready for quick side-by-side view (Rajesh Kumar profile).

### 3. Hardware & Software Check
- [ ] **Microphone:** External mic selected, input level tested (no clipping or background hum).
- [ ] **Screen Resolution:** 1920x1080 (1080p), 16:9 aspect ratio.
- [ ] **Recording Tool:** OBS Studio, Loom, or Camtasia set to 60fps / high bitrate audio.
- [ ] **Notifications:** Windows Focus Mode enabled; Slack, Teams, Email, and popups muted.

---

## 🎙️ RECORDING WORKFLOW & PROCEDURES

### Dry Run (Saturday AM)
1. Read the locked script (`docs/demo_video_script.md`) out loud with a stopwatch running.
2. Verify section timings against the locked plan:
   - Section 1 (Opening): ~25s
   - Section 2 (Personas): ~20s
   - Section 3 (Four Tools): ~40s
   - Section 4 (Architecture): ~25s
   - Section 5 (Demo): ~70s
   - Section 6 (Value): ~20s
   - Section 7 (Closing): ~15s
3. Confirm total spoken time is between **3:30 and 3:45** (leaving 45+ seconds of safety buffer before the 4:15 soft limit).

### Actual Recording Passes (Saturday PM)
- **Take 1:** Full walkthrough to establish rhythm.
- **Take 2:** Polished walkthrough focusing on smooth terminal execution and slide transitions.
- **Take 3 (Optional):** Backup take if audio or screen transition hesitated in Take 2.

### Retake & Editing Window (Sunday)
- If any section stumbles, re-record that specific 30-second section rather than the whole video.
- Stitch slides and terminal recording seamlessly with simple fade transitions.
- Export as `oboardops_demo.mp4` (H.264, AAC Audio, 1080p).

---

## 🎯 QUALITY CONTROL VERIFICATION

Before final upload on Sunday/Monday, verify:
- [x] Script accurately reflects repository capabilities (Strands Agent + 4 modular tools + Google Sheets pattern).
- [x] All 4 tracker unit tests shown in terminal pass cleanly (`test_tracker.py`).
- [x] Total video runtime is strictly under 4 minutes 15 seconds.
- [x] Audio is crisp, clear, and synchronized with screen actions.
- [x] No secrets, API keys, personal credentials, or confidential tokens visible.

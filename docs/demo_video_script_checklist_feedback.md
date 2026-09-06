# Feedback on `demo_video_script.md` — Checklist Tool coverage

Reviewed `docs/demo_video_script.md` against the current state of the Checklist Tool (live Claude call via Amazon Bedrock, Pydantic structured output, Indian HR compliance grounding — see the README's "Technical Implementation" section). Not editing the script directly since it's your recording script — here's what I found, for you to fold in as you see fit.

## What's already accurate

Section 3 ("Solution — The Four Tools") describes the Checklist Tool correctly and doesn't call it a placeholder:

> "Second, the Checklist Tool. Onboarding isn't one-size-fits-all. Different roles and departments need different checklists. This tool generates a personalized checklist so employees know exactly what they need to complete."

No change needed there.

## The gap

Section 5 ("Live Demo Walkthrough," ~90 seconds) is the only place the script shows something running live on screen — and it **only demos the Tracker Tool** (Rajesh Kumar's two hardcoded tasks, log/retrieve/update/view-all). The Checklist Tool is described in Section 3 but never actually demonstrated. Given it's the tool doing the most "AI reasoning" work — a real Claude call, grounded in a maintained Indian labour-law reference, producing a different checklist for every role/department — it's arguably the most demo-worthy moment in the whole product, and it's currently invisible in the walkthrough.

Two related, smaller things worth knowing if you touch this section:
- The `README.md`'s "Current Progress"/"Known Limitations" sections used to describe the Checklist Tool as a placeholder and the agent as "not yet wired" — both were stale as of today and have been corrected (checklist tool is fully live via Bedrock; all 7 tools, including the 3 tracker query functions, are wired into `agent.py`).
- The live walkthrough's "mocked tests... 4/4 passing" framing is still accurate for `test_tracker.py`, but there's now also a live pass (`test_tracker_functions.py`, 3/3) and a new `e2e/` suite verifying checklist output feeds cleanly into the tracker — worth a mention if you want to emphasize how thoroughly this was tested, not required otherwise.

## Suggested addition (drop-in optional)

If you want to add a Checklist Tool beat to Section 5, here's a proposed insert — timed to fit inside the existing 90-second walkthrough budget without needing to renegotiate the other section timings much (maybe trims a few seconds from the Tracker portion, since "view all tasks" could be shown faster):

---

**[SCREEN: Show a role/department input, e.g. "Software Engineer, Engineering"]**

**Speaker:**

"Before we look at the tracker, let's see the Checklist Tool actually generate something. I'll ask for a checklist for a new Software Engineer joining Engineering..."

**[SCREEN: Show the generated checklist — 5 to 7 items, e.g.:]**

- Submit PAN, Aadhaar, and EPF Form 11 to HR; complete ESI KYC if applicable
- Clone the team's repositories and get your local dev environment running
- Request access to core engineering tools — CI/CD, cloud console, project board
- Shadow a senior engineer through one sprint cycle
- Submit your first pull request within two weeks

"Notice this isn't generic advice — it's grounded in real compliance detail. 'EPF Form 11,' 'ESI KYC' — those are actual Indian statutory forms, not something the AI guessed. We built that in deliberately: every checklist is checked against a maintained reference on Indian labour law, so the compliance-related items are accurate, not just plausible-sounding.

**[SCREEN: Show a second checklist for a different role, e.g. "Sales Representative, Sales"]**

And it's genuinely personalized — ask for a Sales Representative instead, and you get CRM setup and territory planning, not a copy-pasted engineering checklist."

---

Total add: roughly 30–40 seconds spoken. If you want to keep the full script at ~4:15, the "view all tasks" beat in the existing Tracker walkthrough (currently its own numbered point) could be trimmed to a single sentence to make room, since "log → retrieve → update" already demonstrates the tracker's core loop without needing all four sub-demos spelled out.

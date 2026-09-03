---
name: indian-hr-compliance
description: Domain reference for Indian labour law, the four Labour Codes, and statutory HR/onboarding compliance (PF, ESI, POSH, gratuity, maternity benefit, Shops & Establishments Act, standing orders). Use when drafting onboarding checklists, offer/appointment letters, HR policies, payroll structures, or compliance audits for India-based employees or entities.
---

# Indian HR & Labour Law Compliance

Reference context for grounding HR work — onboarding checklists, offer letters, policy drafts, payroll structuring, compliance audits — in actual Indian statutory requirements instead of generic (US/UK-flavored) HR boilerplate. This is drafting context, not legal advice: cite it as a starting point and flag that a labour-law counsel or company secretary should verify current thresholds, state-specific rules, and applicability before anything here is treated as final.

**Verify before relying on it**: wage ceilings, contribution rates, and leave entitlements below are commonly-cited figures as of the last update to this file, and central/state governments revise them. Always caveat generated output with "verify current thresholds" rather than presenting numbers as certain.

## 1. The structural shift: four Labour Codes

India has consolidated 29 central labour laws into four Codes, passed 2019–2020. Rollout has been staggered — central rules were notified but the Codes only take effect once a critical mass of states also notify their own rules, so **check current implementation status before assuming the Codes (vs. the older Acts they replace) are what's actually in force** in the relevant state.

| Code | Consolidates | Key HR-relevant provisions |
|---|---|---|
| **Code on Wages, 2019** | Payment of Wages Act, Minimum Wages Act, Payment of Bonus Act, Equal Remuneration Act | Uniform "wages" definition — allowances capped so **at least 50% of total remuneration must count as basic wage**, which raises the PF/gratuity calculation base for CTC structures that previously minimized basic pay. Timely wage payment, floor wage concept, equal pay regardless of gender. |
| **Industrial Relations Code, 2020** | Industrial Disputes Act, Trade Unions Act, Industrial Employment (Standing Orders) Act | Standing Orders (codified service conditions) now mandatory at **300+ workers** (up from 100). Fixed-term employment formally recognized with pro-rata statutory benefits. Layoff/retrenchment notice and government-permission thresholds. |
| **Code on Social Security, 2020** | EPF Act, ESI Act, Maternity Benefit Act, Payment of Gratuity Act, Employees' Compensation Act | Extends social security toward gig/platform workers. Gratuity eligibility for fixed-term employees without the 5-year continuous-service requirement. Retains EPF/ESI/gratuity/maternity benefit structures below with some threshold changes. |
| **Occupational Safety, Health & Working Conditions (OSH) Code, 2020** | Factories Act, Contract Labour Act, Inter-State Migrant Workmen Act | Appointment letter made **mandatory for every employee**. Annual health checkups for notified establishments. Working hours, overtime, leave (calculated on a 240/180-day-worked basis depending on notification), night-shift safeguards for women (with consent + safety conditions).|

## 2. Acts still independently in force (not folded into the Codes)

- **Sexual Harassment of Women at Workplace (Prevention, Prohibition and Redressal) Act, 2013 (POSH Act)** — mandatory Internal Committee (IC) at any office with **10+ employees**; mandatory annual POSH training/awareness; annual IC report; POSH policy must be part of employee handbook and onboarding acknowledgment.
- **Shops and Establishments Act** — **state-specific**, not central. Governs working hours, weekly holidays, leave, and establishment registration for non-factory workplaces (most tech/services/sales offices fall here). Always confirm the specific state's Act (Karnataka, Maharashtra, Delhi, Tamil Nadu, etc. each have their own rules and registration processes) rather than assuming a national standard.
- **Income Tax Act, 1961** — TDS on salary (Section 192), Form 16 issuance annually, Form 12BB investment declarations, PAN mandatory for payroll.
- **Digital Personal Data Protection Act, 2023 (DPDP Act)** — consent requirements for collecting employee personal data (Aadhaar, bank details, health data) during onboarding; data retention and breach-notification obligations for HR systems.
- **Apprentices Act, 1961** — separate stipend/compliance regime for apprentices; do not onboard apprentices under regular-employee checklists.

## 3. Core statutory enrollments at onboarding

| Scheme | Trigger | Employee action | Employer action |
|---|---|---|---|
| **EPF (Provident Fund)** | Mandatory for establishments with 20+ employees; wage ceiling for compulsory coverage commonly cited at ₹15,000/month basic+DA (verify current figure) — many employers still enroll everyone regardless | Submit **Form 11** (declaration of prior PF membership/UAN) | Generate/link UAN, remit employer+employee contribution monthly via EPFO portal |
| **ESI (Employees' State Insurance)** | Establishments with 10+ employees (varies by state), employees earning up to the notified wage ceiling (commonly cited ₹21,000/month, ₹25,000 for persons with disability — verify) | Provide Aadhaar-linked KYC | Register on ESIC portal, issue ESI number, remit contributions |
| **Gratuity** | Applies after 5 years continuous service (Payment of Gratuity Act) — Code on Social Security relaxes this for fixed-term contracts | Submit **Form F** nomination at onboarding, not at exit | Maintain nomination records; statutory ceiling on tax-free gratuity (commonly cited ₹20 lakh — verify) |
| **Professional Tax** | State-levied (not applicable in every state — e.g., not levied in Delhi, Haryana; applies in Karnataka, Maharashtra, West Bengal, etc.) | — | Deduct per state slab, remit to state government |
| **Labour Welfare Fund** | State-specific, small periodic employer+employee contribution | — | Register and remit per state schedule |

## 4. Leave & working-time baselines to check against

Leave entitlements come from whichever of {Factories Act / Shops & Establishments Act (state) / OSH Code once notified} applies to the establishment type — there is no single national annual-leave number. When drafting a leave policy or checklist item, name the governing instrument rather than assuming a flat "X days PTO":

- **Earned/privilege leave**: typically accrues on a worked-days basis (commonly 1 day per ~20 worked days under Factories Act-style formulas).
- **Maternity Benefit Act, 1961 (as amended 2017)**: 26 weeks paid leave for the first two children (12 weeks for the third onward), crèche requirement at 50+ employees, work-from-home option to be explored post-leave where feasible.
- **Paternity leave**: not centrally mandated by statute for private-sector employees (unlike central government employees) — treat as a company policy matter, not a compliance requirement, unless the state/company has its own provision.
- **Weekly holiday + working hours**: Shops & Establishments Act / Factories Act typically cap daily hours (commonly 9/day, 48/week) and mandate at least one weekly off — state-specific overtime multiplier rules apply (commonly 2x for hours beyond the cap).

## 5. Documents & registers HR should be maintaining (auditable)

- Register of employees / wage register / attendance register (format varies by applicable Act)
- POSH Internal Committee register + annual report
- Appointment letters for every employee (now a hard OSH Code requirement, not just best practice)
- Form 16 (annual) and Form 12BB (investment declaration) per employee
- EPF/ESI contribution challans and UAN/ESI number records
- Gratuity nomination (Form F) on file from day one, not collected retroactively
- Standing Orders / certified service rules, once the establishment crosses the applicable worker-count threshold

## 6. How to use this when generating onboarding checklists

When a checklist is being generated for an India-based role, prefer statutory-grounded items over generic ones:

- Replace vague "complete HR paperwork" with named steps: "Submit PAN, Aadhaar, and EPF Form 11 for UAN generation," "Complete ESI KYC if wage is within the notified ceiling," "Acknowledge the POSH policy and Internal Committee contact details."
- Flag state-dependent items explicitly rather than picking one state's rule silently: "Register under the [State] Shops and Establishments Act" rather than naming a specific state unless the role's location is known.
- Distinguish company-policy leave/benefits from statutory-minimum entitlements — don't present a generous company perk as if it were a legal requirement, and vice versa.
- For any numeric threshold (wage ceilings, contribution rates, leave days), phrase output so it reads as "commonly ₹X — confirm current notified figure" rather than asserting a hard number as immutable fact.

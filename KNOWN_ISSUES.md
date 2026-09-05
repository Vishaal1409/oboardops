\# Known Issues — OnboardOps



Tracking minor issues found during testing. None of these are blocking — just things to be aware of or polish if time allows before Sep 14.



\## 1. HR Q\&A tool can match vague questions to overly specific policies

\*\*Found:\*\* Sep 5, 2026 (edge-case testing)

\*\*Details:\*\* Asking a vague question like "tell them about our leave policy" matched to the paternity leave entry instead of the more commonly relevant 21-day annual paid leave policy. Caused by fuzzy text-matching (SequenceMatcher) finding the closest wording match rather than the most contextually relevant one.

\*\*Owner:\*\* Ishitha

\*\*Priority:\*\* Low — not blocking, nice-to-fix if time allows

\*\*Possible fix:\*\* Weight matches toward higher-priority/more common policies when the question is vague, or add default keywords that route generic "leave policy" questions to the main entry.



\## 2. Class-based tools need a wrapper for Strands

\*\*Found:\*\* Aug 30, 2026 (integration testing)

\*\*Details:\*\* Strands requires plain `@tool`-decorated functions, not classes. Ishitha's original HR Q\&A tool (`HRQATool`) was a class, so a wrapper (`tools/hr\_qa\_wrapper.py`) was created to expose it as a simple function.

\*\*Status:\*\* Resolved — pattern documented here in case any future tool runs into the same issue.


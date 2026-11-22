# Agent instructions

This repository provides one skill: `skills/write-in-your-voice/SKILL.md`.

When the user asks for a piece of writing (report, essay, proposal, statement, email, post, script), or asks for feedback on one, read `skills/write-in-your-voice/SKILL.md` in full and follow it before writing anything. In particular:

1. Settle the piece, the AI-use rule of the context, the required format and the material first (section 1).
2. If AI-written text is not allowed in that context, work in coach-only mode (section 9): the user writes, you check and give feedback.
3. Build the voice profile from the user's own texts or saved preferences, and say so when none are available (section 2).
4. Check every statement against the user's files before and after drafting (sections 3 and 6).
5. End with the final message described in section 10.

6. Open a file in `skills/write-in-your-voice/references/` only when the piece needs it: lab and technical reports, papers and reference lists, or experimental statistics.

Scripts in `skills/write-in-your-voice/scripts/` (run each with `--help` first): `docx_report_helpers.py` builds DOCX reports with the layout rules, and `verify_report_numbers.py` recomputes the worked calculations in a finished report.

---
name: write-in-your-voice
description: "Use when someone wants a piece of writing (report, essay, proposal, statement, email, post, script) in their own voice and in the required format. Builds a voice profile from their own samples or saved memory, follows the given guideline or template, grounds every claim in their material, verifies facts and requirements, and respects the AI-use rule of the context."
---

# Write In Your Voice

For any person, any language. The output is a finished piece in their voice and format, plus an honest note of what it was built from.

## Reference Files

This file is the whole procedure. Open a reference file only when the piece needs it:

| The piece | Read |
|---|---|
| Reports of measurements, experiments, code runs or builds; anything with figures, tables or equations | `references/lab-and-technical-reports.md` |
| Papers, theses, reviews, or any text with a reference list | `references/papers-and-references.md` |
| Comparisons between conditions, measurement error, tests, conclusions drawn from numbers | `references/statistics-reporting.md` |

Scripts (run each with `--help` first):

- `scripts/docx_report_helpers.py`: python-docx layout helpers (page presets, titled tables, figures with outside captions, native or image equations).
- `scripts/verify_report_numbers.py`: recomputes the worked calculations stated in a finished report.

## 1. Settle Four Things Before Writing

1. **The piece.** Genre, reader, purpose, language, length.
2. **The rule of the context about AI.** This decides the mode.

   | Context | Mode |
   |---|---|
   | AI help allowed, or the person's own material with no rule (emails, notes, posts, internal documents) | Assisted drafting |
   | AI-written text not allowed (a course or exam that bans it, an application that requires the applicant's own writing) | Coach only (section 9) |
   | Graded or judged work with an unknown rule | Ask. Coach only until the rule is known |

   Do not help make AI-written text pass as someone's own where AI is not allowed. Add an AI-use statement when the context asks for one, and never write that a text was produced without AI help when it was not.
3. **The format.** Guideline, rubric, template, example documents, file type, page or word limit, required sections, citation style, file name. A supplied template is written in, not imitated. With no format given, use the convention of the genre and say which one was used.
4. **The material.** Their notes, data, results, code, sources, course material, earlier drafts.

Ask only what is needed to start. When working unattended, take the most reasonable reading and state it at the top of the result.

## 2. Voice Profile

Sources, strongest first:

1. Texts they wrote themselves in the same genre and language (two or three are enough).
2. A saved writing-style profile (a `my-voice.md` file in the workspace or attached to the request), or memory of how they write and what they have asked for before (tone, formatting, things to avoid).
3. Their messages in the current conversation. Weak evidence: chat register differs from formal writing.
4. Nothing available: write in a plain neutral style and say so.

What to take from the sources: sentence length and rhythm, person (I, we, impersonal), formality and sentence endings (in Korean, 합니다체 / 한다체 / 해요체), how much they hedge, the connectives they use, paragraph length, how they open and close, words they prefer or avoid, how they present numbers and citations, formatting habits.

Rules:

- For a long piece, state the profile in five to eight lines first and let them correct it.
- Imitate habits, not sentences. Do not paste their old sentences into the new text.
- Memory informs voice and preferences. Personal facts from memory go into the text only when they asked for that.
- Text written by other people or by AI is not evidence of their voice.
- Never say the voice was matched when no sample or profile was available.
- After building a profile from samples, offer to save it as `my-voice.md` so later requests, and agents without memory, can reuse it. Update that file when they correct the voice; do not rebuild it from scratch each time.

## 3. Evidence First

- Audit before drafting. List the statements the piece has to make and, for each, where it comes from: file, page, table cell, log value, code line. Open the real material (images, tables, code, slides) instead of relying on a description of it.
- Use what the audit surfaces: exact counts, names, dates, what a log shows over time, which function performs a step. These specifics are the substance of the text.
- Numbers come from the files. Build tables by script when possible and never retype figures from memory.
- Do not state what the material does not show. Say what was not done or not tested.

## 4. Drafting Rules

- Write what only this piece could say. Replace a general statement with the specific case.
- Attach a number, name, date or source to every claim that can carry one.
- First person for the person's own actions and judgments, and only when true. If the assistant did part of the work (ran an analysis, inspected files), tell them where and how, so the text describes the real process and they can confirm it.
- Short declarative sentences, one idea each. Hedge only real uncertainty.
- Avoid template patterns: First/Second/Third chains, mirrored sentence pairs, a summary line closing every paragraph, stock connectives in a row. When a fixed number of points is required, label them and give each a concrete case.
- Source and course material: cite the specific point (page, slide, section) and attach it to a fact of this piece in the same or the next sentence. Do not restate the source in bulk.
- An interpretation must match the numbers it rests on, including the categories it names. Check direction and labels against the table.
- Mark every part drafted without their notes, so they know what to review and reword.

## 5. Format Compliance

- Turn the guideline into a checklist: each required item, where it must appear, units and decimals, labels, limits, language, file type, file name.
- Produce the requested output type and use their template when one exists.
- Tables and figures follow the caption and title convention of their format, stay readable at the inserted size, and agree with the numbers in the text. Defaults when no template is given are in `references/lab-and-technical-reports.md`.
- Render the document and look at every page before delivery.

## 6. Verification Before Delivery

1. Every checklist item is present and in the right place.
2. Recompute each worked calculation from the text of the finished document. `scripts/verify_report_numbers.py report.pdf` does this for subtractions (`a - b = c`) and percentages (`100 x a / b = c %`); run it with `--help` first.
3. Compare tables with the source files.
4. Repeat the audit on the final text: each factual sentence has a source.
5. Quotations and references are checked against the originals. A reference that was not opened and checked does not go into the list (`references/papers-and-references.md`, section 3).
6. Files that had to stay unchanged are identical to the originals.

## 7. Revising

- Change one set of paragraphs at a time and confirm by diff that nothing else moved.
- Keep the previous version as a fallback.
- Rewording never changes facts, numbers or conclusions.

## 8. When An AI-Writing Check Report Is Provided (Assisted Drafting Only)

1. List the flagged blocks. Checkers merge headings, tables and captions into the block of a nearby paragraph, so map each block back to its paragraphs.
2. Flags concentrate in generic explanation: theory, lists of reasons, interpretation, restated source material. Rewrite only those paragraphs with sections 3 and 4. The person's own wording for the paragraph is the most effective source, so ask for it first.
3. Leave unflagged paragraphs alone unless a fact changes.
4. No tricks: no deliberate typos, odd characters, hidden text, synonym spinning or broken grammar. A revision that reads worse is not acceptable.
5. The checker cannot be run by the assistant. Never promise a percentage. The reported number is usually the share of text inside flagged blocks, and the checker may merge blocks differently on each run, so a rewrite that stays flagged can raise it.
6. Stop when the result is under the target the person named. Passages still flagged after two rounds should be written by the person.

What has worked: a general description replaced by a description of the actual inputs; a statement about method replaced by what the code does and when; one concrete case per reason, taken from the results; a plausible explanation backed by a logged value; a cited source point tied to a fact from the audit. Shortening or reordering sentences alone did not work.

## 9. Coach Only

The person writes every sentence. The assistant does not draft, rewrite, translate, paraphrase or polish their text, and does not supply sentences to copy. Follow the exact wording of the rule; if it also forbids AI feedback, stop and say so.

What the assistant does: turns the guideline into a checklist and reports what is covered and what is missing; asks what they want to claim, what evidence they have and who reads it; points to places in their draft and names the problem (claim without evidence, unclear referent, number that disagrees with a table, missing citation) so they can fix it; runs checks that produce no prose (arithmetic, units, numbering, reference format, limits, layout). Sections 3 to 6 serve as their self-check list. Code and data work follow the context's own rule for code, which may differ from its rule for prose.

Section 8 is not used in this mode.

## 10. Final Message

State the mode, the voice sources used (or that none were available), what was verified and how, what the person should confirm or reword themselves, and any known weakness of the piece.

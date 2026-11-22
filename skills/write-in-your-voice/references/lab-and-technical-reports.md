# Lab, Experiment And Technical Reports

Read this when the piece reports measurements, experiments, code runs or a build. It adds layout and evidence rules to the main skill. The person's template or guideline always wins over the defaults here.

## 1. Map The Evidence First

- List every photo, screenshot, waveform, log and result file, and assign each to the experiment, condition and question it supports. Use the exact file names.
- Prefer original photos and screenshots over redrawn diagrams.
- A number that cannot be read with confidence from an image is marked for the person to confirm, or described qualitatively. Do not invent voltages, distances, error values or sample counts.
- Keep theory, measured result, comparison and discussion apart. Error and difference tables are computed from the stated values only.
- For a large job keep a short source list: which file fed which table or figure.

## 2. Reports Built From Code Outputs

- Generate the document with a build script that reads the result files (CSV, JSON, logs) directly. Do not retype numbers.
- Put assertions in the script that tie the prose to the data (which condition was largest, the sign of a difference, a count), so a rerun that changes a result stops the build instead of leaving stale text.
- Show worked calculations in a table column (`a - b`, result) or as an equation. State units and signs, and keep percent apart from percentage points.
- State the software versions and device that the run itself recorded.
- Say where the run happened. If the assistant ran it, the person must know, because the version table describes that run.
- Compare supplied files that had to stay unchanged byte for byte with the originals, and check each statement about a setting against the code that sets it.
- If only the report is graded, deliver the report and package code plus outputs separately, without large datasets or other bulky generated files.

## 3. Figures

- Centered image; the image area holds only the image or its panels.
- Caption in its own centered paragraph directly below the image, never inside the image box.
- Related panels may share one figure with one caption. Unrelated items get separate figures.
- Resolution: about 1800 px wide for a full-width figure, about 850 px for a half-width one, saved at 300 dpi or more. For crops from a PDF, render the page at 300-400 dpi first and crop that; do not enlarge a low-resolution crop.
- Plots made by code: choose the figure size so axis and legend text stay at about 7 pt or more at the inserted width. One colour per series across panels, a different marker shape per series, labelled axes with units, a legend.
- Insert at a fixed physical width so the page layout is stable.

## 4. Tables

- Title in its own centered paragraph directly above the table. Keep title and table on one page; move both to the next page if the title would be left behind.
- Compact grid, centered header row with light shading, readable cell padding. Long explanations belong in the prose, not in cells.
- Repeat the unit in the header. Use the number of decimals the guideline asks for, everywhere.

## 5. Equations

- Use the document's native equation objects (Office Math in DOCX, equation editor in HWP, math mode in LaTeX), not typed plain text.
- Center standalone equations and explain the variables in the sentence before or after.
- Split a long derivation over several lines.
- Converters without a formula renderer leave native equations blank (LibreOffice without its Math component does this). Keep native equations in the editable file and build a second copy for PDF export with the same equations typeset as 600 dpi images. Look at the rendered PDF to confirm.

## 6. Layout Presets

Use the person's template when there is one. Otherwise pick a preset and say which.

| Setting | Compact | Standard |
|---|---|---|
| Page | A4 | A4 |
| Margins (top / bottom / sides) | 2.2 / 2.0 / 2.3 cm | 2.5 / 2.5 / 2.5 cm |
| Body | 10 pt, line spacing 112%, left aligned | 11 pt, line spacing 150%, justified |
| Paragraph spacing | 5 pt before, 2.5 pt after | 0 before, 4 pt after |
| Figure caption | 9 pt bold, in brackets: `[Figure 2. ...]` | 9 pt, plain: `Figure 2. ...` |
| Table title | 9 pt bold, above: `Table 2. ...` | 9 pt, above: `Table 2. ...` |
| Table header fill | light blue `DDEBF7` | light gray `E7E7E7` |

Caption labels follow the language of the report (`그림 2.` / `표 2.` in Korean). Use the font the template names; when it is not installed, use the closest available face and tell the person.

`scripts/docx_report_helpers.py` applies these presets with python-docx: page setup, centered figure with outside caption, titled table, native equation, optional image equation.

## 7. Export

- DOCX to PDF: convert, then open the PDF and look at every page (blank equations, detached table titles, a figure pushed to the next page leaving half a page empty).
- HWP/HWPX: export through the Hancom application itself on the person's machine and reopen the result to check fonts and equations. The assistant cannot verify an HWP file it has not opened.
- Set the document author and title metadata to the person's, not to a tool default.

## 8. Final Checks For This Genre

1. Every figure and table is referred to in the text and numbered in order.
2. Every number in the prose matches its table; run `scripts/verify_report_numbers.py` on the finished file.
3. Axes, units, legends and any required markers are present on every plot.
4. The required items of the guideline sit under the question or section they belong to.

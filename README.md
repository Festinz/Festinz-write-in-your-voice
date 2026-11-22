# write-in-your-voice

An agent skill for writing any piece in **your own voice** and in **the format you were asked for**: reports, essays, proposals, statements, emails, posts, scripts. It works in any language and in Claude, ChatGPT and Codex, Cursor, and Antigravity.

[한국어 안내는 아래에 있습니다.](#한국어-안내)

## Quick start

**1. Get the files.** On the repository page choose **Code > Download ZIP** and unzip it (or `git clone` the repository).

**2. Install for your agent.** Pick one row.

| You use | Do this |
|---|---|
| Claude (web or desktop app) | Open **Customize > Skills**, add a skill, choose **Upload a skill**, and select `release/write-in-your-voice.zip`. |
| Claude Code, ChatGPT desktop app, Codex, Cursor, Antigravity | **Windows:** double-click `install.bat`. **macOS:** double-click `install.command`. **Linux:** run `./install.sh`. Choose your agent from the menu, then restart the agent. |
| A chat without skills (ChatGPT on the web, Gemini, any other assistant) | Open `release/paste-into-chat.md`, copy all of it, and paste it as the first message or as custom instructions. |

**3. Ask.** Copy the form in [`templates/request.md`](templates/request.md), fill in what you have, attach your files and send it. The short version:

```text
Use the write-in-your-voice skill.
Write: the project report for the attached measurements (English, max 5 pages, PDF).
AI rule here: allowed.
Format: guideline.pdf and template.docx (attached).
My voice: the two earlier reports I attached are mine.
Material: the data folder and my notes.
```

You do not have to fill in everything. The agent asks for what it needs, or picks a default and tells you.

### Do this once: save your voice

The first time, give the agent two or three texts you wrote yourself and say:

```text
Read these and write my voice profile into my-voice.md.
```

Correct anything that is wrong, then keep `my-voice.md` in your project folder or attach it to later requests. Agents with memory can also be told "use what you remember about my writing", but the file works everywhere. A blank profile is in [`templates/my-voice.md`](templates/my-voice.md).

## What the skill makes the agent do

1. **Settle four things before writing.** What the piece is, what the context says about AI use, the required format, and the material to write from.
2. **Build a voice profile.** From texts you wrote yourself, a saved `my-voice.md` or memory of your preferences, or, failing those, your messages in the conversation. It states the profile before a long piece so you can correct it, and it never claims your voice was matched when it had nothing to match against.
3. **Put evidence first.** It audits every statement against your files (data, logs, code, sources) before drafting, and writes from the specifics the audit finds.
4. **Follow the format.** It turns the guideline into a checklist, writes in your template when you give one, and looks at the rendered result.
5. **Verify before delivery.** Requirements, arithmetic, tables against source files, citations, and a second audit of the final text.
6. **Tell you what it did.** Which voice sources it used, what it verified, and which parts you should confirm or reword yourself.

### What is included for reports and papers

| Need | Where |
|---|---|
| Lab, experiment and technical reports: evidence mapping, figures with outside captions, titled tables, native equations, layout presets, reports generated from result files | `references/lab-and-technical-reports.md` |
| Papers and theses: section structure, finding sources, verifying every reference before it is listed, citation styles | `references/papers-and-references.md` |
| Experimental statistics: what to report with each number, small-sample uncertainty, choosing a test, multiple comparisons, wording of conclusions | `references/statistics-reporting.md` |
| Building a DOCX with those layout rules | `scripts/docx_report_helpers.py` |
| Rechecking the arithmetic of a finished report | `scripts/verify_report_numbers.py` |

The agent's own tools do the searching, plotting and computing. The skill sets the rules they have to meet. HWP export is described but not automated: it has to run through the Hancom application on your machine.

### What it will not do

The first step asks whether the context allows AI-written text. Where it does not (a course or exam that bans it, an application that requires your own writing), the skill switches to **coach-only** mode: you write every sentence, and the agent checks requirements, points at problems in your draft and verifies numbers and references. It does not draft or rewrite for you there, and it does not help make AI-written text pass as your own.

This is not a "humanizer". It does not exist to make AI-written text pass an AI-writing checker, and it promises no percentage. In contexts where AI help is allowed, it can revise flagged passages by grounding them in your material, and it uses no tricks such as deliberate typos or hidden characters.

## Install in detail

Every option installs the same folder: `skills/write-in-your-voice/`.

| Agent | Where the folder goes | Scope |
|---|---|---|
| Claude (web, desktop) | Upload `release/write-in-your-voice.zip` in **Customize > Skills** | Your account |
| Claude Code | `~/.claude/skills/write-in-your-voice/` | All projects |
| | `<project>/.claude/skills/write-in-your-voice/` | One project |
| ChatGPT desktop app, Codex CLI, Codex IDE extension | `~/.agents/skills/write-in-your-voice/` | All projects |
| | `<project>/.agents/skills/write-in-your-voice/` | One project |
| Cursor | `~/.cursor/skills/write-in-your-voice/` | All projects |
| | `<project>/.cursor/skills/write-in-your-voice/` | One project |
| Antigravity (app, IDE, CLI) | `~/.gemini/config/skills/write-in-your-voice/` | All workspaces |
| | `<workspace>/.agents/skills/write-in-your-voice/` | One workspace |

### Installers

The double-click installers show a menu. From a terminal you can name the agent directly.

```bash
./install.sh                      # menu
./install.sh cursor               # or: claude-code, codex, antigravity, all
./install.sh codex --project ~/code/my-project    # one project only
```

```powershell
.\install.ps1                     # menu
.\install.ps1 -Agent cursor
.\install.ps1 -Agent codex -Project C:\code\my-project
```

Restart the agent after installing so it rescans its skill folders. You can also copy the folder by hand to the location in the table.

### Notes per agent

- **Claude.** The ZIP in `release/` already has the skill folder as its top level, which is what the upload expects. Code execution and file creation must be enabled for skills to run. See [Use skills](https://support.claude.com/en/articles/12512180-use-skills).
- **ChatGPT and Codex.** In the Codex CLI or IDE extension, run `/skills` or type `$` to mention the skill. In the ChatGPT desktop app, type `@` and select it. See [Agent Skills in Codex](https://developers.openai.com/codex/skills).
- **Cursor.** Invoke it with `/write-in-your-voice` or let the agent choose it. Cursor also reads `.claude/skills/` and `.codex/skills/`. See [Agent Skills in Cursor](https://cursor.com/docs/skills).
- **Antigravity.** See [Agent skills in Antigravity](https://antigravity.google/docs/skills).
- **Agents that read `AGENTS.md`.** Copy `AGENTS.md` and the `skills/` folder into your project. `AGENTS.md` tells the agent when to open the skill.

## More request examples

```text
I have to write this scholarship essay myself (AI-written text is not allowed).
Here is the prompt and my draft. Check it against the prompt and tell me what is weak.
```

```text
Draft a reply to this email the way I usually write to professors. Use my-voice.md. Under 120 words.
```

```text
Here is my paper draft and results.csv. Check every number in the text against the file,
verify the reference list, and tell me which statistics are missing.
```

## The scripts

`skills/write-in-your-voice/scripts/verify_report_numbers.py` rereads a finished report and recomputes the worked calculations it states.

```bash
python3 skills/write-in-your-voice/scripts/verify_report_numbers.py report.pdf
# checked 8 worked calculations, 0 mismatch(es)
```

It handles subtractions written as `a - b = c` (or as adjacent table cells) and percentages written as `100 x a / b = c %`. PDF input needs the `pdftotext` command (Poppler); a `.txt` file needs nothing. The exit code is 1 when a stated result is wrong.

`skills/write-in-your-voice/scripts/docx_report_helpers.py` builds DOCX reports with the layout rules of the skill. It needs `python-docx` (and `matplotlib` for image equations).

```bash
pip install python-docx
python3 skills/write-in-your-voice/scripts/docx_report_helpers.py --demo demo.docx
```

```python
from docx_report_helpers import Report

r = Report(preset="compact")            # or "standard"
r.table("Table 1. Measured and nominal resistance", ["Resistor", "Nominal (\u03a9)", "Measured (\u03a9)"],
        [["R1", "1000", "987"], ["R2", "4700", "4712"]], widths_cm=[3, 4, 4])
r.figure("setup.png", width_cm=12, caption="Figure 1. Measurement setup")
r.save("report.docx")
```

## Repository layout

```text
skills/write-in-your-voice/
  SKILL.md                              the skill: the whole procedure
  references/
    lab-and-technical-reports.md        figures, tables, equations, presets, code-output reports
    papers-and-references.md            paper structure, finding and verifying references
    statistics-reporting.md             what to report, tests, wording
  scripts/
    docx_report_helpers.py              build DOCX reports with the layout rules
    verify_report_numbers.py            recompute worked calculations in a report
release/
  write-in-your-voice.zip               ready to upload to Claude
  paste-into-chat.md                    the whole skill as one file, for chats without skills
templates/
  request.md                            fill-in request form (English and Korean)
  my-voice.md                           blank voice profile
AGENTS.md                               entry point for agents without skill support
install.bat, install.command            double-click installers (Windows, macOS)
install.sh, install.ps1                 installers for the terminal
package.py                              rebuild release/ after editing the skill
```

If you edit the skill, run `python3 package.py` to rebuild `release/`. `python3 package.py --check` reports whether `release/` is up to date.

## 한국어 안내

**내 문체**와 **요구된 양식**에 맞춰 글을 써 주는 에이전트 스킬입니다. 보고서, 에세이, 제안서, 자기소개서, 이메일, 발표 대본 등에 쓸 수 있고 언어 제한이 없습니다. Claude, ChatGPT·Codex, Cursor, Antigravity에서 같은 폴더를 그대로 씁니다.

### 빠른 시작

**1. 파일 받기.** 레포 페이지에서 **Code > Download ZIP**을 눌러 받은 뒤 압축을 풉니다.

**2. 쓰는 에이전트에 설치하기.**

| 쓰는 도구 | 할 일 |
|---|---|
| Claude (웹·데스크톱 앱) | **Customize > Skills**에서 스킬 추가 → **Upload a skill** → `release/write-in-your-voice.zip` 선택 |
| Claude Code, ChatGPT 데스크톱 앱, Codex, Cursor, Antigravity | **Windows:** `install.bat` 더블클릭. **macOS:** `install.command` 더블클릭. **Linux:** `./install.sh` 실행. 메뉴에서 에이전트를 고른 뒤 에이전트를 다시 시작 |
| 스킬 기능이 없는 채팅 (웹 ChatGPT, Gemini 등) | `release/paste-into-chat.md` 내용을 전부 복사해 첫 메시지나 맞춤 지침에 붙여 넣기 |

**3. 요청하기.** [`templates/request.md`](templates/request.md)의 한국어 양식을 복사해 채우고 파일과 함께 보냅니다.

```text
write-in-your-voice 스킬을 써 줘.
쓸 글: 첨부한 측정 결과로 프로젝트 보고서 (한국어, 5쪽 이내, PDF)
AI 사용 규정: 허용
양식: guideline.pdf, template.docx (첨부)
내 문체: 첨부한 이전 보고서 두 편이 내가 쓴 글
자료: data 폴더와 내 메모
```

전부 채우지 않아도 됩니다. 에이전트가 필요한 것을 묻거나 기본값을 정하고 알려 줍니다.

### 처음 한 번: 내 문체 저장하기

직접 쓴 글 두세 편을 주고 이렇게 요청하세요.

```text
이 글들을 읽고 내 문체 프로필을 my-voice.md로 써 줘.
```

틀린 부분을 고친 뒤 `my-voice.md`를 프로젝트 폴더에 두거나 다음 요청에 첨부하면 됩니다. 메모리가 있는 에이전트에는 "내 글쓰기에 대해 기억하는 것을 써 줘"라고 해도 되지만, 이 파일은 어느 에이전트에서나 통합니다.

### 스킬이 하는 일

1. 쓰기 전에 네 가지를 확인합니다: 어떤 글인지, AI 사용이 허용되는지, 요구 양식, 근거 자료.
2. 본인이 쓴 글, `my-voice.md`, 메모리로 문체 프로필을 만듭니다. 아무것도 없으면 평이한 문체로 쓰고 그 사실을 알립니다.
3. 초안을 쓰기 전에 모든 서술을 자료(데이터, 로그, 코드, 출처)와 대조합니다.
4. 가이드라인을 체크리스트로 바꿔 양식을 맞추고, 템플릿이 있으면 그 안에 씁니다.
5. 전달 전에 요구사항, 계산, 표, 인용을 다시 검증합니다.
6. 무엇으로 문체를 맞췄는지, 무엇을 검증했는지, 본인이 직접 확인하거나 고쳐 써야 할 부분을 알려 줍니다.

실험·기술 보고서(그림·표·수식·양식 프리셋·결과 파일 기반 문서 생성), 논문(구조·레퍼런스 검색과 검증·인용 양식), 실험 통계 보고 규칙은 `references/` 폴더의 파일 세 개에 있고, 필요할 때만 읽습니다.

AI가 금지된 과제나 지원서에서는 **코칭 모드**로만 동작합니다. 문장은 본인이 쓰고, 에이전트는 요구사항 점검, 초안의 문제 지점 짚기, 숫자·인용 검증만 합니다. 이 스킬은 AI 검사 수치를 낮추기 위한 "humanizer"가 아니며 어떤 수치도 보장하지 않습니다.

## License

MIT. See [LICENSE](LICENSE).

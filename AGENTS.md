# AGENTS.md

Rules for Claude and Codex in `general_dual_simplex_manuscript`. The user often
reads from a phone: be complete and compact.

This repository holds manuscript text, figures and the research record. It
holds no algorithm code. Read `README.md` first.

## Roles

Each session has one role. State it once at the start.

- **Lead** (usually Claude, working with the user): discusses the science,
  drafts text, makes figures, keeps `artifact/`. Start with
  `script/decision-log.py artifact/decisions.md -r 5` and
  `git log --oneline -20`; state where the work stands in one or two sentences.
- **Reviewer** (usually Codex, started by the lead): read-only unless the
  prompt assigns edits. Checks mathematics, evidence, figures or language.
  Returns a verdict, findings with file and line, and open questions.
- Either agent may take either role. Ask the user before changing scientific
  claims, mathematical assumptions, manuscript format or scope.

## Sources

- Package `GeneralDualSimplex`: `/workspace/dual_simplex_functional/general_dual_simplex`
  (`<package>` below).
- Package discussion: `<package>/.ai/`. **Read only**; never edit, stage or
  commit in another repository. Search with
  `<package>/.ai/tool/decision-log.py <package>/.ai/decisions.md -g <pattern>`,
  then read one entry with `-t <words>`. Do not read the whole file.
- When a package note informs a claim or figure, cite the note path and the
  package commit (`git -C <package> rev-parse HEAD`).
- Legacy pilot study (experiments and reports from before the package):
  `/workspace/dual_simplex_functional/general_dual_simplex_experiment`. Read
  only; cite its reports with the full commit. It is not developed further.
- Legacy DSO package `DualSimplex` (`artyomovlab/dualsimplex`), installed in
  this renv for comparison. Cite the commit recorded in `renv.lock`.
- Changes needed in another repository go to the user as a proposal. Do not
  symlink to another repository.

## Evidence

- Cite each numerical finding with its source: report or note path, section or
  table caption, and the full commit of the repository that produced it. Cite
  package version and full commit for claims that depend on the implementation.
  Copy formulas and parameters from the code or report, never from memory.
- Figure data computed here are illustrative unless a cited result backs them;
  say so in the caption draft.
- State assumptions and show derivations. Use primary sources for literature.
  Separate hypotheses, measurements and conclusions.
- Write "confirms", "proves", "exact" or a cause only if the evidence could
  have shown the opposite; otherwise "consistent with". Report a failed
  prediction as failed. Say "the result does not support that" when it does not.
- Round from unrounded values. Round upper bounds up.
- Read HTML reports with `script/extract-report.py <report.html> --out out/<name>`.
  Claim a figure inspected only after opening the image itself. Find a table's
  caption in the report source before naming its number.

## Figures

- Layout: `figure/<figN>/<panel>/` with the SVG, its generator, input data and
  `package_commit.txt` (package commit, version, and `git status --porcelain R src`).
- R runs in this repository's renv, started from the repository root. Approved
  packages are listed in `README.md`. Generators may compute illustrative data
  and draw; they print the properties a caption needs and do not stop or
  branch on them.
- After the first hand edit the SVG is the master. Generators replace data
  groups by id inside it; they never rewrite the file.
- SVG conventions: mm `viewBox`; Inkscape layers; readable ids on every object;
  real text in Liberation Sans/Arial, 5–8 pt; lines 0.4–0.6 pt. A `<text>` with
  `sodipodi:role="line"` tspans needs its own `x`/`y`.
- Verify each change: render with `inkscape <svg> --export-type=png --export-dpi=600`,
  open the PNG, and check with `inkscape --query-all` that text lies inside the
  canvas and inside its box. Inkscape's GTK warnings are harmless.
- Editing with the user: the user saves as Inkscape SVG; the agent keeps a
  numbered backup, edits, and asks the user to use File → Revert. Diff by
  meaning (query boxes and text by id), not by Git lines: Inkscape reformats.

## Writing and language checks

- Plain English, short sentences, active voice. Define a term once and keep it.
  Prefer numbers to vague quantities.
- A language check changes wording, never meaning. Report each change as
  location, original, suggestion and reason. Flag, do not fix, any sentence
  whose claim the evidence does not support.
- Edit only the files assigned in the task. Preserve others' edits.

## Record

- `artifact/decisions.md` is written only by the lead. Entries start
  `## YYYY-MM-DD — Title`, with the title naming the decision, followed by
  context, options, decision, evidence and revisit-if. Append one after a
  conversation that changes direction. Find old ones with `-l` or `-g`.
- Long material goes in `artifact/YYYYMMDD_<topic>.md`; reply with its path.
- Tasks for another agent go in `artifact/handoff/YYYYMMDD-HHMM_<recipient>_<topic>.md`
  (local time). Never rename old files.

## Agents

- Start agents only through Paseo `list_profiles` then `create_agent`; copy the
  profile settings unchanged and label `profile=<name>`. Put the recipient,
  repository and workspace ID in the prompt. Do not use the built-in Agent tool.
- A fresh reviewer from the other provider checks every change to
  mathematics, evidence or figure data, however small. Skip review only when
  the change cannot alter a formula, a claim or a cited number: wording,
  typos, layout, colour, fonts, label position, file moves, README or
  AGENTS.md edits, and illustrative figure data that no claim relies on
  and whose caption draft says it is illustrative. Any other change to a
  generator's data or parameters needs review. When skipping, end the
  commit message with "No review: <reason>". If unsure, review.
- Print `/sys/fs/cgroup/pids.current` before each launch. Read each agent's last
  message with `get_agent_activity`, then archive it.
- One new task, one new agent.

## Git and safety

- Stage files by name; never `git add -A` or `git add .`.
- Ask before deleting a tracked file, adding a dependency (R package or system
  tool), `git push --force`, `git reset --hard` or `git clean -fdx`. Never
  rewrite history. Use ordinary pushes only when the user asks; do not bypass
  push protections.
- Never delete or move a file you did not create to clean Git status; list
  untracked files instead.
- Never create, change or print keys, tokens or SSH configuration. Never print
  process command lines; list processes with `ps -o pid,ppid,stat,comm`.

## Communication

Result first, then evidence and limits. Say each point once. Put a blank line
before every Markdown list. Avoid new jargon and abbreviations. Disagree when
the evidence warrants it. When an agent gets something wrong, propose a dated
house rule.

## House rules

One line per lesson, dated.

- 2026-10-09: Never print process command lines; they can hold tokens.
- 2026-10-26: "Small" does not exempt a change from review. A change is exempt
  only if it cannot alter a formula, a claim or a cited number.

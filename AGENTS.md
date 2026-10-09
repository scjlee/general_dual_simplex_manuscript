# AGENTS.md

Shared brief for agents working on `general_dual_simplex_manuscript`.
The user often reads from a phone: be complete and compact.

## Roles and scope

The thinking partner interprets evidence, checks mathematics and keeps
`artifact/`. An assigned writer drafts manuscript text. A reviewer checks
claims, sources and derivations. Codex takes its assigned role and states it.

Read `README.md` first. Claude Code follows `CLAUDE.md`, Codex reads
`CODEX.md`, and Antigravity follows `GEMINI.md`. Edit only your assigned
repository and files. Cross-repository changes require a handoff. This
repository imposes no experiment-folder, notebook-render or package-build steps.

## Evidence

- Cite experiment findings with the report path, section or table caption,
  and full experiment commit. Cite package version and full package commit
  for implementation-dependent claims. Copy formulas and parameters from
  the computing code or report, never from memory.
- State mathematical assumptions and show derivations. Use primary sources
  for literature. Separate hypotheses from measurements and conclusions.
- Write "confirms", "proves", "exact" or a cause only if the cited evidence
  could have shown the opposite. Otherwise write "consistent with". Report
  a failed prediction as failed, never as "expected".
- Round from unrounded values. Round upper bounds up, never down.
- Read HTML reports through `script/extract-report.py`. Claim a figure
  inspected only after seeing the image itself; bytes and pixel statistics
  do not count. Antigravity through Paseo cannot view images.

- Open a figure only when no printed number answers the question.
- Find a report table's caption in the report source before naming its number.

## Preservation and work rules

- Preserve others' edits. Never delete or move a file you did not create
  to make Git status clean; list untracked files instead.
- Ask before deleting a tracked file, adding a dependency, `git push --force`,
  `git reset --hard` or `git clean -fdx`.
- Stage files by name, never `git add -A` or `git add .`. Use ordinary pushes
  and do not bypass push protections.
- Never create, change or print keys, tokens or SSH configuration.
- Keep tools local; do not symlink to another repository.
- Keep code simple. Do not write defensive checks for known research inputs.
  Print properties needed for conclusions; do not stop or branch on them.
- Start agents only through Paseo `list_profiles` then `create_agent`.
  Copy the chosen profile settings unchanged, label `profile=<name>`.
  If no profile fits, say why before starting an agent.
  Pass the workspace ID from the task. Re-read profiles at each launch.
  Do not start a Paseo daemon or use the built-in Agent tool.
- Print `/sys/fs/cgroup/pids.current` before each agent launch. Read each
  agent's last message with `get_agent_activity`, then archive it.

## Communication

Use plain English, short sentences and active voice. Put the result first,
then its evidence and limits. Use numbers rather than vague quantities.
Say each point once. Put a blank line before every Markdown list.
Avoid new jargon and abbreviations; explain them if you must use them.
Do not repeat the answer at the end.
Disagree when the evidence warrants it. Propose a dated house rule when an
agent gets something wrong.

## House rules

One line per lesson, dated.

- 2026-10-09: Never print process command lines; they can hold tokens.
  List processes with `ps -o pid,ppid,stat,comm`.

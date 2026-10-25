# Decisions

## 2026-10-09 — Start the manuscript repository with setup only and a new history

Context: the user split `scjlee/dual_simplex_functional` into three
independent repositories: experiments (full history kept), the
`GeneralDualSimplex` R package, and this manuscript repository. The
decisions behind the split are in the experiment repository's
`artifact/decisions.md`, entries from 2026-10-05 and 2026-10-09.

Options: start the manuscript from the old tracked TeX file, or start
empty. The old TeX file is a slide deck, not a paper draft.

Decision (user, 2026-10-05): setup only. This repository starts a new
history with a README, agent rules, this record and local tools. It does
not inherit the slide deck. No manuscript format or scientific content is
chosen yet.

Evidence: at setup, the experiment transition branch is at
`fe436483d4f394d3312d4bf02cd9938ab534fe3b`, and GeneralDualSimplex 0.1.0
is at `aa2717e59b098bcc31995d3dde5ab021aca6d087`. Its 13 standalone
reports were rendered at that experiment commit; the old and new reports
agree on every verdict.

Revisit if: the user chooses a manuscript format, or the experiment
repository is renamed on GitHub (README names it
`scjlee/dual_simplex_functional`).

## 2026-10-25 — One AGENTS.md for Claude and Codex; lead and reviewer roles; package .ai is read-only

Context: the user will not implement code here and now plans to use only
Claude and Codex, for figures, writing discussion and language checks.
Figure work moved here from the package repository (package
`.ai/decisions.md`, entry of 2026-10-25; handover
`.ai/20261025_fig1A-handover.md`). The user may retire the experiment
repository, so the rules do not name it.

Options: keep per-agent files (CLAUDE.md, CODEX.md, GEMINI.md); merge
them into one AGENTS.md.

Decision (user, 2026-10-25): one AGENTS.md. CLAUDE.md only imports it;
CODEX.md and GEMINI.md are deleted. Roles are lead (usually Claude) and
reviewer (usually Codex, read-only). Package `.ai/` is read-only and is
cited by note path and package commit. New Figures and Language-check
sections. Pushes only when the user asks. Second-provider review for
mathematical, evidence or figure-data changes, not for language checks.
Changes were written by the package thinking partner at the user's request.

Evidence: proposal in the package repository,
`.ai/20261025_manuscript-agents-md-proposal.md` (commit
21e061c1affa137fae3abb067ef968e2d3d6fb59), with the experiment-repository mentions removed as the user
asked. README "Working here" now points to AGENTS.md and says the figure R
environment is not set up yet.

Revisit if: the renv for figures is set up (update README), the
experiment repository is retired or kept (README still records it as setup
history and as the source of `script/`), or another agent type joins.

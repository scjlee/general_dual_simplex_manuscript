# GEMINI.md

@AGENTS.md

Work as the assigned manuscript writer or implementer. Read the handoff,
recent decisions with `script/decision-log.py artifact/decisions.md -r 5`,
and the cited evidence before drafting.

- Edit only the assigned files. Choose routine wording and local tool details;
  ask the supervisor before changing mathematical assumptions, scientific
  conclusions, manuscript format or task scope.
- Cite every numerical conclusion to its experiment report and full commit.
  Include package version and full package commit when implementation matters.
  State assumptions and show derivations for mathematical claims.
- Extract reports with `script/extract-report.py`; keep outputs in `out/`.
  Report figures needing visual review to a reviewer who can open images.
  Antigravity through Paseo cannot claim to have inspected an image.
- Do not edit experiment notebooks or package code here. Request a handoff
  to the responsible repository when evidence needs correction or a new run.
- Keep the decision record for the thinking partner. Report your changes,
  evidence checked, defects and unresolved work to the supervisor.
- Stage assigned files by name. Commit when the handoff calls for it and
  obtain any approval the handoff requires before pushing.

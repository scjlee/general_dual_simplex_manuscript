# general_dual_simplex_manuscript

Manuscript drafts and mathematical review for the general dual simplex project.
This repository starts a new history for the three-repository transition.
No manuscript format or scientific content is selected during setup.

The companion repositories are `scjlee/dual_simplex_functional`
(experiments and reports, local directory `general_dual_simplex_experiment/`) and `scjlee/general_dual_simplex` (the
`GeneralDualSimplex` R package). At setup, the experiment transition commit is
`fe436483d4f394d3312d4bf02cd9938ab534fe3b` and GeneralDualSimplex 0.1.0 is
at `aa2717e59b098bcc31995d3dde5ab021aca6d087`. These identify the setup
state; cite the versions actually supporting each later claim.

## Working here

Read `AGENTS.md` and the rule file for your agent before editing. Work only
on assigned writing or review. Changes to experiments or package code require
a handoff to that repository. Do not import the historical slide deck.
This repository has no R environment or package build workflow.

Cite numerical findings with the experiment repository, full commit, report
path and section or table caption. Cite the package version and full package
commit when a claim depends on its implementation. State mathematical
assumptions and cite primary sources for literature claims.

## Local tools and record

- `artifact/decisions.md`: the thinking partner's decision record.
- `artifact/handoff/`: dated writing and review handoffs when needed.
- `script/decision-log.py artifact/decisions.md -r 5`: read recent decisions.
- `script/extract-report.py <report.html> --out out/<report-name>`: extract
  report text and figures locally; it uses the existing Python Pillow tool.
  Use `--fig-scale 1` when full-size figures are needed.

The local scripts are copied from the experiment repository at the setup
commit above; their original MIT notice is preserved in `script/LICENSE`.

Keep extraction outputs under ignored `out/`. Open an extracted image before
claiming to have inspected it. Report extraction does not rerun an experiment.

## Git setup

The SSH origin is
`git@github-gds_manuscript:scjlee/general_dual_simplex_manuscript.git`.
Stage files by name and use ordinary pushes. The tracked push-deny settings
are in `.claude/settings.json`. After cloning, install the local hook with:

```sh
cp script/git-hooks/pre-push .git/hooks/pre-push
chmod +x .git/hooks/pre-push
```

Cloning does not install the hook. Do not bypass push protections or copy
credentials and local configuration from another repository.

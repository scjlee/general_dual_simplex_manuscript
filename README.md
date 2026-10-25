# general_dual_simplex_manuscript

Manuscript drafts, figures and the research record for the general dual
simplex project. No manuscript format or scientific content is chosen yet,
and the historical slide deck is not imported.
Agents read `AGENTS.md` before editing; it holds the rules for Claude and Codex.

## Related repositories

| Role | Repository | Local directory |
|---|---|---|
| Current R package `GeneralDualSimplex` | `scjlee/general_dual_simplex` | `../general_dual_simplex` |
| Legacy pilot study (experiments and reports) | `scjlee/dual_simplex_functional` | `../general_dual_simplex_experiment` |
| Legacy DSO R package `DualSimplex` | `artyomovlab/dualsimplex` | installed in this renv |

- The package's discussion record lives in its `.ai/` folder. Agents read it
  but never edit it.
- The legacy pilot study predates the package. It is kept for reference and
  is not developed further. Cite its reports with the full commit.
- The legacy `DualSimplex` package is installed for comparison only.
- Setup state (2026-10-09): pilot study at
  `fe436483d4f394d3312d4bf02cd9938ab534fe3b`, GeneralDualSimplex 0.1.0 at
  `aa2717e59b098bcc31995d3dde5ab021aca6d087`. Cite the versions that support
  each later claim, not these.

## Layout

- `AGENTS.md`: rules for agents. `CLAUDE.md` only imports it.
- `artifact/`: the decision record (`decisions.md`), long notes
  (`YYYYMMDD_<topic>.md`) and agent tasks (`handoff/`, created when needed).
- `figure/<figN>/<panel>/`: the SVG (the master after a hand edit), its
  generator, input data, `package_commit.txt` and PDF/PNG previews.
- `script/`: local tools, copied from the pilot study at the setup commit;
  their MIT notice is in `script/LICENSE`.
- `out/`: ignored scratch output, such as report extracts.
- `renv/`, `renv.lock`, `.Rprofile`: the R environment.

## R environment

R 4.5.3 with renv and Bioconductor 3.22. After cloning, run
`renv::restore()` from the repository root. Run figure scripts from the
root too, for example `Rscript figure/fig1/panelA/points.R`.

- `GeneralDualSimplex` is installed from the local checkout, so `renv.lock`
  records `Source: Local` with no commit. Each figure script writes the
  package commit, installed version and uncommitted `R/` and `src/` changes
  to `package_commit.txt`. After the package changes, reinstall with
  `renv::install("../general_dual_simplex")` and `renv::snapshot()`.
- `DualSimplex` is pinned by its GitHub commit in `renv.lock`.
- Approved packages: GeneralDualSimplex, DualSimplex, ggplot2, patchwork,
  scales, svglite (plus their dependencies). Ask before adding others.

System tools: Inkscape 1.4 or later, Liberation Sans (or Arial), Python 3
(standard library only).

## Local tools

- `script/decision-log.py artifact/decisions.md -r 5`: read recent decisions;
  `-l` lists titles, `-g <pattern>` searches, `-t <words>` prints one entry.
- `script/extract-report.py <report.html> --out out/<report-name>`: extract
  report text and figures; it uses Python Pillow. Use `--fig-scale 1` for
  full-size figures. Extraction does not rerun anything.

## Git setup

The SSH origin is
`git@github-gds_manuscript:scjlee/general_dual_simplex_manuscript.git`.
Stage files by name. Agents push only when the user asks. The tracked
push-deny settings are in `.claude/settings.json`. After cloning, install the
local hook with:

```sh
cp script/git-hooks/pre-push .git/hooks/pre-push
chmod +x .git/hooks/pre-push
```

Cloning does not install the hook. Do not bypass push protections or copy
credentials and local configuration from another repository.

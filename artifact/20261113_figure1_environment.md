# Figure 1 R environment update — 2026-11-13

The user authorized adding the dependencies needed to run
`data/figure1/261106_figure1_components.Rmd`. The environment is updated and
a copy with local file paths rendered successfully. The original Rmd, supplied
data, HTML and PDF were not edited. No scientific claims or calculations were
changed, and no commit or push was made.

## Environment

R 4.5.3, Pandoc 3.1.3. New directly used packages installed in the project's
renv:

| Package | Locked version |
|---|---|
| data.table | 1.18.2.1 |
| ggh4x | 0.3.1 |
| colorspace | 2.1-2 |
| ggrastr | 1.0.2 |
| ggnewscale | 0.5.2 |
| rmarkdown | 2.31 |

The installation added these packages and their required dependencies to the
project library and lockfile. No new system tools were installed. svglite
2.2.2 and knitr 1.51 were already available. Existing locked packages were
retained; GeneralDualSimplex was the only existing package whose version changed.
The configured CRAN snapshot remains 2026-04-23; snapshotting also recorded the
existing Bioconductor 3.22 repository URLs.

GeneralDualSimplex was updated from 0.28.0 to 0.38.0, matching the version
recorded in the first saved simulation result. Its source was the local
checkout at full commit `09dd30edfd7a65715e6ec0261d3ea12b0cd0ee71`.
`git status --porcelain R src` was empty before and after installation. Building
used a scratch copy, so the package repository was not changed. Its installed
source metadata and lockfile retain the original local checkout path.
The saved RDS does not establish the commit that generated the simulations.

`renv::snapshot(type = "all", prompt = FALSE)` saved the environment in
`renv.lock`. A subsequent `renv::status()` reported:

> No issues found -- the project is in a consistent state.

`README.md` now lists the newly approved report packages.

## Render and checks

The scratch Rmd is `out/figure1-environment/figure1-local.Rmd`. Its only
changes from the supplied Rmd are paths: the helper is sourced from
`artifact/20261028_simulation_helpers.R`, the working directory is the
manuscript root, and the RDS is read from `data/figure1/`. Plotting and
calculation code, parameters and chunk evaluation flags are unchanged.
The original Rmd still contains cluster paths and cannot be rendered here
without adapting those paths or using the scratch copy.

Run the scratch copy from the manuscript root with:

```sh
Rscript out/figure1-environment/render.R
```

Output: `out/figure1-environment/figure1-local.html`.

All enabled chunks completed. The reference HTML and new HTML were extracted
with `script/extract-report.py`. Each contains 33 figures, with matching image
dimensions. Printed non-warning output blocks match between the reports.
Each contains seven warning blocks: data.table self-reference repair, min/max
on empty inputs, and numeric coercion of noise-level labels. The data.table
warning wording differs. These warnings were not corrected.

None of the PNG pairs is pixel-identical. Figure 31 was opened in both versions
and visually compared; no comprehensive visual review was performed. No cause
for the pixel differences was tested, and no claim of full numerical or image
equivalence is made.

## Logs and provenance

- `out/figure1-environment/install.log`: dependency installation.
- `out/figure1-environment/gds-install.log`: local package installation.
- `out/figure1-environment/render.log`: complete render output.
- `out/figure1-environment/snapshot.log`: environment snapshot.
- `out/figure1-environment/environment.log`: package loading, versions,
  environment consistency and session information.
- `out/figure1-environment/comparison.txt`: image comparison and printed-output
  comparison results.
- `out/figure1-original-report/report.md`: reference HTML extraction.
- `out/figure1-environment/rendered-report/report.md`: new HTML extraction.

Manuscript HEAD at the check was
`77f1c834ec9a0aee0a945fadace9fe4948d8c63f`. The supplied `data/` directory is
untracked, so that commit does not establish provenance for its files. The
environment changes and this report are uncommitted.

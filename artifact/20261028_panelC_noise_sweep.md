# Panel C draft from the saved noise sweep

Draft: `figure/fig1/panelC_sweep/fig1C_sweep.svg`, with PNG and PDF previews.
The user subsequently requested PNG only for now; only the PNG is delivered.
SVG/PDF are internal supporting artifacts.
The existing Figure 1C master is unchanged. These are illustrative simulation
plots; no manuscript claim relies on them.

## Metric and display

The user supplied the saved `metadata$row$scaled_var` and `scaled_total`
fields and requested colors for noise parameters. For each saved run, the
figure uses the stored across-sample variance of each gene in the **scaled
matrix** Vtilde, computed directly from its stored variances:

    v_g = sum_j (Vtilde_gj - mean_j Vtilde_gj)^2 / (n - 1)
    share_g = 100 * v_g / sum_h v_h

These percentages coincide with the old panel C's Z-based shares under
the uniform scaling used here. The definitions can differ for other
scalings. The y-axis names the stored matrix used in this calculation. The common sample-variance divisor cancels in the
percentage. The figure includes signal and noise together, rather than an
isolated noise contribution. `scaled_total` is retained in the extraction;
x ranks use the observed unscaled totals, low to high, matching the old C.
They do not use the saved `rank` field (which ranks high to low) or rank
by scaled total (which uniform scaling makes constant).

Within each run, rank genes independently by observed total, then average
shares in adjacent, nonoverlapping bins of 30 ranks. Bin centers are the
mean ranks. Curves show arithmetic means of those bin means across ten
seeds; ribbons show their minimum and maximum. The range is descriptive,
not a confidence interval. Genes can change rank and bin between settings
and seeds. The unbinned per-rank means and ranges are also retained. Ties in observed
total keep input gene order, with marker genes first in this archive.

All panels use the same logarithmic y-axis. Poisson and negative binomial
color library fractions; negative binomial additionally uses line style
for dispersion. Multiplicative lognormal colors SD on the log scale;
floored normal colors additive SD in signal units. The lognormal multiplier
has median one and is not corrected to mean one: package `R/simulation.R`,
`ApplyMultiplicativeNoise`, GeneralDualSimplex 0.29.0, current source commit
`bfd5ce69987c17e5a1253a477e9b73e965afc1aa`.

## Input and provenance

- Supplied archive: `/data/simulation_runs_k3.rds`.
- Supplied report: `/data/261027_experiment_script_check.html`, “load”
  (saved row fields and experiment metadata) and “evaluation” (model/parameter
  examples). Extracts: `out/261027_experiment_script_check_source/report.md`.
- Source SHA-256 checksums: `figure/fig1/panelC_sweep/source_sha256.txt`.
- Saved package version: 0.29.0. The source repository's current full commit
  is `bfd5ce69987c17e5a1253a477e9b73e965afc1aa`, with clean R/src. The supplied
  archive does **not** embed its generating commit, and the external report
  does not identify one. We cannot establish that the current checkout
  produced the archive. Do not treat it as verified generation provenance.
- Installed renv package is 0.28.0. This analysis reads plain archived states
  and saved scaling arrays directly; it does not reconstruct R6 objects,
  rerun simulation or call fitted scaling/optimization. The helper is used
  only to decode a compact Matrix if present (the supplied states use native
  Matrix objects). Source package and supplied data are read-only.
- Manuscript base: `d270e7485cf2518b6c04c4b9126c27a4878ce8d2`.

## Extraction checks

Source: `figure/fig1/panelC_sweep/runs.csv` and `checks.csv`; derived from
the archive identified above with `extract_shares.R`. These are local
measurements from supplied data with the generating-commit limitation above.

There are 320 saved runs: ten seeds for 32 settings, all uniform scaling,
with 3,000 retained genes and 500 samples each, K = 3 and marker fold = 5.
The plot uses 310 noisy runs; ten noiseless runs are retained in the run
index but excluded from the four model panels. Parameter grids are:

- Poisson: library fractions 0.01, 0.02, 0.025, 0.05, 0.1, 0.5, 1.
- Negative binomial: the same fractions, crossed with dispersion 0.01 and 0.1.
- Multiplicative lognormal: log SD 0.1, 0.25, 0.5, 0.75, 1.
- Floored normal: additive SD 5, 10, 15, 20, 25.

Recomputing each saved row variance from the active matrix and saved scaling
has maximum absolute discrepancy less than 2.553e-25. Relative to each
run's largest variance, the discrepancy is at most 1.5e-14 (independent
review: `out/panelC_sweep_review/validate.log`). Each run's percentage
shares sum to 100 within floating-point precision. All saved uniform
scalings report convergence. The extraction also independently checks the
old Z definition for comparison, but those values are not plotted.
Complete run checks are retained in `checks.csv`; the summary log is
`out/panelC_sweep_summary.log`.

The final 600 dpi PNG was opened. Inkscape query boxes place all 83 text
objects inside the canvas; labels and legends fit their panel regions.
Every SVG object has an id, with no duplicate ids. A generator refresh
changes only named data groups. No dependency was added.

## Reproduce

Run from the manuscript root in its renv:

```sh
RENV_CONFIG_SANDBOX_ENABLED=FALSE Rscript figure/fig1/panelC_sweep/extract_shares.R
RENV_CONFIG_SANDBOX_ENABLED=FALSE Rscript figure/fig1/panelC_sweep/summarize.R
python3 figure/fig1/panelC_sweep/make_panel.py
inkscape figure/fig1/panelC_sweep/fig1C_sweep.svg --export-type=png --export-dpi=600 --export-background=white --export-background-opacity=1
inkscape figure/fig1/panelC_sweep/fig1C_sweep.svg --export-type=pdf
```

Per-gene extraction (104 MB) is scratch output at
`out/panelC_sweep/gene_shares.csv`; the figure folder retains the run index,
checks, all per-rank summaries and the smaller plotted bin summaries as
inputs. The first unbinned preview is retained at
`out/panelC_sweep/fig1C_sweep_unbinned.png`.

## Caption draft

**C. Gene variance across noise levels with uniform scaling.** Each gene's
across-sample variance in the scaled matrix Vtilde is divided by the sum
of these gene variances and expressed as a percentage. Within each run,
genes are ordered from lowest to highest observed total and grouped into
bins of 30 adjacent ranks. Curves show mean bin shares across ten simulation
seeds; shaded regions span the seed minimum and maximum. Colors identify
library fraction for Poisson and negative-binomial noise, log SD for
multiplicative lognormal noise, and additive SD for normal noise floored
at zero. Negative-binomial dispersion is indicated by solid (0.01) or
dashed (0.1) lines. Axes are shared; the y-axis is logarithmic. Simulations
have K = 3, marker fold = 5, 3,000 genes and 500 samples. Variance includes
both signal and noise. This is an illustrative figure draft, not a claim
of comparative recovery performance. Input: `/data/simulation_runs_k3.rds`,
archived GeneralDualSimplex 0.29.0; source checksums and the unavailable
generating-commit limitation are recorded above.

## Review and correction

Fresh Advisor - Claude review: `out/panelC_sweep_review/review.md`,
verdict **accept after two fixes**. Independent re-binning reproduces
the plotted summaries; alignment, model mapping, line styles, caption
and bounds passed. Both requested fixes are completed: the delivered
PNG is exported on opaque white, with range opacity raised to 0.15, and
the metric explanation is corrected here and in the user response.
No plotted numbers changed after review.

For uniform scaling a_g = 1/m and b_j = 1/n:

    Z = sqrt(mn) Vtilde
    mean_j Vtilde_gj = 1/(mn)
    q_g = sum_j (Z_gj - sqrt(a_g b_j))^2 = mn(n-1) v_g

The constant cancels upon normalizing across genes. Thus the saved
scaled-variance shares and the old Z-based shares agree for these
runs; the maximum measured difference is at most 1.6e-12 percentage
points (`out/panelC_sweep_review/validate.log`). The differences between
this draft and the old C come from the simulation inputs/settings and
binning, rather than from a different variance-share metric.
This correction was explained to the user.

Optional tie-breaking sensitivity was checked independently by the
reviewer; no ranks or plotted data were changed. Missing generation
provenance remains a limitation; parameter labels follow the saved
FRACTION/DISPERSION/NORMAL_SD/MUL_SD fields and the supplied pipeline,
not a verified generation-script commit.

Proposed house rules, not applied to AGENTS.md:

- 2026-10-28: Check whether two variance-share definitions coincide under
  the fitted scaling before describing them as different quantities.
- 2026-10-28: Export manuscript PNG previews onto an explicit opaque white
  background so transparency does not hide curves or line styles.

# Simulation pipeline review and companion code

Input: `/data/current_pipeline.R` (reviewed 2026-10-28).
Companion: `artifact/20261028_simulation_helpers.R`. Run R from the manuscript
root, using its renv. The input script and package repository were not edited.

Implementation source: GeneralDualSimplex **0.29.0**, package commit
**bfd5ce69987c17e5a1253a477e9b73e965afc1aa**; `git status --porcelain R src`
was empty. All package paths below are relative to
`/workspace/dual_simplex_functional/general_dual_simplex` at that commit.
The manuscript renv currently has **0.28.0** installed; see the setup finding.
Related package decision: `.ai/decisions.md`, section
`2026-10-27 — EvaluateBenchmark adds NNLS references: H on the true W, W on the
true H`, at the same full package commit above.

## Verdict and metric priorities

The existing benchmark covers most global recovery metrics. Add run-quality
records and inspect component-specific recovery before expanding the metric list.
The following are recommendations, not changes to the scientific assumptions.

| Location | Finding | Recommendation |
|---|---|---|
| Input lines 125, 131; package `R/benchmark.R`, `EvaluateBenchmark` | Already includes spectral ratio; principal-angle sines and oracle projection RMSE on both sides; correlation, RMSE and total variation; and NNLS references that know the other true factor. Factors are matched by H error; estimated negatives are clipped and columns renormalized before the recovery metrics. | Keep these. Do not add duplicate global metrics. Treat NNLS as a reference estimator, not a universal lower bound. |
| Input lines 121–133; package `R/dso-optimization.R`, slots and stopping documentation | No experiment summary records solver outcome, termination reason, iterations, loss, link error or runtime. Most solver fields already remain in the saved DSO. `converged` can include `step_min`, which by itself is not a convergence or feasibility test. | Put these in an experiment summary, time fitting separately from evaluation, and record warnings/errors without stopping the grid. Interpret stop reason together with final loss: `step_min` can occur at numerical zero loss. Report failures and stops with loss above a stated numerical tolerance, as well as errors among usable fits. |
| Input line 125; package `R/benchmark.R`, `fit_metrics` and preprocessing | Global averages can conceal a missing or inaccurate component, and preprocessing hides raw negativity. | Retain matched per-component H RMSE and W-share TV or RMSE, the worst component, error against true prevalence, and marker/background strata for W. Record negative fraction and negative mass before clipping, nonpositive deconvolution mass weights, and deviation of raw H column sums from one. Use the same H-based permutation for W. |
| Input line 125 and the new `true_vertices` field | Feasibility and accurate subspaces do not establish that the recovered simplex has the true vertices. | Add matched projected-vertex error on both sides, with average and worst-component Euclidean distance over dimensions `2:K`. Reuse the benchmark's H-based component permutation for both sides. Interpret it alongside factor error, oracle projection error and positivity loss. |
| Input lines 67–87 | Entropy, ranks, totals and variances describe the simulated objects; they do not measure recovery. | Keep these as covariates. Add sample depth, zero fraction, retained row/column counts, and minimum component prevalence for interpreting low-depth and rare-component failures. |
| Input line 114 versus lines 40–45; package `R/dso-optimization.R`, `FindSolution.DSProjection` | `set.seed(SEED)` controls the noise draw, but `FindSolution` has its own pinned default `seed = 1L`. | Save separate truth/noise/optimization seeds. Keep `seed = 1L` if a shared optimizer start is deliberate; pass an explicit optimization seed and use multiple starts if initialization variability is a target. |

Additional check if needed: signal reconstruction error against the correctly
depth-scaled noiseless mean. Reconstruction
error alone cannot assess simplex recovery: for this positivity solver the fitted
product is fixed by the rank-K projection up to numerical link error. Vertex
distances depend on the coordinate scaling; compare within a fitted map, and do
not pool raw distances across marginal schemes as though units were identical.
Sources: package `R/dso-optimization-post-processing.R`, `GetFactors`;
`R/dso-projection.R`, reconstruction methods.

## Setup and correctness findings

- **Setup blocker:** the manuscript renv's installed 0.28.0 does not export
  `EvaluateBenchmark`, `ApplyMultiplicativeNoise` or `ApplyNormalNoise`.
  The current package checkout, 0.29.0, exports all three. Update the installed
  package in the environment that will run the grid before using this script.
  Updating another repository is outside this review. The helper itself does
  not require these three functions.
- **Additional environment gap:** `data.table` is absent from this renv, so
  the input's first line also fails here. The other directly used helper
  packages (`magrittr`, `glue`, `purrr`, `dplyr`, `matrixStats`) are present.
  No dependency was added. The companion uses base data.frames and requires
  only the already approved GeneralDualSimplex package.
- **Zero marginals:** input lines 35–46 do not handle all-zero observed rows or
  columns. Low-depth count draws can produce them; scaling/projection can then
  fail. Decide how to filter them and record exclusions before running a large
  grid. Also cap the requested projection dimension by the retained dimensions;
  `max(20, K + 10)` can exceed a small input's dimensions. Sources:
  package `R/dso-scaling.R`, `ScaleDSO.default`; `R/dso-projection.R`, `dual_gsvd`.
- **Keep an error row:** `pmap` at input line 113 aborts on an uncaught error.
  Preserve parameters, warning/error text, stage, and elapsed time for failed
  runs, rather than silently excluding them.
- **Name matching after filtering:** the supplied extra-statistics function
  assigns all truth rows/columns positionally. If the data are subset or reordered
  before `CreateDSO`, align truth to the metadata names. If using `FilterDSO`,
  its metadata still covers the original full data axes; align to those axes
  when filling metadata. The vertex helper instead subsets to active projection
  axes, as required for its matrix products.
- **Marker label pattern:** input line 75 uses `".\\d+$"`; use
  `"\\.\\d+$"` to require a literal dot. Both already handle `marker1.2`;
  this robustness change leaves the current marker factor values unchanged.
- **Noise comparability:** multiplicative noise has multiplier mean
  `exp(sd^2 / 2)` and additive normal noise is clipped at zero. Do not assume
  these are mean-preserving or directly equivalent to a Poisson depth setting.
  Sources: package `R/simulation.R`, `ApplyMultiplicativeNoise`, `ApplyNormalNoise`.

## Store the projected true vertices

Source the helper before the experiment loop:

```r
source("artifact/20261028_simulation_helpers.R")
```

Insert this after `calculate_extra_stats(dso)` and **before** deleting
`dso@misc$ground_truth`:

```r
dso <- save_projected_truth(dso, dso@misc$ground_truth)
dso@misc$ground_truth <- NULL
```

The default saves dimensions `1:K`, including the constant first coordinate.
Use `dims = seq_len(dso@projection$k)` if all retained dimensions are needed.
Access the results with:

```r
dso@misc$true_vertices$Omega  # dimensions x true components
dso@misc$true_vertices$X      # true components x dimensions

# For a two-dimensional overlay on the package's GSVD plots:
t(dso@misc$true_vertices$Omega[c("dim2", "dim3"), , drop = FALSE]) # samples
dso@misc$true_vertices$X[, c("dim2", "dim3"), drop = FALSE]        # features
```

The helper keeps true component names/order and the scaling/projection ids.
It does not relabel them to the fitted, mass-ordered components. Match identities
before computing a vertex error. `DualPlot` does not draw this user field
automatically; the matrices supply coordinates for an added overlay.

For the retained true factors and the run's fitted weights, define
`w = colSums(D_r W)`, `h = rowSums(H D_c)`. Column-normalize `D_r W` and
row-normalize `H D_c` to obtain `W_tilde` and `H_tilde`. The saved coordinates are

\[
\Omega_{\rm true}=\Phi_{d,*}\widetilde W,
\qquad X_{\rm true}=\widetilde H\Psi_{d,*}^{T}.
\]

These follow by applying the same linear maps as the observed normalized
profiles. A pure normalized sample is a column of `W_tilde`, mapped by `Phi`;
a pure normalized feature is a row of `H_tilde`, mapped by `Psi^T`.
In noise, these are projected true vertices, not an envelope fitted to the noisy
point cloud, and they need not satisfy the observed solution's link equation.
The noisy run's weights must be used; a projection fitted on noiseless truth
would put the vertices in another coordinate system.
The current count grid uses one scalar depth fraction per run, which cancels
in profile normalization. For sample-specific depth multipliers `L`, pass the
effective factor `H D_L` to this helper when projecting the depth-scaled signal's
feature profiles; `Omega` is unchanged by those column-depth multipliers.
Sources: manuscript `README.md`, mathematical notation; package
`R/dso-projection.R`, `DSProjection`; `R/dso-visualization.R`, `build_proj_panel`;
manuscript `figure/fig1/panelA/points.R`, `project_genes`.

## Reduce saved RDS size

First try the lossless change `saveRDS(experiments, file, compress = "xz")`.
Measure gzip versus xz on representative runs: compressed size and write time
depend on noise, dimensions and history length.

If only the current K-component fit, `1:K` reduction and benchmark metrics are
needed, replace input line 39 with:

```r
FindProjection(k = K + 1L, method = "svd")
```

The extra singular value preserves `spectral_ratio`; the fit, oracle errors and
principal-angle metrics use only the leading K dimensions. Higher-rank
diagnostics would need a larger projection. This is a proposed parameter choice,
not an edit to the input. Source: package `R/dso-projection.R`, `FindProjection`;
`R/dso-optimization.R`, `FindSolution.DSProjection`; `R/benchmark.R`.

The companion also removes R6 method environments from the serialized form,
while preserving their numeric fields and rebuilding the public package classes
on read. This does not change the fitted DSO in memory:

```r
save_simulation_rds(experiments, "out/experiments_packed.rds")
experiments <- read_simulation_rds("out/experiments_packed.rds")
```

This uses xz and retains histories by default. Use the companion reader;
`readRDS()` alone returns packed lists in the `result` column. Load with the
same GeneralDualSimplex version: the stored `package_version` identifies it;
this format is not a cross-version migration mechanism. Keep the package source
commit and session information with the simulation run.
The saved experiment table is a base data.frame. In a data.table workflow, use
`data.table::setDT(experiments)` after reading it.

If trajectories and warm starts are no longer needed:

```r
save_simulation_rds(experiments, "out/experiments_final.rds",
                    keep_history = FALSE)
```

This additionally removes optimizer histories and trajectories. Endpoint factors,
raw endpoint state, solver summaries, metadata, reductions, observed data,
evaluation and projected true vertices stay. Use `DualPlot(..., history = FALSE)`
after loading such an object. History plots and warm-start continuation are not
supported for the trimmed archive. The original in-memory table is unchanged.
The flag is `dso@misc$storage$history_removed`. If default `DualPlot(dso)` reports
`dim(X) must have a positive length` or a warm start reports
`'dims' cannot be of length 0`, check that flag; load an archive with histories
for those operations, or use `history = FALSE` for endpoint plots.

Avoid replacing `@data` with an empty or zero matrix: this breaks the object's
relationship to its filters, metadata and lineage, and loses downstream data
access. If only summary metrics and vertices are needed, archive an explicitly
smaller plain list/table rather than presenting it as a complete DSO.
Store `base_runs` once, keyed by a stable simulation id; do not put W/H back into
every result just to preserve access to truth. The two marginal schemes also
share the same observed matrix for each noise/seed setting. For larger archives,
a custom data pool keyed by `data_id` can store that matrix once, with per-fit
states referring to it and the reader restoring `@data` before building each
DSO. The current helper keeps a complete data matrix in every packed result.
Sparse storage can help genuinely sparse count matrices; it need not help dense
multiplicative-noise matrices.

## Validation and size measurements

The focused checks passed using the current 0.29.0 package installed into a
temporary library from a temporary source copy. Neither repository's installed
package was changed. Reproduce from the manuscript root after the current
package is available:

```sh
RENV_CONFIG_SANDBOX_ENABLED=FALSE Rscript artifact/20261028_simulation_validation.R
```

The script's optional first argument prepends a temporary package library. The
run here used `/tmp/20261028_pipeline_library`. Source:
`artifact/20261028_simulation_validation.R`; complete output:
`out/20261028_simulation_validation.log`; measurements:
`out/20261028_simulation_validation/size_measurements.csv`, table columns
`format`, `bytes`, `write_seconds`; session:
`out/20261028_simulation_validation/sessionInfo.txt`.
Package version/commit are stated at the top. Manuscript base commit:
`bf3efe48bd5124ab80ae53b069687b2233d928ae`; these companion and validation scripts
are introduced by this change after that base, not contents of that historical
commit.

Checks cover both marginal schemes with noiseless, Poisson, multiplicative and
clipped normal observations; direct maps, constant coordinates and convex
combinations; the noiseless true-mass link identity; subset/reordered
feature/sample axes and extra projection
dimensions; lossless roundtrip of factors, scaled data, barycentric coordinates,
lineage, evaluation, optimizer history and trajectories; trimming without
mutating the original; and QP/alignment history formats as well as positivity.
Restored R6 objects are separate instances even for repeated input references.
This verifies the pipeline's standard package fields; custom R6 methods or
user-added R6 bindings are outside the archive format.
An additional check found identical leading K coordinates and first K+1 singular
values when retaining 4 rather than 20 dimensions on every fixture; record:
`out/20261028_simulation_validation/projection_dimensions.log`.

Illustrative fixture: `GenerateMixture(180, 70, 3, n_marker = 6, marker_fold = 5,
profile_spread_sd = 0.2)`, random seed 53. Four observation types, each with
expression and uniform scaling; projection dimension 20, solution dimension 3,
random initialization with the package's default optimization seed and
`step_init = 0.1`. Poisson uses `dispersion = 0`, `library_size_fraction = 0.08`;
multiplicative uses `sd = 0.25`; normal uses `sd = 3`. Eight DSOs are archived
together as one base data.frame. These are illustrative storage measurements,
not simulation findings or estimates of production savings. Write times are
single measurements, not timing benchmarks.

| Archive | Bytes | Write seconds |
|---|---:|---:|
| Full DSO, gzip | 3,037,820 | 0.235 |
| Full DSO, xz | 1,541,164 | 1.130 |
| Packed DSO, xz, all history | 1,451,092 | 0.760 |
| Packed DSO, xz, history removed | 699,896 | 0.242 |

On this fixture, changing compression alone accounts for most of the lossless
saving; constructor-field packing gives a further reduction. Re-measure on the
actual experiment table before choosing a storage policy.

The unavailable `out/simulation_ground_truth_k3.rds`, unspecified grid vectors,
and missing data.table prevent running the user's complete grid here. A real
data.table input/output path was not exercised in this renv; the helper converts
to a base data.frame before changing its list-column.

Independent review: Claude, profile `Advisor - Claude`, reviewed the formulas,
plot conventions, alignment, roundtrip, trimming, dimension reduction and cited
package behavior. Initial verdict: accept after minor revisions; report:
`artifact/20261028_simulation_review.md`. Revisions correct the interpretation
of `step_min`, promote matched vertex error, clarify the marker-pattern and depth
caveats, document trimmed-object errors, remove a redundant loop and add the
noiseless link check. Final verdict: **accept**; all six findings addressed.

Proposed house rule from review: "2026-10-28: Run plotting checks with
`pdf(NULL)` or write to `out/`; non-interactive R writes `Rplots.pdf` into the
working directory." This proposal has not been added to AGENTS.md.
Also proposed after correcting the audit: "2026-10-28: Interpret a solver's stop
reason together with loss and feasibility; state a numerical tolerance before
classifying a run as unsuccessful."

## User follow-up before commit

The user explained that the additional projection dimensions are intended for
future spectral plots. Retaining a longer spectrum while saving only the first
K+1 bases remains a proposed storage option; the companion currently preserves
all supplied projection dimensions.

The user is considering dropping trajectories and regenerating them through
seeded replay. The discussion covered retaining the projection, optimizer start,
seed, solver parameters and software environment. The companion retains the
optimizer start, seed and explicit parameters when history is removed; its
default still retains history. No spectrum-trimming or replay function was added
in this follow-up.

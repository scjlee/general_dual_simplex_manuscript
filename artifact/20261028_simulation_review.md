# Review: simulation helper and pipeline note (2026-10-28)

Reviewer: Claude (Advisor), read-only. Reviewed the files as of 2026-10-28,
including the author's later edits (base data.frame, `storage` annotation,
`k = K + 1L` proposal, validation section).

- `artifact/20261028_simulation_helpers.R` (92 lines)
- `artifact/20261028_simulation_pipeline.md` (252 lines)

Package source: GeneralDualSimplex 0.29.0, commit
`bfd5ce69987c17e5a1253a477e9b73e965afc1aa`; `git status --porcelain R src` is
empty. Checks ran from `/tmp/20261028_pipeline_library`. Scripts: `check.R`,
`check2.R`, `check3.R` in this folder. All fixture numbers are illustrative.
Fixture: `set.seed(7); GenerateMixture(600, 80, 3, n_marker = 20, marker_fold = 5)`,
with the input's `run_pipeline` settings.

## Verdict

**Accept after minor revisions.** The vertex formula, matrix orientation, axis
alignment, R6 roundtrip and history trimming are correct. I reproduced each of
them independently. One item in the metric audit needs a change (F1). The rest
are wording, dead code or caveats.

## Independent confirmations

- **Formula.** `Omega = Phi[d,] %*% W_tilde` and `X = H_tilde %*% t(Psi[d,])`
  match README notation (`Omega = Phi W~`, `X = H~ Psi^T`, with
  `W~ = D_r W D_w^-1` and `H~ = D_h^-1 H D_c`). On noiseless data, the saved true
  vertices satisfy the link with the true mass, `Omega M X = diag(sigma_1..K)`.
  The maximum error was 2.2e-16 (expression) and 2.0e-15 (uniform), and
  `sum(M) = 1`. This test could have failed, so it is real evidence for the
  formula and the orientation.
- **Plot coordinates.** `DualPlot` draws sample points from `t(sigma * Psi)`
  (`R/dso-reduction.R:102`) and fitted vertices from `t(Omega[dims, ])`
  (`R/dso-visualization.R:358-362`). The sample points equal `Phi %*% V_fs`
  within 2e-15, and the feature points equal `V_ss %*% t(Psi)` within 1.2e-14.
  So the saved true vertices share the plotted coordinate system. Row names
  `dim1..dimK` come from `FindProjection` (`R/dso-projection.R:165-172`), so
  `Omega[c("dim2","dim3"), ]` in note lines 95-97 is valid.
- **Axis alignment.** Helper lines 6-7 subset the truth by
  `colnames(Phi)` and `colnames(Psi)`. These are the scaled active data's names,
  and so they follow the order of `scaling$r` and `scaling$c`. The positional
  `sweep` at lines 10-13 is therefore aligned.
- **R6 packing.** The packed field lists match the `initialize` arguments of
  `DSScaling` (`R/dso-scaling.R:27`) and `DSProjection` (`R/dso-projection.R:28`).
  After a roundtrip, every slot is `identical`, every R6 field including `id`
  is identical, `validObject` passes, `Lineage` shows nothing stale,
  `GetFactors` is identical and `DualPlot` works. `DualSimplexObject` has no
  custom `initialize` method, so `new()` rebuilds the object directly.
- **R6 overhead (fixture).** Uncompressed, the R6 objects serialize to
  2.25 MB (scaling) and 2.35 MB (projection), against 38 KB and 143 KB for their
  fields. With xz, the gap shrinks to 95 KB and 190 KB. One DSO took 473,964 B
  as plain xz, 389,784 B packed with xz, and 164,784 B packed and trimmed.
  This is consistent with the note's statement (lines 243-245) that compression
  gives most of the lossless saving.
- **Trimming.** The trimmed object's evaluation is identical. Warm start fails
  as the note says. The in-memory table is unchanged.
- **`k = K + 1L` (note lines 134-145).** I confirmed this independently on a
  Poisson fixture with uniform scaling. The solution differed by 0 and
  `EvaluateBenchmark` by 0 (same NA pattern). Phi and Psi took 99,660 B with xz
  at k = 20 and 16,604 B at k = 4. The result holds for `method = "svd"`; with
  `irlba` it is only approximate (`FindSolution` documentation).
- **Package claims checked against the code:**
  - `EvaluateBenchmark` contents: `R/benchmark.R:50-90`.
  - Matching by H error and clipping: `R/benchmark.R:55-57`.
  - `step_min` counts as "converged": `run_outcome` at
    `R/dso-optimization.R:480-488`.
  - `seed = 1L` is pinned: `R/dso-optimization.R:169,189`.
  - Multiplicative mean `exp(sd^2/2)` and normal noise clipping:
    `R/simulation.R:304-305,340`.
  - The renv has 0.28.0 and its NAMESPACE lacks all three exports.
  - `data.table` is absent from the renv. The other helper packages are present.
  - A zero row with expression scaling fails with "infinite or missing values
    in 'x'". `CreateDSO` drops zero rows only on the Seurat path
    (`R/dso-object.R:192-193`).
  - The cited package decision `2026-10-27 — EvaluateBenchmark adds NNLS
    references` exists.
  - The size table matches `size_measurements.csv`.

## Findings

**F1 (medium; audit) `artifact/20261028_simulation_pipeline.md:25` and `:30-35`.**
The table treats `step_min` as a "stall" and asks for "failure and stall rates".
On the fixture, all 10 noiseless positivity fits (2 scalings × seeds 1-5)
stopped at `step_min` and were labelled `converged`. Their loss was
≤ 2e-17, so they were feasible, not stalled. Yet H RMSE was 0.079-0.101, while
H `sin_max` was ≤ 2.2e-8. The fitted vertices lay 0.13-0.19 from the true ones,
on a vertex scale of 0.18-0.24.

The subspace is exact, but the chosen simplex is not the true one. This is
consistent with zero-loss positivity solutions not being unique. The
optimization seed changes which one the solver returns: seed 2 gave 0.079,
other seeds about 0.10.

Proposed changes:

- Report `stop_reason` together with `loss`, so that `step_min` at zero loss is
  not counted as a stall.
- Promote the matched projected-vertex distance from "Additional checks if
  needed" to a primary metric, or add a simplex-size measure (fitted against true
  simplex volume in the same map). Neither the existing metrics nor the proposed
  run-quality records can separate "feasible but wrong simplex" from estimation
  noise. The new `true_vertices` field makes this metric cheap.

These are fixture observations, not simulation results. Whether this holds on
the real grid is open; see Q1.

**F2 (low; wording) `artifact/20261028_simulation_pipeline.md:67-68`.** The
current pattern `".\\d+$"` already maps `marker1.2` to `marker1`, because `.`
also matches a literal dot. The two patterns differ only on names without a dot
suffix: `background539` becomes `backgroun`. Those names become NA in either
case, because the factor levels are `marker1..K`. Reword this as a robustness fix
that does not change the current output.

**F3 (low; dead code) `artifact/20261028_simulation_helpers.R:53-57`.**
`raw$runs[[i]]` comes from `run_record` (`R/dso-optimization.R:358-368`). It
holds only `init`, `params`, `seed`, `iterations`, `stop_reason`, `outcome` and
`loss`, never history fields, so the loop does nothing. Delete it; the README
coding style says not to write defensive code.

**F4 (low; usability) `artifact/20261028_simulation_pipeline.md:171-175`.** On
a trimmed object, the default `DualPlot(d)` fails with "dim(X) must have a
positive length", and `FindSolution(warm_start = TRUE)` fails with "'dims'
cannot be of length 0". Quote these messages, and point to
`@misc$storage$history_removed` so readers can recognise the cause.

**F5 (low; caveat) helper lines 7 and 12-13; note lines 105-123.** `X_true`
uses the undepth-scaled `H`. This is exact here because the input's `FRACTION`
is a scalar per run, so the depth factor cancels in the row normalization. The
multiplicative noise mean factor is also a scalar. With per-sample
`library_size` or fraction vectors, `X_true` would need `H D_L`. `Omega_true`
does not change. Add one sentence.

**F6 (suggestion; validation) `artifact/20261028_simulation_validation.R`.**
The script has no check of the noiseless link identity
`Omega_true M_true X_true = diag(sigma_1..K)`, with
`M_true = diag(colSums(D_r W) * rowSums(H D_c))`. This identity is the most
direct test of the formula in the package's own coordinates. Consider adding it
next to the existing map and convex-combination checks.

## Questions

- **Q1.** Is the positivity solver meant to select the true simplex among
  zero-loss solutions? If yes, F1 points to a solver issue for the package
  record. If no, the manuscript benchmark needs a vertex or volume metric to make
  this visible.
- **Q2.** Will higher-rank diagnostics be needed later? This decides whether
  `k = K + 1L` is safe for the archive.
- **Q3.** The note proposes a shared observed-data pool keyed by `data_id`
  (lines 182-186). Is that worth building now? The per-fit `@data` was small on
  count fixtures (21 KB xz) but will be larger for dense multiplicative noise.

## Housekeeping

My `DualPlot` check, run from a non-interactive `Rscript` at the repository
root, created `Rplots.pdf` (00:25:22, 6 seconds after `check.R` was written). I
moved it to `out/20261028_simulation_review/Rplots_from_review_check.pdf`.
Proposed house rule: "2026-10-28: Run plotting checks with
`pdf(NULL)` or write to `out/`; non-interactive R writes `Rplots.pdf` into the
working directory."

## Final verdict after revisions (2026-10-28)

**Accept.** I checked each revision against its finding. I did not rerun the
full checks.

- **F1:** fixed. Line 25 of the note now says to read the stop reason together
  with the final loss, and to report stops with loss above a stated tolerance.
  Line 27 makes the matched projected-vertex error a primary metric, with mean
  and worst-component distance over dimensions `2:K`, using the benchmark's
  H-based permutation. Lines 31-36 keep the warning about coordinate scaling.
- **F2:** fixed at lines 68-70. They now say the current output is unchanged.
- **F3:** fixed. The loop over `raw$runs` is gone (helper lines 48-54).
- **F4:** fixed at lines 182-184. The note names the flag and quotes both error
  messages.
- **F5:** fixed at lines 126-129. The `H D_L` caveat is correct, and `Omega` is
  indeed unaffected.
- **F6:** added at `artifact/20261028_simulation_validation.R:45-50`. Its
  `true_mass = (W^T r) * (H c)` matches the README definition `w * h`. The
  check stops on any error above 1e-10 (line 22).
  `out/20261028_simulation_validation.log` was written 11 seconds after the
  script's last change and ends "All focused checks passed", so the check
  passed. That run covered the noiseless fixtures with both scalings.

**Still open:** questions Q1-Q3. Whether the house rule enters AGENTS.md is the
lead's decision.

# Review: noise grid helper matched on mean noise variance

Recipient: Codex reviewer (profile Advisor - Codex). Role: Reviewer, read-only.
Repository: `/workspace/dual_simplex_functional/general_dual_simplex_manuscript`
(Paseo workspace `wks_f1fc0452fbbda285`). Read `AGENTS.md` first.

## Files to review

- `artifact/20261028_noise_grid.R`: the helper `find_grid_points()`.
- `artifact/20261028_noise_grid.md`: derivation, rounding rule, validation.
- `artifact/20261028_noise_grid_validation.R`: checks.

Write your review only to `out/20261028_noise_grid_review/review.md`. Edit
nothing else. Do not edit, stage or commit in any other repository.

## Purpose

The user sweeps noise models over base simulations
(`/data/simulation_ground_truth_k3.rds`: a data.table with K, MARKER_FOLD,
SEED and a list column `simulation` of `list(W, H)`). The helper returns
`list(fraction, normal_sd, mul_sd, dispersion)` such that Poisson, Normal
and multiplicative noise have the same expected mean per-entry noise
variance, in units of V* = W H, at each target. Values are rounded to
"nice" decimals. NB reuses the Poisson fractions and is not matched.

## Check

1. Mathematics. Compare each variance formula with the noise functions in
   the package source at commit `bfd5ce69987c17e5a1253a477e9b73e965afc1aa`
   (GeneralDualSimplex 0.29.0, `R/simulation.R`: `ApplyNBNoise` with
   `library_size_fraction`, `ApplyNormalNoise`, `ApplyMultiplicativeNoise`).
   Use `git -C <package> show bfd5ce6:R/simulation.R`; the package is at
   `/workspace/dual_simplex_functional/general_dual_simplex` and is read-only.
   Check the scale divisors, the inverses, the NB floor and the
   clipped-Normal expression σ²(Φ(a) − aφ(a)) + μ²Φ(−a). Check that the
   claim "the pipeline does not depend on a global factor of the data" holds
   for `ScaleDSO(type = "uniform")` and `"expression"` (`R/dso-scaling.R`).
2. Code. Pooled moments, `nice_value` (decade, step order, tolerance test,
   mantissa rounding up to 10, floating-point output), `mapply` use, the
   `details` columns. Are the returned values monotone for doubling targets?
3. Run `Rscript artifact/20261028_noise_grid_validation.R` from the
   repository root. It uses a scratch library at
   `out/20261028_marginal_check/lib` holding package 0.29.0 built from the
   commit above; the renv holds 0.28.0. Compare the output with the numbers
   in the note. Recompute at least two values independently.
4. Style: the "Coding style guides" section of `README.md` (simple code,
   no defensive checks).
5. Any statement in the note that the evidence does not support.

## Return

Verdict (approve / approve with changes / reject), findings with file and
line, severity, and open questions. Put the full review in the file above
and a short summary in your last message.

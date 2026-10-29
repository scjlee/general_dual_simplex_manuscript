# Independent review: noise level relative to signal variance

Recipient: fresh Advisor - Claude, profile settings copied unchanged.
Repository: `/workspace/dual_simplex_functional/general_dual_simplex_manuscript`.
Workspace ID: `wks_f1fc0452fbbda285`.
Role: Reviewer. Read README.md and AGENTS.md first.

The user explicitly requests: "Please send our discussion about formulation to Claude for an independent review. And tell me how much difference will this modification make comparing to the current setting."

Review the formulation independently; challenge the lead's recommendation and assumptions. Do not assume the prior committee establishes correctness. Give a verdict, findings with file/line or quoted statement, and unresolved scientific choices. No changes to the helper or manuscript are authorized. You may write only `artifact/20261029_noise_formulation_review.md` and scratch work under `out/20261029_noise_formulation_review/`. Other repositories are read-only.

## Discussion to review

The study compares marginal choices (e.g. uniform and expression) across noise models. Initially the user requested a noise metric independent of "any scaling." We distinguished (a) one calibration held fixed across preprocessing choices, (b) invariance to a common global multiplier, and (c) numerical invariance under arbitrary positive diagonal row/column rescaling of the same signal-observation pair.

For literal (c), the lead and a prior committee proposed entrywise relative MSE, q_entry = mean_ij E[((X_ij - mu_ij)/mu_ij)^2 | mu], requiring strictly positive mu, with equal fractional weighting, sensitivity to small entries and undefined zeros. This is invariant on the same rescaled pair, but does not make regenerating noise with unchanged scalar parameters equivariant.

For comparing marginal methods, the lead instead recommended expected relative Frobenius error q_F = E||X-mu||_F^2 / ||mu||_F^2 in a fixed original representation. The primary argument is paired design: identical signal and identical noisy observation for all marginal choices; matching after each marginal choice would change input along with treatment. Both q_F and q_entry can support valid experiments. q_F weights fractional errors by mu^2 and does not have arbitrary diagonal invariance. No claim of universal neutrality or proven superiority is intended. Fixed-reference spectral calibration can also preserve pairing; it is not inherently invalid.

The user then proposed: noise level 1 means additional noise variance equals Var_ij(mu), level 2 means twice this variance, 0.5 means half. Here mu = W H, and Var_ij is population variance across all entries around the grand mean, not mean within-gene sample variance.

The lead's proposed definition, for a fixed positive-variance signal:

- S_mu = mean_ij[(mu_ij - mean(mu))^2], divisor mn.
- X is observation corrected by its known model-wide expected multiplier: V/f for Poisson/NB at scalar library fraction f; V/exp(s^2/2) for lognormal multiplicative V=mu exp(Z), Z~N(0,s^2); V for additive Normal BEFORE clipping.
- v = mean_ij Var_noise(X_ij | mu) = mean_ij E[(X_ij-mu_ij)^2 | mu] for conditionally unbiased noise.
- L = v/S_mu. It is a variance ratio; sqrt(L) is the RMS noise to signal SD ratio.
- For a uniformly random matrix entry and a noise draw, Var(X) = (1+L) S_mu by total variance. This is NOT claimed to be an exact identity for the empirical variance of each noisy matrix.
- Compute before marginal preprocessing. Common global rescaling cancels; arbitrary row/column rescaling need not cancel.
- This denominator includes between-gene abundance differences and is not an isolated measure of informative mixture variation or recovery difficulty.
- For several simulation seeds, use mean within-matrix population variance for a setup-level denominator (entry-weighted if matrix dimensions differ); numerator is likewise pooled mean noise variance. This matches the ratio of averages, not each seed's individual level or the mean of per-seed ratios.
- Known model-wide correction is defined by generating parameters, never fitted from each noisy realization; it removes global expected gain, not stochastic noise. Poisson Var(V/f)=mu/f still rises as f falls.
- The prior approved convention matches Normal before clipping. Actual clipped Normal has entry-dependent bias; mean squared error includes bias and is not pure variance. The new label does not fix that mismatch. No global factor removes all clipping bias.

## Current helper and proposed comparison

Read `artifact/20261028_noise_grid.R` and its .md note. Current targets are v = 100 * 2^(0:6); mean_mu and mean_mu2 are pooled. It already divides out the expected Poisson/NB and lognormal multipliers in its theoretical calibration, and already matches Normal BEFORE clipping. NB reuses Poisson fractions at phi=.01,.1; it is not equal-noise matched. The rounding routine has a 3% preference tolerance with a fallback, not a strict guarantee.

Current helper source commit: manuscript `29cb5265b0ad7795666f17ab26fbd317c39ff21b`.
Package: GeneralDualSimplex 0.29.0, source commit `bfd5ce69987c17e5a1253a477e9b73e965afc1aa`; R/src worktree clean at the lead's check. Package files are read-only. Inspect `R/simulation.R` for conventions; no need to read package decision record unless needed (use its decision-log search tool if so).

The lead has added `artifact/20261029_noise_level_comparison.R`, which uses base R plus the existing helper and does NOT modify it. It is computing outputs in `out/20261029_noise_level_comparison/` with a console log at `out/20261029_noise_level_comparison.log`. Review the script and its numerical results when available; you may rerun it or independently recompute.

Input `/data/simulation_ground_truth_k3.rds`: 120 saved W,H simulations (K=3; marker folds 2,5,10,100; 30 seeds per fold; each mu 3000 by 500). SHA-256 `78c62b71a6f6969df3e43404e65096dcd014f41e31c0d82db00563235423c522`. Generating commit of supplied archive is not established; the current package commit is implementation context, not proven archive-generation provenance. These are descriptive calculations on the supplied ground truths, not new recovery experiments.

Requested comparisons:

1. Pure relabelling L_old=v_old/S: zero change in physical simulation parameters or recovery outcomes. The expected mean correction is also ALREADY part of the current helper.
2. Selecting new L values changes v=L*S. The user gave .5,1,2 as examples but has not selected a full replacement grid. For illustration only, compare seven doubling levels 1/8,1/4,1/2,1,2,4,8 with the old seven target positions, preserving current rounding. Report exact target shifts and rounded parameter shifts separately. Do NOT treat this grid as adopted.
3. Calculate NB matched fractions f=mean(mu)/(L*S - phi*mean(mu^2)) only where the denominator is positive. New NB level floor is phi*mean(mu^2)/S, NOT phi. Matching NB is a separate design change from relabelling.
4. Actual clipped-Normal MSE remains a diagnostic; show how far it falls below the nominal pre-clipping L at example levels.
5. Compare denominator variation across marker folds/replicates; evaluate whether a setup-average level hides meaningful variation. Quantify between-gene versus within-gene contribution to S without equating either with recoverability.

Please review the science, algebra, pooling convention, code/results, and whether the lead can quantify parameter changes but cannot predict changes in recovery error without rerunning the study. If files or calculations are not yet available, review the formulation first; the lead will send the completed comparison note shortly. Return your verdict in your final message and save the full report to the assigned review artifact. Do not commit or push anything.

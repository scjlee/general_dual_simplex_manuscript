# Figure 1 caption working notes

These describe the selected content, not new scientific conclusions. The full
original captions are preserved verbatim by PDF text extraction in
reference/outline-text.txt. All simulation-driven plots use the uniform-marginal
runs from `/data/k3_simulation_balanced-population_with-pure_both-marginals.rds`.
The archive's generating commit is unknown. Its SHA-256 is
`a29e8a2719087cb157448d74f004ced80daa0373f10b36d54e39cc145434dc7f`.
The render read saved results using GeneralDualSimplex 0.38.0 at package commit
df4a86591f9cabd3d66ca3af8db54dcd46552733 (clean R/ and src/ at rendering).

A. DualSimplex workflow schematic. The clouds, matrices and trajectories are
illustrative, reused from the existing SVG; they are not measured optimization
trajectories. The lower axes denote scaled expression coordinates.

B. Illustrative signal-generation/perturbation schematic: W, profiles; H,
proportions; V*, true signal; ε, noise; V, observed data. The table is retained
from the outline. ‡ Normal noise is clipped to keep observed data non-negative.
Feature-simplex examples use seed 17, noise level 1/2, and the noiseless
baseline. Points and true vertices are taken from the saved simulations.

C. Deconvolution RMSE for W and H, using the saved evaluation metrics. The
narrow noiseless facet has a ∅ strip and a 0 tick. Metric meanings are
retained; no matrix-reconstruction error is introduced.

D. Variance share by raw expression rank and expression bin, before and after
scaling, at noise level 1/4 with the noiseless baseline. Rank points show means
and ribbons the full range, as in the source Rmd. The rank plot's upper y limit
is the 99.9th percentile of the noiseless variance shares; extreme values are
clipped by that existing limit. Bins are fixed by raw expression rank across
all runs. High covers ranks 1–718, mid covers 719–1436, and low covers
1437–2153. The bin width is the number of ranks divided by three and rounded
up. The final bin contains the remaining ranks. See
`panelD/input_data.rds`, entry `rank`.

E. Signal/noise variance shares by expression bin and in total at noise level
1/4. Source covariance terms are omitted from these share visualizations.
The SNR plot uses post-scaling signal/noise shares across noise levels.
Post-scaling SNR is missing for seed 6 at noise level 2 for Normal and Poisson
noise. These runs have no point in E or F's SNR plots. See
`panelE/input_data.rds`, entry `snr`.

F. Spectrum summary at noise level 1/4 and the noiseless baseline, singular-value
ratios across noise levels, and post-scaling SNR versus singular-value ratio.
Points/lines in the spectrum plot summarize the mean; shading shows the full
range. The original spectrum normalization is retained exactly:
`normalized_spectral = spectral / (Matrix::norm(GetData(result, "biwhitened"), "F")^2 - 1)`.
This is not a variance share. The reviewer flagged its interpretation for an
author decision before submission; no numerical correction was made here.
The scatter uses per-model colour gradients for noise level; the original grey
legend is a light/dark proxy, not the literal point colours.

G. The left and middle boxplots show projection RMSE for W and H. The right scatter shows
paired projection RMSE (`oracle_rmse`) and deconvolution RMSE (`rmse`) for W
and H, with a dashed equality line. It uses saved uniform-marginal runs with
noise levels 1/4, 1/2, 1 and 2. Its grey legend shows how lightness changes
with noise level within each model.

H in simplified version 2. Ratio of projection RMSE to deconvolution RMSE,
using the saved metrics and formula `oracle_rmse / rmse`.

The separate simplified version places the first two plots of F and G on one row. Spectrum legend label ∅
omits “(none)” to fit the narrower plot. Plotted values are unchanged.

The outline's causal claims and broader interpretations were not tested by
this artwork task. All such claims remain draft text for scientific review.
The guide's 225 mm height allowance requires a caption under 50 words; these
notes plus the original captions exceed that. The final submission layout and
caption length must be decided together.

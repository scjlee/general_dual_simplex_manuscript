# Figure 1 caption working notes

These describe the selected content, not new scientific conclusions. The full
original captions are preserved verbatim by PDF text extraction in
reference/outline-text.txt. The source archive's generating commit is unknown;
reference/input-manifest.tsv identifies the supplied inputs by SHA-256.
The plotting implementation is GeneralDualSimplex 0.38.0 at package commit
09dd30edfd7a65715e6ec0261d3ea12b0cd0ee71 (clean R/ and src/ at rendering).

A. DualSimplex workflow schematic. The clouds, matrices and trajectories are
illustrative, reused from the existing SVG; they are not measured optimization
trajectories. The lower axes denote scaled expression coordinates.

B. Illustrative signal-generation/perturbation schematic: W, profiles; H,
proportions; V*, true signal; ε, noise; V, observed data. The table is retained
from the outline. ‡ Normal noise is clipped to keep observed data non-negative.
Feature-simplex examples use seed 17, noise level 1/2, and the noiseless
baseline. Points and true vertices are taken from the saved simulations.

C. Deconvolution RMSE for W and H, using the saved evaluation metrics. The
narrow noiseless facet is labelled 0. Original metric labels and meanings are
retained; no matrix-reconstruction error is introduced.

D. Variance share by raw expression rank and expression bin, before and after
scaling, at noise level 1/4 with the noiseless baseline. Rank points show means
and ribbons the full range, as in the source Rmd. The rank plot's upper y limit
is the 99.9th percentile of the noiseless variance shares; extreme values are
clipped by that existing limit. Bins use the source's pooled rank binning.

E. Signal/noise variance shares by expression bin and in total at noise level
1/4. Source covariance terms are omitted from these share visualizations.
The SNR plot uses post-scaling signal/noise shares across noise levels.

F. Spectrum summary at noise level 1/4 and the noiseless baseline, singular-value
ratios across noise levels, and post-scaling SNR versus singular-value ratio.
Points/lines in the spectrum plot summarize the mean; shading shows the full
range. The original spectrum normalization is retained exactly:
`normalized_spectral = spectral / (Matrix::norm(GetData(result, "biwhitened"), "F")^2 - 1)`.
This is not a variance share. The reviewer flagged its interpretation for an
author decision before submission; no numerical correction was made here.
The scatter uses per-model colour gradients for noise level; the original grey
legend is a light/dark proxy, not the literal point colours.

G. Projection RMSE for W/H and the ratio of projection RMSE to deconvolution
RMSE, using the source's saved metrics and formula `oracle_rmse / rmse`.

The outline's causal claims and broader interpretations were not tested by
this artwork task. All such claims remain draft text for scientific review.
The guide's 225 mm height allowance requires a caption under 50 words; these
notes plus the original captions exceed that. The final submission layout and
caption length must be decided together.

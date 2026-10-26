# Panel C alternative: gene shares of variance in the scaled matrix

Date: 2026-10-26. Requested as a visual comparison only. Illustrative
simulation; no manuscript claim relies on these data. This does not select
a replacement for the current panel C or change the discussion's claims.

Files: `figure/fig1/panelC_vtilde/variance_share.R` generates
`variance_by_gene.csv` (individual replicates) and
`variance_share_by_rank.csv` (plot input); `make_fig1C_vtilde.py` creates
`fig1C_vtilde.svg` using panel C's layout. Later refreshes update only
named data groups. `fig1C_vtilde.png` is the 600-dpi Inkscape preview.
`package_commit.txt` records package provenance.

## Definition and provenance

Interpretation of the requested variance: ordinary within-gene variance
across samples of the scaled observed matrix, including signal and noise.
For each replicate and scaling, fit weights to observed V and compute

```
Vtilde = D_r V D_c
v_g = sum_i (Vtilde_gi - mean_i Vtilde_gi)^2 / (n - 1)
share_g = 100 v_g / sum_h v_h
```

The common `n - 1` cancels in the shares. Thus the denominator is the sum
of row variances, rather than the variance of all entries about one grand
mean. There is no division by row or column marginals and no subtraction
of the independence matrix `a b^T`. This differs from current C's weighted
variation in Z; the preview is a comparison of these choices, not evidence
about projection quality.

Simulation parameters, noise definitions, seeds 1–5 and draw ordering are
copied from `figure/fig1/panelC/noise_share.R`; the signal settings are read
from `figure/fig1/panelA/simulation.rds`. Both source files are at manuscript
commit `a54ec56fafa67e2ec5a9bb72bbd2ad3436bc9608`. Implementation:
GeneralDualSimplex 0.28.0 at package commit
`af56ff97da8e38af7c304513c5d26f1c2ff0c910`; no uncommitted `R/` or `src/`
changes. Weight construction was checked against the package's
`R/dso-scaling.R`, `ScaleDSO.default` and `DSScaling$scale` at that commit.

## Caption draft

**C, Where the variance sits before bi-marginal whitening.** Each gene's share of
the total within-gene variance in the scaled observed matrix Ṽ, against
its rank by observed total. Variance is calculated across samples after
subtracting each gene's own mean; total variance is the sum over genes.
Dots show the mean share of the i-th ranked gene over five independent
simulated replicates; bands show the range. Both scalings use the same
observed matrix within a replicate and noise model. Noise models and
parameters match the current panel C. Each plot has its own logarithmic
y-range. Illustrative simulation for layout comparison only, not a
benchmark or a claim about recovery accuracy.

## Verification

- The Poisson first replicate reproduces panel A's observed matrix.
- All scaled matrices have unit sum. All 30 replicate/scaling allocations
  sum to 100%; saved shares reproduce from the saved variances.
- The row-centred variance calculation agrees with R's `var` applied to
  each row. Every plotted mean and range reproduces from per-gene data.
- The SVG was rendered with Inkscape at 600 dpi and its PNG opened.
  Inkscape query boxes place every text object inside the canvas; subplot
  titles fit their plot widths, and all means and band extrema fit the
  plotted ranges. The rotated y-label fits the plot-height box.
- Refreshing data groups leaves the SVG byte-identical. Existing tracked
  files are unchanged.

No fresh review under the AGENTS.md exemption for illustrative figure data
that support no claim and whose caption identifies them as illustrative.

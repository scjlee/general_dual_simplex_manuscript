# Figure 1B: cumulative scaled versus observed mass

Date: 2026-10-26. Status: draft panel; illustrative data, not a benchmark.

## Caption draft

**B. How each scaling allocates gene and sample mass.** Each point is one
gene (left, 500 points per scaling) or one sample (right, 200 points per
scaling), ordered by observed expression total. The x-axis gives the
cumulative share of the observed matrix total `V`; the y-axis gives the
cumulative share of the scaled matrix total `Ṽ = D_r V D_c`. Expression
scaling divides every count by the same grand total, so its points lie on
the diagonal: its scaled shares equal the observed shares. Uniform scaling
balances `Ṽ` to equal gene masses (1/500) and equal sample masses (1/200).
The dashed line marks 50% of the observed total; numbers give the scaled
share there, by linear interpolation between neighbouring points. Genes that together carry 50% of
the observed counts receive 76.3% of the uniform-scaled mass. Samples are
nearly unchanged (51.4%) because their observed totals vary little (662 to
803 counts). Data: the observed matrix of panel A, one illustrative
simulation (500 genes, 200 samples, three components, Poisson sampling at
library-size fraction 0.04, seed 1; no genes or samples removed).

## Provenance

- Generators (archived with their data and SVG in
  `figure/fig1/panelB/archive/20261026_cumulative/`): `mass.R` (data) and
  `make_fig1B.py` (SVG). Input:
  `figure/fig1/panelA/simulation.rds` from `figure/fig1/panelA/points.R`.
- GeneralDualSimplex 0.28.0 at package commit
  `af56ff97da8e38af7c304513c5d26f1c2ff0c910`, no uncommitted `R/` or `src/`
  changes (`figure/fig1/panelB/archive/20261026_cumulative/package_commit.txt`). Scaling formulas:
  package `R/dso-scaling.R`, `ScaleDSO.default`; masses are the achieved
  `a = rowSums(Ṽ)` and `b = colSums(Ṽ)`, not the targets.
- Values from `figure/fig1/panelB/archive/20261026_cumulative/mass_summary.csv`:

| Quantity | Genes | Samples |
| --- | --- | --- |
| Items | 500 | 200 |
| Uniform scaled share at 50% observed (%) | 76.2762910798122 | 51.3896059782609 |
| Expression scaled share at 50% observed (%) | 50 | 50 |
| Items below 50% observed share (%) | 76.2 | 51.0 |
| Observed total, min–max (counts) | 31–948 | 662–803 |
| Max abs. raw − expression cumulative (%) | 1.42e-14 | 1.42e-14 |

  Uniform balancing converged in 7 iterations, maximum relative marginal
  error 7.99e-13; largest deviation of a gene mass from 1/500 is 1.6e-15.

## Limits

- One fixed-seed simulated matrix chosen for panel A's appearance. The
  sample result reflects this simulation's narrow range of library sizes;
  real data usually vary more. Neither number shows that one scaling
  improves projection (see the discussion note, panels C and D).
- At 45 mm width, 500 gene points overlap except where large genes make
  large steps; the samples are separable.

## Validation

PNG preview opened. `inkscape --query-all`: all objects inside the
134 × 67 mm canvas; legend and labels inside their plots. 1,400 point
circles present. Rerunning `mass.R` and `make_fig1B.py` leaves the SVG
byte-identical.

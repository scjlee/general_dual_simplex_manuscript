# Figure 1B: per-item scaled share against rank (log scale)

Date: 2026-10-26. Status: current draft panel; illustrative data, not a
benchmark. It replaces the cumulative version, archived with its generators
and data in `figure/fig1/panelB/archive/20261026_cumulative/` (caption draft:
`artifact/20261026_fig1B-cumulative-mass.md`). The user chose this layout
because uniform scaling reads directly as a horizontal line.

## Caption draft

**B. How each scaling allocates gene and sample mass.** Each point is one
gene (left, 500 per scaling) or one sample (right, 200 per scaling), ranked
by observed expression total. The y-axis gives that item's share of the
scaled matrix total `Ṽ = D_r V D_c`, on a log scale; the two plots use
different y-ranges (genes 0.01–1%, samples 0.4–0.6%).
Uniform scaling balances `Ṽ` to equal shares: 1/500 = 0.2% per gene and
1/200 = 0.5% per sample. Expression scaling divides every count by the same
grand total, so each share equals the item's share of observed counts.
Under expression scaling gene shares span 0.021% to 0.645% (31-fold), and
36% of genes lie above the uniform share. Sample shares span only 0.451% to
0.547% (1.2-fold), because observed sample totals vary little (662 to 803
counts). Data: the observed matrix of panel A, one illustrative simulation
(500 genes, 200 samples, three components, Poisson sampling at library-size
fraction 0.04, seed 1; no genes or samples removed).

## Provenance

- Generators: `figure/fig1/panelB/mass.R` (data) and
  `figure/fig1/panelB/make_fig1B.py` (SVG). Input:
  `figure/fig1/panelA/simulation.rds` from `figure/fig1/panelA/points.R`.
- GeneralDualSimplex 0.28.0 at package commit
  `af56ff97da8e38af7c304513c5d26f1c2ff0c910`, no uncommitted `R/` or `src/`
  changes (`figure/fig1/panelB/package_commit.txt`). Scaling: package
  `R/dso-scaling.R`, `ScaleDSO.default`; shares are the achieved masses
  `a = rowSums(Ṽ)` and `b = colSums(Ṽ)` times 100, not the targets.
- Values from `figure/fig1/panelB/mass_summary.csv`:

| Quantity | Genes | Samples |
| --- | --- | --- |
| Items | 500 | 200 |
| Uniform share (%) | 0.2 (max deviation 1.6e-15 as a fraction) | 0.5 (max deviation 8.7e-19) |
| Expression share, min–max (%) | 0.0210983–0.645201 | 0.450552–0.546515 |
| Expression max/min | 30.58 | 1.213 |
| Items with expression share above uniform (%) | 35.8 | 50.5 |
| Observed total, min–max (counts) | 31–948 | 662–803 |

  Uniform balancing converged in 7 iterations, maximum relative marginal
  error 7.99e-13.

## Limits

- One fixed-seed simulated matrix chosen for panel A's appearance. The
  narrow sample spread reflects this simulation's library sizes; real data
  usually vary more. The panel defines the two scalings; it does not show
  that either improves projection.
- Separate y-ranges (user decision, 2026-10-26): genes 0.01–1%, samples
  0.4–0.6%. The sample axis is magnified about 11 times in log units
  (2 decades versus 0.176 decade), so its spread must not be compared
  visually with the genes. Every plotted share lies inside its range; the
  generator prints a note if new data fall outside.

## Validation

PNG preview opened. `inkscape --query-all`: all objects inside the
134 × 67 mm canvas. 1,400 point circles present. Rerunning `mass.R` and
`make_fig1B.py` leaves the SVG byte-identical.

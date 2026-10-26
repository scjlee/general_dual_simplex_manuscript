# Figure 1 discussion: scaling, noise, and retained mixture information

> **Status (2026-10-26, later):** superseded in part. The current design is
> bi-whitening in panel A and per-gene squared-noise shares in `Z` in panel C;
> see `artifact/20261026_fig1C-noise-share.md`, `artifact/20261026_fig1B-rank-log-share.md`
> and the last Figure 1 entries in `artifact/decisions.md`. Text below is kept as history.

Date: 2026-10-26. This records the current brainstorming direction, not an
approved final figure or a benchmark result. The package context is
GeneralDualSimplex 0.28.0 at commit
`af56ff97da8e38af7c304513c5d26f1c2ff0c910`, with no uncommitted `R/` or
`src/` changes. Earlier background and derivations are in the package's
read-only, untracked working-tree note
`.ai/20261026_manuscript-figure1-discussion-summary.md`, read on 2026-10-26
with that package HEAD; the note itself is not part of the commit. The
current manuscript notation is `V* = WH` for the signal, `V` for
observations, `Ṽ = D_r V D_c` for the scaled matrix, and
`Z = D_a^(-1/2) Ṽ D_b^(-1/2)` for the matrix sent to the SVD
([README](../README.md), Mathematical Notation).

## Reader narrative

The early Figure 1 mock used phrases such as “survived information,”
“exposure versus RMSE,” and “noise concentrate.” The user found them too
vague for a first-time reader. The discussion moved toward one question per
panel:

| Panel | Question | Current direction |
| --- | --- | --- |
| A | What is being compared? | Keep the existing schematic: one mixture and observation, two scaling choices, and projected gene clouds. |
| B | How does each scaling allocate mass across genes? | A cumulative gene-rank versus cumulative mass-share plot. |
| C | Where does measurement variability enter the matrix being projected? | Conditional noise contribution in `Z`, shown against gene abundance, with a composition-related signal comparison if it can be defined clearly. |
| D | What mixture information remains after projection? | A paired oracle projection-error comparison across several exposures. |

Panel B defines the scaling choices; it cannot establish that either one
improves projection. Panel C supplies a proposed mechanism, and D is needed
to test the outcome. A compact three-panel fallback would combine the mass
definition and noise diagnostic into B and retain the outcome as C. This is
a layout option, not a decision to drop a panel.
This sequence replaces the older B/C/D order in section 7 of the package
discussion note, which put the projection outcome in B, exposure in C, and
the noise diagnostic in D.

## A: what is already drawn

[Current panel A](../figure/fig1/panelA/fig1A.png) uses the same simulated
observation for both scaling branches. It shows noisy gene projections and
the component-profile triangle in each branch's projection plane. The plots
have **separate display scales**, so triangle or cloud size across branches
is not a direct quantitative comparison. Axes 2 and 3 name the nonconstant
plane after rigid orientation. Its H oracle RMSE labels (0.151 for uniform,
0.105 for expression) measure a sample-side projection residual, not the
distance of displayed genes from a triangle. The single seed and exposure
were selected for a readable illustration; the labels are not evidence of a
general ranking. See [panel A's noise/axes record](20261026_fig1A-noise-and-axes.md)
and [separate-scale record](20261026_fig1A-separate-scales.md). The values
come from `figure/fig1/panelA/projection_metrics.csv`, generated with
GeneralDualSimplex 0.28.0 at package commit
`af56ff97da8e38af7c304513c5d26f1c2ff0c910`.

## B: choices considered and current preference

The first ideas were row and column sums and then row and column variances.
Sums of `Ṽ` help define the choices: converged uniform balancing gives each
gene mass `1/m` and each sample mass `1/n`; expression scaling divides `V`
by its grand total, preserving the observed gene-total and sample-total
proportions. These are properties of the scaling, not measurements of
information or denoising. Raw row/column variance would mix composition,
depth, and measurement fluctuations; variance across genes within a sample
does not treat genes as replicate measurements.

Several B displays were discussed. The first per-gene ranked mass plot had
a difficult y-axis; equal-size low/middle/high gene-bin bars were simpler
but hid the continuous distribution. A plot with **genes ordered by observed
total count** on the x-axis and **cumulative share of matrix total** on the
y-axis became the preferred direction. Both axes can be percentages. Under
converged uniform scaling the curve lies on the diagonal because the
achieved gene masses are equal. That diagonal is **equal mass by
construction, not an ideal fit or an accuracy target**. The other curve is
the observed distribution of counts over those ordered genes.

Expression scaling multiplies every entry by the same `1/sum(V)`
([package scaling code](../../general_dual_simplex/R/dso-scaling.R),
lines 134–138 and 177 at the package commit above). Thus its mass fraction
for gene `g` is `V[g,+] / sum(V)`, exactly the raw count share; multiply by
100 to express this as a percentage. A requested
dashed “raw, unscaled” curve therefore coincides with the expression curve;
it is not a third result. The current [overlap mock](../out/20261026_fig1B_layouts/layout1_raw_overlap.png)
draws it at the same coordinates and says so. A final panel may use one
legend entry, “Raw counts = expression scaling,” to reduce clutter. The
diagonal must use achieved uniform masses, with balancing convergence
checked; a target line alone would conceal a failed balance.

A fixed-seed simulation matching panel A's observed matrix was used to
compare three layouts: [percentage on both axes](../out/20261026_fig1B_layouts/layout1_cumulative_gene_percent.png),
[absolute rank versus cumulative share](../out/20261026_fig1B_layouts/layout2_rank_cumulative_mass.png),
and [absolute rank versus per-gene share on a log y-axis](../out/20261026_fig1B_layouts/layout3_rank_log_per_gene_mass.png).
The first two have the same curve, differing only in x-axis units. The
third recreates the per-gene reading burden. The simulated matrix has 500
genes, 200 samples, seed 1, marker fold 5, and Poisson observation at
`library_size_fraction = 0.04`; all genes and samples remained after zero
filtering. In this **one illustrative matrix**, the lowest 50% of genes
account for 23.0741% of raw/expression mass versus 50% of uniform mass.
Uniform balancing converged with maximum relative marginal error
`7.98623320252823e-13`. The raw and expression cumulative shares differ
only by floating-point rounding.
These values come from [generator](../out/20261026_fig1B_layouts/generate.R),
[per-gene data](../out/20261026_fig1B_layouts/mass_by_gene.csv), and
[provenance](../out/20261026_fig1B_layouts/provenance.txt), run with
GeneralDualSimplex 0.28.0 at package commit
`af56ff97da8e38af7c304513c5d26f1c2ff0c910`. The `out/` files are
ignored exploratory outputs, and the plot says “illustrative, not a
benchmark.”

Ranking by *observed* totals is deliberate for B because that is what
expression scaling uses and what real data provide. Any C/D gene-abundance
diagnostic should instead consider *expected* abundance in a simulation:
ranking by noisy observations can partly select for the fluctuation being
studied. B concentrates on genes; uniform scaling also changes sample
masses and gene profiles, which needs a caption sentence or a small inset
if sample depth becomes central to the explanation.

## C: proposed mechanism, not yet drawn with final data

“Row and column variance” needs a more precise definition. The reviewers
recommended the conditional measurement variability after the full
transformation to `Z`, where projection occurs. For fixed effective row
and column weights `l_g = r_g/sqrt(a_g)` and `t_i = c_i/sqrt(b_i)`, with
conditional mean `μ[g,i]`, the expected squared perturbation attributed to
gene `g` is

```text
Q_g = l_g^2 × sum_i t_i^2 Var(V[g,i] | μ).
```

Population-derived weights give this fixed-transform diagnostic a clear
meaning. If weights are refitted to every observed matrix, that formula
alone is not the unconditional variability of the whole fitted procedure.
Neither raw across-sample gene variance nor across-gene sample variance
isolates this quantity. A proposed C plot places expected gene abundance
on x and transformed noise contribution on y, ideally alongside the
composition-related signal contribution. The bin definition (total or
per-gene average) must be stated. Even a flatter noise distribution cannot
by itself establish better mixture retention; signal direction and
alignment with noise also matter. The fixed-weight derivation and caveats
are in section 9 of the package's untracked working-tree discussion note
(read 2026-10-26 with the package HEAD stated above).

## D: proposed outcome and limits

The proposed outcome is **paired oracle H projection error**: apply both
scalings to the same observed matrix, then compare how much of the known
`H` remains in each retained space, in common original coordinates. This
does not fit simplex vertices and does not report final factor recovery.
In this conversation, a reviewer proposed at least three declared exposures
(including A's `0.04` setting), repeated latent signals and observation draws,
with fitted weights; a suggested minimum was 10 signals × 5 draws. These
specific counts are a discussion proposal, not a result in the package
note. Marking A's example as one
point would make clear that A illustrates a single draw. A noiseless
reference and a population-weight control could help interpretation.
These are **proposed experiment settings**, not completed runs or an
agreed final design. Any caption must report the actual sampling protocol,
uncertainty, and provenance. A one-setting comparison cannot establish
how the scaling difference changes with exposure.

## Next decisions

1. Decide whether B's final legend should combine raw and expression into
   one entry; the dashed overlap mock is available for comparison. Consider
   “share of that matrix's total” for the y-axis, since each curve uses its
   own matrix total.
2. Define and compute C's signal comparison without mixing composition
   effects into its noise metric.
3. Run and review a replicated paired D experiment before writing any
   claim about projection quality or exposure dependence.
4. Keep the earlier [B–D conceptual mock](../out/figure1_BCD_mock.png) and
   [fictional B mocks](../out/figure1B_cumulative_rank_mock.png) as layout
   history only; their invented values are not evidence.

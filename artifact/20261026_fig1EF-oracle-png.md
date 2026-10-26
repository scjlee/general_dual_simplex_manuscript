# Figure 1E–F: narrower W and H oracle RMSE prototypes

Follow-up: `artifact/20261026_fig1D-samples-and-EF-svg.md` records the
current D/A metric labels, sample companion and E/F SVG masters. The E/F
data and oracle definitions in this note remain unchanged.

Date: 2026-10-26. Current PNG layout draft, superseding the E layout in
`artifact/20261026_fig1DE-png-mock.md`. Illustrative simulations only;
no general recovery claim or benchmark ranking relies on these data.

## User request and output

The user approved E's paired-draw layout and asked to remove the highlighting
of draws shown in D, make the panel narrower, calculate W-side RMSE in E,
move H-side RMSE to F, and label the y-axis simply “oracle RMSE”.

Implemented: remove all draw-1 rings and references to those rings from the
error panels. E and F are each 100 × 69 mm (previous E: 134 × 69 mm), at
600 dpi. D is unchanged, including its representative draw. All five draws
have the same dot style within each scaling. Panel titles distinguish W
and H; both y-axes say “oracle RMSE”. Separate y-ranges reflect their
different native units; their absolute magnitudes are not comparable.

Files:

- `figure/fig1/panelE/fig1E.png`: W oracle error.
- `figure/fig1/panelF/fig1F.png`: H oracle error.
- `figure/fig1/fig1EF_mock.png`: E above F, 100 × 140 mm.
- `figure/fig1/fig1DEF_mock.png`: D above the narrower E and F.
- `figure/fig1/fig1DE_mock.png`: refreshed D–E preview (E now shows W).
- `figure/fig1/panelD/projections.R`: shared data generator.
- `figure/fig1/panelD/make_mock_panels.R`: PNG-only renderer.
- E inputs: `projection_metrics.csv`, `oracle_W.csv`,
  `noiseless_metrics.csv`, `noise_parameters.csv`, `package_commit.txt`.
- F inputs: `projection_metrics.csv`, `oracle_H.csv`,
  `noiseless_metrics.csv`, `noise_parameters.csv`, `package_commit.txt`.

The previous own D/E files were backed up to
`out/20261026_fig1EF_v1/` before editing. The old E `oracle_H.csv` was
archived there, and F now holds the H inputs. No files from A–C were edited.
No SVGs were generated.

## Provenance and simulation design

GeneralDualSimplex 0.28.0 at full package commit
`af56ff97da8e38af7c304513c5d26f1c2ff0c910`, no uncommitted `R/` or `src/`.
Manuscript base: `c29f61dd9936840883af47cbea1fbd4521eee36d`; these are
uncommitted prototypes. All numerical values below come from the new
panelE/panelF CSVs produced by `panelD/projections.R` in that working state,
using the cited package version and commit.

Simulation, seeds, noise models and parameters are unchanged from C and
the previous E, documented in `artifact/20261026_fig1DE-png-mock.md`,
“Design and calculation”. Draw r seeds signal and then noise with r = 1–5;
fresh W/H per draw, same signal across the three noise models, and the same
observed V for the two scalings. Scaling weights are fitted to each V.
There are 30 W projections and 30 H projections on those same matrices.

## Oracle W derivation

Package source: `R/dso-projection.R`, `DSProjection$reconstruct_W_tilde`,
and `R/dso-optimization-post-processing.R`, `GetFactors`, at the package
commit above. The first gives

`W_tilde = D_a Phi^T Omega`.

The second undoes row scaling by D_r⁻¹ and right-multiplies by component
scales. Component scales leave the admissible column span unchanged.
Thus original-W reconstructions lie in the column span of

`B_W = D_r^-1 D_a Phi^T` (m_kept × k).

Let Q_W be an orthonormal basis for that span. Independently for each known
true W component column, its Euclidean least-squares oracle projection is

`W_oracle = Q_W Q_W^T W`,
`RMSE_W = ||W − W_oracle||_F / sqrt(m_kept k)`.

W is the original simulated expression matrix, restricted to retained
nonzero observed genes. No library-fraction multiplication, per-column
normalization, positivity clipping or component fitting is applied. All
500 genes are retained here, giving 1,500 entries per W RMSE. The component
scale is fixed by the known simulation W/H, not inferred from V.

The H oracle is unchanged:
`B_H = D_b D_c^-1 Psi^T`, `Q_H = orth(B_H)`,
`H_oracle = H Q_H Q_H^T`,
`RMSE_H = ||H − H_oracle||_F / sqrt(k n)`.
Here n = 200 and k = 3, giving 600 entries per H RMSE. Both oracles are
unconstrained projections of known truth and may contain negative entries;
neither estimates simplex vertices. F measures H in fraction units, whereas
E measures W in its original expression units.

## Caption drafts

**E. W oracle error.** Oracle RMSE of the known simulated W projected into
the recovered feature subspace, in original expression units. Five fresh
signal and noise draws at C's single noise settings. Within a draw, the
signal is shared across noise models and the observed matrix is shared
by both scalings. Dots: individual draws; grey lines: paired scalings;
bars and top numbers: arithmetic means of the five RMSEs. No draw is
highlighted. Scaling is refitted per observed matrix. The oracle is an
unconstrained least-squares projection, not a nonnegative fitted W.
Illustrative simulation for layout, not a benchmark.

**F. H oracle error.** The same matrices, pairing and display conventions
as E, reporting the known H's oracle RMSE in fraction units. H is projected
into the recovered sample subspace with no clipping or renormalization.
Neither oracle estimates vertices. The y-range is shared across noise
models within a panel but differs between E and F because their factors
have different units. Illustrative simulation for layout, not a benchmark.

## Values and checks

Source: panelE and panelF `projection_metrics.csv`, arithmetic mean over
five draws per noise/scaling pair, with implementation/version/commit above.

| Noise | Uniform W | Expression W | Uniform H | Expression H |
| --- | --- | --- | --- | --- |
| Poisson | 6.4492820 | 5.8564018 | 0.15350435 | 0.10341627 |
| Proportional | 7.3703785 | 8.3089489 | 0.10231862 | 0.16368048 |
| Normal, floored at 0 | 6.5094078 | 5.9261968 | 0.14640282 | 0.09947461 |

Python recalculation from all saved true/oracle entries agrees with all
30 W RMSEs within 9.8 × 10⁻¹⁵ and all 30 H RMSEs within 5.3 × 10⁻¹⁶.
F's H metrics, H entries and noise-free metrics are byte-identical to the
previous E files. D's gene coordinates, vertices and PNG are byte-identical
to their backups. Noise-free W RMSE is below 4.8 × 10⁻¹⁴; noise-free H
RMSE is below 4.7 × 10⁻¹⁶ (`noiseless_metrics.csv` in each panel, not drawn).
Bounds are rounded up. The E–F PNG itself was opened and inspected.

R/grid bounds place all labels inside each 100 × 69 mm canvas; diagnostics
are in `out/20261026_fig1EF_checks/`. `git diff --check` passes.

## Review status

The user explicitly requested skipping review and finishing the fixes.
The fresh Advisor - Claude review was therefore cancelled before a verdict;
agent `86e15b8b-cda7-48c5-9fee-c64dec557483` was read with
`get_agent_activity` and archived. This revision has local numerical and
visual checks only; it does not inherit the prior H-only review as approval
of the new W calculation. Handoff retained at
`artifact/handoff/20261026-0537_claude_fig1EF-W-review.md`.

Reproduce from the repository root:

```sh
RENV_CONFIG_SANDBOX_ENABLED=FALSE Rscript figure/fig1/panelD/projections.R
RENV_CONFIG_SANDBOX_ENABLED=FALSE Rscript figure/fig1/panelD/make_mock_panels.R
```

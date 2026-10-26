# Figure 1 after panel B: narrative options

> **Status (2026-10-26, later):** superseded in part. The current design is
> bi-whitening in panel A and per-gene squared-noise shares in `Z` in panel C;
> see `artifact/20261026_fig1C-noise-share.md`, `artifact/20261026_fig1B-rank-log-share.md`
> and the last Figure 1 entries in `artifact/decisions.md`. Text below is kept as history.

Date: 2026-10-26. Lead brainstorming record, not an approved design. All
numbers below are exploratory: one fixed simulated signal (panel A's
`figure/fig1/panelA/simulation.rds`: 500 genes, 200 samples, k = 3, seed 1,
marker fold 5), computed by scripts in the ignored folder
`out/20261026_fig1C_explore/`. They were run with GeneralDualSimplex 0.28.0 at
package commit `af56ff97da8e38af7c304513c5d26f1c2ff0c910` (no uncommitted
`R/` or `src/` changes) and manuscript commit
`aec9931a314f51fcb84c07c6a454a391aa058b4d`. None is figure data or a benchmark.

## 1. Where the figure stands

- **A** (committed): pipeline `W, H → V* = WH → Noise → V → {uniform,
  expression} scaling → rank-k projection → projected genes`, with an H oracle
  RMSE label above each projection (0.151 uniform, 0.105 expression).
- **B** (drafted, uncommitted, `figure/fig1/panelB/`): each gene's and each
  sample's share of the scaled matrix total, against rank, on a log y-axis.
  Uniform is flat (1/500, 1/200). Expression equals the raw count share.

## 2. User constraints from this conversation

1. Do not plot quantities in `Z` or in the reduced space. `Z` contains the
   `D_a^(-1/2) … D_b^(-1/2)` step (bi-whitening), which the figure never
   introduces. "Noise share in Z" was rejected for that reason.
2. "Energy" (sum of squared values) is unclear; drop it.
3. Introduce panel A's elements step by step. B explains scaling. The next
   panel should prime why a scaling is good or bad and bridge to projection
   and the final RMSE.
4. Figure 1 should also prime that **both scaling and noise model matter**.
   With proportional noise the effect should reverse. The user's conceptual
   mock is `/data/figure1_mock.png`; its values are invented and labelled
   "hypothetical trends".

## 3. Exploratory evidence

### 3.1 The reversal holds on this signal

Paired oracle H RMSE (metric copied from `figure/fig1/panelA/points.R`),
10 noise draws per setting on the same signal, both scalings applied to
each draw. Proportional noise is mean-preserving Gamma:
`V = μ·G`, `G ~ Gamma(shape 1/φ, rate 1/φ)`, so `Var = φμ²`; it is continuous,
not counts (package note §10 calls this a mechanism control). Script
`noise_models.R`, data `noise_models.csv`.

| Noise | Level | Uniform | Expression | Uniform − expression (sd) | Uniform better |
|---|---|---|---|---|---|
| Poisson | exposure 0.01 | 0.2425 | 0.2295 | 0.0130 (0.0051) | 0/10 |
| Poisson | exposure 0.04 | 0.1533 | 0.1059 | 0.0473 (0.0095) | 0/10 |
| Poisson | exposure 0.4 | 0.0409 | 0.0311 | 0.0098 (0.0008) | 0/10 |
| Poisson | exposure 4 | 0.0125 | 0.0098 | 0.0027 (0.0003) | 0/10 |
| Proportional | φ = 0.05 | 0.0227 | 0.0287 | −0.0060 (0.0008) | 10/10 |
| Proportional | φ = 0.2 | 0.0472 | 0.0608 | −0.0137 (0.0019) | 10/10 |
| Proportional | φ = 0.5 | 0.0733 | 0.1053 | −0.0320 (0.0030) | 10/10 |

Panel A's single draw (0.151, 0.105) is typical of the exposure-0.04 draws.
This is one signal; repeated signals and other designs are still needed.

### 3.2 Count-space reason: each scaling matches one noise model

Define a gene's **reliability** as 1 / relative variance of its total count
(relative variance = variance / mean²). The derivations assume independent
entries:

- Poisson: `Var(V_g+) = μ_g+`, so reliability = `μ_g+`. As a share,
  `μ_g+ / Σ_h μ_h+`: exactly the expected expression-scaling weight.
- Proportional: relative variance = `φ Σ_i μ_gi² / μ_g+² = φ(1 + cv_g²)/n`,
  where `cv_g` is the across-sample coefficient of variation of the gene's
  expected values. It does not depend on abundance, so reliability is
  nearly equal across genes, like the uniform weight `1/m`.

On panel A's genes (`reliability.R`): Poisson reliability shares span
0.02426–0.6337% (26.1-fold). Proportional shares span 0.1567–0.2047%
(1.31-fold) against uniform's 0.2%; markers (median 0.1774%) sit slightly
below background (median 0.2037%) because they vary more across samples.

So **expression scaling weights genes in proportion to the inverse relative
variance of their totals under Poisson noise; uniform scaling approximately
does so under proportional noise.** Two limits (section 6): this is precision of
a gene's *total*, not of its mixture information, since profile shape also
sets profile noise. And inverse-variance weighting is not in general the
optimal weighting for estimating a subspace (Hong et al., Optimally Weighted
PCA, flagged by the reviewer; not yet read here). It must not be presented
as the explanation of subspace recovery.

### 3.3 Why the reduced-space measures were dropped

For fixed weights, the noise each gene contributes to the projected matrix
equals its mass `a_g` times the noise of its profile point (b-weighted).
This is an algebraic identity: `Z_g = √a_g f_g D_b^(-1/2)`, where `f_g` is the gene's
profile. The identity holds for fixed weights; it does not describe
refitted weights, which change with each noisy matrix. On panel A's matrix,
with **population scaling and projection held fixed**, the per-gene RMS shift of
profile points in the projection plane, divided by each triangle's RMS vertex
radius, was identical under both scalings
(ratio 0.999–1.001), falling as abundance^−0.49 (`displacement.R`); sample
depths differ by only 1.5% (max/min) there. This is consistent with scaling changing
the *weight* of each gene more than the noise of its point, but it does not
establish equal point variability for panel A's refitted pipeline
(section 6).

### 3.4 Pitfall in the conceptual mock

With pure proportional noise, RMSE against exposure is flat **by
construction**. Both scalings are invariant to multiplying the matrix by a
constant, and the noise is relative. Use the noise level φ (or the
coefficient of variation √φ) as the x-axis for that model, not exposure.

## 4. Narrative options for C onward

### Option 1 (lead's preference): zoom into each box of panel A

| Panel | Box of A | Question | Display |
|---|---|---|---|
| B | Scaling | What weight does each scaling give each gene? | Existing. |
| C | Noise | Which genes are reliable under each noise model? | Same axes as B (gene rank, log share). Grey lines: reliability share under Poisson and under proportional noise. Coloured lines: B's weights. Expected expression weight lies exactly on the Poisson line (B shows observed weights); uniform lies near, not on, the proportional line. Title idea "Each scaling suits one noise model" overstates the evidence (section 6). |
| D | Projection | What does a match or mismatch look like? | 2×2 thumbnails in panel A's style (rows: noise model; columns: scaling), each with its RMSE label. One paired draw per row. |
| E | RMSE label | Does it hold across noise levels? | Paired RMSE: Poisson against exposure, proportional against φ, with replicate spread. |

The reader meets nothing that A did not show. C carries the "why" in count
space. D bridges to the projection, E to the RMSE. A compact variant merges
D into E as insets at marked settings.

### Option 2: one match table

C as a 2×2 grid (noise model × scaling) of per-gene "weight × relative
variance" against abundance: flat when matched, sloped when mismatched.
It needs only B's weights and count-space noise, but the product is more
abstract than Option 1's overlay.

### Option 3: realistic negative binomial as the bridge

Relative variance `1/μ + φ` makes low-count genes Poisson-like and
high-count genes proportional-like, so neither scaling matches across the
whole range. This could motivate noise-matched (prescribed) margins later
in the paper; package note §11 describes the Landa biwhitening mapping.
This is a scope decision for the user. No negative-binomial RMSE has been
run.

### Avoid

`Z`, reduced-space shares, "energy", spectral norms, the mock's
"transformed noise share" bins, and causal or "optimal" wording. C gives a
matching argument; D and E test it.

## 5. Open questions for the user

1. Option 1, 2 or 3 (or a mix)?
2. Should proportional noise be an equal partner in Figure 1 or a labelled
   control? Bulk RNA-seq is usually modelled as negative binomial.
3. Should A's Noise box name the two models, or stay generic?
4. Five panels (A–E) or four (D and E merged)?

## 6. Independent review (Advisor - Codex, 2026-10-26)

Handoff: `artifact/handoff/20261026-0335_codex_fig1-narrative.md`. The
reviewer formed its own proposal before reading this record. It reproduced
the reliability and displacement summaries and the RMSE CSV summaries, and
confirmed section 3.4 (exposure invariance under proportional noise).

**Recommendation: a revised Option 1**, raw measurement variability →
retained H structure → replicated H RMSE.

| Panel | Reader question | Display | Take-home |
|---|---|---|---|
| C | Which measurements fluctuate most relative to their means? | Expected count on x; noise SD ÷ expected count on y; Poisson and proportional facets. | Relative variability falls with abundance under Poisson noise and is constant under proportional noise. |
| D | What mixture structure survives projection? | Noise model × scaling; grey true H and coloured oracle-projected H on identical fixed contrasts of the original H coordinates; paired observations within a row. | Scaling can change retained mixture structure, and its ranking can depend on the noise model. |
| E | Does it persist across draws and noise levels? | H oracle RMSE against exposure (Poisson) and φ (proportional); paired draws; spread across signals; noiseless reference. | The comparison holds for a declared simulation regime, with stated uncertainty. |

D may become insets in E. Define "oracle" plainly: the projection of the
known H, with no simplex vertices estimated.

Corrections, applied above in sections 3.2, 3.3 and the Option 1 table:

1. Total-count precision is not mixture information. Under Poisson
   sampling, given total `N > 0`, the normalized profile has covariance
   `[diag(p) − ppᵀ]/N`, so profile shape `p` matters too.
2. The curves do not coincide exactly: Poisson precision matches
   *population* expression shares (B plots observed shares). Proportional
   precision varies with profile shape, so uniform is only an approximation.
3. `displacement.R` holds population scaling and projection fixed, so it
   cannot show equal point variability for the refitted pipeline.

Critique of the options: Option 1 has the best structure. Panel A's gene clouds
and the H RMSE measure different things, so D should show H. Option 2's
product implies that flattening it is a desirable projection objective,
which is unestablished. Option 3 suits a later sensitivity analysis.

Minimum before outcome panels carry claims: 10 independent signals × 5
paired draws, at least three levels per noise model, noiseless controls;
designs where distinctive genes are relatively low versus high abundance;
unequal sample depths; refitted scaling as the main comparison
(population weights as a labelled mechanism control); report filtering,
balancing failures and a declared rule for choosing the example. Treat
Gamma noise as a continuous mechanism control; Poisson and Gamma settings
are not matched in difficulty.

Literature to read before citing: Hong et al., Optimally Weighted PCA
(https://pmc.ncbi.nlm.nih.gov/articles/PMC12851565/; inverse variance is
not generally optimal there); Landa et al., Biwhitening Reveals the Rank
of a Count Matrix (https://arxiv.org/html/2103.13840v2, sections 2 and 4).

Proposed house rule (not yet adopted): "Name the target whose precision is
measured; total-count precision alone does not establish profile or
composition retention."

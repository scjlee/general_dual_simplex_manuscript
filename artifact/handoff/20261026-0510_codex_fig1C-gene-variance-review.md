# Handoff: review Figure 1C change to each gene's variance in Z

- Recipient: Advisor - Codex (reviewer role)
- Repository: `/workspace/dual_simplex_functional/general_dual_simplex_manuscript`
- Paseo workspace: `wks_eae2eb8dafb28fa0`
- Lead: Claude (Opus 5.5)
- Package: GeneralDualSimplex 0.28.0 at `af56ff97da8e38af7c304513c5d26f1c2ff0c910`
  (`/workspace/dual_simplex_functional/general_dual_simplex`, read-only).
- Supersedes `artifact/handoff/20261026-0506_codex_fig1C-variance-review.md`
  (that review was cancelled: it covered a noise-variance version the user did
  not want).

## Task

Review the uncommitted change against commit `c29f61d`
(`git diff c29f61d -- figure/fig1/panelC artifact/20261026_fig1C-noise-share.md`).
Read-only; scratch outputs only under `out/`. Read `AGENTS.md` first. Return a
verdict, findings with file and line, open questions. Result first, compact.

## The change

The user wants y to be "variance of genes, not noise", to bridge to panel D
because the SVD optimizes an L2 norm. `figure/fig1/panelC/noise_share.R` now
fits each scaling on the observed `V`, forms `Z = D_a^(-1/2) Ṽ D_b^(-1/2)`,
asserts that `√a √bᵀ` is the trivial singular pair (singular value 1), and
plots gene g's share of `Σ_i (Z_gi − √(a_g b_i))²`, which sums to
`Σ_{j≥2} σ_j²`. Replicates, ranking and bands are unchanged. Title and axis:
"Where the variance sits after bi-whitening", "Gene share of variance in Z (%)".
Bands and dots were also recoloured and enlarged (style only).

Check: the identity (trivial pair, sum equals `Σ_{j≥2} σ_j²`, including that
σ₁ = 1 is the largest) against the package (`R/dso-scaling.R`,
`R/dso-projection.R`) and README; whether "variance" is a fair word for
`Σ_i (Z_gi − √(a_g b_i))²` (it is CA-style row inertia, not a sample variance
around the row mean); the record and caption draft
`artifact/20261026_fig1C-noise-share.md`, including the 2.4% signal / 98% noise
statement from `out/20261026_fig1C_noise/signal_fraction.R`; and what may be said
about the link to the SVD's L2 objective. Rerun `noise_share.R` and
`make_fig1C.py` into scratch and compare; open `figure/fig1/panelC/fig1C.png`;
check text inside the canvas.

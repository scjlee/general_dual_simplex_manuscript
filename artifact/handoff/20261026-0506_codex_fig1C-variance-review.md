# Handoff: review Figure 1C change from realized squared noise to noise variance

- Recipient: Advisor - Codex (reviewer role)
- Repository: `/workspace/dual_simplex_functional/general_dual_simplex_manuscript`
- Paseo workspace: `wks_eae2eb8dafb28fa0`
- Lead: Claude (Opus 5.5)
- Package: GeneralDualSimplex 0.28.0 at `af56ff97da8e38af7c304513c5d26f1c2ff0c910`
  (`/workspace/dual_simplex_functional/general_dual_simplex`, read-only).

## Task

Review the uncommitted change against commit `c29f61d` (`git diff c29f61d --
figure/fig1/panelC artifact/20261026_fig1C-noise-share.md`). Read-only; scratch
outputs only under `out/<date>_fig1C_variance_review_codex/`. Read `AGENTS.md` first.
Return a verdict, findings with file and line, open questions. Result first, compact.

## The change

The user asked for "variance" on the y-axis because panel D will bridge to the
projection, and the SVD optimizes an L2 norm. The earlier draft plotted one
realized draw's `Σ_i (l_g (V_gi − μ_gi) t_i)²`. Now
`figure/fig1/panelC/noise_share.R` computes, per replicate and scaling, the
weights `l = r/√a`, `t = c/√b` fitted on the observed `V`, held fixed, and
gene g's noise variance in `Z = D_l V D_t` as `l_g² Σ_i t_i² Var(V_gi)` with
exact model variances at `μ`: Poisson `μ`; proportional `φμ²`; floored normal
`Var(max(X,0))`, `X ~ N(μ, σ²)` (closed form in the script). Shares,
ranking by observed total, 5 independent replicates and min–max bands are
unchanged. Axis label: "Gene share of noise variance (%)". Bands and dots were
also recoloured and enlarged (style only).

Check: the variance formula and its link to `Z` (package `R/dso-scaling.R`,
`R/dso-projection.R`, README notation); the floored-normal moments; whether
"noise variance" is an accurate label given weights fitted on the noisy `V`
(conditional on the fitted weights) and the excluded clipping bias; the
updated record and caption draft `artifact/20261026_fig1C-noise-share.md`;
the claim that this links to the SVD's L2 objective (what may and may not be
said). Rerun `noise_share.R` and `make_fig1C.py` into scratch and compare; open
`figure/fig1/panelC/fig1C.png`; check text inside the canvas.

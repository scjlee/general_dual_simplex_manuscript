# general_dual_simplex_manuscript

Manuscript drafts, figures and the research record for the general dual
simplex project. No manuscript format or scientific content is chosen yet,
and the historical slide deck is not imported.
Agents read `AGENTS.md` before editing; it holds the rules for Claude and Codex.

## Related repositories

| Role | Repository | Local directory |
|---|---|---|
| Current R package `GeneralDualSimplex` | `scjlee/general_dual_simplex` | `../general_dual_simplex` |
| Legacy pilot study (experiments and reports) | `scjlee/dual_simplex_functional` | `../general_dual_simplex_experiment` |
| Legacy DSO R package `DualSimplex` | `artyomovlab/dualsimplex` | installed in this renv |

- The package's discussion record lives in its `.ai/` folder. Agents read it
  but never edit it.
- The legacy pilot study predates the package. It is kept for reference and
  is not developed further. Cite its reports with the full commit.
- The legacy `DualSimplex` package is installed for comparison only.
- Setup state (2026-10-09): pilot study at
  `fe436483d4f394d3312d4bf02cd9938ab534fe3b`, GeneralDualSimplex 0.1.0 at
  `aa2717e59b098bcc31995d3dde5ab021aca6d087`. Cite the versions that support
  each later claim, not these.

## Layout

- `AGENTS.md`: rules for agents. `CLAUDE.md` only imports it.
- `artifact/`: the decision record (`decisions.md`), long notes
  (`YYYYMMDD_<topic>.md`) and agent tasks (`handoff/`, created when needed).
- `figure/<figN>/<panel>/`: the SVG (the master after a hand edit), its
  generator, input data, `package_commit.txt` and PDF/PNG previews.
- `script/`: local tools, copied from the pilot study at the setup commit;
  their MIT notice is in `script/LICENSE`.
- `out/`: ignored scratch output, such as report extracts.
- `renv/`, `renv.lock`, `.Rprofile`: the R environment.

## R environment

R 4.5.3 with renv and Bioconductor 3.22. After cloning, run
`renv::restore()` from the repository root. Run figure scripts from the
root too, for example `Rscript figure/fig1/panelA/points.R`.

- `GeneralDualSimplex` is installed from the local checkout, so `renv.lock`
  records `Source: Local` with no commit. Each figure script writes the
  package commit, installed version and uncommitted `R/` and `src/` changes
  to `package_commit.txt`. After the package changes, reinstall with
  `renv::install("../general_dual_simplex")` and `renv::snapshot()`.
- `DualSimplex` is pinned by its GitHub commit in `renv.lock`.
- Approved packages: GeneralDualSimplex, DualSimplex, ggplot2, patchwork,
  scales, svglite (plus their dependencies). Ask before adding others.

System tools: Inkscape 1.4 or later, Liberation Sans (or Arial), Python 3
(standard library only).

## Local tools

- `script/decision-log.py artifact/decisions.md -r 5`: read recent decisions;
  `-l` lists titles, `-g <pattern>` searches, `-t <words>` prints one entry.
- `script/extract-report.py <report.html> --out out/<report-name>`: extract
  report text and figures; it uses Python Pillow. Use `--fig-scale 1` for
  full-size figures. Extraction does not rerun anything.

## Git setup

The SSH origin is
`git@github-gds_manuscript:scjlee/general_dual_simplex_manuscript.git`.
Stage files by name. Agents push only when the user asks. The tracked
push-deny settings are in `.claude/settings.json`. After cloning, install the
local hook with:

```sh
cp script/git-hooks/pre-push .git/hooks/pre-push
chmod +x .git/hooks/pre-push
```

Cloning does not install the hook. Do not bypass push protections or copy
credentials and local configuration from another repository.

## Coding style guides

- **Code should explain itself.**
- **Use comments wisely.** Comments mainly convey intent, rationale, or context that cannot be expressed clearly in the code itself.
- **DO NOT over-engineer.** Start with the simplest, most straightforward approach that solves the problem. Add complexity only when it is justified.
- **DO NOT write defensive code.** This is research code, and its inputs are known. Add a check only after a real run gave a wrong result without an error.
- **DO NOT copy a value just to rename it.** Read a field where you use it. Add a variable only to change a value or to avoid repeating work.

## Mathematical Notation

For all notations, capital letters indicate real matrices and $\mathbf{bold}$ lower case letters indicate column vectors. We assume $k \ll n < m$. $\mathbf{1}$ indicates a column vector of all 1s with appropriate dimensionality. $D_x$ denotes the diagonal matrix formed from vector $\mathbf{x}$. For any matrix $A$, $A_{i..j, \ast}$ denotes rows $i$ to $j$; $A_{\ast, i..j}$ denotes columns $i$ to $j$.

We write $V^* = WH$ for the ground-truth signal and $V$ for the observed data. In the noiseless theoretical model below, $V = V^*$ and $\mathrm{rank}(V)=k$. Scaling weights $\mathbf{r}, \mathbf{c}$ and the entries of $\mathbf{a}, \mathbf{b}, \mathbf{w}, \mathbf{h}$ are positive, so all diagonal inverses below exist. We choose the first singular vectors as $S_{1,\ast}=(\sqrt{\mathbf{a}})^T$ and $R_{1,\ast}=(\sqrt{\mathbf{b}})^T$, with square roots taken entrywise.

| Notation | Dimension | Description |
|:---|:---|:---|
| $V^*$ | $m \times n$ | Ground-truth signal matrix $V^* = W H$ ($m$ features, $n$ samples) |
| $V$ | $m \times n$ | Observed data matrix; $V = V^*$ in the noiseless theoretical model |
| $W$ | $m \times k$ | Basis matrix with non-negative feature profiles |
| $H$ | $k \times n$ | Coefficient matrix with non-negative entries |
| $\mathbf{r}, \mathbf{c}$ | $m, n$ | Scaling weights defining the pre-processing |
| $\widetilde{V}$ | $m \times n$ | Scaled matrix $\widetilde{V} = D_r V D_c$ where $\sum_{ij} \widetilde{V}_{ij} = 1$. $\widetilde{V} = \widetilde{W} M \widetilde{H}$ |
| $\widetilde{W}, \widetilde{H}$ | $m \times k, k \times n$ | Weighted factor matrices $\widetilde{W} = D_r W D_w^{-1}$ with columns sum 1, $\widetilde{H} = D_h^{-1} H D_c$ with rows sum 1 |
| $\mathbf{w}, \mathbf{h}$ | $k, k$ | Column sums of $D_r W$ and row sums of $H D_c$ respectively, with $\mathbf{w} = W^T \mathbf{r}, \mathbf{h} = H \mathbf{c}$ |
| $M$ | $k \times k$ | Diagonal component mass matrix $M = D_w D_h$ with $\sum_j M_{jj} = 1$ |
| $\mathbf{a}, \mathbf{b}$ | $m, n$ | Row marginals $\mathbf{a} = \widetilde{V} \mathbf{1}$ and column marginals $\mathbf{b} = \widetilde{V}^T \mathbf{1}$ |
| $Z$ | $m \times n$ | Bi-whitened matrix $Z = D_a^{-1/2} \widetilde{V} D_b^{-1/2}$ |
| $S, \Sigma, R$ | $n \times m, n \times n, n \times n$ | Singular value decomposition:  $Z  = S^T \Sigma R$ |
| $\sigma_i$ | Scalar | $i^{th}$ singular value of $Z$ in descending order ($\sigma_1 = 1$) |
| $\Phi, \Psi$ | $k \times m, k \times n$ | Coordinate bases (generalized singular vectors): $\Phi = S_{1..k,\ast} D_a^{-1/2}$, $\Psi = R_{1..k,\ast} D_b^{-1/2}$ where $\Phi_{1,\ast} = \mathbf{1}^T$ and $\Psi_{1,\ast} = \mathbf{1}^T$ |
| $V_{\text{fs}}, V_{\text{ss}}$ | $m \times n, m \times n$ | Normalized profiles: sample-space $V_{\text{ss}} = D_a^{-1} \widetilde{V}$ with $V_{\text{ss}} \mathbf{1} = \mathbf{1}$; feature-space $V_{\text{fs}} = \widetilde{V} D_b^{-1}$ with $V_{\text{fs}}^T \mathbf{1} = \mathbf{1}$ |
| $B_{\text{fs}}, B_{\text{ss}}$ | $k \times n, m \times k$ | Barycentric coordinates: $B_{\text{fs}} = M\widetilde{H}D_b^{-1}$ with columns sum 1 and $V_{\text{fs}} = \widetilde{W}B_{\text{fs}}$; $B_{\text{ss}} = D_a^{-1}\widetilde{W}M$ with rows sum 1 and $V_{\text{ss}} = B_{\text{ss}}\widetilde{H}$ |
| $\Omega, X$ | $k \times k, k \times k$ | Theoretical simplex vertices in GSVD space: $\Omega = \Phi \widetilde{W}$ and $X = \widetilde{H} \Psi^T$ satisfying the link $\Omega M X = \Sigma_{1..k,1..k}$ |


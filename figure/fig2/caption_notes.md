# Figure 2 caption notes (draft)

## a, b: all matrix values are illustrative

The matrices in a and b are illustrative and support no numerical claim.
They come from `figure/fig2/schematic.py` (Python standard library, no
package code; seed 20261109; m = 6 features, k = 3 components, n = 5 samples).

- W and H repeat the Figure 1b draws (same seed and order; identical values).
  V = WH is noiseless.
- Prescribed marginals: a and b drawn once from Dirichlet(4).
  Ṽ = D_r V D_c, with r and c from Sinkhorn iterations until the maximum
  relative row-marginal error was below 1e-13 (achieved: 4.3e-14).
- Z = D_a^(-1/2) Ṽ D_b^(-1/2); w = Wᵀr, h = Hc; W̃ = D_r W D_w^(-1),
  H̃ = D_h^(-1) H D_c, M = D_w D_h (README.md notation).
- Generator check on these matrices: column sums of W̃, row sums of H̃,
  trace(M), sum(Ṽ), sum(a) and sum(b) all differ from 1 by at most 1.2e-16;
  max |Ṽ − W̃MH̃| = 1.4e-17. These are consistent with the key properties
  listed in b, which follow from the definitions above; the check does not
  prove them.
- Cell colours: V, Ṽ and Z are linear in log(value) between each matrix's own
  minimum and maximum; W, W̃, H and H̃ show rank within each matrix; the diagonal
  of M runs from a 30% tint (value 0) to full colour (largest entry); zeros are
  white. Colours are therefore not comparable across matrices.

The generators print these properties; the logs of this run are in the ignored
`out/20261119_fig2_ab/panelA.log` and `panelB.log`.

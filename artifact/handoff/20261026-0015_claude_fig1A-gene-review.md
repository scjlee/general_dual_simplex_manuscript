# Figure 1A gene simplex review

Recipient: fresh Advisor - Claude (profile=Advisor - Claude).
Repository: /workspace/dual_simplex_functional/general_dual_simplex_manuscript
Workspace ID: wks_fac28d65ea0e3234
Role: Reviewer, read-only. AGENTS.md applies. Do not commit or modify files.

User requested upright matrix letters; a single generic Noise box and no
noise parameters in the figure; oracle RMSE above each projection; actual
noisy gene simplex points with markers colored by component, background gray,
no clean point cloud, dashed pure simplex triangle; heatmaps showing bulk
mixtures rather than selected nearly pure samples.

Review the plan now, then review the finished files when notified as part of
this same review task. Data/figure scripts are under figure/fig1/panelA/.
The lead will implement and supply a caption/provenance note.

Plan:
- Keep existing reproducible GenerateMixture(500,200,3,n_marker=20,
  marker_fold=5,profile_spread_sd=.2), seed1, Poisson sampling at fraction .1.
  Choose eight interior mixed columns from H for heatmaps rather than nearly
  pure columns. No scientific claim about a benchmark is made.
- For each existing uniform/expression scaling: estimate k=3 SVD from observed
  Y. Its GSVD has Phi,Psi,sigma and marginals a,b. Scaled row profiles
  F = (Y D_c) / rowSums(Y D_c). Noisy gene coordinates are
  C = F Psi^T = Phi^T Sigma (take dimensions2:3).
- True pure vertices are T = (H D_c) / rowSums(H D_c), times Psi^T.
  Noiseless row profiles are convex combinations of T; dashed triangle is
  those pure component profiles projected into the noisy estimated basis.
- Rotate/reflect (rigid orthogonal Procrustes only, no affine deformation)
  points and vertices together to orient components consistently. Equal
  aspect, shared screen limits for both branches; no clipping/filtering of
  outliers. Plot only C points, colored by known marker block or gray bg.
- Retain the original H oracle RMSE, ||H-HQQ^T||_F/sqrt(kn), Q=orth(
  Psi^T D_b D_c^-1), from this same noisy data; explicitly define it in
  the caption/provenance note. It is not a point-cloud distance or a fitted
  simplex error. Print accurate values and put labels above plots.
- In-place edits to the SVG master only, numbered backup first. Data generator
  remains restricted to six named data-group contents. Other requested
  editorial/layout edits made separately by id.

Please check the math and visual interpretation, especially the true projected
triangle, colored noisy points, retained H metric, and heatmap display scaling.
Return verdict, findings with file/line, and open questions. Do not launch agents.

# Figure 1a reverse scaling review

Recipient: fresh Claude reviewer, profile=Advisor - Claude.
Repository: /workspace/dual_simplex_functional/general_dual_simplex_manuscript
Workspace ID: wks_eae2eb8dafb28fa0
Role: Reviewer. Read only. Do not edit or commit.

The user requested a final gray “Reverse scaling” box in standalone panel 1a
and the full Figure 1 master. Check that putting this step after “Find
solution” correctly describes the route to factors on the original scale.
Use GeneralDualSimplex 0.40.0 at df4a86591f9cabd3d66ca3af8db54dcd46552733,
particularly GetFactors.DualSimplexObject in
../general_dual_simplex/R/dso-optimization-post-processing.R. Check
figure/fig1/panelA/fig1A.svg and figure/fig1/figure1.svg for the scoped change.
Give a short verdict and any findings. The simplified figures are out of scope.

Review result: approved. The reviewer verified the workflow against
`GetFactors.DualSimplexObject` and checked both renders and text bounds.
Reverse scaling happens when extracting original-scale or deconvolution
factors, where the same operation allocates component mass between the
factors. The reviewer noted this distinction for future caption drafting.

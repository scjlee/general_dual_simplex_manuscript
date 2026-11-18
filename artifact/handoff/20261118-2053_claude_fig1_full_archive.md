# Full Figure 1 archive refresh review

Recipient: Claude, fresh Reviewer. Repository: general_dual_simplex_manuscript.
Workspace ID: wks_eae2eb8dafb28fa0. Stay read-only and report in chat.

The user authorized switching the entire figure to
/data/k3_simulation_balanced-population_with-pure_both-marginals.rds. Verify
that all data-driven plots in full and simplified Figures use the uniform
marginal subset as in the supplied Rmd, with the existing analysis/plotting
settings, and that the new C/G values agree with the archive. The lead is
running the actual renderer and assembling during review. Source Rmd:
figure/fig1/reference/261118_figure1_components_render.Rmd. Prior independent
archive extraction: out/20261118_fig1_g/evaluations.rds; no need to reload the
large archive. Review the source changes, re-rendered plotted-input data,
caption/provenance, and assembly for both simplified variants. Check whether
the D rank/bin notes still apply. The expected noiseless comparison for
uniform-marginal runs is in out/20261118_fig1_g/check-noiseless.log. Do not
change files. Report verdict, findings and any open questions.

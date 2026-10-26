# Review W-side oracle E and H-side F PNG prototypes

Recipient: Advisor - Claude, reviewer role (read-only).
Repository: `/workspace/dual_simplex_functional/general_dual_simplex_manuscript`.
Workspace ID: `wks_eae2eb8dafb28fa0`. Lead: Codex.

Read README.md, AGENTS.md and `artifact/20261026_fig1EF-oracle-png.md`.
Review only this new change. Existing dirty A–C/discussion/AGENTS files
are unrelated. Scratch/review output only under
`out/20261026_fig1EF_review/`; do not edit other files or start agents.

User approved E's paired plot and requested: remove highlighting of D's
draws, narrow E, put W-side oracle RMSE in E and move H-side RMSE to F,
and simplify both y labels to “oracle RMSE”. PNG only continues.

Changed code: `figure/fig1/panelD/projections.R` adds raw-W oracle from
the column span of D_r^-1 D_a Phi^T, projects known W by Q_W Q_W^T W,
and writes W data to E and unchanged H data to F. All seed/noise settings
are retained. W is the known simulated W in native expression units, with
no depth multiplication or column normalization. Same retained genes as
the projection (all 500 in these draws).

`figure/fig1/panelD/make_mock_panels.R` uses one paired plot for W/E and H/F,
100 mm wide (old E 134), no rings or draw-1 emphasis in E/F. D is unchanged.
Open `figure/fig1/fig1EF_mock.png` itself. Caption/derivation is in the new
note. Original own files for comparison: `out/20261026_fig1EF_v1/`.

Check W oracle against package `DSProjection$reconstruct_W_tilde` and
`GetFactors` unscaling, dimensions and native-unit interpretation; verify
saved RMSEs from oracle entries, pairing, means and PNG groups; check H
values unchanged after moving to F; identify any caption/mathematical issue.
Package GeneralDualSimplex 0.28.0 at commit
`af56ff97da8e38af7c304513c5d26f1c2ff0c910`, read-only. Return compact
verdict, findings with file/line, and open questions. Save final review to
`out/20261026_fig1EF_review/review.md`, then send the verdict as final.

# Fresh review before Figure 1 SVG commit

Recipient: Advisor - Claude, reviewer role (read-only).
Repository: /workspace/dual_simplex_functional/general_dual_simplex_manuscript.
Workspace ID: wks_eae2eb8dafb28fa0. Lead: Codex.

Read README.md, AGENTS.md and artifact/20261026_fig1_svg-final.md.
The user now explicitly requests a fresh review after completion and before
commit; this overrides the earlier request to skip review. Do not commit
or edit task files. Scratch output/report only under
out/20261026_fig1_final_review/. Do not start additional agents.

Review the full completed A/D/S/E/F work of this session, including the new
W oracle and sample companion that were not previously reviewed, rather
than only the last footer removals. Existing unrelated C, discussion and
AGENTS working-tree changes are excluded.

Current figures:
- A: existing gene SVG, two labels changed from H to W oracle error.
  Its CSV adds oracle_W_rmse; old H diagnostic is retained.
- D: panelD/fig1D.svg, representative gene points, W oracle error.
- S: panelD_samples/sample_simplices.svg, observed samples, H oracle error.
- E/F: panelE/fig1E.svg and panelF/fig1F.svg, W/H errors across five paired
  draws. E/F numbers are means; D/S labels are representative draw 1.
- All final SVGs have matching PNGs; open the images themselves.

Inspect panelA/points.R and make_fig1A.py; panelD/projections.R,
make_fig1DS.py and make_mock_panels.R; panelE/make_fig1EF.py; all inputs
under A/D/S/E/F; the current caption note and the two earlier derivations
it references. Use figure/fig1 prefixes for these paths.
Package GeneralDualSimplex 0.28.0, af56ff97da8e38af7c304513c5d26f1c2ff0c910
is read-only. Check W/H oracle algebra against reconstruct_W_tilde,
reconstruct_H_tilde and GetFactors, native units, sample coordinates and
known triangles, pairing and saved RMSEs, label-to-data mapping and means.
Check SVG rendering/layout, data-only master refresh, all footer removals.
All simulations are illustrative; no general ranking is claimed.

Backups: out/20261026_fig1_final/001/ (before latest SVG/footer changes),
out/20261026_fig1A_Wlabels/001/ (before A labels changed),
out/20261026_fig1D_samples_v1/ (before sample addition).
Local bounds/refresh checks are in out/20261026_fig1_final/.

Return verdict, findings with file/line, and open questions; separate
blocking problems from optional polish. Save report to
out/20261026_fig1_final_review/review.md and send final verdict.

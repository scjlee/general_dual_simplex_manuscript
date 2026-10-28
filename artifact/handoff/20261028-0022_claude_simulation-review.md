# Recipient: Advisor - Claude; independent review

Repository: `/workspace/dual_simplex_functional/general_dual_simplex_manuscript`
Workspace ID: `wks_f1fc0452fbbda285`
Role: reviewer, read-only except your report under `out/20261028_simulation_review/`.

User asks to audit `/data/current_pipeline.R` for important missing metrics,
write code saving projected true vertices in its DSO, and reduce RDS size.
Review the new files:

- `artifact/20261028_simulation_helpers.R`
- `artifact/20261028_simulation_pipeline.md`

Check formulas, matrix orientation and active-axis name alignment; compatibility
with the package's coordinate/plot conventions; preservation and roundtrip
behavior of the R6 packing; history-trimming consequences; and the metric audit
and implementation-dependent claims. Return a verdict, findings by file:line,
and remaining questions. Do not edit the implementation or shared artifacts.
Do not start further agents.

Package source is read-only at `../general_dual_simplex`, version 0.29.0,
commit bfd5ce69987c17e5a1253a477e9b73e965afc1aa, clean R/src. The manuscript
renv has 0.28.0 and lacks the current benchmark/multiplicative/normal exports.
For verification I copied source to `/tmp/20261028_pipeline_package_source`
and installed that copy at `/tmp/20261028_pipeline_library`, leaving both
repositories' environments unchanged. Run R from the manuscript root with
`RENV_CONFIG_SANDBOX_ENABLED=FALSE`, then prepend
`.libPaths(c('/tmp/20261028_pipeline_library', .libPaths()))` before loading the
package. Existing dependencies come from this repo's renv.

I am running focused checks and illustrative compression measurements separately;
the validation section will be updated when results are available. The actual
ground-truth grid RDS and its vectors are not present. No full-grid outcome or
production compression savings can be inferred. Keep the review bounded to the
two deliverables and write results to
`out/20261028_simulation_review/review.md` if useful.

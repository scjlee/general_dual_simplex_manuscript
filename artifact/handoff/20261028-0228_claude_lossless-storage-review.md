# Recipient: Advisor - Claude; independent lossless storage review

Repository: `/workspace/dual_simplex_functional/general_dual_simplex_manuscript`
Workspace ID: `wks_f1fc0452fbbda285`
Role: fresh reviewer. Read-only except scripts/report under
`out/20261028_lossless_storage_review/`. Do not start more agents.

User has 190 experiments with unique 3000 x 500 matrices, one marginal scheme,
and an approximately 1.5 GB gzip archive. Their own diagnostics show data
dominates serialized size. They explicitly require preserving exact observed
values; regeneration and reduced precision are excluded. Prior xz save took
10.74495 min and gzip 1.122408 min. Do not infer production savings from our
illustrative fixtures.

Review only the new compact-data archive option in
`artifact/20261028_simulation_helpers.R`, its validation script
`artifact/20261028_storage_validation.R`, and note
`artifact/20261028_lossless_storage.md`.

The new `compact_data = FALSE` default preserves old behavior. When opted in:
double Matrix slots are copied to a plain archive record, x is stored as
1/2/4-byte integers only when all values are finite, nonnegative, integral and
within signed integer range; signed zeros are tracked. Otherwise the original
8-byte double representation is byte-shuffled and reversed on read. x attributes
and the Matrix's class and other slots are retained. The updated reader restores
the Matrix before the DSO. Old archives retain native Matrix data and remain
readable. No other earlier helpers, including the uncommitted DualPlot overlay,
were changed in this task. No dependency was added.

Check exact preservation, width/endian handling, signed zeros/nonfinite values,
Matrix reconstruction/hash/lineage, old-archive compatibility, no mutation, and
scope of evidence/claims. Keep review bounded; helper parameter/format change
does not alter numerical fitting. Return accept or findings with file:line.

Source package is read-only `../general_dual_simplex`, 0.29.0, clean R/src,
commit bfd5ce69987c17e5a1253a477e9b73e965afc1aa. Current repo renv still has
0.28.0, so prepend `.libPaths(c('/tmp/20261028_pipeline_library',.libPaths()))`
before loading the temp-installed 0.29.0. Start R from manuscript root using
RENV_CONFIG_SANDBOX_ENABLED=FALSE. No package/environment installation is needed.
R is 4.5.3 with zstd support; the gzip option remains available.

Focused validation is running; output:
`out/20261028_storage_validation.log` and
`out/20261028_storage_validation/measurements.csv`. Earlier illustrative DSOs
are in `out/20261028_simulation_validation/full_gzip.rds` (180 x 70). The new
validation script also generates actual 3000 x 500 arrays using the same package
and measures full-object archives. Do not run the whole benchmark again unless
needed to investigate a finding. You may write a final report to
`out/20261028_lossless_storage_review/review.md`.

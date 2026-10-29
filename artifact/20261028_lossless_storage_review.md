# Independent review: compact_data archive option (2026-10-28)

Reviewer: Claude (advisor role), read-only except this folder.
Manuscript base `d270e7485cf2518b6c04c4b9126c27a4878ce8d2` plus uncommitted
`artifact/20261028_simulation_helpers.R`; package 0.29.0
`bfd5ce69987c17e5a1253a477e9b73e965afc1aa` (clean R/src), temp library
`/tmp/20261028_pipeline_library`, R 4.5.3, Matrix 1.7-4.

## Verdict

Accept after one one-line fix (F1). The encoding itself is lossless in every
case I tried. F1 is a loud read failure, not silent data change.

## Findings

F1 (must fix). `artifact/20261028_simulation_helpers.R:116` stores
`class(data)[1L]`, which drops the `package = "Matrix"` attribute.
`unpack_simulation_dso` (`:66-68`) rebuilds the Matrix before any
`GeneralDualSimplex::` call, so in a fresh session that has only sourced the
helper (the usage pattern in the note, lines 15-22), Matrix is not loaded and
`read_simulation_rds()` fails: `"dgeMatrix" is not a defined class`. An old
(native Matrix) archive reads fine in the same fresh session, so this is a
regression of the new format only. Fix: `class = class(data)`. `new()` with a
package-tagged class name loads Matrix itself. Verified on a patched copy:
fresh write + fresh read restores identical serialized Matrix bytes
(`fresh_read_patched.R`). The patched reader also reads archives written by
the current code once the namespace is loaded. The validation script missed
this because it calls `library(GeneralDualSimplex)` first
(`artifact/20261028_storage_validation.R:5`); consider one fresh-process read.

F2 (note, minor). `artifact/20261028_lossless_storage.md:116-118` says
"modest" without numbers. From the table (gzip compact vs original gzip):
continuous 9.64% (Mul, Normal), none 10.96%, Poisson 31.18%; compact zstd vs
original gzip: 11.63-11.67% continuous, 17.97% none, 44.23% Poisson. Suggest
stating these, as properties of this one fixture.

F3 (note, minor). `:126-129` RAM overhead: give the size. Continuous path
retains 3000 x 500 x 8 B = 12.0 MB raw per matrix, about 2.28 GB for 190
experiments, in addition to the original matrices; 1-byte counts about
0.29 GB.

F4 (note, minor). `:59-63` cites R-devel help pages for an "R 4.5+" claim. I
checked locally: R 4.5.3 `saveRDS` has a `zstd` branch and wrote the zstd magic
bytes `28 b5 2f fd`. Cite the local check, and say that reading a zstd archive
needs an R build with zstd support (portability when sharing).

F5 (note, minor). Add that archives written with `compact_data = TRUE` cannot
be read by the earlier helper. Verified: HEAD helper fails loudly with
"got class "list", should be or extend class "Matrix"" (no silent misuse).

## Checks that passed (scripts in this folder)

- `edge.R`: identical serialized bytes and `rlang::hash` after round trip for
  custom NaN payloads (signalling-pattern, negative quiet NaN, NA vs NaN,
  -NaN), subnormal, -0; 0 x 0 dgeMatrix; dgTMatrix with duplicate triplets;
  dgRMatrix; dsyMatrix; unit ddiMatrix; packed dtpMatrix; Dimnames with counts;
  cached Cholesky in `@factors`; 3000 x 500 counts with 1000 -0 entries;
  3000 x 500 lognormal; counts with one 2^31 value (falls to double path).
  Input not mutated. Width selection 255 -> 1, 256 -> 2, 65536 -> 4,
  0.5 -> double (8 bytes/value).
- Code reading: explicit `endian = "little"` on both sides; width 1/2 read
  unsigned, width 4 signed and bounded by `integer.max`; `is.finite` excludes
  NA/NaN/Inf from the integer path; shuffle is transpose 8 x N then N x 8,
  which are inverse permutations; `data_id` slot is carried natively and the
  recomputed hash matches.
- Lead's validation log and CSV: all checks passed; note table matches
  `measurements.csv` exactly.

## Open question (not blocking)

Compact archives rebuild the Matrix with `new()` from stored slots. If a future
Matrix release renames slots, `new()` will error where a native `readRDS` might
still load. Low risk; the stored `package_version` does not record the Matrix
version. Recording `packageVersion("Matrix")` would help diagnose it later.

## Recheck after F1 fix (2026-10-28)

Final verdict: accept. `artifact/20261028_simulation_helpers.R:116` now stores
`class = class(data)`. My fresh-session check (`fresh_read.R`, Matrix not
loaded before reading) now restores identical serialized Matrix bytes using the
current helper. The lead's regression (`artifact/20261028_storage_validation.R:66-86`)
asserts that Matrix is not loaded before reading, compares the serialized bytes
and checks `validObject`; its log `out/20261028_storage_validation/fresh_reader.log`
reads "Fresh-session reader passed." This test failed on the old line, as shown
by my first-round run. Still open: update the byte table and percentages from
the rerun CSV.

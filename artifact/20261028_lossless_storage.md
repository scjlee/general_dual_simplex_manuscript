# Smaller archives with exact observed values

The user has one marginal scheme and no duplicate observed matrices. They require
preserving the observed values exactly, excluding regeneration and reduced
precision. Their reported dominant field is a 3000 x 500 double Matrix.

The existing helper now accepts optional `compact_data = TRUE`. It changes only
the representation of the Matrix's x slot in the archive. On reading, the
original Matrix class, slots, double values and attributes are reconstructed
before the DSO is constructed. The observed matrix is never removed from a
restored DSO. Existing archives remain readable.

```r
source("artifact/20261028_simulation_helpers.R")

save_simulation_rds(
  experiments, "out/experiments_compact.rds",
  compress = "gzip", keep_history = FALSE, compact_data = TRUE
)
experiments <- read_simulation_rds("out/experiments_compact.rds")
```

Use the updated helper for both writing and reading this format: the earlier
reader cannot read compact archives and will error. The option
defaults to FALSE, preserving the earlier storage behavior. Existing compression
and history defaults are unchanged; this example explicitly uses the user's
preferred gzip and removes history.

The encoding uses two lossless representations:

- Nonnegative finite integral values no larger than R's maximum integer use
  the smallest of 1, 2 or 4 bytes per value. The reader restores doubles.
  The original positions of negative zero are saved separately.
- Other double values are written as eight bytes in a specified endian order.
  The bytes are rearranged into eight contiguous planes before compression.
  The reader reverses this permutation and reads the original doubles.

No numerical rounding, truncation, factor approximation or observation deletion
is performed. Matrices other than double Matrix classes retain their previous
representation. This encoding does not rely on duplicated matrices, seeds or
the simulation recipe. It also applies to the x values of sparse double Matrix
classes while preserving their index slots.

For the shuffle path, regard the original bytes as an 8 x N matrix whose column
j contains the eight bytes of value j. Transpose it and serialize columnwise.
On read, reshape the resulting vector as N x 8 and transpose it back. Those two
permutations are inverses. Integer conversion is used only after testing that
every value is integral and within the supported nonnegative range; the width
thresholds are 255 and 65535, then R's maximum signed integer. These domains
are represented without numerical change. Special non-finite or fractional
values use the double path.

Implementation source: GeneralDualSimplex 0.29.0, commit
`bfd5ce69987c17e5a1253a477e9b73e965afc1aa`, clean R/src. Package
`R/dso-object.R`, CreateDSO.default stores the input as a general Matrix;
`R/simulation.R`, ApplyNBNoise returns integer-valued counts stored as doubles.
No package repository, dependency or installed package was changed. The earlier
DualPlot helper additions are preserved.

Native zstd compression is another option in the tested R 4.5.3 build:
use `compress = "zstd"`. The helper already passes the compressor choice to
saveRDS; no dependency is added. Support is optional in R, and reading the file
also needs a build with zstd support, so gzip remains the example here. Source:
[R serialization documentation](https://stat.ethz.ch/R-manual/R-devel/library/base/html/readRDS.html)
and [R connection/compression documentation](https://stat.ethz.ch/R-manual/R-devel/library/base/html/connections.html).

## Validation and illustrative size measurements

Focused validation passed. Initial exploration on 3000 x 500 matrices is recorded in
`out/20261028_storage_search/matrix_measurements.csv` and
`out/20261028_storage_search/count_encodings.csv`; script
`out/20261028_storage_search/benchmark.R`. These are illustrative matrices, not
the user's archive, and do not predict an exact production saving.

The reproducible implementation checks and full-object measurements are in
`artifact/20261028_storage_validation.R`. They exercise integer-width boundaries,
signed zero, non-finite values, fractional and negative data, large integers,
dense and sparse matrices, binary/hash preservation, complete DSO state,
factor/evaluation/lineage preservation, nonmutation and backward reading.

Run from the manuscript root, omitting the temporary library argument if the
current package is already installed in the renv:

```sh
RENV_CONFIG_SANDBOX_ENABLED=FALSE Rscript artifact/20261028_storage_validation.R /tmp/20261028_pipeline_library
```

Results: `out/20261028_storage_validation/measurements.csv`, columns
`noise`, `compress`, `compact_data`, `bytes`, `write_seconds`; log:
`out/20261028_storage_validation.log`; session:
`out/20261028_storage_validation/sessionInfo.txt`. The implementation and
validation are new uncommitted changes after manuscript base commit
`d270e7485cf2518b6c04c4b9126c27a4878ce8d2`; the package version and full commit
are stated above. Tests ran in R 4.5.3 with a temporary 0.29.0 package install,
without changing the repository's installed 0.28.0 package.

The full-object size fixture uses `set.seed(53)` and
`GenerateMixture(3000, 500, 3, n_marker = 20, marker_fold = 5,
profile_spread_sd = 0.2)`. Noise is none, Poisson with `dispersion = 0` and
`library_size_fraction = 0.08`, multiplicative with `sd = 0.25`, or normal with
`sd = 3`. Each DSO has expression scaling, SVD projection dimension 4,
positivity solution dimension 3, random initialization, seed 1,
`step_init = 0.1` and `max_iter = 200`. It includes matrix statistics, a GSVD
reduction, true vertices and EvaluateBenchmark output. Histories are removed
in all storage configurations. The iteration cap is for bounded storage
validation; no recovery conclusion is drawn from these fits.

Table: bytes per illustrative full DSO archive, including its one-row experiment
table. These are measurements of the stated fixture, not the user's archive.

| Noise | Original gzip | Compact gzip | Compact zstd |
|---|---:|---:|---:|
| None | 11,876,117 | 10,574,606 | 9,738,267 |
| Poisson | 1,801,783 | 1,240,012 | 1,005,085 |
| Multiplicative | 11,878,517 | 10,733,650 | 10,492,772 |
| Normal | 11,874,931 | 10,730,622 | 10,493,672 |

For these continuous noisy fixtures, compact gzip is 9.64% smaller than original
gzip; compact zstd is 11.6–11.7% smaller than original gzip. On the noiseless
fixture the respective reductions are 10.96% and 18.00%; on the Poisson fixture
they are 31.18% and 44.22%. These percentages are rounded from the unrounded
byte counts in the CSV and apply only to this fixture.
The tests do not support promising an order-of-magnitude reduction. Counts have
more redundancy and benefit more from the compact integer representation.
Native zstd plus compact storage produced another size/speed tradeoff in this
environment; actual results depend on the user's noise grid, values and machine.
The CSV also includes original zstd and single write timings. Single timings
are indicative checks, not performance benchmarks. The new mode restored the
serialized Matrix bytes and full trimmed packed DSO state identically in these
tests, with unchanged data hashes and evaluation.

Packing allocates an encoded raw vector for each observed Matrix. The current
whole-table writer retains those vectors until the archive is written. For
3000 x 500 continuous matrices, that payload is 12.0 MB per experiment or
2.28 GB for 190 experiments, in addition to the original objects and temporary
per-matrix buffers. One-byte counts need about 0.29 GB of encoded payload for
190 experiments. These decimal byte quantities follow from dimensions times
encoding width; they are not measured peak RAM. This representation trades
temporary memory for disk savings.

Independent review: Claude, profile `Advisor - Claude`, final verdict **accept**.
Record: `artifact/20261028_lossless_storage_review.md`. The first review and a
separate check found a fresh-session loading failure: dropping the package
attribute from the stored Matrix class name prevented its class from loading.
The fix preserves the whole class value. The validation now starts a fresh
`Rscript --vanilla` process with only the documented helper source, verifies
that Matrix was initially unloaded, and checks the restored matrix's serialized
bytes. Log: `out/20261028_storage_validation/fresh_reader.log`. The reviewer
independently verified this fix on the final helper.

Proposed house rule: "2026-10-28: Test archive readers in a fresh R process with
only the documented setup; retain package attributes on stored S4 class names."
The proposal has not been added to AGENTS.md. Matrix version is recorded in
sessionInfo; retaining the same package environment remains the archive policy.

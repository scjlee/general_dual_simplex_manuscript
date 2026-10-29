# Summarize saved per-gene variances by ascending observed-total rank.
# Rscript figure/fig1/panelC_sweep/summarize.R
here <- "figure/fig1/panelC_sweep"
runs <- read.csv(file.path(here, "runs.csv"))
x <- read.csv("out/panelC_sweep/gene_shares.csv")
rows <- list(); bins <- list()
bin_size <- 30L
for (id in which(runs$SEED == min(runs$SEED) & runs$NOISE != "none")) {
  fields <- c("K", "MARKER_FOLD", "NOISE", "FRACTION", "DISPERSION", "NORMAL_SD", "MUL_SD", "MARGINAL")
  same <- rep(TRUE, nrow(runs))
  for (field in fields) {
    target <- runs[[field]][id]
    same <- same & if (is.na(target)) is.na(runs[[field]]) else !is.na(runs[[field]]) & runs[[field]] == target
  }
  ids <- which(same)
  ranked <- lapply(ids, function(i) x[x$run_id == i, ])
  n <- min(vapply(ranked, nrow, integer(1)))
  mat <- vapply(ranked, function(z) z$share_scaled_pct[seq_len(n)], numeric(n))
  rows[[length(rows) + 1L]] <- cbind(runs[rep(id, n), fields], data.frame(rank = seq_len(n),
    mean_pct = rowMeans(mat), lo_pct = apply(mat, 1L, min), hi_pct = apply(mat, 1L, max), n_seeds = length(ids)))
  bin <- ceiling(seq_len(n) / bin_size)
  binned <- vapply(seq_len(ncol(mat)), function(j) as.numeric(tapply(mat[, j], bin, mean)), numeric(max(bin)))
  bins[[length(bins) + 1L]] <- cbind(runs[rep(id, nrow(binned)), fields],
    data.frame(rank = as.numeric(tapply(seq_len(n), bin, mean)),
      rank_first = as.numeric(tapply(seq_len(n), bin, min)),
      rank_last = as.numeric(tapply(seq_len(n), bin, max)),
      mean_pct = rowMeans(binned), lo_pct = apply(binned, 1L, min),
      hi_pct = apply(binned, 1L, max), n_seeds = length(ids)))
}
y <- do.call(rbind, rows)
write.csv(y, file.path(here, "variance_by_rank.csv"), row.names = FALSE)
write.csv(do.call(rbind, bins), file.path(here, "variance_by_rank_bins.csv"), row.names = FALSE)
checks <- read.csv(file.path(here, "checks.csv"))
cat("Runs:", nrow(runs), "; seeds:", paste(sort(unique(runs$SEED)), collapse = ", "), "\n")
cat("Marginal:", paste(unique(runs$MARGINAL), collapse = ", "), "\n")
cat("Genes:", range(checks$genes), "; samples:", range(checks$samples), "\n")
cat("Maximum saved-variance recomputation error:", max(checks$stored_variance_error), "\n")
cat("Maximum bi-whitened leading-pair error:", max(checks$leading_pair_error), "\n")
cat("Nonconverged uniform scalings:", sum(!checks$uniform_converged, na.rm = TRUE), "\n")
cat("Percent-share sums:", range(vapply(split(x$share_scaled_pct, x$run_id), sum, numeric(1))), "\n")
cat("Plotted share range, including bands:", range(y$lo_pct, y$hi_pct), "\n")

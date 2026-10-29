# Run from the manuscript root; uses saved scaling, never fits or simulates.
# Rscript figure/fig1/panelC_sweep/extract_shares.R [input.rds]
library(GeneralDualSimplex)
source("artifact/20261028_simulation_helpers.R")
here <- "figure/fig1/panelC_sweep"
dir.create("out/panelC_sweep", recursive = TRUE, showWarnings = FALSE)
args <- commandArgs(trailingOnly = TRUE)
input <- if (length(args)) args[1] else "/data/simulation_runs_k3.rds"
runs <- as.data.frame(readRDS(input))
write.csv(runs[setdiff(names(runs), "result")], file.path(here, "runs.csv"), row.names = FALSE)
cat("Saved runs:", nrow(runs), "\n")
print(unique(runs[setdiff(names(runs), c("result", "SEED"))]), row.names = FALSE)
cat("Seeds:", sort(unique(runs$SEED)), "\n")
str(runs$result[[1]], max.level = 2, list.len = 20)
versions <- unique(vapply(runs$result, `[[`, character(1), "package_version"))
writeLines(c(paste("input", input), paste("saved_package_version", versions),
             paste("installed_version", packageVersion("GeneralDualSimplex")),
             paste("current_checkout_commit", system2("git", c("-C", "../general_dual_simplex", "rev-parse", "HEAD"), stdout = TRUE)),
             "current_checkout_uncommitted_R_src:", system2("git", c("-C", "../general_dual_simplex", "status", "--porcelain", "R", "src"), stdout = TRUE),
             "The generating commit is not embedded in the supplied RDS; current checkout is context, not verified generation provenance."),
           file.path(here, "package_commit.txt"))
rows <- vector("list", nrow(runs)); checks <- vector("list", nrow(runs))
for (i in seq_len(nrow(runs))) {
  state <- runs$result[[i]]$state
  V <- state$data
  if (is.list(V) && identical(V$format, "matrix-values-v1")) V <- unpack_observed_matrix(V)
  V <- as.matrix(V[state$row_filter, state$column_filter, drop = FALSE])
  s <- state$scaling
  Z <- sweep(s$r / sqrt(s$a) * V, 2L, s$c / sqrt(s$b), "*")
  residual <- Z - sqrt(s$a) %o% sqrt(s$b)
  q <- rowSums(residual^2)
  ord <- order(rowSums(V)) # ascending, matching the existing panel C
  rows[[i]] <- data.frame(run_id = i, gene = rownames(V)[ord], rank = seq_along(ord),
                          observed_total = rowSums(V)[ord], share_Z_pct = 100 * q[ord] / sum(q),
                          scaled_var = state$metadata$row$scaled_var[state$row_filter][ord],
                          scaled_total = state$metadata$row$scaled_total[state$row_filter][ord])
  rows[[i]]$share_scaled_pct <- 100 * rows[[i]]$scaled_var / sum(rows[[i]]$scaled_var)
  # Check the defining singular pair and the independent inertia identity.
  p <- sweep(s$r * V, 2L, s$c, "*") / s$a
  q2 <- s$a * rowSums(sweep(sweep(p, 2L, s$b, "-")^2, 2L, s$b, "/"))
  checks[[i]] <- data.frame(run_id = i, genes = nrow(V), samples = ncol(V),
    total_inertia = sum(q), share_sum = sum(rows[[i]]$share_Z_pct),
    leading_pair_error = max(abs(Z %*% sqrt(s$b) - sqrt(s$a)), abs(crossprod(Z, sqrt(s$a)) - sqrt(s$b))),
    inertia_identity_error = max(abs(q - q2)),
    stored_variance_error = max(abs(state$metadata$row$scaled_var[state$row_filter] - rowSums((sweep(s$r * V, 2L, s$c, "*") - rowMeans(sweep(s$r * V, 2L, s$c, "*")))^2) / (ncol(V) - 1L))),
    uniform_converged = if (runs$MARGINAL[i] == "uniform") isTRUE(s$sinkhorn$converged) else NA)
  runs$result[i] <- list(NULL)
  if (i %% 20L == 0L) cat("Processed", i, "runs\n")
}
write.csv(do.call(rbind, rows), "out/panelC_sweep/gene_shares.csv", row.names = FALSE)
write.csv(do.call(rbind, checks), file.path(here, "checks.csv"), row.names = FALSE)

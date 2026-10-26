# Cumulative gene and sample mass under uniform and expression scaling, Figure 1B.
# Archived 2026-10-26 (replaced by the rank plot in figure/fig1/panelB/).
# Run from the manuscript root: Rscript figure/fig1/panelB/archive/20261026_cumulative/mass.R
# Input: the observed matrix V of panel A (figure/fig1/panelA/simulation.rds),
# with panel A's filter (nonzero genes). Discussion: artifact/20261026_figure1_discussion.md.
# Illustrative single simulated matrix, not a benchmark.
library(GeneralDualSimplex)
here <- "figure/fig1/panelB/archive/20261026_cumulative"
pkg <- "/workspace/dual_simplex_functional/general_dual_simplex"
writeLines(c(
  paste("commit", system2("git", c("-C", pkg, "rev-parse", "HEAD"), stdout = TRUE)),
  paste("installed_version", packageVersion("GeneralDualSimplex")),
  "uncommitted_R_src:", system2("git", c("-C", pkg, "status", "--porcelain", "R", "src"), stdout = TRUE)),
  file.path(here, "package_commit.txt"))

sim <- readRDS("figure/fig1/panelA/simulation.rds")
Yfull <- sim$observed
Y <- Yfull[rowSums(Yfull) > 0, , drop = FALSE]  # same filter as panel A

# Gene mass a = rowSums(D_r V D_c) and sample mass b = colSums(D_r V D_c), as
# achieved by each fitted scaling. Uniform curves use achieved masses, not targets.
scale <- function(type) (CreateDSO(Y) |> ScaleDSO(type = type))@scaling
uniform <- scale("uniform")
expression <- scale("expression")

# One table per margin; items ordered by observed total, ties broken by name.
cumulative <- function(totals, uniform_mass, expression_mass, item) {
  ord <- order(totals, names(totals))
  n <- length(totals)
  data <- data.frame(
    rank = seq_len(n), percent = 100 * seq_len(n) / n,
    name = names(totals)[ord], observed_total = totals[ord],
    uniform_share_percent = 100 * uniform_mass[ord],
    expression_share_percent = 100 * expression_mass[ord],
    uniform_cumulative_percent = 100 * cumsum(uniform_mass[ord]),
    expression_cumulative_percent = 100 * cumsum(expression_mass[ord]),
    raw_cumulative_percent = 100 * cumsum(totals[ord] / sum(totals)))
  names(data)[names(data) == "name"] <- item
  data
}
genes <- cumulative(rowSums(Y), uniform$a, expression$a, "gene")
samples <- cumulative(colSums(Y), uniform$b, expression$b, "sample")
write.csv(genes, file.path(here, "mass_by_gene.csv"), row.names = FALSE)
write.csv(samples, file.path(here, "mass_by_sample.csv"), row.names = FALSE)

# Scaled cumulative share where the observed cumulative share reaches 50%,
# by linear interpolation between consecutive items (origin included).
at_observed_half <- function(data, y) {
  approx(c(0, data$raw_cumulative_percent), c(0, y), xout = 50, ties = "ordered")$y
}
margin_summary <- function(data, prefix, target) {
  n <- nrow(data)
  data.frame(
    quantity = paste0(prefix, c("_count", "_uniform_mass_max_abs_deviation_from_target",
                                "_uniform_cumulative_percent_at_observed_half",
                                "_expression_cumulative_percent_at_observed_half",
                                "_items_percent_at_observed_half",
                                "_max_abs_raw_minus_expression_cumulative_percent",
                                "_observed_total_min", "_observed_total_max")),
    value = c(n, max(abs(data$uniform_share_percent / 100 - target)),
              at_observed_half(data, data$uniform_cumulative_percent),
              at_observed_half(data, data$expression_cumulative_percent),
              100 * sum(data$raw_cumulative_percent < 50) / n,
              max(abs(data$raw_cumulative_percent - data$expression_cumulative_percent)),
              min(data$observed_total), max(data$observed_total)))
}
summary <- rbind(
  data.frame(quantity = c("genes_removed_by_filter", "uniform_converged", "uniform_iterations",
                          "uniform_max_relative_marginal_error",
                          "expression_total_mass", "uniform_total_mass"),
             value = c(nrow(Yfull) - nrow(Y), uniform$sinkhorn$converged,
                       uniform$sinkhorn$iterations, uniform$sinkhorn$max_relative_marginal_error,
                       sum(expression$a), sum(uniform$a))),
  margin_summary(genes, "genes", 1 / nrow(Y)),
  margin_summary(samples, "samples", 1 / ncol(Y)))
write.csv(summary, file.path(here, "mass_summary.csv"), row.names = FALSE)
print(format(summary, digits = 15), row.names = FALSE)

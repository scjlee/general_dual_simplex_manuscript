# Illustrative noisy gene-simplex projections, uniform vs expression scaling.
# Run from the manuscript root: Rscript figure/fig1/panelA/points.R [library_fraction] [seed]
# Source model: package .ai/bench/20261022_space-distortion.R.
# Original derivation: artifact/20261026_fig1A-gene-simplex.md; current noise/axes:
# artifact/20261026_fig1A-noise-and-axes.md.
library(GeneralDualSimplex)
here <- "figure/fig1/panelA"
pkg <- "/workspace/dual_simplex_functional/general_dual_simplex"
writeLines(c(
  paste("commit", system2("git", c("-C", pkg, "rev-parse", "HEAD"), stdout = TRUE)),
  paste("installed_version", packageVersion("GeneralDualSimplex")),
  "uncommitted_R_src:", system2("git", c("-C", pkg, "status", "--porcelain", "R", "src"), stdout = TRUE)),
  file.path(here, "package_commit.txt"))
args <- commandArgs(TRUE)
frac <- if (length(args) >= 1) as.numeric(args[1]) else 0.04
seed <- if (length(args) >= 2) as.integer(args[2]) else 1L
k <- 3
orth <- function(A) qr.Q(qr(A))
set.seed(seed)
sim <- GenerateMixture(500, 200, k, n_marker = 20, marker_fold = 5, profile_spread_sd = 0.2)
Yfull <- ApplyNBNoise(sim, dispersion = 0, library_size_fraction = frac)$Observed
Y <- Yfull[rowSums(Yfull) > 0, , drop = FALSE]
H <- sim$H
X <- sim$W %*% H
saveRDS(list(W = sim$W, H = H, signal = X, observed = Yfull,
             parameters = list(seed = seed, library_fraction = frac, dispersion = 0,
                               n_feature = 500L, n_sample = 200L, k = k, n_marker = 20L,
                               marker_fold = 5, profile_spread_sd = 0.2)),
        file.path(here, "simulation.rds"), version = 3)

# Noisy normalized gene profiles F = Y D_c / rowsums(Y D_c).
# Their projected coordinates C = F Psi^T = Phi^T Sigma.
# Project the true pure component profiles T = H D_c / rowsums(H D_c)
# by the SAME map. The dashed triangle is T Psi^T, not a fitted envelope.
project_genes <- function(type) {
  object <- CreateDSO(Y) |> ScaleDSO(type = type) |> FindProjection(k = k, method = "svd")
  s <- object@scaling; g <- object@projection$gsvd()
  F <- sweep(Y, 2, s$c, "*"); F <- F / rowSums(F)
  T <- sweep(H, 2, s$c, "*"); T <- T / rowSums(T)
  C <- F %*% t(g$Psi)
  vertices <- T %*% t(g$Psi)
  # Rigid rotation/reflection only: orient component identities consistently.
  # Never stretch the triangle or fit/filter the noisy points for display.
  target <- rbind(c(0, 2 / sqrt(6)), c(1 / sqrt(2), -1 / sqrt(6)),
                  c(-1 / sqrt(2), -1 / sqrt(6)))
  centre <- colMeans(vertices[, 2:3])
  v <- sweep(vertices[, 2:3], 2, centre, "-")
  rotation <- svd(crossprod(v, target))
  rotation <- rotation$u %*% t(rotation$v)
  xy <- sweep(C[, 2:3], 2, centre, "-") %*% rotation
  v <- v %*% rotation
  group <- ifelse(grepl("^marker", rownames(Y)),
                  sub("^marker([0-9]+)\\..*$", "marker\\1", rownames(Y)), "background")
  # Retain the original H-subspace diagnostic. Figure labels now report W
  # recovery to match the gene objects (D and E); neither is a point-cloud RMSE.
  Q <- orth(t(g$Psi) * (g$b / s$c))
  Hor <- t(Q %*% crossprod(Q, t(H)))
  W <- sim$W[rownames(Y), , drop = FALSE]
  Qw <- orth(t(g$Phi) * (g$a / s$r))
  Wor <- Qw %*% crossprod(Qw, W)
  # The true noiseless profiles are convex combinations of the true vertices.
  F0 <- sweep(X[rownames(Y), , drop = FALSE], 2, s$c, "*"); F0 <- F0 / rowSums(F0)
  B0 <- sweep(sim$W[rownames(Y), , drop = FALSE], 2, rowSums(sweep(H, 2, s$c, "*")), "*")
  B0 <- B0 / rowSums(B0)
  list(
    points = data.frame(scaling = type, gene = rownames(Y), group = group, x = xy[, 1], y = xy[, 2]),
    vertices = data.frame(scaling = type, component = seq_len(k), x = v[, 1], y = v[, 2]),
    metrics = data.frame(scaling = type, oracle_H_rmse = sqrt(mean((Hor - H)^2)),
                         oracle_W_rmse = sqrt(mean((Wor - W)^2)),
                         coordinate_identity_error = max(abs(C - t(g$Phi) %*% diag(g$sigma[1:k]))),
                         constant_coordinate_error = max(abs(C[, 1] - 1)),
                         noiseless_convex_error = max(abs(F0 - B0 %*% T)),
                         genes = nrow(Y), markers = sum(group != "background"),
                         background = sum(group == "background")))
}
projections <- lapply(c("uniform", "expression"), project_genes)
write.csv(do.call(rbind, lapply(projections, `[[`, "points")), file.path(here, "gene_points.csv"), row.names = FALSE)
write.csv(do.call(rbind, lapply(projections, `[[`, "vertices")), file.path(here, "simplex_vertices.csv"), row.names = FALSE)
metrics <- do.call(rbind, lapply(projections, `[[`, "metrics"))
write.csv(metrics, file.path(here, "projection_metrics.csv"), row.names = FALSE)
print(metrics, row.names = FALSE, digits = 7)

# Heatmaps: eight genuinely mixed columns, matched to fixed interior targets.
# No point selection is performed for the projection plots above.
targets <- rbind(c(.65, .20, .15), c(.55, .30, .15), c(.40, .40, .20),
                 c(.20, .60, .20), c(.15, .55, .30), c(.20, .35, .45),
                 c(.20, .20, .60), c(.33, .33, .34))
available <- which(apply(H, 2, min) >= .1)
smp <- integer(nrow(targets))
for (i in seq_len(nrow(targets))) {
  distance <- colSums((H[, available, drop = FALSE] - targets[i, ])^2)
  smp[i] <- available[which.min(distance)]
  available <- setdiff(available, smp[i])
}
genes <- c(paste0("marker", rep(1:k, each = 2), ".", 1:2), "background1", "background2")
Wshow <- sim$W[genes, , drop = FALSE]
Xshow <- X[genes, smp, drop = FALSE]
Yshow <- Yfull[genes, smp, drop = FALSE]
# Show relative profiles: W scaled within rows; H uses its actual fractions.
# Signal and observed tiles share a per-gene scale after adjusting only the
# known scalar sampling depth for display. Original observed values are saved.
shared_max <- apply(cbind(Xshow, Yshow / frac), 1, max)
tile <- function(name, raw, display) data.frame(matrix = name, row = c(row(raw)), col = c(col(raw)),
                                              value = c(display), raw_value = c(raw))
tiles <- rbind(tile("W", Wshow, Wshow / apply(Wshow, 1, max)),
               tile("H", H[, smp], H[, smp]),
               tile("X", Xshow, Xshow / shared_max),
               tile("Y", Yshow, (Yshow / frac) / shared_max))
write.csv(tiles, file.path(here, "tiles.csv"), row.names = FALSE)
write.csv(data.frame(display_column = seq_along(smp), sample = colnames(H)[smp],
                     t(H[, smp])), file.path(here, "heatmap_samples.csv"), row.names = FALSE)
cat("Heatmap fraction range:", range(H[, smp]), "; column sums:", range(colSums(H[, smp])), "\n")
cat("All projections contain every nonzero observed gene; heatmap sample selection only affects heatmaps.\n")

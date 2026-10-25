# Oracle projection of the true H onto the estimated H space, uniform vs expression scaling.
# Setting follows the package's .ai/bench/20261022_space-distortion.R (k = 3, Poisson, spread 0.2, marker fold 5).
# Usage (repo root): Rscript figure/fig1/panelA/points.R [library_size_fraction] [seed]
library(GeneralDualSimplex)
here <- "figure/fig1/panelA"
pkg <- "/workspace/dual_simplex_functional/general_dual_simplex"
writeLines(c(
  paste("commit", system2("git", c("-C", pkg, "rev-parse", "HEAD"), stdout = TRUE)),
  paste("installed_version", packageVersion("GeneralDualSimplex")),
  "uncommitted_R_src:", system2("git", c("-C", pkg, "status", "--porcelain", "R", "src"), stdout = TRUE)),
  file.path(here, "package_commit.txt"))
args <- commandArgs(TRUE)
frac <- if (length(args) >= 1) as.numeric(args[1]) else 0.1
seed <- if (length(args) >= 2) as.integer(args[2]) else 1L
k <- 3
orth <- function(A) qr.Q(qr(A))
set.seed(seed)
sim <- GenerateMixture(500, 200, k, n_marker = 20, marker_fold = 5, profile_spread_sd = 0.2)
Yfull <- ApplyNBNoise(sim, dispersion = 0, library_size_fraction = frac)$Observed
Y <- Yfull[rowSums(Yfull) > 0, ]
H <- sim$H
oracle <- function(type) {
  V <- CreateDSO(Y) |> ScaleDSO(type = type) |> FindProjection(k = k, method = "svd")
  s <- V@scaling; g <- V@projection$gsvd()
  Q <- orth(t(g$Psi) * (g$b / s$c))
  t(Q %*% crossprod(Q, t(H)))
}
# Heatmap tiles: 2 markers per component + 2 background genes, 8 samples ordered by dominant component.
genes <- c(paste0("marker", rep(1:k, each = 2), ".", 1:2), rownames(sim$W)[k * 20 + 1:2])
smp <- order(apply(H, 2, which.max), -apply(H, 2, max))
smp <- unlist(lapply(1:k, function(j) head(smp[apply(H[, smp], 2, which.max) == j], c(3, 3, 2)[j])))
rescale <- function(M) { L <- log1p(M); (L - min(L)) / (max(L) - min(L)) }
tile <- function(name, M) data.frame(matrix = name, row = c(row(M)), col = c(col(M)), value = c(rescale(M)))
X <- sim$W %*% H
tiles <- rbind(tile("W", sim$W[genes, ]), tile("H", H[, smp]),
               tile("X", X[genes, smp]), tile("Y", Yfull[genes, smp]))
write.csv(tiles, file.path(here, "tiles.csv"), row.names = FALSE)

pts <- rbind(
  data.frame(set = "truth", sample = seq_len(ncol(H)), t(H)),
  data.frame(set = "uniform", sample = seq_len(ncol(H)), t(oracle("uniform"))),
  data.frame(set = "expression", sample = seq_len(ncol(H)), t(oracle("expression"))))
names(pts)[3:5] <- paste0("h", 1:k)
out <- file.path(here, sprintf("points_frac%s_seed%d.csv", frac, seed))
write.csv(pts, out, row.names = FALSE)
for (st in c("uniform", "expression")) {
  e <- as.matrix(pts[pts$set == st, 3:5]) - as.matrix(pts[pts$set == "truth", 3:5])
  cat(sprintf("%-10s oracle RMSE %.4f  max|colsum-1| %.1e\n", st, sqrt(mean(e^2)),
              max(abs(rowSums(pts[pts$set == st, 3:5]) - 1))))
}
cat("wrote", out, "\n")

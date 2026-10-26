# Illustrative data for D/S simplex and E/F oracle-error SVG/PNG figures.
# RENV_CONFIG_SANDBOX_ENABLED=FALSE Rscript figure/fig1/panelD/projections.R
# Simulation/noise design copied from panelC/noise_share.R; gene projection and
# H oracle copied from panelA/points.R; W oracle and sample geometry use the
# dual package reconstruction maps (artifact/20261026_fig1EF-oracle-png.md
# and artifact/20261026_fig1D-samples-and-EF-svg.md). No simplex is fitted.
library(GeneralDualSimplex)
d_dir <- "figure/fig1/panelD"
e_dir <- "figure/fig1/panelE"
f_dir <- "figure/fig1/panelF"
sample_dir <- "figure/fig1/panelD_samples"
dir.create(e_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(f_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(sample_dir, recursive = TRUE, showWarnings = FALSE)
pkg <- "/workspace/dual_simplex_functional/general_dual_simplex"
provenance <- c(
  paste("commit", system2("git", c("-C", pkg, "rev-parse", "HEAD"), stdout = TRUE)),
  paste("installed_version", packageVersion("GeneralDualSimplex")),
  "uncommitted_R_src:", system2("git", c("-C", pkg, "status", "--porcelain", "R", "src"), stdout = TRUE))
writeLines(provenance, file.path(d_dir, "package_commit.txt"))
writeLines(provenance, file.path(e_dir, "package_commit.txt"))
writeLines(provenance, file.path(f_dir, "package_commit.txt"))
writeLines(provenance, file.path(sample_dir, "package_commit.txt"))
A <- readRDS("figure/fig1/panelA/simulation.rds")
pa <- A$parameters
frac <- pa$library_fraction
med <- median(frac * A$signal)
phi <- 1 / med
sigma <- sqrt(med)
models <- c("Poisson", "Proportional", "Normal, floored at 0")
scalings <- c("uniform", "expression")
write.csv(data.frame(model = models, library_fraction = frac,
  median_expected_count_A = med, phi = c(NA, phi, NA), sigma = c(NA, NA, sigma),
  replicates = 5L, representative_draw = 1L),
  file.path(e_dir, "noise_parameters.csv"), row.names = FALSE)
metrics <- genes <- vertices <- oracle <- oracle_w <- noiseless <- list()
sample_points <- sample_vertices <- sample_checks <- list()
for (model in models) for (draw in 1:5) {
  # Regenerate the signal before EACH model, exactly as in C. Within a model,
  # each draw has a fresh signal and noise. Both scalings receive the same V.
  set.seed(draw)
  sim <- GenerateMixture(pa$n_feature, pa$n_sample, pa$k, n_marker = pa$n_marker,
    marker_fold = pa$marker_fold, profile_spread_sd = pa$profile_spread_sd)
  H <- sim$H
  mu <- frac * sim$W %*% H
  V <- switch(model,
    Poisson = ApplyNBNoise(sim, dispersion = 0, library_size_fraction = frac)$Observed,
    Proportional = mu * matrix(rgamma(length(mu), shape = 1 / phi, rate = 1 / phi), nrow(mu)),
    `Normal, floored at 0` = pmax(mu + matrix(rnorm(length(mu), 0, sigma), nrow(mu)), 0))
  if (draw == 1 && model == "Poisson")
    cat("Maximum difference from panel A observed V:", max(abs(V - A$observed)), "\n")
  V <- V[rowSums(V) > 0, , drop = FALSE]
  for (sc in scalings) {
    object <- CreateDSO(V) |> ScaleDSO(type = sc) |> FindProjection(k = pa$k, method = "svd")
    s <- object@scaling
    g <- object@projection$gsvd()
    # Package reconstruct_H_tilde gives X Psi D_b. Undo D_c: the recovered
    # H row space is spanned by the rows of Psi D_b D_c^-1. Thus A below is
    # n x k, Q = orth(A), and Hor = H Q Q^T is the Euclidean least-squares
    # projection of each true H row, with no clipping or renormalization.
    basis <- t(g$Psi) * (g$b / s$c)
    Q <- qr.Q(qr(basis))
    Hor <- t(Q %*% crossprod(Q, t(H)))
    residual <- H - Hor
    # reconstruct_W_tilde = D_a Phi^T Omega. Undo D_r: the original
    # W column space is span(D_r^-1 D_a Phi^T), an m_kept x k basis.
    # Project the original simulated W in native expression units, without
    # library-fraction rescaling, column normalization, or positivity constraints.
    W <- sim$W[rownames(V), , drop = FALSE]
    basis_w <- t(g$Phi) * (g$a / s$r)
    Qw <- qr.Q(qr(basis_w))
    Wor <- Qw %*% crossprod(Qw, W)
    metrics[[length(metrics) + 1]] <- data.frame(model, draw, scaling = sc,
      oracle_H_rmse = sqrt(mean(residual^2)), genes = nrow(V),
      uniform_converged = if (sc == "uniform") isTRUE(s$sinkhorn$converged) else NA,
      residual_orthogonality_error = max(abs(residual %*% Q)),
      least_squares_agreement_error = max(abs(Hor - t(basis %*% qr.coef(qr(basis), t(H))))),
      oracle_W_rmse = sqrt(mean((W - Wor)^2)),
      W_residual_orthogonality_error = max(abs(crossprod(Qw, W - Wor))),
      W_least_squares_agreement_error = max(abs(Wor - basis_w %*% qr.coef(qr(basis_w), W))))
    oracle[[length(oracle) + 1]] <- data.frame(model, draw, scaling = sc,
      component = rep(seq_len(pa$k), ncol(H)), sample = rep(colnames(H), each = pa$k),
      true_H = c(H), oracle_H = c(Hor))
    oracle_w[[length(oracle_w) + 1]] <- data.frame(model, draw, scaling = sc,
      component = rep(seq_len(pa$k), each = nrow(W)), gene = rep(rownames(W), pa$k),
      true_W = c(W), oracle_W = c(Wor))
    if (draw == 1) {
      F <- sweep(V, 2, s$c, "*")
      F <- F / rowSums(F)
      T <- sweep(H, 2, s$c, "*")
      T <- T / rowSums(T)
      C <- F %*% t(g$Psi)
      v <- T %*% t(g$Psi)
      target <- rbind(c(0, 2 / sqrt(6)), c(1 / sqrt(2), -1 / sqrt(6)),
                      c(-1 / sqrt(2), -1 / sqrt(6)))
      centre <- colMeans(v[, 2:3])
      v <- sweep(v[, 2:3], 2, centre, "-")
      rot <- svd(crossprod(v, target))
      rot <- rot$u %*% t(rot$v)
      xy <- sweep(C[, 2:3], 2, centre, "-") %*% rot
      v <- v %*% rot
      group <- ifelse(grepl("^marker", rownames(V)),
        sub("^marker([0-9]+)\\..*$", "marker\\1", rownames(V)), "background")
      genes[[length(genes) + 1]] <- data.frame(model, draw, scaling = sc,
        gene = rownames(V), group, x = xy[, 1], y = xy[, 2])
      vertices[[length(vertices) + 1]] <- data.frame(model, draw, scaling = sc,
        component = seq_len(pa$k), x = v[, 1], y = v[, 2])
      # Dual feature-space simplex: normalized observed sample columns and
      # known pure W columns, mapped with the SAME Phi. The first coordinate
      # is 1; plot dimensions 2:3 after the same rigid orientation rule.
      Fs <- V * s$r
      Fs <- sweep(Fs, 2, colSums(Fs), "/")
      Ts <- W * s$r
      Ts <- sweep(Ts, 2, colSums(Ts), "/")
      Cs <- t(g$Phi %*% Fs)
      vs <- t(g$Phi %*% Ts)
      cs <- colMeans(vs[, 2:3])
      vs <- sweep(vs[, 2:3], 2, cs, "-")
      rs <- svd(crossprod(vs, target))
      rs <- rs$u %*% t(rs$v)
      xys <- sweep(Cs[, 2:3], 2, cs, "-") %*% rs
      vs <- vs %*% rs
      sample_points[[length(sample_points) + 1]] <- data.frame(model, draw,
        scaling = sc, sample = colnames(V), x = xys[, 1], y = xys[, 2])
      sample_vertices[[length(sample_vertices) + 1]] <- data.frame(model, draw,
        scaling = sc, component = seq_len(pa$k), x = vs[, 1], y = vs[, 2])
      # Noiseless normalized samples are convex combinations of the known
      # W vertices: weights are colNormalize(D_colSums(D_r W) H).
      F0s <- mu[rownames(V), , drop = FALSE] * s$r
      F0s <- sweep(F0s, 2, colSums(F0s), "/")
      Bs <- H * colSums(W * s$r)
      Bs <- sweep(Bs, 2, colSums(Bs), "/")
      sample_checks[[length(sample_checks) + 1]] <- data.frame(model, draw, scaling = sc,
        constant_coordinate_error = max(abs(Cs[, 1] - 1)),
        svd_coordinate_identity_error = max(abs(t(Cs) - g$sigma * g$Psi)),
        noiseless_convex_error = max(abs(F0s - Ts %*% Bs)),
        samples = nrow(Cs), oracle_H_rmse = sqrt(mean(residual^2)))
    }
  }
  if (model == "Poisson") for (sc in scalings) {
    obj0 <- CreateDSO(mu) |> ScaleDSO(type = sc) |> FindProjection(k = pa$k, method = "svd")
    s0 <- obj0@scaling
    g0 <- obj0@projection$gsvd()
    Q0 <- qr.Q(qr(t(g0$Psi) * (g0$b / s0$c)))
    H0 <- t(Q0 %*% crossprod(Q0, t(H)))
    Qw0 <- qr.Q(qr(t(g0$Phi) * (g0$a / s0$r)))
    W0 <- Qw0 %*% crossprod(Qw0, sim$W)
    noiseless[[length(noiseless) + 1]] <- data.frame(draw, scaling = sc,
      oracle_H_rmse = sqrt(mean((H - H0)^2)),
      oracle_W_rmse = sqrt(mean((sim$W - W0)^2)))
  }
}
m <- do.call(rbind, metrics)
h_cols <- c("model", "draw", "scaling", "oracle_H_rmse", "genes", "uniform_converged",
            "residual_orthogonality_error", "least_squares_agreement_error")
w_cols <- c("model", "draw", "scaling", "oracle_W_rmse", "genes", "uniform_converged",
            "W_residual_orthogonality_error", "W_least_squares_agreement_error")
write.csv(m[, w_cols], file.path(e_dir, "projection_metrics.csv"), row.names = FALSE)
write.csv(m[, h_cols], file.path(f_dir, "projection_metrics.csv"), row.names = FALSE)
write.csv(do.call(rbind, oracle), file.path(f_dir, "oracle_H.csv"), row.names = FALSE)
write.csv(do.call(rbind, oracle_w), file.path(e_dir, "oracle_W.csv"), row.names = FALSE)
n0 <- do.call(rbind, noiseless)
write.csv(n0[, c("draw", "scaling", "oracle_W_rmse")], file.path(e_dir, "noiseless_metrics.csv"), row.names = FALSE)
write.csv(n0[, c("draw", "scaling", "oracle_H_rmse")], file.path(f_dir, "noiseless_metrics.csv"), row.names = FALSE)
file.copy(file.path(e_dir, "noise_parameters.csv"), file.path(f_dir, "noise_parameters.csv"), overwrite = TRUE)
write.csv(do.call(rbind, genes), file.path(d_dir, "gene_points.csv"), row.names = FALSE)
write.csv(do.call(rbind, vertices), file.path(d_dir, "simplex_vertices.csv"), row.names = FALSE)
write.csv(do.call(rbind, sample_points), file.path(sample_dir, "sample_points.csv"), row.names = FALSE)
write.csv(do.call(rbind, sample_vertices), file.path(sample_dir, "simplex_vertices.csv"), row.names = FALSE)
write.csv(do.call(rbind, sample_checks), file.path(sample_dir, "projection_checks.csv"), row.names = FALSE)
print(do.call(rbind, sample_checks), row.names = FALSE, digits = 7)
print(m, row.names = FALSE, digits = 7)
cat("Mean oracle H RMSE (five draws):\n")
print(aggregate(oracle_H_rmse ~ model + scaling, m, mean), row.names = FALSE, digits = 8)
cat("Mean oracle W RMSE (five draws; original W expression units):\n")
print(aggregate(oracle_W_rmse ~ model + scaling, m, mean), row.names = FALSE, digits = 8)
cat("Noise matching: median mu_A =", med, "; phi =", phi, "; sigma =", sigma, "\n")
cat("Maximum noiseless H RMSE:", max(n0$oracle_H_rmse), "\n")
cat("Maximum noiseless W RMSE:", max(n0$oracle_W_rmse), "\n")
cat("All data are illustrative; these five draws are not benchmark evidence.\n")

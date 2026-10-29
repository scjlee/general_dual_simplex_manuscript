# Run from the manuscript root; optional first argument: temporary package library.
args <- commandArgs(TRUE)
if (length(args)) .libPaths(c(args[1L], .libPaths()))
library(GeneralDualSimplex)
source("artifact/20261028_simulation_helpers.R")
grDevices::pdf(NULL)
out <- "out/20261028_vertex_overlay"
dir.create(out, recursive = TRUE, showWarnings = FALSE)
experiments <- readRDS("out/20261028_simulation_validation/full_gzip.rds")

same <- function(x, y) stopifnot(identical(x, y))
for (i in seq_len(nrow(experiments))) {
  d <- experiments$result[[i]]
  d@metadata$row$group <- factor(rep(c("A", "B"), length.out = nrow(d@data)))
  d@metadata$column$group <- factor(rep(c("A", "B"), length.out = ncol(d@data)))
  p <- DualPlot(d, history = FALSE, solution = FALSE, raster = FALSE,
                color_by = "group")
  original <- lapply(1:2, function(j) ggplot2::ggplot_build(p[[j]])$data)
  vertices <- d@misc$true_vertices
  vertex_copy <- vertices
  overlaid <- add_true_vertices(p, vertices)
  for (j in 1:2) {
    built <- ggplot2::ggplot_build(overlaid[[j]])$data
    same(built[seq_along(original[[j]])], original[[j]])
    same(ggplot2::ggplot_build(p[[j]])$data, original[[j]])
    same(length(overlaid[[j]]$scales$scales), length(p[[j]]$scales$scales))
    edges <- built[[length(built)]]
    stopifnot(nrow(edges) == 3L, all(edges$linetype == "dashed"),
              all(edges$colour == "black"), all(edges$linewidth == 0.4),
              identical(tail(overlaid[[j]]$layers, 1)[[1]]$show.legend, FALSE))
    coordinates <- if (j == 1L) vertices$X[, c("dim2", "dim3")] else {
      t(vertices$Omega[c("dim2", "dim3"), ])
    }
    same(unname(as.matrix(edges[, c("x", "y")])),
         unname(coordinates[c(1, 1, 2), ]))
    same(unname(as.matrix(edges[, c("xend", "yend")])),
         unname(coordinates[c(2, 3, 3), ]))
  }
  same(vertices, vertex_copy)

  reversed <- add_true_vertices(
    DualPlot(d, dims = c(3, 2), history = FALSE, solution = FALSE, raster = FALSE),
    vertices, dims = c(3, 2), colour = "firebrick", linewidth = 0.5
  )
  for (j in 1:2) {
    edges <- tail(ggplot2::ggplot_build(reversed[[j]])$data, 1)[[1]]
    coordinates <- if (j == 1L) vertices$X[, c("dim3", "dim2")] else {
      t(vertices$Omega[c("dim3", "dim2"), ])
    }
    same(unname(as.matrix(edges[, c("x", "y")])),
         unname(coordinates[c(1, 1, 2), ]))
    stopifnot(all(edges$colour == "firebrick"), all(edges$linewidth == 0.5))
  }
}

# Four projected simplex vertices require all six edges, not just a boundary.
vertices$X <- rbind(vertices$X, colMeans(vertices$X))
vertices$Omega <- cbind(vertices$Omega, rowMeans(vertices$Omega))
four <- add_true_vertices(p, vertices)
stopifnot(nrow(tail(ggplot2::ggplot_build(four[[1]])$data, 1)[[1]]) == 6L,
          nrow(tail(ggplot2::ggplot_build(four[[2]])$data, 1)[[1]]) == 6L)

# History-trimmed objects retain the same plotting path with history = FALSE.
d <- unpack_simulation_dso(pack_simulation_dso(experiments$result[[4]],
                                               keep_history = FALSE))
preview <- add_true_vertices(
  DualPlot(d, history = FALSE, solution = FALSE, raster = FALSE),
  d@misc$true_vertices
) + patchwork::plot_annotation(
  title = "Illustrative fixture: dashed true simplex edges",
  caption = "Precomputed vertices; no scientific result is claimed."
)
ggplot2::ggsave(file.path(out, "preview.png"), preview,
                width = 8, height = 3.8, dpi = 600)
writeLines(capture.output(sessionInfo()), file.path(out, "sessionInfo.txt"))
cat("Overlay checks passed: correct panels and edges, unchanged base plots,\n",
    "styles, reversed dimensions, four vertices, and history-trimmed plots.\n")
grDevices::dev.off()

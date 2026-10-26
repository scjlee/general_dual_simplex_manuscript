# Render SVG masters where present; retain R/grid layout drafts for montages.
# RENV_CONFIG_SANDBOX_ENABLED=FALSE Rscript figure/fig1/panelD/make_mock_panels.R
library(grid)
d_dir <- "figure/fig1/panelD"
e_dir <- "figure/fig1/panelE"
f_dir <- "figure/fig1/panelF"
genes <- read.csv(file.path(d_dir, "gene_points.csv"))
vertices <- read.csv(file.path(d_dir, "simplex_vertices.csv"))
metrics <- read.csv(file.path(f_dir, "projection_metrics.csv"))
w_metrics <- read.csv(file.path(e_dir, "projection_metrics.csv"))
sample_dir <- "figure/fig1/panelD_samples"
samples <- read.csv(file.path(sample_dir, "sample_points.csv"))
sample_vertices <- read.csv(file.path(sample_dir, "simplex_vertices.csv"))
models <- c("Poisson", "Proportional", "Normal, floored at 0")
scalings <- c("uniform", "expression")
branch <- c(uniform = "#E07B28", expression = "#2A7BBF")
gene_col <- c(background = "#B8B8B8", marker1 = "#009E73", marker2 = "#CC79A7", marker3 = "#D69B00")
ink <- "#1A1A1A"
muted <- "#555555"
mm <- function(x) unit(x, "mm")
txt <- function(label, x, y, size = 6, col = ink, bold = FALSE, just = "left") {
  grid.text(label, x = mm(x), y = unit(1, "npc") - mm(y), just = c(just, "centre"),
    gp = gpar(fontfamily = "Liberation Sans", fontsize = size,
              col = col, fontface = if (bold) "bold" else "plain", lineheight = 1.1))
}
seg <- function(x, y, xend, yend, col = "#CCCCCC", lwd = 0.5, lty = 1) {
  grid.lines(x = mm(c(x, xend)), y = unit(1, "npc") - mm(c(y, yend)),
    gp = gpar(col = col, lwd = lwd, lty = lty))
}
dot <- function(x, y, col, diameter = 1.2, pch = 16) {
  grid.points(x = mm(x), y = unit(1, "npc") - mm(y), pch = pch,
    size = mm(diameter), gp = gpar(col = col, fill = col))
}
draw_D <- function(offset = 0, sample_side = FALSE) {
  txt(if (sample_side) "S" else "D", 1.2, offset + 5, 8, bold = TRUE)
  txt(if (sample_side) "Representative sample simplices" else "Representative gene simplices",
      7, offset + 5, 8, bold = TRUE)
  left <- c(10, 47, 84)
  side <- 29.5
  for (j in seq_along(models)) {
    model <- models[j]
    txt(model, left[j] + side / 2, offset + 13, 6.5, bold = TRUE, just = "centre")
    for (i in seq_along(scalings)) {
      sc <- scalings[i]
      x0 <- left[j]
      y0 <- offset + c(21, 59)[i]
      source_points <- if (sample_side) samples else genes
      source_vertices <- if (sample_side) sample_vertices else vertices
      p <- source_points[source_points$model == model & source_points$scaling == sc, ]
      v <- source_vertices[source_vertices$model == model & source_vertices$scaling == sc, ]
      z <- rbind(p[, c("x", "y")], v[, c("x", "y")])
      mid <- c(mean(range(z$x)), mean(range(z$y)))
      span <- max(diff(range(z$x)), diff(range(z$y)))
      # Fit all points and vertices, independently, preserving equal aspect.
      # Two-mm padding keeps dots within the frame without clipping.
      px <- function(x) x0 + side / 2 + (x - mid[1]) / span * (side - 4)
      py <- function(y) y0 + side / 2 - (y - mid[2]) / span * (side - 4)
      if (sample_side) {
        dot(px(p$x), py(p$y), "#929292", diameter = .85)
        for (component in 1:3)
          dot(px(v$x[component]), py(v$y[component]), gene_col[component + 1], diameter = 1.4)
      } else {
        for (group in names(gene_col)) {
          g <- p[p$group == group, ]
          dot(px(g$x), py(g$y), adjustcolor(gene_col[group], alpha.f = .85),
            diameter = if (group == "background") .65 else .95)
        }
      }
      vv <- rbind(v, v[1, ])
      grid.lines(x = mm(px(vv$x)), y = unit(1, "npc") - mm(py(vv$y)),
        gp = gpar(col = "#666666", lwd = .5, lty = "22"))
      grid.rect(x = mm(x0), y = unit(1, "npc") - mm(y0), width = mm(side), height = mm(side),
        just = c("left", "top"), gp = gpar(fill = NA, col = branch[sc], lwd = .6))
      # Report recovery of the plotted entities: genes -> W, samples -> H.
      md <- if (sample_side) metrics else w_metrics
      m <- md[md$model == model & md$draw == 1 & md$scaling == sc, ]
      error <- m[[if (sample_side) "oracle_H_rmse" else "oracle_W_rmse"]]
      txt(sprintf("oracle RMSE: %.3f", error), x0 + side / 2, y0 - 2.4,
          5.5, col = muted, just = "centre")
      cat(sprintf("%s: %s / %s: %d points, 3 vertices; span %.7g; draw-1 RMSE %.7g\n",
        if (sample_side) "Samples" else "D", model, sc, nrow(p), span, error))
    }
  }
  for (i in 1:2)
    grid.text(c("Uniform scaling", "Expression scaling")[i], x = mm(6.5),
      y = unit(1, "npc") - mm(offset + c(35.75, 73.75)[i]), rot = 90,
      gp = gpar(fontfamily = "Liberation Sans", fontsize = 6.5, col = branch[i], fontface = "bold"))
  txt("Projection 2", 61.75, offset + 92.7, 6, just = "centre")
  grid.text("Projection 3", x = mm(117), y = unit(1, "npc") - mm(offset + 54.75),
    rot = -90, gp = gpar(fontfamily = "Liberation Sans", fontsize = 6, col = ink))
  # Coordinates are rigidly oriented mixtures of GSVD dimensions 2 and 3, as in A.
  txt(if (sample_side) "Components:" else "Markers:", 10, offset + 98, 5.8, col = muted)
  for (i in 1:3) {
    dot(25 + 6 * (i - 1), offset + 98, gene_col[i + 1], 1)
    txt(as.character(i), 26 + 6 * (i - 1), offset + 98, 5.8, col = gene_col[i + 1])
  }
  dot(45, offset + 98, if (sample_side) "#929292" else gene_col[1], 1)
  txt(if (sample_side) "Samples" else "Background", 46.5, offset + 98, 5.8, col = muted)
  seg(67, offset + 98, 72, offset + 98, col = "#666666", lty = "22")
  txt("True components, projected", 73.5, offset + 98, 5.8, col = muted)
  txt("Separate plot scales; equal aspect.",
      60, offset + 103, 5.8, col = muted, just = "centre")
}
draw_error <- function(side, letter, data, offset = 0) {
  txt(letter, 1.2, offset + 5, 8, bold = TRUE)
  txt(paste(side, "oracle error"), 7, offset + 5, 8, bold = TRUE)
  value <- paste0("oracle_", side, "_rmse")
  ymax <- max(pretty(c(0, data[[value]]), n = 4))
  yticks <- pretty(c(0, ymax), n = 4)
  top <- offset + 18
  bottom <- offset + 47
  py <- function(value) bottom - value / ymax * (bottom - top)
  for (j in seq_along(models)) {
    model <- models[j]
    x0 <- c(15, 44, 73)[j]
    xx <- x0 + c(5, 18)
    txt(model, x0 + 11.5, offset + 12.5, 6.5, bold = TRUE, just = "centre")
    for (y in yticks) {
      seg(x0, py(y), x0 + 23, py(y), col = "#E3E3E3", lwd = .4)
      if (j == 1) txt(format(y, trim = TRUE, scientific = FALSE), x0 - 1.4, py(y), 5.5,
                      col = muted, just = "right")
    }
    seg(x0, bottom, x0 + 23, bottom, col = "#777777")
    seg(x0, top, x0, bottom, col = "#777777")
    # Deterministic offsets distinguish all five pairs without changing values.
    shifts <- seq(-1.2, 1.2, length.out = 5)
    for (r in 1:5) {
      z <- data[data$model == model & data$draw == r, ]
      yy <- z[[value]][match(scalings, z$scaling)]
      seg(xx[1] + shifts[r], py(yy[1]), xx[2] + shifts[r], py(yy[2]),
          col = "#B8B8B8", lwd = .4)
    }
    for (i in seq_along(scalings)) {
      sc <- scalings[i]
      z <- data[data$model == model & data$scaling == sc, ]
      z <- z[order(z$draw), ]
      dot(xx[i] + shifts, py(z[[value]]), branch[sc], 1.5)
      avg <- mean(z[[value]])
      seg(xx[i] - 2.1, py(avg), xx[i] + 2.1, py(avg), col = branch[sc], lwd = 1)
      txt(sprintf("%.3f", avg), xx[i], offset + 16, 5.5, col = branch[sc], bold = TRUE, just = "centre")
      txt(c("Uniform", "Expression")[i], xx[i], bottom + 3.5, 5.8,
          col = branch[sc], just = "centre")
      cat(sprintf("%s (%s): %s / %s: n=5, mean %.8g, range %.8g–%.8g\n",
                  letter, side, model, sc, avg, min(z[[value]]), max(z[[value]])))
    }
  }
  grid.text("oracle RMSE", x = mm(3.3), y = unit(1, "npc") - mm((top + bottom) / 2),
    rot = 90, gp = gpar(fontfamily = "Liberation Sans", fontsize = 6, col = ink))
}
draw_E <- function(offset = 0) draw_error("W", "E", w_metrics, offset)
draw_F <- function(offset = 0) draw_error("H", "F", metrics, offset)
render <- function(path, height, draw, width = 134) {
  png(path, width = width, height = height, units = "mm", res = 600,
      type = "cairo", bg = "white", pointsize = 6)
  grid.newpage()
  draw()
  dev.off()
  cat("Wrote", path, width, "x", height, "mm, 600 dpi\n")
}
inset_error <- function(draw, top) {
  pushViewport(viewport(x = mm(17), y = unit(1, "npc") - mm(top),
    width = mm(100), height = mm(54), just = c("left", "top")))
  draw()
  popViewport()
}
render_master <- function(svg, preview, draw, width, height) {
  if (file.exists(svg)) {
    system2("inkscape", c(svg, "--export-type=png", "--export-dpi=600", "-o", preview))
  } else {
    render(preview, height, draw, width = width)
  }
}
render_master(file.path(d_dir, "fig1D.svg"), file.path(d_dir, "fig1D.png"), draw_D, 119, 107)
render_master(file.path(sample_dir, "sample_simplices.svg"), file.path(sample_dir, "sample_simplices.png"),
              function() draw_D(sample_side = TRUE), 119, 107)
# All SVGs become masters once created. Refresh PNGs from the masters.
for (letter in c("E", "F")) {
  directory <- if (letter == "E") e_dir else f_dir
  svg <- file.path(directory, paste0("fig1", letter, ".svg"))
  preview <- file.path(directory, paste0("fig1", letter, ".png"))
  render_master(svg, preview, if (letter == "E") draw_E else draw_F, 100, 54)
}
render("figure/fig1/fig1EF_mock.png", 110, function() { draw_E(); draw_F(56) }, width = 100)
render("figure/fig1/fig1DE_mock.png", 163, function() { draw_D(); inset_error(draw_E, 109) })
render("figure/fig1/fig1DEF_mock.png", 219, function() {
  draw_D(); inset_error(draw_E, 109); inset_error(draw_F, 165)
})

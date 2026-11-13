# Presentation and SVG export only. Analysis stays in figure1_components.Rmd.
export_plot <- function(p, name, width_mm, height_mm, data) {
  panel <- dirname(name)
  stem <- basename(name)
  folder <- file.path("figure/fig1", panel, "generated")
  dir.create(folder, recursive = TRUE, showWarnings = FALSE)
  inputs[[panel]][[stem]] <<- data
  p <- p + theme(
    text = element_text(family = "Liberation Sans", size = 5.5),
    plot.title = element_text(size = 6, face = "plain", margin = margin(b = 2)),
    axis.title = element_text(size = 5.5), axis.text = element_text(size = 5),
    strip.text = element_text(size = 5, margin = margin(1, 1, 1, 1)),
    legend.text = element_text(size = 5), legend.title = element_text(size = 5),
    legend.key.size = grid::unit(2, "mm"),
    legend.key.spacing = grid::unit(0.3, "mm"),
    legend.spacing = grid::unit(0.5, "mm"),
    legend.box.spacing = grid::unit(0.5, "mm"),
    legend.margin = margin(0, 0, 0, 0),
    panel.spacing = grid::unit(0.6, "mm"),
    axis.ticks.length = grid::unit(0.6, "mm"),
    axis.line = element_line(linewidth = 0.15),
    axis.ticks = element_line(linewidth = 0.15),
    strip.background = element_rect(linewidth = 0.15),
    plot.margin = margin(1, 1, 1, 1)
  )
  for (i in seq_along(p$layers)) {
    if (panel != "panelB" && !is.null(p$layers[[i]]$aes_params$size))
      p$layers[[i]]$aes_params$size <- p$layers[[i]]$aes_params$size / 3
    if (!is.null(p$layers[[i]]$aes_params$linewidth))
      p$layers[[i]]$aes_params$linewidth <- 0.15
  }
  if (panel == "panelB") p <- p + theme(axis.title = element_blank(),
    axis.text = element_blank(), axis.ticks = element_blank(),
    plot.title = element_text(size = 5.5, hjust = 0.5))
  if (panel %in% c("panelC", "panelF", "panelG") && stem != "spectrum" && stem != "snr-ratio")
    p <- p + theme(axis.text.x = element_text(angle = 60, hjust = 1))
  if (name == "panelD/bins") p <- p + theme(axis.text.x = element_text(angle = 90, hjust = 1))
  if (name == "panelE/total") p <- p + theme(axis.text.x = element_text(angle = 60, hjust = 1))
  if (name == "panelE/snr") p <- p + theme(axis.text.x = element_text(angle = 60, hjust = 1))
  if (panel %in% c("panelC", "panelG") || name == "panelF/ratio")
    p$facet$params$labeller <- labeller(NOISE = c(none = "0", Normal = "Normal",
      Poisson = "Poisson", Mul = "Mul", NB = "NB"))
  # Short labels keep the original quantities and leave room for 5 pt tick text.
  if (panel %in% c("panelC", "panelG")) p <- p + labs(y = "RMSE")
  if (panel == "panelC") p <- p + labs(title = paste(sub("rmse-", "", stem), "deconvolution"))
  if (stem %in% c("projection-W", "projection-H"))
    p <- p + labs(title = paste(sub("projection-", "", stem), "projection"))
  if (name == "panelG/fraction") p <- p + labs(y = "Projection / deconvolution RMSE")
  if (name == "panelF/spectrum") p <- p + labs(title = "Rank 3; noise level 0.25", y = "Normalized singular value")
  if (name == "panelF/ratio") p <- p + labs(title = NULL, y = "σ(k+1) / σ(k)")
  if (name == "panelF/snr-ratio") p <- p + labs(title = NULL, y = "σ(k+1) / σ(k)", x = "Post-scaling SNR")
  if (name == "panelE/snr") p <- p + labs(title = NULL, y = "Post-scaling SNR")
  # Shrink the original scatter legend's oversized example symbols.
  if (name == "panelF/snr-ratio") {
    p <- p + guides(
      shape = guide_legend(override.aes = list(color = base_noise_colors, size = 1)),
      fill = guide_legend(order = 2, override.aes = list(shape = 22, size = 1.5, color = NA))
    )
  }
  ggsave(file.path(folder, paste0(stem, ".svg")), p, device = svglite::svglite,
    width = width_mm, height = height_mm, units = "mm", bg = "white")
  cat(name, ":", width_mm, "x", height_mm, "mm\n")
  invisible(p)
}

write_provenance <- function() {
  commit <- system2("git", c("-C", "../general_dual_simplex", "rev-parse", "HEAD"), stdout = TRUE)
  dirty <- system2("git", c("-C", "../general_dual_simplex", "status", "--porcelain", "R", "src"), stdout = TRUE)
  note <- c(paste("Package commit:", commit),
    paste("Installed version:", as.character(packageVersion("GeneralDualSimplex"))),
    "git status --porcelain R src:", dirty,
    "Input: data/figure1/k3_simulation_balanced-population.rds (supplied archive; generating commit unknown)",
    "Generator: figure/fig1/figure1_components.Rmd")
  for (panel in names(inputs)) writeLines(note, file.path("figure/fig1", panel,
    if (panel == "panelB") "results_package_commit.txt" else "package_commit.txt"))
}

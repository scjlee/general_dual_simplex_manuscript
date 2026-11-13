# File export and provenance only. All plot styling and labels live in the Rmd.
export_plot <- function(p, name, width_mm, height_mm, data) {
  panel <- dirname(name)
  stem <- basename(name)
  folder <- file.path("figure/fig1", panel, "generated")
  dir.create(folder, recursive = TRUE, showWarnings = FALSE)
  inputs[[panel]][[stem]] <<- data
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

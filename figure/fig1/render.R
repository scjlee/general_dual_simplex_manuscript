# Run from the manuscript repository root, in its renv.
figure_dir <- normalizePath("figure/fig1")
rmarkdown::render(
  file.path(figure_dir, "figure1_components.Rmd"),
  output_dir = figure_dir,
  intermediates_dir = file.path(figure_dir, "render"),
  output_options = list(pandoc_args = c("--resource-path", figure_dir)),
  knit_root_dir = getwd(), envir = new.env(), clean = FALSE
)

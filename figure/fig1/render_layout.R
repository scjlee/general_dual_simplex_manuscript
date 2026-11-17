# Render only E-left and the new h layout from saved plotted inputs.
# Run from the repository root; no simulations or provenance files are changed.
lines <- readLines("figure/fig1/figure1_components.Rmd")
run_chunk <- function(name) {
  start <- match(paste0("```{r ", name, "}"), lines)
  end <- start + which(lines[(start + 1):length(lines)] == "```")[1]
  eval(parse(text = lines[(start + 1):(end - 1)]), envir = .GlobalEnv)
}
run_chunk("setup")
plot_dt_long <- readRDS("figure/fig1/panelE/input_data.rds")[["by-bin"]]
run_chunk("E-by-bin")
plot_data_wide <- readRDS("figure/fig1/panelG/input_data.rds")[["fraction"]]
run_chunk("H-side-by-side")

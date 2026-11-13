library(data.table)
library(GeneralDualSimplex)
library(ggplot2)
library(ggtext)
library(ggrastr)
library(ggh4x)
library(magrittr)
f <- glue::glue
pmap <- purrr::pmap
knitr::opts_chunk$set(dev = "svglite", fig.ext = "svg",
  fig.path = "figure/fig1/render/", echo = FALSE, message = FALSE,
  warning = TRUE, cache = FALSE, fig.show = "hide")
theme_set(theme_classic(base_family = "Liberation Sans", base_size = 5.5) + theme(
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
  ))
# Subscript spans set their own 5 pt size; F ratio axis titles are 6.5 pt.
update_geom_defaults("point", list(size = 0.35, stroke = 0.15))
update_geom_defaults("line", list(linewidth = 0.15))
update_geom_defaults("polygon", list(linewidth = 0.15))
update_geom_defaults("boxplot", list(linewidth = 0.15, size = 0.3))
# Labels for the narrow noiseless facet in the error and ratio plots.
noise_strip_labels <- c(none = "0", Normal = "Normal", Poisson = "Poisson",
  Mul = "Mul", NB = "NB")
inputs <- list()
source("figure/fig1/simulation_helpers.R", local = TRUE)
source("figure/fig1/export_helpers.R", local = TRUE)
base_noise_colors <- c(
  "Normal" = "#CC79A7", 
  "Poisson" = "#D55E00", 
  "Mul" = "#0072B2", 
  "NB" = "#009E73"
)
plot_dt <- readRDS("figure/fig1/panelF/input_data.rds")$spectrum
K <- 3L
expanded_color <- c("none" = "black", base_noise_colors)
  
p <- ggplot(
  plot_dt[component %in% as.character(2:10) & NOISE_LEVEL %in% c("0", "1/4")],
  mapping = aes(
    x = component,
    y = normalized_spectral,
    color = NOISE,
    fill = NOISE,
    group = NOISE
  )
) +
  geom_vline(xintercept = f("{K}"), linetype = "dashed", color = "gray50") +
  stat_summary(
    geom = "ribbon",
    fun.min = min,
    fun.max = max,
    alpha = 0.25,
    color = NA
  ) +
  scale_fill_manual(values = expanded_color) +
  stat_summary(
    geom = "point",
    fun = mean,
    size = 2 / 3
  ) +
  stat_summary(
    geom = "line",
    fun = mean,
    linewidth = 0.15
  ) +
  scale_color_manual(values = expanded_color) +
  labs(
    title = "Rank 3; noise level 0.25",
    x = "k",
    y = "Normalized singular value",
    color = "Noise",
    fill = "Noise"
  ) +
  theme(
    legend.position = "bottom"
  )
export_plot(p, "panelF/spectrum", 52, 39, plot_dt)

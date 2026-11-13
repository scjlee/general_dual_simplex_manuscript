## ----setup--------------------------------------------------------------------
library(data.table)
library(GeneralDualSimplex)
library(ggplot2)
library(ggh4x)
library(magrittr)
f <- glue::glue
pmap <- purrr::pmap
source("figure/fig1/simulation_helpers.R")
source("figure/fig1/export_helpers.R")
knitr::opts_chunk$set(dev = "svglite", fig.ext = "svg",
  fig.path = "figure/fig1/render/", echo = FALSE, message = FALSE,
  warning = TRUE, cache = FALSE, fig.show = "hide")
theme_set(theme_classic(base_family = "Liberation Sans", base_size = 5.5))
update_geom_defaults("point", list(size = 0.35, stroke = 0.15))
update_geom_defaults("line", list(linewidth = 0.15))
update_geom_defaults("polygon", list(linewidth = 0.15))
update_geom_defaults("boxplot", list(linewidth = 0.15, size = 0.3))
inputs <- list()


## ----gradient-----------------------------------------------------------------
make_gradient <- function(color, n = 4, darken.by = 0.2, lighten.by = 0.8) {
  colorRampPalette(c(
    colorspace::darken(color, amount = darken.by),
    colorspace::lighten(color, amount = lighten.by)
  ))(n)
}


## ----load---------------------------------------------------------------------
K <- 3L

experiments <- read_simulation_rds(f("data/figure1/k{K}_simulation_balanced-population.rds"))
experiments[["NOISE"]] %<>% factor(levels = c("none", "Normal", "Poisson", "Mul", "NB"))


## ----noise-levels-------------------------------------------------------------
all_noise_levels <- unique(experiments$NOISE_LEVEL)

experiments <- experiments[NOISE_LEVEL != "1/3"]
experiments[["NOISE_LEVEL"]] %<>%
  as.character() %>%
  factor(levels = all_noise_levels[all_noise_levels != "1/3"])


## ----representative-settings--------------------------------------------------
EXAMPLE_L <- "1/2"
EXAMPLE_SEED <- 17

show_names <- list(
  "none" = "Noiseless",
  "Normal" = "Normal",
  "Poisson" = "Poisson",
  "Mul" = "Multiplicative",
  "NB" = "Neg. Binom."
)


## ----B-features---------------------------------------------------------------
for (noise in unique(experiments$NOISE)) {
  fvertex <- experiments[
    NOISE == noise
    & NOISE_LEVEL %in% c("0", EXAMPLE_L)
    & SEED == EXAMPLE_SEED,
    result
  ][[1]] %>%
    slot("misc") %>%
    getElement("true_vertices") %>%
    getElement("X") %>%
    as.data.table(keep.rownames = T)
  
  
  fdata <- experiments[
    NOISE == noise
    & NOISE_LEVEL %in% c("0", EXAMPLE_L)
    & SEED == EXAMPLE_SEED,
    result
  ][[1]] %>%
    slot("reduction") %>%
    getElement("gsvd") %>%
    slot("features") %>%
    as.data.table(keep.rownames = T)
  
  p <- ggplot(mapping = aes(x = dim2, y = dim3)) +
    geom_polygon(
      data = fvertex,
      fill = "#E69F00",
      alpha = 0.25,
      color = "black",
      linetype = "dashed"
    ) +
    geom_point(
      data = fdata,
      color = "gray50",
      size = 0.08
    ) +
    labs(title = show_names[[noise]]) +
    theme(
      plot.title = element_text(hjust = 0.5, size = 20),
      axis.title = element_blank(),
      axis.ticks = element_blank(),
      axis.text = element_blank()
    )
  
  export_plot(p, paste0("panelB/feature-", noise), 16.4, 18, list(vertices = fvertex, points = fdata))
}


## ----evaluation-data----------------------------------------------------------
evaluations <- pmap(experiments, function(..., result) {
  c(
    list(...),
    as.data.table(result@misc$evaluation, keep.rownames = T)
  )}) %>%
  rbindlist()

evaluations[["SEED"]] %<>% factor()
evaluations[["NOISE"]] %<>% factor(levels = c("none", "Normal", "Poisson", "Mul", "NB"))


## ----noise-models-------------------------------------------------------------
noise_model_to_plot <- c("none", "Normal", "Poisson", "Mul", "NB")


## ----C-W----------------------------------------------------------------------
which.side <- "W"
p <- ggplot(
  evaluations[NOISE %in% noise_model_to_plot & metric == "rmse" & side == which.side],
  mapping = aes(
    x = NOISE_LEVEL,
    y = value
  )
) +
  geom_boxplot(outliers = F) +
  geom_point() +  #aes(color = SEED)) +
  facet_grid(
    cols = vars(NOISE),
    space = "free",
    scales = "free_x"
  ) +
  guides(color = "none") +
  labs(
    title = f("Deconvolusion error of {which.side}"),
    x = "Noise level",
    y = "RMSE (lower is better)"
  ) +
  theme(
    legend.position = "bottom",
    axis.text.x = element_text(angle = 45, hjust = 1)
  )
export_plot(p, "panelC/rmse-W", 43, 37, evaluations[metric == "rmse" & side == which.side])


## ----C-H----------------------------------------------------------------------
which.side <- "H"
p <- ggplot(
  evaluations[NOISE %in% noise_model_to_plot & metric == "rmse" & side == which.side],
  mapping = aes(
    x = NOISE_LEVEL,
    y = value
  )
) +
  geom_boxplot(outliers = F) +
  geom_point() +  #aes(color = SEED)) +
  facet_grid(
    cols = vars(NOISE),
    space = "free",
    scales = "free_x"
  ) +
  guides(color = "none") +
  labs(
    title = f("Deconvolusion error of {which.side}"),
    x = "Noise level",
    y = "RMSE (lower is better)"
  ) +
  theme(
    legend.position = "bottom",
    axis.text.x = element_text(angle = 45, hjust = 1)
  )
export_plot(p, "panelC/rmse-H", 43, 37, evaluations[metric == "rmse" & side == which.side])


## ----feature-data-------------------------------------------------------------
fdata <- pmap(experiments, function(..., result) {
  c(
    list(...),
    as.data.table(result@metadata$row, keep.rownames = T)
  )}) %>%
  rbindlist()

fdata[["SEED"]] %<>% factor()
fdata[["type"]] %<>% factor(levels = c("marker", "background"))
fdata[["NOISE"]] %<>% factor(levels = c("none", "Normal", "Poisson", "Mul", "NB"))

fdata[, `:=`(
  mass_sum = sum(total),
  sacling_sum = sum(scaling),
  scaled_mass_sum = sum(scaled_total),
  var_sum = sum(var),
  scaled_var_sum = sum(scaled_var)

), by = c("SEED", "NOISE", "NOISE_LEVEL")]

fdata[, `:=`(
  var_share = 100 * var / var_sum,
  scaled_var_share = 100 * scaled_var / scaled_var_sum,
  
  signal_var_share = 100 * signal_var / var_sum,
  noise_var_share = 100 * noise_var / var_sum,
  cov_share = 100 * 2 * cov / var_sum,

  scaled_signal_var_share = 100 * scaled_signal_var / scaled_var_sum,
  scaled_noise_var_share = 100 * scaled_noise_var / scaled_var_sum,
  scaled_cov_share = 100 * 2 * scaled_cov / scaled_var_sum

)]

fdata[, `:=`(
  var_share_ratio = scaled_var_share / var_share,
  bin = factor(dplyr::ntile(rank, 5))
)]

n_seed <- length(unique(experiments$SEED))


## ----rank-data----------------------------------------------------------------
plot_dt_long <- fdata[
  NOISE_LEVEL %in%  c("0", "1/4"),
  .(NOISE, rank, bin, var_share, scaled_var_share)
] %>%
  melt(
    id.vars = c("NOISE", "rank", "bin"),
    variable.name = "scaling",
    value.name = "var_share"
  )

setattr(plot_dt_long[["scaling"]], "levels", c("Before", "After"))


## ----D-rank-------------------------------------------------------------------
p <- ggplot(
  plot_dt_long,
  mapping = aes(
    x = rank,
    y = var_share,
    color = scaling,
    fill = scaling
  )
) +
  stat_summary(
    geom = "ribbon",
    fun.min = min,
    fun.max = max,
    alpha = 0.25,
    color = NA
  ) +
  scale_fill_manual(values = c("Before" = "#009E73", "After" = '#D55E00')) +
  stat_summary(
    geom = "point",
    fun = mean,
    size = 0.1
  ) +
  scale_color_manual(values = c("Before" = "#009E73", "After" = '#D55E00')) +
  facet_grid(cols = vars(NOISE)) +
  scale_y_continuous(expand = expansion(mult = c(0.01, 0))) +
  coord_cartesian(
    ylim = c(0, plot_dt_long[NOISE == "none", quantile(var_share, probs = 0.999)]),
    expand = FALSE
  ) +
  labs(
    x = "Raw expression rank (high -> low)",
    y = "Variance share (%)",
    color = "Scaling",
    fill = "Scaling"
  ) +
  theme(
    axis.ticks.x = element_blank(),
    axis.text.x = element_blank(),
    legend.position = "bottom"
  )
export_plot(p, "panelD/rank", 47, 37, plot_dt_long)


## ----D-bin--------------------------------------------------------------------
before_pal <- colorRampPalette(c(
  colorspace::darken("#009E73", amount = 0.2),
  colorspace::lighten("#009E73", amount = 0.8)
))(5)
after_pal  <- colorRampPalette(c(
  colorspace::darken("#D55E00", amount = 0.2),
  colorspace::lighten("#D55E00", amount = 0.75)
))(5)


bin_labels <- c(
  "1 (high)",
  "2",
  "3",
  "4",
  "5 (low)"
)

plot_data <- plot_dt_long[, .(var_share = sum(var_share) / n_seed), by = .(NOISE, scaling, bin)]


p <- ggplot(
  mapping = aes(
    x = NOISE,
    y = var_share,
    fill = bin,
    group = bin
  )
) +
  geom_col(
    data = plot_data[scaling == "Before"],
    aes(
      x = NOISE,
      y = var_share,
      fill = bin
    )
  ) +
  scale_fill_manual(
    name = "Expr. bin",
    values = setNames(before_pal, as.character(1:5)),
    breaks = as.character(1:5),
    labels = bin_labels
  ) +
  ggnewscale::new_scale_fill() +
  
  geom_col(
    data = plot_data[scaling == "After"],
    aes(
      x = NOISE,
      y = var_share,
      fill = bin
    )
  ) +
  scale_fill_manual(
    name = NULL,
    values = setNames(after_pal, as.character(1:5)),
    breaks = as.character(1:5),
    labels = bin_labels
  ) +
  labs(
    x = "Noise",
    y = "Mean variance share (%)",
    fill = "Expr. bin"
  ) +
  facet_grid(cols = vars(scaling)) +
  theme(
    axis.text.x = element_text(angle = 45, hjust = 1)
  )
export_plot(p, "panelD/bins", 34, 37, plot_data)


## ----signal-noise-data--------------------------------------------------------
plot_dt_long <- fdata[
  NOISE_LEVEL == "1/4",
  .(NOISE, SEED, bin, signal_var_share, noise_var_share, scaled_signal_var_share, scaled_noise_var_share)
] %>%
  melt(
    id.vars = c("NOISE", "SEED", "bin"),
    measure.vars = measure(
      scaling = factor,
      type = factor,
      pattern = "^(scaled_)?(signal|noise)_var_share$"
    ),
    value.name = "var_share"
  )

setattr(plot_dt_long[["scaling"]], "levels", c("Before", "After"))
setattr(plot_dt_long[["type"]], "levels", c("Noise", "Signal"))


## ----E-by-bin-----------------------------------------------------------------
p <- ggplot(
  plot_dt_long[NOISE != "none", .(var_share = sum(var_share)), by = .(NOISE, scaling, bin, type, SEED)],
  mapping = aes(
    x = bin,
    y = var_share,
    fill = type
  )
) +
  stat_summary(
    fun = mean,
    geom = "col",
    position = position_dodge(width = 0.8),
    width = 0.7,
    alpha = 0.8
  ) +
  scale_fill_manual(values = c("Signal" = "#0072B2", "Noise" = '#CC79A7')) +
  geom_point(
    position = position_jitterdodge(
      jitter.width = 0.15,
      jitter.height = 0,
      dodge.width = 0.8,
      seed = 1
    ),
    color = "black",
    size = 0.8,
    alpha = 0.6,
    show.legend = FALSE
  ) +
  facet_nested(cols = vars(NOISE, scaling))+
  scale_y_continuous(expand = expansion(mult = c(0.01, 0.01))) +
  labs(
    x = "Raw expression bin (high -> low)",
    y = "Variance share (%)",
    fill = "Source"
  ) +
  theme(
    axis.ticks.x = element_blank(),
    axis.text.x = element_blank(),
    legend.position = "bottom"
  )
export_plot(p, "panelE/by-bin", 77, 40, plot_dt_long)


## ----E-total------------------------------------------------------------------
p <- ggplot(
  plot_dt_long[NOISE != "none", .(var_share = sum(var_share) / n_seed), by = .(NOISE, scaling, type)],
  mapping = aes(
    x = NOISE,
    y = var_share,
    fill = type,
    group = type
  )
) +
  stat_summary(
    fun = sum,
    geom = "col",
    position = "stack"
  ) +
  scale_fill_manual(values = c("Signal" = "#0072B2", "Noise" = '#CC79A7')) +
  labs(
    x = "Noise",
    y = "Mean variance share (%)",
    fill = "Source"
  ) +
  facet_grid(cols = vars(scaling)) +
  theme(
    axis.text.x = element_text(angle = 45, hjust = 1)
  )
export_plot(p, "panelE/total", 43, 40, plot_dt_long)


## ----E-SNR--------------------------------------------------------------------
aggr_fdata <- fdata[
  ,
  .(
    total_signal_share = sum(scaled_signal_var_share),
    total_noise_share = sum(scaled_noise_var_share)
  ),
  by = .(NOISE, NOISE_LEVEL, SEED)
]

aggr_fdata[, snr := total_signal_share / total_noise_share]


p <- ggplot(
  aggr_fdata[NOISE != "none"],
  mapping = aes(
    x = NOISE_LEVEL,
    y = snr
  )
) +
  geom_boxplot(outlier.shape = NA) +
  geom_point(
    show.legend = FALSE
  ) +
  facet_grid(cols = vars(NOISE)) +
  labs(
    title = "Signal-to-noise ratio",
    x = "Noise level",
    y = "SNR (higher is better)"
  )
export_plot(p, "panelE/snr", 50, 40, aggr_fdata)


## ----spectral-data------------------------------------------------------------
base_noise_colors <- c(
  "Normal" = "#CC79A7", 
  "Poisson" = "#D55E00", 
  "Mul" = "#0072B2", 
  "NB" = "#009E73"
)


plot_dt <- experiments %>%
  pmap(function(..., result) {
    inertia <- result %>%
      GetData("biwhitened") %>%
      Matrix::norm(type = "F") %>%
      `^`(2) %>%
      `-`(1)
    
    spectral <- result@misc$spectral
    spectral_gap <- spectral[K] - spectral[K+1]

    c(
      list(...),
      data.table(
        component = names(spectral),
        spectral = spectral,
        normalized_spectral = spectral / inertia,
        spectral_gap = spectral_gap,
        normalized_spectral_gap = spectral_gap / inertia
      )
    )}) %>%
    rbindlist()

plot_dt[["component"]] %<>% 
  gsub("^dim", "", .) %>%
  factor(levels = as.character(1:30))


## ----F-spectrum---------------------------------------------------------------
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
    size = 2
  ) +
  stat_summary(
    geom = "line",
    fun = mean,
    linewidth = 1
  ) +
  scale_color_manual(values = expanded_color) +
  labs(
    title = "Rank-3 signal (noise level = 0.25)",
    x = "k",
    y = bquote(~ "Normalize singular value" ~ σ[k]),
    color = "Noise",
    fill = "Noise"
  ) +
  theme(
    legend.position = "bottom"
  )
export_plot(p, "panelF/spectrum", 52, 39, plot_dt)


## ----F-ratio------------------------------------------------------------------
p <- ggplot(
  evaluations[metric ==  "singular_value_ratio"],
  mapping = aes(
    x = NOISE_LEVEL,
    y = value
  )
) +
  geom_boxplot(outlier.shape = NA) +
  geom_point() +  # aes(color = factor(SEED))) +
  facet_grid(cols = vars(NOISE), space = "free", scales = "free_x") + # Locked y-axis across Normal, Mul, NB
  guides(color = "none") +
  labs(
    title = "Normalized singular value ratio",
    x = "Noise level",
    y = bquote(σ[k+1] / σ[k] ~ "(lower is better)")
  ) +
  theme(
    axis.text.x = element_text(angle = 45, hjust = 1)
  )
export_plot(p, "panelF/ratio", 65, 39, evaluations[metric == "singular_value_ratio"])


## ----F-SNR-ratio--------------------------------------------------------------
EXAMPLE_Ls <- c("2","1", "1/2", "1/4")

color_vals <- base_noise_colors %>%
  sapply(make_gradient, n = length(EXAMPLE_Ls), lighten.by = 0.5) %>%
  as.vector() %>%
  setNames(
    nm  = paste0(
      rep(names(base_noise_colors), each = length(EXAMPLE_Ls)),
      ".",
      rep(EXAMPLE_Ls, length(base_noise_colors))
    )
  )


set.seed(1993)
p <- merge(
  aggr_fdata,
  evaluations[metric == "singular_value_ratio", .(NOISE, NOISE_LEVEL, SEED, singular_value_ratio = value)],
  by = c('NOISE', 'NOISE_LEVEL', 'SEED')
) %>%
  `[`(NOISE != "none") %>%
  `[`(sample(.N)) %>%
  ggplot(aes(x = snr, y = singular_value_ratio)) +
  geom_point(
    aes(
      color = interaction(NOISE, NOISE_LEVEL),
      shape = NOISE,
      fill  = NOISE_LEVEL
    )
  ) +
  scale_color_manual(
    values = color_vals,
    guide = "none"
  ) +
  scale_shape_manual(
    values = c("Normal" = 16, "Poisson" = 17, "Mul" = 15, "NB" = 3),
    guide = guide_legend(
      override.aes = list(color = base_noise_colors, size = 3)
    )
  ) +
  scale_fill_grey(
    name  = "Noise level",
    start = 0.85,
    end   = 0.2,
    guide = guide_legend(
      order = 2,
      override.aes = list(
        shape = 22, # Filled square icon
        size  = 6,
        color = NA 
      )
    )
  ) +
  labs(
    title = "SNR vs σ ratio",
    x = "SNR",
    y = bquote(σ[k+1] / σ[k] ~ "(lower is better)")
  ) +
  theme(
    legend.position = "right",
    legend.box = "vertical"
  )
export_plot(p, "panelF/snr-ratio", 53, 39, list(snr = aggr_fdata, evaluations = evaluations[metric == "singular_value_ratio"]))


## ----G-W----------------------------------------------------------------------
which.side <- "W"
p <- ggplot(
      evaluations[metric == "oracle_rmse" & side == which.side],
      mapping = aes(
        x = NOISE_LEVEL,
        y = value
      )
    ) +
      geom_boxplot(outlier.shape = NA) +
      geom_point() +  # aes(color = factor(SEED))) +
      facet_grid(cols = vars(NOISE), space = "free", scales = "free_x") +
      guides(color = "none") +
      labs(
        title =  f("{which.side}-side projection error"),
        x = "Noise level",
        y = "RMSE (lower is better)"
      ) +
      theme(
        axis.text.x = element_text(angle = 45, hjust = 1)
      )
export_plot(p, "panelG/projection-W", 54, 36, evaluations[metric == "oracle_rmse" & side == which.side])


## ----G-H----------------------------------------------------------------------
which.side <- "H"
p <- ggplot(
      evaluations[metric == "oracle_rmse" & side == which.side],
      mapping = aes(
        x = NOISE_LEVEL,
        y = value
      )
    ) +
      geom_boxplot(outlier.shape = NA) +
      geom_point() +  # aes(color = factor(SEED))) +
      facet_grid(cols = vars(NOISE), space = "free", scales = "free_x") +
      guides(color = "none") +
      labs(
        title =  f("{which.side}-side projection error"),
        x = "Noise level",
        y = "RMSE (lower is better)"
      ) +
      theme(
        axis.text.x = element_text(angle = 45, hjust = 1)
      )
export_plot(p, "panelG/projection-H", 54, 36, evaluations[metric == "oracle_rmse" & side == which.side])


## ----projection-ratios-data---------------------------------------------------
plot_data_wide <- c("W", "H") %>%
  lapply(function(which.side) {
    plot_data <- evaluations[
      NOISE != "none"
      & (side == which.side | is.na(side))
      & metric %in% c(
        "singular_value_ratio",
        "oracle_rmse", "rmse",
        "oracle_one_minus_r2", "one_minus_r2"
      ),
      .(NOISE, NOISE_LEVEL, SEED, side, metric, value)
    ]
    
    plot_data_wide <- dcast(
      plot_data,
      NOISE + NOISE_LEVEL + SEED + rowid(metric) ~ metric,
      value.var = "value"
    )[, metric := NULL]
    
    plot_data_wide[["side"]] <- which.side
    
    plot_data_wide
  }) %>%
  rbindlist()

plot_data_wide[["side"]] %<>% factor(levels = c("W", "H"))


## ----projection-ratios--------------------------------------------------------
plot_data_wide[, `:=`(
  oracle_rmse_pct = (oracle_rmse / rmse)
)]


## ----G-ratio------------------------------------------------------------------
p <- ggplot(
  plot_data_wide,
  mapping = aes(
    x = NOISE_LEVEL,
    y = oracle_rmse_pct
  )
) +
  geom_boxplot(outlier.shape = NA) +
  geom_point(
    size = 0.75
  ) +
  facet_grid(
    rows = vars(side),
    cols = vars(NOISE),
    space = "free",
    scales = "free"
  ) +
  guides(color = "none") +
  labs(
    x = "Noise level",
    y = "RMSE ratio (projection / deconvolution)"
  ) +
  theme(
    axis.text.x = element_text(angle = 45, hjust = 1)
  )
export_plot(p, "panelG/fraction", 62, 36, plot_data_wide)


## ----save-inputs--------------------------------------------------------------
for (panel in names(inputs)) saveRDS(inputs[[panel]], file.path("figure/fig1", panel, "input_data.rds"))
write_provenance()
cat("Retained simulations:", nrow(experiments), "\n")
cat("Seeds:", n_seed, "\n")
cat("Representative simplex: seed", EXAMPLE_SEED, "noise level", EXAMPLE_L, "\n")
cat("D and E selected noise level: 1/4; noiseless baseline retained in D.\n")


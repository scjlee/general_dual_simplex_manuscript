---
title: "Figure 1 — selected panels and SVG export"
output:
  html_document:
    self_contained: true
---

This working copy renders the panels shown in the supplied outline and an optional
log-SNR plot that is excluded from assembly. Run from
this repository root with `Rscript figure/fig1/render.R`. Generated panel SVGs
are in each panel's `generated/` directory. Edit the assembled `figure1.svg`;
re-rendering replaces its named data groups, preserving the surrounding layout.



``` r
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
```



# Load the supplied simulations





# B — feature simplices only




```
## panelB/feature-none : 17.9 x 21.5 mm
```

```
## panelB/feature-Poisson : 17.9 x 21.5 mm
```

```
## panelB/feature-NB : 17.9 x 21.5 mm
```

```
## panelB/feature-Normal : 17.9 x 21.5 mm
```

```
## panelB/feature-Mul : 17.9 x 21.5 mm
```

# C — deconvolution RMSE






```
## panelC/rmse-W : 43 x 41.5 mm
```


```
## panelC/rmse-H : 43 x 41.5 mm
```

# D — variance share by rank and expression bin


```
## Warning in `[.data.table`(fdata, , `:=`(mass_sum = sum(total), sacling_sum =
## sum(scaling), : A shallow copy of this data.table was taken so that := can add
## or remove 5 columns by reference. At an earlier point, this data.table was
## copied by R (or was created manually using structure() or similar). Avoid
## names<- and attr<- which in R currently (and oddly) may copy the whole
## data.table. Use set* syntax instead to avoid copying: ?set, ?setnames and
## ?setattr. It's also not unusual for data.table-agnostic packages to produce
## tables affected by this issue. If this message doesn't help, please report your
## use case to the data.table issue tracker so the root cause can be fixed or this
## message improved.
```




```
## panelD/rank : 47 x 41.5 mm
```


```
## Warning in min(x): no non-missing arguments to min; returning Inf
```

```
## Warning in max(x): no non-missing arguments to max; returning -Inf
```

```
## Warning in min(x): no non-missing arguments to min; returning Inf
```

```
## Warning in max(x): no non-missing arguments to max; returning -Inf
```

```
## panelD/bins : 34 x 41.5 mm
```

# E — signal/noise variance shares and SNR




```
## panelE/by-bin : 77 x 45 mm
```


```
## panelE/total : 43 x 45 mm
```


```
## panelE/snr : 50 x 45 mm
```

# F — spectral separation




```
## panelF/spectrum : 52 x 44 mm
```


```
## panelF/ratio : 65 x 44 mm
```


```
## panelF/snr-ratio : 53 x 44 mm
```

```
## panelF/log-snr-ratio : 53 x 39 mm
```

# G — projection RMSE and its fraction of deconvolution RMSE


```
## panelG/projection-W : 50 x 40.4 mm
```


```
## panelG/projection-H : 50 x 40.4 mm
```




```
## Warning in `[.data.table`(plot_data_wide, , `:=`(oracle_rmse_pct =
## (oracle_rmse/rmse))): A shallow copy of this data.table was taken so that :=
## can add or remove 1 columns by reference. At an earlier point, this data.table
## was copied by R (or was created manually using structure() or similar). Avoid
## names<- and attr<- which in R currently (and oddly) may copy the whole
## data.table. Use set* syntax instead to avoid copying: ?set, ?setnames and
## ?setattr. It's also not unusual for data.table-agnostic packages to produce
## tables affected by this issue. If this message doesn't help, please report your
## use case to the data.table issue tracker so the root cause can be fixed or this
## message improved.
```


```
## panelG/fraction : 72 x 40.4 mm
```


```
## Retained simulations: 340
```

```
## Seeds: 20
```

```
## Representative simplex: seed 17 noise level 1/2
```

```
## D and E selected noise level: 1/4; noiseless baseline retained in D.
```

# SVG gallery


## Panel B

![B: feature-none](panelB/generated/feature-none.svg)

![B: feature-Normal](panelB/generated/feature-Normal.svg)

![B: feature-Poisson](panelB/generated/feature-Poisson.svg)

![B: feature-Mul](panelB/generated/feature-Mul.svg)

![B: feature-NB](panelB/generated/feature-NB.svg)


## Panel C

![C: rmse-W](panelC/generated/rmse-W.svg)

![C: rmse-H](panelC/generated/rmse-H.svg)


## Panel D

![D: rank](panelD/generated/rank.svg)

![D: bins](panelD/generated/bins.svg)


## Panel E

![E: by-bin](panelE/generated/by-bin.svg)

![E: total](panelE/generated/total.svg)

![E: snr](panelE/generated/snr.svg)


## Panel F

![F: spectrum](panelF/generated/spectrum.svg)

![F: ratio](panelF/generated/ratio.svg)

![F: snr-ratio](panelF/generated/snr-ratio.svg)

### Optional log-SNR plot — not assembled

![F: log-snr-ratio](panelF/generated/log-snr-ratio.svg)


## Panel G

![G: projection-W](panelG/generated/projection-W.svg)

![G: projection-H](panelG/generated/projection-H.svg)

![G: fraction](panelG/generated/fraction.svg)


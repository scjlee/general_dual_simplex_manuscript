# Saved noise sweep: panel C draft

The requested delivery is `fig1C_sweep.png` only. The SVG master and PDF
are internal supporting artifacts for rendering and verification. This is a separate draft; it does
not replace `../panelC/fig1C.svg`.

The plot uses the saved `metadata$row$scaled_var`: sample variance in the
scaled matrix Vtilde. It divides each gene's variance by the sum across
genes and plots percentages. Under uniform scaling, these normalized shares coincide with the old
panel C metric in Z; the definitions can differ for other scalings.
Only uniform scaling is present in the supplied archive.

Colors represent noise parameters. In the negative-binomial panel,
line styles distinguish dispersions. Genes rank by unscaled observed total,
from low to high, independently within each run. The display averages 30
adjacent ranks per seed, then shows mean and min–max across ten seeds.
The range is descriptive, not a confidence interval.

Reproduce from the repository root:

```sh
RENV_CONFIG_SANDBOX_ENABLED=FALSE Rscript figure/fig1/panelC_sweep/extract_shares.R
RENV_CONFIG_SANDBOX_ENABLED=FALSE Rscript figure/fig1/panelC_sweep/summarize.R
python3 figure/fig1/panelC_sweep/make_panel.py
inkscape figure/fig1/panelC_sweep/fig1C_sweep.svg --export-type=png --export-dpi=600 --export-background=white --export-background-opacity=1
inkscape figure/fig1/panelC_sweep/fig1C_sweep.svg --export-type=pdf
```

The first step reads `/data/simulation_runs_k3.rds`; an alternative path
can be supplied as an argument. It extracts saved states without rerunning
simulations or fitting. It checks the stored variances using the matrices
and saved scaling. The large per-gene scratch extraction goes in `out/`.

`variance_by_rank.csv` retains every rank's mean/min/max across seeds.
`variance_by_rank_bins.csv` contains the actual plotted data. `runs.csv`
indexes all source runs and `checks.csv` records numerical verification.
`package_commit.txt` and `source_sha256.txt` record available provenance.
The generating package commit is unavailable in the supplied archive;
the current checkout commit is recorded only as context.

The SVG is the master. Later generator runs replace only the named data
groups. If changing bin size in `summarize.R`, update the subtitle manually.
Axes, labels and legends also need manual edits if their settings change.
Full caption, metric derivation and limitations:
`artifact/20261028_panelC_noise_sweep.md` (from repository root).

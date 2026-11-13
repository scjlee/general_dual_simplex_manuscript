# Regeneration after rasterization

Source Rmd: user commit ce1218e54d983fa0f63ff2c5d52ffc4c741414ac.
Ran Rscript figure/fig1/render.R, then assemble.py, Inkscape PNG/PDF exports and verify.py.
The previous master is backed up at backups/figure1-003.svg.

All saved panel input RDS checksums are unchanged. The master outside the generated plot groups is unchanged, including layout, schematics and annotations.
B and D contain ten inline PNG layers at approximately 1200 dpi; text and other geometry remain vector.
The SVG decreased from 6,501,433 to 2,544,087 bytes; PDF from 2,418,006 to 809,218 bytes.
The PDF has one page; all 385 text boxes pass page and plot bounds checks.
The 600 dpi PNG was opened and inspected.

No new scientific review was requested: these are rendering and point-style changes only; no formulas, claims or plotted numerical data changed. The previous scientific-review notes still apply.

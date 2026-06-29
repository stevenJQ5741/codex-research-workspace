# Data Management and Reproducible Analysis Rules

## Purpose

Rules for handling raw data, processed data, scripts, figures, and reports.

## Raw data

1. Store original files in `data/raw/`.
2. Never overwrite raw data.
3. Never edit original CSV, TXT, Excel, DSC, or measurement files directly.
4. If cleaning is needed, create new files in `data/processed/`.

## Processed data

1. Store processed data in `data/processed/`.
2. Include the script used to generate it.
3. Record filtering, smoothing, trimming, baseline correction, and assumptions.
4. Use clear file names.

## Outputs

Use:

- figures: `outputs/figures/`
- tables: `outputs/tables/`
- reports: `outputs/reports/`
- presentations: `outputs/presentations/`

## Python analysis

Prefer:

- pandas
- numpy
- matplotlib

Rules:

1. Avoid unnecessary dependencies.
2. Use clear relative paths.
3. Avoid hard-coded absolute paths.
4. Save figures and tables systematically.
5. Print key intermediate results when useful.
6. Make scripts rerunnable.
7. Use consistent units.
8. Include error handling when appropriate.

## Experimental analysis report format

Always report:

1. input files
2. preprocessing
3. assumptions
4. calculation method
5. results
6. limitations
7. suggested next steps

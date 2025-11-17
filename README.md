# Customer Data Analysis (automata)

A small analysis project for investigating billing discrepancies from workflow/run data.

This repository contains data loading, processing, scenario analyses, and visualization helpers used to answer the technical task in `data-analyst-technical-task-data.xlsx`.

## Quick summary

- Purpose: identify and visualize billing issues (e.g. unexpected sample types billed in LIVE workflows) and support a reconciliation between customer expectations and invoice data.
- Data: the project expects `data-analyst-technical-task-data.xlsx` at the repository root (already included).
- Primary code: the `src/` package contains data processing (`src/data_processing`), plotting helpers (`src/visualizations`), and small utilities (`src/utils`).

## Requirements

- Python 3.12+
- See `pyproject.toml` for the pinned dependencies. Key runtime deps:
	- pandas
	- openpyxl
	- matplotlib
	- seaborn
	- plotly

If you use Poetry (recommended):

```bash
poetry install
poetry shell
```

Note: the project was developed against Python >= 3.12 as declared in `pyproject.toml`.

## Project layout

- `data-analyst-technical-task-data.xlsx` — source dataset with sheets: `QC Checks`, `Workflows`, `Runs`.
- `notebooks/` — exploratory and reproducible notebooks (recommended starting point: `main.ipynb`).
- `src/` — Python package containing main logic:
	- `src/data_processing/data_loader.py` — load/clean/merge functions and canonical billable/usage filters (functions: `data_load_clean()`, `final_merge()`, `get_billable_data()`, `get_usage_live_data()`).
	- `src/data_processing/billable_samples.py` — billing-specific filtering and sensitivity analysis helpers (e.g. `get_checks_live_finished()`, `analyze_qc_sensitivity()`).
	- `src/data_processing/scenario1_deep_analysis.py` — deeper scenario investigations (e.g. `investigate_bone_marrow_in_live`).
	- `src/visualizations/` — ready-to-run plotting helpers for Scenario analyses (e.g. `visual1_billing_dispute()`, `visual2_monthly_trend()`, ...).
	- `src/utils/config.py` — plotting and pandas display configuration (colors, styles).

## Notes on billing logic

The repository enforces a conservative, canonical definition of a "billable" sample in several places:

1. Environment must be `live` (production).
2. Run `OUTCOME` must be `finished`.
3. `QC_CHECK` must equal `pass` (missing QC is excluded by the conservative definition).

Some analyses in `billable_samples.py` include sensitivity checks that compare the conservative rule against looser definitions (e.g., including missing QC). See `analyze_qc_sensitivity()` for details.

## Notebooks

- `main.ipynb` — top-level walkthrough and quick visuals.
- `scenario1_billing_reconciliation.ipynb` — focused scenario 1 analysis and visuals.
- `data_checks.ipynb` — quick data validation and exploratory tables.

Open them in order to reproduce the report.

## Where to start

1. Ensure dependencies are installed (see Requirements).
2. Open `notebooks/main.ipynb` and run the first cells to load and inspect data.
3. Use `src/data_processing/data_loader.py` to programmatically load and filter data when writing scripts.

## Troubleshooting

- Missing `data-analyst-technical-task-data.xlsx`: place the file in the repo root.
- Pandas datetime conversion errors: ensure the Excel sheets have the expected column names (`TIMESTAMP`, `WORKFLOW_TIMESTAMP`, `START_TIME`, `STOP_TIME`).
- If a function raises `ValueError` about missing columns, run the loader (`data_load_clean()`) first to build the expected columns.

## Contact / Author

Meghana Patakota — [LinkedIn]

---
Small, self-contained repository intended for analysis and reporting. If you'd like, I can also add a minimal `Makefile` or a short CLI script to run the main report end-to-end.
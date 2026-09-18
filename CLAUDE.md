# Claude instructions

This file contains the same repository guidance as [`AGENTS.md`](AGENTS.md). Read both files when changing the project, and keep them aligned if the shared workflow changes. These rules apply to the whole `Assignment 1` repository.

## Project scope

This repository contains the data-understanding and preprocessing part of the Data Analysis & Learning Methods assignment. The main executable document is [`version1.ipynb`](version1.ipynb). It loads the recordings, checks their structure and quality, explores the sensor signals, makes the preprocessing decision, and writes the processed handoff in [`data/recordings/processed/current/`](data/recordings/processed/current/).

The owner of this part of the project is responsible for:

- loading and understanding the raw recordings;
- exploratory data analysis and visualisations;
- missing-value, duplicate, timestamp, and outlier checks;
- deciding and documenting preprocessing;
- reproducible processed-data exports and quality reports;
- handing the data and its limitations to the modelling work.

Windowing, feature engineering, feature selection, and supervised modelling belong to later work unless the user explicitly asks for them. Do not add class weights, sampling schemes, or train/test splitting to this preprocessing notebook by assumption.

## Read the sources before changing methodology

For a change that affects the analysis, data structure, or interpretation, inspect the relevant source material before editing:

- [`course_files/assignment/Assignment12026.pdf`](course_files/assignment/Assignment12026.pdf)
- [`course_files/assignment/AssignmentOne.pdf`](course_files/assignment/AssignmentOne.pdf)
- the relevant lecture PDFs in [`course_files/lecture_files/`](course_files/lecture_files/)
- the affected cells in [`version1.ipynb`](version1.ipynb)
- [`data/recordings/processed/README.md`](data/recordings/processed/README.md)

Use the PDFs as requirements and context, not as decoration. Check the exact page or section when a decision depends on a course rule. If a PDF cannot be read with the available tools, say so and use another local PDF reader or ask for help instead of guessing.

When explaining a change, refer to the repository files, notebook sections or cells, manifest columns, and source pages that support it. Prefer a concrete code reference such as `recording_registry.csv:recording_id` over a general statement. Never invent a result, ID, page number, or source claim.

Before editing, inspect the current Git status and preserve unrelated work. Keep changes within the requested scope.

## Code style

Write code in the order a person would follow it: load inputs, validate assumptions, transform data, inspect results, and save outputs. Use descriptive names and small, readable blocks. Keep existing paths, schemas, and variable names when they already communicate the project model.

Add a comment only when it explains a non-obvious reason, a constraint, or a decision that will help the next reader. Do not comment obvious Python. Every new code comment must use `#` and start with lowercase text.

```python
# keep the original timestamps for the later sensor-alignment check
raw_timestamps = sensor_data["time"].copy()
```

The lowercase rule applies to notebook code comments and comments added to scripts. It does not require changing comments that already exist outside the requested edit.

## Notebook and documentation style

Notebook markdown should explain what a check measures, why it matters, what the run found, and what follows from that result. Keep the existing student-like, academic voice: direct paragraphs, careful interpretation, and technical vocabulary where it helps.

Use the actual values from the final notebook run. If code changes a count, ID, peak, sample total, or quality result, update every dependent markdown cell and README paragraph. Remove stale claims rather than leaving two versions of a result in the notebook.

Use plain language inspired by the project’s humanizer guidance:

- remove filler, staged introductions, and repeated conclusions;
- avoid inflated claims, decorative bold, and chatbot phrasing;
- use a contrast only when both sides carry information;
- keep uncertainty where the data does not support a stronger claim;
- avoid em dashes unless the surrounding writing already uses them naturally.

Keep code, paths, formulas, column names, and generated data unchanged when humanizing prose. Read the surrounding paragraphs first so additions sound like the same author. The processed-data README can use first-person handoff language where it already does.

## Data and reproducibility rules

- Treat source archives and raw recording folders as read-only. Do not edit files in `data/recordings/archives/` or `data/recordings/raw/` to make a check pass.
- Use [`data/recordings/recording_registry.csv`](data/recordings/recording_registry.csv) for stable recording IDs. Do not reassign existing IDs through sorted-folder enumeration.
- Keep the selected sensor schema and units consistent with the notebook and manifest.
- Keep `DeploymentData/` outside the training-data preparation workflow and unchanged unless the user explicitly asks otherwise.
- Do not copy personal Downloads paths into code or documentation. Repository copies must be validated before source copies are removed or ignored.
- Keep generated files traceable to the notebook run. A processed CSV, quality report, preprocessing log, and manifest entry must refer to the same source recording and sensor stream.

## Checks before handing work back

After changing the notebook or data workflow:

1. Run `version1.ipynb` from a fresh kernel and save the intended outputs.
2. Check that the registry and discovered raw folders agree exactly, with unique IDs and source folders.
3. Check schemas, timestamps, missing and infinite values, duplicates, sensor alignment, and sample counts.
4. Check that every generated processed path is present in the manifest and that no stale ride directory remains outside it.
5. Check that processed values and timestamps match the validated raw inputs when preprocessing is meant to leave them unchanged.
6. Read the final notebook markdown and README for old counts, labels, IDs, or unsupported conclusions.
7. Run `git diff --check`, inspect `git status`, and report any validation that could not be completed.

Do not claim that a notebook run or validation passed unless it actually ran. Do not silently discard outputs or unrelated changes.

## Handoff and collaboration

When finishing a task, state what changed, which files were affected, what checks were run, and what remains for the next stage. Keep recording IDs available for tracing, but do not use them as model features. Keep each ride’s windows together when a later stage creates a train, validation, or test split. Fit scaling, balancing, and other learned transformations on training data only.

Keep this file and [`AGENTS.md`](AGENTS.md) aligned when shared workflow rules change. Do not commit or push changes unless the user asks for it.

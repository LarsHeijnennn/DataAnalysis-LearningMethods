# Data understanding and preprocessing — handoff

My part of the project was to understand the recordings, check their quality and prepare them for the next stage. The analysis is in [version1.ipynb](../../../version1.ipynb). The validated recordings are in [current/](current/).

You can load these files directly. You do not need to rerun the notebook before working on features or models.

## What I did

- Loaded all 31 recordings, including accelerometer, gyroscope and gravity data.
- Checked missing values, duplicates, invalid values, timestamps and sampling intervals. No structural problems appeared, so no correction was needed.
- Compared recordings across road labels and participants using descriptive statistics and plots.
- Preserved every sample because the annotation files contain no cycling start/stop labels and the measurements do not provide a reproducible cutoff rule.
- Repeated the quality checks and verified that saving and loading preserved all values and timestamps.

The notebook links the methods to the lectures and provided practical. Raw files are unchanged. No filtering, clipping, resampling, scaling or model windowing has been applied. Magnitude calculations are used only for exploration and are not added to the exported files.

## Why complete recordings are preserved

Phone handling may appear near the start or end of a recording. Those movements cannot be separated reliably from genuine road motion with the available labels. Choosing cutoffs by eye would add an undocumented decision and could discard useful signal.

All 31 recordings remain complete. The export contains **142,536 accelerometer samples**, **142,537 gyroscope samples** and **142,537 gravity samples**. Section 6 explains this decision; Appendix A can plot every complete recording when `SHOW_ALL_RECORDINGS = True`.

## Files to use

Inside `current/`:

| File | Contents |
|---|---|
| `manifest.csv` | Sensor file paths, recording/participant IDs, labels, units and sample counts |
| `P01/R001/Accelerometer.csv`, etc. | Complete measurements for each recording and sensor |
| `preprocessing_log.csv` | Input and output sample counts for every stream |
| `quality_raw.csv` / `quality_validated.csv` | Structural checks before and after copying |

Sensor files keep `time`, `seconds_elapsed`, `z`, `y`, `x`. `time` is an integer Unix timestamp in nanoseconds. `seconds_elapsed` refers to the original recording start. Acceleration and gravity use m/s²; gyroscope values use rad/s under the standardised export setup.

## How to load the data

Run this from a notebook in **Assignment 1**. Adjust the path if you copy the folder elsewhere.

```python
from pathlib import Path
import pandas as pd

processed_dir = Path("data/recordings/processed/current")
manifest = pd.read_csv(processed_dir / "manifest.csv")

recordings = {
    (row.recording_id, row.sensor): pd.read_csv(
        processed_dir / row.relative_path, float_precision="round_trip"
    )
    for row in manifest.itertuples(index=False)
}
labels = manifest[["recording_id", "participant_id", "class"]].drop_duplicates()

# inspect one complete accelerometer stream
example = recordings[("R001", "Accelerometer")]
example.head()
```

These are time-series measurements, not windows or a feature table. Keep recordings separate. If you combine sensors, use timestamps rather than assuming that matching row numbers mean matching times.

## What comes next

The next stage is windowing, feature engineering, feature selection and supervised modelling. Keep IDs for splitting and tracing results, not as model features. Windows from one recording should stay in the same split. Fit scalers on training data only, following the practical.

Phone handling at recording edges remains a possible source of noise. Any later window selection should use a documented rule and avoid learning decisions from validation or test data.

Another important limitation is participant coverage: P01 has 12 bumpy and 7 smooth recordings; P02 has 12 smooth and no bumpy recordings. They used different phones, so a model could pick up participant/device differences instead of road quality. Repeated routes, placement and unmeasured speed also affect interpretation. The independent deployment dataset has not been used.

## Rebuilding the files

Open `version1.ipynb` and run it from a fresh kernel. Package versions are printed in Setup. Section 7 rewrites the generated files in `current/`, but never the raw recordings.

The notebook's source inventory links IDs to original filenames. Processed IDs do not anonymise the original raw files.

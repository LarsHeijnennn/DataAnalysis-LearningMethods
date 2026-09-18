# Data understanding and preprocessing

This folder contains the output of my part of the project: loading the recordings, understanding the data, checking its quality, exploring the signals, and preparing a clean handoff for feature engineering and modelling. The full analysis is in [version1.ipynb](../../../version1.ipynb). The notebook can rebuild everything in [current/](current/) from the raw recordings.

## What `version1.ipynb` does

The notebook starts with one bumpy recording and inspects its accelerometer, gyroscope, and gravity streams. This gives a first look at the columns, units, value ranges, timestamps, and sampling frequency before applying the same checks to the full dataset.

It then loads all recordings through [recording_registry.csv](../recording_registry.csv). The registry gives every ride a stable ID, so adding new data does not change the IDs of earlier rides. The notebook combines this with metadata about the participant, road label, device, and recording settings.

For each selected sensor file, the notebook checks:

- the expected five-column schema;
- missing or infinite values;
- duplicate rows and timestamps;
- timestamps that move backwards;
- sampling frequency and unusually large time gaps;
- sample-count and timestamp alignment between sensors.

The EDA compares representative smooth and bumpy rides before summarising every recording. It uses vector magnitude to compare signals without depending on one phone axis. The plots cover acceleration and rotation, participant and class differences, large peaks, and possible phone handling near the start and end of a ride.

The final sections record the preprocessing decision, repeat the quality checks on the prepared copies, and write the processed files. Each saved CSV is loaded again and compared with its in-memory source. The notebook also checks that the folders in `current/` match the manifest, which prevents old generated files from remaining unnoticed.

## Main findings

The dataset contains 41 recordings and 123 selected sensor files. There are 22 bumpy and 19 smooth rides. P01 contributes 12 bumpy and 7 smooth recordings, while P02 contributes 10 bumpy and 12 smooth recordings.

All 123 files pass the structural checks. I found no missing or infinite values, duplicate rows, duplicate timestamps, or non-positive time steps. The observed sampling frequency ranges from 99.58 to 99.94 Hz, close to the intended 100 Hz. R020 has one fewer accelerometer sample than gyroscope and gravity samples at the end. The difference is about 10 ms. Sensor streams should therefore be combined by timestamp instead of row number.

The largest acceleration peak is 40.72 m/s² in smooth recording R021 at 0.64 seconds. This happens near the start of the recording, where phone handling is a plausible explanation. Within P02, the median acceleration-magnitude standard deviation is 2.128 m/s² for bumpy rides and 1.581 m/s² for smooth rides. The gyroscope summaries overlap more. The ten bumpy rides share a route and recording session, which may explain part of the acceleration difference.

Movement is often stronger near the recording edges. The annotation files do not contain cycling start and stop times, so the sensor data cannot show exactly where phone handling ends and cycling begins.

## Preprocessing decision

The files have no structural problems that require correction. I kept every sample and did not filter, clip, resample, scale, or impute the signals. Magnitude is calculated only for EDA and is not saved as an extra feature.

I also kept the complete start and end of every recording. Choosing cutoffs by eye would be difficult to reproduce and could remove genuine road movement. Windowing and any rule for excluding edge windows belong to the feature-engineering stage.

The processed export contains 192,366 accelerometer samples, 192,367 gyroscope samples, and 192,367 gravity samples.

## Collection setup and limitations

All recordings followed the same collection protocol. The phone was face down in a tight right trouser pocket, cycling speed was constant, and the same gear was used where applicable.

Both participants recorded both road labels, which gives each phone model examples of smooth and bumpy roads. Device still identifies the participant because P01 used an iPhone 17 Pro and P02 used an iPhone 13 Pro.

Brian recorded all ten new bumpy rides on the Kruisstraat route during one short session. A random split could place very similar conditions in both training and evaluation data. Windows from one ride must stay in the same split. A route- or session-grouped sensitivity check would also be useful once reliable group labels are available.

The separate deployment recording is not used in this notebook.

## How this relates to the course

The [September 4 lecture](../../../course_files/lecture_files/5ARE0-Lecture-20260904.pdf) covers raw measurements, sampling, missing values, and decisions about conditioning data. These topics guide the structural checks and the decision to leave valid samples unchanged.

The [September 8 lecture](../../../course_files/lecture_files/5ARE0-Lecture-20260908.pdf) introduces combinations such as vector magnitude and features calculated over time windows. This notebook uses magnitude for exploration. Windowing and feature calculation come after this handoff.

The [assignment instructions](../../../course_files/assignment/Assignment12026.pdf) require separate raw and processed data, consistent labels and timestamps, documented preprocessing choices, and reproducible code. The notebook follows this structure and leaves the raw files unchanged.

## Processed files

`P01` and `P02` are participant IDs. `R001`, `R002`, and so on are individual rides. Every processed ride has separate accelerometer, gyroscope, and gravity files because the sensors measure different quantities and use different units.

Start with `manifest.csv`. It links each processed file to its recording ID, participant, class, raw folder, device, sample count, and unit.

| File | Contents |
|---|---|
| `../recording_registry.csv` | Stable mapping from recording IDs to raw folders |
| `manifest.csv` | Main index for the processed data |
| `P01/R001/Accelerometer.csv`, etc. | Complete sensor streams for each ride |
| `preprocessing_log.csv` | Input and output sample counts for every stream |
| `quality_raw.csv` | Structural checks on the raw streams |
| `quality_validated.csv` | The same checks after preparation |

Sensor files keep `time`, `seconds_elapsed`, `z`, `y`, and `x`. `time` is a Unix timestamp in nanoseconds. `seconds_elapsed` starts at the beginning of the original recording. Acceleration and gravity use m/s², while gyroscope values use rad/s.

## Loading the processed data

Run this from a notebook in the `Assignment 1` folder. Change the path if the data was copied somewhere else.

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

# inspect one accelerometer stream
example = recordings[("R001", "Accelerometer")]
example.head()
```

These files contain complete time series. They do not contain windows or a feature table. Keep each ride separate and match sensor measurements by timestamp when streams are combined.

## Next step

My part ends with this processed and documented handoff. The next stage is windowing, feature engineering, feature selection, and supervised modelling. Recording IDs are useful for splitting and tracing results, but they must not become model features. Fit any scaling or balancing method on the training data only.

Phone handling near the edges may still add noise. If edge windows are removed later, the rule should be set before evaluating the models and applied consistently to all recordings.

## Rebuilding the files

Open `version1.ipynb` and run it from a fresh kernel. The setup section prints the package versions. The notebook reads stable IDs from `recording_registry.csv`, rebuilds `current/`, and stops if the registry and raw folders do not match.

The participant IDs organise the processed export. They do not anonymise the names used in the raw folders.

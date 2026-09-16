# Data understanding and preprocessing handoff

This folder is my handoff from the data-understanding and preprocessing part of the project. The full analysis is in [version1.ipynb](../../../version1.ipynb). I went through the raw recordings, checked their quality, explored the signals, and exported a traceable copy for the rest of the group. You can use the files in [current/](current/) directly for feature engineering and modelling; there is no need to rerun the notebook first.

## What is in `current/`?

`P01` and `P02` are the participant IDs. `R001`, `R002`, and so on are individual rides. Each ride has three sensor files: `Accelerometer.csv`, `Gyroscope.csv`, and `Gravity.csv`. I kept the streams separate because they measure different things and have different units.

Start with `manifest.csv`. It tells you the participant, road label, original raw folder, device, and file path for every sensor stream. For modelling, you mainly need the manifest and the sensor files it points to. The other CSVs are evidence of the checks I did, so you can leave them alone unless you need them for the report.

## What I checked

I loaded all 31 recordings, which gives 93 selected sensor files in total. I checked every stream for missing values, invalid values, duplicate rows or timestamps, timestamp order, and sampling gaps. I also compared the recordings by road label and participant using descriptive statistics and plots.

All 93 files passed these checks. There were no missing or infinite values, duplicate rows or timestamps, or backwards time steps. The observed sampling rate was between 99.58 and 99.94 Hz, which is close to the intended 100 Hz. R020 has one fewer accelerometer sample than its gyroscope and gravity streams at the end of the recording. This is a difference of about 10 ms, rather than a missing block of data. If you combine sensor streams later, match them by timestamp instead of row number.

I also checked whether unusually large values looked like sensor errors or outliers. The largest acceleration peak is 40.72 m/s² in smooth recording R021 at 0.64 seconds, where phone handling is a plausible explanation. In the P01 recordings, the bumpy rides show higher and more sustained acceleration variation than the smooth rides. The gyroscope values overlap more. P02 only has smooth rides, so it cannot provide a clean comparison between the road labels. These observations are useful for later feature engineering, but they are not enough to justify deleting individual values.

## What I changed

The files did not have structural problems that needed correction. I therefore kept all samples and did not filter, clip, resample, scale, or impute anything. I calculated magnitudes only for exploration, and they are not included in the exported files. Windowing is also not done here; that belongs with feature engineering and modelling.

The beginning or end of a recording includes phone handling. I compared fixed five-second start and end segments with the middle of each ride to inspect this. The plots show that movement is often stronger at an edge than in the middle, especially for the accelerometer and gyroscope. That is consistent with handling the phone or stopping, but it does not prove that every edge sample is contaminated. The available annotation files do not say when cycling starts or stops, so I could not turn that diagnostic into a reliable cropping rule. Cutting parts of a ride by eye would have been arbitrary. I therefore kept the 31 complete recordings as they are. The export contains 142,536 accelerometer samples, 142,537 gyroscope samples, and 142,537 gravity samples.

## How this relates to the course

The [September 4 lecture](../../../course_files/lecture_files/5ARE0-Lecture-20260904.pdf) discusses keeping raw measurements, checking sampling, and deciding how to condition data. That is why I inspected the raw streams before applying any preprocessing. The same lecture covers missing values, but there were none here, so imputation was unnecessary.

The [September 8 lecture](../../../course_files/lecture_files/5ARE0-Lecture-20260908.pdf) introduces combining measurements into features and extracting characteristics over time windows. I used vector magnitude only as an EDA view of the three axes. Creating windows and choosing model features come after this handoff.

The [assignment instructions](../../../course_files/assignment/Assignment12026.pdf) ask us to keep raw and processed data separate, use consistent labels and timestamps, and document the data-management choices. This export does that while leaving the raw recordings unchanged.

## Files to use

Inside `current/`:

| File | Contents |
|---|---|
| `manifest.csv` | The main index for the exported data |
| `P01/R001/Accelerometer.csv`, etc. | The three complete sensor streams for each ride |
| `preprocessing_log.csv` | Input and output sample counts for each stream |
| `quality_raw.csv` / `quality_validated.csv` | Results of the structural checks before and after exporting |

Sensor files keep `time`, `seconds_elapsed`, `z`, `y`, and `x`. `time` is a Unix timestamp in nanoseconds, while `seconds_elapsed` is measured from the start of the original recording. Acceleration and gravity use m/s²; gyroscope values use rad/s.

## How to load the data

Run this from a notebook in the `Assignment 1` folder. Change the path if you copied the data somewhere else.

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

These files contain time series, not windows or a feature table. Keep the recordings separate. If you combine sensor streams, use timestamps instead of assuming that the same row number means the same moment in time.

## What still needs to happen

The next step is windowing, feature engineering, feature selection, and supervised modelling. Keep the IDs for splitting and tracing the results, but do not use them as model features. Windows from one ride should stay in the same data split. Any scaling should be fitted on the training set only.

Phone handling near the edges of a recording may still add noise. If you decide to remove windows later, use a clear rule and decide it without looking at validation or test results.

There is an important limitation in the data: P01 has 12 bumpy and 7 smooth recordings, while P02 has 12 smooth recordings and no bumpy recordings. The participants also used different phones. A model could therefore learn differences between participants or devices instead of differences in road quality. Routes, phone placement, and speed may also affect the measurements. The separate deployment dataset has not been used here.

## Rebuilding the files

Open `version1.ipynb` and run it from a fresh kernel. The package versions are printed in the setup section. The notebook rewrites the generated files in `current/` and leaves the raw recordings untouched.

The manifest links each processed ID to its original raw folder. The participant IDs only organise the processed export; they do not anonymise the raw files.

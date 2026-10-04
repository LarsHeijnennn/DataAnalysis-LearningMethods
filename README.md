# Group 24: Bicycle lane quality

`group24.ipynb` follows 41 labeled bicycle rides from raw-data checks through feature extraction and model evaluation. It aligns the sensor streams by timestamp and compares four supervised classifiers with four clustering methods. The selected model is then applied to one independent deployment recording. All analysis code is in the notebook, which runs without project Python scripts or saved model checkpoints.

## Setup

Use 64-bit Python 3.12 with the pinned package versions in the installation commands below. A separate `requirements.txt` is not needed for the submission. The notebook was tested with Python 3.12.14 on macOS; it has not been run on Windows. Its code uses `pathlib` and relative paths for Windows, macOS and Linux, without absolute user paths or OS-specific shell commands.

Package the submission as `group24_HAR_submission.zip` with exactly four top-level entries and no enclosing project folder:

```text
group24.ipynb
group24_Report.pdf
README.md
data/
  recordings/
    recording_registry.csv
    raw/<class>/<participant>/<recording>/*.csv
  DeploymentData/
    Accelerometer.csv
    Gyroscope.csv
    Gravity.csv
```

After extraction, the setup commands below copy `data/DeploymentData/` to a top-level `DeploymentData/` folder. This is required because the executed notebook reads the external sensors from that location. The extra folder is created locally during setup and is not a fifth entry in the ZIP. The working repository already contains this folder; the copy uses the same sensor files.

Build the archive from the files shown above, rather than compressing the whole working repository. Keep the registry and every raw recording's sensor and metadata CSVs. Exclude `.git/`, `.venv/`, `archive/`, `course_files/`, the root `DeploymentData/`, the development `requirements.txt`, source recording ZIP archives, generated outputs and system files such as `.DS_Store`. Processed sensor files, features, model checkpoints and deployment results are rebuilt by the notebook and are not required inputs.

Run the setup commands in the folder containing `group24.ipynb`, called `Assignment 1` in this repository. Paths with spaces work. Create a fresh environment on each computer, since virtual environments cannot be copied between operating systems.

### macOS (Terminal)

Install Python 3.12 if necessary, then run:

```sh
cp -R data/DeploymentData .
python3.12 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install numpy==2.5.2 pandas==3.0.5 matplotlib==3.11.1 scikit-learn==1.9.0 scipy==1.18.1 joblib==1.6.0 threadpoolctl==3.6.0 IPython==9.17.1 ipykernel==7.3.0 nbformat==5.11.1 nbclient==0.11.0
.venv/bin/python -m pip check
.venv/bin/python -m ipykernel install --user --name dalm-assignment --display-name "Python 3.12 (Group 24)"
```

### Windows (PowerShell)

Install 64-bit Python 3.12 with the Python launcher, then run:

```powershell
Copy-Item -Path data/DeploymentData -Destination . -Recurse -Force
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install numpy==2.5.2 pandas==3.0.5 matplotlib==3.11.1 scikit-learn==1.9.0 scipy==1.18.1 joblib==1.6.0 threadpoolctl==3.6.0 IPython==9.17.1 ipykernel==7.3.0 nbformat==5.11.1 nbclient==0.11.0
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m ipykernel install --user --name dalm-assignment --display-name "Python 3.12 (Group 24)"
```

The commands call the environment's Python directly. You do not need to activate it through a PowerShell script or change the execution policy. On Linux, use the macOS commands with Python 3.12 installed.

### Run the notebook

Open `group24.ipynb` in an editor that supports Jupyter notebooks, such as VS Code with its Python and Jupyter extensions. Select the Python 3.12 (Group 24) kernel and restart it. Run all cells in order, then save the notebook. The first code cell prints the Python and package versions and stops if they do not match Python 3.12 and the pinned analysis packages. Run from the project folder or its repository parent so the notebook can find the raw data.

To run the notebook and save all outputs from a macOS or Linux terminal:

```sh
.venv/bin/python -c "from pathlib import Path; import nbformat; from nbclient import NotebookClient; p=Path('group24.ipynb'); n=nbformat.read(p, as_version=4); NotebookClient(n, timeout=1200, kernel_name='dalm-assignment', resources={'metadata': {'path': str(Path.cwd())}}).execute(); nbformat.write(n, p)"
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\python.exe -c "from pathlib import Path; import nbformat; from nbclient import NotebookClient; p=Path('group24.ipynb'); n=nbformat.read(p, as_version=4); NotebookClient(n, timeout=1200, kernel_name='dalm-assignment', resources={'metadata': {'path': str(Path.cwd())}}).execute(); nbformat.write(n, p)"
```

Running the notebook rebuilds the outputs listed below and requires write access to the project folder. The source sensor CSVs stay unchanged.

If the notebook cannot find its inputs, check that you extracted the complete `data/` folder and ran the setup copy command to create `DeploymentData/` beside the notebook. If the version check fails, check that you selected the newly installed kernel. Small numerical and timing differences between computers are possible even with pinned packages. The eight held-out recording IDs and random seeds are fixed.

The version-check error refers to the working repository's `requirements.txt`; the installation commands in this README contain the same pins, so that file is not needed in the ZIP.

## Dataset description

Two participants collected 41 labeled rides in Eindhoven and Helmond using Sensor Logger at a target rate of 100 Hz. There are 22 bumpy and 19 smooth rides: P01 contributes 12 bumpy and 7 smooth, and P02 contributes 10 bumpy and 12 smooth.

The phones were placed face down in a tight right trouser pocket. Recording starts before placement and ends after removal, so the start and end can include phone handling. Participant and device are inseparable in this dataset, and some routes and recording sessions repeat.

- `data/recordings/raw/<class>/<participant>/<recording>/` contains the original per-ride CSVs and `Metadata.csv`. Classes are `bumpy` and `smooth`. The notebook uses the calibrated `Accelerometer.csv`, `Gyroscope.csv` and `Gravity.csv`; additional exported files are not model inputs.
- `data/recordings/recording_registry.csv` maps stable IDs `R001` through `R041` to relative `source_folder` paths. Every raw ride must appear exactly once. Registry paths use forward slashes on all systems.
- `data/DeploymentData/` contains one independent recording without road labels; setup copies it to `DeploymentData/` for the notebook. The notebook uses it for inference after model selection and excludes it from training, tuning and test scoring. Without road labels, its predictions cannot establish deployment accuracy.

Each selected sensor CSV has five columns: `time`, `seconds_elapsed`, `x`, `y` and `z` (axis order in the file may differ). `time` is an integer Unix timestamp in nanoseconds; `seconds_elapsed` is elapsed recording time in seconds. Acceleration and gravity are measured in m/s² and gyroscope values in rad/s. Timestamp alignment handles the one-sample difference at the end of R020. Complete source streams contain 192,366 accelerometer samples and 192,367 samples each for gyroscope and gravity.

The notebook creates 709 overlapping windows of 500 samples (approximately five seconds), with a new window every 250 samples. Each window gets its ride's label, which may not describe stops, handling or short changes in the road surface. Splitting by recording keeps overlapping windows from the same ride in one fold. It does not establish how well the model transfers to a new rider, route or day. Longer rides contribute more windows to the window-level metrics.

### Participant identifiers and privacy

Raw participant folders use P01/P02, recording folders use stable R### IDs, and the registry and generated manifest use matching paths. Persistent device IDs in `Metadata.csv` are replaced with Device01/Device02. Phone model names are retained for interpreting device differences.

Saved notebook output paths were updated directly for this identifier cleanup without rerunning the analysis. Sensor measurements, timestamps, model results, figures and execution counts are unchanged. Required author names and student numbers remain on the notebook title page. Dates and general collection locations remain documented for interpreting the study; the identifiers have been pseudonymized rather than making the data impossible to re-identify.

Historical archives, Git history and local backups may retain original identifiers and must not be included in the submission ZIP. Use only the submission inputs listed above.

## Generated outputs

| Directory | Contents |
|---|---|
| `data/recordings/processed/current/` | Complete validated sensor streams, manifest, structural quality reports and preprocessing log |
| `data/features/supervised/current/` | Window features, split, grouped model comparison, feature-selection scores, selected features, held-out ride/window predictions, boundary sensitivity and model checkpoints |
| `data/features/unsupervised/current/` | Configuration/sensitivity tables, clustering metrics and composition, cluster assignments, grouped cluster-to-road prediction results and fitted model checkpoints |
| `data/deployment/current/` | Sensor retention, individual window predictions, disjoint one-second timeline, contiguous predicted segments and the deployment figure |

The notebook checks the structure of every selected stream and reads each exported file back to confirm that the raw measurements stayed unchanged. `run_summary.json` records the values used in the notebook's written results.

To load a checkpoint, use the class definitions from the notebook and the same environment. The saved transformations and models are fitted on training data only, without refitting on held-out or deployment data.

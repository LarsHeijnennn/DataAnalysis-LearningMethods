import nbformat


def markdown(source):
    return nbformat.v4.new_markdown_cell(source)


def code(source):
    return nbformat.v4.new_code_cell(source)


simple_part3_cells = [
    markdown("""## 2. Unsupervised models from the lectures

The four clustering methods are K-means, agglomerative clustering, DBSCAN and a Gaussian mixture model (GMM). These are the methods covered in the clustering lectures. The number of clusters is set to two because the recordings have two known road classes. PCA is used only to reduce the selected feature set and to make a two-dimensional visualisation possible.
"""),
    code("""from sklearn.cluster import AgglomerativeClustering, DBSCAN, KMeans
from sklearn.decomposition import PCA
from sklearn.mixture import GaussianMixture

selected_feature_table = pd.read_csv(feature_dir / "selected_features.csv")
selected_feature_names = selected_feature_table.loc[
    selected_feature_table["selected"], "feature"
].tolist()

unsupervised_preprocessor = Pipeline([
    ("scale", StandardScaler()),
    ("pca", PCA(n_components=0.95)),
])
X_unsupervised_train = unsupervised_preprocessor.fit_transform(
    X_train[selected_feature_names]
)

print(f"Features from Part 2: {len(selected_feature_names)}")
print(f"PCA components kept: {X_unsupervised_train.shape[1]}")
print("Models: K-means, agglomerative clustering, DBSCAN and GMM")
"""),
    markdown("""## 3. Clustering results

Clustering does not use the road-class labels when making clusters. After clustering, the known labels are used only to check whether each cluster mainly represents smooth or bumpy road. This produces a simple cluster-agreement accuracy. It is an exploratory result, not a separate predictive test score.
"""),
    code("""def cluster_agreement(cluster_labels, road_labels):
    cluster_labels = np.asarray(cluster_labels)
    road_labels = pd.Series(road_labels).reset_index(drop=True)
    predicted_labels = []

    for cluster_id in cluster_labels:
        members = road_labels[cluster_labels == cluster_id]
        predicted_labels.append(members.mode().iloc[0])

    return accuracy_score(road_labels, predicted_labels)


unsupervised_models = {
    "K-means": KMeans(n_clusters=2, random_state=RANDOM_STATE),
    "Agglomerative clustering": AgglomerativeClustering(n_clusters=2),
    "DBSCAN": DBSCAN(eps=3.0, min_samples=5),
    "Gaussian mixture model": GaussianMixture(n_components=2, random_state=RANDOM_STATE),
}

unsupervised_rows = []
fitted_unsupervised_models = {}

for model_name, model in unsupervised_models.items():
    cluster_labels = model.fit_predict(X_unsupervised_train)
    agreement_accuracy = cluster_agreement(cluster_labels, y_train)
    number_of_clusters = len(set(cluster_labels))

    fitted_unsupervised_models[model_name] = cluster_labels
    unsupervised_rows.append({
        "model": model_name,
        "cluster_agreement_accuracy": agreement_accuracy,
        "number_of_clusters": number_of_clusters,
        "noise_fraction": float(np.mean(cluster_labels == -1)),
    })

unsupervised_comparison = pd.DataFrame(unsupervised_rows).sort_values(
    "cluster_agreement_accuracy", ascending=False
)
best_unsupervised_model_name = unsupervised_comparison.iloc[0]["model"]

unsupervised_comparison.to_csv(
    unsupervised_dir / "unsupervised_model_comparison.csv", index=False
)
unsupervised_comparison.round(3)
"""),
    markdown("""## 4. Visualisation of the best clustering result

The plot shows the first two principal components. The left panel colours the windows using the known road classes, while the right panel colours them using the clusters. This helps assess whether the cluster structure resembles the recorded smooth and bumpy labels.
"""),
    code("""best_cluster_labels = fitted_unsupervised_models[best_unsupervised_model_name]

figure, axes = plt.subplots(1, 2, figsize=(12, 5), sharex=True, sharey=True)
for road_class, color in [("smooth", "tab:blue"), ("bumpy", "tab:orange")]:
    mask = y_train.to_numpy() == road_class
    axes[0].scatter(
        X_unsupervised_train[mask, 0],
        X_unsupervised_train[mask, 1],
        label=road_class,
        color=color,
        alpha=0.65,
        s=20,
    )
axes[0].set_title("Known training road labels")
axes[0].set_xlabel("PCA component 1")
axes[0].set_ylabel("PCA component 2")
axes[0].legend(title="Road class")

for cluster_id in sorted(set(best_cluster_labels)):
    mask = best_cluster_labels == cluster_id
    label = "noise" if cluster_id == -1 else f"cluster {cluster_id}"
    axes[1].scatter(
        X_unsupervised_train[mask, 0],
        X_unsupervised_train[mask, 1],
        label=label,
        alpha=0.65,
        s=20,
    )
axes[1].set_title(f"{best_unsupervised_model_name} clusters")
axes[1].set_xlabel("PCA component 1")
axes[1].legend(title="Cluster")
figure.suptitle("Training windows in the first two PCA components")
figure.tight_layout()
plt.show()
"""),
    markdown("""## 5. Supervised versus unsupervised comparison and final model

The supervised result is the held-out accuracy already calculated in Part 2. The unsupervised value is kept separate because it is an exploratory cluster-agreement score calculated on the training data. The supervised random forest is selected for deployment because it was evaluated on independent held-out rides and can directly predict the class of a new window.
"""),
    code("""supervised_test_accuracy = float(test_results.iloc[0]["test_accuracy"])
best_unsupervised_result = unsupervised_comparison.iloc[0]

model_comparison = pd.DataFrame([
    {
        "approach": "Supervised",
        "model": best_model_name,
        "accuracy": supervised_test_accuracy,
        "evaluation_data": "held-out rides from Part 2",
        "purpose": "predict a road class for a new window",
    },
    {
        "approach": "Unsupervised",
        "model": best_unsupervised_model_name,
        "accuracy": best_unsupervised_result["cluster_agreement_accuracy"],
        "evaluation_data": "training rides after clustering",
        "purpose": "explore whether natural groups resemble the road classes",
    },
])

final_choice = {
    "approach": "Supervised",
    "selected_model": best_model_name,
    "reason": "It has the strongest valid held-out accuracy and can predict new windows.",
}

model_comparison.to_csv(
    unsupervised_dir / "supervised_unsupervised_comparison.csv", index=False
)
pd.DataFrame([final_choice]).to_csv(
    unsupervised_dir / "final_model_selection.csv", index=False
)

print(f"Final model for deployment: {best_model_name}")
model_comparison.round(3)
"""),
    markdown("""## 6. Deploy the final model on the independent recording

The independent deployment recording is kept outside model training and evaluation. The selected supervised pipeline is applied after the same alignment, windowing and feature calculation used for the labelled recordings.
"""),
    code("""deployment_source_dir = Path("DeploymentData")
deployment_dir = Path("data/deployment/current")
deployment_dir.mkdir(parents=True, exist_ok=True)

deployment_sensor_paths = sorted(deployment_source_dir.rglob("*.csv"))
if not deployment_sensor_paths:
    raise FileNotFoundError(f"No deployment CSV files found in {deployment_source_dir}")

deployment_streams = {}
for sensor_path in deployment_sensor_paths:
    sensor_name = sensor_path.stem.lower()
    if sensor_name not in {"accelerometer", "gyroscope", "gravity"}:
        continue
    sensor_data = pd.read_csv(sensor_path)
    if sensor_data.isna().any().any() or not np.isfinite(sensor_data.select_dtypes(include=np.number)).all().all():
        raise ValueError(f"Deployment stream contains missing or infinite values: {sensor_path}")
    deployment_streams[sensor_name.title()] = sensor_data

expected_sensors = {"Accelerometer", "Gyroscope", "Gravity"}
if set(deployment_streams) != expected_sensors:
    raise ValueError(f"Expected {expected_sensors}; found {set(deployment_streams)}")

deployment_recording = align_sensor_streams(deployment_streams)
deployment_rate_hz, deployment_max_gap_seconds = sampling_diagnostics(deployment_recording)
deployment_features = pd.DataFrame(make_window_features(
    deployment_recording,
    recording_id="DeploymentData",
    participant_id="external",
    road_class=None,
))
deployment_X = deployment_features[feature_columns]

if deployment_X.columns.tolist() != feature_columns:
    raise ValueError("Deployment feature table does not match the labelled feature schema.")

print(f"Deployment aligned samples: {len(deployment_recording)}")
print(f"Deployment median sample rate: {deployment_rate_hz:.2f} Hz; largest gap: {deployment_max_gap_seconds:.4f} s")
print(f"Deployment windows: {len(deployment_features)}")
"""),
    code("""deployment_predictions = best_pipeline.predict(deployment_X)
deployment_output = deployment_features[[
    "recording_id",
    "window_start_seconds",
    "window_end_seconds",
]].copy()
deployment_output["predicted_class"] = deployment_predictions

deployment_output.to_csv(
    deployment_dir / "deployment_window_predictions.csv", index=False
)

class_colours = {"smooth": "tab:blue", "bumpy": "tab:orange"}
figure, axis = plt.subplots(figsize=(12, 3))
for road_class, color in class_colours.items():
    rows = deployment_output[deployment_output["predicted_class"] == road_class]
    for _, row in rows.iterrows():
        axis.axvspan(
            row["window_start_seconds"],
            row["window_end_seconds"],
            color=color,
            alpha=0.6,
        )
axis.set_xlabel("Time in the external recording (seconds)")
axis.set_yticks([])
axis.set_title(f"Deployment prediction using {best_model_name}")
legend_handles = [
    plt.Rectangle((0, 0), 1, 1, color=color, alpha=0.6, label=road_class)
    for road_class, color in class_colours.items()
]
axis.legend(handles=legend_handles, loc="upper right")
figure.tight_layout()
figure.savefig(deployment_dir / "deployment_lane_quality_timeline.png", dpi=150)
plt.show()

print(f"Deployment model: {best_model_name}")
print(deployment_output["predicted_class"].value_counts().rename("windows"))
"""),
    markdown("""## 7. Part 3 outputs and limitations

The unsupervised models are used to explore the structure of the training windows. Their agreement value is not a held-out prediction result because clustering has no class labels during fitting. The random forest remains the deployment model because its performance was checked on held-out rides in Part 2. The external recording is not used to train or select any model.
"""),
    code("""print("Saved Part 3 outputs:")
for path in sorted(unsupervised_dir.glob("*.csv")):
    print(f"- {path}")
for path in sorted(deployment_dir.glob("*")):
    print(f"- {path}")
"""),
]


version3 = nbformat.read("version3.ipynb", as_version=4)
version3.cells = version3.cells[:6] + simple_part3_cells
nbformat.write(version3, "version3.ipynb")

pipeline = nbformat.read("project_pipeline.ipynb", as_version=4)
part3_start = next(
    index
    for index, cell in enumerate(pipeline.cells)
    if cell.cell_type == "markdown" and cell.source.startswith("# Part 3:")
)
pipeline_cells = [markdown("""# Part 3: Unsupervised learning, comparison and deployment

**Part 3 owner: Amir**

This section uses only the four clustering methods discussed in the course lectures: K-means, agglomerative clustering, DBSCAN and a Gaussian mixture model. It then compares the exploratory clustering result with the held-out supervised result from Part 2 and deploys the supervised model on the independent recording.
""")]
for cell in simple_part3_cells:
    copied = nbformat.from_dict(cell)
    if copied.cell_type == "markdown":
        copied.source = copied.source.replace("## 2.", "## 9.", 1).replace("## 3.", "## 10.", 1).replace("## 4.", "## 11.", 1).replace("## 5.", "## 12.", 1).replace("## 6.", "## 13.", 1).replace("## 7.", "## 14.", 1)
    pipeline_cells.append(copied)
pipeline.cells = pipeline.cells[:part3_start] + pipeline_cells
nbformat.write(pipeline, "project_pipeline.ipynb")

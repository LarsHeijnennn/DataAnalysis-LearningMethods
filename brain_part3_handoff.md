# Part 3 handoff for Brian

Brian, start from the `brain` branch. It is a copy of the revised work, so your changes can build on it without changing `main` or Amir’s branch.

## Branches

- **`main`** contains the current work, including the separate [version1.ipynb](version1.ipynb) and [version2.ipynb](version2.ipynb) notebooks and the merged [project_pipeline.ipynb](project_pipeline.ipynb).
- **`amir-revised-by-lars`** is the revised version. It adds [project_pipeline.ipynb](project_pipeline.ipynb), which puts Parts 1 and 2 together, and updates the saved feature and model-result files.
- **`brain`** on the remote mirrors the updated `main`. The existing local branch is named `brian`. This is the branch for your Part 3 work.

`brain` is synchronized with `main` for this handoff. `amir-revised-by-lars` remains at commit `394dffb2`.

## What the merged notebook does

The merged notebook checks and exports the 41 rides, then turns the sensor data into 709 overlapping five-second windows with 121 candidate features. It compares four supervised classifiers using grouped cross-validation, keeping each ride’s windows together. Feature selection, scaling, and model tuning happen inside the folds; the eight held-out rides are reserved for the final evaluation.

The current run selects random forest using grouped cross-validation (macro F1 0.950). Its held-out accuracy is 0.963 and macro F1 is 0.960 on 136 windows. Majority vote matches all eight held-out ride labels. That is a small test set, so it does not establish performance on new riders or routes.

## Part 3

Amir has now implemented Part 3 in both `project_pipeline.ipynb` and the separate `version3.ipynb`. It fits K-means, agglomerative clustering, DBSCAN and GMM using label-free feature preparation, reports exploratory training agreement, and deploys the supervised model selected in Part 2. DBSCAN noise remains unassigned and does not count as a cluster or a correct agreement match. The clustering agreement is not a held-out predictive score.

If Part 3 uses the existing windows, the saved feature table is `data/features/supervised/current/window_features.csv`. Keep labels and ride IDs separate from model inputs unless the assignment specifically says otherwise.

## Getting the branch

In an existing clone, run:

```sh
git fetch origin
git switch --track -c brain origin/brain
```

The notebook metadata update in `version2.ipynb` is included in this handoff.

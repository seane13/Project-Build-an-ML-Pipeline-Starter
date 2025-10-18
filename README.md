# NYC Airbnb ML Pipeline

**Author:** Sean Endicott
**W&B Project:** [nyc_airbnb (public)](https://wandb.ai/seane13-western-governors-university/nyc_airbnb)
**GitHub Repo:** [Project-Build-an-ML-Pipeline-Starter](https://github.com/seane13/Project-Build-an-ML-Pipeline-Starter)

---

## Project Overview

This project implements a reusable end-to-end ML workflow for predicting short-term rental prices in New York City, designed for property management teams who receive fresh bulk data weekly and need reliable, automated retraining.

The pipeline uses **MLflow**, **Hydra configuration**, and **Weights & Biases (W&B)** to orchestrate:
- Data downloading and cleaning
- Quality testing
- Data splitting
- Model training and hyperparameter search
- Model selection and production model promotion
- Test-set evaluation
- Reproducible, versioned releases

---

## Table of Contents

- [Quick Start](#quick-start)
- [Rubric & Submission Links](#rubric--submission-links)
- [Pipeline Steps](#pipeline-steps)
- [Versioning & Re-releases](#versioning--re-releases)
- [Common Issues](#common-issues)
- [License](#license)

---

## Quick Start

### Requirements
- **Python 3.10**
- **conda** (for environments)
- A free [Weights & Biases](https://wandb.ai/) account (API key required)

### Setup
git clone https://github.com/seane13/Project-Build-an-ML-Pipeline-Starter.git
cd Project-Build-an-ML-Pipeline-Starter
conda env create -f environment.yml
conda activate nyc_airbnb_dev
wandb login [your API key]

### Run Full Pipeline
mlflow run .

### To run specific steps (e.g., just cleaning and splitting):
mlflow run . -P steps=download,basic_cleaning,data_split


### Override any config parameter using Hydra:
mlflow run . -P steps=train_random_forest
-P hydra_options="modeling.random_forest.n_estimators=50"


---

## Rubric & Submission Links

- **W&B project:** [nyc_airbnb](https://wandb.ai/seane13-western-governors-university/nyc_airbnb) (public)
- **GitHub repo:** [Project-Build-an-ML-Pipeline-Starter](https://github.com/seane13/Project-Build-an-ML-Pipeline-Starter)
- Please paste these links in your submission box AND keep them in this README for reviewers.

---

## Pipeline Steps

1. **Download data:** Produces `sample.csv` artifact in W&B.
2. **Basic cleaning:** Cleans data, enforces NYC boundaries, outputs `clean_sample.csv`.
   - All parameters have type annotations and docstrings, and are accessed from `config.yaml` (not hardcoded).
3. **Data quality tests:** `test_row_count`, `test_price_range`, and geoboundary checks included. The latest `clean_sample.csv` is manually tagged as `reference` in W&B.
4. **Split data:** Outputs `trainval_data.csv` and `test_data.csv` artifacts.
5. **Train Random Forest:**
   - Implements required pipeline steps, logs MAE, exports MLflow model as artifact.
   - Multiple runs logged via Hydra for hyperparameter search.
6. **Promote best model:** Tag the artifact with best MAE as `prod` in W&B.
7. **Test Regression Model:** Compares test-set MAE to validation; checks for overfitting.
8. **Visualize pipeline:** View graph in W&B Artifacts Lineage tab.
9. **Release:** Tag and release (e.g., `v1.0.0`). All config defaults reflect best hyperparameters.
10. **New Data Sample:** Run release (`v1.0.0`) on new sample (`sample2.csv`). Project already includes geoboundary cleaning as required; initial failure and required fix steps are documented in the code.

---

## Versioning & Re-releases

- Releases are tagged on GitHub (`v1.0.0`, `v1.0.1`, etc.).
- Latest stable version referenced in MLflow runs.
- See [GitHub releases](https://github.com/seane13/Project-Build-an-ML-Pipeline-Starter/releases).

---

## Common Issues

- If MLflow cannot find a release tag, ensure the tag exists both locally and on GitHub.
- For environment issues, clean old `mlflow-*` conda environments:

for e in $(conda info --envs | grep mlflow | cut -f1 -d" "); do conda env remove --name $e -y; done


---

## License

See [LICENSE.txt](LICENSE.txt).

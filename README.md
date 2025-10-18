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

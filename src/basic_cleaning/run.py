#!/usr/bin/env python
"""
Download from W&B the raw dataset and apply some basic data cleaning,
exporting the result to a new artifact.
"""
import argparse
import logging
import wandb
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):
    run = wandb.init(project="nyc_airbnb",job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact
    artifact_local_path = run.use_artifact(args.input_artifact).file()
    df = pd.read_csv(artifact_local_path)

    # Drop outliers
    idx = df["price"].between(args.min_price, args.max_price)
    df = df[idx].copy()

    # Convert last_review to datetime
    df["last_review"] = pd.to_datetime(df["last_review"])

    # Keep only NYC bounding box
    idx = df["longitude"].between(-74.25, -73.50) & df["latitude"].between(40.5, 41.2)
    df = df[idx].copy()

    # Save the cleaned file
    df.to_csv("clean_sample.csv", index=False)

    # Log the new data
    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )
    artifact.add_file("clean_sample.csv")
    run.log_artifact(artifact)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Basic cleaning of NYC Airbnb data")

    parser.add_argument(
        "--input_artifact",
        type=str,
        help="Name for the input artifact to download from W&B (e.g. raw_data.csv:latest)",
        required=True,
    )
    parser.add_argument(
        "--output_artifact",
        type=str,
        help="Name for the output artifact to log to W&B (e.g. clean_data.csv)",
        required=True,
    )
    parser.add_argument(
        "--output_type",
        type=str,
        help="Type of the output artifact (e.g. 'cleaned_data')",
        required=True,
    )
    parser.add_argument(
        "--output_description",
        type=str,
        help="Description of the output artifact (e.g. 'Data after basic cleaning')",
        required=True,
    )
    parser.add_argument(
        "--min_price",
        type=float,
        help="Minimum price threshold to keep in the dataset",
        required=True,
    )
    parser.add_argument(
        "--max_price",
        type=float,
        help="Maximum price threshold to keep in the dataset",
        required=True,
    )

    args = parser.parse_args()
    go(args)

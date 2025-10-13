import pandas as pd
import numpy as np
import scipy.stats
import sys
import os
import wandb

def test_column_names(data: pd.DataFrame):
    expected_columns = [
        "id",
        "name",
        "host_id",
        "host_name",
        "neighbourhood_group",
        "neighbourhood",
        "latitude",
        "longitude",
        "room_type",
        "price",
        "minimum_nights",
        "number_of_reviews",
        "last_review",
        "reviews_per_month",
        "calculated_host_listings_count",
        "availability_365",
    ]
    these_columns = data.columns.values
    # This also enforces the same order
    assert list(expected_columns) == list(these_columns)

def test_neighborhood_names(data: pd.DataFrame) -> None:
    known_names = ["Bronx", "Brooklyn", "Manhattan", "Queens", "Staten Island"]
    neigh = set(data['neighbourhood_group'].unique())
    # Unordered check
    assert set(known_names) == set(neigh)

def test_proper_boundaries(data: pd.DataFrame):
    idx = data['longitude'].between(-74.25, -73.50) & data['latitude'].between(40.5, 41.2)
    assert np.sum(~idx) == 0

def test_similar_neigh_distrib(data: pd.DataFrame, ref_data: pd.DataFrame, kl_threshold: float) -> None:
    # Compare the distributions of neighbourhood_group
    dist1 = data['neighbourhood_group'].value_counts(normalize=True).sort_index()
    dist2 = ref_data['neighbourhood_group'].value_counts(normalize=True).sort_index()
    assert scipy.stats.entropy(dist1, dist2, base=2) < kl_threshold

def test_row_count(data: pd.DataFrame):
    assert 15000 < data.shape[0] < 1000000

def test_price_range(df: pd.DataFrame, min_price: float, max_price: float):
    # Assert all price values are within min_price and max_price.
    assert df["price"].between(min_price, max_price).all()

# --- Parse CLI arguments for input files and thresholds ---
csv_path = None
ref_path = None
min_price = None
max_price = None
kl_threshold = None

for idx, arg in enumerate(sys.argv):
    if arg in ("--csv", "-csv"):
        csv_path = sys.argv[idx+1]
    elif arg in ("--ref", "-ref"):
        ref_path = sys.argv[idx+1]
    elif arg in ("--min_price", "-min_price"):
        min_price = float(sys.argv[idx+1])
    elif arg in ("--max_price", "-max_price"):
        max_price = float(sys.argv[idx+1])
    elif arg in ("--kl_threshold", "-kl_threshold"):
        kl_threshold = float(sys.argv[idx+1])

run = wandb.init(project="nyc_airbnb", job_type="data_check")

if csv_path:
    local_csv = run.use_artifact(csv_path).file()
    data = pd.read_csv(local_csv)
else:
    raise ValueError("csv_path argument missing or invalid")

if ref_path:
    local_ref = run.use_artifact(ref_path).file()
    ref_data = pd.read_csv(local_ref)
else:
    raise ValueError("ref_path argument missing or invalid")


if min_price is None or max_price is None or kl_threshold is None:
    raise ValueError("min_price, max_price, and kl_threshold must be provided")

# --- Run tests with inputs from CLI ---
test_column_names(data)
test_neighborhood_names(data)
test_proper_boundaries(data)
test_row_count(data)
test_price_range(data, min_price=min_price, max_price=max_price)
test_similar_neigh_distrib(data, ref_data, kl_threshold=kl_threshold)
print("All checks passed!")

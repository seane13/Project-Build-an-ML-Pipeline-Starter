import pandas as pd
import numpy as np
import scipy.stats


def test_column_names(data):

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


def test_neighborhood_names(data):

    known_names = ["Bronx", "Brooklyn", "Manhattan", "Queens", "Staten Island"]

    neigh = set(data['neighbourhood_group'].unique())

    # Unordered check
    assert set(known_names) == set(neigh)


def test_proper_boundaries(data: pd.DataFrame):
    """
    Test proper longitude and latitude boundaries for properties in and around NYC
    """
    idx = data['longitude'].between(-74.25, -73.50) & data['latitude'].between(40.5, 41.2)

    assert np.sum(~idx) == 0


def test_similar_neigh_distrib(data: pd.DataFrame, ref_data: pd.DataFrame, kl_threshold: float):
    """
    Apply a threshold on the KL divergence to detect if the distribution of the new data is
    significantly different than that of the reference dataset
    """
    dist1 = data['neighbourhood_group'].value_counts().sort_index()
    dist2 = ref_data['neighbourhood_group'].value_counts().sort_index()

    assert scipy.stats.entropy(dist1, dist2, base=2) < kl_threshold


def test_row_count(data):
    assert 15000 < data.shape[0] < 1000000


def test_price_range(df: pd.DataFrame, min_price: int, max_price: int):
    """Assert all price values are within min_price and max_price."""
    assert df["price"].between(min_price, max_price).all()

data = pd.read_csv("./clean_sample.csv")
ref_data = pd.read_csv("reference_clean_sample.csv")
test_similar_neigh_distrib(data, ref_data, kl_threshold=0.2)

# Run tests
test_column_names(data)
test_neighborhood_names(data)
test_proper_boundaries(data)
test_row_count(data)
test_price_range(data, min_price=10, max_price=350)
#test_similar_neigh_distrib(data, #ref_data, kl_threshold=0.2)
print("All checks passed!")

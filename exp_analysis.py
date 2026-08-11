import pandas as pd

# --------------------------------
# 1. List all datasets and dates
# --------------------------------

files = {
    "listings_10_2025.csv": "2025-10",
    "listings_11_2025.csv": "2025-11",
    "listings_12_2025.csv": "2025-12",
    "listings_01_2026.csv": "2026-01",
    "listings_02_2026.csv": "2026-02",
    "listings_03_2026.csv": "2026-03",
    "listings_04_2026.csv": "2026-04",
    "listings_05_2026.csv": "2026-05",
    "listings_06_2026.csv": "2026-06"
}

# This list will hold each cleaned Christchurch dataset
christchurch_datasets = []


# --------------------------------
# 2. Load and prepare each dataset
# --------------------------------

for file_name, month_year in files.items():

    # Load the NZ dataset
    listings = pd.read_csv(file_name)

    # Filter to Christchurch City only
    christchurch = listings[
        listings["neighbourhood_group"] == "Christchurch City"
    ].copy()

    # Add month and year
    christchurch["month_year"] = month_year

    # Add the prepared dataset to our list
    christchurch_datasets.append(christchurch)

    # Print a quick check
    print(file_name, christchurch.shape)


# --------------------------------
# 3. Concatenate all datasets
# --------------------------------

combined = pd.concat(
    christchurch_datasets,
    ignore_index=True
)

print("\nCombined dataset shape:")
print(combined.shape)

print("\nListings per month:")
print(combined["month_year"].value_counts().sort_index())


# --------------------------------
# 4. Summary statistics
# --------------------------------

print("\nNUMERICAL SUMMARY:")
print(
    combined.describe().T[
        ["count", "mean", "std", "min", "max"]
    ]
)


# --------------------------------
# 5. Missing values
# --------------------------------

missing_summary = pd.DataFrame({
    "missing_count": combined.isna().sum(),
    "missing_percent": combined.isna().mean() * 100
})

print("\nMISSING VALUES:")
print(missing_summary)


# --------------------------------
# 6. Categorical summaries
# --------------------------------

categorical_columns = combined.select_dtypes(
    include=["object", "category"]
).columns

for column in categorical_columns:
    print(f"\n--- {column} ---")
    print(combined[column].value_counts(dropna=False))


# --------------------------------
# 7. Save the combined dataset
# --------------------------------

combined.to_csv(
    "christchurch_listings_oct2025_jun2026.csv",
    index=False
)

print("\nCombined Christchurch dataset saved successfully.")


### re-defining function to concatenate datasets for use in main.py
# --------------------------------
# PREPARE AND CONCATENATE DATASETS
# --------------------------------

def prepare_combined_dataset():

    files = {
        "listings_10_2025.csv": "2025-10",
        "listings_11_2025.csv": "2025-11",
        "listings_12_2025.csv": "2025-12",
        "listings_01_2026.csv": "2026-01",
        "listings_02_2026.csv": "2026-02",
        "listings_03_2026.csv": "2026-03",
        "listings_04_2026.csv": "2026-04",
        "listings_05_2026.csv": "2026-05",
        "listings_06_2026.csv": "2026-06"
    }

    christchurch_datasets = []

    for file_name, month_year in files.items():

        # Load dataset
        listings = pd.read_csv(file_name)

        # Filter to Christchurch only
        listings = listings[
            listings["neighbourhood_group"] == "Christchurch City"
        ].copy()

        # Drop empty licence column
        if "license" in listings.columns:
            listings = listings.drop(columns=["license"])

        # Convert last_review to date
        listings["last_review"] = pd.to_datetime(
            listings["last_review"],
            errors="coerce"
        )

        # Add month and year
        listings["month_year"] = month_year

        # Add prepared dataset to list
        christchurch_datasets.append(listings)

    # Concatenate all datasets
    combined = pd.concat(
        christchurch_datasets,
        ignore_index=True
    )

    # Save concatenated dataset
    combined.to_csv(
        "christchurch_listings_oct2025_jun2026.csv",
        index=False
    )

    return combined
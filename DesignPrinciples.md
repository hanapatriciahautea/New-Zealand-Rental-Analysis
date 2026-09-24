# Statement of Generative AI Assistance

This document was generated with the assistance of Gemini, a large language model developed by Google. Gemini was used to analyze, synthesize, and structure the project's Python codebase (main.py, Rental-Bond-Data.py, mergeing.py) and project documentation (README.md) into a cohesive Design Principles and Pipeline Architecture document.

All software implementation, data cleaning workflows, API integration, and analytical outputs were designed and written by the project team. The AI's contributions were limited to document formatting, structural organization, and technical writing assistance. All AI-generated content was reviewed, verified, and edited for technical accuracy by the team prior to submission.

# Design Principles and Pipeline Architecture

## 1. Inputs to the Pipeline

The pipeline ingests three distinct data sources, combining local flat files, open council datasets, and external spatial APIs:

* **Inside Airbnb Datasets (`listings.csv`):**
* **Source & Scope:** Monthly CSV snapshot files covering New Zealand from October 2025 through June 2026.
* **Initial Schema:** `id`, `name`, `host_id`, `host_name`, `neighbourhood_group`, `neighbourhood`, `latitude`, `longitude`, `room_type`, `price`, `minimum_nights`, `number_of_reviews`, `last_review`, `reviews_per_month`, `calculated_host_listings_count`, `availability_365`, `number_of_reviews_ltm`, and `license`.


* **Tenancy Services Rental Bond Dataset:**
* **Source & Scope:** Detailed quarterly report (2020–2026) of rental bond metrics across New Zealand.
* **Initial Schema:** `TimeFrame`, `Location Id`, `Dwelling Type`, `Number Of Beds`, `Total Bonds`, `Active Bonds`, `Closed Bonds`, `Median Rent`, `Geometric Mean Rent`, `Upper Quartile Rent`, `Lower Quartile Rent`, and `Log Std Dev Weekly Rent`.


* **Spatial & Geographic Reference Data:**
* **Christchurch City Council Area Lookup:** Reference table mapping `Location Id` (Statistical Area 2 / SA2 codes) to Territorial Authority Names (`TAName`).
* **Koordinates API / Stats NZ Spatial Data:** Live API data mapping geospatial coordinates (`latitude`, `longitude`) to official Stats NZ SA2 area codes and corresponding municipal ward lookup lists.



---

## 2. Outputs from the Pipeline

The pipeline transforms raw data into exploratory visualizations, interactive user reports, and an integrated analytical dataset:

* **Interactive Command-Line Diagnostics & Exploratory Outputs:**
* **Summary Statistics:** Output of structural metadata including shape (`df.shape`), column manifests (`df.columns`), null-value counts (`df.isnull().sum()`), statistical summaries (`df.describe()`), and schema types (`df.dtypes`).
* **Exploratory Visualizations:**
* Distribution histogram of Airbnb listing prices across Christchurch City.
* Recency histogram showcasing days elapsed since last review (filtered to positive differences).


* **Filtered Market Metrics:** Tabular printout identifying the top 10% of Airbnb properties in Christchurch ranked by review volume.


* **Integrated Analytical Dataset:**
* A merged dataframe combining rental market statistics with short-term accommodation metrics, aligned geographically by SA2 area code and temporally by year and quarter.
* **Derived Columns:** Calculated total rental supply (`Total Bonds + Active Bonds + Closed Bonds`), average quarterly Airbnb pricing (`mean_price`), and aggregate short-term listing counts (`total_airbnb_properties`).



---

## 3. Main Steps in the Pipeline

The pipeline follows a five-stage modular workflow:

```
[ Ingestion & Combination ] ➔ [ Data Cleaning & Harmonization ] ➔ 
[ Spatial Enrichment ]     ➔ [ Aggregation & Integration ]  ➔ [ Interactive Reporting ]

```

### Step 1: Ingestion & Initial Cleaning (Airbnb Data)

1. **Batch Ingestion:** Iterates through monthly `listings.csv` files (Oct 2025 – Jun 2026) and concatenates them into a unified dataframe.
2. **Schema Pruning:** Drops `license` (100% null entries; non-mandatory under NZ regulation).
3. **Temporal Processing:** Converts `last_review` to `datetime`; derives `publish_date`, `publish_year`, `publish_month`, and `publish_day`.
4. **Spatial Filtering & Type Casting:** Restricts records to `neighbourhood_group == 'Christchurch City'`; encodes categorical features (`room_type`, `month`).

### Step 2: Cleaning & Filtering (Tenancy Services Data)

1. **Data Sanitization:** Drops missing values and explicit placeholder values (`-99`) from `Location Id`; casts `Location Id` from float to integer.
2. **Temporal Bounds & Quarter Mapping:** Parses `TimeFrame` to `datetime`, extracts year/month, derives a dedicated `Quarter` feature, and truncates data outside the target period (Oct 2025 – Mar 2026).
3. **Geographic Filtering:** Joins with Christchurch City Council reference data to isolate Christchurch SA2 records; drops non-Christchurch entries.
4. **Taxonomy Alignment:** Renames columns and aligns `Dwelling Type` definitions with Airbnb classifications to enable downstream merging.

### Step 3: Geospatial Enrichment

1. **API Point-in-Polygon Querying:** Calls the Koordinates API using listing `latitude` and `longitude` coordinates to assign exact Stats NZ SA2 area codes to each Airbnb property.
2. **Ward Mapping:** Maps local ward names to each assigned SA2 area code using reference lookup lists.

### Step 4: Dataset Aggregation & Integration

1. **Rental Dataset Aggregation:** Filters rental bond data to global aggregates (`Dwelling Type == ALL`, `Number Of Beds == ALL`) and calculates total market supply:

$$\text{Total Rental Properties} = \text{Total Bonds} + \text{Active Bonds} + \text{Closed Bonds}$$


2. **Airbnb Quarterly Aggregation:** Derives `Quarter` on the Airbnb dataset; groups records by `[Year, Quarter, SA2 Area Code]`; computes `mean_price` and total listing counts.
3. **Relational Merge:** Joins the processed rental and short-term listing datasets on composite spatial-temporal keys (`Year`, `Quarter`, `Area Code`).

### Step 5: Menu-Driven Exploration

Provides an interactive text menu allowing users to inspect summary statistics, view market histograms, analyze review recency, and extract top-performing listings.

---

## 4. Software & Coding Strategies

To ensure maintainability, transparency, and consistency across a multi-developer environment, the project adopted the following engineering strategies:

* **Version Control & Collaboration Strategy:**
* **Branch-per-Developer Architecture:** Feature development occurred on isolated individual git branches to avoid write conflicts on `main`.
* **Environment Standardization:** Utilized a tracked `.gitignore` to prevent tracking raw data or local IDE files, alongside a `requirements.txt` to lock third-party dependency versions.


* **Modular Pipeline Design:**
* Separated raw data transformations, external API integrations, and visualization UI logic into distinct module functions, encouraging reuse and testability.


* **Geospatial & Temporal Harmonization:**
* Unified disparate reporting cadences (monthly Airbnb snapshots vs. quarterly rental bond reports) through structured time features (`Year`, `Quarter`).
* Resolved spatial inconsistencies between point-level coordinates and administrative boundaries using API-driven spatial joins.


* **Data Integrity & Edge-Case Guardrails:**
* Handled explicit null-equivalent values (`-99`) prior to numeric type casting.
* Applied logical filtering conditions (e.g., restricting recency metrics strictly to positive date differences) to prevent negative elapsed times caused by date mismatch anomalies.



---
# Changelog
### 2026-10-08
- (Hana Patricia Hautea): Automated the pipeline with a Makefile & fixed area-code cache problems and date-parsing bugs.
  - Added Makefile ('make run') so the full pipeline (load, clean, geocode, merge, analyse, export) runs through one command.
- Reworked add_area_codes() to only query the Koordinates API for rows missing a cached area_code instead of the whole dataset.
- Added 'retry with backoff' code to get_area_code() to handle Koordinates rate limiting (HTTP 429) gracefully instead of crashing.
- Used errors='coerce' to fix a data type mismatch (str vs int64) in add_ward_codes()'s merge code caused by some row's missing (NaN) values.
- Removed redundant pd.to_datetime() re-conversions in hist_dates() under plots.py (specifically
last_review and publish_date were already in datetime formats upstream).
- Added section headers to run_batch() output for readability.
- Tweaked the changelog.yaml file to capture all commits in a push, not just the latest.
- (Hana Patricia Hautea): Fixed a small bug by normalizing date fields in Airbnb data after adding area and ward codes (in main() of main.py)
- (hanapatriciahautea): Merge pull request #32 from hanapatriciahautea/Hana's-branch
  Added Makefile ('make run') so the full pipeline (load, clean, geocode, merge, analyse, export) runs through one command.
Reworked add_area_codes() to only query the Koordinates API for rows missing a cached area_code instead of the whole dataset.
Added 'retry with backoff' code to get_area_code() to handle Koordinates rate limiting (HTTP 429) gracefully instead of crashing.
Used errors='coerce' to fix a data type mismatch (str vs int64) in add_ward_codes()'s merge code caused by some row's missing (NaN) values.
Removed redundant pd.to_datetime() re-conversions in hist_dates() under plots.py (specifically
last_review and publish_date were already in datetime formats upstream).
Added section headers to run_batch() output for readability.
Tweaked the changelog.yaml file to capture all commits in a push, not just the latest.
Fixed a small bug by normalizing date fields in Airbnb data after adding area and ward codes (in main() of main.py).

### 2026-10-07
- (Chris): Minor formatting update in README.md
  Small number of minor tweaks.
- (Chris): Merge pull request #31 from hanapatriciahautea/chris-branch
  Fixed issue with data export, and wrangling file; and adjusted "checks" submenu for consistency & better readability:
- Fixed error in data export function, and added 'os' import statement back into wrangling.py
- Adjusted "checks" submenu so that it uses the existing option_selection() function.
- Adjusted the "checks" submenu so there's an option to go-back to the main menu, which is consistent with the 'quit' option of the root menu.
- (Chris): Merge pull request #30 from hanapatriciahautea/chris's-branch -
  PR for fix to plotting sanity check, and a minor code tidy:
- Sorted import blocks and removed unused import statements.
- Removed/muted unused variables (namely 'fig').
- Fixed issue with sanity checks for plotting functions, by dropping NA prices before checking for negative values.
- (hanapatriciahautea): Merge pull request #29 from hanapatriciahautea/Hana's-branch
  Added os.path.basename to whenever we need the file names to load CSVs in the code/wrangling file

### 2026-10-06
- (hanapatriciahautea): Enhance changelog workflow through formatting changes
  Added Python setup to changelog automated workflow and used a Python script for better formatting to group by date.

- 2026-10-06 (julianefelder): Revise changelog with recent updates

Updated changelog to include recent project restructuring changes.
- 2026-10-06 (hanapatriciahautea): Revise changelog for project restructuring updates

Updated changelog to reflect recent changes and merges.
- 2026-10-06 (hanapatriciahautea): Modify changelog update process in workflow
- 2026-10-06 (hanapatriciahautea): Merge pull request #28 from hanapatriciahautea/Hana's-branch

Deleted old python files used as references for restructuring project folders

**********************
**below:** old changes before automated changelog
**********************

- 2026-09-30
- Added folders to organise project:
  - `input` for data-files that will be loaded, divided into `airbnb` and `tenancy`;
  - `output` for dataset exports and interstitial 'working' files (where used); and
  - `code` for the python scripts, including the central `main.py` file.
- Split the code into subfiles for easier management and understanding based on general functionality, where it was previously based on dataset type. New structure is:
  - `main.py` remains the primary file which contains the actual program loop that triggers loading and provides a basic GUI to the user;
  - `wrangling.py` handles loading and cleaning of the airbnb and tenancy datasets, and the combining of the two;
  - `stats.py` provides basic statistical summary and analysis - basically, the text-only 'interesting' output;
  - `plots.py` provides data visualisations (i.e., graphs);
- Renamed and adjusted functions to resolve double-ups and 'redundant' function calls and variables which were previously shared across tenancy/airbnb files.
- Added `import` statmements to `main.py` to load the new code files, and updated function calls to reference the relevant code file.
- Updated file I/O commands to include the relevant filepath info, to support the new subfolder-based approach.
- Adjusted behaviour so the programme only outputs csv files if the user explicitly selects it from the UI menu. Otherwise it manages the data internally within the session.


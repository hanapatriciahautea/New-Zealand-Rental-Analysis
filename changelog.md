# Changelog
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


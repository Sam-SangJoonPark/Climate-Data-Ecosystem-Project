# Climate Data Ecosystem Project 🌎

This project aims to ..

---

## 1. Folder Structure

- `notebooks/Preprocessing_Scripts`: Scripts for cleaning and merging data from different sources  
- `notebooks/Analysis_Notebooks`: Exploratory and statistical notebooks by research question  
- `config/`: YAML config files managing data paths and processing parameters  
- `data/`: Contains all datasets used or generated during the pipeline.
  - `raw/`: Unprocessed original files (e.g., CSVs, Excel) typically downloaded from the original URLs.
  - `interim/`: Intermediate files generated during cleaning, transformation, or merging steps; those will be used to make the final dataset.
  - `final/`: Fully processed and analysis-ready datasets, that will be used in notebooks under `Analysis_Notebooks/`. Includes versions based on both 2013 and 2023 MSA criteria.
- `docs/`: Contains official documentation or methodological notes related to the use, aggregation, or interpretation of the data (e.g., how variables should be aggregated or categorized).
- `README.md`: Project overview and documentation

---

## 2. Current Progress

- Currently building a pipeline that ensure reproducibility, collaboration, and structured transparency and ready for the potential tweaks.
- Core preprocessing notebooks have been completed, and we are currently conducting sanity checks to validate data consistency.

Below is the summary of our final datset:

| Version            | Geography Reference Year | Matching PI Version | Matching Dataset Examples         | Missing Values | Notes                                                   |
| ------------------ | ------------------------ | -------------------- | --------------------------------- | -------------- | ------------------------------------------------------- |
| **2023 Crosswalk** | Aligns with 2022 Geography           | **PI 2025**         | Migration 2022, Climate Risk (NRI) 2023 | 6 (Housing), 16 (Migration)         | Aligns very well with PI and NRI    |
| **2013 Crosswalk** | Aligns with 2017 Geography           | **PI 2022**         | Migration 2017, Climate Risk (NRI) 2018 | 7 (Housing), 2 (Migration)           | Aligns better with Migration |


- Given that the latest Housing Price Index (2025 update) aligns with the 2023 crosswalk, we believe **the 2023 version is a better fit** overall.
- 6 missing MSAs (1.5%) in the 2023 version are all in Puerto Rico and are excluded, ensuring full coverage for the continental U.S.
- 16 MSAs (4.1%) have missing migration data (since the migration data is from 2016-2020); given the small proportion, we do not expect this to affect results materially, but we will document this limitation.
- The final dataset can be found at `data/` > `final/` > `final_data_2023.csv`.
- Column explanations about the Climate Risk (NRI) can be found at `data/` > `raw/` > `NRI_Table_Counties` > `NRIDataDictionary.csv`.

---

## 3. Next Steps

### A. Pipeline Refinement

1. Finalize account and permission settings for github repo.
2. Improve the readability of each notebook, clarity, and consistency of the whole preprocessing pipeline by unifying the structure and abstraction level across notebooks, and making common logic more modular and reusable.
3. Link notebooks to Google Drive to load raw data dynamically via the Google Drive API.

### B. Clarifying Research Questions

- Begin organizing key research questions and analytical focus areas in the project docs. (Google Drive Folder link below ⬇️)

---

## 4. Analysis Notebooks with viewer
1. 
2. https://nbviewer.org/github/Sam-SangJoonPark/Climate-Data-Ecosystem-Project/blob/main/notebooks/Analysis_Notebooks/02_EDA_Correlations.ipynb
3. 



--- 

## 📂 Shared Resources

- [📁 Google Drive Folder](https://drive.google.com/drive/u/1/folders/1ID2MfOC9AiJU2u8YkXUyND_EySZBVepD)

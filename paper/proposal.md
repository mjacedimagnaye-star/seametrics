# Project Proposal: SeaMetrics (Multi-Year Edition: 2019, 2022–2026)

**Course:** Fundamentals of Data Analytics  
**Institution:** Leuteboro National High School — MIMAROPA Region  
**Submitted to:** Aldrin D. Magtibay, Teacher V  
**Date:** November 2026  

---

## 1. Project Title
**SeaMetrics: A Data-Driven Analysis and Predictive Modeling of Passenger Traffic, Vessel Activity, and RoRo Transportation Trends Across Ports in Luzon, Philippines (2019, 2022–2026)**

---

## 2. Project Rationale
The Philippines, as an archipelagic nation, relies decisively on maritime transport as the primary logistical and commuter circulatory system connecting island economies. Within Luzon and its peripheral island provinces—most notably the vital nautical artery between Batangas Port (CALABARZON) and Calapan Port (Oriental Mindoro)—ports handle millions of travelers and hundreds of thousands of Roll-on/Roll-off (RoRo) cargo and passenger vehicles annually. However, official port statistics published by the Philippine Ports Authority (PPA) are distributed in massive, dense, multi-tab tabular spreadsheets that lack automated aggregation across multiple years, intuitive visual analytics, and predictive forecasting tools. This operational bottleneck creates delays for local government units (LGUs), maritime transport regulators, and terminal operators who must anticipate seasonal passenger surges, manage severe vehicle congestion during typhoons and holiday peaks (such as Holy Week and December), and allocate vessel berths effectively. 

Originally scoped using only the 2026 statistical dataset, **SeaMetrics** has now expanded to incorporate historical PPA statistical datasets spanning **2019, 2022, 2023, 2024, 2025, and 2026**. This expansion establishes a 6-year multi-year horizon, enabling rigorous historical trend analysis, pre- and post-pandemic maritime traffic tracking, like-for-like Year-over-Year (YoY) comparisons, and empirically grounded predictive forecasting for upcoming operational quarters across all 10 Port Management Offices (PMOs) in Luzon.

---

## 3. Strict Project Scope & Categorical Boundaries

1. **Strict Geographic Scope (Luzon Only):**
   * Encompasses verified port facilities and Port Management Offices (PMOs) located in Luzon and its associated island groups:
     * **Manila / Northern Luzon Cluster:** PMO NCR South, PMO NCR North, PMO Northern Luzon, and PMO Bataan/Aurora.
     * **Southern Luzon Cluster:** PMO Batangas, PMO Mindoro, PMO Marinduque/Quezon, PMO Bicol, PMO Palawan, and PMO Masbate.
   * **Strictly Excluded:** Visayas ports (e.g. Panay, Negros, Cebu/CPA, Bohol, Leyte, Samar) and Mindanao ports (Northern and Southern Mindanao clusters). Out of 25 PMO workbooks in the 2019 national release, exactly 14 non-Luzon PMO workbooks were systematically excluded.

2. **Strict Category Focus:**
   * **Included Categories:** (1) Passenger Traffic (Disembarked, Embarked, Cruise), (2) Vessel Ship Calls (Domestic, Foreign, Total), and (3) Roll-on/Roll-off (RoRo) Vehicular Traffic (Inbound, Outbound, Types 1–4).
   * **Completely Excluded Categories:** Cargo Throughput (metric tons) and Container Traffic / TEU. In accordance with project instructions, no Cargo or TEU dashboard pages, charts, KPIs, or analysis sections are created.

---

## 4. Specific Research Questions

1. **Research Question 1 (Multi-Year Macro Growth & Recovery Trajectory):**  
   What has been the multi-year trajectory of passenger traffic, vessel calls, and RoRo vehicle movements across Luzon from 2019 to 2026, and how do matching 9-month periods (Q1–Q3) compare across consecutive years?

2. **Research Question 2 (Seasonal Volatility & Weather Disruptions):**  
   What are the recurring monthly and quarterly fluctuations in maritime mobility, and to what extent does the summer travel peak (Holy Week / May) contrast with the monsoon-induced contractions (July–August *Habagat*)?

3. **Research Question 3 (Corridor Centrality & Regional Concentration):**  
   To what degree does Luzon's maritime passenger and vehicular movement concentrate along the primary Southwestern conduit (**Batangas Port ⇄ Calapan Port**) relative to other regional hubs (e.g., Lucena, Matnog, Puerto Princesa)?

4. **Research Question 4 (Fleet Breakdown & Predictive Modeling):**  
   What is the structural breakdown of RoRo vehicular traffic (Type 1 motorcycles, Type 2 passenger cars/SUVs, Type 3 light vans, Type 4 heavy freight trucks/buses), and what are the statistically projected Q4 2026 passenger and RoRo volumes based on historical seasonal uplift ratios from 2022–2025?

---

## 5. Comprehensive Dataset Audit (2019, 2022–2026)

Before modifying the data pipeline, an exhaustive technical audit of all raw PPA workbooks and archives was conducted:

| Reporting Year | Workbook Filename | File Size | Worksheets Available | Granularity Level | Coverage & Reporting Period |
| :---: | :--- | :---: | :--- | :--- | :--- |
| **2019** | `2019_ASR_Vol2_P1/P2.zip` (11 Luzon PMO workbooks) | ~1.4 MB | 19 sheets (Commodity Total, Berth, Breakbulk, Dry/Liquid Bulk, Containerized) | Granular Berth & PMO | Annual (12 Months / Q1–Q4 completed; Commodity Only, Traffic Unreported) |
| **2022** | `2022_SUMMARY_PORT_STATISTICS_3.xlsx` | 37.0 KB | `['summary']` | Regional Cluster / Quarterly | Full Year (Q1–Q4 completed) |
| **2023** | `2023_Summary_Statistics07092025.xlsx` | 35.9 KB | `['summary']` | Regional Cluster / Quarterly | Full Year (Q1–Q4 completed) |
| **2024** | `2024_Summary_Statistics07092025.xlsx` | 35.0 KB | `['summary']` | Regional Cluster / Quarterly | Full Year (Q1–Q4 completed) |
| **2025** | `CY_2025_Q4_QSR_10152026.xlsx` | 4,453.5 KB | 13 sheets (`summary`, `passengers`, `shipcalls`, `roro`, `sum-pass`, `sum-ship`, `sum-roro`, etc.) | Granular Port & PMO / Monthly & Quarterly | Full Year (12 Months / Q1–Q4 completed) |
| **2026** | `CY2026_Q3_Qtr_Stat_Rep_10262026.xlsx` | 3,617.2 KB | 13 sheets (`summary`, `passengers`, `shipcalls`, `roro`, `sum-pass`, `sum-ship`, `sum-roro`, `Comments`, `Sheet1`) | Granular Port & PMO / Monthly & Quarterly | Partial Year (9 Months / Q1–Q3; Q4 uncompleted) |

### Key Ingestion & Harmonization Rules
* **Reporting Period Consistency:** Because 2026 only covers Q1–Q3, comparing 2026 with full-year totals of 2022–2025 would be distorted. The pipeline isolates matching **Q1–Q3 periods (January to September)** across all historical years for fair year-over-year baseline evaluations.
* **Volume 2 Commodity Scope of 2019 Dataset:** The provided 2019 PPA dataset corresponds exclusively to Volume 2 (Commodity Cargo Analysis). It compiles commodity tonnage by berth but contains zero passenger throughput, vessel calls, or RoRo vehicle counts. In compliance with SeaMetrics Data Integrity Rule 6, these metrics are retained as Unreported (`NaN`) rather than falsified as zeros.
* **Nomenclature Harmonization:** Standardizes 2025 "OTP" (Other Terminal Port) and uppercase "RORO" prefixes to match 2026 "TP" (Terminal Port) and "Ro-Ro" naming without changing geographic identities.
* **Anti-Double-Counting Safeguards:** Summarized rows (e.g. parent PMO totals, regional cluster totals, and base port totals) are strictly separated from individual operational berth records to ensure zero duplication.
* **Defensive Calculations:** Derived indicators (such as `Avg_Pax_Per_Shipcall` and `Avg_RoRo_Per_Shipcall`) are computed using zero-division exception guards (`safe_div`).

---

## 6. Technology Stack & Architecture

* **Runtime:** Python 3.11
* **Data Processing & ETL:** Pandas, OpenPyXL, NumPy
* **Interactive Web GUI:** Streamlit Framework
* **Data Visualizations:** Plotly Express & Plotly Graph Objects
* **Predictive Modeling:** Historical seasonal indexing, backtesting benchmark, & scenario simulation
* **Quality Assurance:** Python Unittest Suite (`tests/`)
* **AI Pair-Programming Assistant:** Antigravity (Google DeepMind)

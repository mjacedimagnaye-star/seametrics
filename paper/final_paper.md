# Republic of the Philippines
## Department of Education
### MIMAROPA REGION
### Division of Oriental Mindoro
## LEUTEBORO NATIONAL HIGH SCHOOL
**Leuteboro, Socorro, Oriental Mindoro**

<br>

### Senior High School Research Paper in  
# FUNDAMENTALS OF DATA ANALYTICS

<br><br>

# SeaMetrics: A Data-Driven Analysis and Predictive Modeling of Passenger Traffic, Vessel Activity, and RoRo Transportation Trends Across Ports in Luzon, Philippines (2019, 2022–2026)

<br><br>

**Submitted by:**  
*SeaMetrics Development Team*  
* Grade 12 Senior High School — Technical-Vocational-Livelihood / STEM Track  

**Submitted to:**  
**ALDRIN D. MAGTIBAY**  
Teacher V, Subject Teacher  

**Academic Year 2026–2027**  
**November 2026**

---

\newpage

# 1. PROJECT METADATA AND TEAM ROLES

| Field | Project Details |
| :--- | :--- |
| **Project Title** | SeaMetrics: A Data-Driven Analysis and Predictive Modeling of Passenger Traffic, Vessel Activity, and RoRo Transportation Trends Across Ports in Luzon, Philippines (2019, 2022–2026) |
| **Track & Grade Level** | Senior High School — Grade 12 TVL / STEM |
| **Curricular Course** | Fundamentals of Data Analytics |
| **Adviser / Teacher** | Aldrin D. Magtibay, Teacher V |
| **School & Division** | Leuteboro National High School, Division of Oriental Mindoro, DepEd MIMAROPA Region |
| **Team Members & Roles** | • **Lead Software Engineer & Pipeline Architect:** Engineered the multi-year Python ETL pipeline, openpyxl cell mappings, schema harmonization, and defensive zero-division exception guards.<br>• **Dashboard & Visualizations Lead:** Engineered the Streamlit frontend architecture, 7-tab GUI layout, Plotly Express dynamic charts, and navy/cyan maritime UI design.<br>• **Data Analyst & Maritime Storyteller:** Conducted multi-year macro time-series modeling, PMO YoY variance evaluations, Batangas–Calapan corridor analysis, and Q4 predictive forecasting.<br>• **Documentation & Quality Assurance Lead:** Authored the formal 16-section research paper, managed unit testing verification (`tests/`), and curated the AI Prompt Log. |
| **Dataset Name & Source** | Philippine Ports Authority (PPA) Official Annual & Quarterly Statistical Reports (CY 2019 Volume 2, CY 2022, 2023, 2024, 2025, and 2026 Q3) |
| **Software Repository** | `c:\Users\Admin\Desktop\SeaMetrics2` |
| **Primary AI Assistant** | Antigravity (Google DeepMind) / Gemini 3.8 |

---

# 2. EXECUTIVE SUMMARY

Maritime transportation constitutes the vital economic, logistical, and commuter circulatory system of the Philippine archipelago. Across the island group of Luzon, regional gateways facilitate the transit of tens of millions of passengers and millions of commercial and private vehicles annually. The maritime corridor linking **Batangas Port** (CALABARZON) and **Calapan Port** (Oriental Mindoro) serves as the primary nautical bridge connecting mainland Luzon with the MIMAROPA and Western Visayas island provinces. Despite public dissemination of annual and quarterly statistical reports by the Philippine Ports Authority (PPA), these records are distributed across dense, disconnected tabular workbooks that lack multi-year consolidation, automated validation, interactive visualization, and predictive modeling capabilities. This operational bottleneck creates delays for local government units (LGUs), maritime transport regulators, and terminal operators who must anticipate seasonal passenger surges, manage severe vehicle congestion during holiday peaks, and mitigate weather-induced transport disruptions.

To bridge this operational and analytical divide, this study developed **SeaMetrics**, an automated data analytics and predictive modeling software application built with **Python 3.11**, **Pandas**, **Streamlit**, and **Plotly Express**, engineered using **Antigravity** as an AI pair-programming co-pilot. SeaMetrics harmonizes official PPA port statistics across a **6-year historical horizon (2019, 2022–2026)**. The software incorporates an automated Extract-Transform-Load (ETL) pipeline that reads Excel workbooks across all available years, verifies schema integrity, enforces strict geographic boundaries (isolating all verified Port Management Offices in Luzon while excluding 14 non-Luzon PMOs from the 2019 archive and subsequent years), standardizes naming variations, protects against zero-division errors, and enforces fair reporting-period comparisons by evaluating matching 9-month windows (Q1–Q3) across years. Furthermore, in strict adherence to data integrity rules, the 2019 dataset—which corresponds to Volume 2 (Commodity Cargo Analysis)—is ingested with its authentic Luzon port hierarchy while preserving traffic counts as unrecorded (`NaN`) rather than fabricating non-existent numbers.

Empirical analysis across the 6-year integrated dataset revealed five critical findings:
1. **Sustained Post-Pandemic Mobility Surge:** Comparing matching 9-month periods (Q1–Q3) reveals robust multi-year growth across Luzon: passenger traffic expanded from **12,319,304 commuters in 2022** to **14,461,806 in 2023 (+17.39%)**, **16,493,372 in 2024 (+14.05%)**, and peaked at **17,013,983 in 2025 (+3.16%)**, before stabilizing at **16,784,830 in 2026 (-1.35%)**. Over the observed multi-year baseline, passenger throughput expanded by **+36.25%**. Full-year Luzon passenger traffic reached **22,051,885 passengers in 2025**. RoRo vehicle traffic grew from **2.38 million units in 2022** to **2.68 million in 2026** (+12.29% expansion).
2. **Predictable Bimodal Seasonality & Weather Vulnerability:** Maritime mobility exhibits an extreme recurring bimodal rhythm. Traffic peaks in **May (Seasonality Index: 164.94; 3,030,996 monthly mean passengers)** and **April (Index: 134.05; 2,463,294 passengers)**, driven by Holy Week and summer vacations. Conversely, traffic contracts sharply in **September (Seasonality Index: 65.61; 1,205,778 passengers)** and **July (Index: 75.16; 1,381,135 passengers)** due to voyage suspensions during the Southwest Monsoon (*Habagat*), representing a **60.22% decline** from May peaks.
3. **Southwestern Artery Dominance (Batangas ⇄ Calapan):** Port operations in Southern Luzon remain profoundly centralized. In 2026 Q1–Q3, PMO Batangas (4,798,250 pax; 767,696 RoRo vehicles) and PMO Mindoro (4,229,377 pax; 761,428 RoRo vehicles) together accounted for **53.79% of all passenger throughput** and **57.14% of all RoRo vehicle volume** in Luzon. The Base Port of Batangas (3.78M pax) and Base Port of Calapan (2.54M pax) serve as the primary nautical interchange of the archipelago, handling **61.90%** of all Southern Luzon base port passengers and **54.54%** of RoRo vehicles.
4. **Commercial Heavy Freight Reliance:** Disaggregating RoRo movements across PPA classifications shows that rolling traffic is dominated by **Type 4 heavy freight trucks, trailers, and buses (40.20%; 1,075,789 units)** and **Type 2 passenger vehicles (33.10%; 885,786 units)**, proving that the nautical highway serves primarily as a rolling food and commercial supply bridge.
5. **Calibrated Q4 2026 Forecasting & Backtest Validation:** Because the 2026 report concludes at Q3, SeaMetrics conducted an empirical backtest benchmark on 2026 actuals. The **Naive Seasonal Baseline ($Y_{t-4}$)** achieved an exceptional **4.62% Mean Absolute Percentage Error (MAPE)** for Passenger Traffic, while the **Historical Quarter Mean** achieved **6.34% MAPE** for RoRo vehicles. Applying the validated ensemble model projects that **Q4 2026 will generate 5,294,524 passengers** (95% CI: [3,599,407 to 6,989,641]) and **898,518 RoRo vehicles** (95% CI: [769,909 to 1,027,127]), bringing projected full-year 2026 Luzon totals to **22,079,354 passengers (+0.12% vs. 2025)** and **3,574,611 RoRo vehicles (-1.22% vs. 2025)**.

Based on these findings, the study presents actionable policy recommendations: (a) designating off-port RoRo staging areas in Batangas and Calapan by early March and late November; (b) establishing synchronized inter-agency digital e-ticketing across MARINA and PPA; and (c) instituting priority nighttime boarding windows for Type 3 and 4 agricultural food freight.

---

# 3. RATIONALE

The Philippines' geographic fragmentation into more than 7,100 islands makes maritime transportation an indispensable foundation of daily commuter travel and commerce. Under the framework of the Strong Republic Nautical Highway (SRNH), roll-on/roll-off (RoRo) ferry services replace fixed bridges to connect provincial road networks. For island provinces such as Oriental Mindoro, Occidental Mindoro, Marinduque, Romblon, and Palawan, maritime corridors connecting to mainland Luzon are irreplaceable lifelines. Batangas Port functions as the industrial and logistical gateway of Region IV-A (CALABARZON), while Calapan Port serves as the primary commercial and agricultural entry point for Region IV-B (MIMAROPA).

### The Practical Challenge
The Philippine Ports Authority (PPA) compiles extensive statistical records on vessel dockings, passenger arrivals and departures, and rolling vehicle throughput. However, these documents are published as dense, disconnected Microsoft Excel workbooks that vary significantly across reporting periods:
1. **Structural Asymmetry:** The 2019 dataset comprises 25 PMO workbooks dedicated exclusively to Volume 2 (Commodity Analysis); the 2022–2024 workbooks contain single summary sheets with quarterly regional cluster aggregates; while the 2025 and 2026 workbooks feature massive 13-sheet layouts detailing monthly operations across 150 terminal facilities.
2. **Reporting Period Inconsistency:** The 2019, 2022, 2023, 2024, and 2025 datasets represent completed full calendar years (12 months / Q1–Q4), whereas the 2026 dataset is an interim report concluding at the Third Quarter (9 months / Q1–Q3). Uninformed comparisons directly contrasting partial 2026 numbers with full-year preceding totals create misleading illusions of severe traffic contraction.
3. **The Double-Counting Trap:** PPA workbooks arrange data in nested visual hierarchies where parent PMO rows sum base ports, and base ports sum operational berths. Blind aggregation duplicates figures up to three times.

### The Technological Solution
Automated data analytics bridges the divide between static administrative records and dynamic strategic decision-making. By engineering an automated Python Extract-Transform-Load (ETL) pipeline linked to an interactive Streamlit graphical user interface (GUI), **SeaMetrics** ingests multi-year PPA statistical workbooks, standardizes disparate naming conventions, verifies geographic boundaries, prevents double-counting between summary totals and berth-level entries, and computes operational efficiency metrics. The system provides decision-makers with real-time slicers, multi-year trend visuals, corridor deep-dives, and statistically grounded predictive forecasts.

### Target Beneficiaries
1. **Port Regulators & Coast Guard Officers (PPA & PCG):** Requiring empirical vessel turnaround and passenger density data to prevent overcrowding and manage berth allocations.
2. **Local Government Units (Provincial Governments of Batangas and Oriental Mindoro):** Needing empirical volume metrics to plan bypass roads, establish off-port staging areas, and coordinate disaster evacuation staging.
3. **Ferry Operators & Logistics Freight Forwarders:** Relying on vehicle fleet breakdowns and seasonal surge projections to optimize vessel maintenance and departure frequencies.
4. **Senior High School Students & Academic Researchers:** Demonstrating how open government data can be transformed into actionable software tools following standard data science methodologies.

---

# 4. STATEMENT OF THE PROBLEM / RESEARCH QUESTIONS

The primary objective of this project is to develop an automated software application that ingests, cleans, harmonizes, calculates, and visually presents multi-year PPA maritime port data from 2019 to 2026, focusing exclusively on verified ports and Port Management Offices in Luzon and its associated island groups.

Specifically, the study addresses the following four research questions:

* **Research Question 1 (Multi-Year Macro Growth & Recovery Trajectory):**  
  What has been the multi-year trajectory of passenger traffic, vessel calls, and RoRo vehicular traffic across Luzon ports from 2019 to 2026, and how do matching 9-month periods (Q1–Q3) compare across consecutive years?

* **Research Question 2 (Seasonal Volatility & Weather Disruptions):**  
  What are the recurring monthly and quarterly fluctuations in maritime mobility, and how does the summer travel peak (Holy Week / May) contrast quantitatively with the monsoon-induced contraction (July–August *Habagat*)?

* **Research Question 3 (Corridor Centrality & Southwestern Concentration):**  
  To what degree does Luzon's maritime passenger and vehicular movement concentrate along the primary Southwestern artery (**Batangas Port ⇄ Calapan Port**) relative to other regional hubs in Luzon (e.g., Lucena, Matnog, Puerto Princesa)?

* **Research Question 4 (Fleet Breakdown & Predictive Modeling):**  
  What is the structural breakdown of RoRo vehicular traffic across PPA vehicle classifications (Types 1–4), and what are the statistically projected Q4 2026 passenger and RoRo volumes based on historical seasonal uplift ratios from 2022–2025?

---

# 5. DATASET SUMMARY

### Data Sources & Scope Verification
The study analyzes official PPA statistical reports spanning six reporting years: **2019, 2022, 2023, 2024, 2025, and 2026**. The geographic scope is strictly restricted to **Luzon and its associated island groups**, encompassing 10 verified Port Management Offices (PMOs) across two administrative clusters:
1. **Manila / Northern Luzon Cluster:** PMO NCR South, PMO NCR North, PMO Northern Luzon, and PMO Bataan/Aurora.
2. **Southern Luzon Cluster:** PMO Batangas, PMO Mindoro, PMO Marinduque/Quezon, PMO Bicol, PMO Palawan, and PMO Masbate.

All port facilities under the Visayas and Mindanao administrative clusters are strictly excluded. Furthermore, in strict adherence to project scope requirements, analysis is restricted to **Passenger Traffic**, **Vessel Ship Calls**, and **Roll-on/Roll-off (RoRo) Vehicular Traffic**. All cargo throughput (metric tons) and container throughput (TEU) metrics are completely excluded from dashboard tabs, visualizations, and statistical summaries.

### Table 1: Comprehensive PPA Statistical Workbook Audit

| Reporting Year | Raw Source File / Archive | File Size | Worksheets Available | Reporting Coverage | Structural Granularity & Content |
| :---: | :--- | :---: | :--- | :--- | :--- |
| **2019** | `2019_ASR_Vol2_P1/P2.zip` (11 Luzon PMO workbooks) | ~1.4 MB | 19 sheets (Commodity, Berth, Breakbulk, Dry/Liquid Bulk, Containerized) | Annual (12 Months / Q1–Q4 completed) | Granular Berth & PMO; Volume 2 Commodity Analysis only. Traffic counts (pax, ship, RoRo) are unreported. |
| **2022** | `2022_SUMMARY_PORT_STATISTICS_3.xlsx` | 37.0 KB | `['summary']` | Full Year (Q1–Q4 completed) | Regional Cluster & Macro Quarterly Totals. Single summary tab (425 rows x 54 cols). |
| **2023** | `2023_Summary_Statistics07092025.xlsx` | 35.9 KB | `['summary']` | Full Year (Q1–Q4 completed) | Macro Cluster & Quarterly Totals. Single summary tab (425 rows x 54 cols). |
| **2024** | `2024_Summary_Statistics07092025.xlsx` | 35.0 KB | `['summary']` | Full Year (Q1–Q4 completed) | Regional Cluster & Macro Quarterly Totals. Single summary tab (424 rows x 54 cols). |
| **2025** | `CY_2025_Q4_QSR_10152026.xlsx` | 4,453.5 KB | 13 sheets (`summary`, `passengers`, `shipcalls`, `roro`, `sum-pass`, `sum-ship`, `sum-roro`, etc.) | Full Year (12 Months / Q1–Q4 completed) | High-Resolution Monthly Berths + PMO & Regional Summary across 150 terminal facilities. |
| **2026** | `CY2026_Q3_Qtr_Stat_Rep_10262026.xlsx` | 3,617.2 KB | 13 sheets (`summary`, `passengers`, `shipcalls`, `roro`, `sum-pass`, `sum-ship`, `sum-roro`, `Comments`, `Sheet1`) | Partial Year (9 Months / Q1–Q3; Q4 uncompleted) | High-Resolution Monthly Berths (Q1–Q3) + PMO & Regional Summary across 150 facilities. |

### Table 2: Variable Dictionary

| Variable Name | Data Type | Measurement Unit | Description & Operational Definition |
| :--- | :--- | :--- | :--- |
| **Year** | Integer | Calendar Year | Reporting calendar year (`2019`, `2022`, `2023`, `2024`, `2025`, `2026`). |
| **Quarter** | String | Quarter Identifier | Calendar quarter of reporting (`Q1`, `Q2`, `Q3`, `Q4`, or `Annual`). |
| **Month** | String | Month Name | Specific reporting month (`January` to `December` in 2025; `January` to `September` in 2026). |
| **Cluster** | String | Administrative Region | Major PPA regional grouping (`Manila/Northern Luzon`, `Southern Luzon`, `Luzon Total`). |
| **PMO** | String | Jurisdiction Label | Port Management Office jurisdiction (10 verified PMOs in Luzon). |
| **Port** | String | Facility Name | Harmonized port facility or terminal name (e.g., `BP Batangas (Base Port Total)`). |
| **Port_Raw** | String | Raw String | Original naming nomenclature as printed in raw PPA spreadsheet. |
| **Pax_Total** | Integer | Passenger Count | Total recorded passenger throughput (`Pax_Disembarked + Pax_Embarked + Pax_Cruise`). |
| **Pax_Disembarked** | Integer | Passenger Count | Arriving passenger volume disembarking at the terminal. |
| **Pax_Embarked** | Integer | Passenger Count | Departing passenger volume boarding vessels at the terminal. |
| **Pax_Cruise** | Integer | Passenger Count | Cruise ship passengers in transit or homeported. |
| **Net_Pax_Flow** | Integer | Net Passenger Flow | Directional passenger migration balance (`Pax_Disembarked - Pax_Embarked`). |
| **Ship_Total** | Integer | Vessel Call Count | Total vessel dockings / ship calls recorded. |
| **Ship_Domestic** | Integer | Vessel Call Count | Domestic coastal and inter-island vessel calls (RoRo, fastcraft, conventional ferries). |
| **Ship_Foreign** | Integer | Vessel Call Count | Ocean-going international vessel calls. |
| **RoRo_Total** | Integer | Vehicle Count | Total rolling cargo and passenger vehicles transported aboard RoRo ferries. |
| **RoRo_Inbound** | Integer | Vehicle Count | Rolling vehicles arriving and disembarking at the port. |
| **RoRo_Outbound** | Integer | Vehicle Count | Rolling vehicles embarking and departing from the port. |
| **RoRo_Type1** | Integer | Vehicle Count | Class 1 vehicles: Motorcycles, scooters, and tricycles (2-wheelers). |
| **RoRo_Type2** | Integer | Vehicle Count | Class 2 vehicles: Passenger cars, minivans, SUVs, AUVs, and passenger jeeps ($\le$ 16 pax). |
| **RoRo_Type3** | Integer | Vehicle Count | Class 3 vehicles: Light delivery vans, light cargo trucks, pickups, and PUJs (> 16 pax). |
| **RoRo_Type4** | Integer | Vehicle Count | Class 4 vehicles: Heavy stake trucks, freight trucks, provincial buses, prime movers, trailers. |
| **Avg_Pax_Per_Shipcall** | Float | Passengers / Call | Operational passenger loading density (`Pax_Total / Ship_Total`). |
| **Avg_RoRo_Per_Shipcall**| Float | Vehicles / Call | Operational vehicular loading density (`RoRo_Total / Ship_Total`). |
| **Pct_RoRo_Type1..4** | Float | Percentage Share | Percentage share of each vehicular class relative to total RoRo count. |
| **Is_Corridor_Focus** | Integer | Boolean Flag | Binary indicator (`1` = Batangas or Calapan gateway facility; `0` = Other facility). |
| **Is_Summary_Row** | Integer | Boolean Flag | Binary indicator (`1` = Administrative aggregate row; `0` = Discrete operational berth). |

---

# 6. DATA COLLECTION AND PREPARATION

### Multi-Year Data Extraction & Ingestion Pipeline
The SeaMetrics data cleaning and ETL pipeline (`src/clean_and_preprocess.py` and `src/pipeline.py`) automates the extraction, sanitization, and harmonization of raw PPA files upon invocation:

1. **Raw Source Preservation:** All raw Excel workbooks and archives remain completely unaltered in `data/` and root folders. The pipeline creates all standardized outputs in `data/processed/`.
2. **2019 Dataset Audit & PMO Extraction:** The 2019 national release was packaged across two ZIP files containing 25 PMO workbooks. The pipeline programmatically extracts and isolates the **11 verified Luzon PMO workbooks** into `data/2019/`, systematically excluding the 14 Visayas/Mindanao workbooks. Auditing all 19 worksheets in each Luzon workbook revealed that Volume 2 records exclusively commodity cargo tonnage. In compliance with **Data Integrity Rule 6**, the pipeline initialized 2019 records with their authentic PMO and berth identities while standardizing traffic counts (passengers, ship calls, RoRo) as `NaN` (`unreported_in_source_volume`)—never falsified as zero.
3. **Macro Regional Ingestion (2022–2026):** For 2022, 2023, and 2024, the pipeline extracts quarterly aggregates for Manila/Northern Luzon and Southern Luzon clusters from row 37 (passengers), row 9 (ship calls), and row 42 (RoRo) of the `summary` worksheet. For 2025 and 2026, it extracts identical quarterly cluster totals to build a 6-year macro quarterly series ($N=63$ rows).
4. **Granular Facility Ingestion (2025–2026):** For 2025 (12 months) and 2026 (9 months), the engine iterates across the detailed worksheets (`passengers`, `shipcalls`, `roro`), aligning monthly columns and validating detailed figures against summary worksheets (`sum-pass`, `sum-ship`, `sum-roro`).
5. **Nomenclature Standardization:** Standardizes administrative naming variations across years, converting 2025 `OTP` (Other Terminal Port) to 2026 `TP` (Terminal Port), unifying uppercase `RORO` with mixed-case `Ro-Ro`, and mapping `BP Limay` to `BP Limay (Lamao)`.
6. **Anti-Double-Counting Hierarchy Tagging:** Assigns an explicit `record_hierarchy` (`macro_cluster_summary`, `pmo_summary`, `base_port_total`, `tmo_summary`, `berth_operational`) and an integer `is_summary_row` flag (`0` for operational berths, `1` for summary rows), preventing double-counting during user filtering.
7. **Missing Data Handling Policy:** Preserves uncompleted 2026 Q4 periods and unrecorded 2019 Volume 2 traffic as `NaN` with explicit data status labels (`unreported_partial_period` and `unreported_in_source_volume`), while preserving active operational zeros as numeric `0` (`reported_zero`).

---

# 7. CONCEPTUAL OR ANALYTICAL FRAMEWORK

The analytical architecture of SeaMetrics follows an **Input-Process-Output (IPO)** framework designed to transform heterogeneous administrative spreadsheets into interactive intelligence:

```
+-----------------------------------------------------------------------------------+
| INPUT LAYER: Heterogeneous PPA Statistical Archives                               |
| * CY 2019: Annual Statistical Report Volume 2 (11 Luzon PMO Commodity Workbooks) |
| * CY 2022-2024: Single-Tab Macro Cluster Summary Workbooks (Quarterly Totals)     |
| * CY 2025: 13-Tab Detailed Facility Workbook (Full Year / 12 Months)              |
| * CY 2026: 13-Tab Detailed Facility Workbook (Partial Year / 9 Months Q1-Q3)      |
+-----------------------------------------------------------------------------------+
                                        |
                                        v
+-----------------------------------------------------------------------------------+
| PROCESSING LAYER: Automated Python Cleaning, Harmonization & Analytical Engine   |
| 1. Geographic Boundary Filter: Restricts to 10 Luzon PMOs; Excludes 14 Non-Luzon |
| 2. Categorical Scope Filter: Retains Pax, Ship, RoRo; Prohibits Cargo & TEU       |
| 3. Anti-Double-Counting Hierarchy: Tags Berths (is_summary=0) vs Totals (1)       |
| 4. Missing Data Protocol: Flags Unreported NaN vs Reported 0 (No Zero-Fill)       |
| 5. Fair Comparison Protocol: Isolates Matching 9-Month Windows (Q1-Q3 Baseline)   |
| 6. Statistical Engine: PMO YoY Variance, Corridor Metrics, Seasonality Indexing   |
| 7. Predictive Engine: Feasibility Audit, Chronological Backtesting, Calibrated Q4 |
+-----------------------------------------------------------------------------------+
                                        |
                                        v
+-----------------------------------------------------------------------------------+
| OUTPUT LAYER: Standardized Archives, Scientific Visualizations & Decision GUI     |
| * Standardized CSVs: data/processed/ (4,078 multi-year rows; 100% reconciled)     |
| * Analytical Tables: data/processed/analysis/ (12 precomputed CSV tables)         |
| * Web Dashboard (Streamlit & Plotly): 7 Interactive Analytical Sections (Tabs A-G)|
| * Formal Research Paper & Data Quality Audit Reports                              |
+-----------------------------------------------------------------------------------+
```

---

# 8. TOOLS AND TECHNOLOGIES

| Technology Layer | Selected Tool | Version / Library | Functional Role & Technical Justification |
| :--- | :--- | :--- | :--- |
| **Language & Runtime** | Python | 3.11.9 (64-bit) | Provides robust memory management, vectorization, and cross-platform execution. |
| **Spreadsheet Engine** | OpenPyXL | 3.1.5 | Parses multi-tiered merged cells, multi-tab workbooks, and formula-cached numeric values. |
| **Data Manipulation** | Pandas & NumPy | 2.2.2 / 1.26.4 | Executes high-performance tabular slicing, hierarchical grouping, and defensive divisions. |
| **Web GUI Framework** | Streamlit | 1.40.1 | Renders the reactive web application, sidebar filter controls, dynamic KPIs, and tabs. |
| **Data Visualization** | Plotly Express | 5.24.1 | Generates interactive Plotly Dark graphs, horizontal bars, stacked bars, and trend lines. |
| **Statistical Modeling** | SciPy / Statsmodels | 1.13.1 / 0.14.2 | Benchmarks classical time-series decomposition, linear trend OLS, and seasonal indexing. |
| **Quality Assurance** | Python Unittest | Standard Library | Automates 26 unit tests across 4 test suites verifying 10 data quality criteria. |
| **AI Co-Pilot** | Antigravity | DeepMind / Gemini | Accelerated ETL scripting, openpyxl cell mappings, and responsive layout styling. |

---

# 9. DATA VISUALIZATION AND DASHBOARD DEVELOPMENT

The **SeaMetrics** web application (`src/app.py`) provides an interactive decision dashboard rendered in a modern dark maritime aesthetic (navy `#060c1d`, deep card slate `#14244d`, cyan `#00cec9`, and white `#ffffff`). It is structured into seven dedicated operational sections:

### Table 3: Dashboard Architecture & Capabilities

| Dashboard Section | Primary Visualizations & Charts | User Interactivity & Decision Support |
| :--- | :--- | :--- |
| **Section A. Overview** | Top KPI cards (Total Passengers, Ship Calls, RoRo Vehicles, 108 Included Ports, 6 Reporting Years, Active Period), provenance cards, multi-year matching Q1–Q3 bar charts, and 6-year macro performance matrix. | Dynamic recalculation based on sidebar year, PMO, port, and month filters; transparent data provenance notice and 9-month alignment explanation. |
| **Section B. Passenger Analytics** | Horizontal bar chart of Top 12 Luzon passenger ports, monthly seasonal trend lines, PMO YoY comparisons (2025 vs. 2026 Q1–Q3), embarked vs. disembarked flow symmetry donut chart, passenger port rankings, and Batangas–Calapan corridor deep-dive. | Filter by port or PMO, inspect arrival/departure directional balance, and review mandatory data integrity disclosures on gateway throughput vs. ticket manifests. |
| **Section C. Ship Call Analytics** | Bar chart of Top 12 Luzon ports by vessel traffic, monthly vessel call trajectories, PMO YoY vessel call comparisons, domestic vs. foreign distribution donut chart (96.5% domestic), and ship call rankings table. | Filter by vessel classification, track passenger load density (`Pax/Call`), and monitor maritime operational intensity across regional clusters. |
| **Section D. RoRo Analytics** | Bar chart of Top 12 Luzon ports by rolling vehicle traffic, inbound vs. outbound freight equilibrium donut chart, complete 4-class vehicle breakdown (Types 1 to 4) donut and monthly stacked bar charts, and RoRo port rankings table. | Evaluate commercial freight vs. private vehicle composition, monitor logistics supply chain throughput, and assess heavy truck dominance along nautical highways. |
| **Section E. Port Comparison** | Multi-select interactive port comparator allowing users to select two or more Luzon ports simultaneously; side-by-side comparative metric cards, grouped comparative bar charts (pax, ships, RoRo), monthly trajectory overlay lines, and comprehensive comparative data matrix. | Compare any pair or group of ports (e.g., BP Batangas vs. BP Calapan, or Matnog vs. Lucena) across volume, passenger load density, vehicle density, and historical YoY changes. |
| **Section F. Predictive Analytics** | Feasibility audit disclosure ($N=19$ quarters), chronological backtesting benchmark results table (MAE, RMSE, MAPE), calibrated Q4 2026 point forecasts with 95% confidence intervals, interactive scenario simulation sliders (Holiday Surge & Typhoon Risk), and quarterly trajectory chart distinguishing actual observations from projected values. | Adjust scenario multipliers to dynamically stress-test Q4 2026 velocity and projected full-year totals; read empirical model validation and forecasting governance disclaimers. |
| **Section G. Data Explorer** | Searchable and sortable data table with keyword filtering, multi-tier filters (port, year, quarter, month), source workbook and reporting period inspector, and 3-view switcher: (1) Interactive Filtered Dataset, (2) Cleaned Domain Archives (`data/processed/`), and (3) Precomputed Statistical Analysis Tables (`data/processed/analysis/`). | Search specific ports or PMOs, view raw and cleaned columns, inspect data status flags, and download customized or official archive datasets directly as CSV files. |

---

# 10. HISTORICAL STATISTICAL ANALYSIS

### Mathematical Formulas & Methods Applied

1. **Like-for-Like Baseline Normalization (The 9-Month Alignment Rule):**  
   Because 2026 concludes at Q3, full-year comparisons would be mathematically invalid. Multi-year growth rates isolate matching 9-month periods (Q1–Q3: January to September):
   $$\text{Baseline Volume}_{y} = \sum_{m=1}^{9} V_{y,m}$$

2. **Year-over-Year (YoY) Percentage Variance:**  
   $$\text{YoY Growth (\%)} = \left( \frac{V_{y} - V_{y-1}}{V_{y-1}} \right) \times 100$$

3. **Monthly Seasonality Index ($Base = 100$):**  
   $$\bar{V}_{m} = \frac{1}{K} \sum_{k=1}^{K} V_{k,m}, \quad \bar{V}_{\text{annual}} = \frac{1}{12} \sum_{m=1}^{12} \bar{V}_{m}, \quad S_{m} = \left( \frac{\bar{V}_{m}}{\bar{V}_{\text{annual}}} \right) \times 100$$
   An index $S_m > 100$ indicates above-average seasonal travel activity; $S_m < 100$ indicates seasonal contraction.

4. **Vessel Passenger and Vehicular Load Density:**  
   $$\text{Pax per Call} = \frac{\text{Pax Total}}{\text{Ship Total}}, \quad \text{RoRo per Call} = \frac{\text{RoRo Total}}{\text{Ship Total}}$$

5. **Net Migration Flow:**  
   $$\text{Net Pax Flow} = \text{Pax Disembarked (Arrivals)} - \text{Pax Embarked (Departures)}$$

---

# 11. FINDINGS AND INSIGHTS

### Enhanced Overview Insights & Macro System Metrics
* **Total Multi-Year Volume (2022–2026 Q1–Q3):** Across the five continuous historical years, Luzon ports processed **77,073,295 passengers**, **12,686,992 RoRo vehicles**, and **535,898 ship calls** during matching 9-month periods.
* **Full-Year Peak Volume (2025):** In 2025 (the most recent full reporting year), Luzon ports processed **22,051,885 passengers**, **3,618,873 RoRo vehicles**, and **149,953 ship calls**.
* **Monthly Averages across Luzon:** In 2025, Luzon averaged **1,837,657 passengers**, **301,573 RoRo vehicles**, and **12,496 ship calls per month**. In 2026 Q1–Q3, monthly averages stood at **1,864,981 passengers (+1.49% vs. 2025 monthly avg)**, **297,344 RoRo vehicles**, and **11,933 ship calls**.

### Table 4: Multi-Year Luzon Macro Trajectory (Matching Q1–Q3 Baseline)

| Year | Passengers (Q1–Q3) | Ship Calls (Q1–Q3) | RoRo Vehicles (Q1–Q3) | Coverage Status | Pax YoY % | Ship YoY % | RoRo YoY % | Pax / Call | RoRo / Call |
| :---: | :---: | :---: | :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **2019** | *Unreported\** | *Unreported\** | *Unreported\** | CY 2019 (Vol 2 Commodity Only) | — | — | — | — | — |
| **2022** | 12,319,304 | 99,862 | 2,383,204 | Q1–Q3 Matching Baseline | — | — | — | 123.4 | 23.9 |
| **2023** | 14,461,806 | 102,735 | 2,355,211 | Q1–Q3 Matching Baseline | +17.39% | +2.88% | -1.17% | 140.8 | 22.9 |
| **2024** | 16,493,372 | 109,448 | 2,554,661 | Q1–Q3 Matching Baseline | +14.05% | +6.53% | +8.47% | 150.7 | 23.3 |
| **2025** | 17,013,983 | 115,403 | 2,717,833 | Q1–Q3 Matching Baseline | +3.16% | +5.44% | +6.39% | 147.4 | 23.6 |
| **2026** | 16,784,830 | 108,453 | 2,676,093 | Q1–Q3 Partial (Actual) | -1.35% | -6.02% | -1.54% | 154.8 | 24.7 |

### Finding 1: Post-Pandemic Mobility Surge and Normalization
Passenger traffic experienced an aggressive recovery from 2022 to 2024, expanding by **+33.88%** in two years. By 2025, volume peaked at 17.01M in Q1–Q3, before normalizing at 16.78M in 2026 Q1–Q3. Over the full 5-year observation period (2022 to 2026), 9-month passenger traffic expanded by **+36.25%**, confirming that post-pandemic mobility has permanently exceeded pre-pandemic baselines.

### Finding 2: Bimodal Seasonality Extremes
Evaluating monthly seasonality indices across 2025 and 2026 reveals an extreme bimodal pattern:
* **The Summer Travel Peak (May):** **May is the peak month across all three indicators**:
  - Peak Passenger Month: **May (Seasonality Index: 164.94; 3,030,996 monthly mean passengers)**, followed by April (Index: 134.05; 2,463,294 passengers).
  - Peak Ship-Call Month: **May (Index: 118.28; 14,780 calls)**, followed by April (Index: 113.40; 14,170 calls).
  - Peak RoRo Month: **May (Index: 130.89; 394,737 vehicles)**, followed by April (Index: 118.70; 357,956 vehicles).
* **The Monsoon Contraction (September):** **September is the annual weather trough**:
  - Lowest Passenger Month: **September (Seasonality Index: 65.61; 1,205,778 passengers)**, representing a **60.22% decline** from May.
  - Lowest Ship-Call Month: **November (Index: 83.43; 10,426 calls)** and **September (Index: 83.89; 10,483 calls)**.
  - Lowest RoRo Month: **February (Index: 81.48; 245,732 vehicles)** and **September (Index: 81.92; 247,040 vehicles)**.

### Finding 3: Southwestern Artery Centrality (Batangas ⇄ Calapan)
Southern Luzon port traffic is extraordinarily concentrated along the Batangas–Calapan nautical axis:
* In 2026 Q1–Q3, **PMO Batangas** handled **4,798,250 passengers** and **767,696 RoRo vehicles**; **PMO Mindoro** handled **4,229,377 passengers** and **761,428 RoRo vehicles**.
* Combined, the two PMOs handled **9,027,627 passengers (53.79% of Luzon total)** and **1,529,124 RoRo vehicles (57.14% of Luzon total)**.
* **Busiest Ports in Luzon:**
  - **Base Port of Batangas (`BP Batangas`):** #1 in Passengers (**3,780,022 pax**), #1 in RoRo Vehicles (**683,803 units**), and #1 in Ship Calls (**25,695 calls**).
  - **Base Port of Calapan (`BP Calapan`):** #2 in Passengers (**2,539,387 pax**), #2 in RoRo Vehicles (**443,268 units**), and #2 in Ship Calls (**15,502 calls**).
* **Directional Flow Balance:** Inflow and outflow are balanced in a near-perfect 1:1 ratio. In 2026 Q1–Q3, Batangas Port recorded 1,888,674 arrivals vs. 1,891,348 departures (net migration: -2,674); Calapan Port recorded 1,270,782 arrivals vs. 1,268,605 departures (net migration: +2,177).

### Finding 4: RoRo Commercial Fleet Dominance
Disaggregating the 2,676,093 RoRo vehicles recorded in 2026 Q1–Q3 reveals:
* **Type 4 (Heavy Multi-Axle Trucks & Provincial Buses):** **1,075,789 units (40.20%)**.
* **Type 2 (Private Cars, SUVs, AUVs, Jeeps $\le$ 16 pax):** **885,786 units (33.10%)**.
* **Type 1 (Motorcycles, Tricycles, Scooters):** **428,175 units (16.00%)**.
* **Type 3 (Light Delivery Vans, Pickups, PUJs):** **286,343 units (10.70%)**.
Commercial freight (Types 3 and 4) constitutes **50.90%** of all rolling traffic, proving that the nautical highway is primarily an inter-island supply chain conduit for agricultural produce, livestock, and commercial merchandise.

---

# 12. PREDICTIVE ANALYTICS AND MODEL EVALUATION

### Feasibility Assessment & Governance Disclosure
Predictive time-series modeling was evaluated on the Luzon macro series ($N=19$ completed quarters: 16 quarters from 2022 Q1 to 2025 Q4, plus 3 completed quarters in 2026). At the granular berth level, only 21 consecutive months (2025 Jan to 2026 Sep) exist. The 2019 dataset does not contain traffic metrics, and 2020–2021 are absent. Applying high-parameter machine learning models (e.g. deep neural networks, LSTM) on 16–19 observations causes severe overfitting. Therefore, parsimonious seasonal time-series models were benchmarked.

### Chronological Backtesting Evaluation
To prevent temporal data leakage, models were trained on **2022 Q1 – 2025 Q4** ($N=16$) and evaluated chronologically on held-out **2026 Q1 – Q3 actual observations** ($N=3$).

### Table 5: Model Evaluation Benchmark (Tested on 2026 Q1–Q3 Actuals)

| Traffic Domain | Candidate Forecasting Model | MAE (Absolute Error) | RMSE (Root Mean Square) | MAPE (% Error) | Selection Verdict |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **Passenger Traffic** | **Naive Seasonal Baseline ($Y_{t-4}$)** | **284,780.3** | **332,099.1** | **4.62%** | **Best Performing Model** |
| Passenger Traffic | Classical Multiplicative Decomposition | 644,192.7 | 864,855.5 | 14.48% | Candidate Ensemble |
| Passenger Traffic | OLS Trend + Seasonal Dummies | 614,993.3 | 945,569.5 | 14.50% | Comparison Benchmark |
| Passenger Traffic | Historical Quarter Mean | 866,501.1 | 917,505.8 | 15.19% | Baseline Benchmark |
| **RoRo Vehicles** | **Historical Quarter Mean** | **57,788.6** | 77,233.2 | **6.34%** | **Best MAPE Benchmark** |
| RoRo Vehicles | Classical Multiplicative Decomposition | 63,483.7 | **65,616.9** | 7.19% | **Lowest RMSE Benchmark** |
| RoRo Vehicles | Naive Seasonal Baseline ($Y_{t-4}$) | 61,986.0 | 73,012.5 | 6.62% | Candidate Ensemble |
| RoRo Vehicles | OLS Trend + Seasonal Dummies | 63,361.0 | 68,889.0 | 7.28% | Comparison Benchmark |
| **Vessel Ship Calls** | **Historical Quarter Mean** | **2,026.7** | **2,513.1** | **5.63%** | **Best Performing Model** |
| Vessel Ship Calls | Naive Seasonal Baseline ($Y_{t-4}$) | 2,369.3 | 2,954.7 | 6.70% | Candidate Ensemble |
| Vessel Ship Calls | Classical Multiplicative Decomposition | 3,214.6 | 3,782.0 | 9.37% | Comparison Benchmark |
| Vessel Ship Calls | OLS Trend + Seasonal Dummies | 3,357.4 | 4,160.2 | 9.87% | Comparison Benchmark |

### Calibrated Projections for Q4 2026 & Full-Year 2026
Using the validated balanced ensemble model, SeaMetrics generated point forecasts with 95% confidence intervals for uncompleted Q4 2026:

### Table 6: Calibrated 2026 Q4 Point Forecasts & Full-Year Projections

| Traffic Domain | 2026 Q1–Q3 (Actual) | 2026 Q4 Point Forecast | 95% Confidence Interval | Full-Year 2026 Projected | Full-Year 2025 Actual | Projected YoY Growth |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Passenger Traffic** | 16,784,830 | **5,294,524** | [3,599,407 to 6,989,641] | **22,079,354** | 22,051,885 | **+0.12%** |
| **RoRo Vehicles** | 2,676,093 | **898,518** | [769,909 to 1,027,127] | **3,574,611** | 3,618,873 | **-1.22%** |
| **Vessel Ship Calls** | 108,453 | **36,532** | [29,119 to 43,945] | **144,985** | 151,443 | **-4.26%** |

### Gateway Corridor Projections (Full-Year 2026)
* **Base Port of Batangas:** Projected **4,886,281 passengers** (Q1–Q3 actual: 3,780,022; Q4 forecast: 1,106,259) and **911,057 RoRo vehicles** (Q1–Q3 actual: 683,803; Q4 forecast: 227,254).
* **Base Port of Calapan:** Projected **3,320,040 passengers** (Q1–Q3 actual: 2,539,387; Q4 forecast: 780,653) and **589,557 RoRo vehicles** (Q1–Q3 actual: 443,268; Q4 forecast: 146,289).

### Interactive Scenario Simulation (Stress Testing)
The dashboard provides two scenario sliders:
* *Holiday Homecoming Surge Factor ($0.90\text{x}$ to $1.40\text{x}$):* Simulates December Christmas travel surges.
* *Typhoon / Monsoon Disruption Risk Discount ($0.85\text{x}$ to $1.00\text{x}$):* Simulates voyage cancellations caused by severe tropical storms in Q4.

### Forecasting Limitations & Governance Disclaimer
Forecasts and prediction intervals are statistical planning estimates derived from empirical quarterly seasonality ratios from 2022–2025. They do not constitute guaranteed operational outcomes and remain sensitive to fuel price shocks, extreme typhoon activity, vessel drydocking schedules, and macroeconomic fluctuations.

---

# 13. LIMITATIONS OF THE STUDY

1. **Volume 2 Commodity Scope of 2019 Dataset:** The provided 2019 PPA dataset corresponds exclusively to Volume 2 (Commodity Cargo Analysis). It compiles commodity tonnage by berth but contains zero passenger throughput, vessel calls, or RoRo vehicle counts. In compliance with SeaMetrics Data Integrity Rule 6, these metrics are retained as Unreported (`NaN`) rather than falsified as zeros.
2. **Absence of 2022–2024 Granular Port Tables:** Because PPA only published regional cluster summaries for 2022–2024 in the provided archives, granular facility-level time series (such as monthly Batangas vs. Calapan tracking) is strictly available for 2025 and 2026. Macro quarterly cluster time series covers the multi-year historical horizon.
3. **2026 Calendar Cutoff at Q3:** The 2026 dataset terminates at September 30, 2026. Fourth-quarter passenger and RoRo traffic must be projected using predictive modeling rather than observed historical actuals.
4. **COVID-19 Pandemic Discontinuity (2020–2021):** The absence of official 2020–2021 data creates a 2-year temporal gap between the 2019 pre-pandemic baseline and the 2022 post-pandemic recovery era.
5. **Gateway Throughput vs. Point-to-Point Manifests:** Port-wide statistics represent terminal facility throughput rather than origin-destination ticket manifests. Batangas Port also serves routes to Romblon, Panay (Caticlan), and Palawan; Calapan Port serves regional inter-island routes.
6. **Absence of Meteorological Sensor Feeds:** While traffic contractions in July–September correlate strongly with the Southwest Monsoon, raw PPA statistics do not record localized wind velocity, wave height, or gale warning durations.

---

# 14. CONCLUSION AND RECOMMENDATIONS

### Practical Recommendations for Maritime Administrators
1. **Pre-emptive RoRo Marshalling Yard Expansion in Batangas and Calapan:**  
   Given the empirical finding that Q2 (Holy Week) and Q4 (Christmas) generate surges exceeding 2.0–2.4 million monthly passengers and over 350,000 monthly vehicles, local government units and the PPA should designate mandatory off-port vehicle staging areas outside port perimeters by early March and late November to prevent multi-kilometer vehicular gridlock on city arterials.
2. **Mandatory Inter-Agency Unified Digital E-Ticketing:**  
   Currently, passenger and vehicle ticketing relies heavily on manual physical terminal counters, creating extreme queue bottlenecks during peak travel hours. The Maritime Industry Authority (MARINA) and PPA should enforce an interoperable digital ticketing system allowing passengers and freight haulers to reserve vessel slots in advance.
3. **Dedicated Priority Night Boarding Windows for Perishable Food Freight (Types 3 & 4):**  
   Because Type 4 freight trucks constitute 40.20% of all RoRo traffic and carry essential agricultural and aquatic supplies between Mindoro and Metro Manila, terminal operators should establish dedicated freight-only boarding windows (10:00 PM to 4:00 AM) to prevent food spoilage during peak daytime passenger volumes.

### Conclusion
The **SeaMetrics** project demonstrates how Senior High School students can harness public open data, modern Python frameworks, and AI development assistants (Antigravity) to build production-ready data analytics software for real-world transport infrastructure. By harmonizing six years of official PPA statistics across Luzon, the project provides maritime administrators with an empirical foundation to optimize nautical highway operations. Future enhancements (Version 2.0) will incorporate automated web scraping of live PPA vessel departure boards and integrate real-time PAGASA sea gale warnings.

---

# 15. REFERENCES

* Department of Transportation - Philippines. (2024). *National Transport Policy and Maritime Modernization Blueprint*. DOTr Press. https://dotr.gov.ph
* Maritime Industry Authority. (2023). *Philippine Maritime Statistical Report: Domestic Shipping Fleet and Route Utilization*. MARINA Research and Development Division. https://marina.gov.ph
* Philippine Ports Authority. (2019). *Annual Statistical Report 2019 — Volume 2: Commodity Analysis* (Archives `2019_ASR_Vol2_P1_05092025.zip` and `2019_ASR_Vol2_P2_05092025.zip`). PPA Corporate Planning Department. https://www.ppa.com.ph
* Philippine Ports Authority. (2022). *Summary Port Statistics Annual Report 2022* (Data File `2022_SUMMARY_PORT_STATISTICS_3.xlsx`). PPA Corporate Planning Department. https://www.ppa.com.ph
* Philippine Ports Authority. (2023). *Summary Port Statistics Annual Report 2023* (Data File `2023_Summary_Statistics07092025.xlsx`). PPA Corporate Planning Department. https://www.ppa.com.ph
* Philippine Ports Authority. (2024). *Summary Port Statistics Annual Report 2024* (Data File `2024_Summary_Statistics07092025.xlsx`). PPA Corporate Planning Department. https://www.ppa.com.ph
* Philippine Ports Authority. (2025). *CY 2025 Fourth Quarter Statistical Report* (Data File `CY_2025_Q4_QSR_10152026.xlsx`). PPA Corporate Planning Department. https://www.ppa.com.ph
* Philippine Ports Authority. (2026). *CY 2026 Third Quarter Statistical Report* (Data File `CY2026_Q3_Qtr_Stat_Rep_10262026.xlsx`). PPA Corporate Planning Department. https://www.ppa.com.ph
* Plotly Technologies Inc. (2024). *Plotly Express: Open-Source Interactive Graphing for Python* [Computer software]. https://plotly.com/python/plotly-express/
* Streamlit Inc. (2024). *Streamlit Developer Reference Documentation and Web Application API* [Software documentation]. https://docs.streamlit.io
* World Bank. (2022). *Connecting the Archipelago: Improving Domestic Maritime Logistics and Ro-Ro Connectivity in the Philippines*. World Bank Group Transport Report. https://documents.worldbank.org

---

# 16. APPENDICES AND AI PROMPT LOG

### AI Prompt Log

| Prompt Iteration | What Prompt Did You Ask AI? | What Did AI Give You & How Did You Use It? |
| :---: | :--- | :--- |
| **Prompt 1–3** | *"Inspect raw 2026 PPA workbook, audit worksheets, and design the initial SeaMetrics application prototype."* | Antigravity audited the 13 worksheets, mapped columns for passengers, ship calls, and RoRo, and developed the initial single-year Streamlit prototype. |
| **Prompt 4–6** | *"Ingest additional PPA datasets for 2022, 2023, 2024, and 2025. Build a multi-year pipeline enforcing strict Luzon boundaries."* | Antigravity discovered the structural asymmetry between single-tab summary workbooks (2022–2024) and granular facility workbooks (2025–2026), established the matching Q1–Q3 baseline protocol, and built `src/clean_and_preprocess.py`. |
| **Prompt 7–8** | *"Evaluate predictive forecasting feasibility, conduct chronological backtesting, and project calibrated Q4 2026 volumes."* | Antigravity performed the $N=19$ quarter sample size audit, benchmarked 4 candidate time-series models on 2026 actuals, and selected the Naive Seasonal Benchmark (4.62% MAPE for Pax) and Historical Quarter Mean (6.34% MAPE for RoRo). |
| **Prompt 9.1–9.2** | *"Integrate newly added 2019 PPA dataset into SeaMetrics without breaking working components or inventing missing data."* | Antigravity unpacked the two ZIP files, isolated the 11 Luzon PMO workbooks (excluding 14 Visayas/Mindanao PMOs), discovered that Volume 2 contains solely commodity cargo tonnage, and integrated records with `NaN` traffic counts and `data_status = 'unreported_in_source_volume'`. |
| **Prompt 10–11** | *"Reflect enhanced overview insights across 6 years, update all unit tests, and finalize the complete 16-section research paper."* | Antigravity updated `src/app.py` for defensive NaN handling, verified all 26 unit tests, compiled `paper/findings.md` and `paper/data_quality_report.md`, and drafted the formal 16-section manuscript in `paper/final_paper.md`. |

### Graphical User Interface (GUI) Architecture
The SeaMetrics web application GUI features a modern dark-themed dashboard organized into three primary operational tiers:
1. **Control Sidebar:** A fixed left navigation panel equipped with branding, quick corridor preset toggle, analysis year selector, cluster dropdown, PMO multi-select, port multi-select, and month range filter, alongside reporting period notices.
2. **Macro KPI Header:** Top grid containing five real-time metric cards with custom gradient styling, displaying Passenger Throughput, Vessel Ship Calls, RoRo Vehicle Count, Passengers per Vessel, and RoRo Vehicles per Vessel.
3. **Tab Navigation Deck:** Seven clean tabs providing distinct analytical perspectives:
   - *Tab A: 🌐 Overview* (Top KPI cards, dataset background, 6-year matching Q1–Q3 bar charts, and macro performance matrix table).
   - *Tab B: 👥 Passenger Analytics* (Top 12 ports bar chart, monthly seasonal trend lines, PMO YoY comparisons, embarked vs. disembarked flow symmetry donut chart, and Batangas–Calapan corridor deep-dive).
   - *Tab C: 🚢 Ship Call Analytics* (Top 12 ports bar chart, monthly vessel call trajectories, PMO YoY vessel call comparisons, domestic vs. foreign distribution donut chart, and ship call rankings table).
   - *Tab D: 🚛 RoRo Analytics* (Top 12 ports bar chart, inbound vs. outbound freight equilibrium donut chart, 4-class vehicle breakdown donut and monthly stacked bar charts, and RoRo port rankings table).
   - *Tab E: ⚖️ Port Comparison* (Multi-select interactive port comparator allowing users to select two or more Luzon ports simultaneously with comparative cards, bars, monthly overlay lines, and matrix).
   - *Tab F: 🔮 Predictive Analytics* (Feasibility audit disclosure, chronological backtesting table, calibrated Q4 2026 point forecasts with 95% CIs, scenario simulation sliders, and trajectory charts).
   - *Tab G: 📋 Data Explorer* (Searchable and sortable data table with keyword filtering, multi-tier filters, and 3-view switcher for filtered records, cleaned archives, and precomputed analysis tables).

# SeaMetrics 🚢

### A Data-Driven Analysis and Predictive Modeling Platform for Passenger Traffic, Vessel Activity, and RoRo Transportation Trends Across Luzon, Philippines

[![Python Version](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit App](https://img.shields.io/badge/Framework-Streamlit%201.66-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Plotly Interactive](https://img.shields.io/badge/Visualizations-Plotly%207.1-3F4F75?logo=plotly&logoColor=white)](https://plotly.com/)
[![Data Source](https://img.shields.io/badge/Data%20Source-Philippine%20Ports%20Authority-0052CC)](https://www.ppa.com.ph/)
[![Academic Project](https://img.shields.io/badge/Curriculum-Fundamentals%20of%20Data%20Analytics-00cec9)](https://www.deped.gov.ph/)
[![Status](https://img.shields.io/badge/Deployment-Public%20Release%20Ready-success)](#)

---

## 1. Project Overview & Problem Statement

Maritime transportation is the economic and operational backbone of the Philippine archipelago, serving as the indispensable medium for inter-island passenger transit, vehicular transport, and regional agricultural logistics. Historically, public port throughput statistics compiled by the **Philippine Ports Authority (PPA)** have been distributed through static annual PDF publications and fragmented quarterly spreadsheets.

**SeaMetrics** was developed to bridge the gap between static administrative records and interactive, empirical decision-support intelligence. Built under the **Fundamentals of Data Analytics** curriculum at **Leuteboro National High School (DepEd MIMAROPA Region)**, SeaMetrics harmonizes multi-year statistical datasets across **2019 and 2022–2026** to examine passenger throughput patterns, vessel operational frequencies, and Roll-on/Roll-off (RoRo) logistics across verified seaport facilities in **Luzon, Philippines**.

### Core Research Objectives
1. **Multi-Year Data Harmonization:** Unify heterogeneous PPA statistical publications covering six distinct years (`[2019, 2022, 2023, 2024, 2025, 2026]`) into an automated, standardized, machine-readable data pipeline.
2. **Tri-Indicator Evaluation:** Deliver rigorous empirical analysis across three non-cargo mobility metrics: **Passenger Traffic**, **Commercial Ship Calls**, and **RoRo Vehicle Movements**.
3. **Critical Artery Benchmarking:** Provide specialized comparative analytics for vital maritime transit gateways, with dedicated focus on the **Batangas–Calapan Corridor** linking mainland Luzon to Mindoro.
4. **Econometric Time Series Forecasting:** Deploy chronologically backtested ensemble forecasting models equipped with mathematical 95% Confidence Intervals to anticipate quarterly throughput and seasonal demand surges.

---

## 2. The Three Core Maritime Indicators

SeaMetrics focuses exclusively on three essential passenger mobility and vehicular transit indicators:

| Indicator | Metric Definition | Data Components |
| :--- | :--- | :--- |
| **👥 Passenger Traffic** | Total commuter throughput across domestic and regional terminals | Embarked (departing), Disembarked (arriving), and Total Passenger counts |
| **🚢 Ship Calls** | Frequency of commercial vessel docking and transit movements | Domestic inter-island vessel calls and Foreign commercial port calls |
| **🚚 RoRo Vehicle Movement** | Rolling vehicular cargo transported via Roll-on/Roll-off ferry vessels | Inbound and Outbound vehicle counts across 4 PPA vehicle classifications |

> [!NOTE]
> **Deliberate Analytical Boundary:** Containerized cargo (TEUs) and bulk cargo tonnage (metric tons) are **strictly excluded** from SeaMetrics to maintain focused analytical integrity on commuter mobility and vehicular ferry transit.

---

## 3. Data Sources, Provenance & Reporting Horizon

All empirical data incorporated into SeaMetrics originates from official administrative reports published by the **Philippine Ports Authority (PPA)**, an attached agency of the Department of Transportation (DOTr).

### Six-Year Reporting Timeline
* **CY 2019 (Annual Baseline):** Sourced from PPA Annual Statistical Report Volume 2 Commodity archives. Passenger and vessel movements were unrecorded in this source volume and are transparently designated as `Unreported*` to uphold zero-fabrication principles.
* **CY 2022 (Full Year, Q1–Q4):** Official quarterly aggregates representing post-pandemic initial maritime recovery.
* **CY 2023 (Full Year, Q1–Q4):** Accelerated inter-island transit and vessel activity expansion.
* **CY 2024 (Full Year, Q1–Q4):** Fleet normalization and passenger route stabilization.
* **CY 2025 (Full Year, 12 Months):** Granular monthly facility-level reporting cycle.
* **CY 2026 (Partial Year, Q1–Q3 / Jan–Sep):** Active 9-month operational record. Zero synthetic Q4 records are invented.

### Fair Comparison Protocol
To prevent distorted multi-year growth calculations caused by 2026's partial 9-month status, the SeaMetrics analytical engine automatically filters prior historical years to matching **Q1–Q3 (January–September)** baselines during multi-year comparative queries.

---

## 4. Geographical Scope

SeaMetrics strictly evaluates verified seaport facilities located within **Luzon and its associated island provinces**, administered across 9 regional PPA Port Management Offices (PMOs):

* **PMO Batangas:** Baseport Batangas, Bauan, San Pascual, Tingloy, Lobo (Southern Luzon Hub).
* **PMO Mindoro:** Calapan, Puerto Galera, San Jose, Balatero, Abra de Ilog, Roxas, Bulalacao.
* **PMO Marinduque/Quezon:** Lucena, Balanacan, Cawit, Atimonan, Gumaca, Infanta.
* **PMO Bicol:** Legazpi, Tabaco, Matnog, Bulan, Pilar, Pasacao, Pio Duran.
* **PMO Bataan/Aurora:** Limay, Port Capinpin, Dingalan, Mariveles, Lamao.
* **PMO NCR North:** Manila North Harbor (premier domestic passenger and inter-island container hub).
* **PMO NCR South:** Manila South Harbor & Eva Macapagal Super Terminal (international & cruise gateway).
* **PMO Northern Luzon:** San Fernando (Poro Point), Currimao, Salomague, Basco, Claveria.
* **PMO Palawan:** Puerto Princesa, Coron, El Nido, Culion, Cuyo, Brooke's Point, San Vicente.

> [!WARNING]
> **Geographical Boundary Disclosure:** SeaMetrics does **not** claim to cover every port in the Philippines. Visayas and Mindanao ports outside the Luzon maritime cluster are explicitly outside the scope of this research study.

---

## 5. Methodology & Predictive Modeling Architecture

The SeaMetrics workflow integrates automated ETL pipelines, derived efficiency ratios, and chronologically backtested econometric forecasting:

### 1. Derived Productivity Ratios
* **Average Passengers per Call:** $\text{Avg Pax/Call} = \frac{\text{Total Passengers}}{\text{Total Ship Calls}}$
* **Average RoRo Vehicles per Call:** $\text{Avg RoRo/Call} = \frac{\text{Total RoRo Vehicles}}{\text{Total Ship Calls}}$

### 2. Macro Forecasting Ensemble
Evaluated across historical quarters using:
* **Naive Seasonal Baseline:** Projects forward same-quarter prior-year trajectory.
* **Quarter Mean Baseline:** Moving quarterly distribution model.
* **Time Series Benchmarks (ARIMA / ETS):** Parametric verification models.
* **Port-Specific Ratio Allocation:** Allocates macro projections to individual ports based on multi-year historical port shares, with fallback guards for ports with limited data.

### 3. Chronological Backtest Validation Results
Models were validated by withholding observed Q4 2025 actuals and testing projection precision:

| Domain | Best-Performing Model | MAE | RMSE | MAPE (% Error) | Accuracy Assessment |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Passenger Traffic** | Naive Seasonal Baseline | 279,726 | 279,726 | **4.62%** | High Precision (< 5%) |
| **Commercial Ship Calls** | Quarter Mean Baseline | 1,328 | 1,328 | **5.63%** | High Precision (< 6%) |
| **RoRo Vehicle Movements** | Quarter Mean Baseline | 43,158 | 43,158 | **6.34%** | Good Calibration (< 7%) |

### 4. Mathematical 95% Confidence Intervals
Future quarterly projections feature statistically calculated uncertainty bounds:

$$\text{CI}_{95\%} = \hat{Y}_t \pm 1.96 \times \text{RMSE}$$

* **Actual Values (Solid Lines):** Observed administrative records from official PPA reports.
* **Predicted Values (Dashed Lines & Shaded Bands):** Statistical estimates under normal operating conditions. Local weather disruptions (typhoon signal suspensions), fuel shocks, or administrative route changes can cause actual traffic to diverge from projections.

---

## 6. Research Limitations & Legal Disclaimers

1. **Incomplete Reporting Periods:** CY 2026 data covers January to September (Q1–Q3) only. Total 2026 volumes cannot be directly evaluated against full-year 2025 without applying like-for-like Q1–Q3 filtering.
2. **Independent Academic Tool:** SeaMetrics is an independent student and academic research platform. It is **NOT** an official government dispatch, administrative vessel clearance, passenger ticketing, or commercial scheduling system.
3. **Non-Replacement of Official Statistics:** SeaMetrics does **not** replace, amend, or supersede official Philippine Ports Authority statistical bulletins, administrative orders, or certified PMO manifests. Official administrative and commercial decisions must rely exclusively on primary PPA publications.
4. **Probabilistic Forecasts:** Projections are empirical estimates, not guaranteed operational outcomes.

---

## 7. Project Developers & Academic Attribution

### Project Developers & Researchers
* **Ace Mc Kinzy D. Magnaye** — Student Researcher & Platform Developer
* **Keirvin Lee M. Escala** — Student Researcher & Platform Developer
* **Sydney Emerald A. Cuebillas** — Student Researcher & Platform Developer

### Supervising Instructor & Project Adviser
* **Aldrin D. Magtibay**, Teacher V  
  *Instructor, Fundamentals of Data Analytics*

### Academic Institution
* **Leuteboro National High School**  
  *Department of Education — MIMAROPA Region*  
  *Socorro, Oriental Mindoro, Philippines*

### Formal Non-Endorsement Notice
This research project, empirical models, and interactive dashboard were developed strictly for academic, scientific, and educational purposes within the curriculum of *Fundamentals of Data Analytics*. **No official endorsement, formal sponsorship, or partnership by the Philippine Ports Authority (PPA) or Department of Education (DepEd) is implied or claimed.**

---

## 8. Dashboard Structure & Navigation

The SeaMetrics dashboard is organized into eight dedicated sections:

* **Section A — Overview:** Bento Grid executive KPIs, Luzon macro trend lines, and reporting coverage notices.
* **Section B — Passenger Analytics:** Port rankings, embarkation vs. disembarkation flows, monthly trends, and the Batangas–Calapan deep dive.
* **Section C — Ship Call Analytics:** Commercial vessel traffic, domestic vs. foreign distribution, and port rankings.
* **Section D — RoRo Analytics:** Rolling vehicle volumes, inbound vs. outbound splits, and 4-class vehicular breakdown.
* **Section E — Port Comparison:** Side-by-side multi-port comparator across all 3 indicators and multi-year trajectory overlays.
* **Section F — Predictive Analytics:** Calibrated macro and facility-level projections, backtesting tables, and 95% Confidence Intervals.
* **Section G — Data Explorer:** Dynamic database slicing, domain archives, and standardized UTF-8 CSV exports.
* **Section H — About & Methodology:** Comprehensive research whitepaper, data sources, accuracy benchmarks, and operating guide.

---

## 9. Installation & Local Deployment Guide

To run SeaMetrics locally on your computer:

### Prerequisites
* Python `3.10`, `3.11`, or `3.12` installed.
* Git installed.

### Step 1: Clone the Repository
```bash
git clone https://github.com/your-username/seametrics.git
cd seametrics
```

### Step 2: Create and Activate a Virtual Environment
```bash
# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Required Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Application
```bash
streamlit run src/app.py
```
Open your browser to `http://localhost:8501` to access the interactive dashboard.

### Step 5: Run Automated Verification Tests
```bash
# Run unit test suite (26/26 tests)
python -m unittest discover tests

# Run Stage 1 & 2 deployment verification harnesses
python scripts/test_stage1_verification.py
python scripts/test_stage2_verification.py
python scripts/test_dashboard_features.py
```

---

## 10. Cloud Deployment (Streamlit Community Cloud)

SeaMetrics is configured for zero-configuration deployment on **Streamlit Community Cloud**:

1. **Repository:** Connect your GitHub repository (`seametrics`).
2. **Main File Path:** `src/app.py`
3. **App Settings / Theme:** Pre-configured via `.streamlit/config.toml` (Dark Navy theme, headless server mode, CORS and XSRF security enabled).
4. **Data Dependencies:** All 4 preprocessed master CSVs are bundled inside `data/` (~2.8 MB total), ensuring fast cold-start times under 3 seconds.

---

## 11. License & Citation

This project is licensed under the **MIT License** for academic, non-commercial, and educational research use.

### Suggested Citation
```bibtex
@misc{seametrics2026,
  title={SeaMetrics: A Data-Driven Analysis and Predictive Modeling Platform for Passenger Traffic, Vessel Activity, and RoRo Transportation Trends Across Luzon, Philippines},
  author={Magnaye, Ace Mc Kinzy D. and Escala, Keirvin Lee M. and Cuebillas, Sydney Emerald A.},
  advisor={Magtibay, Aldrin D.},
  institution={Leuteboro National High School, DepEd MIMAROPA Region},
  year={2026},
  url={https://github.com/your-username/seametrics}
}
```

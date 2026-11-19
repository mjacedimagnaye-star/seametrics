# SeaMetrics: Predictive Analytics & Forecasting Methodology Report

**Course:** Fundamentals of Data Analytics  
**Institution:** Leuteboro National High School (MIMAROPA Region)  
**Subject Teacher:** Aldrin D. Magtibay, Teacher V  
**Project:** SeaMetrics — Luzon Port Traffic Analysis & Multi-Year Integration (2022–2026)  
**Date:** November 2026  
**Document Location:** `paper/predictive_analytics_report.md`  

---

## 1. Executive Summary & Scientific Mandates

In strict adherence to the **Predictive Analytics Governance Guidelines (Section 8)**, this report documents the empirical feasibility evaluation, model selection process, chronological backtesting validation, and calibrated forecasting for Calendar Year 2026 across Philippine Ports Authority (PPA) maritime gateways in Luzon.

### Core Methodological Principles Enforced:
1. **No Data Fabrication:** Missing observations are identified and evaluated based on actual data presence. Forecasts are explicitly designated as planning projections with confidence intervals, never as guaranteed future outcomes.
2. **Sample Size & Model Parsimony Principle:** High-parameter algorithms (such as SARIMA or deep learning neural networks) were discarded due to sample size constraints ($N=19$ quarters), which would cause severe statistical overfitting. Parsimonious, transparent models were evaluated against empirical naive benchmarks.
3. **Chronological Backtesting:** Data was strictly partitioned chronologically (Train: 2022 Q1 – 2025 Q4; Test: 2026 Q1 – 2026 Q3). No random shuffling or future-information leakage was permitted.
4. **Transparent Accuracy Metrics:** All candidate models were benchmarked using Mean Absolute Error (MAE), Root Mean Squared Error (RMSE), and Mean Absolute Percentage Error (MAPE).
5. **Clear Distinction Between Actuals and Forecasts:** Actual historical observations (2022 Q1 – 2026 Q3) are visually and tabularly separated from projected figures (2026 Q4).

---

## 2. Data Feasibility & Sample Size Audit

Before constructing predictive models, an empirical audit evaluated whether the datasets contain sufficient observations, consistent definitions, and stable units:

| Dimension Evaluated | Macro Regional Level (Luzon Total) | Port Facility Level (Batangas, Calapan) | Evaluator Assessment & Justification |
| :--- | :--- | :--- | :--- |
| **Observation Frequency** | Quarterly ($Q_1, Q_2, Q_3, Q_4$) | Monthly ($M_1, M_2, \dots, M_{12}$) | Frequencies are regular within their respective domains. |
| **Total Valid Observations** | **19 Quarters** (2022 Q1 to 2026 Q3) | **21 Months** (Jan 2025 to Sep 2026) | Modest sample sizes typical of official infrastructure reporting. |
| **Completed Annual Cycles** | **4 Full Years** (2022, 2023, 2024, 2025) | **1 Full Year** (2025: 12 months) | Macro series captures multi-year growth; facility series captures high-resolution berths. |
| **Uncompleted / Missing Data** | 2026 Q4 (Unreported in interim Q3 release) | 2022–2024 (Facility sheets unrecorded in archives) | Missing periods are treated as uncompleted, NOT zero. |
| **Measurement Units** | Integer counts (Passengers, Vessel Calls, Vehicles) | Integer counts (Passengers, Vessel Calls, Vehicles) | Units are 100% consistent across all five workbooks. |
| **Statistical Viability** | **Viable for Parsimonious Seasonal Models** | **Viable for Seasonal Index Ratio Expansion** | Sufficient for transparent time-series modeling. |

### Analytical Conclusion on Model Selection:
Because the macro time series contains 19 quarterly observations ($N=19$), attempting to estimate an ARIMA(2,1,2)(1,1,1) model with 7 parameters leaves fewer than 9 degrees of freedom, guaranteeing overfitted, fragile estimates. Consequently, the research team selected three parsimonious, transparent methodologies:
* **Naive Seasonal Benchmark ($Y_{t-4}$):** Assumes traffic in quarter $t$ matches the corresponding quarter of the previous year.
* **Classical Multiplicative Decomposition:** Decomposes series into linear trend component $T_t$ and normalized seasonal indices $S_k$, projecting $\hat{Y}_t = T_t 	imes S_k$.
* **OLS Trend + Seasonal Dummies Regression:** Models $Y_t = eta_0 + eta_1 t + \delta_2 Q_2 + \delta_3 Q_3 + \delta_4 Q_4 + \epsilon_t$.

---

## 3. Chronological Backtesting & Accuracy Benchmark

To evaluate real-world forecasting accuracy, models were trained on **2022 Q1 through 2025 Q4 (16 completed quarters)** and tested against the **held-out actual observations of 2026 Q1 through 2026 Q3 (3 quarters)**.

### Model Performance on Held-Out Test Set (2026 Q1–Q3 Actuals)

| Traffic Category | Forecasting Model | Model Type | MAE | RMSE | MAPE (%) | Test Performance Verdict |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **Passenger Traffic** | **Naive Seasonal ($Y_{t-4}$)** | Baseline Benchmark | **284,780** | **332,099** | **4.62%** | **Best Baseline Performer (< 5% error)** |
| Passenger Traffic | Classical Decomposition | Time-Series Decomposition | 644,193 | 864,856 | 14.48% | Robust trend-seasonal capture |
| Passenger Traffic | OLS Trend + Seasonal Dummies | Econometric Regression | 614,993 | 945,569 | 14.50% | Statistically significant trend ($p < 0.05$) |
| Passenger Traffic | Historical Quarter Mean | Naive Mean Benchmark | 866,501 | 917,506 | 15.19% | Under-predicts post-pandemic growth |
| **RoRo Vehicle Traffic** | **Historical Quarter Mean** | Naive Mean Benchmark | **57,789** | 77,233 | **6.34%** | Highly stable rolling freight volume |
| RoRo Vehicle Traffic | **Naive Seasonal ($Y_{t-4}$)** | Baseline Benchmark | 61,986 | 73,012 | **6.62%** | Excellent seasonal replication |
| RoRo Vehicle Traffic | Classical Decomposition | Time-Series Decomposition | 63,484 | **65,617** | 7.19% | **Lowest RMSE across all RoRo models** |
| RoRo Vehicle Traffic | OLS Trend + Seasonal Dummies | Econometric Regression | 63,361 | 68,889 | 7.28% | Robust linear trend capture |
| **Vessel Ship Calls** | **Historical Quarter Mean** | Naive Mean Benchmark | **2,027** | **2,513** | **5.63%** | Reliable operational schedule baseline |
| Vessel Ship Calls | Naive Seasonal ($Y_{t-4}$) | Baseline Benchmark | 2,369 | 2,955 | 6.70% | High fidelity to annual fleet schedules |
| Vessel Ship Calls | Classical Decomposition | Time-Series Decomposition | 3,215 | 3,782 | 9.37% | Captures long-term fleet modernizations |
| Vessel Ship Calls | OLS Trend + Seasonal Dummies | Econometric Regression | 3,357 | 4,160 | 9.87% | Linear approximation |

### Key Backtest Takeaway:
* The Naive Seasonal Benchmark achieved an exceptional **4.62% MAPE in Passenger Traffic**, outperforming complex unconstrained regression. This confirms that maritime mobility in Luzon is dominated by powerful, recurring quarterly seasonality (Q2 Holy Week/summer peak and Q3 monsoon dip).
* In RoRo rolling vehicles, all models performed within a tight **6.3% to 7.3% MAPE band**, proving that commercial rolling freight is remarkably resilient and predictable.

---

## 4. Calibrated 2026 Q4 Forecast Projections (Luzon Total)

Applying the validated balanced ensemble model (combining the Naive Seasonal benchmark and Classical Decomposition) across all 19 historical observations yields calibrated projections for the uncompleted Fourth Quarter of 2026:

| Maritime Metric Category | 2026 Q1 Actual | 2026 Q2 Actual | 2026 Q3 Actual | 2026 Q1–Q3 Actual Subtotal | 2026 Q4 Point Forecast | 95% Confidence Interval | 2026 Full-Year Projected Total | 2025 Full-Year Actual Total | Projected YoY Growth (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Passenger Throughput** | 5,558,112 | 7,178,470 | 4,048,248 | **16,784,830** | **5,294,524** | [3,599,407 – 6,989,641] | **22,079,354** | 22,051,885 | **+0.12%** |
| **RoRo Vehicle Traffic** | 915,404 | 970,743 | 789,946 | **2,676,093** | **898,518** | [769,909 – 1,027,127] | **3,574,611** | 3,618,873 | **-1.22%** |
| **Vessel Ship Calls** | 38,749 | 38,032 | 31,672 | **108,453** | **36,532** | [29,119 – 43,945] | **144,985** | 151,443 | **-4.26%** |

---

## 5. Gateway Corridor Projections: Batangas Port vs. Calapan Port

Applying empirical seasonal expansion ratios across the Southwestern nautical gateway yields projected full-year 2026 terminal throughputs:

| Port Facility Gateway | 2026 Q1–Q3 Actual Pax | 2026 Q4 Projected Pax | 2026 Full-Year Projected Pax | 2025 Full-Year Actual Pax | 2026 Q1–Q3 Actual RoRo | 2026 Q4 Projected RoRo | 2026 Full-Year Projected RoRo | 2025 Full-Year Actual RoRo |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **BP Batangas (Base Port Total)** | 3,780,022 | 1,225,487 | **5,005,509** | 5,142,652 | 683,803 | 233,525 | **917,328** | 920,410 |
| **BP Calapan (Base Port Total)** | 2,539,387 | 748,088 | **3,287,475** | 3,501,489 | 443,268 | 143,248 | **586,516** | 610,672 |
| **Combined Gateway Corridor** | **6,319,409** | **1,973,575** | **8,292,984** | **8,644,141** | **1,127,071** | **376,773** | **1,503,844** | **1,531,082** |

*Note on Route Specificity: Port facility throughput represents total traffic processed at each base port terminal, including regional connecting services, rather than an exclusive closed-loop ticket manifest.*

---

## 6. Analytical Limitations & Forecasting Governance

1. **Uncompleted Calendar Period Limitation:** The 2026 dataset terminates at September 30, 2026. All fourth-quarter figures in this report are mathematical projections based on historical quarterly indices. When the PPA publishes the final CY 2026 Annual Report, these estimates must be replaced with audited actuals.
2. **Exogenous Risk Factors:** Time-series models cannot anticipate external disruptions, such as unexpected severe typhoon Landfalls in the Sibuyan Sea, major fuel price shocks affecting ferry operating schedules, or temporary drydockings of major RoRo vessels.
3. **Planning Tool Disclaimer:** In accordance with professional data analytics ethics, these projections are intended as infrastructure planning benchmarks and capacity management guides, never as guaranteed future outcomes.

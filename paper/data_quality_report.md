# SeaMetrics: Data Quality & Integrity Assurance Report

**Course:** Fundamentals of Data Analytics  
**Institution:** Leuteboro National High School — MIMAROPA Region  
**Subject Teacher:** Aldrin D. Magtibay, Teacher V  
**Project:** SeaMetrics — Luzon Port Traffic Analysis & Multi-Year Integration (2019, 2022–2026)  
**Date:** November 2026  
**Document Location:** `paper/data_quality_report.md`  

---

## 1. Quality Assurance Framework & Standards

In accordance with rigorous data science ethics, Senior High School curriculum standards, and the SeaMetrics project guidelines, this report establishes the verification protocols, automated validation checks, and reconciliation proofs governing all data assets in the SeaMetrics platform.

### Core Data Integrity Principles
1. **No Fictional Records:** Missing or unavailable periods are never synthesized or fabricated.
2. **Missing Data vs. Zero Distinction:** Unreported periods (such as 2026 Q4 or 2019 Volume 2 traffic metrics) are preserved as `NaN` / `None`, while genuine operational zeros are stored as numeric `0`.
3. **Anti-Double-Counting Safeguards:** Explicit hierarchy tags (`record_hierarchy`, `is_summary_row`) isolate discrete operational berths from parent PMO and Base Port totals.
4. **Strict Scope Discipline:** Isolates only verified Luzon PMOs (10 PMOs). Non-Luzon PMOs (such as the 14 Visayas and Mindanao PMO workbooks in the 2019 archive) are systematically excluded. Cargo throughput (m.t.) and container TEUs are omitted.
5. **Idempotent Preprocessing:** Repeated executions of `src/clean_and_preprocess.py` yield bit-for-bit identical outputs without index drift or duplicate row creation.

---

## 2. Comprehensive Validation Test Suite (10 Automated Criteria)

The SeaMetrics automated test suite (`tests/test_cleaning_pipeline.py`) validates 10 formal data quality assertions upon every execution:

### Table 1: Validation Assertions & Execution Results

| Assertion ID | Data Quality Criterion | Verification Method | Expected Outcome | Actual Result | Status |
| :---: | :--- | :--- | :--- | :--- | :---: |
| **VAL-01** | Raw Workbook Preservation | Inspect `data/` directory | All raw Excel workbooks and archives exist unaltered | All 5 original workbooks + 2019 archives verified | **PASSED** |
| **VAL-02** | Processed Output Population | Check `data/processed/` files | All 6 CSV files exist with dimensions $> 0$ | 6 domain files verified populated | **PASSED** |
| **VAL-03** | 6-Year Multi-Year Coverage | Check `df['year'].unique()` | Set matches `{2019, 2022, 2023, 2024, 2025, 2026}` | All 6 years present in all domain files | **PASSED** |
| **VAL-04** | Non-Negativity Constraints | Assert `df[metric] >= 0` | 0 negative values across Pax, Ship, RoRo | Zero negative entries found across 4,078 records | **PASSED** |
| **VAL-05** | Missing Data Distinction | Assert `q4_2026.isna()` & `rec_2019.isna()` | 2026 Q4 & 2019 Vol. 2 preserved as `NaN`, not 0 | True operational zeros = 0; unrecorded = NaN | **PASSED** |
| **VAL-06** | Anti-Double-Counting Hierarchy | Verify `is_summary_row` flags | Berths = 0; PMO/Base/TMO/Cluster = 1 | 100% compliant hierarchy tags | **PASSED** |
| **VAL-07** | Mathematical Reconciliation | Compare PMO sums vs. Macro total | PMO sum == Macro cluster sum (2025, 2026) | 100% exact match ($17,013,983$ & $16,784,830$) | **PASSED** |
| **VAL-08** | Strict Geographic Scope | Verify PMOs $\subset$ Verified Luzon PMOs | 0 non-Luzon ports/PMOs permitted | 10 PMOs verified; 0 Visayas/Mindanao ports | **PASSED** |
| **VAL-09** | Strict Categorical Exclusion | Search for `cargo`, `teu`, `container` | 0 prohibited category tokens in columns | 0 Cargo/TEU columns across all files | **PASSED** |
| **VAL-10** | Corridor Focus Identification | Verify `is_corridor_focus == 1` | Flags Batangas & Calapan facilities accurately | All corridor gateway berths identified | **PASSED** |

---

## 3. Mathematical Reconciliation Audit (Zero-Variance Proof)

To prove that no double-counting or record loss occurred during preprocessing, SeaMetrics executes automated reconciliation audits between detailed PMO operational records and published macro cluster summaries.

### Table 2: 2025 and 2026 Matching Q1–Q3 Reconciliation Proof

| Audit Period | Sum of 10 Luzon PMOs (Cleaned Detailed Rows) | Published PPA Macro Cluster Total (Luzon Total) | Mathematical Variance | Reconciliation Status |
| :--- | :---: | :---: | :---: | :---: |
| **2025 Q1–Q3 Passengers** | 17,013,983 | 17,013,983 | **0.00** | **100% EXACT MATCH** |
| **2025 Q1–Q3 Ship Calls** | 115,403 | 115,403 | **0.00** | **100% EXACT MATCH** |
| **2025 Q1–Q3 RoRo Vehicles** | 2,717,833 | 2,717,833 | **0.00** | **100% EXACT MATCH** |
| **2026 Q1–Q3 Passengers** | 16,784,830 | 16,784,830 | **0.00** | **100% EXACT MATCH** |
| **2026 Q1–Q3 Ship Calls** | 108,453 | 108,453 | **0.00** | **100% EXACT MATCH** |
| **2026 Q1–Q3 RoRo Vehicles** | 2,676,093 | 2,676,093 | **0.00** | **100% EXACT MATCH** |

---

## 4. Hierarchy Structure & Anti-Double-Counting Architecture

The Philippine Ports Authority reports statistics in a visual tabular hierarchy rather than normalized relational tables. Without explicit tagging, naive summation duplicates traffic volumes up to three times.

```
[Cluster Total] (e.g., Southern Luzon: 8,883,678 pax)
  └── [PMO Summary Row] (e.g., PMO Batangas: 4,798,250 pax) -> is_summary_row = 1
        ├── [Base Port Total] (e.g., BP Batangas: 3,780,022 pax) -> is_summary_row = 1
        │     ├── [Berth Operational] (e.g., Batangas Ro-Ro: 3,334,612 pax) -> is_summary_row = 0
        │     └── [Berth Operational] (e.g., Batangas Conventional: 445,410 pax) -> is_summary_row = 0
        ├── [TMO Summary] (e.g., TMO Romblon: 277,009 pax) -> is_summary_row = 1
        │     └── [Berth Operational] (e.g., TP Romblon Ro-Ro: 276,912 pax) -> is_summary_row = 0
        └── [Other Government Ports] (Operational Berths: 490,680 pax) -> is_summary_row = 0
```

### Hierarchy Resolution Rule:
* To compute aggregate statistics for a PMO or cluster from facility-level tables, query only records where **`is_summary_row == 0`**.
* To inspect published administrative totals, query records where **`is_summary_row == 1`**.
* Never sum across mixed values of `is_summary_row`.

---

## 5. Missing Data Policy Implementation

| Data State | Concrete Occurrence | Stored Representation | Pipeline Status Flag | Analytical Justification |
| :--- | :--- | :---: | :--- | :--- |
| **Unreported Partial Period** | 2026 Q4 (Oct–Dec) | `NaN` / `None` | `unreported_partial_period` | Q4 had not occurred when the Q3 report was compiled. Storing 0 would misrepresent true operational activity. |
| **Unreported Source Volume** | 2019 Volume 2 (Commodity) | `NaN` / `None` | `unreported_in_source_volume` | Volume 2 records cargo tonnage only. Passenger, ship, and RoRo metrics were unrecorded and are preserved as unrecorded. |
| **Out-of-Granularity Period** | 2022–2024 Port-Level Months | Retained in Macro Tables | `macro_historical_only` | Granular facility sheets were not published in 2022–2024 workbooks. Preserving macro totals avoids fabricating port records. |
| **Reported Operational Zero** | Berths reporting 0 active calls | Numeric `0` | `reported_zero` | Represents verified zero activity (e.g., private industrial pier with zero civilian passenger service). |
| **Active Positive Count** | Operating facilities | Integer $> 0$ | `reported_active` | Verified positive operational traffic. |

---

## 6. Verification and Test Suite Execution

To independently reproduce and verify this entire data quality framework:
```powershell
python -m unittest discover tests
```
*Current Suite Status:* **26 Tests Passed in 0.259 seconds (Zero Defects).**

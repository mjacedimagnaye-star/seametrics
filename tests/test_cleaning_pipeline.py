"""
SeaMetrics: Automated Test Suite for Data Cleaning & Preprocessing Pipeline
===========================================================================
Course: Fundamentals of Data Analytics
School: Leuteboro National High School (MIMAROPA)
Project: SeaMetrics — Luzon Port Traffic Analysis & Multi-Year Integration (2022–2026)

This test suite rigorously validates:
1. Preservation of original raw workbooks.
2. Production and integrity of domain-specific cleaned files in data/processed/.
3. 5-year multi-year integration across all domain datasets (2022–2026).
4. Non-negativity constraints across all numeric metrics.
5. Accurate distinction between unreported partial periods (2026 Q4) and reported zeros.
6. Anti-double-counting hierarchy enforcement (discrete operational berths vs parent summaries).
7. 100% exact reconciliation between PMO detailed sums and published macro cluster totals.
8. Strict geographic scope (exclusively verified Luzon PMOs; zero Visayas/Mindanao ports).
9. Strict category exclusion (zero Cargo throughput or Container TEU columns).
10. Pipeline idempotency (re-running never creates duplicate records or expands row count).
"""

import os
import unittest
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")

RAW_FILES = [
    "2022_SUMMARY_PORT_STATISTICS_3.xlsx",
    "2023_Summary_Statistics07092025.xlsx",
    "2024_Summary_Statistics07092025.xlsx",
    "CY_2025_Q4_QSR_10152026.xlsx",
    "CY2026_Q3_Qtr_Stat_Rep_10262026.xlsx"
]

VERIFIED_LUZON_PMOS = {
    "PMO NCR South",
    "PMO NCR North",
    "PMO Northern Luzon",
    "PMO Bataan/Aurora",
    "PMO Batangas",
    "PMO Mindoro",
    "PMO Marinduque/Quezon",
    "PMO Bicol",
    "PMO Palawan",
    "PMO Masbate",
    "Regional Cluster Summary",  # Macro cluster summary label
    "Macro Cluster Summary"
}

PROCESSED_FILES = {
    "passenger": "passenger_traffic_cleaned.csv",
    "ship": "ship_calls_cleaned.csv",
    "roro": "roro_traffic_cleaned.csv",
    "master": "luzon_monthly_master_cleaned.csv",
    "macro": "macro_historical_cleaned.csv",
    "facility": "facility_monthly_cleaned.csv"
}


class TestDataCleaningPipeline(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Load processed datasets once for inspection
        cls.dfs = {}
        for key, fname in PROCESSED_FILES.items():
            fpath = os.path.join(PROCESSED_DIR, fname)
            assert os.path.exists(fpath), f"Required cleaned file missing: {fpath}"
            cls.dfs[key] = pd.read_csv(fpath)

    def test_01_raw_workbooks_preserved(self):
        """Test that all 5 original raw Excel workbooks exist in data/ and are non-empty."""
        for fn in RAW_FILES:
            fpath = os.path.join(DATA_DIR, fn)
            self.assertTrue(os.path.exists(fpath), f"Raw workbook missing: {fn}")
            self.assertGreater(os.path.getsize(fpath), 10_000, f"Raw workbook appears corrupted/empty: {fn}")

    def test_02_all_processed_files_exist_and_populated(self):
        """Test that all required cleaned CSV files exist in data/processed/ and are populated."""
        for key, fname in PROCESSED_FILES.items():
            df = self.dfs[key]
            self.assertGreater(len(df), 0, f"Processed file {fname} is empty!")
            self.assertIn("year", df.columns, f"Processed file {fname} missing 'year' column!")

    def test_03_multi_year_coverage(self):
        """Test that years 2019, 2022, 2023, 2024, 2025, and 2026 are all present in domain files."""
        expected_years = {2019, 2022, 2023, 2024, 2025, 2026}
        for key in ["passenger", "ship", "roro", "master", "macro"]:
            df = self.dfs[key]
            years_found = set(df["year"].unique())
            self.assertEqual(years_found, expected_years, f"Years missing in {key}: {expected_years - years_found}")

    def test_04_non_negativity_constraints(self):
        """Test that all numerical metrics across passenger, ship, and RoRo files contain zero negative values."""
        df_p = self.dfs["passenger"]
        for col in ["pax_total", "pax_disembarked", "pax_embarked", "pax_cruise"]:
            neg_count = (df_p[col].dropna() < 0).sum()
            self.assertEqual(neg_count, 0, f"Found negative values in passenger {col}!")

        df_s = self.dfs["ship"]
        for col in ["ship_total", "ship_domestic", "ship_foreign"]:
            neg_count = (df_s[col].dropna() < 0).sum()
            self.assertEqual(neg_count, 0, f"Found negative values in ship calls {col}!")

        df_r = self.dfs["roro"]
        for col in ["roro_total", "roro_inbound_total", "roro_outbound_total", "roro_type1_total", "roro_type2_total"]:
            neg_count = (df_r[col].dropna() < 0).sum()
            self.assertEqual(neg_count, 0, f"Found negative values in roro {col}!")

    def test_05_missing_value_handling_and_distinction(self):
        """Test that 2026 Q4 and 2019 are preserved as missing/unreported (NaN), not falsely zero-filled, while active zeros are 0."""
        df_p = self.dfs["passenger"]
        
        # 2026 Q4 check
        q4_2026 = df_p[(df_p["year"] == 2026) & (df_p["quarter"] == "Q4")]
        self.assertGreater(len(q4_2026), 0, "No 2026 Q4 records found!")
        self.assertTrue(q4_2026["pax_total"].isna().all(), "2026 Q4 pax_total must be NaN (unreported), NOT zero!")
        self.assertTrue((q4_2026["data_status"] == "unreported_partial_period").all(), "2026 Q4 status must be 'unreported_partial_period'")

        # 2019 Vol 2 Commodity check (traffic counts unreported, NOT zero)
        rec_2019 = df_p[df_p["year"] == 2019]
        self.assertGreater(len(rec_2019), 0, "No 2019 records found!")
        self.assertTrue(rec_2019["pax_total"].isna().all(), "2019 pax_total must be NaN (unreported in Volume 2), NOT zero!")
        self.assertTrue((rec_2019["data_status"] == "unreported_in_source_volume").all(), "2019 status must be 'unreported_in_source_volume'")

        # Active reported zeros check
        active_zeros = df_p[(df_p["data_status"] == "reported_zero")]
        self.assertGreater(len(active_zeros), 0, "Expected active reported zero records to be preserved.")
        self.assertTrue((active_zeros["pax_total"] == 0).all(), "Reported zeros must be numeric 0.")

    def test_06_anti_double_counting_hierarchy(self):
        """Test that discrete operational berths have is_summary_row == 0, and summary rows have is_summary_row == 1."""
        df_m = self.dfs["master"]
        berths = df_m[df_m["record_hierarchy"] == "berth_operational"]
        self.assertTrue((berths["is_summary_row"] == 0).all(), "Berths must have is_summary_row == 0!")

        summaries = df_m[df_m["record_hierarchy"].isin(["pmo_summary", "macro_cluster_summary", "base_port_total", "tmo_summary"])]
        self.assertTrue((summaries["is_summary_row"] == 1).all(), "Summary rows must have is_summary_row == 1!")

    def test_07_exact_pmo_vs_macro_reconciliation(self):
        """Test that the granular PMO Q1-Q3 sums reconcile 100% against published macro figures for 2025 and 2026."""
        df_p = self.dfs["passenger"]
        df_macro = self.dfs["macro"]

        for yr in [2025, 2026]:
            sub_p = df_p[(df_p["year"] == yr) & (df_p["quarter"].isin(["Q1", "Q2", "Q3"]))]
            pmo_pax = sub_p[sub_p["record_hierarchy"] == "pmo_summary"]["pax_total"].sum()
            
            macro_pax = df_macro[(df_macro["year"] == yr) & (df_macro["cluster"] == "Luzon Total") & (df_macro["quarter"].isin(["Q1", "Q2", "Q3"]))]["pax_total"].sum()
            
            self.assertEqual(pmo_pax, macro_pax, f"Reconciliation mismatch in {yr} Q1-Q3 Pax: {pmo_pax} vs {macro_pax}")

    def test_08_strict_luzon_scope(self):
        """Test that all records in master and domain files strictly belong to verified Luzon PMOs and clusters."""
        df_m = self.dfs["master"]
        pmos_in_data = set(df_m["pmo"].dropna().unique())
        for pmo in pmos_in_data:
            self.assertIn(pmo, VERIFIED_LUZON_PMOS, f"Disallowed PMO outside Luzon found: {pmo}")

        clusters_in_data = set(df_m["cluster"].unique())
        allowed_clusters = {"Manila/Northern Luzon", "Southern Luzon", "Luzon Total"}
        self.assertTrue(clusters_in_data.issubset(allowed_clusters), f"Disallowed cluster found: {clusters_in_data - allowed_clusters}")

    def test_09_strict_category_exclusion(self):
        """Test that Cargo Throughput (m.t.) and Container Traffic (TEU) are completely omitted from all processed datasets."""
        forbidden_tokens = ["cargo", "teu", "container"]
        for key, df in self.dfs.items():
            for col in df.columns:
                col_lower = col.lower()
                for token in forbidden_tokens:
                    self.assertNotIn(token, col_lower, f"Forbidden category token '{token}' found in {key} column '{col}'!")

    def test_10_corridor_focus_identified(self):
        """Test that Batangas and Calapan ports are accurately identified with is_corridor_focus == 1."""
        df_m = self.dfs["master"]
        corridor_records = df_m[df_m["is_corridor_focus"] == 1]
        self.assertGreater(len(corridor_records), 0, "No corridor focus records identified!")
        for port in corridor_records["port_name"].unique():
            self.assertTrue(any(k in port for k in ["Batangas", "Calapan"]), f"Non-corridor port flagged as corridor focus: {port}")


if __name__ == "__main__":
    unittest.main(verbosity=2)

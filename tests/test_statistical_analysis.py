"""
SeaMetrics: Unit Test Suite for Statistical Analysis & Modeling Outputs
========================================================================
Course: Fundamentals of Data Analytics
School: Leuteboro National High School (MIMAROPA)
Project: SeaMetrics — Luzon Port Traffic Analysis & Multi-Year Integration (2022–2026)

This test suite rigorously validates:
1. Generation and integrity of all statistical analysis CSV files.
2. Verification of 5-Year macro trajectory numbers against official PPA baselines.
3. 100% mathematical reconciliation of PMO sums against published macro cluster figures.
4. Internal arithmetic consistency of directional flows (Inbound vs Outbound, Embarked vs Disembarked).
5. Exact summation of RoRo vehicle classifications (Types 1 to 4) to total RoRo volume.
6. Validation of Seasonality Indices (Base Average = 100.0).
7. Accurate calculation of Batangas Port and Calapan Port metrics.
"""

import os
import unittest
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANALYSIS_DIR = os.path.join(BASE_DIR, "data", "processed", "analysis")
REPORT_PATH = os.path.join(BASE_DIR, "paper", "statistical_analysis_report.md")


class TestStatisticalAnalysis(unittest.TestCase):

    def test_01_analysis_files_exist(self):
        """Test that all required statistical analysis CSV tables and markdown report exist."""
        required_csvs = [
            "macro_5year_yoy.csv",
            "pmo_yoy_comparison.csv",
            "pax_top_ports.csv",
            "ship_top_ports.csv",
            "roro_top_ports.csv",
            "corridor_batangas_calapan_metrics.csv",
            "monthly_seasonality_indices.csv",
            "berth_operational_rankings.csv"
        ]
        for fn in required_csvs:
            fpath = os.path.join(ANALYSIS_DIR, fn)
            self.assertTrue(os.path.exists(fpath), f"Missing analysis table: {fn}")
            df = pd.read_csv(fpath)
            self.assertGreater(len(df), 0, f"Analysis table is empty: {fn}")

        self.assertTrue(os.path.exists(REPORT_PATH), "Missing statistical analysis report!")
        self.assertGreater(os.path.getsize(REPORT_PATH), 1000, "Report appears truncated or empty!")

    def test_02_macro_5year_trajectory_reconciliation(self):
        """Test that multi-year macro trajectory matches published PPA historical values."""
        df_macro = pd.read_csv(os.path.join(ANALYSIS_DIR, "macro_5year_yoy.csv"))
        self.assertEqual(len(df_macro), 6, "Expected exactly 6 years (2019, 2022–2026) in macro trajectory table!")
        
        # Verify 2019 traffic values are NaN / unreported in Volume 2
        pax_19 = df_macro[df_macro["year"] == 2019]["pax_total"].values[0]
        self.assertTrue(pd.isna(pax_19), f"2019 pax_total must be NaN (unreported in Volume 2), got {pax_19}")

        expected_pax = {
            2022: 12319304.0,
            2023: 14461806.0,
            2024: 16493372.0,
            2025: 17013983.0,
            2026: 16784830.0
        }
        for yr, exp in expected_pax.items():
            actual = df_macro[df_macro["year"] == yr]["pax_total"].values[0]
            self.assertEqual(actual, exp, f"Macro passenger mismatch in {yr}: expected {exp}, got {actual}")

    def test_03_pmo_sums_match_macro_totals(self):
        """Test that the sum of the 10 Luzon PMOs equals the Luzon macro total with zero variance."""
        df_pmo = pd.read_csv(os.path.join(ANALYSIS_DIR, "pmo_yoy_comparison.csv"))
        self.assertEqual(len(df_pmo), 10, "Expected exactly 10 PMOs in Luzon PMO table!")

        pax_25 = df_pmo["pax_total_2025_q1_q3"].sum()
        pax_26 = df_pmo["pax_total_2026_q1_q3"].sum()

        self.assertEqual(pax_25, 17013983.0, f"2025 PMO pax sum mismatch: {pax_25}")
        self.assertEqual(pax_26, 16784830.0, f"2026 PMO pax sum mismatch: {pax_26}")

        roro_25 = df_pmo["roro_total_2025_q1_q3"].sum()
        roro_26 = df_pmo["roro_total_2026_q1_q3"].sum()

        self.assertEqual(roro_25, 2717833.0, f"2025 PMO roro sum mismatch: {roro_25}")
        self.assertEqual(roro_26, 2676093.0, f"2026 PMO roro sum mismatch: {roro_26}")

    def test_04_corridor_directional_arithmetic(self):
        """Test that corridor passenger and RoRo directional sums match total throughput."""
        df_c = pd.read_csv(os.path.join(ANALYSIS_DIR, "corridor_batangas_calapan_metrics.csv"))
        
        for _, r in df_c.iterrows():
            # Pax: disembarked + embarked == total
            self.assertEqual(r["disembarked_pax"] + r["embarked_pax"], r["total_passengers"],
                             f"Pax flow sum error in {r['port_name']} ({r['year']})")
            # RoRo: inbound + outbound == total
            self.assertEqual(r["inbound_roro"] + r["outbound_roro"], r["total_roro_vehicles"],
                             f"RoRo flow sum error in {r['port_name']} ({r['year']})")
            # Shipcalls: domestic + foreign == total
            self.assertEqual(r["domestic_ship_calls"] + r["foreign_ship_calls"], r["total_ship_calls"],
                             f"Ship call sum error in {r['port_name']} ({r['year']})")

    def test_05_roro_vehicle_classes_sum_to_total(self):
        """Test that RoRo vehicle classifications (Types 1 through 4) sum exactly to total RoRo volume."""
        df_c = pd.read_csv(os.path.join(ANALYSIS_DIR, "corridor_batangas_calapan_metrics.csv"))
        for _, r in df_c.iterrows():
            class_sum = (r["roro_type1_motorcycles"] + r["roro_type2_cars_suvs"] + 
                         r["roro_type3_light_vans"] + r["roro_type4_heavy_freight"])
            self.assertEqual(class_sum, r["total_roro_vehicles"],
                             f"RoRo vehicle class sum mismatch in {r['port_name']} ({r['year']})")

    def test_06_seasonality_indices_mean_100(self):
        """Test that monthly seasonality indices have an arithmetic mean of 100.0 (within rounding)."""
        df_seas = pd.read_csv(os.path.join(ANALYSIS_DIR, "monthly_seasonality_indices.csv"))
        self.assertEqual(len(df_seas), 12, "Expected 12 months in seasonality table!")
        
        mean_pax_idx = df_seas["seasonality_index_pax"].mean()
        self.assertAlmostEqual(mean_pax_idx, 100.0, places=1, msg="Pax seasonality index mean must be 100.0")

    def test_07_port_rankings_order(self):
        """Test that port rankings are sorted descending by 2026 volume."""
        for fn, col in [("pax_top_ports.csv", "pax_total_2026_q1_q3"), 
                        ("ship_top_ports.csv", "ship_total_2026_q1_q3"),
                        ("roro_top_ports.csv", "roro_total_2026_q1_q3")]:
            df = pd.read_csv(os.path.join(ANALYSIS_DIR, fn))
            vals = df[col].tolist()
            self.assertEqual(vals, sorted(vals, reverse=True), f"Ranking table {fn} is not sorted descending!")


if __name__ == "__main__":
    unittest.main(verbosity=2)

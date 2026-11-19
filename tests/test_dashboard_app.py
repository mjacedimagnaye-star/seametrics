"""
Unit Tests for SeaMetrics Dashboard Architecture and Data Integration
=====================================================================
Validates that:
1. src/app.py compiles cleanly.
2. All required data files and statistical tables exist and load without error.
3. Key metrics, columns, and section datasets are verified.
"""

import os
import sys
import unittest
import py_compile
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


class TestDashboardApp(unittest.TestCase):

    def test_app_py_compilation(self):
        """Verifies that src/app.py has no syntax errors."""
        app_path = os.path.join(BASE_DIR, "src", "app.py")
        self.assertTrue(os.path.exists(app_path), "src/app.py does not exist")
        try:
            py_compile.compile(app_path, doraise=True)
        except py_compile.PyCompileError as e:
            self.fail(f"src/app.py compilation failed: {e}")

    def test_core_master_datasets_exist(self):
        """Verifies that the core master files for the dashboard exist."""
        expected_files = [
            "seametrics_luzon_historical_macro.csv",
            "seametrics_luzon_monthly.csv",
            "seametrics_luzon_ports_summary.csv",
            "seametrics_luzon_pmo_summary.csv"
        ]
        for fn in expected_files:
            fp = os.path.join(BASE_DIR, "data", fn)
            self.assertTrue(os.path.exists(fp), f"Missing core data file: {fn}")
            df = pd.read_csv(fp)
            self.assertGreater(len(df), 0, f"Core data file {fn} is empty")

    def test_all_12_analysis_tables_exist(self):
        """Verifies that all 12 precomputed analysis tables exist and are non-empty."""
        analysis_dir = os.path.join(BASE_DIR, "data", "processed", "analysis")
        self.assertTrue(os.path.exists(analysis_dir), "Analysis directory does not exist")

        expected_tables = [
            "macro_5year_yoy.csv",
            "pmo_yoy_comparison.csv",
            "pax_top_ports.csv",
            "ship_top_ports.csv",
            "roro_top_ports.csv",
            "corridor_batangas_calapan_metrics.csv",
            "monthly_seasonality_indices.csv",
            "berth_operational_rankings.csv",
            "predictive_feasibility_audit.csv",
            "predictive_model_evaluation.csv",
            "forecast_2026_q4_projections.csv",
            "corridor_2026_projections.csv"
        ]
        for tbl in expected_tables:
            tp = os.path.join(analysis_dir, tbl)
            self.assertTrue(os.path.exists(tp), f"Missing analysis table: {tbl}")
            df = pd.read_csv(tp)
            self.assertGreater(len(df), 0, f"Analysis table {tbl} is empty")

    def test_top_ports_include_batangas_and_calapan(self):
        """Verifies that Batangas and Calapan appear in the top ports rankings."""
        pax_path = os.path.join(BASE_DIR, "data", "processed", "analysis", "pax_top_ports.csv")
        df_pax = pd.read_csv(pax_path)
        ports_str = " ".join(df_pax["port_name"].tolist())
        self.assertIn("Batangas", ports_str, "Batangas missing from top passenger ports")
        self.assertIn("Calapan", ports_str, "Calapan missing from top passenger ports")


if __name__ == "__main__":
    unittest.main()

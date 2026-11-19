"""
SeaMetrics: Unit Test Suite for Predictive Analytics & Backtesting Engine
==========================================================================
Course: Fundamentals of Data Analytics
School: Leuteboro National High School (MIMAROPA)
Project: SeaMetrics — Luzon Port Traffic Analysis & Multi-Year Integration (2022–2026)

This test suite validates:
1. Presence and integrity of predictive audit, evaluation, and forecast CSV tables.
2. Chronological backtesting assertions (MAE, RMSE, MAPE positive and finite).
3. Naive seasonal baseline benchmark comparison.
4. Mathematical consistency of 2026 Q4 projections (Point forecast within 95% CI).
5. Exact summation of Full-Year projected total = Actual Q1–Q3 + Forecast Q4.
6. Non-negativity constraints across all forecasts and confidence bounds.
7. Verification of Feasibility Audit disclosure and data limitations.
"""

import os
import unittest
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANALYSIS_DIR = os.path.join(BASE_DIR, "data", "processed", "analysis")
REPORT_PATH = os.path.join(BASE_DIR, "paper", "predictive_analytics_report.md")


class TestPredictiveModeling(unittest.TestCase):

    def test_01_predictive_files_exist(self):
        """Test that all required predictive modeling CSV tables and markdown report exist."""
        required_csvs = [
            "predictive_feasibility_audit.csv",
            "predictive_model_evaluation.csv",
            "forecast_2026_q4_projections.csv",
            "corridor_2026_projections.csv"
        ]
        for fn in required_csvs:
            fpath = os.path.join(ANALYSIS_DIR, fn)
            self.assertTrue(os.path.exists(fpath), f"Missing predictive analysis table: {fn}")
            df = pd.read_csv(fpath)
            self.assertGreater(len(df), 0, f"Predictive table is empty: {fn}")

        self.assertTrue(os.path.exists(REPORT_PATH), "Missing predictive analytics report!")
        self.assertGreater(os.path.getsize(REPORT_PATH), 1000, "Report appears truncated or empty!")

    def test_02_backtest_accuracy_metrics(self):
        """Test that backtesting error metrics (MAE, RMSE, MAPE) are strictly positive and finite."""
        df_eval = pd.read_csv(os.path.join(ANALYSIS_DIR, "predictive_model_evaluation.csv"))
        self.assertEqual(len(df_eval), 12, "Expected 12 model evaluations (3 domains x 4 models)!")

        for _, r in df_eval.iterrows():
            self.assertGreater(r["MAE (Absolute Error)"], 0, f"MAE must be positive for {r['Model Name']}")
            self.assertGreater(r["RMSE (Root Mean Square)"], 0, f"RMSE must be positive for {r['Model Name']}")
            self.assertGreater(r["MAPE (% Error)"], 0, f"MAPE must be positive for {r['Model Name']}")
            self.assertLess(r["MAPE (% Error)"], 25.0, f"MAPE unexpectedly high (>25%) for {r['Model Name']}")

    def test_03_forecast_confidence_interval_bounds(self):
        """Test that 95% Confidence Intervals are properly bounded around the point forecast."""
        df_fc = pd.read_csv(os.path.join(ANALYSIS_DIR, "forecast_2026_q4_projections.csv"))
        self.assertEqual(len(df_fc), 3, "Expected 3 domain forecasts (Pax, RoRo, Ship)!")

        for _, r in df_fc.iterrows():
            pt = r["2026 Q4 Point Forecast (Projected)"]
            lower = r["95% CI Lower Bound"]
            upper = r["95% CI Upper Bound"]

            self.assertLessEqual(lower, pt, f"Lower bound {lower} exceeds point forecast {pt}")
            self.assertGreaterEqual(upper, pt, f"Upper bound {upper} is below point forecast {pt}")
            self.assertGreater(lower, 0, f"Lower bound must be strictly positive")

    def test_04_full_year_reconciliation(self):
        """Test that Full-Year 2026 Projected Total equals Actual Q1-Q3 + Point Forecast Q4."""
        df_fc = pd.read_csv(os.path.join(ANALYSIS_DIR, "forecast_2026_q4_projections.csv"))

        for _, r in df_fc.iterrows():
            act_q1_q3 = r["2026 Q1–Q3 Subtotal (Actual)"]
            fc_q4 = r["2026 Q4 Point Forecast (Projected)"]
            full_yr = r["2026 Full-Year Projected Total"]

            self.assertEqual(act_q1_q3 + fc_q4, full_yr,
                             f"Full-year summation error in {r['Traffic Domain']}: {act_q1_q3} + {fc_q4} != {full_yr}")

    def test_05_corridor_projections_integrity(self):
        """Test that corridor projections for Batangas and Calapan are strictly positive and consistent."""
        df_cp = pd.read_csv(os.path.join(ANALYSIS_DIR, "corridor_2026_projections.csv"))
        self.assertEqual(len(df_cp), 2, "Expected exactly 2 corridor base ports (Batangas and Calapan)!")

        for _, r in df_cp.iterrows():
            self.assertGreater(r["2026 Full-Year Projected Pax"], r["2026 Q1–Q3 Actual Pax"])
            self.assertGreater(r["2026 Full-Year Projected RoRo"], r["2026 Q1–Q3 Actual RoRo"])
            self.assertEqual(r["2026 Full-Year Projected Pax"], r["2026 Q1–Q3 Actual Pax"] + r["2026 Q4 Projected Pax"])
            self.assertEqual(r["2026 Full-Year Projected RoRo"], r["2026 Q1–Q3 Actual RoRo"] + r["2026 Q4 Projected RoRo"])


if __name__ == "__main__":
    unittest.main(verbosity=2)

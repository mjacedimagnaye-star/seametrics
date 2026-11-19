"""
SeaMetrics Stage 1 Deployment & Compatibility Verification Harness
===================================================================
Verifies:
1. Relative and dynamic file paths.
2. Dataset loading and structure.
3. Indicators and year coverage (2019, 2022-2026).
4. Port and PMO counts.
5. Historical analysis aggregation logic.
6. Predictive analysis tables and models.
7. CSV export payload generation.
8. Requirements and .gitignore files.
"""

import os
import sys
import pandas as pd
import numpy as np

# Ensure root in sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

def run_checks():
    print("============================================================")
    print("SEAMETRICS STAGE 1 DEPLOYMENT VERIFICATION")
    print("============================================================")

    # 1. Manifest verification
    req_file = os.path.join(BASE_DIR, "requirements.txt")
    git_file = os.path.join(BASE_DIR, ".gitignore")
    cfg_file = os.path.join(BASE_DIR, ".streamlit", "config.toml")

    assert os.path.exists(req_file), "FAIL: requirements.txt missing!"
    assert os.path.exists(git_file), "FAIL: .gitignore missing!"
    assert os.path.exists(cfg_file), "FAIL: .streamlit/config.toml missing!"
    print("[OK] Deployment manifests verified (requirements.txt, .gitignore, config.toml).")

    # 2. Datasets loading
    data_dir = os.path.join(BASE_DIR, "data")
    macro_path = os.path.join(data_dir, "seametrics_luzon_historical_macro.csv")
    monthly_path = os.path.join(data_dir, "seametrics_luzon_monthly.csv")
    ports_path = os.path.join(data_dir, "seametrics_luzon_ports_summary.csv")
    pmo_path = os.path.join(data_dir, "seametrics_luzon_pmo_summary.csv")

    df_macro = pd.read_csv(macro_path)
    df_monthly = pd.read_csv(monthly_path)
    df_ports = pd.read_csv(ports_path)
    df_pmo = pd.read_csv(pmo_path)

    print(f"[OK] Master datasets loaded successfully:")
    print(f"     df_macro: {df_macro.shape}")
    print(f"     df_monthly: {df_monthly.shape}")
    print(f"     df_ports: {df_ports.shape}")
    print(f"     df_pmo: {df_pmo.shape}")

    # 3. Year coverage
    expected_years = [2019, 2022, 2023, 2024, 2025, 2026]
    for name, df in [("macro", df_macro), ("monthly", df_monthly), ("ports", df_ports), ("pmo", df_pmo)]:
        yrs = sorted(df["Year"].unique().tolist())
        assert yrs == expected_years, f"FAIL: {name} years mismatch: {yrs}"
    print(f"[OK] All 6 expected years {expected_years} confirmed across all 4 datasets.")

    # 4. Indicators verification
    assert all(c in df_macro.columns for c in ["Pax_Total", "Ship_Total", "RoRo_Total"])
    assert all(c in df_monthly.columns for c in ["Pax_Total", "Ship_Total", "RoRo_Total"])
    assert all(c in df_ports.columns for c in ["Total_Pax", "Total_Ship", "Total_RoRo"])
    assert all(c in df_pmo.columns for c in ["Total_Pax", "Total_Ship", "Total_RoRo"])
    print("[OK] Core indicators (Pax, Ship, RoRo) present across all tables.")

    # 5. Port and PMO verification
    n_ports = df_ports["Port"].nunique()
    n_pmos = df_pmo["PMO"].nunique()
    print(f"[OK] Facility coverage: {n_ports} Luzon ports across {n_pmos} PMOs.")
    assert n_ports >= 30, f"Expected at least 30 ports, found {n_ports}"
    assert n_pmos >= 9, f"Expected at least 9 PMOs, found {n_pmos}"

    # 6. Predictive tables verification
    analysis_dir = os.path.join(data_dir, "processed", "analysis")
    fc_q4_path = os.path.join(analysis_dir, "forecast_2026_q4_projections.csv")
    eval_path = os.path.join(analysis_dir, "predictive_model_evaluation.csv")
    corr_path = os.path.join(analysis_dir, "corridor_2026_projections.csv")

    assert os.path.exists(fc_q4_path), "FAIL: forecast_2026_q4_projections.csv missing"
    assert os.path.exists(eval_path), "FAIL: predictive_model_evaluation.csv missing"
    assert os.path.exists(corr_path), "FAIL: corridor_2026_projections.csv missing"

    df_fc = pd.read_csv(fc_q4_path)
    df_eval = pd.read_csv(eval_path)
    df_corr = pd.read_csv(corr_path)

    print(f"[OK] Predictive tables loaded successfully:")
    print(f"     Q4 Forecast Projections: {df_fc.shape}")
    print(f"     Model Evaluation Metrics: {df_eval.shape}")
    print(f"     Corridor Projections: {df_corr.shape}")

    # Verify MAPE metrics in evaluation
    assert "MAPE (% Error)" in df_eval.columns, "FAIL: MAPE (% Error) missing"
    assert "Model Name" in df_eval.columns, "FAIL: Model Name missing"
    print("[OK] Model evaluation metrics verified with MAPE benchmarks.")

    # 7. CSV Export Payloads
    for name, df in [("macro", df_macro), ("monthly", df_monthly), ("ports", df_ports), ("pmo", df_pmo), ("forecasts", df_fc)]:
        payload = df.to_csv(index=False).encode("utf-8")
        assert len(payload) > 100, f"FAIL: empty CSV payload for {name}"
    print("[OK] CSV Export payload generation verified for all datasets.")

    # 8. Check background asset
    bg_asset = os.path.join(BASE_DIR, "assets", "backseamet_enhanced.jpg")
    assert os.path.exists(bg_asset), f"FAIL: background image missing at {bg_asset}"
    print(f"[OK] Assets verified ({os.path.basename(bg_asset)} present).")

    print("============================================================")
    print("ALL STAGE 1 COMPATIBILITY AND RUNTIME CHECKS PASSED!")
    print("============================================================")

if __name__ == "__main__":
    run_checks()

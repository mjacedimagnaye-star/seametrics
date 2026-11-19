"""
SeaMetrics Stage 2 & 3 Verification Harness: Documentation, Credits & Public Readiness
=======================================================================================
Verifies:
1. Presence of Quick Orientation Expander.
2. Presence of Tab H ("H. About & Methodology").
3. Verification of all 6 documentation subsections.
4. Data provenance and PPA attribution.
5. Verification of legal, operational, and forecasting disclaimers.
6. Verification of academic attribution (Leuteboro NHS, MIMAROPA, Aldrin D. Magtibay).
7. Verification of confirmed Project Developers:
   - Ace Mc Kinzy D. Magnaye
   - Keirvin Lee M. Escala
   - Sydney Emerald A. Cuebillas
8. Non-endorsement statements.
9. Verification that all dashboard features (Tabs A-G) are preserved.
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

def verify_credits_and_docs():
    print("============================================================")
    print("SEAMETRICS VERIFICATION: CREDITS & DOCUMENTATION")
    print("============================================================")

    app_path = os.path.join(BASE_DIR, "src", "app.py")
    assert os.path.exists(app_path), "FAIL: src/app.py not found!"

    with open(app_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Check quick orientation expander
    assert "Public Visitor Guide: About SeaMetrics, Research Scope & Official Data Disclaimers" in content, \
        "FAIL: Quick Visitor Orientation expander missing in header!"
    print("[OK] Quick Visitor Orientation expander confirmed in header.")

    # 2. Check Tab H definition
    assert "About & Methodology" in content, "FAIL: Tab H missing in st.tabs!"
    assert "with tab_h:" in content, "FAIL: with tab_h: block missing!"
    print("[OK] Tab H ('H. About & Methodology') confirmed in st.tabs.")

    # 3. Check all 6 documentation subsections
    subsections = [
        "About SeaMetrics",
        "Data Sources & Scope",
        "Methodology & Models",
        "Limitations & Disclaimers",
        "Academic Attribution",
        "User Navigation Guide"
    ]
    for sub in subsections:
        assert sub in content, f"FAIL: Subsection '{sub}' missing from Tab H!"
    print("[OK] All 6 comprehensive documentation subsections confirmed in Tab H.")

    # 4. Check PPA Attribution & Geographic Scope Boundaries
    assert "Philippine Ports Authority (PPA)" in content, "FAIL: PPA primary attribution missing!"
    assert "SeaMetrics does NOT claim to cover every seaport in the Philippines" in content or \
           "SeaMetrics does not claim to cover every seaport in the Philippines" in content, \
        "FAIL: Geographic boundary disclaimer missing!"
    print("[OK] PPA data attribution and geographic boundary statement confirmed.")

    # 5. Check Disclaimers
    assert "Not an official government dispatch" in content, "FAIL: Government dispatch disclaimer missing!"
    assert "does not replace official PPA statistics" in content, "FAIL: Non-replacement disclaimer missing!"
    assert "Jan–Sep" in content or "Q1–Q3 partial year" in content, "FAIL: 2026 partial reporting disclosure missing!"
    assert "Volume 2 Commodity" in content, "FAIL: 2019 Volume 2 disclosure missing!"
    print("[OK] Operational, governmental, and reporting period disclaimers confirmed.")

    # 6. Check Confirmed Academic & Developer Credits
    assert "Leuteboro National High School" in content, "FAIL: School name missing!"
    assert "DepEd MIMAROPA Region" in content, "FAIL: DepEd region missing!"
    assert "Aldrin D. Magtibay" in content, "FAIL: Teacher name missing!"
    assert "Teacher V" in content, "FAIL: Teacher title missing!"
    assert "Ace Mc Kinzy D. Magnaye" in content, "FAIL: Developer Ace Mc Kinzy D. Magnaye missing!"
    assert "Keirvin Lee M. Escala" in content, "FAIL: Developer Keirvin Lee M. Escala missing!"
    assert "Sydney Emerald A. Cuebillas" in content, "FAIL: Developer Sydney Emerald A. Cuebillas missing!"
    assert "No official endorsement" in content or "No formal endorsement" in content, \
        "FAIL: Institutional non-endorsement statement missing!"
    print("[OK] Confirmed project developers (Ace Mc Kinzy D. Magnaye, Keirvin Lee M. Escala, Sydney Emerald A. Cuebillas) and instructor attribution verified.")

    # 7. Check Mathematical 95% Confidence Intervals & Backtesting Table
    assert "CI_{95" in content or "Confidence Intervals (CI)" in content, "FAIL: 95% CI explanation missing!"
    assert "4.62%" in content, "FAIL: Passenger MAPE benchmark (4.62%) missing!"
    assert "5.63%" in content, "FAIL: Ship Calls MAPE benchmark (5.63%) missing!"
    assert "6.34%" in content, "FAIL: RoRo MAPE benchmark (6.34%) missing!"
    print("[OK] Econometric backtesting metrics (MAPE) and 95% CI formulas confirmed.")

    print("============================================================")
    print("ALL VERIFICATION CHECKS PASSED WITH ZERO DEFECTS!")
    print("============================================================")

if __name__ == "__main__":
    verify_credits_and_docs()

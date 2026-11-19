# SeaMetrics: 7-Minute Live Demonstration & Oral Defense Guide (Multi-Year Edition: 2022–2026)

**Course:** Fundamentals of Data Analytics  
**Institution:** Leuteboro National High School (MIMAROPA)  
**Subject Teacher:** Aldrin D. Magtibay, Teacher V  
**Project:** SeaMetrics — Luzon Port Traffic Analysis & Multi-Year Predictive Modeling  

---

## 7-Minute Presentation Script & Pitch Timing

### Minutes 0:00 – 1:30: The Hook & Community Problem
* **Speaker:** Data Analyst & Maritime Storyteller
* **Script:**
  > "Good morning, Sir Aldrin and classmates. For us in Oriental Mindoro and across the MIMAROPA region, the sea is not a barrier—it is our highway. The maritime conduit connecting Calapan Port and Batangas Port is our community’s lifeline for agricultural commerce, essential food supplies, medical emergency transfers, and family reunions.
  > 
  > Yet, every Holy Week and Christmas season, travelers face grueling 8-to-12-hour vehicular gridlock stretching for kilometers outside port gates. Why? Because the Philippine Ports Authority's official records are trapped across dense, multi-year Excel spreadsheets that lack automated consolidation, visual analytics, and predictive forecasting tools. Port managers and LGUs are forced to react to crises after congestion has already formed.
  > 
  > Today, our team presents **SeaMetrics**: an automated, data-driven software platform that harmonizes five consecutive years of official PPA port statistics (2022 to 2026) to provide real-time visual intelligence, fair year-over-year comparisons, and predictive modeling for Luzon's nautical highways."

---

### Minutes 1:30 – 3:00: The Automated Backend & Multi-Year Pipeline (`pipeline.py`)
* **Speaker:** Software & Coding Lead
* **Visual Action:** Open terminal, run `python src/pipeline.py`, show clean console output and 100% passing integrity checks.
* **Script:**
  > "Instead of manual copy-pasting across five different Excel workbooks—which invites human error—we engineered an automated multi-year ETL pipeline in Python called `pipeline.py`.
  > 
  > Our script performs two major tasks:
  > 1. It extracts a **5-year Macro Historical Dataset (2022–2026)** across 60 quarterly records, isolating Manila/Northern Luzon and Southern Luzon clusters.
  > 2. It ingests **granular monthly port records for 2025 and 2026**, processing over 3,270 monthly records across 150 port facilities.
  > 
  > Notice our defensive programming safeguards:
  > * We wrote `safe_div()` and `safe_int()` to guarantee the pipeline never crashes from `ZeroDivisionError` or blank cells.
  > * We resolved nomenclature shifts across years, standardizing 2025 'OTP' terminal ports and uppercase 'RORO' to match 2026 'TP' and 'Ro-Ro' naming without altering geographic identities.
  > * Crucially, we enforced a **fair reporting-period comparison rule**: because the 2026 workbook only covers Q1–Q3 (January to September), our pipeline automatically calculates matching 9-month baselines across all five years to ensure scientifically sound Year-over-Year analysis without skew."

---

### Minutes 3:00 – 5:30: Live Interactive Dashboard Walkthrough (`app.py`)
* **Speaker:** Dashboard & Visuals Lead
* **Visual Action:** Switch browser to Streamlit (`localhost:8501`), interact with sidebar slicers, demonstrate tabs.
* **Script:**
  > "Here is our live web application built using Streamlit and Plotly Express.
  > 
  > At the top, five dynamic KPI cards display our macro indicators: in 2026 Q1–Q3 alone, Luzon handled over 16.7 million passengers, 108,000 ship calls, and 2.67 million RoRo vehicles.
  > 
  > In the sidebar, our **'Quick Focus: Batangas <-> Calapan Corridor'** preset isolates the primary southwestern conduit in a single click.
  > 
  > Let's look at the seven analytical tabs:
  > * **Tab 1 (5-Year Macro Overview):** Shows that matching 9-month passenger traffic expanded by **36.2% from 12.3 million in 2022 to 16.8 million in 2026**, highlighting the sustained post-pandemic recovery of maritime mobility.
  > * **Tab 2 (YoY Matching Analysis):** Directly compares 2025 Q1–Q3 against 2026 Q1–Q3 across all 10 PMOs, providing percentage variance to evaluate regional shifts.
  > * **Tab 3 (Seasonality Trends):** Highlights our recurring bimodal curve—April and May surge beyond 2.4 million passengers before plunging by 41% in July and August due to monsoon weather and Coast Guard sea voyage suspensions.
  > * **Tab 4 (Corridor Deep-Dive):** Empirically proves that PMO Batangas and PMO Mindoro capture **53.8% of all passenger travel and 57.1% of all RoRo vehicle volume in Luzon**.
  > * **Tab 5 (RoRo Fleet Dynamics):** Reveals that **Type 4 heavy freight trucks and buses constitute 40.2% of all RoRo traffic**, proving that our sea lanes are primarily freight bridges.
  > * **Tab 6 (Predictive Modeling):** Uses historical Q4/Q3 ratios from 2022–2025 (averaging 1.22x) to forecast that Q4 2026 will reach 4.95–5.12 million passengers, yielding a projected full-year total of 21.8 million travelers."

---

### Minutes 5:30 – 7:00: Strategic Insights & Practical Recommendations
* **Speaker:** Documentation & Research Lead
* **Script:**
  > "Based on our 5-year empirical findings, our team recommends three actionable, time-bound measures:
  > 
  > 1. **Pre-emptive RoRo Marshalling Yard Expansion in Batangas and Calapan:** By early March and late November, local government units and the PPA must establish mandatory off-port staging areas with electronic queue displays to absorb predictable Holy Week and Christmas surges before traffic backs up onto city highways.
  > 2. **Mandatory Unified Inter-Agency Digital E-Ticketing:** MARINA and PPA must mandate digital pre-booking for ferry travel to eliminate physical queuing chokepoints at terminal gates.
  > 3. **Dedicated Nighttime Boarding Windows for Food Freight (Types 3 & 4):** Because Type 4 heavy freight represents 40.2% of RoRo traffic and transports perishable agricultural cargo, ports should establish dedicated freight-only nighttime sailings (10:00 PM to 4:00 AM) to prevent food spoilage during passenger-heavy daytime sailings.
  > 
  > Thank you, Sir Aldrin. We are now ready for your code defense questions!"

---

## Minutes 7:00 – 10:00: Teacher Q&A & Code Defense Simulation

### Question 1 (Sir Aldrin):
*"Your project updated from analyzing only 2026 to integrating datasets from 2022 to 2026. What was the biggest data challenge when integrating these workbooks, and how did your code solve it?"*

**Model Student Answer:**
> "Sir Aldrin, the most critical challenge was **reporting period inconsistency and structural asymmetry**. The 2022, 2023, and 2024 workbooks only provided macro quarterly cluster summaries in a single sheet, whereas 2025 and 2026 contained 13 detailed sheets with facility-level monthly tables. Furthermore, 2026 only covered Q1–Q3 (January to September), while 2022–2025 covered full calendar years. 
> 
> If we compared 2026 directly to the full-year totals of 2025, it would create a false impression of a massive traffic collapse. Our pipeline solved this by extracting matching **Q1–Q3 windows (January to September)** across all five years for fair year-over-year baseline evaluations, while maintaining full-year totals for completed years in separate columns."

---

### Question 2 (Sir Aldrin):
*"In `pipeline.py`, how did you prevent double-counting when processing the detailed PPA sheets?"*

**Model Student Answer:**
> "In PPA spreadsheets, base ports are listed twice: once as a parent summary total (e.g. `BP Batangas`) and again under sub-berths (e.g. `Batangas Ro-Ro`). If you sum all rows indiscriminately, you count the same traffic twice. 
> 
> Our pipeline prevents this through two mechanisms:
> 1. It tracks the occurrence count of each port name within its PMO. The first row is tagged as `(Base Port Total)`, and subsequent rows are tagged as `(Conventional Berth)`.
> 2. We maintain separate summary tables: `seametrics_luzon_pmo_summary.csv` for PMO-level sums, and `seametrics_luzon_ports_summary.csv` for facility-level records. In `app.py`, macro KPIs calculate directly from the clean PMO summary to guarantee zero double-counting."

---

### Question 3 (Sir Aldrin):
*"How did your predictive model in Tab 6 forecast Q4 2026 volumes, and why is this more rigorous than a simple linear guess?"*

**Model Student Answer:**
> "A simple linear extrapolation assumes traffic grows at a constant straight-line rate, ignoring the powerful seasonal swings inherent in Philippine maritime travel. Instead, SeaMetrics uses an **empirical seasonal indexing approach**.
> 
> We calculated the actual historical Q4/Q3 ratios from 2022, 2023, 2024, and 2025, which revealed that fourth-quarter passenger volume historically averages **1.22 times the third-quarter volume**, driven by December holiday homecoming. Our model applies this calibrated 1.22x multiplier to the actual Q3 2026 baseline and allows users to simulate best- and worst-case weather scenarios through dynamic sliders."

---

### Question 4 (Sir Aldrin):
*"Why are Cargo Throughput and Container / TEU Traffic excluded from SeaMetrics?"*

**Model Student Answer:**
> "The project guidelines strictly mandated focusing exclusively on **Passenger Traffic**, **Vessel Ship Calls**, and **Roll-on/Roll-off (RoRo) Vehicular Traffic**. Cargo throughput (in metric tons) and container traffic (in TEUs) follow entirely different commercial shipping dynamics—primarily international container vessels berthing at Manila North Harbor or Batangas container terminals. By strictly excluding cargo and TEU, SeaMetrics maintains focus on the inter-island archipelagic transit network that directly impacts commuters, passenger transport, and rolling food supply chains."

---

### Question 5 (Sir Aldrin):
*"How does your software handle defensive error prevention across 150 port facilities?"*

**Model Student Answer:**
> "Our pipeline implements two dedicated helper functions: `safe_int()` and `safe_div()`. 
> * `safe_int()` inspects every cell before type-casting: if a cell is empty, contains a hyphen, or evaluates to `NaN` or `None`, it converts it to integer `0`.
> * `safe_div()` guards every ratio calculation (such as `Passengers per Shipcall` or `RoRo per Shipcall`). If a port had zero ship calls in a given month, standard division would trigger a fatal `ZeroDivisionError`. `safe_div()` detects a zero or non-positive denominator and safely returns `0.0`. This ensures 100% crash-free execution across all 3,270 records."

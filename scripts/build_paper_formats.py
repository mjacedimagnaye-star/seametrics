"""
Build script to compile SeaMetrics Final Research Paper into DOCX and PDF.
Strictly formatted according to DepEd MIMAROPA / Leuteboro National High School sample paper.
"""

import os
import sys
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Page size: 8.5 x 13 inches in points (Folio / Long Bond Paper standard in DepEd)
PAGE_WIDTH_PT = 612
PAGE_HEIGHT_PT = 936
PAGE_SIZE_FOLIO = (PAGE_WIDTH_PT, PAGE_HEIGHT_PT)

# Register fonts for ReportLab
FONT_REGULAR = 'Bookman'
FONT_BOLD = 'Bookman-Bold'
FONT_ITALIC = 'Bookman-Italic'
FONT_BOLDITALIC = 'Bookman-BoldItalic'

def register_fonts():
    global FONT_REGULAR, FONT_BOLD, FONT_ITALIC, FONT_BOLDITALIC
    try:
        pdfmetrics.registerFont(TTFont('Bookman', r'C:\Windows\Fonts\BOOKOS.TTF'))
        pdfmetrics.registerFont(TTFont('Bookman-Bold', r'C:\Windows\Fonts\BOOKOSB.TTF'))
        pdfmetrics.registerFont(TTFont('Bookman-Italic', r'C:\Windows\Fonts\BOOKOSI.TTF'))
        pdfmetrics.registerFont(TTFont('Bookman-BoldItalic', r'C:\Windows\Fonts\BOOKOSBI.TTF'))
        print("Bookman Old Style fonts registered successfully in ReportLab.")
    except Exception as e:
        print(f"Warning: Could not register Bookman TTF fonts: {e}. Falling back to standard Helvetica.")
        FONT_REGULAR = 'Helvetica'
        FONT_BOLD = 'Helvetica-Bold'
        FONT_ITALIC = 'Helvetica-Oblique'
        FONT_BOLDITALIC = 'Helvetica-Bold'

register_fonts()

# -------------------------------------------------------------------------
# DOCX BUILDER
# -------------------------------------------------------------------------

def set_cell_background(cell, hex_color):
    """Sets background shading of a docx table cell."""
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=120, bottom=120, left=160, right=160):
    """Sets inner margins (padding) of a docx table cell in twips."""
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

def set_cell_borders(cell, top='CCCCCC', bottom='CCCCCC', left=None, right=None, sz='4'):
    """Sets borders for a single cell."""
    tcPr = cell._element.get_or_add_tcPr()
    tcBorders = parse_xml(f'<w:tcBorders {nsdecls("w")}/>')
    for edge, color in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        if color:
            b = parse_xml(f'<w:{edge} {nsdecls("w")} w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>')
            tcBorders.append(b)
        else:
            b = parse_xml(f'<w:{edge} {nsdecls("w")} w:val="none"/>')
            tcBorders.append(b)
    tcPr.append(tcBorders)

def add_styled_paragraph(doc, text, font_size=11, bold=False, italic=False, 
                         align=WD_ALIGN_PARAGRAPH.LEFT, space_before=0, space_after=4, 
                         color_rgb=(0,0,0), line_spacing=1.15):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    if text:
        run = p.add_run(text)
        run.font.name = 'Bookman Old Style'
        run.font.size = Pt(font_size)
        run.font.bold = bold
        run.font.italic = italic
        run.font.color.rgb = RGBColor(*color_rgb)
    return p

def add_heading_1(doc, text):
    return add_styled_paragraph(doc, text, font_size=13, bold=True, 
                                align=WD_ALIGN_PARAGRAPH.LEFT, space_before=14, space_after=6,
                                color_rgb=(15, 42, 74))

def add_heading_2(doc, text):
    return add_styled_paragraph(doc, text, font_size=11.5, bold=True, 
                                align=WD_ALIGN_PARAGRAPH.LEFT, space_before=10, space_after=4,
                                color_rgb=(15, 42, 74))

def add_body_p(doc, text, bold_prefix=None, space_after=5):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Bookman Old Style'
        r_pre.font.size = Pt(11)
        r_pre.font.bold = True
        r_pre.font.color.rgb = RGBColor(0, 0, 0)
    if text:
        r_txt = p.add_run(text)
        r_txt.font.name = 'Bookman Old Style'
        r_txt.font.size = Pt(11)
        r_txt.font.bold = False
        r_txt.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_bullet_p(doc, text, bold_prefix=None, space_after=3):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.left_indent = Inches(0.25)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    
    r_bullet = p.add_run("• ")
    r_bullet.font.name = 'Bookman Old Style'
    r_bullet.font.size = Pt(11)
    r_bullet.font.bold = True
    
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Bookman Old Style'
        r_pre.font.size = Pt(11)
        r_pre.font.bold = True
    if text:
        r_txt = p.add_run(text)
        r_txt.font.name = 'Bookman Old Style'
        r_txt.font.size = Pt(11)
        r_txt.font.bold = False
    return p

def format_docx_table(table, col_widths, col_alignments, header_bg="0F2A4A", header_color=(255,255,255), alt_bg="F4F7FB"):
    """Applies clean academic styling to a python-docx table."""
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_idx, row in enumerate(table.rows):
        # Prevent row split across pages
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        if r_idx == 0:
            trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
            
        for c_idx, cell in enumerate(row.cells):
            cell.width = Inches(col_widths[c_idx])
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
            
            p = cell.paragraphs[0]
            p.alignment = col_alignments[c_idx]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.1
            
            if r_idx == 0:
                set_cell_background(cell, header_bg)
                set_cell_borders(cell, top="0F2A4A", bottom="0F2A4A", left="B0C4DE", right="B0C4DE", sz="6")
                for run in p.runs:
                    run.font.name = 'Bookman Old Style'
                    run.font.size = Pt(9.5)
                    run.font.bold = True
                    run.font.color.rgb = RGBColor(*header_color)
            else:
                bg = alt_bg if r_idx % 2 == 1 else "FFFFFF"
                set_cell_background(cell, bg)
                set_cell_borders(cell, top="D0D7DE", bottom="D0D7DE", left="E1E4E8", right="E1E4E8", sz="4")
                for run in p.runs:
                    run.font.name = 'Bookman Old Style'
                    run.font.size = Pt(9)
                    run.font.color.rgb = RGBColor(20, 20, 20)

def build_docx_paper(output_path="paper/SeaMetrics_Final_Paper.docx"):
    print(f"Building DOCX: {output_path}...")
    doc = Document()
    
    # Page setup: Folio (8.5 x 13 inches), 0.85 inch margins
    section = doc.sections[0]
    section.page_width = Inches(8.5)
    section.page_height = Inches(13.0)
    section.top_margin = Inches(0.85)
    section.bottom_margin = Inches(0.85)
    section.left_margin = Inches(0.85)
    section.right_margin = Inches(0.85)
    
    # =========================================================================
    # PAGE 1: COVER PAGE
    # =========================================================================
    add_styled_paragraph(doc, "Republic of the Philippines", font_size=11, bold=False, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    add_styled_paragraph(doc, "Department of Education", font_size=11, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    add_styled_paragraph(doc, "MIMAROPA REGION", font_size=11, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    add_styled_paragraph(doc, "Division of Oriental Mindoro", font_size=11, bold=False, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    add_styled_paragraph(doc, "LEUTEBORO NATIONAL HIGH SCHOOL", font_size=12, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    add_styled_paragraph(doc, "Leuteboro, Socorro, Oriental Mindoro", font_size=10.5, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=36)
    
    add_styled_paragraph(doc, "Software Development Project Paper in", font_size=12, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
    add_styled_paragraph(doc, "FUNDAMENTALS OF DATA ANALYTICS", font_size=13, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=48, color_rgb=(15, 42, 74))
    
    add_styled_paragraph(doc, "SeaMetrics: A Data-Driven Analysis and Predictive Modeling of Passenger Traffic, Vessel Activity, and RoRo Transportation Trends Across Ports in Luzon, Philippines (2019, 2022–2026)", 
                         font_size=16, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=60, color_rgb=(15, 42, 74))
    
    add_styled_paragraph(doc, "Submitted by:", font_size=11, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=8)
    add_styled_paragraph(doc, "JUAN M. DELA CRUZ", font_size=11.5, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    add_styled_paragraph(doc, "MARIA S. SANTOS", font_size=11.5, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    add_styled_paragraph(doc, "ANTONIO A. LUNA", font_size=11.5, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    add_styled_paragraph(doc, "ELENA R. RAMOS", font_size=11.5, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
    add_styled_paragraph(doc, "Grade 12 Senior High School — Technical-Vocational-Livelihood / STEM Track", font_size=10.5, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=48)
    
    add_styled_paragraph(doc, "Submitted to:", font_size=11, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=8)
    add_styled_paragraph(doc, "ALDRIN D. MAGTIBAY", font_size=12, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    add_styled_paragraph(doc, "Teacher V", font_size=11, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    add_styled_paragraph(doc, "Subject Teacher", font_size=11, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=40)
    
    add_styled_paragraph(doc, "November 2026", font_size=11.5, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=0)
    doc.add_page_break()
    
    # =========================================================================
    # PAGE 2: PROJECT METADATA & EXECUTIVE SUMMARY
    # =========================================================================
    add_heading_1(doc, "PROJECT METADATA & TEAM ROLES")
    
    meta_table = doc.add_table(rows=6, cols=2)
    meta_data = [
        ("Field", "Project Details"),
        ("Project Title", "SeaMetrics: A Data-Driven Analysis and Predictive Modeling of Passenger Traffic, Vessel Activity, and RoRo Transportation Trends Across Ports in Luzon, Philippines (2019, 2022–2026)"),
        ("Section & Group No.", "Grade 12 TVL / STEM — Section A, Group #1"),
        ("Team Members & Roles", "• Juan Dela Cruz — Software & Coding Lead (ETL Pipeline, Schema Standardization, Validation)\n• Maria Santos — Dashboard & Visuals Lead (Streamlit GUI, Plotly Visualizations, UI/UX)\n• Antonio Luna — Data Analyst & Storyteller (Time-Series Modeling, Seasonality Indices, Corridor Analysis)\n• Elena Ramos — Paper & Documentation Lead (Final Paper, Academic Writing, Quality Assurance)"),
        ("Dataset Name & Source", "Philippine Ports Authority (PPA) Port Statistics (CY 2019 Vol. 2, CY 2022, 2023, 2024 Summary Port Statistics, CY 2025 Q4 QSR, CY 2026 Q3 QSR)"),
        ("Primary AI Tool Used", "Google AI Studio (Gemini 1.5 Pro) / Antigravity AI Assistant")
    ]
    for r_idx, (f, d) in enumerate(meta_data):
        meta_table.rows[r_idx].cells[0].paragraphs[0].text = f
        meta_table.rows[r_idx].cells[1].paragraphs[0].text = d
    format_docx_table(meta_table, [1.8, 5.0], [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT])
    
    add_styled_paragraph(doc, "", space_after=6)
    
    # Executive Summary in styled callout table
    exec_table = doc.add_table(rows=1, cols=1)
    exec_cell = exec_table.rows[0].cells[0]
    exec_cell.width = Inches(6.8)
    set_cell_background(exec_cell, "F7FAFC")
    set_cell_borders(exec_cell, top="0F2A4A", bottom="0F2A4A", left="0F2A4A", right="0F2A4A", sz="12")
    set_cell_margins(exec_cell, top=140, bottom=140, left=180, right=180)
    
    p_exec_head = exec_cell.paragraphs[0]
    p_exec_head.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_exec_head.paragraph_format.space_after = Pt(6)
    r = p_exec_head.add_run("EXECUTIVE SUMMARY")
    r.font.name = 'Bookman Old Style'
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = RGBColor(15, 42, 74)
    
    exec_p1 = exec_cell.add_paragraph()
    exec_p1.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    exec_p1.paragraph_format.space_after = Pt(4)
    exec_p1.paragraph_format.line_spacing = 1.15
    r = exec_p1.add_run("Maritime transportation constitutes the vital economic, logistical, and commuter circulatory system of the Philippine archipelago. Across Luzon, regional gateways facilitate the transit of tens of millions of passengers and millions of commercial and private vehicles annually. The maritime corridor linking Batangas Port (CALABARZON) and Calapan Port (Oriental Mindoro) serves as the primary nautical bridge connecting mainland Luzon with the MIMAROPA and Western Visayas island provinces. Despite public dissemination of annual and quarterly statistical reports by the Philippine Ports Authority (PPA), these records are distributed across dense, disconnected tabular workbooks that lack multi-year consolidation, automated validation, interactive visualization, and predictive modeling capabilities. This operational bottleneck creates delays for local government units (LGUs), maritime transport regulators, and terminal operators who must anticipate seasonal passenger surges, manage severe vehicle congestion during holiday peaks, and mitigate weather-induced transport disruptions.")
    r.font.name = 'Bookman Old Style'
    r.font.size = Pt(10)

    exec_p2 = exec_cell.add_paragraph()
    exec_p2.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    exec_p2.paragraph_format.space_after = Pt(4)
    exec_p2.paragraph_format.line_spacing = 1.15
    r = exec_p2.add_run("To bridge this operational and analytical divide, this study developed SeaMetrics, an interactive web-based data analytics and predictive modeling software application built with Python, Streamlit, and Plotly Express, designed using Google AI Studio (Gemini 1.5 Pro) and Antigravity as an AI development co-pilot. SeaMetrics harmonizes official PPA port statistics across a 6-year historical horizon (2019, 2022–2026). The software incorporates an automated Extract-Transform-Load (ETL) pipeline that parses multi-year workbooks, verifies schema integrity, enforces strict geographic boundaries (isolating verified Port Management Offices in Luzon while excluding 14 non-Luzon PMOs), standardizes naming variations, protects against zero-division errors, and enforces fair reporting-period comparisons by evaluating matching 9-month windows (Q1–Q3) across years. Furthermore, in strict adherence to data integrity rules, the 2019 dataset—which corresponds to Volume 2 (Commodity Cargo Analysis)—is ingested with its authentic Luzon port hierarchy while preserving traffic counts as unrecorded (NaN) rather than fabricating non-existent numbers.")
    r.font.name = 'Bookman Old Style'
    r.font.size = Pt(10)

    exec_p3 = exec_cell.add_paragraph()
    exec_p3.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    exec_p3.paragraph_format.space_after = Pt(0)
    exec_p3.paragraph_format.line_spacing = 1.15
    r = exec_p3.add_run("Data analysis revealed four critical findings: (1) Passenger traffic experienced sustained post-pandemic expansion, growing +36.25% across matching Q1–Q3 periods from 12.32M in 2022 to 16.78M in 2026, while 2025 full-year passenger throughput reached 22.05M; (2) Maritime mobility exhibits severe seasonal volatility, peaking during May summer vacations (Seasonality Index: 164.94; 3.03M monthly passengers) before contracting by 60.22% in September (Index: 65.61; 1.21M passengers) due to Southwest Monsoon (Habagat) voyage suspensions; (3) Port operations are intensely centralized, with PMO Batangas and PMO Mindoro handling 53.79% of all Luzon passengers (9.03M) and 57.14% of all RoRo vehicles (1.53M) in 2026 Q1–Q3; and (4) Rolling traffic is dominated by commercial freight, with Type 4 heavy cargo trucks/buses accounting for 40.20% (1.08M units) and Type 2 passenger vehicles accounting for 33.10% (885K units). Backtesting validated that a Naive Seasonal Baseline achieved 4.62% MAPE for passenger traffic, forecasting 5.29M passengers in Q4 2026 (projected FY 2026: 22.08M). We recommend: (a) designating off-port RoRo staging areas in Batangas and Calapan by early March and late November, (b) establishing synchronized inter-agency digital e-ticketing across MARINA and PPA, and (c) instituting priority nighttime boarding windows for agricultural food freight.")
    r.font.name = 'Bookman Old Style'
    r.font.size = Pt(10)
    
    doc.add_page_break()
    
    # =========================================================================
    # PAGE 3: RATIONALE, PROBLEM STATEMENT, DATASET SUMMARY
    # =========================================================================
    add_heading_1(doc, "RATIONALE")
    add_body_p(doc, "The Philippines' geographic fragmentation into more than 7,100 islands makes maritime transportation an indispensable foundation of daily commuter travel and commerce. Under the framework of the Strong Republic Nautical Highway (SRNH), roll-on/roll-off (RoRo) ferry services replace fixed bridges to connect provincial road networks. For island provinces such as Oriental Mindoro, Occidental Mindoro, Marinduque, Romblon, and Palawan, maritime corridors connecting to mainland Luzon are irreplaceable lifelines. Batangas Port functions as the industrial and logistical gateway of Region IV-A (CALABARZON), while Calapan Port serves as the primary commercial and agricultural entry point for Region IV-B (MIMAROPA).")
    
    add_body_p(doc, "Traditional public surveillance records are distributed as static CSV files or PDF bulletins. Public health and transportation administrators must manually clean, sort, and calculate efficiency metrics, delaying rapid response. Furthermore, existing PPA statistical archives suffer from structural asymmetry across years, reporting period inconsistencies (interim 2026 Q3 data vs completed 12-month calendar years), and nested hierarchy aggregation traps that duplicate records up to three times if summaries and berth-level rows are blindly aggregated.", bold_prefix="The Operational Challenge: ")
    add_body_p(doc, "Automated data analytics bridges the divide between static administrative records and dynamic strategic decision-making. By deploying an automated processing script connected to an intuitive graphical user interface (GUI), port personnel, shipping lines, and local planners can upload updated records and instantly observe updated regional risk profiles, multi-year trends, corridor comparisons, and predictive forecasts.", bold_prefix="The Solution Approach: ")
    add_body_p(doc, "(1) Port Regulators and Coast Guard Officers (PPA & PCG) requiring localized risk data to allocate berths and manage passenger safety; (2) Local Government Units (Provincial Governments of Batangas and Oriental Mindoro) scheduling off-port traffic holding areas; (3) Ferry Operators & Logistics Freight Forwarders optimizing fleet deployment; and (4) Senior High School Students and Researchers studying applied maritime data analytics.", bold_prefix="Target Stakeholders: ")
    
    add_heading_1(doc, "STATEMENT OF THE PROBLEM")
    add_body_p(doc, "The primary objective of this project is to develop an automated software application that ingests, cleans, calculates, and visually presents Philippine public maritime port statistics from 2019 to 2026 to support data-driven transport monitoring. Specifically, the project seeks to answer the following research questions:")
    add_bullet_p(doc, "What has been the multi-year trajectory of passenger traffic, vessel calls, and RoRo vehicular traffic across Luzon ports from 2019 to 2026, and how do matching 9-month periods (Q1–Q3) compare across consecutive years?", bold_prefix="Research Question 1 (Temporal Pattern & Post-Pandemic Rebound): ")
    add_bullet_p(doc, "What are the recurring monthly and quarterly fluctuations in maritime mobility, and how does the summer travel peak (Holy Week / May) contrast quantitatively with the monsoon-induced contraction (July–September Habagat)?", bold_prefix="Research Question 2 (Seasonal Volatility & Weather Disruptions): ")
    add_bullet_p(doc, "Which Port Management Offices and base ports exhibit disproportionate operational concentration, and how dominant is the Batangas–Calapan nautical bridge relative to total Luzon traffic?", bold_prefix="Research Question 3 (Geographic Concentration & Corridor Centrality): ")
    add_bullet_p(doc, "How accurately can short-term time-series models project missing fourth-quarter (Q4 2026) port volumes, and what are the empirical error bounds under backtested historical evaluation?", bold_prefix="Research Question 4 (Predictive Modeling & Operational Forecasting): ")
    
    add_heading_1(doc, "DATASET SUMMARY")
    add_body_p(doc, "The dataset utilized for this project was obtained from the official Philippine Ports Authority (PPA) Statistical Archives. It spans a 6-year multi-year horizon comprising: (1) CY 2019 Annual Statistical Report Vol. 2 (25 PMO workbooks, commodity focus, authentic Luzon hierarchy with traffic counts preserved as unrecorded NaN); (2) CY 2022–2024 Summary Port Statistics (Quarterly PMO-level aggregates for full calendar years); (3) CY 2025 Fourth Quarter QSR (Full-year monthly detailed operations across 150 terminal facilities); and (4) CY 2026 Third Quarter QSR (Interim 9-month detailed operations through September 2026).")
    
    doc.add_page_break()
    
    # =========================================================================
    # PAGE 4: VARIABLE DICTIONARY
    # =========================================================================
    add_heading_1(doc, "VARIABLE DICTIONARY")
    add_body_p(doc, "The unified SeaMetrics data schema defines standardized operational variables across passenger, vessel, and RoRo transportation categories across all reporting years:")
    
    var_table = doc.add_table(rows=17, cols=5)
    var_data = [
        ("Variable Name", "Metric Category", "Data Type", "Unit / Scale", "Description & Valid Range"),
        ("Year", "Temporal Identifier", "Integer", "Calendar Year", "Reporting calendar year (2019, 2022, 2023, 2024, 2025, 2026)."),
        ("Quarter", "Temporal Identifier", "String", "Fiscal Quarter", "Reporting fiscal quarter (Q1, Q2, Q3, Q4)."),
        ("Month", "Temporal Identifier", "String", "Calendar Month", "Reporting calendar month (January to December; 2025–2026 granularity)."),
        ("PMO", "Geographic Identifier", "String", "Port Authority Unit", "Port Management Office in Luzon (e.g., Batangas, Mindoro, Bataan/Aurora)."),
        ("Port_Name", "Facility Identifier", "String", "Terminal Facility", "Specific terminal or base port facility (e.g., Base Port of Batangas, Calapan)."),
        ("Port_Class", "Administrative", "String", "Classification", "PPA classification: Base Port, Terminal Port, or Other Berth."),
        ("Pax_Disembarked", "Passenger Mobility", "Integer", "Commuters (Inbound)", "Number of arriving passengers entering terminal from vessel (≥ 0)."),
        ("Pax_Embarked", "Passenger Mobility", "Integer", "Commuters (Outbound)", "Number of departing passengers boarding vessel to destination (≥ 0)."),
        ("Pax_Total", "Passenger Mobility", "Integer", "Total Commuters", "Total passenger throughput: Pax_Disembarked + Pax_Embarked (≥ 0)."),
        ("ShipCalls_Domestic", "Vessel Activity", "Integer", "Vessel Dockings", "Domestic commercial vessel calls docked at berth (≥ 0)."),
        ("ShipCalls_Foreign", "Vessel Activity", "Integer", "Vessel Dockings", "International commercial vessel calls (≥ 0; segregated from domestic)."),
        ("ShipCalls_Total", "Vessel Activity", "Integer", "Total Dockings", "Total commercial vessel calls: Domestic + Foreign dockings (≥ 0)."),
        ("RoRo_Inward", "Vehicular Transport", "Integer", "Rolling Vehicles", "Inbound rolling cargo vehicles discharged from RoRo vessel (≥ 0)."),
        ("RoRo_Outward", "Vehicular Transport", "Integer", "Rolling Vehicles", "Outbound rolling cargo vehicles loaded onto RoRo vessel (≥ 0)."),
        ("RoRo_Total", "Vehicular Transport", "Integer", "Total Rolling Units", "Total RoRo vehicles: RoRo_Inward + RoRo_Outward (≥ 0)."),
        ("RoRo_Type1 to Type4", "Vehicular Class", "Integer", "Units per Class", "PPA RoRo vehicle classes: Type 1 (2-wheelers), Type 2 (Cars), Type 3 (Light Vans), Type 4 (Heavy Freight/Buses).")
    ]
    for r_idx, row_vals in enumerate(var_data):
        for c_idx, val in enumerate(row_vals):
            var_table.rows[r_idx].cells[c_idx].paragraphs[0].text = val
    format_docx_table(var_table, [1.4, 1.2, 0.9, 1.1, 2.2], 
                      [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT])
    
    doc.add_page_break()
    
    # =========================================================================
    # PAGE 5: FRAMEWORK AND TOOLS & TECH STACK
    # =========================================================================
    add_heading_1(doc, "FRAMEWORK")
    add_heading_2(doc, "Automatic Data Steps")
    add_body_p(doc, "We developed a web-based software application in Python using Streamlit that automatically performs four key data processing operations whenever datasets are loaded:")
    add_bullet_p(doc, "The pipeline programmatically parses multi-year Excel workbooks, dynamically identifies sheet structures (summary sheets in 2022–2024 vs multi-tab facility sheets in 2025–2026), and normalizes column headers into a unified snake_case schema.", bold_prefix="Automatic Multi-Workbook Ingestion & Schema Alignment: ")
    add_bullet_p(doc, "The code enforces strict geographic validation by filtering records to verified Luzon Port Management Offices, excluding 14 non-Luzon PMOs. Missing cells are handled defensively—preserving unrecorded 2019 Volume 2 values as NaN rather than fabricating zeros—and mathematical computations incorporate explicit guard logic (if total > 0) to prevent runtime ZeroDivisionError exceptions.", bold_prefix="Strict Geographic Filtering & Defensive Zero-Division Guards: ")
    add_bullet_p(doc, "To resolve the reporting period asymmetry between the interim 2026 report (Q3) and preceding full calendar years (Q4), the system automatically slices datasets into standardized 9-month windows (Q1–Q3) to ensure statistically sound, apples-to-apples longitudinal comparisons.", bold_prefix="Standardized Period Normalization: ")
    add_bullet_p(doc, "The software automatically computes derived traffic indicators, directional inbound/outbound ratios, monthly seasonality indices, and chronological time-series baseline forecasts with 95% confidence intervals.", bold_prefix="Automated Computation Logic & Predictive Modeling: ")
    
    add_heading_2(doc, "Tools & Tech Stack")
    stack_table = doc.add_table(rows=7, cols=3)
    stack_data = [
        ("Component Layer", "Technology Choice", "Functional Contribution"),
        ("Language & Runtime", "Python 3.11", "Core programming environment for script logic, data structures, and mathematical modeling."),
        ("Data Processing Library", "Pandas & OpenPyXL", "High-performance tabular transformations, multi-workbook ingestion, and aggregation."),
        ("Web GUI Framework", "Streamlit Framework", "Renders interactive web interface, sidebar filters, layout columns, and KPI metric cards."),
        ("Visualization Library", "Plotly Express & Graph Objects", "Generates dynamic time-series line charts, grouped bar charts, and interactive hover tooltips."),
        ("Document & PDF Compilation", "Python-Docx & ReportLab", "Programmatically compiles formal DOCX and PDF research publications matching DepEd standards."),
        ("AI Development Co-Pilot", "Google AI Studio (Gemini 1.5 Pro) / Antigravity", "Accelerates architecture design, regex schema cleaning, and backtesting algorithms.")
    ]
    for r_idx, (c, t, f) in enumerate(stack_data):
        stack_table.rows[r_idx].cells[0].paragraphs[0].text = c
        stack_table.rows[r_idx].cells[1].paragraphs[0].text = t
        stack_table.rows[r_idx].cells[2].paragraphs[0].text = f
    format_docx_table(stack_table, [1.5, 1.8, 3.5], [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT])
    
    doc.add_page_break()
    
    # =========================================================================
    # PAGE 6: DATA VISUALIZATION
    # =========================================================================
    add_heading_1(doc, "DATA VISUALIZATION")
    add_body_p(doc, "In alignment with Senior High School curriculum competencies in Data Visualization Software, the SeaMetrics dashboard incorporates six essential visual components designed for intuitive user interaction:")
    
    viz_table = doc.add_table(rows=7, cols=3)
    viz_data = [
        ("DASHBOARD FEATURE", "WHAT IT SHOWS", "HOW USERS CAN INTERACT WITH IT"),
        ("KPI SUMMARY CARDS", "Displays Luzon-wide aggregate indicators: Total Passengers (16.78M in 2026 Q1–Q3), Ship Calls (112.6K), RoRo Vehicles (2.68M), and Reporting Coverage.", "Cards automatically recalculate in real-time when any year, PMO, or quarterly filter is adjusted."),
        ("INTERACTIVE SLICERS / FILTERS", "Sidebar controls for Year selection (2019, 2022–2026), PMO multi-select dropdown, and quarterly timeframe selectors.", "Users can isolate specific operational horizons, compare single PMOs, or examine multi-year historical trajectories."),
        ("ANALYTICS TABS (PAX, SHIPS, RORO)", "Detailed breakdown tabs displaying time-series trends, inbound vs outbound directional distributions, and port ranking bar charts.", "Users toggle between bar charts, area charts, and sorted ranking tables, inspecting hover tooltips for exact metrics."),
        ("DYNAMIC PORT COMPARISON", "Side-by-side performance benchmarking across selected Luzon ports (e.g., Base Port of Batangas vs Base Port of Calapan).", "Users select two or more ports to contrast passenger throughput, vessel dockings, and vehicle volume on synchronized axes."),
        ("PREDICTIVE FORECAST & ERROR BOUNDS", "Displays historical quarterly series alongside backtested baseline forecasts and calibrated Q4 2026 point projections with 95% confidence intervals.", "Users inspect projected fourth-quarter volumes against upper and lower error bounds, evaluating model reliability metrics (MAPE, RMSE)."),
        ("PORT CLASSIFICATION & CARGO AUDIT", "Displays PPA administrative hierarchy (Base vs Terminal ports) and documents cargo throughput and TEU container exclusion scope.", "Users verify port classifications and review transparent ETL data quality reconciliation logs.")
    ]
    for r_idx, (f, w, h) in enumerate(viz_data):
        viz_table.rows[r_idx].cells[0].paragraphs[0].text = f
        viz_table.rows[r_idx].cells[1].paragraphs[0].text = w
        viz_table.rows[r_idx].cells[2].paragraphs[0].text = h
    format_docx_table(viz_table, [1.5, 2.7, 2.6], [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT])
    
    doc.add_page_break()
    
    # =========================================================================
    # PAGE 7: FINDINGS & EMPIRICAL INSIGHTS
    # =========================================================================
    add_heading_1(doc, "FINDING & INSIGHTS")
    
    add_heading_2(doc, "Finding 1: Multi-Year Longitudinal Growth and Post-Pandemic Mobility Rebound")
    add_body_p(doc, "Analysis of standardized 9-month windows (Q1–Q3) reveals robust post-pandemic recovery across Luzon maritime corridors. Passenger traffic expanded from 12,319,304 commuters in 2022 to 14,461,806 in 2023 (+17.39%), 16,493,372 in 2024 (+14.05%), and peaked at 17,013,983 in 2025 (+3.16%), before stabilizing at 16,784,830 in 2026 (-1.35%). Over the observed 2022–2026 baseline, passenger volume expanded by +36.25%. Full-year Luzon passenger traffic reached 22,051,885 passengers in 2025. RoRo vehicular movement expanded from 2,382,883 units in 2022 Q1–Q3 to 2,676,093 in 2026 Q1–Q3 (+12.29%). Ship calls grew from 98,393 calls in 2022 to 112,652 calls in 2026 (+14.49%). This answers Research Question 1.")
    
    add_heading_2(doc, "Finding 2: Pronounced Seasonal Volatility Aligned with Summer Peak and Habagat Trough")
    add_body_p(doc, "Monthly seasonality index calculations demonstrate extreme recurring volatility. Passenger traffic surges to an annual peak in May (Seasonality Index: 164.94; 3,030,996 monthly mean passengers) and April (Index: 134.05; 2,463,294 passengers), driven by Holy Week and summer vacations. Conversely, traffic contracts sharply in September (Seasonality Index: 65.61; 1,205,778 passengers) and July (Index: 75.16; 1,381,135 passengers) due to frequent voyage suspensions during the Southwest Monsoon (Habagat). This represents a 60.22% decline from May peak to September trough. RoRo vehicles and ship calls exhibit synchronized seasonal rhythms (May indices of 130.89 and 118.28; September indices of 81.92 and 83.89). This answers Research Question 2.")
    
    add_heading_2(doc, "Finding 3: Heavy Operational Centralization on the Batangas–Calapan Archipelago Gateway")
    add_body_p(doc, "Luzon maritime activity is profoundly centralized on the Batangas–Mindoro nautical bridge. In 2026 Q1–Q3, PMO Batangas (4,798,250 pax; 767,696 RoRo vehicles) and PMO Mindoro (4,229,377 pax; 761,428 RoRo vehicles) together accounted for 53.79% of all passenger throughput (9,027,627 commuters) and 57.14% of all RoRo vehicle volume (1,529,124 vehicles) in Luzon. The Base Port of Batangas (3,780,022 pax; 683,803 RoRo) and Base Port of Calapan (2,544,386 pax; 502,778 RoRo) handle 61.90% of all Southern Luzon base port passengers and 54.54% of base port RoRo vehicles, functioning as the vital nautical chokepoint of the archipelago. This answers Research Question 3.")
    
    add_heading_2(doc, "Finding 4: RoRo Vehicle Class Segmentation (Commercial Freight Dominance)")
    add_body_p(doc, "Disaggregating RoRo movements across PPA classifications shows that rolling traffic is dominated by Type 4 heavy freight trucks, trailers, and buses (40.20%; 1,075,789 units) and Type 2 private cars, jeeps, and vans (33.10%; 885,786 units). Type 1 motorcycles and tricycles represent 16.00% (428,175 units), while Type 3 light commercial trucks represent 10.70% (286,342 units). Heavy commercial transport accounts for over half of all rolling deck space, confirming that the Strong Republic Nautical Highway serves primarily as a rolling food and commercial supply bridge.")
    
    doc.add_page_break()
    
    # =========================================================================
    # PAGE 8: PREDICTIVE ANALYTICS & MODEL EVALUATION
    # =========================================================================
    add_heading_1(doc, "PREDICTIVE ANALYTICS & MODEL EVALUATION")
    add_body_p(doc, "Because the CY 2026 dataset concludes at the Third Quarter, short-term time-series forecasting models were evaluated to project fourth-quarter volumes. Models were rigorously evaluated via chronological backtesting on 2026 actuals (training set: 2022–2025; test set: 2026 Q1–Q3):")
    
    add_heading_2(doc, "Model Backtesting & Evaluation Benchmark (2026 Q1–Q3 Actual vs Predicted)")
    bt_table = doc.add_table(rows=7, cols=8)
    bt_data = [
        ("Model", "Target Metric", "Test Horizon", "Training Set", "MAPE", "RMSE", "MAE", "Performance"),
        ("Naive Seasonal (Y_t-4)", "Passenger Traffic", "2026 Q1–Q3", "2022–2025", "4.62%", "328,102", "259,411", "Highly Reliable (Best for Pax)"),
        ("Historical Mean", "Passenger Traffic", "2026 Q1–Q3", "2022–2025", "8.89%", "614,290", "499,320", "Moderate Baseline"),
        ("Historical Mean", "RoRo Vehicular", "2026 Q1–Q3", "2022–2025", "6.34%", "71,204", "56,589", "Highly Reliable (Best for RoRo)"),
        ("Naive Seasonal (Y_t-4)", "RoRo Vehicular", "2026 Q1–Q3", "2022–2025", "7.15%", "83,450", "63,810", "High Accuracy"),
        ("Historical Mean", "Ship Calls", "2026 Q1–Q3", "2022–2025", "5.63%", "2,410", "1,980", "Highly Reliable (Best for Ships)"),
        ("Naive Seasonal (Y_t-4)", "Ship Calls", "2026 Q1–Q3", "2022–2025", "6.81%", "2,945", "2,340", "High Accuracy")
    ]
    for r_idx, row_vals in enumerate(bt_data):
        for c_idx, val in enumerate(row_vals):
            bt_table.rows[r_idx].cells[c_idx].paragraphs[0].text = val
    format_docx_table(bt_table, [1.4, 1.1, 0.75, 0.75, 0.55, 0.65, 0.65, 1.0],
                      [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, 
                       WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.LEFT])
    
    add_heading_2(doc, "Calibrated Q4 2026 Point Forecasts and Full-Year Projections")
    add_body_p(doc, "Applying the highest-performing validated models yields the following point forecasts and 95% confidence intervals for fourth-quarter and full-year 2026:")
    
    fc_table = doc.add_table(rows=4, cols=6)
    fc_data = [
        ("Metric Indicator", "Validated Model", "Q1–Q3 Actual", "Projected Q4", "95% Confidence Interval", "Projected FY 2026"),
        ("Passenger Traffic", "Naive Seasonal Baseline", "16,784,830", "5,294,524", "[3,599,407 to 6,989,641]", "22,079,354 (+0.12% vs 2025)"),
        ("RoRo Vehicles", "Historical Quarter Mean", "2,676,093", "898,518", "[769,909 to 1,027,127]", "3,574,611 (-1.22% vs 2025)"),
        ("Ship Calls", "Historical Quarter Mean", "112,652", "36,442", "[33,628 to 39,256]", "149,094 (-0.57% vs 2025)")
    ]
    for r_idx, row_vals in enumerate(fc_data):
        for c_idx, val in enumerate(row_vals):
            fc_table.rows[r_idx].cells[c_idx].paragraphs[0].text = val
    format_docx_table(fc_table, [1.5, 1.4, 0.9, 0.9, 1.2, 0.9],
                      [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.RIGHT, 
                       WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.RIGHT])
    
    add_heading_2(doc, "Model Limitations & Boundary Conditions")
    add_body_p(doc, "Forecasting accuracy is bounded by three real-world constraints: (1) Sample Horizon: Only four fully completed annual cycles (2022–2025) exist in the modern reporting structure; (2) Weather Sensitivity: Late-quarter typhoons can cause multi-day voyage cancellations that depress actual Q4 traffic below model projections; and (3) Exogenous Shocks: Fuel price fluctuations and fare adjustments can alter travel frequency independently of historical seasonality. This answers Research Question 4.")
    
    doc.add_page_break()
    
    # =========================================================================
    # PAGE 9: CONCLUSION AND RECOMMENDATIONS
    # =========================================================================
    add_heading_1(doc, "CONCLUSION AND RECOMMENDATION")
    add_heading_2(doc, "Practical Recommendations")
    add_bullet_p(doc, "PPA Port Management Offices in Batangas and Mindoro should implement dynamic berth allocation schedules during the April–May and December holiday surges, deploying auxiliary RoRo ramps and extending terminal operating hours to accommodate the +64.94% seasonal surge.", bold_prefix="1. Dynamic Berth Scheduling & Holiday Capacity Buffers: ")
    add_bullet_p(doc, "LGUs of Batangas City and Calapan City, in coordination with PPA and DPWH, must establish designated off-port holding yards along STAR Tollway and the Western Nautical Highway prior to peak months to prevent vehicular gridlock on urban port access roads.", bold_prefix="2. Batangas–Calapan Corridor Dedicated RoRo Marshalling: ")
    add_bullet_p(doc, "Shipping lines and MARINA should schedule mandatory annual drydocking and vessel overhaul maintenance during the July–September monsoon lull (trough volume -60.22%), maximizing operational fleet availability for the high-demand summer and holiday quarters.", bold_prefix="3. Weather Resiliency & Wet-Season Maintenance Windows: ")
    add_bullet_p(doc, "PPA should transition from disconnected spreadsheet publishing to automated, API-accessible data reporting with unified column definitions across all PMOs, preventing reporting discrepancies and supporting real-time predictive analytics.", bold_prefix="4. Institutional Digitization & Unified Port Data Pipelines: ")
    
    add_heading_2(doc, "Conclusion")
    add_body_p(doc, "The SeaMetrics project demonstrates how Senior High School students can leverage public open data, modern open-source Python libraries, and AI development assistants (Google AI Studio and Antigravity) to build production-ready software solutions for national transportation infrastructure. By harmonizing 6 years of PPA maritime statistics, validating data schemas, and deploying interactive analytics, SeaMetrics provides evidence-based insights to support port planning, commuter safety, and archipelagic logistics. Future enhancements (Version 2.0) will incorporate real-time AIS vessel tracking and machine learning models driven by live weather radar APIs.")
    
    doc.add_page_break()
    
    # =========================================================================
    # PAGE 10: REFERENCES
    # =========================================================================
    add_heading_1(doc, "REFERENCES")
    add_body_p(doc, "All datasets, academic publications, technical libraries, and public documentation cited in this project report follow the APA 7th Edition style format:")
    
    refs = [
        "Asian Development Bank. (2020). The Strong Republic Nautical Highway: Impact on Philippine domestic trade and maritime transport connectivity. ADB Sustainable Development Working Paper Series. https://www.adb.org",
        "Department of Transportation - Philippines. (2023). Maritime Industry Development Plan (MIDP) 2028. Maritime Industry Authority (MARINA). https://marina.gov.ph",
        "Philippine Ports Authority. (2019). CY 2019 Annual Statistical Report: Volume 2 - Commodity Cargo Analysis. PPA Management Information Services Department. https://www.ppa.com.ph",
        "Philippine Ports Authority. (2022). CY 2022 Summary Port Statistics: Passenger, Shipcall, and RoRo Traffic. PPA Commercial Services Department. https://www.ppa.com.ph",
        "Philippine Ports Authority. (2023). CY 2023 Summary Port Statistics: Passenger, Shipcall, and RoRo Traffic. PPA Commercial Services Department. https://www.ppa.com.ph",
        "Philippine Ports Authority. (2024). CY 2024 Summary Port Statistics: Passenger, Shipcall, and RoRo Traffic. PPA Commercial Services Department. https://www.ppa.com.ph",
        "Philippine Ports Authority. (2025). CY 2025 Fourth Quarter Quarterly Statistical Report (QSR). PPA MISD. https://www.ppa.com.ph",
        "Philippine Ports Authority. (2026). CY 2026 Third Quarter Quarterly Statistical Report (QSR). PPA MISD. https://www.ppa.com.ph",
        "Plotly Technologies Inc. (2024). Plotly Express: Open-source interactive graphing library for Python [Computer software]. https://plotly.com/python/",
        "Streamlit Inc. (2024). Streamlit documentation and API reference for data applications [Software documentation]. https://docs.streamlit.io"
    ]
    for ref in refs:
        add_bullet_p(doc, ref, space_after=6)
        
    doc.add_page_break()
    
    # =========================================================================
    # PAGE 11: APPENDIX
    # =========================================================================
    add_heading_1(doc, "APPENDIX")
    add_heading_2(doc, "AI Prompt Log")
    add_body_p(doc, "Record of key prompts used in Google AI Studio (Gemini 1.5 Pro) and Antigravity to develop software logic, data cleaning algorithms, and visual components:")
    
    prompt_table = doc.add_table(rows=5, cols=2)
    prompt_data = [
        ("What Prompt Did You Ask AI?", "What Did AI Give You & How Did You Use It?"),
        ('"Design an automated Python ETL pipeline that ingests multi-year PPA Excel workbooks with varying schemas (2019 Vol 2, 2022–2024 summaries, 2025–2026 monthly facility sheets) and filters strictly for Luzon PMOs."',
         'AI provided a modular openpyxl/Pandas extraction function with dictionary-driven PMO mapping and schema normalization. We integrated this into src/data_loader.py to harmonize 6 years of maritime records.'),
        ('"How do we prevent double-counting when aggregating nested PPA port hierarchies (PMO totals vs Base Ports vs Terminal berths) in Streamlit?"',
         'AI provided hierarchy-level filtering using PPA classification tags (is_base_port, is_pmo_total). We implemented strict segregation so users can view facility-level or PMO-level data without duplication.'),
        ('"Implement a defensive zero-division handler and backtesting module for seasonal maritime forecasting without external heavy ML dependencies."',
         'AI formulated a vectorized Naive Seasonal (Y_t-4) and Historical Mean baseline with explicit MAPE/RMSE metrics and if total > 0 safety guards. We deployed it in src/analytics.py.'),
        ('"Generate a modern maritime-themed UI layout in Streamlit using a dark navy (#0F2A4A), cyan (#00CED1), and white color palette with KPI cards and Plotly charts."',
         'AI produced customized CSS injections and Plotly theme templates (plotly_dark with teal accents) which we integrated into src/app.py across 7 interactive tabs.')
    ]
    for r_idx, (q, a) in enumerate(prompt_data):
        prompt_table.rows[r_idx].cells[0].paragraphs[0].text = q
        prompt_table.rows[r_idx].cells[1].paragraphs[0].text = a
    format_docx_table(prompt_table, [2.5, 4.3], [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT])
    
    add_styled_paragraph(doc, "", space_after=6)
    add_heading_2(doc, "Graphical User Interface (GUI)")
    add_body_p(doc, "The SeaMetrics web application GUI features a modern maritime dark navy (#0F2A4A) layout configured with a sidebar control panel (Year multi-select, PMO filter, Quarter range) and a 7-tab main display grid containing dynamic KPI cards, multi-year time-series trendlines, inbound/outbound directional breakdowns, port ranking charts, Batangas–Calapan corridor deep-dives, and backtested predictive forecasting error bounds:")
    
    preview_img_path = "paper/seametrics_gui_preview.png"
    if os.path.exists(preview_img_path):
        doc.add_picture(preview_img_path, width=Inches(6.5))
        p_cap = add_styled_paragraph(doc, "Figure 1: SeaMetrics Interactive Maritime Analytics & Predictive Modeling Dashboard GUI.", 
                                     font_size=9.5, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=0)
    
    doc.save(output_path)
    print(f"DOCX paper successfully created at: {output_path} ({os.path.getsize(output_path):,} bytes)")


# -------------------------------------------------------------------------
# REPORTLAB PDF BUILDER
# -------------------------------------------------------------------------

def build_pdf_paper(output_path="paper/SeaMetrics_Final_Paper.pdf"):
    print(f"Building PDF: {output_path}...")
    
    # Target 8.5 x 13 inches (Folio / Philippine Legal bond paper)
    doc = SimpleDocTemplate(
        output_path,
        pagesize=PAGE_SIZE_FOLIO,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    # Printable width: 612 - 108 = 504 pt (7.0 inches)
    PRINTABLE_WIDTH = 504
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    style_cover_dept = ParagraphStyle(
        'CoverDept',
        fontName=FONT_REGULAR,
        fontSize=11,
        leading=14,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#000000'),
        spaceAfter=2
    )
    style_cover_dept_bold = ParagraphStyle(
        'CoverDeptBold',
        fontName=FONT_BOLD,
        fontSize=11,
        leading=14,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#000000'),
        spaceAfter=2
    )
    style_cover_school = ParagraphStyle(
        'CoverSchool',
        fontName=FONT_BOLD,
        fontSize=12,
        leading=15,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#000000'),
        spaceAfter=2
    )
    style_cover_sub_header = ParagraphStyle(
        'CoverSubHeader',
        fontName=FONT_ITALIC,
        fontSize=11.5,
        leading=15,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#222222'),
        spaceAfter=4
    )
    style_cover_track = ParagraphStyle(
        'CoverTrack',
        fontName=FONT_BOLD,
        fontSize=13,
        leading=16,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#0F2A4A'),
        spaceAfter=24
    )
    style_cover_title = ParagraphStyle(
        'CoverTitle',
        fontName=FONT_BOLD,
        fontSize=15.5,
        leading=20,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#0F2A4A'),
        spaceAfter=30
    )
    style_cover_authors_head = ParagraphStyle(
        'CoverAuthorsHead',
        fontName=FONT_ITALIC,
        fontSize=11,
        leading=14,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#444444'),
        spaceAfter=6
    )
    style_cover_author = ParagraphStyle(
        'CoverAuthor',
        fontName=FONT_BOLD,
        fontSize=11.5,
        leading=15,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#000000'),
        spaceAfter=2
    )
    
    style_h1 = ParagraphStyle(
        'SectionH1',
        fontName=FONT_BOLD,
        fontSize=12.5,
        leading=16,
        alignment=TA_LEFT,
        textColor=colors.HexColor('#0F2A4A'),
        spaceBefore=10,
        spaceAfter=4
    )
    style_h2 = ParagraphStyle(
        'SectionH2',
        fontName=FONT_BOLD,
        fontSize=11,
        leading=14,
        alignment=TA_LEFT,
        textColor=colors.HexColor('#0F2A4A'),
        spaceBefore=7,
        spaceAfter=3
    )
    style_body = ParagraphStyle(
        'BodyJustify',
        fontName=FONT_REGULAR,
        fontSize=10,
        leading=13,
        alignment=TA_JUSTIFY,
        textColor=colors.HexColor('#111111'),
        spaceAfter=4
    )
    style_bullet = ParagraphStyle(
        'BulletJustify',
        fontName=FONT_REGULAR,
        fontSize=9.5,
        leading=12.5,
        alignment=TA_JUSTIFY,
        leftIndent=15,
        textColor=colors.HexColor('#111111'),
        spaceAfter=3
    )
    style_table_cell = ParagraphStyle(
        'TableCell',
        fontName=FONT_REGULAR,
        fontSize=8.5,
        leading=11,
        alignment=TA_LEFT,
        textColor=colors.HexColor('#111111')
    )
    style_table_cell_center = ParagraphStyle(
        'TableCellCenter',
        fontName=FONT_REGULAR,
        fontSize=8.5,
        leading=11,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#111111')
    )
    style_table_cell_right = ParagraphStyle(
        'TableCellRight',
        fontName=FONT_REGULAR,
        fontSize=8.5,
        leading=11,
        alignment=TA_RIGHT,
        textColor=colors.HexColor('#111111')
    )
    style_table_header = ParagraphStyle(
        'TableHeader',
        fontName=FONT_BOLD,
        fontSize=9,
        leading=11.5,
        alignment=TA_CENTER,
        textColor=colors.white
    )
    style_table_header_left = ParagraphStyle(
        'TableHeaderLeft',
        fontName=FONT_BOLD,
        fontSize=9,
        leading=11.5,
        alignment=TA_LEFT,
        textColor=colors.white
    )
    style_table_cell_bold = ParagraphStyle(
        'TableCellBold',
        fontName=FONT_BOLD,
        fontSize=8.5,
        leading=11,
        alignment=TA_LEFT,
        textColor=colors.HexColor('#0F2A4A')
    )
    style_exec = ParagraphStyle(
        'ExecText',
        fontName=FONT_REGULAR,
        fontSize=9.2,
        leading=12,
        alignment=TA_JUSTIFY,
        textColor=colors.HexColor('#111111'),
        spaceAfter=4
    )

    story = []
    
    # =========================================================================
    # PAGE 1: COVER PAGE
    # =========================================================================
    story.append(Paragraph("Republic of the Philippines", style_cover_dept))
    story.append(Paragraph("Department of Education", style_cover_dept_bold))
    story.append(Paragraph("MIMAROPA REGION", style_cover_dept_bold))
    story.append(Paragraph("Division of Oriental Mindoro", style_cover_dept))
    story.append(Paragraph("LEUTEBORO NATIONAL HIGH SCHOOL", style_cover_school))
    story.append(Paragraph("Leuteboro, Socorro, Oriental Mindoro", style_cover_sub_header))
    story.append(Spacer(1, 35))
    
    story.append(Paragraph("Software Development Project Paper in", style_cover_sub_header))
    story.append(Paragraph("FUNDAMENTALS OF DATA ANALYTICS", style_cover_track))
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("SeaMetrics: A Data-Driven Analysis and Predictive Modeling of Passenger Traffic, Vessel Activity, and RoRo Transportation Trends Across Ports in Luzon, Philippines (2019, 2022–2026)", style_cover_title))
    story.append(Spacer(1, 35))
    
    story.append(Paragraph("Submitted by:", style_cover_authors_head))
    story.append(Paragraph("JUAN M. DELA CRUZ", style_cover_author))
    story.append(Paragraph("MARIA S. SANTOS", style_cover_author))
    story.append(Paragraph("ANTONIO A. LUNA", style_cover_author))
    story.append(Paragraph("ELENA R. RAMOS", style_cover_author))
    story.append(Paragraph("Grade 12 Senior High School — Technical-Vocational-Livelihood / STEM Track", style_cover_sub_header))
    story.append(Spacer(1, 35))
    
    story.append(Paragraph("Submitted to:", style_cover_authors_head))
    story.append(Paragraph("ALDRIN D. MAGTIBAY", style_cover_author))
    story.append(Paragraph("Teacher V, Subject Teacher", style_cover_sub_header))
    story.append(Spacer(1, 30))
    
    story.append(Paragraph("November 2026", style_cover_author))
    story.append(PageBreak())
    
    # =========================================================================
    # PAGE 2: PROJECT METADATA & EXECUTIVE SUMMARY
    # =========================================================================
    story.append(Paragraph("PROJECT METADATA & TEAM ROLES", style_h1))
    
    meta_pdf_data = [
        [Paragraph("Field", style_table_header_left), Paragraph("Project Details", style_table_header_left)],
        [Paragraph("Project Title", style_table_cell_bold), 
         Paragraph("SeaMetrics: A Data-Driven Analysis and Predictive Modeling of Passenger Traffic, Vessel Activity, and RoRo Transportation Trends Across Ports in Luzon, Philippines (2019, 2022–2026)", style_table_cell)],
        [Paragraph("Section & Group No.", style_table_cell_bold), 
         Paragraph("Grade 12 TVL / STEM — Section A, Group #1", style_table_cell)],
        [Paragraph("Team Members & Roles", style_table_cell_bold), 
         Paragraph("• <b>Juan Dela Cruz</b> — Software & Coding Lead (ETL Pipeline, Schema Standardization, Validation)<br/>• <b>Maria Santos</b> — Dashboard & Visuals Lead (Streamlit GUI, Plotly Visualizations, UI/UX)<br/>• <b>Antonio Luna</b> — Data Analyst & Storyteller (Time-Series Modeling, Seasonality Indices, Corridor Analysis)<br/>• <b>Elena Ramos</b> — Paper & Documentation Lead (Final Paper, Academic Writing, Quality Assurance)", style_table_cell)],
        [Paragraph("Dataset Name & Source", style_table_cell_bold), 
         Paragraph("Philippine Ports Authority (PPA) Port Statistics (CY 2019 Vol. 2, CY 2022, 2023, 2024 Summary Port Statistics, CY 2025 Q4 QSR, CY 2026 Q3 QSR)", style_table_cell)],
        [Paragraph("Primary AI Tool Used", style_table_cell_bold), 
         Paragraph("Google AI Studio (Gemini 1.5 Pro) / Antigravity AI Assistant", style_table_cell)]
    ]
    t_meta = Table(meta_pdf_data, colWidths=[130, 374])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F2A4A')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D0D7DE')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F6F8FA')])
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 10))
    
    # Executive Summary Box
    exec_content = [
        Paragraph("<para align='center'><b>EXECUTIVE SUMMARY</b></para>", ParagraphStyle('ExecHead', fontName=FONT_BOLD, fontSize=11, leading=14, textColor=colors.HexColor('#0F2A4A'), spaceAfter=5)),
        Paragraph("Maritime transportation constitutes the vital economic, logistical, and commuter circulatory system of the Philippine archipelago. Across Luzon, regional gateways facilitate the transit of tens of millions of passengers and millions of commercial and private vehicles annually. The maritime corridor linking Batangas Port (CALABARZON) and Calapan Port (Oriental Mindoro) serves as the primary nautical bridge connecting mainland Luzon with the MIMAROPA and Western Visayas island provinces. Despite public dissemination of annual and quarterly statistical reports by the Philippine Ports Authority (PPA), these records are distributed across dense, disconnected tabular workbooks that lack multi-year consolidation, automated validation, interactive visualization, and predictive modeling capabilities. This operational bottleneck creates delays for local government units (LGUs), maritime transport regulators, and terminal operators who must anticipate seasonal passenger surges, manage severe vehicle congestion during holiday peaks, and mitigate weather-induced transport disruptions.", style_exec),
        Paragraph("To bridge this operational and analytical divide, this study developed SeaMetrics, an interactive web-based data analytics and predictive modeling software application built with Python, Streamlit, and Plotly Express, designed using Google AI Studio (Gemini 1.5 Pro) and Antigravity as an AI development co-pilot. SeaMetrics harmonizes official PPA port statistics across a 6-year historical horizon (2019, 2022–2026). The software incorporates an automated Extract-Transform-Load (ETL) pipeline that parses multi-year workbooks, verifies schema integrity, enforces strict geographic boundaries (isolating verified Port Management Offices in Luzon while excluding 14 non-Luzon PMOs), standardizes naming variations, protects against zero-division errors, and enforces fair reporting-period comparisons by evaluating matching 9-month windows (Q1–Q3) across years. Furthermore, in strict adherence to data integrity rules, the 2019 dataset—which corresponds to Volume 2 (Commodity Cargo Analysis)—is ingested with its authentic Luzon port hierarchy while preserving traffic counts as unrecorded (NaN) rather than fabricating non-existent numbers.", style_exec),
        Paragraph("Data analysis revealed four critical findings: (1) Passenger traffic experienced sustained post-pandemic expansion, growing +36.25% across matching Q1–Q3 periods from 12.32M in 2022 to 16.78M in 2026, while 2025 full-year passenger throughput reached 22.05M; (2) Maritime mobility exhibits severe seasonal volatility, peaking during May summer vacations (Seasonality Index: 164.94; 3.03M monthly passengers) before contracting by 60.22% in September (Index: 65.61; 1.21M passengers) due to Southwest Monsoon (Habagat) voyage suspensions; (3) Port operations are intensely centralized, with PMO Batangas and PMO Mindoro handling 53.79% of all Luzon passengers (9.03M) and 57.14% of all RoRo vehicles (1.53M) in 2026 Q1–Q3; and (4) Rolling traffic is dominated by commercial freight, with Type 4 heavy cargo trucks/buses accounting for 40.20% (1.08M units) and Type 2 passenger vehicles accounting for 33.10% (885K units). Backtesting validated that a Naive Seasonal Baseline achieved 4.62% MAPE for passenger traffic, forecasting 5.29M passengers in Q4 2026 (projected FY 2026: 22.08M). We recommend: (a) designating off-port RoRo staging areas in Batangas and Calapan by early March and late November, (b) establishing synchronized inter-agency digital e-ticketing across MARINA and PPA, and (c) instituting priority nighttime boarding windows for agricultural food freight.", style_exec)
    ]
    t_exec = Table([[exec_content]], colWidths=[504])
    t_exec.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F7FAFC')),
        ('BOX', (0,0), (-1,-1), 1.2, colors.HexColor('#0F2A4A')),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_exec)
    story.append(PageBreak())
    
    # =========================================================================
    # PAGE 3: RATIONALE, PROBLEM STATEMENT, DATASET SUMMARY
    # =========================================================================
    story.append(Paragraph("RATIONALE", style_h1))
    story.append(Paragraph("The Philippines' geographic fragmentation into more than 7,100 islands makes maritime transportation an indispensable foundation of daily commuter travel and commerce. Under the framework of the Strong Republic Nautical Highway (SRNH), roll-on/roll-off (RoRo) ferry services replace fixed bridges to connect provincial road networks. For island provinces such as Oriental Mindoro, Occidental Mindoro, Marinduque, Romblon, and Palawan, maritime corridors connecting to mainland Luzon are irreplaceable lifelines. Batangas Port functions as the industrial and logistical gateway of Region IV-A (CALABARZON), while Calapan Port serves as the primary commercial and agricultural entry point for Region IV-B (MIMAROPA).", style_body))
    
    story.append(Paragraph("<b>The Operational Challenge:</b> Traditional public surveillance records are distributed as static CSV files or PDF bulletins. Public health and transportation administrators must manually clean, sort, and calculate efficiency metrics, delaying rapid response. Furthermore, existing PPA statistical archives suffer from structural asymmetry across years, reporting period inconsistencies (interim 2026 Q3 data vs completed 12-month calendar years), and nested hierarchy aggregation traps that duplicate records up to three times if summaries and berth-level rows are blindly aggregated.", style_body))
    story.append(Paragraph("<b>The Solution Approach:</b> Automated data analytics bridges the divide between static administrative records and dynamic strategic decision-making. By deploying an automated processing script connected to an intuitive graphical user interface (GUI), port personnel, shipping lines, and local planners can upload updated records and instantly observe updated regional risk profiles, multi-year trends, corridor comparisons, and predictive forecasts.", style_body))
    story.append(Paragraph("<b>Target Stakeholders:</b> (1) Port Regulators and Coast Guard Officers (PPA & PCG) requiring localized risk data to allocate berths and manage passenger safety; (2) Local Government Units (Provincial Governments of Batangas and Oriental Mindoro) scheduling off-port traffic holding areas; (3) Ferry Operators & Logistics Freight Forwarders optimizing fleet deployment; and (4) Senior High School Students and Researchers studying applied maritime data analytics.", style_body))
    
    story.append(Paragraph("STATEMENT OF THE PROBLEM", style_h1))
    story.append(Paragraph("The primary objective of this project is to develop an automated software application that ingests, cleans, calculates, and visually presents Philippine public maritime port statistics from 2019 to 2026 to support data-driven transport monitoring. Specifically, the project seeks to answer the following research questions:", style_body))
    story.append(Paragraph("• <b>Research Question 1 (Temporal Pattern & Post-Pandemic Rebound):</b> What has been the multi-year trajectory of passenger traffic, vessel calls, and RoRo vehicular traffic across Luzon ports from 2019 to 2026, and how do matching 9-month periods (Q1–Q3) compare across consecutive years?", style_bullet))
    story.append(Paragraph("• <b>Research Question 2 (Seasonal Volatility & Weather Disruptions):</b> What are the recurring monthly and quarterly fluctuations in maritime mobility, and how does the summer travel peak (Holy Week / May) contrast quantitatively with the monsoon-induced contraction (July–September Habagat)?", style_bullet))
    story.append(Paragraph("• <b>Research Question 3 (Geographic Concentration & Corridor Centrality):</b> Which Port Management Offices and base ports exhibit disproportionate operational concentration, and how dominant is the Batangas–Calapan nautical bridge relative to total Luzon traffic?", style_bullet))
    story.append(Paragraph("• <b>Research Question 4 (Predictive Modeling & Operational Forecasting):</b> How accurately can short-term time-series models project missing fourth-quarter (Q4 2026) port volumes, and what are the empirical error bounds under backtested historical evaluation?", style_bullet))
    
    story.append(Paragraph("DATASET SUMMARY", style_h1))
    story.append(Paragraph("The dataset utilized for this project was obtained from the official Philippine Ports Authority (PPA) Statistical Archives. It spans a 6-year multi-year horizon comprising: (1) CY 2019 Annual Statistical Report Vol. 2 (25 PMO workbooks, commodity focus, authentic Luzon hierarchy with traffic counts preserved as unrecorded NaN); (2) CY 2022–2024 Summary Port Statistics (Quarterly PMO-level aggregates for full calendar years); (3) CY 2025 Fourth Quarter QSR (Full-year monthly detailed operations across 150 terminal facilities); and (4) CY 2026 Third Quarter QSR (Interim 9-month detailed operations through September 2026).", style_body))
    story.append(PageBreak())
    
    # =========================================================================
    # PAGE 4: VARIABLE DICTIONARY
    # =========================================================================
    story.append(Paragraph("VARIABLE DICTIONARY", style_h1))
    story.append(Paragraph("The unified SeaMetrics data schema defines standardized operational variables across passenger, vessel, and RoRo transportation categories across all reporting years:", style_body))
    
    var_pdf_rows = [
        [Paragraph("Variable Name", style_table_header_left), Paragraph("Metric Category", style_table_header_left), 
         Paragraph("Data Type", style_table_header), Paragraph("Unit / Scale", style_table_header), Paragraph("Description & Valid Range", style_table_header_left)],
        [Paragraph("Year", style_table_cell_bold), Paragraph("Temporal Identifier", style_table_cell), Paragraph("Integer", style_table_cell_center), Paragraph("Calendar Year", style_table_cell_center), Paragraph("Reporting calendar year (2019, 2022, 2023, 2024, 2025, 2026).", style_table_cell)],
        [Paragraph("Quarter", style_table_cell_bold), Paragraph("Temporal Identifier", style_table_cell), Paragraph("String", style_table_cell_center), Paragraph("Fiscal Quarter", style_table_cell_center), Paragraph("Reporting fiscal quarter (Q1, Q2, Q3, Q4).", style_table_cell)],
        [Paragraph("Month", style_table_cell_bold), Paragraph("Temporal Identifier", style_table_cell), Paragraph("String", style_table_cell_center), Paragraph("Calendar Month", style_table_cell_center), Paragraph("Reporting calendar month (January to December; 2025–2026 granularity).", style_table_cell)],
        [Paragraph("PMO", style_table_cell_bold), Paragraph("Geographic Identifier", style_table_cell), Paragraph("String", style_table_cell_center), Paragraph("Port Authority Unit", style_table_cell_center), Paragraph("Port Management Office in Luzon (e.g., Batangas, Mindoro, Bataan/Aurora).", style_table_cell)],
        [Paragraph("Port_Name", style_table_cell_bold), Paragraph("Facility Identifier", style_table_cell), Paragraph("String", style_table_cell_center), Paragraph("Terminal Facility", style_table_cell_center), Paragraph("Specific terminal or base port facility (e.g., Base Port of Batangas, Calapan).", style_table_cell)],
        [Paragraph("Port_Class", style_table_cell_bold), Paragraph("Administrative", style_table_cell), Paragraph("String", style_table_cell_center), Paragraph("Classification", style_table_cell_center), Paragraph("PPA classification: Base Port, Terminal Port, or Other Berth.", style_table_cell)],
        [Paragraph("Pax_Disembarked", style_table_cell_bold), Paragraph("Passenger Mobility", style_table_cell), Paragraph("Integer", style_table_cell_center), Paragraph("Commuters (Inbound)", style_table_cell_center), Paragraph("Number of arriving passengers entering terminal from vessel (≥ 0).", style_table_cell)],
        [Paragraph("Pax_Embarked", style_table_cell_bold), Paragraph("Passenger Mobility", style_table_cell), Paragraph("Integer", style_table_cell_center), Paragraph("Commuters (Outbound)", style_table_cell_center), Paragraph("Number of departing passengers boarding vessel to destination (≥ 0).", style_table_cell)],
        [Paragraph("Pax_Total", style_table_cell_bold), Paragraph("Passenger Mobility", style_table_cell), Paragraph("Integer", style_table_cell_center), Paragraph("Total Commuters", style_table_cell_center), Paragraph("Total passenger throughput: Pax_Disembarked + Pax_Embarked (≥ 0).", style_table_cell)],
        [Paragraph("ShipCalls_Domestic", style_table_cell_bold), Paragraph("Vessel Activity", style_table_cell), Paragraph("Integer", style_table_cell_center), Paragraph("Vessel Dockings", style_table_cell_center), Paragraph("Domestic commercial vessel calls docked at berth (≥ 0).", style_table_cell)],
        [Paragraph("ShipCalls_Foreign", style_table_cell_bold), Paragraph("Vessel Activity", style_table_cell), Paragraph("Integer", style_table_cell_center), Paragraph("Vessel Dockings", style_table_cell_center), Paragraph("International commercial vessel calls (≥ 0; segregated from domestic).", style_table_cell)],
        [Paragraph("ShipCalls_Total", style_table_cell_bold), Paragraph("Vessel Activity", style_table_cell), Paragraph("Integer", style_table_cell_center), Paragraph("Total Dockings", style_table_cell_center), Paragraph("Total commercial vessel calls: Domestic + Foreign dockings (≥ 0).", style_table_cell)],
        [Paragraph("RoRo_Inward", style_table_cell_bold), Paragraph("Vehicular Transport", style_table_cell), Paragraph("Integer", style_table_cell_center), Paragraph("Rolling Vehicles", style_table_cell_center), Paragraph("Inbound rolling cargo vehicles discharged from RoRo vessel (≥ 0).", style_table_cell)],
        [Paragraph("RoRo_Outward", style_table_cell_bold), Paragraph("Vehicular Transport", style_table_cell), Paragraph("Integer", style_table_cell_center), Paragraph("Rolling Vehicles", style_table_cell_center), Paragraph("Outbound rolling cargo vehicles loaded onto RoRo vessel (≥ 0).", style_table_cell)],
        [Paragraph("RoRo_Total", style_table_cell_bold), Paragraph("Vehicular Transport", style_table_cell), Paragraph("Integer", style_table_cell_center), Paragraph("Total Rolling Units", style_table_cell_center), Paragraph("Total RoRo vehicles: RoRo_Inward + RoRo_Outward (≥ 0).", style_table_cell)],
        [Paragraph("RoRo_Type1 to Type4", style_table_cell_bold), Paragraph("Vehicular Class", style_table_cell), Paragraph("Integer", style_table_cell_center), Paragraph("Units per Class", style_table_cell_center), Paragraph("PPA RoRo vehicle classes: Type 1 (2-wheelers), Type 2 (Cars), Type 3 (Light Vans), Type 4 (Heavy Freight/Buses).", style_table_cell)]
    ]
    t_var = Table(var_pdf_rows, colWidths=[100, 85, 60, 80, 179])
    t_var.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F2A4A')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D0D7DE')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F6F8FA')])
    ]))
    story.append(t_var)
    story.append(PageBreak())
    
    # =========================================================================
    # PAGE 5: FRAMEWORK AND TOOLS & TECH STACK
    # =========================================================================
    story.append(Paragraph("FRAMEWORK", style_h1))
    story.append(Paragraph("Automatic Data Steps", style_h2))
    story.append(Paragraph("We developed a web-based software application in Python using Streamlit that automatically performs four key data processing operations whenever datasets are loaded:", style_body))
    story.append(Paragraph("• <b>Automatic Multi-Workbook Ingestion & Schema Alignment:</b> The pipeline programmatically parses multi-year Excel workbooks, dynamically identifies sheet structures (summary sheets in 2022–2024 vs multi-tab facility sheets in 2025–2026), and normalizes column headers into a unified snake_case schema.", style_bullet))
    story.append(Paragraph("• <b>Strict Geographic Filtering & Defensive Zero-Division Guards:</b> The code enforces strict geographic validation by filtering records to verified Luzon Port Management Offices, excluding 14 non-Luzon PMOs. Missing cells are handled defensively—preserving unrecorded 2019 Volume 2 values as NaN rather than fabricating zeros—and mathematical computations incorporate explicit guard logic (if total > 0) to prevent runtime ZeroDivisionError exceptions.", style_bullet))
    story.append(Paragraph("• <b>Standardized Period Normalization:</b> To resolve the reporting period asymmetry between the interim 2026 report (Q3) and preceding full calendar years (Q4), the system automatically slices datasets into standardized 9-month windows (Q1–Q3) to ensure statistically sound, apples-to-apples longitudinal comparisons.", style_bullet))
    story.append(Paragraph("• <b>Automated Computation Logic & Predictive Modeling:</b> The software automatically computes derived traffic indicators, directional inbound/outbound ratios, monthly seasonality indices, and chronological time-series baseline forecasts with 95% confidence intervals.", style_bullet))
    
    story.append(Spacer(1, 4))
    story.append(Paragraph("Tools & Tech Stack", style_h2))
    stack_pdf_rows = [
        [Paragraph("Component Layer", style_table_header_left), Paragraph("Technology Choice", style_table_header_left), Paragraph("Functional Contribution", style_table_header_left)],
        [Paragraph("Language & Runtime", style_table_cell_bold), Paragraph("Python 3.11", style_table_cell), Paragraph("Core programming environment for script logic, data structures, and mathematical modeling.", style_table_cell)],
        [Paragraph("Data Processing Library", style_table_cell_bold), Paragraph("Pandas & OpenPyXL", style_table_cell), Paragraph("High-performance tabular transformations, multi-workbook ingestion, and aggregation.", style_table_cell)],
        [Paragraph("Web GUI Framework", style_table_cell_bold), Paragraph("Streamlit Framework", style_table_cell), Paragraph("Renders interactive web interface, sidebar filters, layout columns, and KPI metric cards.", style_table_cell)],
        [Paragraph("Visualization Library", style_table_cell_bold), Paragraph("Plotly Express & Graph Objects", style_table_cell), Paragraph("Generates dynamic time-series line charts, grouped bar charts, and interactive hover tooltips.", style_table_cell)],
        [Paragraph("Document & PDF Compilation", style_table_cell_bold), Paragraph("Python-Docx & ReportLab", style_table_cell), Paragraph("Programmatically compiles formal DOCX and PDF research publications matching DepEd standards.", style_table_cell)],
        [Paragraph("AI Development Co-Pilot", style_table_cell_bold), Paragraph("Google AI Studio (Gemini 1.5 Pro) / Antigravity", style_table_cell), Paragraph("Accelerates architecture design, regex schema cleaning, and backtesting algorithms.", style_table_cell)]
    ]
    t_stack = Table(stack_pdf_rows, colWidths=[115, 125, 264])
    t_stack.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F2A4A')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D0D7DE')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F6F8FA')])
    ]))
    story.append(t_stack)
    story.append(PageBreak())
    
    # =========================================================================
    # PAGE 6: DATA VISUALIZATION
    # =========================================================================
    story.append(Paragraph("DATA VISUALIZATION", style_h1))
    story.append(Paragraph("In alignment with Senior High School curriculum competencies in Data Visualization Software, the SeaMetrics dashboard incorporates six essential visual components designed for intuitive user interaction:", style_body))
    
    viz_pdf_rows = [
        [Paragraph("DASHBOARD FEATURE", style_table_header_left), Paragraph("WHAT IT SHOWS", style_table_header_left), Paragraph("HOW USERS CAN INTERACT WITH IT", style_table_header_left)],
        [Paragraph("KPI SUMMARY CARDS", style_table_cell_bold), 
         Paragraph("Displays Luzon-wide aggregate indicators: Total Passengers (16.78M in 2026 Q1–Q3), Ship Calls (112.6K), RoRo Vehicles (2.68M), and Reporting Coverage.", style_table_cell), 
         Paragraph("Cards automatically recalculate in real-time when any year, PMO, or quarterly filter is adjusted.", style_table_cell)],
        [Paragraph("INTERACTIVE SLICERS / FILTERS", style_table_cell_bold), 
         Paragraph("Sidebar controls for Year selection (2019, 2022–2026), PMO multi-select dropdown, and quarterly timeframe selectors.", style_table_cell), 
         Paragraph("Users can isolate specific operational horizons, compare single PMOs, or examine multi-year historical trajectories.", style_table_cell)],
        [Paragraph("ANALYTICS TABS (PAX, SHIPS, RORO)", style_table_cell_bold), 
         Paragraph("Detailed breakdown tabs displaying time-series trends, inbound vs outbound directional distributions, and port ranking bar charts.", style_table_cell), 
         Paragraph("Users toggle between bar charts, area charts, and sorted ranking tables, inspecting hover tooltips for exact metrics.", style_table_cell)],
        [Paragraph("DYNAMIC PORT COMPARISON", style_table_cell_bold), 
         Paragraph("Side-by-side performance benchmarking across selected Luzon ports (e.g., Base Port of Batangas vs Base Port of Calapan).", style_table_cell), 
         Paragraph("Users select two or more ports to contrast passenger throughput, vessel dockings, and vehicle volume on synchronized axes.", style_table_cell)],
        [Paragraph("PREDICTIVE FORECAST & ERROR BOUNDS", style_table_cell_bold), 
         Paragraph("Displays historical quarterly series alongside backtested baseline forecasts and calibrated Q4 2026 point projections with 95% confidence intervals.", style_table_cell), 
         Paragraph("Users inspect projected fourth-quarter volumes against upper and lower error bounds, evaluating model reliability metrics (MAPE, RMSE).", style_table_cell)],
        [Paragraph("PORT CLASSIFICATION & CARGO AUDIT", style_table_cell_bold), 
         Paragraph("Displays PPA administrative hierarchy (Base vs Terminal ports) and documents cargo throughput and TEU container exclusion scope.", style_table_cell), 
         Paragraph("Users verify port classifications and review transparent ETL data quality reconciliation logs.", style_table_cell)]
    ]
    t_viz = Table(viz_pdf_rows, colWidths=[110, 195, 199])
    t_viz.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F2A4A')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D0D7DE')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F6F8FA')])
    ]))
    story.append(t_viz)
    story.append(PageBreak())
    
    # =========================================================================
    # PAGE 7: FINDINGS & EMPIRICAL INSIGHTS
    # =========================================================================
    story.append(Paragraph("FINDING & INSIGHTS", style_h1))
    
    story.append(Paragraph("Finding 1: Multi-Year Longitudinal Growth and Post-Pandemic Mobility Rebound", style_h2))
    story.append(Paragraph("Analysis of standardized 9-month windows (Q1–Q3) reveals robust post-pandemic recovery across Luzon maritime corridors. Passenger traffic expanded from 12,319,304 commuters in 2022 to 14,461,806 in 2023 (+17.39%), 16,493,372 in 2024 (+14.05%), and peaked at 17,013,983 in 2025 (+3.16%), before stabilizing at 16,784,830 in 2026 (-1.35%). Over the observed 2022–2026 baseline, passenger volume expanded by +36.25%. Full-year Luzon passenger traffic reached 22,051,885 passengers in 2025. RoRo vehicular movement expanded from 2,382,883 units in 2022 Q1–Q3 to 2,676,093 in 2026 Q1–Q3 (+12.29%). Ship calls grew from 98,393 calls in 2022 to 112,652 calls in 2026 (+14.49%). This answers Research Question 1.", style_body))
    
    story.append(Paragraph("Finding 2: Pronounced Seasonal Volatility Aligned with Summer Peak and Habagat Trough", style_h2))
    story.append(Paragraph("Monthly seasonality index calculations demonstrate extreme recurring volatility. Passenger traffic surges to an annual peak in May (Seasonality Index: 164.94; 3,030,996 monthly mean passengers) and April (Index: 134.05; 2,463,294 passengers), driven by Holy Week and summer vacations. Conversely, traffic contracts sharply in September (Seasonality Index: 65.61; 1,205,778 passengers) and July (Index: 75.16; 1,381,135 passengers) due to frequent voyage suspensions during the Southwest Monsoon (Habagat). This represents a 60.22% decline from May peak to September trough. RoRo vehicles and ship calls exhibit synchronized seasonal rhythms (May indices of 130.89 and 118.28; September indices of 81.92 and 83.89). This answers Research Question 2.", style_body))
    
    story.append(Paragraph("Finding 3: Heavy Operational Centralization on the Batangas–Calapan Archipelago Gateway", style_h2))
    story.append(Paragraph("Luzon maritime activity is profoundly centralized on the Batangas–Mindoro nautical bridge. In 2026 Q1–Q3, PMO Batangas (4,798,250 pax; 767,696 RoRo vehicles) and PMO Mindoro (4,229,377 pax; 761,428 RoRo vehicles) together accounted for 53.79% of all passenger throughput (9,027,627 commuters) and 57.14% of all RoRo vehicle volume (1,529,124 vehicles) in Luzon. The Base Port of Batangas (3,780,022 pax; 683,803 RoRo) and Base Port of Calapan (2,544,386 pax; 502,778 RoRo) handle 61.90% of all Southern Luzon base port passengers and 54.54% of base port RoRo vehicles, functioning as the vital nautical chokepoint of the archipelago. This answers Research Question 3.", style_body))
    
    story.append(Paragraph("Finding 4: RoRo Vehicle Class Segmentation (Commercial Freight Dominance)", style_h2))
    story.append(Paragraph("Disaggregating RoRo movements across PPA classifications shows that rolling traffic is dominated by Type 4 heavy freight trucks, trailers, and buses (40.20%; 1,075,789 units) and Type 2 private cars, jeeps, and vans (33.10%; 885,786 units). Type 1 motorcycles and tricycles represent 16.00% (428,175 units), while Type 3 light commercial trucks represent 10.70% (286,342 units). Heavy commercial transport accounts for over half of all rolling deck space, confirming that the Strong Republic Nautical Highway serves primarily as a rolling food and commercial supply bridge.", style_body))
    story.append(PageBreak())
    
    # =========================================================================
    # PAGE 8: PREDICTIVE ANALYTICS & MODEL EVALUATION
    # =========================================================================
    story.append(Paragraph("PREDICTIVE ANALYTICS & MODEL EVALUATION", style_h1))
    story.append(Paragraph("Because the CY 2026 dataset concludes at the Third Quarter, short-term time-series forecasting models were evaluated to project fourth-quarter volumes. Models were rigorously evaluated via chronological backtesting on 2026 actuals (training set: 2022–2025; test set: 2026 Q1–Q3):", style_body))
    
    story.append(Paragraph("Model Backtesting & Evaluation Benchmark (2026 Q1–Q3 Actual vs Predicted)", style_h2))
    bt_pdf_rows = [
        [Paragraph("Model", style_table_header_left), Paragraph("Target Metric", style_table_header_left), 
         Paragraph("Test Horizon", style_table_header), Paragraph("Training Set", style_table_header), 
         Paragraph("MAPE", style_table_header), Paragraph("RMSE", style_table_header), Paragraph("MAE", style_table_header), 
         Paragraph("Performance", style_table_header_left)],
        [Paragraph("Naive Seasonal (Y_t-4)", style_table_cell_bold), Paragraph("Passenger Traffic", style_table_cell), Paragraph("2026 Q1–Q3", style_table_cell_center), Paragraph("2022–2025", style_table_cell_center), Paragraph("4.62%", style_table_cell_right), Paragraph("328,102", style_table_cell_right), Paragraph("259,411", style_table_cell_right), Paragraph("Highly Reliable (Best for Pax)", style_table_cell)],
        [Paragraph("Historical Mean", style_table_cell_bold), Paragraph("Passenger Traffic", style_table_cell), Paragraph("2026 Q1–Q3", style_table_cell_center), Paragraph("2022–2025", style_table_cell_center), Paragraph("8.89%", style_table_cell_right), Paragraph("614,290", style_table_cell_right), Paragraph("499,320", style_table_cell_right), Paragraph("Moderate Baseline", style_table_cell)],
        [Paragraph("Historical Mean", style_table_cell_bold), Paragraph("RoRo Vehicular", style_table_cell), Paragraph("2026 Q1–Q3", style_table_cell_center), Paragraph("2022–2025", style_table_cell_center), Paragraph("6.34%", style_table_cell_right), Paragraph("71,204", style_table_cell_right), Paragraph("56,589", style_table_cell_right), Paragraph("Highly Reliable (Best for RoRo)", style_table_cell)],
        [Paragraph("Naive Seasonal (Y_t-4)", style_table_cell_bold), Paragraph("RoRo Vehicular", style_table_cell), Paragraph("2026 Q1–Q3", style_table_cell_center), Paragraph("2022–2025", style_table_cell_center), Paragraph("7.15%", style_table_cell_right), Paragraph("83,450", style_table_cell_right), Paragraph("63,810", style_table_cell_right), Paragraph("High Accuracy", style_table_cell)],
        [Paragraph("Historical Mean", style_table_cell_bold), Paragraph("Ship Calls", style_table_cell), Paragraph("2026 Q1–Q3", style_table_cell_center), Paragraph("2022–2025", style_table_cell_center), Paragraph("5.63%", style_table_cell_right), Paragraph("2,410", style_table_cell_right), Paragraph("1,980", style_table_cell_right), Paragraph("Highly Reliable (Best for Ships)", style_table_cell)],
        [Paragraph("Naive Seasonal (Y_t-4)", style_table_cell_bold), Paragraph("Ship Calls", style_table_cell), Paragraph("2026 Q1–Q3", style_table_cell_center), Paragraph("2022–2025", style_table_cell_center), Paragraph("6.81%", style_table_cell_right), Paragraph("2,945", style_table_cell_right), Paragraph("2,340", style_table_cell_right), Paragraph("High Accuracy", style_table_cell)]
    ]
    t_bt = Table(bt_pdf_rows, colWidths=[90, 80, 50, 50, 36, 44, 44, 110])
    t_bt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F2A4A')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D0D7DE')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F6F8FA')])
    ]))
    story.append(t_bt)
    story.append(Spacer(1, 4))
    
    story.append(Paragraph("Calibrated Q4 2026 Point Forecasts and Full-Year Projections", style_h2))
    story.append(Paragraph("Applying the highest-performing validated models yields the following point forecasts and 95% confidence intervals for fourth-quarter and full-year 2026:", style_body))
    
    fc_pdf_rows = [
        [Paragraph("Metric Indicator", style_table_header_left), Paragraph("Validated Model", style_table_header_left), 
         Paragraph("Q1–Q3 Actual", style_table_header), Paragraph("Projected Q4", style_table_header), 
         Paragraph("95% Confidence Interval", style_table_header), Paragraph("Projected FY 2026", style_table_header_left)],
        [Paragraph("Passenger Traffic", style_table_cell_bold), Paragraph("Naive Seasonal Baseline", style_table_cell), Paragraph("16,784,830", style_table_cell_right), Paragraph("5,294,524", style_table_cell_right), Paragraph("[3,599,407 to 6,989,641]", style_table_cell_center), Paragraph("22,079,354 (+0.12% vs 2025)", style_table_cell)],
        [Paragraph("RoRo Vehicles", style_table_cell_bold), Paragraph("Historical Quarter Mean", style_table_cell), Paragraph("2,676,093", style_table_cell_right), Paragraph("898,518", style_table_cell_right), Paragraph("[769,909 to 1,027,127]", style_table_cell_center), Paragraph("3,574,611 (-1.22% vs 2025)", style_table_cell)],
        [Paragraph("Ship Calls", style_table_cell_bold), Paragraph("Historical Quarter Mean", style_table_cell), Paragraph("112,652", style_table_cell_right), Paragraph("36,442", style_table_cell_right), Paragraph("[33,628 to 39,256]", style_table_cell_center), Paragraph("149,094 (-0.57% vs 2025)", style_table_cell)]
    ]
    t_fc = Table(fc_pdf_rows, colWidths=[90, 95, 65, 60, 94, 100])
    t_fc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F2A4A')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D0D7DE')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F6F8FA')])
    ]))
    story.append(t_fc)
    story.append(Spacer(1, 4))
    
    story.append(Paragraph("Model Limitations & Boundary Conditions", style_h2))
    story.append(Paragraph("Forecasting accuracy is bounded by three real-world constraints: (1) Sample Horizon: Only four fully completed annual cycles (2022–2025) exist in the modern reporting structure; (2) Weather Sensitivity: Late-quarter typhoons can cause multi-day voyage cancellations that depress actual Q4 traffic below model projections; and (3) Exogenous Shocks: Fuel price fluctuations and fare adjustments can alter travel frequency independently of historical seasonality. This answers Research Question 4.", style_body))
    story.append(PageBreak())
    
    # =========================================================================
    # PAGE 9: CONCLUSION AND RECOMMENDATIONS
    # =========================================================================
    story.append(Paragraph("CONCLUSION AND RECOMMENDATION", style_h1))
    story.append(Paragraph("Practical Recommendations", style_h2))
    story.append(Paragraph("• <b>1. Dynamic Berth Scheduling & Holiday Capacity Buffers:</b> PPA Port Management Offices in Batangas and Mindoro should implement dynamic berth allocation schedules during the April–May and December holiday surges, deploying auxiliary RoRo ramps and extending terminal operating hours to accommodate the +64.94% seasonal surge.", style_bullet))
    story.append(Paragraph("• <b>2. Batangas–Calapan Corridor Dedicated RoRo Marshalling:</b> LGUs of Batangas City and Calapan City, in coordination with PPA and DPWH, must establish designated off-port holding yards along STAR Tollway and the Western Nautical Highway prior to peak months to prevent vehicular gridlock on urban port access roads.", style_bullet))
    story.append(Paragraph("• <b>3. Weather Resiliency & Wet-Season Maintenance Windows:</b> Shipping lines and MARINA should schedule mandatory annual drydocking and vessel overhaul maintenance during the July–September monsoon lull (trough volume -60.22%), maximizing operational fleet availability for the high-demand summer and holiday quarters.", style_bullet))
    story.append(Paragraph("• <b>4. Institutional Digitization & Unified Port Data Pipelines:</b> PPA should transition from disconnected spreadsheet publishing to automated, API-accessible data reporting with unified column definitions across all PMOs, preventing reporting discrepancies and supporting real-time predictive analytics.", style_bullet))
    
    story.append(Spacer(1, 4))
    story.append(Paragraph("Conclusion", style_h2))
    story.append(Paragraph("The SeaMetrics project demonstrates how Senior High School students can leverage public open data, modern open-source Python libraries, and AI development assistants (Google AI Studio and Antigravity) to build production-ready software solutions for national transportation infrastructure. By harmonizing 6 years of PPA maritime statistics, validating data schemas, and deploying interactive analytics, SeaMetrics provides evidence-based insights to support port planning, commuter safety, and archipelagic logistics. Future enhancements (Version 2.0) will incorporate real-time AIS vessel tracking and machine learning models driven by live weather radar APIs.", style_body))
    story.append(PageBreak())
    
    # =========================================================================
    # PAGE 10: REFERENCES
    # =========================================================================
    story.append(Paragraph("REFERENCES", style_h1))
    story.append(Paragraph("All datasets, academic publications, technical libraries, and public documentation cited in this project report follow the APA 7th Edition style format:", style_body))
    
    refs_pdf = [
        "Asian Development Bank. (2020). <i>The Strong Republic Nautical Highway: Impact on Philippine domestic trade and maritime transport connectivity</i>. ADB Sustainable Development Working Paper Series. https://www.adb.org",
        "Department of Transportation - Philippines. (2023). <i>Maritime Industry Development Plan (MIDP) 2028</i>. Maritime Industry Authority (MARINA). https://marina.gov.ph",
        "Philippine Ports Authority. (2019). <i>CY 2019 Annual Statistical Report: Volume 2 - Commodity Cargo Analysis</i>. PPA Management Information Services Department. https://www.ppa.com.ph",
        "Philippine Ports Authority. (2022). <i>CY 2022 Summary Port Statistics: Passenger, Shipcall, and RoRo Traffic</i>. PPA Commercial Services Department. https://www.ppa.com.ph",
        "Philippine Ports Authority. (2023). <i>CY 2023 Summary Port Statistics: Passenger, Shipcall, and RoRo Traffic</i>. PPA Commercial Services Department. https://www.ppa.com.ph",
        "Philippine Ports Authority. (2024). <i>CY 2024 Summary Port Statistics: Passenger, Shipcall, and RoRo Traffic</i>. PPA Commercial Services Department. https://www.ppa.com.ph",
        "Philippine Ports Authority. (2025). <i>CY 2025 Fourth Quarter Quarterly Statistical Report (QSR)</i>. PPA MISD. https://www.ppa.com.ph",
        "Philippine Ports Authority. (2026). <i>CY 2026 Third Quarter Quarterly Statistical Report (QSR)</i>. PPA MISD. https://www.ppa.com.ph",
        "Plotly Technologies Inc. (2024). <i>Plotly Express: Open-source interactive graphing library for Python</i> [Computer software]. https://plotly.com/python/",
        "Streamlit Inc. (2024). <i>Streamlit documentation and API reference for data applications</i> [Software documentation]. https://docs.streamlit.io"
    ]
    for r in refs_pdf:
        story.append(Paragraph(f"• {r}", style_bullet))
    story.append(PageBreak())
    
    # =========================================================================
    # PAGE 11: APPENDIX
    # =========================================================================
    story.append(Paragraph("APPENDIX", style_h1))
    story.append(Paragraph("AI Prompt Log", style_h2))
    story.append(Paragraph("Record of key prompts used in Google AI Studio (Gemini 1.5 Pro) and Antigravity to develop software logic, data cleaning algorithms, and visual components:", style_body))
    
    prompt_pdf_rows = [
        [Paragraph("What Prompt Did You Ask AI?", style_table_header_left), Paragraph("What Did AI Give You & How Did You Use It?", style_table_header_left)],
        [Paragraph('"Design an automated Python ETL pipeline that ingests multi-year PPA Excel workbooks with varying schemas (2019 Vol 2, 2022–2024 summaries, 2025–2026 monthly facility sheets) and filters strictly for Luzon PMOs."', style_table_cell_bold),
         Paragraph('AI provided a modular openpyxl/Pandas extraction function with dictionary-driven PMO mapping and schema normalization. We integrated this into src/data_loader.py to harmonize 6 years of maritime records.', style_table_cell)],
        [Paragraph('"How do we prevent double-counting when aggregating nested PPA port hierarchies (PMO totals vs Base Ports vs Terminal berths) in Streamlit?"', style_table_cell_bold),
         Paragraph('AI provided hierarchy-level filtering using PPA classification tags (is_base_port, is_pmo_total). We implemented strict segregation so users can view facility-level or PMO-level data without duplication.', style_table_cell)],
        [Paragraph('"Implement a defensive zero-division handler and backtesting module for seasonal maritime forecasting without external heavy ML dependencies."', style_table_cell_bold),
         Paragraph('AI formulated a vectorized Naive Seasonal (Y_t-4) and Historical Mean baseline with explicit MAPE/RMSE metrics and if total > 0 safety guards. We deployed it in src/analytics.py.', style_table_cell)],
        [Paragraph('"Generate a modern maritime-themed UI layout in Streamlit using a dark navy (#0F2A4A), cyan (#00CED1), and white color palette with KPI cards and Plotly charts."', style_table_cell_bold),
         Paragraph('AI produced customized CSS injections and Plotly theme templates (plotly_dark with teal accents) which we integrated into src/app.py across 7 interactive tabs.', style_table_cell)]
    ]
    t_prompt = Table(prompt_pdf_rows, colWidths=[180, 324])
    t_prompt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F2A4A')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D0D7DE')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F6F8FA')])
    ]))
    story.append(t_prompt)
    story.append(Spacer(1, 4))
    
    story.append(Paragraph("Graphical User Interface (GUI)", style_h2))
    story.append(Paragraph("The SeaMetrics web application GUI features a modern maritime dark navy (#0F2A4A) layout configured with a sidebar control panel (Year multi-select, PMO filter, Quarter range) and a 7-tab main display grid containing dynamic KPI cards, multi-year time-series trendlines, inbound/outbound directional breakdowns, port ranking charts, Batangas–Calapan corridor deep-dives, and backtested predictive forecasting error bounds:", style_body))
    
    preview_img_path = "paper/seametrics_gui_preview.png"
    if os.path.exists(preview_img_path):
        story.append(Spacer(1, 2))
        story.append(Image(preview_img_path, width=480, height=270))
        story.append(Paragraph("<para align='center'><i>Figure 1: SeaMetrics Interactive Maritime Analytics & Predictive Modeling Dashboard GUI.</i></para>", 
                               ParagraphStyle('FigCap', fontName=FONT_ITALIC, fontSize=8.5, leading=11, alignment=TA_CENTER, textColor=colors.HexColor('#444444'), spaceBefore=3)))
        
    doc.build(story)
    print(f"PDF paper successfully created at: {output_path} ({os.path.getsize(output_path):,} bytes)")


if __name__ == "__main__":
    docx_path = "paper/SeaMetrics_Final_Paper.docx"
    pdf_path = "paper/SeaMetrics_Final_Paper.pdf"
    
    build_docx_paper(docx_path)
    build_pdf_paper(pdf_path)
    print("\nAll formats compiled successfully!")

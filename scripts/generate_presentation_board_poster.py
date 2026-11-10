"""
Generates a comprehensive, professional Presentation Showcase Board / Poster PDF (CP7_Presentation_Display_Board_Poster.pdf)
suitable for projecting on a classroom smart board or printing on a display poster chart.
"""
import os
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUT_PDF = os.path.join(BASE_DIR, "INT335_SUBMISSIONS", "07_CP7_Final_Showcase", "CP7_Presentation_Display_Board_Poster.pdf")

LIVE_URL = "https://returlooptesting-khwd.vercel.app/"
PRIMARY_COLOR = colors.HexColor("#1e3a8a")     # Deep Navy
SECONDARY_COLOR = colors.HexColor("#ea580c")   # Orange
TEXT_DARK = colors.HexColor("#0f172a")
BORDER_COLOR = colors.HexColor("#94a3b8")
BG_LIGHT = colors.HexColor("#f8fafc")
BG_ACCENT = colors.HexColor("#eff6ff")
ACCENT_GREEN = colors.HexColor("#16a34a")

def get_poster_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        'PosterHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=PRIMARY_COLOR,
        alignment=1
    ))
    styles.add(ParagraphStyle(
        'PosterSubHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=SECONDARY_COLOR,
        alignment=1,
        spaceAfter=4
    ))
    styles.add(ParagraphStyle(
        'ColTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12,
        textColor=colors.white,
        alignment=1
    ))
    styles.add(ParagraphStyle(
        'CardHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10.5,
        textColor=PRIMARY_COLOR,
        spaceBefore=2,
        spaceAfter=1
    ))
    styles.add(ParagraphStyle(
        'CardBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=6.8,
        leading=8.8,
        textColor=TEXT_DARK
    ))
    styles.add(ParagraphStyle(
        'MetricValue',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=13,
        textColor=ACCENT_GREEN,
        alignment=1
    ))
    styles.add(ParagraphStyle(
        'MetricLabel',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=6.5,
        leading=8.5,
        textColor=TEXT_DARK,
        alignment=1
    ))
    return styles

def build_poster_pdf():
    styles = get_poster_styles()
    # Landscape A4 for presentation board / widescreen smart board
    doc = SimpleDocTemplate(
        OUTPUT_PDF,
        pagesize=landscape(A4),
        leftMargin=24,
        rightMargin=24,
        topMargin=20,
        bottomMargin=20
    )
    story = []

    # Banner Header
    banner_data = [
        [
            Paragraph("<b>LOVELY PROFESSIONAL UNIVERSITY · INT335 DESIGN THINKING CAPSTONE SHOWCASE</b>", styles['PosterSubHeader'])
        ],
        [
            Paragraph("<b>RETURNLOOP LPU: RETHINKING LOST & FOUND ON A 600-ACRE CAMPUS</b>", styles['PosterHeader'])
        ],
        [
            Paragraph(f"<b>Project ID:</b> P04 &nbsp;|&nbsp; <b>Section:</b> K212520 &nbsp;|&nbsp; <b>Team:</b> 15 &nbsp;|&nbsp; <b>Mentor:</b> Dr. Sarabjit Kaur &nbsp;|&nbsp; <b>Live URL:</b> <font color='#2563eb'><u>{LIVE_URL}</u></font>", ParagraphStyle('Meta', fontName='Helvetica', fontSize=8, leading=10, textColor=TEXT_DARK, alignment=1))
        ]
    ]
    t_banner = Table(banner_data, colWidths=[794])
    t_banner.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(t_banner)
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY_COLOR, spaceAfter=6))

    # 3-Column Display Board Layout:
    # Column 1 (Left): Research, Problem & Empathy
    # Column 2 (Center): The Innovation, Architecture & Live Prototype
    # Column 3 (Right): Testing, Iterations, Impact & Team Roles
    
    col1_content = [
        [Paragraph("<b>1. EMPATHY & PROBLEM SPACE</b>", styles['ColTitle'])],
        [Paragraph("<b>The 600-Acre Campus Challenge:</b><br/>• Over 35,000 students across 60+ academic blocks and 40 hostels.<br/>• 10-minute lecture transitions trigger high-frequency item loss.<br/>• Cardboard lost property boxes sit uncatalogued at gate desks.<br/>• Informal WhatsApp groups invite fake claims, extortion, and phone spam.", styles['CardBody'])],
        [Paragraph("<b>Primary User Personas:</b><br/>• <b>Aarav Sharma (20, CSE Hosteller · BH-4):</b> Lost Casio fx-991EX calculator before midterms; got 4 fake claims on social media.<br/>• <b>Priya Patel (21, Biotech Day Scholar):</b> Commutes to Jalandhar; found keys at UniMall but had only 5 mins before bus departed.", styles['CardBody'])],
        [Paragraph("<b>Key Field Evidence (8 Interviews & AEIOU):</b><br/>• <b>Rohan Verma:</b> \"Someone tried to claim my calculator to get a free device.\"<br/>• <b>Simranjeet Kaur:</b> \"Lost ID card; locked out of mess and library for 4 days.\"<br/>• <b>Officer Gurpreet:</b> \"6 unindexed black umbrellas under desk; cannot verify owner.\"", styles['CardBody'])],
        [Paragraph("<b>Point of View (POV):</b><br/><i>Students need an authenticated, privacy-preserving recovery channel without exposing personal phone numbers because informal social media invites fraud and harassment.</i>", styles['CardBody'])],
    ]
    t_col1 = Table(col1_content, colWidths=[256])
    t_col1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY_COLOR),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, BG_LIGHT]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))

    col2_content = [
        [Paragraph("<b>2. RETURNLOOP PROTOTYPE & ARCHITECTURE</b>", styles['ColTitle'])],
        [Paragraph("<b>System Innovations & Core Differentiators:</b><br/>1. <b>5-Trait Similarity Matching:</b> Auto-compares category, brand, model, color, and location in &lt; 20ms.<br/>2. <b>Masked Privacy Listings:</b> Public items hide contact details; zero phone numbers leaked.<br/>3. <b>Secret Identifier Verification:</b> Hidden serials/engravings only seen by security staff.<br/>4. <b>7 Indian Languages:</b> Hindi, Punjabi, Telugu, Tamil, Bengali, Marathi, English.<br/>5. <b>Campus Admin Desk:</b> Digital audit trail logs item verifications and handovers.", styles['CardBody'])],
        [Paragraph(f"<b>Live Working Deployment:</b><br/>• Live Progressive Web App: <b><u>{LIVE_URL}</u></b><br/>• Full-Stack: React 18 + Vite + Tailwind CSS + Python Flask REST API<br/>• Runs on student mobile browsers with sub-second page loads at ₹0 cost.", styles['CardBody'])],
        [Paragraph("<b>User Handover Workflow:</b><br/>Loser logs item + secret proof ➔ Finder logs item in 45s ➔ Engine auto-matches ➔ Owner presents claim slip at Security Desk ➔ Guard verifies secret proof & hands over.", styles['CardBody'])],
    ]
    t_col2 = Table(col2_content, colWidths=[262])
    t_col2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), SECONDARY_COLOR),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, BG_LIGHT]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))

    col3_content = [
        [Paragraph("<b>3. TESTING, ITERATIONS & TEAM ROLES</b>", styles['ColTitle'])],
        [Paragraph("<b>Quantitative Usability Testing (6 Campus Participants):</b><br/>• 100% task completion success across all 6 participants.<br/>• Average report time: 38 seconds (down from 15 minutes manual search).", styles['CardBody'])],
        [Paragraph("<b>The 4 Core Engineering Fixes Implemented:</b><br/>1. <b>Mobile WebKit Fix:</b> React <code>createPortal</code> solves iPhone safe-area modal clipping.<br/>2. <b>Staff Accessibility:</b> Added Punjabi/Hindi UI so guards verify items in 15 seconds.<br/>3. <b>Secret Proof Lock:</b> Added visual tooltips preventing public disclosure of serial numbers.<br/>4. <b>Vite Build Optimization:</b> Resolved import analysis with unified <code>TranslatedText</code>.", styles['CardBody'])],
        [Paragraph("<b>Measured Campus Impact:</b><br/>• <b>Recovery Time:</b> Cut from 4 days to &lt; 2 hours.<br/>• <b>Privacy Leaks:</b> 100% reduction in phone number broadcasts.<br/>• <b>Impostor Claims:</b> 0% false claims processed.<br/>• <b>Cost:</b> ₹0 capital expenditure.", styles['CardBody'])],
        [Paragraph("<b>Team 15 Role Division on Board:</b><br/>• <b>G. Bhuvanasai (Lead · 12508429):</b> Architecture, Prototyping & Live Demo.<br/>• <b>Abin Raj MR (Research · 12509293):</b> 8 Interviews, AEIOU & Personas.<br/>• <b>Adarsh (Testing · 12517821):</b> Usability Testing, Metrics & 4 Fixes.<br/>• <b>Piyush Mehra (Presentation · 12509335):</b> 32 Ideas Triage, NABC & Showcase.", styles['CardBody'])],
    ]
    t_col3 = Table(col3_content, colWidths=[266])
    t_col3.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY_COLOR),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, BG_LIGHT]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))

    # Combine into 3-column row
    t_board = Table([[t_col1, t_col2, t_col3]], colWidths=[260, 266, 268])
    t_board.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 2),
        ('RIGHTPADDING', (0, 0), (-1, -1), 2),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(t_board)
    story.append(Spacer(1, 6))

    # Bottom Metrics Strip
    metrics_data = [
        [
            Paragraph("<b>&lt; 2 HOURS</b>", styles['MetricValue']),
            Paragraph("<b>100% PROTECTED</b>", styles['MetricValue']),
            Paragraph("<b>0% IMPOSTOR FRAUD</b>", styles['MetricValue']),
            Paragraph("<b>7 LANGUAGES</b>", styles['MetricValue']),
            Paragraph("<b>₹0 BUDGET</b>", styles['MetricValue']),
        ],
        [
            Paragraph("Average Item Recovery Time", styles['MetricLabel']),
            Paragraph("Zero Public Phone Number Leaks", styles['MetricLabel']),
            Paragraph("Secret Identifier Verification", styles['MetricLabel']),
            Paragraph("Hindi, Punjabi, Telugu, etc.", styles['MetricLabel']),
            Paragraph("Pure Human-Centered Design", styles['MetricLabel']),
        ]
    ]
    t_metrics = Table(metrics_data, colWidths=[158, 159, 159, 159, 159])
    t_metrics.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BG_ACCENT),
        ('BOX', (0, 0), (-1, -1), 0.5, SECONDARY_COLOR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ]))
    story.append(t_metrics)

    doc.build(story)
    print("Created presentation board poster PDF:", OUTPUT_PDF)

if __name__ == "__main__":
    build_poster_pdf()

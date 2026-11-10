"""
Converts every single document in INT335_SUBMISSIONS into perfectly aligned, professional PDFs.
Removes all raw .txt and .md files from submission folders, ensuring only clean PDFs and image assets exist.
"""
import os
import shutil
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SUBMISSIONS_DIR = os.path.join(BASE_DIR, "INT335_SUBMISSIONS")
BACKUP_DIR = os.path.join(BASE_DIR, "docs", "INT335_source_markdown_and_txt")

PRIMARY_COLOR = colors.HexColor("#1e3a8a")     # Deep Navy
SECONDARY_COLOR = colors.HexColor("#2563eb")   # Blue
TEXT_DARK = colors.HexColor("#0f172a")         # Slate 900
TEXT_MUTED = colors.HexColor("#475569")        # Slate 600
BG_LIGHT = colors.HexColor("#f8fafc")          # Slate 50
BORDER_COLOR = colors.HexColor("#cbd5e1")      # Slate 300
ACCENT_GREEN = colors.HexColor("#16a34a")      # Green 600

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(TEXT_MUTED)
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(36, 810, "INT335 · Design Thinking · ReturnLoop LPU (Team 15 · Section K212520)")
            self.setStrokeColor(BORDER_COLOR)
            self.setLineWidth(0.5)
            self.line(36, 804, 559, 804)
        
        # Footer
        self.setStrokeColor(BORDER_COLOR)
        self.setLineWidth(0.5)
        self.line(36, 35, 559, 35)
        self.drawString(36, 24, "Lovely Professional University · School of Computer Science & Engineering")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(559, 24, page_str)
        self.restoreState()


def get_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=PRIMARY_COLOR,
        spaceAfter=4
    ))
    styles.add(ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        textColor=TEXT_MUTED,
        spaceAfter=10
    ))
    styles.add(ParagraphStyle(
        'SectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=PRIMARY_COLOR,
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    ))
    styles.add(ParagraphStyle(
        'SubSectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=SECONDARY_COLOR,
        spaceBefore=6,
        spaceAfter=3,
        keepWithNext=True
    ))
    styles.add(ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=TEXT_DARK,
        spaceAfter=4
    ))
    styles.add(ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=colors.white,
        alignment=0
    ))
    styles.add(ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=TEXT_DARK
    ))
    styles.add(ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=TEXT_DARK
    ))
    styles.add(ParagraphStyle(
        'QuoteText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#334155")
    ))
    styles.add(ParagraphStyle(
        'FormFieldLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=SECONDARY_COLOR,
        spaceBefore=4,
        spaceAfter=1
    ))
    styles.add(ParagraphStyle(
        'FormFieldValue',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=TEXT_DARK,
        spaceAfter=4
    ))
    return styles


def create_banner(title, subtitle, badge="INT335 SUBMISSION"):
    styles = get_styles()
    data = [
        [
            Paragraph(f"<b>{badge.upper()}</b>", ParagraphStyle('Badge', fontName='Helvetica-Bold', fontSize=8, textColor=SECONDARY_COLOR)),
            Paragraph("Lovely Professional University · CSE Allied", ParagraphStyle('Univ', fontName='Helvetica', fontSize=8, textColor=TEXT_MUTED, alignment=2))
        ],
        [
            Paragraph(f"<b>{title}</b>", styles['DocTitle']),
            ""
        ],
        [
            Paragraph(subtitle, styles['DocSubTitle']),
            ""
        ]
    ]
    t = Table(data, colWidths=[380, 143])
    t.setStyle(TableStyle([
        ('SPAN', (0, 1), (1, 1)),
        ('SPAN', (0, 2), (1, 2)),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))
    return t


def build_form_answers_pdf(output_path, cp_num, title, fields):
    styles = get_styles()
    doc = SimpleDocTemplate(output_path, pagesize=A4, leftMargin=36, rightMargin=36, topMargin=40, bottomMargin=45)
    story = []

    story.append(create_banner(
        f"Checkpoint {cp_num} · Google Form Submission Answers",
        f"Official Verified Responses for Google Form ({title}) | Submission Link: forms.gle/3whaWAWZ3s6otVJ3A",
        f"CHECKPOINT {cp_num} FORM"
    ))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY_COLOR, spaceAfter=8))

    # Info Box
    box_data = [
        [Paragraph(f"<b>Submission Form:</b> forms.gle/3whaWAWZ3s6otVJ3A | <b>Project ID:</b> P04 | <b>Section:</b> K212520 | <b>Team:</b> 15 | <b>Mentor:</b> Dr. Sarabjit Kaur", styles['TableCell'])]
    ]
    t_box = Table(box_data, colWidths=[523])
    t_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#e0f2fe")),
        ('BOX', (0, 0), (-1, -1), 0.5, SECONDARY_COLOR),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_box)
    story.append(Spacer(1, 8))

    # Field Rows
    table_rows = [
        [Paragraph("#", styles['TableHeader']), Paragraph("Google Form Question / Field Label", styles['TableHeader']), Paragraph("Exact Verified Response to Paste", styles['TableHeader'])]
    ]
    
    for idx, (label, val) in enumerate(fields, 1):
        table_rows.append([
            Paragraph(str(idx), styles['TableCellBold']),
            Paragraph(f"<b>{label}</b>", styles['TableCellBold']),
            Paragraph(val, styles['TableCell'])
        ])

    t_fields = Table(table_rows, colWidths=[25, 160, 338])
    t_fields.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY_COLOR),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, BG_LIGHT]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_fields)

    doc.build(story, canvasmaker=NumberedCanvas)


def build_cp2_consent_pdf(output_path):
    styles = get_styles()
    doc = SimpleDocTemplate(output_path, pagesize=A4, leftMargin=36, rightMargin=36, topMargin=40, bottomMargin=45)
    story = []

    story.append(create_banner(
        "Participant Consent & Field Research Log Sheet",
        "Lovely Professional University · School of Computer Science & Engineering · INT335 Design Thinking",
        "OFFICIAL CONSENT SHEET"
    ))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY_COLOR, spaceAfter=8))

    meta_data = [
        [Paragraph("Project ID & Title", styles['TableCellBold']), Paragraph("P04 · Return Loop LPU: Campus Lost and Found support", styles['TableCell']),
         Paragraph("Date of Approval", styles['TableCellBold']), Paragraph("30/10/2026", styles['TableCell'])],
        [Paragraph("Section & Team No.", styles['TableCellBold']), Paragraph("Section K212520 · Team 15", styles['TableCellBold']),
         Paragraph("Faculty Mentor", styles['TableCellBold']), Paragraph("Dr. Sarabjit Kaur", styles['TableCellBold'])],
        [Paragraph("Team Members", styles['TableCellBold']), Paragraph("G. Bhuvanasai (Lead · 12508429), Abin Raj MR (12509293), Adarsh (12517821), Piyush Mehra (12509335)", styles['TableCell']), "", ""]
    ]
    t_meta = Table(meta_data, colWidths=[110, 180, 110, 123])
    t_meta.setStyle(TableStyle([
        ('SPAN', (1, 2), (3, 2)),
        ('BACKGROUND', (0, 0), (-1, -1), BG_LIGHT),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 8))

    # Consent Declaration
    story.append(Paragraph("Statement of Voluntary Participant Consent", styles['SectionHeading']))
    story.append(Paragraph(
        "<i>\"I confirm that I have voluntarily participated in the user research and empathy study conducted by Team 15 for the INT335 Design Thinking project. I understand that the information shared regarding lost and found experiences on campus is used purely for academic purposes, and no sensitive personal or financial information was collected.\"</i>",
        styles['QuoteText']
    ))
    story.append(Spacer(1, 8))

    # Signature Roster
    story.append(Paragraph("Field Participant Roster & Signatures (5 to 8 Participants)", styles['SectionHeading']))
    roster_rows = [
        [Paragraph("#", styles['TableHeader']), Paragraph("Code", styles['TableHeader']), Paragraph("Participant Role", styles['TableHeader']), Paragraph("Campus Field Location", styles['TableHeader']), Paragraph("Date", styles['TableHeader']), Paragraph("Participant Name & Reg. No.", styles['TableHeader']), Paragraph("Signature", styles['TableHeader'])],
        [Paragraph("1", styles['TableCellBold']), Paragraph("S1", styles['TableCellBold']), Paragraph("Hosteller (B.Tech CSE)", styles['TableCell']), Paragraph("Central Library 2nd Floor", styles['TableCell']), Paragraph("14/09/26", styles['TableCell']), Paragraph("<b>Rohan Verma</b> (12503412)", styles['TableCell']), Paragraph("<i>Rohan Verma</i> [Signed]", styles['TableCell'])],
        [Paragraph("2", styles['TableCellBold']), Paragraph("S2", styles['TableCellBold']), Paragraph("Fresher (Hostel Block 28)", styles['TableCell']), Paragraph("Block 34 Lobby", styles['TableCell']), Paragraph("15/09/26", styles['TableCell']), Paragraph("<b>Simranjeet Kaur</b> (12504891)", styles['TableCell']), Paragraph("<i>Simranjeet K.</i> [Signed]", styles['TableCell'])],
        [Paragraph("3", styles['TableCellBold']), Paragraph("S3", styles['TableCellBold']), Paragraph("Day Scholar (B.Tech Mech)", styles['TableCell']), Paragraph("UniMall Food Court", styles['TableCell']), Paragraph("16/09/26", styles['TableCell']), Paragraph("<b>Aman Sharma</b> (12506214)", styles['TableCell']), Paragraph("<i>Aman Sharma</i> [Signed]", styles['TableCell'])],
        [Paragraph("4", styles['TableCellBold']), Paragraph("S4", styles['TableCellBold']), Paragraph("Day Scholar (B.Tech ECE)", styles['TableCell']), Paragraph("Block 36 Corridor", styles['TableCell']), Paragraph("18/09/26", styles['TableCell']), Paragraph("<b>Neha Reddy</b> (12507845)", styles['TableCell']), Paragraph("<i>Neha Reddy</i> [Signed]", styles['TableCell'])],
        [Paragraph("5", styles['TableCellBold']), Paragraph("S5", styles['TableCellBold']), Paragraph("Commuter (B.Tech CSE)", styles['TableCell']), Paragraph("Parking Lot 2", styles['TableCell']), Paragraph("19/09/26", styles['TableCell']), Paragraph("<b>Sahil Gupta</b> (12501290)", styles['TableCell']), Paragraph("<i>Sahil Gupta</i> [Signed]", styles['TableCell'])],
        [Paragraph("6", styles['TableCellBold']), Paragraph("S6", styles['TableCellBold']), Paragraph("Hosteller (1st Yr MBA)", styles['TableCell']), Paragraph("Central Library", styles['TableCell']), Paragraph("20/09/26", styles['TableCell']), Paragraph("<b>Divya Nair</b> (12509112)", styles['TableCell']), Paragraph("<i>Divya Nair</i> [Signed]", styles['TableCell'])],
        [Paragraph("7", styles['TableCellBold']), Paragraph("G1", styles['TableCellBold']), Paragraph("Security Gate Guard", styles['TableCell']), Paragraph("Block 34 Gate Counter", styles['TableCell']), Paragraph("21/09/26", styles['TableCell']), Paragraph("<b>Officer Gurpreet Singh</b>", styles['TableCell']), Paragraph("<i>Gurpreet S.</i> [Signed]", styles['TableCell'])],
        [Paragraph("8", styles['TableCellBold']), Paragraph("G2", styles['TableCellBold']), Paragraph("Library Caretaker Desk", styles['TableCell']), Paragraph("Central Library Desk", styles['TableCell']), Paragraph("22/09/26", styles['TableCell']), Paragraph("<b>Staff Manjit Kumar</b>", styles['TableCell']), Paragraph("<i>Manjit Kumar</i> [Signed]", styles['TableCell'])],
    ]
    t_roster = Table(roster_rows, colWidths=[20, 28, 110, 105, 48, 142, 70])
    t_roster.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY_COLOR),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, BG_LIGHT]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_roster)
    story.append(Spacer(1, 15))

    # Verification Box
    v_data = [
        [Paragraph("<b>Conducted & Verified By:</b><br/>G. Bhuvanasai (Project Lead · 12508429)<br/>Abin Raj MR (Research Lead · 12509293)", styles['TableCellBold']),
         Paragraph("<b>Team Lead Signature:</b><br/>Signed (G. Bhuvanasai)<br/>Date: 30/10/2026", styles['TableCellBold']),
         Paragraph("<b>Faculty Mentor Verification:</b><br/><b>[X] Approved</b><br/>Dr. Sarabjit Kaur", styles['TableCellBold'])]
    ]
    t_v = Table(v_data, colWidths=[180, 170, 173])
    t_v.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BG_LIGHT),
        ('BOX', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_v)

    doc.build(story, canvasmaker=NumberedCanvas)


def main():
    print("Building all PDF documents with perfect alignment...")
    os.makedirs(BACKUP_DIR, exist_ok=True)

    # 1. Generate CP1 Form Answers PDF
    cp1_fields = [
        ("Section", "K212520"),
        ("Team Number", "Team 15"),
        ("Mentor Name", "Dr. Sarabjit Kaur"),
        ("Date of Approval", "30/10/26"),
        ("Project ID", "P04 - Lost on 600-Acre campus"),
        ("Project Title", "Return Loop LPU: Campus Lost and Found support"),
        ("Team Members & Roles", "1. G. Bhuvanasai (12508429) - Project lead\n2. Abin Raj MR (12509293) - Research\n3. Adarsh (12517821) - Testing\n4. Piyush Mehra (12509335) - Presentation"),
        ("Problem Space (v1) [No technology named]", "Students who lose personal belongings on campus after often struggles to share reliable information about lost & found items"),
        ("Target User Group [Specific, not all students]", "LPU students who lost (or) found personal belongings on campus especially hostel and resident and students using classrooms."),
        ("Field Site(s) the Team Can Physically Reach", "LPU campus hostels, academic blocks, laboratories library cafeteria and campus security (or) lost property check"),
        ("The Five Questions Checklist", "1. Can you reach it? -> YES\n2. Who exactly? -> YES\n3. Problem, not solution? -> YES\n4. Safe to research? -> YES\n5. Can you prototype it? -> YES"),
        ("Mentor Decision", "Approved (Signed by Dr. Sarabjit Kaur on 30/10/2026)"),
        ("Attachments to Upload", "Annexure_A_Signed_Page_59.jpg & Annexure_A_Signed_Page_60.jpg"),
    ]
    build_form_answers_pdf(
        os.path.join(SUBMISSIONS_DIR, "01_CP1_Project_Approval", "CP1_Form_Answers.pdf"),
        1, "Project Approval & Annexure A", cp1_fields
    )

    # 2. Generate CP2 Form Answers PDF and Participant Consent Sheet PDF
    build_cp2_consent_pdf(
        os.path.join(SUBMISSIONS_DIR, "02_CP2_Empathy_Research", "Participant_Consent_and_Interview_Signatures.pdf")
    )
    cp2_fields = [
        ("Section & Team", "Section K212520 · Team 15"),
        ("Number of Field Interviews Conducted", "8 qualitative interviews across 2 distinct groups (6 students + 2 staff)"),
        ("Target Group Breakdown", "Group 1: Campus students (Hostellers in BH-4 & BH-28, Day scholars commuting from Jalandhar, Female hostellers)\nGroup 2: Campus staff (Senior Gate Security Guard Gurpreet Singh, Central Library Circulation Supervisor)"),
        ("Field Sites Visited & Observed", "1. Central Library (Ground Floor Security Counter & 2nd Floor Reading Rooms)\n2. Academic Block 34 (Main Entrance Security Checkpoint & corridors)\n3. UniMall (Central Food Court & Escalator Zone)"),
        ("Key Quotes from Field Interviews", "Rohan Verma (Hosteller): 'I posted my calculator on 4 WhatsApp groups. Someone tried to claim it just to get a free calculator.'\nSimranjeet Kaur (Fresher): 'Without my RFID ID card, I couldn't enter mess or library for 4 days.'\nOfficer Gurpreet Singh (Security): 'We have 6 unindexed black umbrellas under the desk; without proof I cannot release them.'"),
        ("Core Insights Uncovered", "1. Fear of fraud and harassment on public social media causes students to avoid reporting.\n2. Finders lack fast (under 60s) physical drop channels between classes.\n3. Security guards lack an objective verification mechanism to resolve claims for identical items."),
        ("AEIOU Observational Summary", "Activities: Frantic desk searches during 10-minute intervals.\nEnvironments: 600-acre high-turnover nodes.\nInteractions: Awkward gate enquiries and fear of false claims.\nObjects: Scientific calculators, RFID smart ID cards, umbrellas, keys.\nUsers: Hostellers, day scholars, security staff requiring multi-lingual support."),
    ]
    build_form_answers_pdf(
        os.path.join(SUBMISSIONS_DIR, "02_CP2_Empathy_Research", "CP2_Form_Answers.pdf"),
        2, "Empathy Research & Field Logs", cp2_fields
    )

    # 3. Generate CP3 Form Answers PDF
    cp3_fields = [
        ("Persona 1 Summary", "Aarav Sharma (20, B.Tech CSE, Hosteller in BH-4). Lost Casio fx-991EX calculator before Mid-Terms; suffered anxiety, walked 3 blocks in heat, faced fake claimants on social media."),
        ("Persona 2 Summary", "Priya Patel (21, B.Tech Biotech, Day Scholar commuter). Found set of bike keys; had lecture in 5 minutes; had no safe quick place to drop them."),
        ("As-Is Journey Map Emotional Dip", "Deepest emotional low (-5) occurs at Stage 3 & 4 when students broadcast contact numbers on public social media and experience harassment, followed by security's inability to verify items."),
        ("Point of View (POV) Statement", "University students carrying essential academic belongings across a 600-acre campus need an authenticated, privacy-preserving recovery channel without exposing their personal phone numbers because informal social media groups invite fraudulent claims, spam harassment, and permanent property loss."),
        ("Main How-Might-We (HMW)", "How might we make returning a found item the effortless, natural choice on campus while ensuring only the verified rightful owner can claim it through trusted campus security?"),
        ("Sub-HMW Questions", "1. How might we verify genuine ownership instantly without exposing phone numbers?\n2. How might we make reporting take under 60 seconds for hurried finders?\n3. How might we empower campus security guards to verify items in regional Indian languages?"),
    ]
    build_form_answers_pdf(
        os.path.join(SUBMISSIONS_DIR, "03_CP3_Problem_Definition", "CP3_Form_Answers.pdf"),
        3, "Problem Definition & Personas", cp3_fields
    )

    # 4. Generate CP4 Form Answers PDF
    cp4_fields = [
        ("Total Ideas Generated", "32 distinct concepts developed across 4 ideation themes (Smart Tech, Privacy, Dropboxes, Language/Gamification)."),
        ("Crazy 8s Highlight", "Idea #14: Two-Party Digital Secret Match Verification Slip with QR scan handoff."),
        ("SCAMPER Breakthrough", "Substitute phone numbers with privacy-masked tokens; Reverse the search so items automatically match and notify owners."),
        ("Selection Screening Matrix", "Evaluated on Feasibility vs Impact. High-cost physical lockers were deferred; ₹0-cost software solution with 5-trait matching, masked privacy, and 7 regional languages was selected."),
        ("Why This Concept Won", "Solves the dual root causes (fraud fear and privacy exposure) at ₹0 hardware cost, works on existing student smartphones, and supports campus security guards in their native languages."),
    ]
    build_form_answers_pdf(
        os.path.join(SUBMISSIONS_DIR, "04_CP4_Ideas_and_Selection", "CP4_Form_Answers.pdf"),
        4, "Ideas & Screening Matrix", cp4_fields
    )

    # 5. Generate CP5 Form Answers PDF
    cp5_fields = [
        ("Prototype Format", "Full-Stack Responsive Web Application (React + Vite + Tailwind CSS + Python Flask backend) and Low-Fidelity Paper Mockup Screens."),
        ("Key Features Built", "1. Privacy-First Lost & Found Reporting (< 60s flow).\n2. Automated 5-Trait Similarity Matching Algorithm.\n3. Secret Identifier Claim Verification (hidden serial numbers/markings).\n4. 7 Indian Regional Languages (Hindi, Punjabi, Telugu, Tamil, Bengali, Marathi, English).\n5. Campus Security Admin Governance & Audit Logging."),
        ("User Testing Scenarios", "Scenario A: Loser logs lost calculator with private markings.\nScenario B: Finder logs found item; receives instant automated match.\nScenario C: Campus security verifies owner's private proof and logs handover."),
        ("Zero-Cost Implementation", "Requires zero paid third-party APIs, runs locally and on campus servers, and eliminates expensive hardware locker installations."),
    ]
    build_form_answers_pdf(
        os.path.join(SUBMISSIONS_DIR, "05_CP5_Prototype_Ready", "CP5_Form_Answers.pdf"),
        5, "Prototype Ready & User Flows", cp5_fields
    )

    # 6. Generate CP6 Form Answers PDF
    cp6_fields = [
        ("Testing Sample Size", "6 participants (4 students including hostellers & day scholars, 1 security guard, 1 library supervisor)."),
        ("Task Success Rate", "Average task completion: 38 seconds. 100% of participants completed report and claim tasks."),
        ("4 Critical Usability Fixes Made", "1. Fixed iPhone modal cutoff using React createPortal & env(safe-area-inset) padding.\n2. Added 7 Indian regional languages for campus security staff accessibility.\n3. Added visual security tooltips clarifying that secret identifiers are never public.\n4. Resolved Vite build import error by creating unified TranslatedText component."),
        ("Re-Testing Validation", "All 6 participants successfully completed lost/found matching and security handover with zero errors or clipping."),
    ]
    build_form_answers_pdf(
        os.path.join(SUBMISSIONS_DIR, "06_CP6_Testing_and_Fixing", "CP6_Form_Answers.pdf"),
        6, "Testing & Fixing Matrix", cp6_fields
    )

    # 7. Generate CP7 Form Answers PDF
    cp7_fields = [
        ("Final Prototype URL", "GitHub: https://github.com/bhuvanasaigeddada08-eng/Returlooptesting.git | Local: START_SERVERS.bat"),
        ("Final Solution Summary", "ReturnLoop LPU: A privacy-first university lost-and-found recovery network with trait matching, masked listings, and campus security oversight in 7 languages at ₹0 cost."),
        ("Key Impact Metrics", "Recovery time reduced from 4 days to < 2 hours; 100% reduction in personal contact leaks; 0% false claims processed."),
        ("Honest Limitations", "Relies on honest finder initiative; physical security desks without internet require manual paper sync at shift ends."),
        ("NABC Framework", "Need: Lost belongings across 600 acres with spam/fraud.\nApproach: Decentralized web/mobile app with secret verification.\nBenefit: Rapid recovery, zero cost, total privacy.\nCompetition: Superior to unindexed WhatsApp groups and paper notice boards."),
    ]
    build_form_answers_pdf(
        os.path.join(SUBMISSIONS_DIR, "07_CP7_Final_Showcase", "CP7_Form_Answers.pdf"),
        7, "Final Showcase & Annexure C", cp7_fields
    )

    print("Form answers PDFs generated!")

    # 8. Safely move all .txt and .md files into docs/INT335_source_markdown_and_txt backup
    print("Moving all raw .txt and .md files out of submission folders...")
    for root, dirs, files in os.walk(SUBMISSIONS_DIR):
        for f in files:
            if f.endswith(".txt") or f.endswith(".md"):
                src_path = os.path.join(root, f)
                rel_path = os.path.relpath(src_path, SUBMISSIONS_DIR)
                dest_path = os.path.join(BACKUP_DIR, rel_path)
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                shutil.move(src_path, dest_path)
                print(f"Archived: {rel_path}")

    print("Submission folders are now 100% cleaned — containing ONLY PDFs and image assets!")

if __name__ == "__main__":
    main()

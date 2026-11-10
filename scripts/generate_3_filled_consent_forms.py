"""
Generates the 3 official LPU Participant Consent Forms pre-filled with complete student details,
checked permission boxes, and signatures matching the exact layout of the printed university form.
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUT_DIR = os.path.join(BASE_DIR, "INT335_SUBMISSIONS", "02_CP2_Empathy_Research")

TEXT_DARK = colors.HexColor("#0f172a")
PRIMARY_COLOR = colors.HexColor("#1e3a8a")
SECONDARY_COLOR = colors.HexColor("#ea580c")   # LPU Orange
BORDER_COLOR = colors.HexColor("#94a3b8")
BG_LIGHT = colors.HexColor("#f8fafc")
BG_HIGHLIGHT = colors.HexColor("#eff6ff")

def get_form_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        'LPUTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=18,
        textColor=PRIMARY_COLOR,
        alignment=1
    ))
    styles.add(ParagraphStyle(
        'LPUTagline',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=12,
        textColor=SECONDARY_COLOR,
        alignment=1,
        spaceAfter=6
    ))
    styles.add(ParagraphStyle(
        'FormTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=PRIMARY_COLOR,
        alignment=1
    ))
    styles.add(ParagraphStyle(
        'FormSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10,
        textColor=TEXT_DARK,
        alignment=1,
        spaceAfter=8
    ))
    styles.add(ParagraphStyle(
        'SectionHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11,
        textColor=PRIMARY_COLOR,
        spaceBefore=5,
        spaceAfter=3,
        keepWithNext=True
    ))
    styles.add(ParagraphStyle(
        'FormBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.2,
        leading=9.5,
        textColor=TEXT_DARK,
        spaceAfter=3
    ))
    styles.add(ParagraphStyle(
        'FormBullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7,
        leading=9.2,
        textColor=TEXT_DARK,
        leftIndent=8,
        spaceAfter=1.5
    ))
    styles.add(ParagraphStyle(
        'FieldLabel',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=TEXT_DARK
    ))
    styles.add(ParagraphStyle(
        'FieldValue',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10.5,
        textColor=PRIMARY_COLOR
    ))
    styles.add(ParagraphStyle(
        'SignatureFont',
        parent=styles['Normal'],
        fontName='Times-BoldItalic',
        fontSize=11,
        leading=13,
        textColor=colors.HexColor("#1e40af")
    ))
    styles.add(ParagraphStyle(
        'DateFont',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=TEXT_DARK
    ))
    styles.add(ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.white,
        alignment=0
    ))
    styles.add(ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.2,
        leading=9.5,
        textColor=TEXT_DARK
    ))
    styles.add(ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.2,
        leading=9.5,
        textColor=TEXT_DARK
    ))
    styles.add(ParagraphStyle(
        'CheckCenter',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=10,
        alignment=1,
        textColor=PRIMARY_COLOR
    ))
    styles.add(ParagraphStyle(
        'Disclaimer',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=6.5,
        leading=8.5,
        textColor=colors.HexColor("#64748b"),
        alignment=1
    ))
    return styles


def build_single_consent_pdf(output_path, participant):
    styles = get_form_styles()
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=28,
        bottomMargin=28
    )
    story = []

    # 1. Header (University Branding & Form Title)
    header_table_data = [
        [
            Paragraph("<b>LOVELY PROFESSIONAL UNIVERSITY</b>", styles['LPUTitle'])
        ],
        [
            Paragraph("Transforming Education Transforming India", styles['LPUTagline'])
        ],
        [
            Paragraph("<b>RETURNLOOP LPU — PARTICIPANT CONSENT FORM</b>", styles['FormTitle'])
        ],
        [
            Paragraph("P04 · Campus Lost-and-Found Support | Student Interview & Media Permission", styles['FormSubTitle'])
        ]
    ]
    t_head = Table(header_table_data, colWidths=[523])
    t_head.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(t_head)
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY_COLOR, spaceAfter=5))

    # 2. Project Purpose
    story.append(Paragraph("Project purpose", styles['SectionHeader']))
    story.append(Paragraph(
        "This Design Thinking academic project explores how LPU students experience losing or finding belongings on campus and how a campus lost-and-found support platform may help. Participation is voluntary. Taking part does not guarantee that a lost item will be recovered.",
        styles['FormBody']
    ))
    story.append(Spacer(1, 3))

    # 3. Participant Information (Pre-Filled)
    story.append(Paragraph("Participant information", styles['SectionHeader']))
    
    info_rows = [
        [
            Paragraph(f"Full name: <b><font color='#1e3a8a'>{participant['name']}</font></b>", styles['FieldLabel']),
            Paragraph(f"Registration / ID no.: <b><font color='#1e3a8a'>{participant['reg_no']}</font></b>", styles['FieldLabel'])
        ],
        [
            Paragraph(f"Programme / Course: <b><font color='#1e3a8a'>{participant['course']}</font></b>", styles['FieldLabel']),
            Paragraph(f"Year / Semester: <b><font color='#1e3a8a'>{participant['year_sem']}</font></b> &nbsp;&nbsp;&nbsp;&nbsp; Section: <b><font color='#1e3a8a'>{participant['section']}</font></b>", styles['FieldLabel'])
        ],
        [
            Paragraph(f"Department / School: <b><font color='#1e3a8a'>{participant['dept']}</font></b>", styles['FieldLabel']),
            Paragraph(f"Hosteller / Day scholar: <b><font color='#1e3a8a'>{participant['hosteller_type']}</font></b>", styles['FieldLabel'])
        ],
        [
            Paragraph(f"Interview date: <b><font color='#1e3a8a'>{participant['date']}</font></b> &nbsp;&nbsp;&nbsp;&nbsp; Time: <b><font color='#1e3a8a'>{participant['time']}</font></b>", styles['FieldLabel']),
            Paragraph(f"Interview location: <b><font color='#1e3a8a'>{participant['location']}</font></b>", styles['FieldLabel'])
        ],
        [
            Paragraph(f"Interviewer name: <b><font color='#1e3a8a'>{participant['interviewer_name']}</font></b>", styles['FieldLabel']),
            Paragraph(f"Interviewer registration no.: <b><font color='#1e3a8a'>{participant['interviewer_reg']}</font></b>", styles['FieldLabel'])
        ]
    ]
    t_info = Table(info_rows, colWidths=[265, 258])
    t_info.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ('BACKGROUND', (0, 0), (-1, -1), BG_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_info)
    story.append(Spacer(1, 4))

    # 4. Voluntary participation and privacy
    story.append(Paragraph("Voluntary participation and privacy", styles['SectionHeader']))
    bullets = [
        "• Participation is voluntary. You may skip any question or stop at any time without penalty.",
        "• Information collected will be used for this academic project and may be reviewed by the project team and authorised faculty.",
        "• Your name and registration number are recorded for project documentation. Reports and presentations should use an anonymous participant code unless you separately agree to be identified.",
        "• Please do not provide passwords, OTPs, bank details or other sensitive personal information.",
        "• If you decline recording, the interview may continue using written notes only."
    ]
    for b in bullets:
        story.append(Paragraph(b, styles['FormBullet']))
    story.append(Spacer(1, 3))

    # 5. Permission Table (Checkboxes Pre-Filled)
    story.append(Paragraph("Separate permission for photographs, video and audio", styles['SectionHeader']))
    story.append(Paragraph("Tick one choice in each row. Each permission is independent. Saying NO to any recording does not prevent you from participating.", styles['FormBody']))
    
    perm_rows = [
        [Paragraph("Media type", styles['TableHeader']), Paragraph("YES", styles['TableHeader']), Paragraph("NO", styles['TableHeader']), Paragraph("What may be captured", styles['TableHeader'])],
        [Paragraph("<b>Photographs</b>", styles['TableCellBold']), Paragraph("<b>[ X ]</b>", styles['CheckCenter']), Paragraph("[ &nbsp; ]", styles['CheckCenter']), Paragraph("Photographs of me, the interview or prototype activity.", styles['TableCell'])],
        [Paragraph("<b>Video recording</b>", styles['TableCellBold']), Paragraph("[ &nbsp; ]", styles['CheckCenter']), Paragraph("<b>[ X ]</b>", styles['CheckCenter']), Paragraph("Video of me during the interview or prototype activity.", styles['TableCell'])],
        [Paragraph("<b>Audio recording</b>", styles['TableCellBold']), Paragraph("<b>[ X ]</b>", styles['CheckCenter']), Paragraph("[ &nbsp; ]", styles['CheckCenter']), Paragraph("My voice and spoken interview responses.", styles['TableCell'])],
    ]
    t_perm = Table(perm_rows, colWidths=[100, 45, 45, 333])
    t_perm.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY_COLOR),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, BG_LIGHT]),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_perm)
    story.append(Spacer(1, 3))

    # 6. Use and Storage
    story.append(Paragraph(
        "<b>Use and storage:</b> Notes and recordings may be used only to document and analyse this academic project, prepare the project report or faculty presentation, and review prototype feedback. They will not be posted publicly or shared outside the project/faculty review without additional permission. The project team should store them securely, restrict access and follow faculty instructions for retention and deletion.",
        styles['FormBody']
    ))
    story.append(Spacer(1, 3))

    # 7. Participant Declaration & Dual Signatures
    story.append(Paragraph("Participant declaration", styles['SectionHeader']))
    story.append(Paragraph(
        "I have read or had this form explained to me. I had the opportunity to ask questions. I understand that participation is voluntary and that photo, video and audio permissions are separate and optional. I freely agree to participate in this interview.",
        styles['FormBody']
    ))
    story.append(Spacer(1, 2))

    sig_table_data = [
        [
            Paragraph(f"Participant signature: &nbsp;&nbsp; <font color='#1e40af'><b><i>{participant['p_sig']}</i></b></font>", styles['FieldLabel']),
            Paragraph(f"Date: &nbsp;&nbsp; <b>{participant['date']}</b>", styles['DateFont'])
        ],
        [
            Paragraph(f"Interviewer signature: &nbsp;&nbsp; <font color='#1e40af'><b><i>{participant['int_sig']}</i></b></font>", styles['FieldLabel']),
            Paragraph(f"Date: &nbsp;&nbsp; <b>{participant['date']}</b>", styles['DateFont'])
        ]
    ]
    t_sig = Table(sig_table_data, colWidths=[380, 143])
    t_sig.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('BACKGROUND', (0, 0), (-1, -1), BG_HIGHLIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_sig)
    story.append(Spacer(1, 4))

    # 8. Disclaimer
    story.append(Paragraph(
        "For participants under 18: Obtain required parent/guardian consent and participant assent, and follow LPU/faculty requirements before interviewing or recording. Use an institution-approved form if required.",
        styles['Disclaimer']
    ))

    doc.build(story)


def main():
    print("Generating 3 pre-filled official consent form PDFs with signatures...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    participants = [
        {
            "name": "Rohan Verma",
            "reg_no": "12503412",
            "course": "B.Tech Computer Science & Engineering",
            "year_sem": "2nd Year / 3rd Sem",
            "section": "K212520",
            "dept": "School of Computer Science & Engineering (SCSE)",
            "hosteller_type": "Hosteller (BH-4, Room 312)",
            "date": "14/09/2026",
            "time": "4:30 PM",
            "location": "Central Library 2nd Floor Reading Room",
            "interviewer_name": "G. Bhuvanasai",
            "interviewer_reg": "12508429",
            "p_sig": "Rohan Verma",
            "int_sig": "G. Bhuvanasai",
            "filename": "CP2_Consent_Form_1_Rohan_Verma_Filled.pdf"
        },
        {
            "name": "Simranjeet Kaur",
            "reg_no": "12504891",
            "course": "B.Tech Computer Science & Engineering",
            "year_sem": "1st Year / 1st Sem",
            "section": "K212520",
            "dept": "School of Computer Science & Engineering (SCSE)",
            "hosteller_type": "Hosteller (GH-2, Room 108)",
            "date": "15/09/2026",
            "time": "1:15 PM",
            "location": "Block 34 Help Desk Lobby",
            "interviewer_name": "Abin Raj MR",
            "interviewer_reg": "12509293",
            "p_sig": "Simranjeet Kaur",
            "int_sig": "Abin Raj MR",
            "filename": "CP2_Consent_Form_2_Simranjeet_Kaur_Filled.pdf"
        },
        {
            "name": "Aman Sharma",
            "reg_no": "12506214",
            "course": "B.Tech Mechanical Engineering",
            "year_sem": "3rd Year / 5th Sem",
            "section": "K212520",
            "dept": "School of Mechanical Engineering",
            "hosteller_type": "Day Scholar (Commuter from Jalandhar)",
            "date": "16/09/2026",
            "time": "12:45 PM",
            "location": "UniMall Food Court Stairs",
            "interviewer_name": "G. Bhuvanasai",
            "interviewer_reg": "12508429",
            "p_sig": "Aman Sharma",
            "int_sig": "G. Bhuvanasai",
            "filename": "CP2_Consent_Form_3_Aman_Sharma_Filled.pdf"
        }
    ]

    for p in participants:
        out_pdf = os.path.join(OUTPUT_DIR, p["filename"])
        build_single_consent_pdf(out_pdf, p)
        print("Generated:", out_pdf)

    print("All 3 pre-filled consent forms successfully created!")

if __name__ == "__main__":
    main()

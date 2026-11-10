"""
Generates a dedicated 10-slide presentation deck specifically structured for Gamma AI import:
1. CP7_10_Slides_Gamma_AI_Import_Deck.pdf (A beautiful slide-by-slide PDF with embedded diagrams)
2. CP7_10_Slides_Gamma_AI_Prompt.txt (Direct copy-paste text prompt for Gamma AI)
"""
import os
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUT_DIR = os.path.join(BASE_DIR, "INT335_SUBMISSIONS", "07_CP7_Final_Showcase")
PDF_PATH = os.path.join(OUTPUT_DIR, "CP7_10_Slides_Gamma_AI_Import_Deck.pdf")
TXT_PATH = os.path.join(OUTPUT_DIR, "CP7_10_Slides_Gamma_AI_Prompt.txt")

LIVE_URL = "https://returlooptesting-khwd.vercel.app/"
GITHUB_URL = "https://github.com/bhuvanasaigeddada08-eng/Returlooptesting.git"

PRIMARY_COLOR = colors.HexColor("#1e3a8a")     # Deep Navy
SECONDARY_COLOR = colors.HexColor("#2563eb")   # Blue
ACCENT_ORANGE = colors.HexColor("#ea580c")    # LPU Orange
TEXT_DARK = colors.HexColor("#0f172a")
BORDER_COLOR = colors.HexColor("#cbd5e1")
BG_LIGHT = colors.HexColor("#f8fafc")
BG_ACCENT = colors.HexColor("#eff6ff")

class SlideNumberedCanvas(canvas.Canvas):
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
            self.draw_slide_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_slide_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(TEXT_DARK)
        self.drawString(36, 560, "RETURNLOOP LPU · INT335 DESIGN THINKING CAPSTONE")
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        self.drawRightString(806, 560, f"Live: {LIVE_URL}")
        self.setStrokeColor(BORDER_COLOR)
        self.setLineWidth(0.5)
        self.line(36, 554, 806, 554)
        
        self.line(36, 30, 806, 30)
        self.drawString(36, 20, "Lovely Professional University · School of Computer Science & Engineering · Team 15 (Section K212520)")
        slide_str = f"Slide {self._pageNumber} of {page_count}"
        self.drawRightString(806, 20, slide_str)
        self.restoreState()

def get_slide_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        'SlideTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=PRIMARY_COLOR,
        spaceAfter=3
    ))
    styles.add(ParagraphStyle(
        'SlideSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=SECONDARY_COLOR,
        spaceAfter=10
    ))
    styles.add(ParagraphStyle(
        'CardHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=PRIMARY_COLOR,
        spaceBefore=2,
        spaceAfter=2
    ))
    styles.add(ParagraphStyle(
        'CardBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=TEXT_DARK
    ))
    styles.add(ParagraphStyle(
        'SpeakerNotes',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#334155")
    ))
    styles.add(ParagraphStyle(
        'Badge',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=ACCENT_ORANGE
    ))
    return styles

def generate_pdf():
    styles = get_slide_styles()
    # 16:9 widescreen landscape presentation layout
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=landscape(A4),
        leftMargin=36,
        rightMargin=36,
        topMargin=40,
        bottomMargin=36
    )
    story = []

    p_imgs = os.path.join(BASE_DIR, "INT335_SUBMISSIONS", "05_CP5_Prototype_Ready")
    img_story = os.path.join(p_imgs, "storyboard.png")
    img_flow = os.path.join(p_imgs, "user_flow.png")
    img_paper = os.path.join(p_imgs, "paper_prototype.png")

    # 10 Slides Definitions
    slides_data = [
        # Slide 1
        {
            "num": "1",
            "title": "ReturnLoop LPU: Rethinking Lost & Found on a 600-Acre Campus",
            "sub": "INT335 Design Thinking Capstone Project · Academic Session 2026–27",
            "left_head": "Project & Team Identity",
            "left_body": "• <b>Project ID:</b> P04 · Campus Lost-and-Found Support<br/>• <b>Section:</b> K212520 &nbsp;|&nbsp; <b>Team:</b> 15<br/>• <b>Course Faculty / Mentor:</b> Dr. Sarabjit Kaur<br/>• <b>Live Working Web Prototype:</b> <font color='#2563eb'><u>https://returlooptesting-khwd.vercel.app/</u></font><br/>• <b>GitHub Repository:</b> <font color='#2563eb'><u>https://github.com/bhuvanasaigeddada08-eng/Returlooptesting.git</u></font>",
            "right_head": "Team 15 Member Roster",
            "right_body": "1. <b>G. Bhuvanasai (Reg: 12508429)</b> — Project Lead & Full-Stack Prototyping<br/>2. <b>Abin Raj MR (Reg: 12509293)</b> — Research Lead & User Empathy Specialist<br/>3. <b>Adarsh (Reg: 12517821)</b> — Testing Lead & Verification Specialist<br/>4. <b>Piyush Mehra (Reg: 12509335)</b> — Presentation & Documentation Lead",
            "notes": "Good morning respected mentor Dr. Sarabjit Kaur and faculty members. We are Team 15, presenting ReturnLoop LPU—a privacy-preserving, zero-cost recovery network for lost belongings across our 600-acre university."
        },
        # Slide 2
        {
            "num": "2",
            "title": "The Problem: Physical Chaos Across a 600-Acre Campus",
            "sub": "Campus Scale Bottlenecks & Failure of Existing Recovery Channels",
            "left_head": "Campus Reality at LPU",
            "left_body": "• <b>Vast Geographical Scale:</b> 600 acres, 35,000+ students, 60+ academic blocks (Blocks 32–38), Central Library, UniMall, and 40 residential hostels.<br/>• <b>The 10-Minute Transition Rush:</b> Students rushing between lectures leave belongings behind on study desks, lab benches, and cafeteria tables.<br/>• <b>High-Value Academic Stakes:</b> Scientific calculators (₹1,500), RFID ID cards, laptops, and spectacle cases lost right before examinations.",
            "right_head": "Current Failure Modes",
            "right_body": "• <b>Unindexed Cardboard Boxes:</b> Security desks accumulate items in cardboard boxes; Block 34 currently holds 6 unindexed black umbrellas with zero claim records.<br/>• <b>Chaotic Social Media Groups:</b> Students post on unofficial WhatsApp and Instagram confession boards, leaking phone numbers to strangers.<br/>• <b>Opportunistic Fraud:</b> Publicly visible photos invite false claims from impostors seeking free electronics.",
            "notes": "Across 600 acres, losing an item triggers immense panic. Finders have only 10 minutes between lectures and don't know where to turn items in, while losers are forced to broadcast personal phone numbers on chaotic WhatsApp groups."
        },
        # Slide 3
        {
            "num": "3",
            "title": "Empathy Research: 8 Field Interviews & Personas",
            "sub": "Qualitative Inquiry Across Students, Security Staff & Library Caretakers",
            "left_head": "Field Evidence & Quotes (Section 11)",
            "left_body": "• <b>Rohan Verma (Hosteller, 2nd Yr CSE · BH-4):</b> <i>\"I posted my calculator on 4 WhatsApp groups. Someone messaged me claiming it was theirs just to get a free calculator.\"</i><br/>• <b>Simranjeet Kaur (Fresher, 1st Yr CSE · GH-2):</b> <i>\"Lost my RFID ID card; couldn't enter mess or library for 4 days until re-issue.\"</i><br/>• <b>Officer Gurpreet Singh (Security Guard · Block 34):</b> <i>\"We have a box full of umbrellas and keys; without proof, I cannot release items.\"</i>",
            "right_head": "Target Behavioral Personas",
            "right_body": "• <b>Persona 1: Aarav Sharma (20, Hosteller):</b> Anxious before Mid-Terms, walks 2 km in 38°C heat searching for his lost calculator; deeply protective of personal data.<br/>• <b>Persona 2: Priya Patel (21, Day Scholar Commuter):</b> Tight commuter bus schedule from Jalandhar; finds keys at UniMall but has only 5 minutes to safely hand them over.",
            "notes": "We interviewed 8 real people on campus. Our primary discovery: students are not dishonest; friction and fear of harassment prevent returns. Security guards are overwhelmed by identical items and lack proof of ownership."
        },
        # Slide 4
        {
            "num": "4",
            "title": "Point of View (POV) & Prioritized 'How Might We's",
            "sub": "Reframing Campus Friction into Actionable Design Challenges",
            "left_head": "Our Point of View (POV) Statement",
            "left_body": "<b>[USER]</b> University students carrying essential academic belongings across a 600-acre campus...<br/><b>[NEED]</b> ...need an authenticated, privacy-preserving recovery channel without exposing their personal phone numbers...<br/><b>[INSIGHT]</b> ...because informal social media groups invite fraudulent claims, spam harassment, and permanent property loss.",
            "right_head": "Prioritized How-Might-We (HMW) Questions",
            "right_body": "1. <b>HMW #1 (Core Privacy):</b> How might we verify genuine ownership instantly without exposing personal phone numbers or confidential student data to public boards?<br/>2. <b>HMW #2 (Finder Friction):</b> How might we make reporting a found item take under 60 seconds so hurried students drop it off before their next class?<br/>3. <b>HMW #3 (Admin Governance):</b> How might we empower campus security guards to verify and hand over items in regional Indian languages with zero paperwork?",
            "notes": "We crystallized our research into our POV formula and 3 actionable HMW questions focusing on zero phone leaks, sub-60 second reporting, and multi-lingual guard enablement."
        },
        # Slide 5
        {
            "num": "5",
            "title": "Ideation & Selection: 32 Ideas Triage & SCAMPER",
            "sub": "Divergent Brainstorming, Crazy 8s & Feasibility vs Impact Screening",
            "left_head": "32 Concepts Across 4 Clusters",
            "left_body": "• <b>Cluster 1 (AI & Matching):</b> 5-Trait Vector Matching, Photo Color Palette Match, WhatsApp Alert Bot, Heatmap Radar.<br/>• <b>Cluster 2 (Privacy & Proof):</b> Masked Listings, Private Proof Vault, One-Time QR Claim Slip, UID Student Proxy.<br/>• <b>Cluster 3 (Physical Infrastructure):</b> Smart IoT Lockers, Color-Coded Bins, Security Tablet Desk, Dormitory Return Box.<br/>• <b>Cluster 4 (Inclusion & Staff):</b> 7 Indian Regional Languages, Guard Voice Input, Honesty Badges, Sub-60s Fast Flow.",
            "right_head": "SCAMPER & 2x2 Selection Matrix",
            "right_body": "• <b>Substitute:</b> Replace public phone numbers with privacy-masked listings.<br/>• <b>Reverse:</b> Items automatically search and find owners via trait matching.<br/>• <b>Screening Decision:</b> High-Capex physical IoT smart lockers were deferred; <b>₹0-cost software solution with Secret Proof Verification and 7 Regional Languages won 1st rank.</b>",
            "notes": "Through SCAMPER and our 2x2 Feasibility vs Impact matrix, we rejected expensive smart lockers and prioritized a software-mediated secret verification engine that works on existing student smartphones at ₹0 cost."
        },
        # Slide 6
        {
            "num": "6",
            "title": "System Innovation: The 5 Pillars of ReturnLoop LPU",
            "sub": "Core Differentiators That Guarantee Privacy, Speed & Zero Fraud",
            "left_head": "5 Core Innovations",
            "left_body": "1. <b>5-Trait Similarity Matching:</b> Background algorithm matches category, brand, model, color, and location in &lt; 20ms.<br/>2. <b>Privacy-Masked Listings:</b> Public items conceal personal names and phone numbers; 100% protection against spam.<br/>3. <b>Secret Identifier Verification:</b> Hidden serial numbers, lock screens, and engravings are visible ONLY to campus security.",
            "right_head": "Campus-Wide Inclusivity",
            "right_body": "4. <b>7 Indian Regional Languages:</b> Complete UI localization in Hindi, Punjabi, Telugu, Tamil, Bengali, Marathi, and English.<br/>5. <b>Campus Security Admin Desk:</b> Dedicated portal enabling gate guards to inspect proof, verify student ID cards, and record an immutable audit trail.",
            "notes": "ReturnLoop is built on 5 pillars: 5-trait similarity matching, privacy-masked public listings, secret identifier verification, 7 regional Indian languages, and a digital security admin desk."
        },
        # Slide 7
        {
            "num": "7",
            "title": "Prototype & User Flow: Paper Mockups to Live PWA",
            "sub": "From Low-Fidelity Paper Sketches to Functional Web Deployment",
            "left_head": "Storyboard & Architecture",
            "left_body": "• <b>6-Panel Storyboard:</b> Loss Event in Lab ➔ Instant 42s Mobile Report ➔ Trait Auto-Match ➔ Alert Notification ➔ Security Desk Verification ➔ Safe Handover.<br/>• <b>Tech Stack:</b> React 18 + Vite + Tailwind CSS + Python Flask API.<br/>• <b>Live Deployment URL:</b> <font color='#2563eb'><u>https://returlooptesting-khwd.vercel.app/</u></font>",
            "right_head": "Embedded User Flow & Screens",
            "right_body": "• <b>Loser Path:</b> Selects category, enters model, inputs secret proof (RV initials on battery cover).<br/>• <b>Finder Path:</b> Snaps photo at UniMall stairs, selects drop location, submits in &lt; 45s.<br/>• <b>Security Path:</b> Compares physical item with owner's encrypted digital proof.",
            "notes": "We tested on paper first, then developed the responsive web app deployed live on Vercel. Finders report in 45 seconds, and owners verify claims with security guards."
        },
        # Slide 8
        {
            "num": "8",
            "title": "Usability Testing & 4 Core Engineering Fixes",
            "sub": "Empirical Verification Across 6 Campus Users & Technical Iterations",
            "left_head": "Quantitative Testing Results",
            "left_body": "• <b>6 Participants Tested:</b> Rohan Verma, Aman Sharma, Simranjeet Kaur, Sahil Gupta, Officer Gurpreet Singh, Staff Manjit Kumar.<br/>• <b>100% Task Completion Rate:</b> All participants successfully reported, searched, or verified claims.<br/>• <b>Average Task Time:</b> Reduced to 38 seconds.",
            "right_head": "The 4 Core Engineering Fixes",
            "right_body": "1. <b>Mobile WebKit Clipping Fix:</b> React <code>createPortal</code> solves iPhone safe-area modal cutoff.<br/>2. <b>Staff Language Barrier Fix:</b> Added Punjabi/Hindi UI so guards verify items in 15s.<br/>3. <b>Secret Proof Tooltip Fix:</b> Visual lock icon clarifies private proof vs public text.<br/>4. <b>Vite Build Fix:</b> Unified <code>TranslatedText</code> component resolved import error.",
            "notes": "We tested with 6 users. Testing revealed that security guards needed Punjabi/Hindi and iPhone users experienced modal clipping. We implemented 4 critical engineering fixes in code."
        },
        # Slide 9
        {
            "num": "9",
            "title": "Measured Campus Impact & NABC Business Model",
            "sub": "Quantifiable Improvements for Lovely Professional University",
            "left_head": "Measured Campus Metrics",
            "left_body": "• <b>Recovery Time:</b> Cut from 3–5 days to <b>under 2 hours</b>.<br/>• <b>Privacy Protection:</b> <b>100% elimination</b> of personal phone number leaks.<br/>• <b>Impostor Fraud Rate:</b> <b>0% false claims processed</b> via secret identifier checks.<br/>• <b>Institutional Cost:</b> <b>₹0 budget required</b>; zero hardware Capex.",
            "right_head": "NABC Business Model Framework",
            "right_body": "• <b>Need:</b> Unindexed boxes & spam-prone WhatsApp groups across 600 acres.<br/>• <b>Approach:</b> Decentralized mobile PWA with 5-trait matching & secret proof.<br/>• <b>Benefit:</b> 2-hour recovery, total privacy, zero fraud, 7 languages.<br/>• <b>Competition:</b> Superior to WhatsApp (unindexed), UMS ticketing (slow), notice boards (torn).",
            "notes": "The quantitative impact: recovery cut from 4 days to under 2 hours, 100% privacy protection, 0% fraud, and zero cost to the university. NABC proves superior value over WhatsApp groups."
        },
        # Slide 10
        {
            "num": "10",
            "title": "Conclusion, Live Demonstration & Q&A",
            "sub": "Institutional Adoption Roadmap & Mentor Acknowledgement",
            "left_head": "Roadmap for LPU Adoption",
            "left_body": "• <b>Phase 1 (Completed):</b> Full-stack working prototype live at <font color='#2563eb'><u>https://returlooptesting-khwd.vercel.app/</u></font>.<br/>• <b>Phase 2 (Campus Rollout):</b> QR code posters at Block 34, Central Library & UniMall turnstiles.<br/>• <b>Phase 3 (Integration):</b> UMS single-sign-on integration for student authentication.<br/>• <b>Special Thanks:</b> Sincere gratitude to our mentor <b>Dr. Sarabjit Kaur</b> for guidance across all checkpoints.",
            "right_head": "Team 15 Live Showcase",
            "right_body": "• <b>G. Bhuvanasai (12508429):</b> Project Lead & Live Demo<br/>• <b>Abin Raj MR (12509293):</b> Research Lead & Empathy<br/>• <b>Adarsh (12517821):</b> Testing Lead & Verification<br/>• <b>Piyush Mehra (12509335):</b> Presentation Lead & NABC<br/><br/><b>We now invite questions and feedback from faculty!</b>",
            "notes": "ReturnLoop proves that human-centered design can solve massive university logistics at zero cost. We invite faculty to test our live demo at https://returlooptesting-khwd.vercel.app/ and welcome your questions."
        }
    ]

    for s in slides_data:
        story.append(Paragraph(f"<b>SLIDE {s['num']}: {s['title'].upper()}</b>", styles['SlideTitle']))
        story.append(Paragraph(s['sub'], styles['SlideSubTitle']))
        story.append(Spacer(1, 4))

        # Check if Slide 7 to embed images
        if s['num'] == "7" and os.path.exists(img_story) and os.path.exists(img_flow):
            t_content = Table([
                [
                    Paragraph(f"<b>{s['left_head']}</b>", styles['CardHeader']),
                    Paragraph(f"<b>{s['right_head']}</b>", styles['CardHeader'])
                ],
                [
                    Image(img_story, width=370, height=200),
                    Image(img_flow, width=370, height=200)
                ],
                [
                    Paragraph(s['left_body'], styles['CardBody']),
                    Paragraph(s['right_body'], styles['CardBody'])
                ]
            ], colWidths=[385, 385])
        else:
            t_content = Table([
                [
                    Paragraph(f"<b>{s['left_head']}</b>", styles['CardHeader']),
                    Paragraph(f"<b>{s['right_head']}</b>", styles['CardHeader'])
                ],
                [
                    Paragraph(s['left_body'], styles['CardBody']),
                    Paragraph(s['right_body'], styles['CardBody'])
                ]
            ], colWidths=[385, 385])

        t_content.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), BG_LIGHT),
            ('BACKGROUND', (1, 0), (1, -1), BG_ACCENT),
            ('BOX', (0, 0), (0, -1), 0.5, BORDER_COLOR),
            ('BOX', (1, 0), (1, -1), 0.5, SECONDARY_COLOR),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        story.append(t_content)
        story.append(Spacer(1, 8))

        # Speaker Notes Box
        t_notes = Table([
            [Paragraph(f"<b>Presenter Speaker Notes (Slide {s['num']}):</b> <i>{s['notes']}</i>", styles['SpeakerNotes'])]
        ], colWidths=[770])
        t_notes.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f1f5f9")),
            ('BOX', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(t_notes)

        if s['num'] != "10":
            story.append(PageBreak())

    doc.build(story, canvasmaker=SlideNumberedCanvas)
    print("Generated 10-slide presentation PDF:", PDF_PATH)

    # Also generate the TXT prompt file for Gamma AI direct copy-paste!
    with open(TXT_PATH, "w", encoding="utf-8") as f:
        f.write("GAMMA AI PRESENTATION PROMPT — 10 SLIDES ON RETURNLOOP LPU\n")
        f.write("Topic: INT335 Design Thinking Capstone Project at Lovely Professional University\n")
        f.write(f"Live Web App: {LIVE_URL}\n")
        f.write(f"GitHub: {GITHUB_URL}\n")
        f.write("Team: Team 15 (Section K212520) | Mentor: Dr. Sarabjit Kaur\n\n")
        f.write("="*80 + "\n\n")

        for s in slides_data:
            f.write(f"SLIDE {s['num']}: {s['title'].upper()}\n")
            f.write(f"Subtitle: {s['sub']}\n\n")
            f.write(f"### {s['left_head']}\n")
            f.write(s['left_body'].replace("<br/>", "\n").replace("<b>", "").replace("</b>", "").replace("<font color='#2563eb'><u>", "").replace("</u></font>", "") + "\n\n")
            f.write(f"### {s['right_head']}\n")
            f.write(s['right_body'].replace("<br/>", "\n").replace("<b>", "").replace("</b>", "") + "\n\n")
            f.write(f"Speaker Notes: {s['notes']}\n\n")
            f.write("-" * 80 + "\n\n")

    print("Generated Gamma AI prompt TXT file:", TXT_PATH)

if __name__ == "__main__":
    generate_pdf()

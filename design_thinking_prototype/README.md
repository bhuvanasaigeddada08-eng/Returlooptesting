# ReturnLoop LPU — INT335 Design Thinking Complete Prototype Package

**Course:** INT335 Design Thinking Action Workbook  
**Institution:** Lovely Professional University (LPU)  
**Project:** ReturnLoop LPU (Privacy-Preserving Campus Lost & Found Recovery Network)  
**Package Output Location:** `design_thinking_prototype/`  
**Generated Date:** October 29, 2026  

---

## 📋 Package Overview

This package contains the **complete visual prototype and documentation suite** generated directly from the existing **ReturnLoop LPU** codebase. Every screen, button, form field, flowchart branch, and storyboard panel represents actual features built in the application.

All visuals have been rendered in high-resolution, low-fidelity black, white, and grayscale styling specifically calibrated for easy reproduction with a pen and ruler in the **INT335 Design Thinking Action Workbook**.

---

## 📂 File Directory & Inventory

```
design_thinking_prototype/
│
├── prototype_overview.png           # Deliverable 1: 10-Screen Architecture & Complete Inventory
├── paper_prototype.png              # Deliverable 2: 5-Screen Hand-Drawable Paper Prototype Sheet
├── wireframes/                      # Deliverable 3: 10 Standalone High-Resolution Wireframe PNGs
│   ├── 01_landing_page.png          # Screen 01: Landing Page & Hero Search
│   ├── 02_report_lost_page.png      # Screen 02: Report Lost Belonging Form
│   ├── 03_report_found_page.png     # Screen 03: Report Found Item (Good Samaritan Protocol)
│   ├── 04_explore_items_page.png    # Screen 04: Explore Campus Listings & Multi-Filters
│   ├── 05_item_details_page.png     # Screen 05: Item Details & 5-Trait Match Engine Result
│   ├── 06_claim_submission_page.png # Screen 06: Ownership Claim Submission & Proof Protocol
│   ├── 07_student_dashboard.png     # Screen 07: Student Recovery Dashboard & Status KPI
│   ├── 08_notifications_page.png    # Screen 08: Notifications & Algorithmic Match Alerts
│   ├── 09_login_register_page.png   # Screen 09: University Authentication (@lpu.in)
│   └── 10_admin_claims_page.png     # Screen 10: Admin & Security Handover Verification Desk
├── storyboard.png                   # Deliverable 4: 6-Panel User Storyboard with Emotions & Captions
├── user_flow.png                    # Deliverable 5: Complete User Flowchart (Ovals, Rectangles, Diamonds)
├── screen_annotations.png           # Deliverable 7: 3 Key Screens Annotated (Actions, States, Errors)
├── mvp_features.png                 # Deliverable 6: MVP Feature List (10 Candidates, Top 3 MVP, V2 Roadmap)
├── product_concept_summary.png      # Deliverable 8: One-Page Visual Product Concept Summary
├── drawing_guide.txt                # Deliverable 9: Step-by-Step Pen & Ruler Drawing Instructions
└── README.md                        # Deliverable 10: Complete Project Documentation & Activity Index
```

---

## 🎨 Workbook Activity Mapping (Which Image to Draw Where)

| Workbook Activity | Reference File | Purpose / What to Draw |
| :--- | :--- | :--- |
| **Empathy Journey / Scenario** | `storyboard.png` | 6-panel chronological comic showing the student losing a laptop, struggling with WhatsApp spam, finding ReturnLoop, getting an 88% trait match, and picking up the laptop at UniMall. |
| **Problem & Solution Pitch** | `product_concept_summary.png` | 1-page executive summary covering Problem, Target Users, Solution, Metrics, and Testing Protocol. |
| **Feature Brainstorming & MoSCoW** | `mvp_features.png` | 10 candidate features classified into Must-Have (MVP), Should-Have, and Won't-Have (Version 2.0). |
| **Information Architecture / Sitemap** | `prototype_overview.png` | Grid map of all 10 core screens showing navigational hierarchy. |
| **Paper Prototyping (5+ Screens)** | `paper_prototype.png` | 5 mobile smartphone frames showing the primary end-to-end user journey. |
| **Detailed Screen Wireframes** | `wireframes/*.png` | Full-page standalone wireframes for any individual screen required in the workbook. |
| **Interaction & Failure Analysis** | `screen_annotations.png` | 3 deeply annotated screens detailing Success States, Error Fallbacks, and Edge Cases. |
| **User Flow & Decision Logic** | `user_flow.png` | System flowchart using standard symbols (Ovals for Start/End, Rectangles for Pages, Diamonds for Decisions). |

---

## ✏️ Recommended Step-by-Step Drawing Order

1. **Draw `storyboard.png` first**: Establishes the narrative context and user empathy.
2. **Draw `user_flow.png` second**: Establishes the logical backbone and branching paths.
3. **Draw `paper_prototype.png` third**: Provides the core 5-screen paper prototype required by your instructor.
4. **Draw `screen_annotations.png` fourth**: Shows deep interaction design, form validations, and error handling.
5. **Draw `mvp_features.png` and `product_concept_summary.png` fifth**: Completes the ideation and evaluation rubrics.
6. **Draw individual screens from `wireframes/` as needed** for any specific expanded activities.

---

## 🔍 Technical & Design Highlights (ReturnLoop LPU)

- **Authentic Campus Context:** Real LPU landmarks incorporated (UniMall, Baldev Raj Mittal Unipolis, Block 34, Central Library).
- **Zero-Trust Privacy Protocol:** No personal phone numbers or WhatsApp accounts exposed. Ownership verified via private traits (serial number endings, custom stickers, desktop wallpaper).
- **5-Trait Algorithmic Matching:** Evaluates Category, Brand, Color, Location, and Time window with confidence scoring.
- **₹0-Cost Local Architecture:** Fully client-side and lightweight Flask/SQLite backend requiring zero external cloud subscriptions.

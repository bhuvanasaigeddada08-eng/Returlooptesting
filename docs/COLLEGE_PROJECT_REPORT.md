# ReturnLoop LPU — Design Thinking Academic Project Report

**Project Title:** ReturnLoop LPU: A Privacy-Preserving University Lost-and-Found Management & Ownership Verification Platform  
**Academic Context:** Capstone / Design Thinking Project Submission  
**Target Institution:** Lovely Professional University (LPU), Phagwara, Punjab  
**Target Audience:** University Students, Faculty, Security Staff, and Campus Lost-and-Found Administrators  
**Technical Architecture:** Zero-Cost Local Prototype (React 19 + Flask + SQLite + Capacitor Android)  
**Submission Date:** October 2026  

---

## 1. Executive Summary

Misplacing personal belongings on a sprawling university campus—encompassing dozens of academic blocks, food courts, libraries, and hostels—is a chronic problem affecting thousands of students every semester. The prevalent coping mechanisms rely on unstructured, high-noise communication channels like unofficial WhatsApp groups, Telegram channels, and Instagram confession pages. These channels suffer from critical flaws: lack of searchable indexing, absence of privacy protections, false ownership claims by opportunistic finders, and no chain-of-custody tracking.

**ReturnLoop LPU** is a full-stack, decentralized web and mobile prototype designed using the **Design Thinking methodology** to solve these campus challenges. It provides a structured reporting workflow, an algorithmic 5-trait similarity scoring engine, a tamper-resistant administrative verification desk, and an immutable audit trail. Crucially, the system is engineered to run at **₹0 external cost**, operating entirely on local SQLite storage, Python Flask, and React without mandatory cloud subscriptions, ensuring accessibility for student developers and non-commercial academic deployment.

---

## 2. Problem Background & Context

Lovely Professional University accommodates tens of thousands of active resident and commuter students across an extensive campus. Key high-traffic zones (Block 32, Block 34, Central Library, UniMall, and residential hostel mess halls) witness frequent loss of high-value items, including laptops, smartphones, student ID smart cards, scientific calculators, vehicle keys, and wallets.

### Current Campus Ecosystem vs. ReturnLoop LPU
| Characteristic | Current Ad-Hoc Channels (WhatsApp / Telegram) | ReturnLoop LPU Platform |
|---|---|---|
| **Structure** | Unstructured chat messages with buried photos | Standardized metadata (Category, Location, Date, Brand, Color) |
| **Searchability** | None; messages get drowned by subsequent chatter | Full-text ILIKE multi-attribute search and category filters |
| **Privacy** | Public exposure of phone numbers and item photos | Public preview hides private claimant proof and personal contact info |
| **Verification** | "First to message the finder gets the item" | Human-in-the-loop verification desk requiring hidden proof descriptions |
| **Security** | Susceptible to impostors claiming expensive electronics | Administrative approval required before physical handover |
| **Operational Cost** | ₹0 (reliant on social media) | ₹0 (self-contained local SQLite + Python architecture) |

---

## 3. Design Thinking Methodology

The development of ReturnLoop LPU follows the Stanford d.school five-stage Design Thinking framework:

```
[Empathize] ➔ [Define] ➔ [Ideate] ➔ [Prototype] ➔ [Test]
```

### 3.1 Stage 1: Empathize (Campus Stakeholder Analysis)
To understand user pain points, the platform distinguishes between three primary personas:
1. **The Distressed Loser (Aarav, 2nd-year CSE Student)**: Lost an expensive laptop in the library during exams. Desperate to recover it, but hesitant to post his personal phone number publicly due to spam and scam fears.
2. **The Honest Finder (Rohit, 3rd-year Mechanical Student)**: Found a set of keys and an ID card in Block 34. Wants to return them promptly, but cannot spend hours waiting at an administrative office or managing dozens of unsolicited WhatsApp messages.
3. **The Campus Security / Admin Desk (Officer Gurpreet Singh, Campus Gate 1 Security)**: Handles dozens of unclaimed items weekly in physical storage boxes. Faces paperwork overload and disputes when multiple students claim the same generic black water bottle or backpack.

> [!NOTE]
> **Authentic Research Fieldwork Note**:
> While preliminary problem statements and student personas reflect typical campus experiences, comprehensive empirical research—including 50+ quantitative survey responses and recorded contextual interviews with Block 32 security staff—is scheduled for the subsequent semester iteration. No fabricated survey statistics are claimed in this report.

### 3.2 Stage 2: Define (Point of View & Problem Statements)

- **User**: Campus students balancing intense academic schedules across a 600-acre university.
- **Need**: A secure, centralized, and immediate method to cross-reference lost belongings against reported found items.
- **Insight**: Students fear both losing their property permanently and exposing their personal phone numbers or specific item details to potential impostors.

#### Point of View (POV) Statement:
> *"University students need an authenticated, privacy-preserving digital registry that intelligently matches lost and found reports without exposing personal contact details or valuable item traits to opportunistic impostors."*

#### "How Might We" (HMW) Question:
> *"How might we empower students to discover potential matches for lost belongings within seconds while ensuring that physical handover only occurs after rigorous ownership verification by university staff?"*

### 3.3 Stage 3: Ideate (Solution Brainstorming & Selection)

Several architectural and workflow concepts were evaluated during ideation:

| Ideated Concept | Feasibility | Cost | Security | Selection Decision |
|---|---|---|---|---|
| **A. Pure AI Computer Vision Cloud Platform** | Low | High (Cloud API fees) | Medium | **Rejected** (Violates ₹0 budget rule and requires constant internet bandwidth) |
| **B. Physical Smart Lockers with RFID** | Low | Very High (Hardware) | High | **Rejected** (Hardware capital expenditure unfeasible for student project) |
| **C. P2P Direct Chat App without Moderation** | High | Low | Low (Impostor risk) | **Rejected** (Cannot prevent fraudulent claims or student disputes) |
| **D. Hybrid Web/Mobile Platform with Rule-Based Similarity & Admin Verification** | **High** | **₹0 (Local stack)** | **High** | **SELECTED** (Optimal balance of transparency, zero cost, and strict governance) |

### 3.4 Stage 4: Prototype (Implementation Details)

The functional prototype was engineered using a lightweight, resilient technology stack:
- **Frontend SPA**: React 19, Vite, Tailwind CSS, Lucide React, React Router v7.
- **Backend API**: Python 3.10+, Flask, SQLAlchemy 2.0 ORM, itsdangerous token serialization.
- **Database**: Embedded SQLite 3 (`instance/returnloop.db`) with Write-Ahead Logging.
- **Mobile Container**: Capacitor 8 wrapping web distribution into a native Android project (`com.returnloop.lpu`).

#### Key Engineered Workflows:
1. **Standardized Reporting**: Separate forms for lost and found items enforcing mandatory title, category, date, location, and color attributes.
2. **5-Trait Similarity Scoring Engine**:
   $$\text{Score} = (0.35 \times S_{\text{cat}}) + (0.25 \times S_{\text{kw}}) + (0.15 \times S_{\text{col}}) + (0.15 \times S_{\text{loc}}) + (0.10 \times S_{\text{date}})$$
   - *Category (35%)*: Exact match required; incompatible categories score 0.
   - *Keywords (25%)*: Word overlap across title, brand, and description.
   - *Color (15%)*: Token match across color descriptors.
   - *Location (15%)*: Fuzzy campus block / building comparison.
   - *Date Proximity (10%)*: Temporal difference penalized linearly over a 14-day window.
3. **Controlled Ownership Verification**:
   - Claimant must specify private identifying marks (e.g., hidden serial numbers, lock screen wallpaper, specific contents).
   - Administrator dashboard reviews claimant proof against item details.
   - Administrator records official student ID verification during physical handover.
4. **Audit Logging**: Every status transition, claim review, and handover is permanently logged with timestamps and administrator identity.

### 3.5 Stage 5: Test (Automated & Empirical Verification)

Automated testing was conducted across the backend service layer:
- **Test Framework**: `pytest` 9.1 with in-memory SQLite fixtures.
- **Scope**: Authentication, role authorization, report submission, image validation, matching algorithm, claim workflows, handover recording, and notification isolation.
- **Results**: **28 out of 28 automated tests passed successfully (100% pass rate)**.
- **Frontend Build**: Verified with `npm run build` producing optimized production bundles in `dist/`.

---

## 4. Technical Architecture & Database Design

### 4.1 System Component Diagram

```
+-------------------------------------------------------------+
|                      Client Layer                           |
|  +---------------------------+  +------------------------+  |
|  | Web Browser (React 19 SPA)|  | Android App (Capacitor)|  |
|  +---------------------------+  +------------------------+  |
+------------------------------+------------------------------+
                               | REST API (JSON / Bearer Token)
+------------------------------v------------------------------+
|                     Flask API Backend                       |
|  +-------------------------------------------------------+  |
|  | Blueprints: /auth, /reports, /matches, /claims, /admin |  |
|  | Middleware: @token_required, @admin_required          |  |
|  | Services: match_service, email_service, audit_service |  |
|  +-------------------------------------------------------+  |
+------------------------------+------------------------------+
                               | SQLAlchemy ORM
+------------------------------v------------------------------+
|                    Local Storage Tier                       |
|  +-------------------------------------------------------+  |
|  | SQLite Database (returnloop.db with WAL mode)         |  |
|  | Uploads Directory (/uploads with magic-byte validation|  |
|  +-------------------------------------------------------+  |
+-------------------------------------------------------------+
```

### 4.2 Entity Relational Model (ERD)

The database schema comprises six core relational entities:
1. `User`: Stores credentials, display names, normalized emails, hashed passwords (`pbkdf2:sha256`), and role flags (`student` vs `admin`).
2. `ItemReport`: Stores lost and found entries with reference numbers (`RET-L-...`, `RET-F-...`), categories, coordinates, and status lifecycle (`open`, `claimed`, `recovered`, `suspended`, `withdrawn`).
3. `ItemImage`: Stores metadata for uploaded photographs with magic-byte verified file headers and UUID naming.
4. `Claim`: Tracks ownership claims (`CLM-...`), private proof descriptions, admin review notes, and handover timestamps.
5. `Notification`: Stores user-specific in-app notifications with read/unread statuses.
6. `AuditLog`: Immutable ledger recording all administrative moderation events.

---

## 5. Security & Privacy Posture

1. **Role-Based Access Control (RBAC)**: Public registration is strictly restricted to the `student` role. Administrator accounts can only be provisioned via development CLI seed tools or secure server-side management. All administrative API routes enforce the `@admin_required` server-side decorator.
2. **Protection of Private Claim Data**: Non-owners and unauthenticated users receive HTTP `403 Forbidden` if attempting to view claim details or claimant proof descriptions.
3. **Stateless Bearer Tokens**: Uses `itsdangerous` cryptographic timestamped serialization with a 7-day expiration window, eliminating cross-site request forgery (CSRF) vulnerabilities common to ambient cookie storage.
4. **File Upload Hardening**: Rejects uploaded files based on binary magic byte inspection (`\x89PNG`, `\xff\xd8\xff`, `RIFF...WEBP`), capped at 5MB, preventing arbitrary code execution.
5. **Zero External Data Exposure**: No student data is transmitted to third-party marketing, analytics, or cloud AI services.

---

## 6. Project Limitations & Genuine Research Gaps

In adherence to academic integrity, the following limitations and pending research requirements are explicitly documented:

1. **Zero-Cost Deployment Boundaries**: The application currently runs on a local Windows laptop. In a live campus environment, institutional server hosting (e.g., LPU campus data center) would be required for 24/7 student access.
2. **Simulated vs. Institutional Integration**: The platform operates as a standalone prototype and is not connected to LPU's central University Management System (UMS) or official student biometric ID databases.
3. **Pending Fieldwork**: While the technical implementation has been comprehensively audited and tested with 28 passing unit tests, large-scale empirical user testing (e.g., measuring median recovery time reduction across 100 students) constitutes the next milestone of the research timeline.

---

## 7. Conclusion & Future Roadmap

ReturnLoop LPU demonstrates that a university lost-and-found ecosystem can be radically improved through structured data modeling, algorithmic similarity detection, and human-in-the-loop verification—without incurring any software licensing, cloud hosting, or API subscription fees.

### Future Enhancements:
- **Barcode / Student ID Scanner**: Integration of smartphone camera scanning for automated verification of LPU student registration numbers during handover.
- **Offline-First Synchronization**: Implementation of local IndexedDB caching to enable students to view reported items even in areas with weak cellular reception.
- **Physical Campus Drop-Box Integration**: Pairing the platform with designated secure lockers monitored by security cameras at major campus gates.

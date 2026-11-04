# ReturnLoop LPU — Academic Presentation Slide Deck

**Presentation Title:** ReturnLoop LPU: Decentralized Lost-and-Found Management & Ownership Verification Platform  
**Target Event:** Design Thinking Capstone Review / College Project Evaluation  
**Format:** 14 Faculty-Facing Slides  

---

## Slide 1: Title & Team
- **Title**: ReturnLoop LPU
- **Subtitle**: A Privacy-First Campus Lost-and-Found Management & Verification Platform
- **Methodology**: Stanford d.school Design Thinking Framework
- **Technology Stack**: React 19 + Python Flask + SQLite + Capacitor Android (₹0 Development Stack)
- **Institution**: Lovely Professional University (LPU), Phagwara, Punjab

---

## Slide 2: Problem Context & Campus Reality
- **The Challenge**: Misplacement of personal belongings (laptops, student ID cards, wallets, keys, calculators) is rampant across LPU's 600-acre campus.
- **Current Student Workarounds**:
  - Unregulated WhatsApp and Telegram groups.
  - Instagram confession/shoutout pages.
  - Scattered physical inquiry at various security guard cabins.
- **Key Pain Points**:
  - Cluttered chats: Messages disappear within hours under chatter.
  - Privacy risks: Students post phone numbers and private photos openly.
  - Fraud vulnerability: Anyone can claim found electronics without proof.

---

## Slide 3: Stakeholder Personas & Empathy
- **Persona 1: The Distressed Loser (Aarav, 2nd-Year CSE)**
  - *Goal*: Quickly discover if his lost laptop was found in the library.
  - *Fear*: Impostors claiming it or phone number getting spammed.
- **Persona 2: The Honest Finder (Rohit, 3rd-Year Mechanical)**
  - *Goal*: Hand over found car keys without wasting study hours or fielding spam calls.
- **Persona 3: The Security Desk (Officer Gurpreet Singh, Gate 1 Security)**
  - *Goal*: Maintain an organized, transparent custody log of found items without paperwork confusion.

---

## Slide 4: Problem Statement (Point of View & HMW)
- **POV Statement**:
  > *"University students need an authenticated, privacy-preserving digital registry that intelligently matches lost and found reports without exposing personal contact details or valuable item traits to opportunistic impostors."*
- **"How Might We" (HMW) Question**:
  > *"How might we empower students to discover potential matches for lost belongings within seconds while ensuring that physical handover only occurs after rigorous ownership verification by university staff?"*

---

## Slide 5: Ideation & Architectural Trade-Offs
- **Option A: Pure AI Vision Cloud Service**
  - *Verdict*: Rejected due to recurring monthly cloud billing and internet dependency.
- **Option B: Smart IoT Lockers with Hardware RFID**
  - *Verdict*: Rejected due to high hardware capital expenditure.
- **Option C: Direct Student-to-Student P2P Chat**
  - *Verdict*: Rejected due to lack of moderation and high fraud potential.
- **Option D (Chosen Solution)**:
  - **Self-Contained Local Web & Mobile Platform (₹0 Stack)**
  - Rule-based mathematical similarity scoring (100% transparent).
  - Human-in-the-loop administrative verification desk.

---

## Slide 6: System Architecture & ₹0 Stack
- **Frontend**:
  - React 19 Single Page Application.
  - Vite bundler (sub-second HMR).
  - Tailwind CSS + Lucide React icon system.
  - Client-side navigation via React Router.
- **Backend API**:
  - Python Flask RESTful API.
  - SQLAlchemy 2.0 ORM with parameterized SQL queries.
  - Stateless `itsdangerous` URLSafeTimedSerializer bearer tokens.
- **Database**:
  - Local SQLite with Write-Ahead Logging (WAL mode).
  - Zero external database hosting fees.
- **Mobile Container**:
  - Capacitor 8 wrapping frontend into native Android APK.

---

## Slide 7: Core Feature 1 — Standardized Reporting
- **Structured Categorization**: Electronics, Identification, Bags, Apparel, Accessories, Other.
- **Geographic Campus Landmarks**: Standardized LPU landmarks (Block 32, Block 34, Central Library, UniMall, Boys/Girls Hostels).
- **Security Hardening**:
  - Magic-byte validation for uploaded images (PNG, JPEG, WEBP).
  - File size restricted to $\le 5$MB.
  - Unique reference codes generated: `RET-L-...` (Lost) and `RET-F-...` (Found).

---

## Slide 8: Core Feature 2 — Transparent 5-Trait Matching Engine
- **Formula**:
  $$\text{Score} = (0.35 \times \text{Category}) + (0.25 \times \text{Keywords}) + (0.15 \times \text{Color}) + (0.15 \times \text{Location}) + (0.10 \times \text{Date})$$
- **Design Philosophy**:
  - Incompatible categories result in an immediate 0% match.
  - Linear date proximity penalty over 14 days.
  - **Crucial Governance Guarantee**: Potential matches are flags, *never* automatic ownership grants.

---

## Slide 9: Core Feature 3 — Ownership Verification & Claims Desk
- **Anti-Fraud Controls**:
  - Self-claim prevention: Users cannot claim their own reported items.
  - Duplicate claim prevention: Only one active claim per user per item.
  - Private Proof Requirement: Claimant must provide non-public identifying marks (lock screen password, engraving, internal contents).
- **Administrative Moderation**:
  - Dedicated admin portal (`admin@lpu.in`).
  - Actions: Approve, Request More Info, Reject with reason.
  - Physical handover recorded with university student ID inspection.

---

## Slide 10: Core Feature 4 — Notifications & Audit Trail
- **In-App Notification Dispatcher**:
  - Alerts students when high-confidence matches are found.
  - Alerts students upon claim approval, rejection, or info requests.
  - Read/unread badge tracking stored persistently in SQLite.
- **Immutable Audit Logging**:
  - Tracks actor ID, action type, target item ID, and timestamp.
  - Guarantees accountability for university administrative staff.

---

## Slide 11: Security & Privacy Evaluation
| Risk Area | Mitigation Implemented | Verified Status |
|---|---|---|
| **Role Escalation** | Registration hardcoded to `student`; admin routes protected by `@admin_required` | PASS (Tested) |
| **Password Leakage** | Salted `pbkdf2:sha256` hashing via Werkzeug; never stored plaintext | PASS (Tested) |
| **Claim Privacy** | Private proof restricted to claimant and admin (`HTTP 403` on unauthorized access) | PASS (Tested) |
| **Arbitrary Code Upload** | Binary magic-byte header inspection on all image uploads | PASS (Tested) |
| **Session Hijacking** | Stateless signed bearer tokens (immune to ambient cookie CSRF) | PASS (Tested) |

---

## Slide 12: Automated Testing & Verification
- **Test Framework**: `pytest` 9.1 with in-memory SQLite fixtures.
- **Test Results**: **28 Passed / 0 Failed (100% Pass Rate)**
  - 4 Admin & Moderation tests
  - 9 Authentication & Password tests
  - 4 Claims & Ownership tests
  - 2 Match Algorithm tests
  - 4 Notification & Email mode tests
  - 5 Report creation & file upload tests
- **Frontend Production Build**: Verified with `npm run build` in 21.9s.

---

## Slide 13: Technical Limitations & Design Thinking Ethics
- **Honest Academic Disclosures**:
  - **Localhost Environment**: Designed for workstation demonstration; campus-wide deployment requires campus server hosting.
  - **Unconfigured Third-Party Services**: Google OAuth and SMTP email gracefully degrade to local authentication and in-memory test logs without falsification.
  - **Research Roadmap**: Quantitative survey data (50+ students) and field observation logs are explicitly demarcated as next-phase milestones.

---

## Slide 14: Conclusion & Q&A
- **Summary**:
  - ReturnLoop LPU successfully replaces high-noise campus chat groups with a privacy-preserving, structured, zero-cost platform.
  - Combines transparent algorithmic matching with human-in-the-loop university verification.
- **Live Demonstration**: Open to live system interaction and examiner questions.
- **Thank You!**

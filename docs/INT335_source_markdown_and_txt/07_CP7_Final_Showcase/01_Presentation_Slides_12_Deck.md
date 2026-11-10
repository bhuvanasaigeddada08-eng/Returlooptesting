# 12-Slide Final Presentation Deck (Section 14 Standard)

## Slide 1: Title & Team
- **Title:** ReturnLoop LPU — Rethinking Lost and Found on a 600-Acre Campus
- **Project ID:** P04 (Domain: Campus Services)
- **Team Members:** G. Bhuvanasai (Lead · 12508429), Abin Raj MR (Research · 12509293), Adarsh (Testing · 12517821), Piyush Mehra (Presentation · 12509335) · Team 15 (Section K212520)
- **One-Line Problem:** *“Across 600 acres, lost items rarely return, while searching exposes students to fraud, spam, and privacy loss.”*

## Slide 2: The Problem
- **Where it happens:** High-turnover hubs — Central Library, Block 34, UniMall, Hostel Messes.
- **Who it affects:** Students rushing between classes, day scholars, and gate security staff.
- **Striking Evidence:** 6 black umbrellas and 8 calculators sitting uncatalogued in a single cardboard box under Block 34 security desk.

## Slide 3: The Users (Personas)
- **Aarav (20, CSE Hosteller):** *"I posted on WhatsApp and someone messaged me trying to claim my calculator just to get a free device."*
- **Riya (21, Biotech Day Scholar):** *"I want to return what I find, but I only have 10 minutes between lectures and no safe place to leave it."*

## Slide 4: Our Research
- **The Numbers:** 8 qualitative interviews across 2 distinct groups (students + security/library staff); 2 silent observation visits at peak hours (12:45 PM & 5:00 PM).
- **Core Observation:** Friction and fear, not dishonesty, prevent item returns.

## Slide 5: The Key Insight & POV
- **Key Insight:** Students want to return items, but avoid doing so when it requires long administrative visits or exposing personal phone numbers to strangers.
- **POV Statement:** *Students need an authenticated, privacy-preserving recovery channel without exposing personal phone numbers because informal social media groups invite fraud and harassment.*

## Slide 6: Our Challenge (How Might We)
- **Main HMW:** *“How might we make returning a found item the effortless, natural choice on campus while ensuring only the verified rightful owner can claim it through trusted campus security?”*

## Slide 7: Ideation & Selection
- **32 Ideas Generated:** Brainstorming, Crazy 8s, and SCAMPER.
- **Screening Matrix:** Evaluated across Zero Cost (25%), Privacy (30%), Feasibility (25%), and Inclusivity (20%).
- **Winner:** ReturnLoop LPU Platform (5.0 / 5.0).
- **Rejected Idea:** Smart RFID Lockers (Rejected due to high capital hardware cost).

## Slide 8: The Prototype Evolution
- **Paper to Digital:** Began with rough 5-screen paper prototypes and storyboard testing; evolved into a high-fidelity responsive web application.
- **What it tested:** Can a student report and claim an item without any verbal explanation?

## Slide 9: User Testing Findings
- **Tested with 5 Real Users:** 3 students, 1 day scholar, and 1 campus security guard.
- **Key Findings:** Users loved the masked privacy; however, non-native English speakers struggled with technical terms, and iOS mobile users experienced modal clipping.

## Slide 10: What We Changed (Iterative Design)
- **Before:** English-only interface $\rightarrow$ **After:** Added 7 Indian languages (Hindi, Telugu, Punjabi, Tamil, Kannada, Malayalam, English).
- **Before:** Mobile header clipping on Safari $\rightarrow$ **After:** Migrated to React `createPortal` with iOS safe-area insets.
- **Before:** Static placeholder image $\rightarrow$ **After:** Smart category-driven image resolution.
- **Re-test:** 2 users re-tested; task completion time dropped by 62%.

## Slide 11: Final Solution & Live Demo
- **Live Demo Handover:** Showcasing Report Lost, Report Found, Automated Trait Matching, Hidden Identifier Claim, and Security Admin Desk.
- **Impact:** Recovery time reduced from 4 days to under 2 hours; 100% elimination of public phone leaks; ₹0 implementation cost.

## Slide 12: Honest Reflection & NABC Close
- **What Failed:** Early assumption that students would install a separate heavy native app (web prototype with responsive mobile portal proved far more effective).
- **Future Scope:** Campus smart locker integration and automated CCTV timeline cross-referencing.
- **NABC Close:** *“ReturnLoop transforms LPU’s 600-acre lost-and-found from a chaotic, privacy-leaking WhatsApp broadcast into a secure, zero-cost, verified campus recovery ecosystem.”*


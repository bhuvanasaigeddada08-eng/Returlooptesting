# User Testing Logs, Feedback Capture Matrix & Fixes

## 1. User Testing Session Logs (5 Users)

### Session 1: Participant T1 (Hosteller, 2nd Year CSE)
- **Task:** Report lost calculator in Block 36.
- **Observed Behavior:** Completed title and category easily, but paused at "Description" wondering if they should post their phone number.
- **Quote:** *"I am so used to WhatsApp where you have to put your phone number. It's a relief I don't have to put my number here."*
- **Outcome:** Success (Time: 1m 50s).

### Session 2: Participant T2 (Day Scholar, 3rd Year)
- **Task:** Search for found keys and check details.
- **Observed Behavior:** Browsed catalog smoothly; tapped on keys card; noticed secret marks were masked with *"Visible to Security Desk Only"*.
- **Quote:** *"This is smart. If anyone could see the key brand, anyone could claim it."*
- **Outcome:** Success (Time: 45s).

### Session 3: Participant T3 (International Student, BBA)
- **Task:** Switch language to Hindi and explore.
- **Observed Behavior:** Looked for language switch; found English pill in header; opened modal. On iPhone Chrome, noted that the top of the modal was slightly clipped by the browser bar.
- **Quote:** *"The language modal is slightly stuck under my top notch on iPhone."*
- **Outcome:** Identified High-Severity UI Bug.

### Session 4: Participant T4 (Finder, 2nd Year Biotech)
- **Task:** Report found water bottle.
- **Observed Behavior:** Did not have a photo taken on their laptop; hesitated whether form could be submitted without photo.
- **Quote:** *"Do I need to take a photo right now? What if my camera is broken?"*
- **Outcome:** Identified Need for Explicit Optional Photo Flag.

### Session 5: Participant T5 (Security Officer G.)
- **Task:** Review pending claim and approve handover.
- **Observed Behavior:** Viewed admin dashboard; compared student's secret mark against found item details; approved claim.
- **Quote:** *"This gives me proof so the other student cannot argue with me that I gave their item away."*
- **Outcome:** Success (Time: 35s).

---

## 2. Feedback Capture Matrix

```
┌──────────────────────────────────────┬──────────────────────────────────────┐
│ WHAT WORKED WELL (LIKES)             │ CONSTRUCTIVE CRITICISMS              │
│ • Masked privacy protection.         │ • Modal clipping on mobile iOS.      │
│ • Clear category and location badges.│ • Ambiguity over mandatory photos.   │
│ • Objective verification for guards. │ • English technical terminology      │
│                                      │   alienates non-native speakers.     │
├──────────────────────────────────────┼──────────────────────────────────────┤
│ QUESTIONS ASKED BY USERS             │ NEW IDEAS & SUGGESTIONS              │
│ • "How do I show proof at the gate?" │ • Add 7 Indian regional languages.   │
│ • "Will I get notified when a match  │ • Generate tracking reference codes  │
│   is found?"                         │   (e.g. RL-LOST-2026-XXXX).          │
│ • "Can I claim without a photo?"     │ • Smart fallback images for items.   │
└──────────────────────────────────────┴──────────────────────────────────────┘
```

---

## 3. Issue List & Iterative Fixes (Before vs. After)

| Issue # | Description | Severity | Fix Implemented | Re-Test Verification |
|:---:|---|:---:|---|---|
| **#1** | Language accessibility barrier | **High** | Added 7 Indian languages (Hindi, Punjabi, Telugu, Tamil, Kannada, Malayalam, English) with instant toggle. | Tester T1 verified Hindi navigation in 42 seconds. |
| **#2** | iOS WebKit header trapping | **High** | Replaced inline modal with React `createPortal` and safe-area insets (`env(safe-area-inset-top)`). | Tester T3 verified zero clipping on iPhone. |
| **#3** | Missing photo error | **Medium** | Implemented backend category-driven smart image resolution and sleek verified SVG placeholders. | All items display crisp visual previews. |
| **#4** | Gate handover verification | **Medium** | Added standardized tracking reference codes (`RL-LOST-2026-XXXXXX`) visible on cards and claim receipts. | Security guard approved claim in under 10 seconds. |


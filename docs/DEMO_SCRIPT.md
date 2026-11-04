# ReturnLoop LPU — Faculty Demonstration Script

This document provides a complete, step-by-step walkthrough script for presenting **ReturnLoop LPU** to evaluators, faculty mentors, and project review panels.

---

## 1. Demonstration Setup & Pre-Flight Checklist

### Test Environment
- **Laptop Host**: Windows 11
- **Backend**: Flask running on `http://127.0.0.1:5000` (Terminal 1)
- **Frontend**: Vite + React running on `http://localhost:5173` (Terminal 2)
- **Database**: SQLite (`backend/instance/returnloop.db`) pre-seeded with test data.

### Demonstration Credentials
| Role | Email | Password | Intended Screen |
|---|---|---|---|
| **Student (Reporting)** | `student@lpu.in` | `StudentPass123!` | Student Dashboard & Report Forms |
| **Student 2 (Claiming)** | `rohit.sharma@lpu.in` | `StudentPass123!` | Public Search & Claim Modal |
| **Administrator** | `admin@lpu.in` | `AdminPass123!` | Administrator Verification Desk |

---

## 2. Step-by-Step Demonstration Flow

### Scene 1: Introduction & Landing Page (2 minutes)
1. **Action**: Open browser to `http://localhost:5173/`.
2. **Key Talking Points**:
   - "Good morning, evaluators. This is ReturnLoop LPU, a decentralized, privacy-focused lost-and-found management platform built for Lovely Professional University."
   - "Every semester, hundreds of laptops, ID cards, wallets, and water bottles are misplaced in blocks 32, 34, and the Central Library. Unregulated WhatsApp groups lead to noise and privacy leaks."
   - "ReturnLoop LPU replaces chaotic chat groups with structured reporting, a transparent 5-trait similarity matching engine, and controlled administrative verification at ₹0 cost."
3. **Features to Highlight**:
   - Public search entry point without requiring login.
   - Category filter pills (Electronics, Identification, Bags, Apparel, Accessories, Other).
   - Live campus statistics counters.
   - Privacy-safe item preview cards (sensitive contact details are hidden).

---

### Scene 2: Student Login & Reporting a Lost Belonging (3 minutes)
1. **Action**: Click **"Sign In"** in the top navigation.
2. **Action**: Enter `student@lpu.in` / `StudentPass123!`. Click **"Log In"**.
3. **Action**: Explain the **Student Dashboard**:
   - Welcome banner with student display name.
   - Quick counters: My Lost Items (active count), My Found Items, Active Claims, Unread Alerts.
   - Quick action shortcuts: "Report Lost Item", "Report Found Item", "Browse All Items".
4. **Action**: Click **"Report Lost Item"** button.
5. **Action**: Fill the structured report form:
   - **Title**: `HP Pavilion Laptop Silver 15-inch`
   - **Category**: `Electronics`
   - **Location**: `Central Library 3rd Floor Reading Hall`
   - **Date Lost**: Select yesterday's date.
   - **Color**: `Silver`
   - **Brand**: `HP`
   - **Description**: `Left on table near the window next to pillar 4. Has a green sticker on the top corner.`
6. **Action**: Click **"Submit Report"**.
7. **Action**: Show instant toast notification: *"Lost item report created with reference RET-L-..."*.
8. **Action**: Navigate to **"My Items & Claims"** to show the report registered with status `Open`.

---

### Scene 3: Reporting a Found Item & Transparent 5-Trait Match Suggestion (3 minutes)
1. **Action**: Log out of the first student account.
2. **Action**: Log in as another student (`rohit.sharma@lpu.in` / `StudentPass123!`) or use the public found submission.
3. **Action**: Click **"Report Found Item"**.
4. **Action**: Fill the found item report:
   - **Title**: `Silver HP Laptop found on desk`
   - **Category**: `Electronics`
   - **Location**: `Central Library 3rd Floor`
   - **Date Found**: Select yesterday's date.
   - **Color**: `Silver`
   - **Brand**: `HP`
   - **Storage Location**: `Submitted to Block 32 Security Guard Room`
5. **Action**: Click **"Submit Report"**.
6. **Action**: Instantly open the newly created found item details page (`/items/<id>`).
7. **Action**: Point out the **"Potential Matches Detected"** section:
   - Show how the algorithm computed a similarity score (e.g., 90%+ match).
   - Explain the transparent weighting:
     * Category similarity: 35%
     * Keyword similarity: 25%
     * Color similarity: 15%
     * Location similarity: 15%
     * Date proximity: 10%
   - Emphasize to faculty: *"Notice we never claim verified ownership automatically. We simply flag potential alignment to avoid false claims."*

---

### Scene 4: Ownership Claim Submission (2 minutes)
1. **Action**: As the student claiming the item, click **"Claim This Item"**.
2. **Action**: Explain the verification form:
   - *"To prevent impostors from claiming expensive electronics, the student must provide private identifying proof that only the true owner would know."*
3. **Action**: Enter private proof:
   - **Claim Proof Description**: `Lock screen wallpaper is an anime character. Wallpaper password starts with 'Aarav2026'. Inside the laptop bag pocket is an LPU library card ending in 4421.`
4. **Action**: Click **"Submit Ownership Claim"**.
5. **Action**: Show the claim created with reference `CLM-...` and status `Submitted / Under Review`.

---

### Scene 5: Administrator Verification Desk & Physical Handover (3 minutes)
1. **Action**: Log out and log in as Administrator (`admin@lpu.in` / `AdminPass123!`).
2. **Action**: Explain the **Administrator Dashboard**:
   - Total campus reports, pending claims queue, resolved items count.
   - Real-time audit log stream.
3. **Action**: Click **"Pending Claims"** tab or navigate to `/admin/claims`.
4. **Action**: Locate the claim submitted in Scene 4.
5. **Action**: Click **"Review Claim"**:
   - View claimant identity, item reported, and private claimant proof description.
   - Show administrative options: **"Approve Claim"**, **"Request More Information"**, **"Reject Claim"**.
6. **Action**: Click **"Approve Claim"**:
   - The status transitions to `Approved (Awaiting Handover)`.
   - The claimant instantly receives an in-app notification instructing them to visit the designated security desk with their physical student ID.
7. **Action**: In the review dialog, click **"Confirm Physical Handover"**:
   - Enter handover verification note: `Student verified with University ID 12104523. Laptop unlocked successfully in presence of Security Officer.`
   - Click **"Complete Handover"**.
8. **Action**: Observe state updates:
   - Claim status becomes `Handover Completed`.
   - Item report status updates to `Recovered`.
   - All competing claims on that item are automatically resolved.
   - An immutable audit trail entry is logged in the `audit_logs` table.

---

### Scene 6: In-App Notifications & Audit Trail (2 minutes)
1. **Action**: Log back in as `student@lpu.in`.
2. **Action**: Click the **Bell Icon** in the navigation header.
3. **Action**: Show notifications:
   - "High-confidence potential match detected for your HP Laptop report"
   - "Your claim CLM-... has been approved! Please collect your item from Block 32 Security."
   - "Physical handover recorded. Item marked as recovered."
4. **Action**: Mark a notification as read and show the unread counter badge decrementing.

---

### Scene 7: Reliability, Privacy, & Persistence Verification (2 minutes)
1. **Action**: Explain backend persistence:
   - Close backend terminal (Ctrl + C), then restart it: `python run.py`.
   - Refresh the browser.
   - Show that all reports, claims, notifications, and audit records remain intact in `returnloop.db`.
2. **Action**: Summarize testing:
   - Show terminal with `pytest` passing all 28 automated tests.

---

## 3. Fallback Plan for Live Demos

| Contingency | Cause | Fallback Action |
|---|---|---|
| **Port conflict on 5000** | Lingering Flask process | Run `Get-Process python \| Stop-Process -Force` and restart `python run.py`. |
| **Port conflict on 5173** | Vite running in multiple tabs | Accept the alternative port (5174) or terminate node process. |
| **Accidental database deletion** | File cleared | Restore the pre-seeded snapshot from `backups/20261023_153844/returnloop.db`. |
| **Google Sign-In clicked** | User taps Google button | Explain the designed graceful fallback banner: *"Google Sign-In is intentionally unconfigured for ₹0 local privacy. Standard credentials work out of the box."* |

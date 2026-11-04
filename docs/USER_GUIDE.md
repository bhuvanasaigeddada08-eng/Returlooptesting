# ReturnLoop LPU - User Manual & Operating Guide

A comprehensive guide for students, faculty, and campus security administrators.

---

## 1. For Students

### A. Reporting a Lost Item
1. Sign in with your university account.
2. Click **Report Lost** in the top navigation bar.
3. Complete the form:
   - **Title**: Descriptive name (e.g. `HP Pavilion 15-inch Laptop`).
   - **Category**: Select the matching category.
   - **Color & Brand**: Precise color and manufacturer.
   - **Approximate Campus Location**: Select where you last remember having the item (e.g. `Central Library`, `Block 34`).
   - **Approximate Date**: When you noticed it missing.
   - **Private Verification Details**: Enter unique marks (scratches, wallpaper description, stickers). These details are hidden from the public.
4. Click **Submit Lost Report**. ReturnLoop will instantly search for existing found reports that match your item and notify you.

### B. Reporting a Found Item
1. Click **Report Found** in the top navigation bar.
2. Enter the item's title, category, color, location where discovered, and custody instructions (e.g. `Deposited with Block 34 Helpdesk`).
3. For sensitive items like student ID cards or room keys, do not publicly publish full registration numbers.

### C. Finding & Claiming Your Belonging
1. Browse reports on the **Explore Items** page or check suggested matches on your dashboard.
2. If you spot your item in the **Found Items** section, click **View Details**.
3. Click **Claim This Belonging**.
4. Describe your verifiable proof of ownership in detail (unlock patterns, screen wallpapers, secret engravings, purchase invoice details).
5. Submit the claim. Campus Security will verify your proof against the physical item.
6. Once approved, you will receive an in-app notification to visit the **Block 34 Security Office** with your Student ID card to collect your belonging.

---

## 2. For Campus Security Administrators

### A. Reviewing Pending Claims
1. Log in with your security administrator account (`admin@returnloop.lpu.in`).
2. Navigate to **Admin Portal > Claim Reviews** (`/admin/claims`).
3. Click **Inspect** to review the claimant's submitted proof alongside the found item details.
4. Choose an action:
   - **Approve Claim**: If the proof conclusively matches the item. The student receives directions to visit the helpdesk.
   - **Request Proof**: If clarification or additional evidence is needed.
   - **Reject Claim**: If the proof is incorrect or fraudulent (mandatory explanation required).

### B. Completing Physical Handover
1. When the student arrives at Block 34 Helpdesk, verify their physical Student ID card.
2. Under the approved claim in the Admin Portal, click **Record Verified Physical Handover**.
3. Enter your handover verification notes (student ID number, signature reference).
4. Submit. The system will mark the claim as `handover_completed`, change the item report status to `recovered`, and log an immutable audit entry.

### C. Moderating Content
1. Navigate to **Admin Portal > Item Moderation** (`/admin/items`).
2. If an item contains inappropriate text, spam, or sensitive student data:
   - Click **Moderate Status**.
   - Select `Suspended` and record a reason.
   - The item will be hidden from public exploration immediately.

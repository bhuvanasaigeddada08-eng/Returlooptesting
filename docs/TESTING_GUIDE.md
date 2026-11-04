# ReturnLoop LPU - Testing Guide & Automated Test Report

## 1. Overview
The ReturnLoop LPU test suite consists of automated integration and unit tests covering authentication, route authorization, report creation, privacy safeguards, the transparent matching algorithm, claim workflows, duplicate protection, administrative moderation, and handover completion.

Testing framework: **Pytest** with Flask's test client and in-memory SQLite database.

---

## 2. Running Automated Tests

Run all tests from the repository root:
```powershell
.\backend_venv\Scripts\pytest.exe backend\tests -v
```

To run a specific test module:
```powershell
.\backend_venv\Scripts\pytest.exe backend\tests\test_matching.py -v
```

---

## 3. Automated Test Suite Results

All **24 tests** execute and pass cleanly:

| Test Identifier | Category | Status | Verified Functionality |
|---|---|---|---|
| `test_register_student_success` | Auth | PASSED | Student account creation with password hashing and JWT token issuance |
| `test_register_duplicate_email` | Auth | PASSED | Prevents duplicate registration with existing institutional email (409) |
| `test_register_weak_password` | Auth | PASSED | Rejects passwords under 8 characters or lacking letters/numbers (400) |
| `test_login_success` | Auth | PASSED | Validates credentials and returns bearer token and user profile |
| `test_login_invalid_password` | Auth | PASSED | Rejects invalid password attempt with generic secure message (401) |
| `test_protected_route_unauthenticated` | Auth | PASSED | Blocks unauthenticated request to protected endpoint (401) |
| `test_protected_route_authenticated` | Auth | PASSED | Authenticates valid bearer token and injects current user |
| `test_change_password` | Auth | PASSED | Updates user password, verifies old password, and clears initial change flag |
| `test_unauthorized_student_access_admin_route` | Auth | PASSED | Role-based protection: rejects regular students accessing `/api/admin/*` (403) |
| `test_create_report_success` | Reports | PASSED | Generates lost report with unique reference code (RL-LOST-YYYY-XXXX) |
| `test_create_report_validation_errors` | Reports | PASSED | Validates title, category, color, location, and date bounds |
| `test_privacy_safe_public_view` | Reports | PASSED | **Privacy Safeguard**: Hides private identifying details and email from public |
| `test_report_editing_permissions` | Reports | PASSED | Only report owner or administrator can edit report metadata (403 on others) |
| `test_invalid_image_upload_rejected` | Reports | PASSED | Rejects non-image binaries and unauthorized file extensions |
| `test_matching_algorithm_high_match` | Matching | PASSED | Algorithmic scoring produces 75%+ score for matching category, location, date |
| `test_matching_different_categories` | Matching | PASSED | Verifies 0% category score when items belong to different categories |
| `test_submit_claim_success` | Claims | PASSED | Student submits private ownership explanation against found report |
| `test_cannot_claim_own_reported_item` | Claims | PASSED | Business rule: users cannot submit a claim for an item they reported finding |
| `test_prevent_duplicate_claims` | Claims | PASSED | Prevents duplicate active claims by the same user for the same item (409) |
| `test_unauthorized_user_cannot_read_private_claim` | Claims | PASSED | **Confidentiality**: Third-party students cannot read private claim proof (403) |
| `test_admin_dashboard_metrics` | Admin | PASSED | Real-time database aggregations (active lost, active found, pending claims) |
| `test_admin_claim_approval_workflow` | Admin | PASSED | Administrator reviews and approves claim with justification |
| `test_admin_claim_rejection_requires_reason` | Admin | PASSED | Enforces mandatory administrative justification when rejecting claims |
| `test_admin_suspends_item_report` | Admin | PASSED | Administrator moderates and suspends inappropriate/spam report |

---

## 4. Manual Acceptance Testing Checklist

1. **Guest Browsing**: Open landing page without signing in, search for "HP", filter by "Electronics".
2. **Student Flow**:
   - Register or sign in as `aarav.sharma@lpu.in` (password: `StudentPass123!`).
   - Report a lost item at Central Library.
   - Inspect suggestions under "Potential Matches" with score breakdown.
   - Submit an ownership claim for a found item with private proof.
3. **Administrator Flow**:
   - Sign in as `admin@returnloop.lpu.in` (password: `AdminPass123!`).
   - Open `/admin` to verify live campus metrics and category distribution.
   - Go to `/admin/claims` to view submitted private proof.
   - Approve claim and click "Record Verified Physical Handover" with student verification notes.
   - Go to `/admin/audit-logs` to inspect the generated immutable audit trail.

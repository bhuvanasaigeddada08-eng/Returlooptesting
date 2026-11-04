# ReturnLoop LPU - RESTful API Documentation

ReturnLoop LPU exposes a REST API powered by Python, Flask, SQLAlchemy, and Flask-CORS. All endpoints return JSON payloads with appropriate HTTP status codes.

---

## 1. Authentication & Session Management

All authenticated endpoints require an `Authorization` header formatted as:
`Authorization: Bearer <signed_token>`

### `POST /api/auth/register`
Creates a new student account.
- **Access**: Public
- **Request Body**:
  ```json
  {
    "display_name": "Aarav Sharma",
    "email": "aarav.sharma@lpu.in",
    "phone": "9876543210",
    "password": "SecurePassword123"
  }
  ```
- **Responses**:
  - `201 Created`: Returns user object and bearer session token.
  - `400 Bad Request`: Validation failure.
  - `409 Conflict`: Email already exists.

### `POST /api/auth/login`
Authenticates a user and issues a signed token.
- **Access**: Public
- **Request Body**:
  ```json
  {
    "email": "aarav.sharma@lpu.in",
    "password": "StudentPass123!"
  }
  ```
- **Responses**:
  - `200 OK`: Returns user profile and token.
  - `401 Unauthorized`: Invalid credentials.

### `GET /api/auth/me`
Retrieves current profile and notification preferences.
- **Access**: Authenticated

### `POST /api/auth/change-password`
Changes current user password and clears `must_change_password` flag.
- **Access**: Authenticated
- **Request Body**:
  ```json
  {
    "current_password": "OldPassword123!",
    "new_password": "NewPassword123!"
  }
  ```

---

## 2. Reports Management

### `GET /api/reports`
Lists campus reports with pagination, keyword search, and filters.
- **Access**: Public (Privacy-safe: contact details & secret proof omitted)
- **Query Parameters**:
  - `q` (string): Keyword search on title, description, color, brand, reference code.
  - `type` (string): `lost` or `found`.
  - `category` (string): Category name.
  - `location` (string): Campus building or location.
  - `sort` (string): `newest` or `oldest`.
  - `page` (int): Page number (default: 1).
  - `per_page` (int): Items per page (default: 12).

### `POST /api/reports`
Publishes a new lost or found item report.
- **Access**: Authenticated Student or Admin
- **Request Body**:
  ```json
  {
    "report_type": "lost",
    "title": "HP Pavilion 15-inch Laptop",
    "category": "Electronics",
    "description": "Left near study desk section B in Central Library.",
    "color": "Blue",
    "brand": "HP",
    "general_location": "Central Library",
    "event_date": "2026-10-21",
    "identifying_characteristics": "Scratch near power button, sticker of Tux Linux."
  }
  ```

### `GET /api/reports/<id>`
Retrieves single item report. Owners and administrators receive full private fields.

### `PATCH /api/reports/<id>`
Updates an existing report. Must be owner or admin.

### `POST /api/reports/<id>/recover`
Marks a lost report as recovered. Must be owner or admin.

### `POST /api/reports/<id>/withdraw`
Withdraws report from active listings. Must be owner or admin.

### `POST /api/reports/<id>/images`
Uploads a validated image (PNG, JPG, WEBP, max 5MB). File magic bytes are checked.

---

## 3. Algorithmic Transparent Matching

### `GET /api/matches/<report_id>`
Calculates potential matches between the target item and opposite reports (lost ↔ found).
- **Access**: Public / Authenticated
- **Algorithm Weights**:
  - Category Match: 35%
  - Keyword Overlap: 25%
  - Color Match: 15%
  - Campus Location Proximity: 15%
  - Date Proximity: 10%
- **Response**:
  ```json
  {
    "matches": [
      {
        "item": { ... },
        "match_score": 85.0,
        "breakdown": {
          "category": { "score": 35.0, "detail": "Exact category match (Electronics)" },
          "keywords": { "score": 15.0, "detail": "3 matching keywords: hp, pavilion, laptop" },
          "color": { "score": 15.0, "detail": "Identical color reported (Blue)" },
          "location": { "score": 15.0, "detail": "Exact campus location match (Central Library)" },
          "date": { "score": 5.0, "detail": "Dates are within 1 week" }
        },
        "disclaimer": "This score is an algorithmic heuristic suggestion..."
      }
    ]
  }
  ```

---

## 4. Ownership Claims

### `POST /api/claims/<report_id>`
Submits an ownership claim against a found report.
- **Access**: Authenticated (Cannot claim own report; duplicate active claims blocked)
- **Request Body**:
  ```json
  {
    "private_ownership_explanation": "Lock pattern is a Z shape, wallpaper is cosmic nebula, bill attached."
  }
  ```

### `GET /api/claims/my`
Retrieves claims submitted by current student.

### `GET /api/claims/<id>`
Retrieves details of a claim. Claimant and administrators only.

### `POST /api/claims/<id>/withdraw`
Withdraws a pending claim.

---

## 5. In-App Notifications

### `GET /api/notifications`
Returns in-app notifications with unread count.

### `POST /api/notifications/<id>/read`
Marks single notification as read.

### `POST /api/notifications/read-all`
Marks all user notifications as read.

---

## 6. Administrator & Security Workflows

All endpoints require `admin` role authorization.

### `GET /api/admin/dashboard`
Returns live metrics, category breakdown, recent reports, claims, and audit logs.

### `GET /api/admin/reports`
Filters and inspects all reports (including suspended and withdrawn).

### `PATCH /api/admin/reports/<id>/status`
Moderates report status (`active`, `claim_pending`, `recovered`, `withdrawn`, `suspended`) with logged reason.

### `GET /api/admin/claims`
Lists all claims across the campus.

### `POST /api/admin/claims/<id>/approve`
Approves claim with verification reason. Notifies student to visit Block 34 Helpdesk.

### `POST /api/admin/claims/<id>/reject`
Rejects claim with mandatory reason. Logs audit event and notifies student.

### `POST /api/admin/claims/<id>/request-information`
Requests additional proof from claimant with instructions.

### `POST /api/admin/claims/<id>/handover`
Records physical handover: verifies Student ID, logs responsible administrator, marks item report as `recovered`, and completes the case.

### `GET /api/admin/audit-logs`
Paginated audit log records tracking all administrative and security actions.

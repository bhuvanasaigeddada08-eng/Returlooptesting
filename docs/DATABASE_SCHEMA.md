# ReturnLoop LPU - Database Architecture & Schema

ReturnLoop LPU utilizes a normalized relational schema modeled in SQLAlchemy. For local development and demonstrations, it runs on SQLite (`instance/returnloop.db`), designed for migration to PostgreSQL.

---

## Entity Relationship Overview

```mermaid
erDiagram
    User ||--o{ ItemReport : "reports"
    User ||--o{ Claim : "claimant"
    User ||--o{ Notification : "receives"
    User ||--o{ AuditLog : "initiates"
    ItemReport ||--o{ ItemImage : "has"
    ItemReport ||--o{ Claim : "receives"

    User {
        int id PK
        string email UK
        string display_name
        string phone
        string password_hash
        string role "student | admin"
        boolean is_active
        boolean must_change_password
        text notification_preferences
        datetime created_at
        datetime updated_at
    }

    ItemReport {
        int id PK
        string reference_code UK "e.g. RL-LOST-2026-A1B2"
        int user_id FK
        string report_type "lost | found"
        string title
        string category
        text description
        string color
        string brand
        string general_location "e.g. Central Library"
        string event_date
        text identifying_characteristics "Private"
        text safe_handover_instructions
        string status "active | claim_pending | recovered | withdrawn | suspended"
        datetime created_at
        datetime updated_at
    }

    ItemImage {
        int id PK
        int item_report_id FK
        string file_path
        string file_name
        boolean is_primary
        datetime created_at
    }

    Claim {
        int id PK
        string reference_code UK "e.g. CLM-2026-A1B2C3"
        int item_report_id FK
        int claimant_user_id FK
        text private_ownership_explanation "Confidential Proof"
        string status "pending | approved | rejected | more_info_needed | handover_completed"
        text administrator_reason
        int reviewed_by_id FK
        datetime reviewed_at
        datetime handover_at
        int handover_admin_id FK
        text handover_notes
        datetime created_at
        datetime updated_at
    }

    Notification {
        int id PK
        int user_id FK
        string title
        text message
        string notification_type "match | claim_update | admin_message | handover"
        string link
        boolean is_read
        datetime created_at
    }

    AuditLog {
        int id PK
        int actor_user_id FK
        string action
        string target_type
        int target_id
        text details "JSON String"
        string ip_address
        datetime created_at
    }
```

---

## Detailed Table Specifications

### 1. `users`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | Primary Key, Auto Increment | Unique internal identifier |
| `email` | String(120) | Unique, Not Null, Index | Institutional university email address |
| `display_name` | String(100) | Not Null | Student or Staff display name |
| `phone` | String(25) | Nullable | Optional contact number (private) |
| `password_hash` | String(255) | Not Null | Werkzeug-generated pbkdf2:sha256 hash |
| `role` | String(20) | Default 'student', Not Null | `student` or `admin` |
| `is_active` | Boolean | Default True, Not Null | Account active status flag |
| `must_change_password` | Boolean | Default False, Not Null | Enforces initial password update on seeded admin |
| `notification_preferences` | Text | Default JSON | User preference flags for alerts |
| `created_at` | DateTime | Default UTC now | Registration timestamp |
| `updated_at` | DateTime | Auto-updated UTC now | Modification timestamp |

### 2. `item_reports`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | Primary Key, Auto Increment | Unique internal identifier |
| `reference_code` | String(30) | Unique, Not Null, Index | Public tracking identifier (e.g. `RL-LOST-2026-3F8A`) |
| `user_id` | Integer | Foreign Key (`users.id`), On Delete Cascade | Reporter user ID |
| `report_type` | String(10) | Not Null, Index | `lost` or `found` |
| `title` | String(150) | Not Null, Index | Item name / headline |
| `category` | String(50) | Not Null, Index | Category (Electronics, ID & Cards, etc.) |
| `description` | Text | Not Null | Public description of appearance and context |
| `color` | String(50) | Not Null, Index | Primary color trait for matching |
| `brand` | String(80) | Nullable | Brand or manufacturer name |
| `general_location` | String(100) | Not Null, Index | LPU campus location (e.g. Block 34, Central Library) |
| `event_date` | String(20) | Not Null | ISO YYYY-MM-DD date when lost or found |
| `identifying_characteristics` | Text | Nullable | Confidential verification notes (Owner & Admin only) |
| `safe_handover_instructions` | Text | Nullable | Custody location and safe recovery guidance |
| `status` | String(20) | Default 'active', Index | `active`, `claim_pending`, `recovered`, `withdrawn`, `suspended` |

### 3. `claims`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | Primary Key | Unique internal claim ID |
| `reference_code` | String(30) | Unique, Index | Case tracking number (e.g. `CLM-2026-9E4B`) |
| `item_report_id` | Integer | Foreign Key (`item_reports.id`) | Target found item |
| `claimant_user_id` | Integer | Foreign Key (`users.id`) | Claimant student ID |
| `private_ownership_explanation` | Text | Not Null | Confidential proof submitted by student |
| `status` | String(25) | Default 'pending', Index | `pending`, `approved`, `rejected`, `more_info_needed`, `handover_completed` |
| `administrator_reason` | Text | Nullable | Administrator verification or rejection justification |
| `reviewed_by_id` | Integer | Foreign Key (`users.id`), Nullable | Verifying administrator user ID |
| `handover_at` | DateTime | Nullable | Timestamp of in-person handover |
| `handover_admin_id` | Integer | Foreign Key (`users.id`), Nullable | Admin who verified ID and gave item |
| `handover_notes` | Text | Nullable | Student ID verified, logbook signatures |

---

## State Transition Rules

```mermaid
stateDiagram-v2
    [*] --> Active : Report Created
    Active --> ClaimPending : Student Files Claim
    ClaimPending --> Active : Claim Rejected / Withdrawn
    ClaimPending --> HandoverCompleted : Admin Verified & Handover Recorded
    Active --> Recovered : Owner Marks Recovered
    Active --> Withdrawn : Owner Withdrawn
    Active --> Suspended : Admin Moderation
    Suspended --> Active : Admin Reactivated
    HandoverCompleted --> [*]
    Recovered --> [*]
    Withdrawn --> [*]
```

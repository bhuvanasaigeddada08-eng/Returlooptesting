# ReturnLoop LPU

> **Centralized University Lost-and-Found Management System with Android APK Readiness**  
> *Developed for Lovely Professional University campus community (Student Prototype)*

---

## 1. Problem Statement

Students and faculty frequently misplace belongings across sprawling university campuses—such as laptops at the Central Library, student ID cards at food courts, keys along hostel pathways, or water flasks in auditoriums. Without a centralized digital registry, lost items often languish indefinitely at security desks, students post fragmented messages across social media groups, and campus staff struggle to verify genuine ownership while avoiding fraudulent claims.

**ReturnLoop LPU** solves this problem by providing:
1. A centralized registry for reporting both lost belongings and discovered items.
2. An algorithmic, transparent matching engine that automatically detects potential matches between lost and found items.
3. A confidential claim submission workflow where students provide verifiable ownership proof visible only to authorized security officers.
4. An auditable administrator handover system that verifies student ID credentials and records official physical returns.
5. Android APK readiness via Capacitor for deployment to student mobile devices.

> [!NOTE]  
> **Prototype Notice**: ReturnLoop LPU is an independent student prototype developed for academic and campus recovery demonstration. It is not an officially endorsed or university-integrated LPU service.

---

## 2. Technology Stack

- **Frontend**:
  - React 19 + Vite 8
  - Tailwind CSS 3.4 (custom navy/slate palette with university branding)
  - Lucide React icons
  - React Router DOM 7
  - Capacitor Core & CLI (`@capacitor/core`, `@capacitor/cli`, `@capacitor/android`)
- **Backend**:
  - Python 3.10+
  - Flask 3.1 & Flask REST API
  - Flask-SQLAlchemy 3.1 & SQLAlchemy 2.0 ORM
  - Flask-CORS with strict origin whitelisting
  - Werkzeug Security password hashing (`pbkdf2:sha256`)
  - ItsDangerous cryptographically signed timed bearer tokens
- **Database**:
  - SQLite (default for development: `backend/instance/returnloop.db`)
  - SQLAlchemy models fully compatible with PostgreSQL migration
- **Testing**:
  - Pytest 9.1 with in-memory SQLite fixtures (28 passing unit & integration tests)

---

## 3. Project Directory Structure

```
ReturnLoop/
├── backend/
│   ├── app/
│   │   ├── models/          # User, ItemReport, ItemImage, Claim, Notification, AuditLog
│   │   ├── routes/          # auth, reports, matches, claims, notifications, admin
│   │   ├── services/        # match_service, notification_service, audit_service
│   │   └── utils/           # auth_middleware, file_upload, validators
│   ├── instance/            # SQLite development database (returnloop.db)
│   ├── tests/               # 28 Pytest automated test suites (100% passing)
│   ├── config.py            # Environment-driven configuration
│   ├── requirements.txt     # Python backend dependencies
│   ├── run.py               # Application entrypoint & dev admin auto-provisioning
│   └── seed_data.py         # Realistic synthetic LPU campus seed data
├── frontend/
│   ├── android/             # Complete native Android Gradle project (Capacitor)
│   ├── src/
│   │   ├── components/      # Navbar, Footer, ItemCard, MatchCard, StatusBadge, etc.
│   │   ├── context/         # AuthContext
│   │   ├── layouts/         # MainLayout, AdminLayout
│   │   ├── pages/           # Landing, Explore, Details, Claim, Dashboard, Admin, etc.
│   │   ├── services/        # Centralized api.js client
│   │   └── utils/           # constants.js (Categories, Locations, API URL)
│   ├── capacitor.config.json # Capacitor configuration (appId: com.returnloop.lpu)
│   ├── package.json
│   ├── tailwind.config.js
│   └── vite.config.js
├── docs/
│   ├── INSTALLATION.md      # Complete step-by-step Windows setup guide
│   ├── PROJECT_AUDIT.md     # Comprehensive architectural and security audit
│   ├── KNOWN_LIMITATIONS.md # Technical boundaries, ₹0 stack, and research disclosures
│   ├── DEMO_SCRIPT.md       # 7-scene presentation and faculty demo walkthrough
│   ├── COLLEGE_PROJECT_REPORT.md # Academic Design Thinking project report
│   ├── PRESENTATION_SLIDES.md # 14-slide academic review deck
│   ├── VIVA_QUESTIONS.md    # Comprehensive faculty viva voce preparation guide
│   ├── API_DOCUMENTATION.md # Detailed REST API endpoint specification
│   ├── DATABASE_SCHEMA.md   # Schema tables, ER diagram, and state machine
│   ├── ANDROID_BUILD_GUIDE.md # Android Studio and APK packaging guide
│   ├── TESTING_GUIDE.md     # Test suite breakdown and verification matrix
│   └── USER_GUIDE.md        # Student and Administrator user guide
├── backups/                 # Database snapshots and timestamped backups
├── .env.example
├── .gitignore
└── README.md
```

---

## 4. Quick Start & Installation

### Prerequisites
- Python 3.10+
- Node.js v18+ & npm v9+

### Backend Setup
1. Open terminal and navigate to the project root:
   ```powershell
   # Create and activate Python virtual environment
   python -m venv backend_venv
   .\backend_venv\Scripts\Activate.ps1

   # Install dependencies
   pip install -r backend/requirements.txt
   ```

2. Seed synthetic demonstration data:
   ```powershell
   python backend/seed_data.py
   ```

3. Start the Flask Backend Server:
   ```powershell
   python backend/run.py
   ```
   *The backend will be running on `http://127.0.0.1:5000`.*

### Frontend Setup
1. In a separate terminal, navigate to `frontend`:
   ```powershell
   cd frontend
   npm install
   ```

2. Start the Vite React Development Server:
   ```powershell
   npm run dev
   ```
   *The web application will open at `http://localhost:5173`.*

---

## 5. Demonstration Accounts

The database comes pre-seeded with realistic synthetic LPU campus data and demo accounts:

| Role | Email | Password | Access |
|---|---|---|---|
| **Campus Security Admin** | `admin@returnloop.lpu.in` | `AdminPass123!` | Full Admin Portal (`/admin`), claim moderation, handover logs |
| **Student (Demo 1)** | `aarav.sharma@lpu.in` | `StudentPass123!` | Student Dashboard, lost HP laptop report, pending claim |
| **Student (Demo 2)** | `priya.patel@lpu.in` | `StudentPass123!` | Found items, bike keys report |

> **Convenience Feature**: The login page (`/login`) includes **"Fill Student Demo"** and **"Fill Admin Demo"** buttons for one-click evaluation without typing credentials manually.

---

## 6. Running Automated Tests

Run the full Pytest test suite:
```powershell
.\backend_venv\Scripts\pytest.exe backend\tests -v
```
All **28 tests** will run against in-memory SQLite and validate:
- Student registration, password complexity, and duplicate email prevention.
- Role-based authorization (blocking students from administrator endpoints).
- Privacy-safe item serialization (hiding sensitive fields from the public).
- Transparent matching algorithm weights (category 35%, keywords 25%, color 15%, location 15%, date 10%).
- Claim submission, duplicate claim blocking, and private proof confidentiality.
- Administrative claim review, rejection justifications, and physical handover logging.
- Image header magic byte checks and executable file rejection.

---

## 7. Android APK Readiness (Capacitor)

The frontend is fully configured with Capacitor to generate native Android APKs:
- **Application ID**: `com.returnloop.lpu`
- **Application Name**: `ReturnLoop LPU`
- **Pre-generated Native Project**: Located in `frontend/android/`

### To build the APK in Android Studio:
1. Build the production React web bundle:
   ```bash
   cd frontend
   npm run build
   npx cap sync android
   ```
2. Open the `frontend/android` folder in **Android Studio**.
3. Select **Build > Build Bundle(s) / APK(s) > Build APK(s)** or click **Run (▶)** to test directly on your connected Android phone.
4. Output debug APK location:
   ```
   frontend/android/app/build/outputs/apk/debug/app-debug.apk
   ```

> For comprehensive details on configuring physical device LAN communication, firewall rules, and signed release APKs, see [docs/ANDROID_BUILD_GUIDE.md](docs/ANDROID_BUILD_GUIDE.md).

---

## 8. Security & Privacy Safeguards

- **No Plaintext Passwords**: Hashed via Werkzeug's PBKDF2 with SHA-256 and unique per-user salts.
- **Privacy-First Data Exposure**: Reporter email, phone numbers, and identifying marks are stripped from public responses and visible only to the owner and authenticated administrators.
- **Confidential Claims**: Claim ownership explanations (passwords, serial fragments, unique stickers) are never displayed publicly.
- **Tamper-Proof Audit Logging**: Administrative moderation actions, status transitions, and physical handovers write immutable audit log records.
- **Strict File Upload Validation**: Validates file extensions, size limits (5MB max), and inspects file header magic bytes (PNG, JPEG, WEBP) to prevent disguised executable uploads.

---

## 9. Cloud Deployment & Academic Documentation Index

| Document | Purpose |
| :--- | :--- |
| [docs/FREE_DEPLOYMENT_GUIDE.md](docs/FREE_DEPLOYMENT_GUIDE.md) | Complete ₹0 step-by-step deployment to Netlify + Render |
| [docs/PRODUCTION_ENVIRONMENT.md](docs/PRODUCTION_ENVIRONMENT.md) | Production environment variables and secrets specification |
| [docs/DATABASE_MIGRATION_GUIDE.md](docs/DATABASE_MIGRATION_GUIDE.md) | PostgreSQL migration guide & verification instructions |
| [docs/FREE_TIER_LIMITATIONS.md](docs/FREE_TIER_LIMITATIONS.md) | Two-month free-tier quotas, cold starts, and zero-charge guarantee |
| [docs/BACKUP_RESTORE_GUIDE.md](docs/BACKUP_RESTORE_GUIDE.md) | Automated JSON database export & demo data purging |
| [docs/DEPLOYMENT_TEST_REPORT.md](docs/DEPLOYMENT_TEST_REPORT.md) | 28/28 passing test audit and architectural verification |
| [docs/COLLEGE_PROJECT_REPORT.md](docs/COLLEGE_PROJECT_REPORT.md) | Stanford d.school Design Thinking academic report |
| [docs/PRESENTATION_SLIDES.md](docs/PRESENTATION_SLIDES.md) | 14-slide faculty evaluation presentation |
| [docs/VIVA_QUESTIONS.md](docs/VIVA_QUESTIONS.md) | Comprehensive evaluator Q&A defense preparation |


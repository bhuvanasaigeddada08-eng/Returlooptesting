# ReturnLoop LPU — Known Technical Limitations & Environment Boundaries

This document provides a transparent, truthful assessment of the technical boundaries, architectural trade-offs, and deliberate design decisions in **ReturnLoop LPU**. It is prepared for academic evaluation and faculty review.

---

## 1. Architectural & Cost Limitations

### 1.1 Localhost & Zero-Cost Architecture (₹0 Stack)
- **Constraint**: The system is designed to run locally on a student's Windows workstation without mandatory paid cloud subscriptions (AWS, GCP, Vercel, Firebase, Render, Supabase).
- **Trade-off**: The platform relies on the host workstation running the backend. If the host machine is powered off, the API is unavailable to clients.
- **Production Path**: In a real university deployment, the Flask backend and SQLite database would be deployed behind Nginx or Gunicorn on an internal university Linux server (e.g., Ubuntu Server on campus intranet) or a cost-effective cloud instance.

### 1.2 Database Concurrency (SQLite)
- **Constraint**: SQLite is chosen as the default zero-configuration database.
- **Trade-off**: SQLite handles typical college-scale concurrency (hundreds of simultaneous reads using Write-Ahead Logging `WAL` mode), but high-frequency concurrent write spikes across thousands of simultaneous users can encounter file lock contention.
- **Production Path**: For campus-wide scale (>10,000 active students), the SQLAlchemy configuration can seamlessly migrate to PostgreSQL by updating `DATABASE_URL` in `backend/config.py` without rewriting application code.

### 1.3 Local Image Storage
- **Constraint**: Uploaded item photographs are stored in the local filesystem under `backend/uploads/`.
- **Trade-off**: Images are served directly via Flask. While local development is instantaneous, horizontal backend scaling would require shared networked storage or S3-compatible object storage (e.g., MinIO or AWS S3).

---

## 2. Authentication & Third-Party Integrations

### 2.1 Google Sign-In Configuration
- **Constraint**: Google OAuth 2.0 requires registering an OAuth Client ID in Google Cloud Console with authorized origins (`http://localhost:5173`).
- **Behavior When Unconfigured**: ReturnLoop LPU honestly returns `{ "enabled": false, "client_id": null }` from `/api/auth/google/config`. The frontend displays an informative banner and seamlessly falls back to standard email/password authentication.
- **Security Rule**: The prototype never fabricates or simulates a fake Google login. When configured, Google ID tokens are verified cryptographically via Google's tokeninfo endpoint, checking audience (`aud`) and issuer (`iss`).

### 2.2 Email Notifications & SMTP
- **Constraint**: University SMTP relays or services like SendGrid/Gmail App Passwords require external credentials.
- **Behavior When Unconfigured**: The system operates in safe test mode (`TEST_MODE=True`). Outgoing notification emails are logged in memory and recorded in application logs without attempting delivery or throwing errors.
- **Critical Guarantee**: Failure to deliver an email *never* causes an in-app notification to fail. In-app notifications persist reliably in SQLite regardless of SMTP status.

---

## 3. Mobile & Android Networking Limitations

### 3.1 The `localhost` Loopback Boundary
- **Constraint**: When running inside an Android APK (emulator or physical phone), `localhost` or `127.0.0.1` refers to the Android device itself, **not** the developer laptop.
- **Behavior**: To connect an Android device running the APK to the laptop backend, the laptop's local LAN IP (e.g., `http://192.168.1.x:5000`) must be specified in `VITE_API_BASE_URL` prior to `npm run build` and `npx cap sync android`.
- **Offline Mode**: The current mobile prototype requires connectivity to the backend API; offline offline-first synchronization (e.g., WatermelonDB or Couchbase Lite) is designated for future phases.

### 3.2 Android Gradle Tooling Prerequisites
- **Constraint**: Compiling the native Android APK from the command line requires:
  1. OpenJDK 17 or 21 (available via Android Studio JBR: `C:\Program Files\Android\Android Studio\jbr`).
  2. Android SDK Command-line Tools and Platform Tools (located at `C:\Users\bhuva\AppData\Local\Android\Sdk`).
  3. Compatible Gradle distribution (Gradle 8.13+ required by Android Gradle Plugin 8.13.0).
- **Fallback**: The project is structured so that developers can simply open `frontend/android` in Android Studio and click **Run (▶)**, allowing Android Studio's IDE to automatically manage Gradle execution and device deployment.

---

## 4. Matching Algorithm & Governance Boundaries

### 4.1 Probabilistic Matching vs. Ownership Proof
- **Constraint**: The 5-trait matching algorithm (Category 35%, Keywords 25%, Color 15%, Location 15%, Date 10%) outputs a similarity score from 0% to 100%.
- **Governance**: A 95% match score does **not** grant automatic item handover. ReturnLoop LPU enforces a strict human-in-the-loop governance model:
  1. Student must submit a claim with hidden identifying marks or proof.
  2. University administrator must review and approve the claim.
  3. Physical handover is conducted and signed off by the administrator.

### 4.2 University Affiliation Disclaimer
- **Status**: ReturnLoop LPU is a student-engineered prototype developed for academic and design-thinking coursework.
- **Clarification**: It is not officially endorsed by, integrated into, or operated by Lovely Professional University IT administration. No official campus enterprise systems (e.g., University Management System / UMS) are accessed or modified.

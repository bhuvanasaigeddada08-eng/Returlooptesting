# ReturnLoop LPU — Comprehensive Faculty Viva Voce Q&A Guide

This guide prepares the student developer to answer technical, architectural, security, design thinking, and mobile packaging questions during project evaluation and viva voce examinations.

---

## 1. Design Thinking & Product Strategy Questions

### Q1: Why did you choose the Design Thinking approach instead of jump-starting standard software development?
**Answer:**
Design Thinking prioritizes deep stakeholder empathy over premature assumptions. If we had simply built a standard CRUD website, we would have likely repeated the mistakes of campus chat groups—focusing only on posting messages. Through the **Empathize** and **Define** stages, we uncovered that the primary bottleneck in lost property recovery is not simply broadcasting lost items, but **ownership verification and fraud prevention**. Students fear posting private details publicly, and campus security staff struggle to verify genuine owners among multiple claimants. Design Thinking led directly to our two key innovations: the **hidden claim proof mechanism** and the **administrative verification desk**.

### Q2: How did you define your target personas?
**Answer:**
We modeled three distinct personas:
1. *The Distressed Loser* (e.g., student who lost a laptop during exam week and needs quick recovery without privacy exposure).
2. *The Honest Finder* (e.g., student who found items in an academic block and wants a friction-free way to log them without being spammed).
3. *The Campus Security / Administrative Officer* (e.g., staff member managing physical custody boxes and needing an indisputable audit trail of handovers).

### Q3: What research is already completed, and what is planned next?
**Answer:**
We have completed problem identification, heuristic analysis of existing campus chat channels, persona mapping, architectural ideation, prototype implementation, and automated test verification. For academic integrity, we have explicitly documented that large-scale quantitative field surveys (50+ students) and recorded physical security desk interviews constitute the next empirical milestone.

---

## 2. Architecture & Technology Stack Questions

### Q4: Why did you choose Flask and SQLite instead of a cloud database like MongoDB Atlas or Firebase?
**Answer:**
Our design constraint was a strict **₹0 budget** that works completely offline on a student's Windows laptop without paid subscriptions or external network dependencies.
- **SQLite** is zero-configuration, requires no background database daemon, and provides atomic ACID transactions. With Write-Ahead Logging (`WAL` mode) enabled, it easily supports the concurrent read loads typical of a university campus.
- **Flask with SQLAlchemy 2.0 ORM** provides a clean, maintainable RESTful API with parameterized queries that completely eliminate SQL injection vulnerabilities.
- If the university ever decides to deploy campus-wide for 50,000 students, the SQLAlchemy database URI in `config.py` can be switched to PostgreSQL without changing any application business logic.

### Q5: How do the frontend and backend communicate?
**Answer:**
They are strictly decoupled:
- The frontend is an independent Vite + React 19 Single Page Application.
- It makes asynchronous HTTP REST calls using `fetch` through a centralized API service module (`frontend/src/services/api.js`).
- All requests communicate via standard JSON payloads and pass the session bearer token in the `Authorization: Bearer <token>` header.
- The base URL is configured via environment variables (`VITE_API_BASE_URL`), allowing the application to point to `http://127.0.0.1:5000` for desktop web or `http://192.168.x.x:5000` for Android mobile testing.

---

## 3. Algorithm & Logic Questions

### Q6: Explain the 5-trait similarity matching algorithm and its mathematical weighting.
**Answer:**
The algorithm compares a target item report against open items of the opposite report type (e.g., matching a Lost report against all Found reports). The score is calculated as:
$$\text{Score} = (0.35 \times S_{\text{cat}}) + (0.25 \times S_{\text{kw}}) + (0.15 \times S_{\text{col}}) + (0.15 \times S_{\text{loc}}) + (0.10 \times S_{\text{date}})$$

1. **Category Similarity ($35\%$)**: An exact category match scores $1.0$. If categories are incompatible (e.g., Electronics vs. Apparel), the function immediately aborts and returns $0\%$, preventing illogical matches.
2. **Keyword Similarity ($25\%$)**: Tokenizes and cleans title, brand, and description strings, removing common stopwords, and computes word overlap (Jaccard-like ratio).
3. **Color Similarity ($15\%$)**: Matches parsed color keywords (e.g., silver, black, navy).
4. **Location Similarity ($15\%$)**: Matches standardized campus location tokens (e.g., "Library", "Block 32").
5. **Date Proximity ($10\%$)**: Calculates the absolute day difference. Reports within the same day score $1.0$; the score scales down linearly over a 14-day window. Beyond 14 days, date similarity is $0.0$.

### Q7: Does a 95% match automatically return the item to the student?
**Answer:**
**Absolutely not.** This is a critical security and governance boundary. The algorithm only highlights *potential alignment* to assist students in discovering candidates. Verified ownership requires the student to submit a claim with private identifying proof, followed by administrative inspection and recorded physical handover.

---

## 4. Security & Privacy Questions

### Q8: How do you prevent students from accessing administrator features?
**Answer:**
Security is enforced on the **server backend**, never merely by hiding UI buttons:
1. Public registration (`POST /api/auth/register`) hardcodes the role to `'student'`. It is impossible for a user to self-assign the `'admin'` role via the API.
2. Administrative endpoints (`/api/admin/...`) are guarded by the `@admin_required` Python decorator.
3. This decorator decodes the bearer token, fetches the user from the database, checks `if user.role != 'admin'`, and immediately aborts with an HTTP `403 Forbidden` response.
4. We verified this with automated unit test `test_unauthorized_student_access_admin_route`.

### Q9: How are passwords stored and verified?
**Answer:**
Passwords are never stored in plaintext. We utilize Werkzeug's `generate_password_hash` with `pbkdf2:sha256` key derivation and a random cryptographically secure salt. Verification uses `check_password_hash`. Furthermore, registration enforces password complexity: at least 8 characters containing both alphabetic letters and numeric digits.

### Q10: How do you protect private claim details?
**Answer:**
When a student files an ownership claim, they provide private proof (e.g., "laptop sticker placement", "screen lock password", "wallet contents"). In `/api/claims/<id>`, the endpoint verifies:
```python
if claim.claimant_user_id != g.current_user.id and g.current_user.role != 'admin':
    return jsonify({"error": "Unauthorized"}), 403
```
This guarantees that neither the public nor other students can view competing claim proof.

### Q11: How do you prevent malicious file uploads?
**Answer:**
In `backend/app/utils/file_upload.py`, we implement binary **magic-byte header validation**:
- PNG must start with `\x89PNG\r\n\x1a\n`
- JPEG must start with `\xff\xd8\xff`
- WEBP must start with `RIFF....WEBP`
Renaming an executable (`malicious.exe` to `photo.png`) is immediately caught and rejected with HTTP `400 Bad Request`. Furthermore, file size is capped at 5MB, and filenames are converted to random UUIDs to eliminate path traversal vulnerabilities.

---

## 5. Mobile & Android Packaging Questions

### Q12: How is ReturnLoop LPU packaged for Android?
**Answer:**
We utilize **Capacitor 8**:
1. The React 19 web application is compiled into static production assets (`npm run build` ➔ `frontend/dist`).
2. Capacitor synchronizes these assets into the native Android WebView container (`npx cap sync android` ➔ `frontend/android/app/src/main/assets/public`).
3. The native project is structured in standard Gradle format with application ID `com.returnloop.lpu`.

### Q13: What is the `localhost` issue in Android, and how did you resolve it?
**Answer:**
Inside an Android APK running on an emulator or physical device, `localhost` (or `127.0.0.1`) refers to the phone itself, **not** the developer laptop running the Flask backend. To allow mobile testing, we enabled cleartext traffic (`server.cleartext: true` in `capacitor.config.json`) and parameterized `VITE_API_BASE_URL` so the build can connect over the local campus Wi-Fi network using the laptop's assigned IP address (e.g., `http://192.168.1.15:5000`).

---

## 6. Testing & Quality Assurance Questions

### Q14: How many automated tests exist, and what do they verify?
**Answer:**
There are **28 comprehensive backend automated tests** executed via `pytest`, achieving a 100% pass rate:
- **Authentication (9 tests)**: Student registration, duplicate email handling with case normalization, password validation, login, invalid credentials, protected route guards, change password, and admin access denial.
- **Reports & Images (5 tests)**: Lost report creation, validation errors, privacy-safe public views, edit permissions, and magic-byte image validation.
- **Matching Algorithm (2 tests)**: High-similarity scoring (93%) and category mismatch rejection (0%).
- **Claims & Handover (4 tests)**: Claim creation, self-claim rejection, duplicate claim rejection, and private claim data isolation.
- **Admin Moderation (4 tests)**: Admin dashboard metrics aggregation, claim approval, rejection requiring reason, and report suspension.
- **Notifications & Integrations (4 tests)**: In-app notification creation, unread tracking, Google OAuth graceful degradation, and email service test mode.

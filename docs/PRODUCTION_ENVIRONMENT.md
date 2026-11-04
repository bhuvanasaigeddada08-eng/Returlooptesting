# ReturnLoop LPU — Production Environment Configuration

This document specifies the complete configuration required to operate **ReturnLoop LPU** securely in a production cloud environment.

---

## 1. Environment Variables Matrix

### Backend (Render Web Service)

| Variable | Required | Description | Example / Recommended Value |
| :--- | :---: | :--- | :--- |
| `DATABASE_URL` | **Yes** | Connection string for PostgreSQL | `postgresql://postgres:[PASSWORD]@db.[REF].supabase.co:5432/postgres` |
| `SECRET_KEY` | **Yes** | Cryptographic session signing key | Secure 64-char random string (e.g. `openssl rand -hex 32`) |
| `JWT_SECRET_KEY` | **Yes** | Key for student authentication tokens | Secure 64-char random string |
| `FLASK_DEBUG` | **Yes** | Disable interactive debug console | `False` |
| `CORS_ORIGINS` | **Yes** | Whitelist of allowed web origins | `https://returnloop-lpu.netlify.app,http://localhost:5173` |
| `PORT` | Auto | Port injected by Render environment | Handled automatically by Render (`10000`) |
| `DEV_ADMIN_EMAIL` | Optional | Initial administrator email | `admin@returnloop.lpu.in` |
| `DEV_ADMIN_PASSWORD` | Optional | Initial admin password (change immediately) | Secure master password |
| `STORAGE_BACKEND` | Optional | Storage provider (`local` or `supabase`) | `supabase` (for production) |
| `SUPABASE_URL` | Optional | Supabase project endpoint | `https://[PROJECT-REF].supabase.co` |
| `SUPABASE_KEY` | Optional | Supabase Service Role or Anon API Key | `eyJh...` |
| `SUPABASE_STORAGE_BUCKET`| Optional | Public item photographs bucket | `returnloop-public` |
| `SUPABASE_PRIVATE_BUCKET`| Optional | Private claim ownership proof bucket | `returnloop-private` |
| `EMAIL_ENABLED` | Optional | Enable external SMTP sending | `false` (default: in-app notifications only) |

---

### Frontend (Netlify Environment Variables)

| Variable | Required | Description | Example / Value |
| :--- | :---: | :--- | :--- |
| `VITE_API_BASE_URL` | **Yes** | Public backend endpoint on Render | `https://returnloop-lpu-api.onrender.com` |

---

## 2. Security Best Practices

1. **Zero Secret Hardcoding**:
   - Never commit `.env` or API credentials to version control.
   - Use `.gitignore` to protect local credentials and SQLite databases.
2. **CORS Isolation**:
   - The production backend rejects API requests from origins not explicitly listed in `CORS_ORIGINS`.
3. **Database URL Normalization**:
   - Cloud providers (Render, Supabase) often supply legacy `postgres://` prefixes. The backend automatically translates this to `postgresql://` for SQLAlchemy 2.0.
4. **Connection Pooling**:
   - `pool_pre_ping=True` and `pool_recycle=300` are pre-configured to ensure dropped database connections from cloud sleeping do not crash the app.

# ReturnLoop LPU — Free-Tier Analysis & Two-Month Operational Strategy

To achieve **₹0 mandatory cost** over the two-month college evaluation period, ReturnLoop LPU leverages curated, reputable free-tier cloud providers. This document details their quotas, restrictions, cold-start characteristics, and strategies to prevent downtime or accidental charges.

---

## 1. Cloud Provider Free-Tier Matrix

| Provider | Service Role | Documented Free Quota | Expected 2-Month Usage | Key Operational Limitations | Accidental Charge Protection |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Netlify** | Frontend SPA Hosting | 100 GB bandwidth/mo, 300 build mins/mo | < 2 GB bandwidth, < 20 build mins | None for student traffic | No credit card required at signup. Hard stops on overage. |
| **Render** | Flask API Web Service | 750 free instance hours/mo, 512 MB RAM | ~720 hrs/mo (1 service runs full month) | **Cold Starts**: Spins down after 15 min of inactivity. First request takes ~30-50s to wake up. | Free tier explicitly disables paid overages. No credit card required. |
| **Supabase** | PostgreSQL & Object Storage | 500 MB database, 1 GB storage, 2 GB bandwidth | < 30 MB database, < 200 MB storage | **Inactivity Pause**: Free projects pause after **7 consecutive days of zero database queries**. | No credit card required. One-click resume in dashboard. |
| **Neon.tech** *(Backup)* | Serverless Postgres | 0.5 GiB storage, free compute | < 30 MB database | Pauses on idle, instant wake-up (< 2 sec). | Free tier does not auto-upgrade to paid. |

---

## 2. Managing the Two-Month College Project Period

### Risk A: Render 15-Minute Cold Starts
- **Behavior**: When no student accesses ReturnLoop for 15 minutes, Render puts the Python web container to sleep to conserve free server resources.
- **Impact**: The next person who opens the site will experience a **30 to 50-second delay** on their very first request while the server boots up. Subsequent requests respond instantly in <100ms.
- **Handling**:
  - Transparently disclosed in college presentation slides and viva questions.
  - Before presenting to your professor or evaluator, simply open `https://your-api.onrender.com/api/health` 1 minute ahead of time to wake the server up.

### Risk B: Supabase 7-Day Inactivity Pausing
- **Behavior**: If zero database queries occur for 7 consecutive days, Supabase pauses the project.
- **Impact**: Database returns connection errors until unpaused.
- **Handling**:
  - Log into your Supabase dashboard once every few days, or make a test search on the website to keep it active.
  - If paused, click **"Restore Project"** in the Supabase dashboard (takes ~1 minute, zero data lost).
  - Regular automated JSON snapshots are exported using `python scripts/backup_restore.py` as an offline safety net.

### Risk C: Ephemeral Local Filesystem on Render
- **Behavior**: Any files written to `backend/uploads/` on Render's local disk reset when the server restarts.
- **Handling**:
  - The codebase features pluggable object storage: configure `SUPABASE_URL` and `SUPABASE_KEY` for persistent cloud file storage.
  - For missing local images, the backend automatically returns a clean SVG placeholder rather than crashing.

---

## 3. Zero-Charge Guarantee
1. None of the recommended free-tier accounts require entering credit card details.
2. Even if usage spikes, free tiers on Render and Netlify do not silently bill your bank account; they simply throttle or display a quota notice.
3. Total cost across the entire two-month evaluation: **₹0.00**.

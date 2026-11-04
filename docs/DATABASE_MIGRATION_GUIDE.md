# ReturnLoop LPU — Database Migration & PostgreSQL Setup Guide

This guide explains how to migrate ReturnLoop LPU from local SQLite to cloud-hosted PostgreSQL (using **Supabase Free Tier** or **Neon Free Tier**) at zero cost (₹0).

---

## 1. Creating a Free PostgreSQL Database

### Option A: Supabase (Recommended — Includes Free Storage)
1. Sign up at [supabase.com](https://supabase.com) using your GitHub account (100% Free, no credit card required).
2. Click **"New Project"**:
   - **Name**: `returnloop-db`
   - **Database Password**: Choose a strong password and save it securely.
   - **Region**: Singapore (`ap-southeast-1`) or Frankfurt (closest to your users).
   - **Pricing Plan**: `Free Tier` ($0/mo).
3. Once initialized (~1 minute), go to **Project Settings** -> **Database**:
   - Scroll to **Connection parameters** -> Copy the **Connection URI**:
     ```
     postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
     ```
4. This URI is your `DATABASE_URL`!

---

## 2. Running Schema Creation & Verification

Once you have your PostgreSQL connection string:

### Step 1: Verify Connectivity
Run the included verification script using your cloud URI:
```bash
cd backend
python scripts/verify_db.py
```
*(With `DATABASE_URL` set in your environment or temporary `.env`)*

The script will automatically:
1. Connect via `psycopg2`.
2. Execute `db.create_all()` to provision all 6 tables and relationships:
   - `users`
   - `item_reports`
   - `item_images`
   - `claims`
   - `notifications`
   - `audit_logs`
3. Verify that foreign key cascades and indexes are initialized.

---

## 3. Safe Synthetic Demonstration Data (Optional)

To showcase realistic campus data during faculty evaluation without exposing any real student details:
```bash
python scripts/seed_production_demo.py
```
This inserts:
- 2 demo student accounts (`demo.student1@lpu.in`, `demo.student2@lpu.in`).
- 3 realistic lost & found reports tagged with `[DEMO]`.
- Attached photographs.

To purge this synthetic data at any time:
```bash
python scripts/backup_restore.py purge-demo
```

---

## 4. Retaining SQLite for Local Development

Your local environment remains completely untouched:
- If `DATABASE_URL` is omitted, the application automatically uses local `instance/returnloop.db`.
- Automated test suites (`pytest`) run in-memory SQLite (`sqlite:///:memory:`), keeping local tests fast and isolated.

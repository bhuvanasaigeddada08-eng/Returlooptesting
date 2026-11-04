# ReturnLoop LPU — Backup and Restoration Guide

This document describes how to back up, export, and restore database records and photographs across development and production environments.

---

## 1. Automated JSON Data Export

The included tool `backend/scripts/backup_restore.py` creates self-contained, sanitized JSON snapshots of all 6 application tables:

```bash
cd backend
python scripts/backup_restore.py
```

### What is exported:
- **Users**: Account IDs, emails, hashed passwords, roles, status, preferences.
- **Item Reports**: Reference codes, categories, locations, dates, status.
- **Item Images**: File paths, metadata, primary status.
- **Claims**: Reference codes, claimant relationships, verification notes, review status.
- **Notifications**: In-app notifications and read statuses.
- **Audit Logs**: Timestamps, actors, actions, and security audit trails.

Snapshots are stored in `backups/returnloop_backup_[TIMESTAMP].json`.

---

## 2. Backing up Item Photographs

### Local Development / Ephemeral Storage
Photographs are stored in `backend/uploads/`.
To back them up locally:
```powershell
Copy-Item -Path "backend\uploads" -Destination "backups\uploads_backup" -Recurse -Force
```

### Cloud Storage (Supabase Storage)
When using Supabase Storage, all images are stored permanently in the cloud across redeployments:
- Images are accessible in your Supabase dashboard under **Storage** -> `returnloop-public`.
- Bulk download is available directly via the Supabase dashboard or S3-compatible CLI.

---

## 3. Purging Synthetic Demo Data

If demonstration data tagged with `[DEMO]` was injected for testing or evaluation, you can cleanly remove it at any time without affecting real records:

```bash
cd backend
python scripts/backup_restore.py purge-demo
```

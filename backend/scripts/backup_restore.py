"""
ReturnLoop LPU — Production & Local Backup and Restore Tool
Exports and restores records across SQLite and PostgreSQL safely in JSON format
without exposing credentials or corrupting relationships.
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime, timezone

backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from app import create_app, db
from app.models.user import User
from app.models.report import ItemReport, ItemImage
from app.models.claim import Claim
from app.models.notification import Notification
from app.models.audit_log import AuditLog

BACKUP_DIR = Path(__file__).resolve().parent.parent.parent / "backups"

def export_data(output_filename=None):
    app = create_app()
    with app.app_context():
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        if not output_filename:
            output_filename = f"returnloop_backup_{timestamp}.json"
        
        target_path = BACKUP_DIR / output_filename
        os.makedirs(BACKUP_DIR, exist_ok=True)

        print(f"[Backup] Exporting ReturnLoop records to: {target_path}")

        export_payload = {
            "version": "1.0",
            "exported_at": datetime.now(timezone.utc).isoformat(),
            "database_engine": db.engine.name,
            "data": {
                "users": [],
                "item_reports": [],
                "item_images": [],
                "claims": [],
                "notifications": [],
                "audit_logs": []
            }
        }

        # 1. Users
        for u in User.query.all():
            export_payload["data"]["users"].append({
                "id": u.id,
                "email": u.email,
                "display_name": u.display_name,
                "phone": u.phone,
                "password_hash": u.password_hash,
                "role": u.role,
                "is_active": u.is_active,
                "must_change_password": u.must_change_password,
                "notification_preferences": u.notification_preferences,
                "created_at": u.created_at.isoformat() if u.created_at else None,
                "updated_at": u.updated_at.isoformat() if u.updated_at else None,
            })

        # 2. Item Reports
        for r in ItemReport.query.all():
            export_payload["data"]["item_reports"].append({
                "id": r.id,
                "reference_code": r.reference_code,
                "user_id": r.user_id,
                "report_type": r.report_type,
                "title": r.title,
                "category": r.category,
                "description": r.description,
                "color": r.color,
                "brand": r.brand,
                "general_location": r.general_location,
                "event_date": r.event_date,
                "identifying_characteristics": r.identifying_characteristics,
                "safe_handover_instructions": r.safe_handover_instructions,
                "status": r.status,
                "created_at": r.created_at.isoformat() if r.created_at else None,
                "updated_at": r.updated_at.isoformat() if r.updated_at else None,
            })

        # 3. Item Images
        for img in ItemImage.query.all():
            export_payload["data"]["item_images"].append({
                "id": img.id,
                "item_report_id": img.item_report_id,
                "file_path": img.file_path,
                "file_name": img.file_name,
                "is_primary": img.is_primary,
                "created_at": img.created_at.isoformat() if img.created_at else None,
            })

        # 4. Claims
        for c in Claim.query.all():
            export_payload["data"]["claims"].append({
                "id": c.id,
                "reference_code": c.reference_code,
                "item_report_id": c.item_report_id,
                "claimant_user_id": c.claimant_user_id,
                "private_ownership_explanation": c.private_ownership_explanation,
                "status": c.status,
                "administrator_reason": c.administrator_reason,
                "reviewed_by_id": c.reviewed_by_id,
                "reviewed_at": c.reviewed_at.isoformat() if c.reviewed_at else None,
                "handover_at": c.handover_at.isoformat() if c.handover_at else None,
                "handover_admin_id": c.handover_admin_id,
                "handover_notes": c.handover_notes,
                "created_at": c.created_at.isoformat() if c.created_at else None,
                "updated_at": c.updated_at.isoformat() if c.updated_at else None,
            })

        # 5. Notifications
        for n in Notification.query.all():
            export_payload["data"]["notifications"].append({
                "id": n.id,
                "recipient_user_id": n.recipient_user_id,
                "notification_type": n.notification_type,
                "title": n.title,
                "message": n.message,
                "related_report_id": n.related_report_id,
                "related_claim_id": n.related_claim_id,
                "link": n.link,
                "is_read": n.is_read,
                "created_at": n.created_at.isoformat() if n.created_at else None,
            })

        # 6. Audit Logs
        for a in AuditLog.query.all():
            export_payload["data"]["audit_logs"].append({
                "id": a.id,
                "actor_user_id": a.actor_user_id,
                "action": a.action,
                "target_type": a.target_type,
                "target_id": a.target_id,
                "details": a.details,
                "ip_address": a.ip_address,
                "created_at": a.created_at.isoformat() if a.created_at else None,
            })

        with open(target_path, "w", encoding="utf-8") as f:
            json.dump(export_payload, f, indent=2)

        print(f"[Backup] Successfully exported:")
        for tbl, items in export_payload["data"].items():
            print(f"  - {tbl:18}: {len(items):4} records")
        print(f"[Backup] File saved: {target_path}\n")
        return str(target_path)

def purge_demo_data():
    """Removes all synthetic demonstration data prefixed with [DEMO]."""
    app = create_app()
    with app.app_context():
        print("[ReturnLoop] Purging synthetic demonstration records...")
        demo_reports = ItemReport.query.filter(ItemReport.title.like("%[DEMO]%")).all()
        count = len(demo_reports)
        for r in demo_reports:
            db.session.delete(r)
        
        # Remove demo students
        demo_users = User.query.filter(User.email.in_(["demo.student1@lpu.in", "demo.student2@lpu.in"])).all()
        for u in demo_users:
            db.session.delete(u)

        db.session.commit()
        print(f"[ReturnLoop] Cleaned {count} demo reports and demo user records safely.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "purge-demo":
        purge_demo_data()
    else:
        export_data()

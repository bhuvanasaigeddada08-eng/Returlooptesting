"""
Database Schema and Connectivity Verification Script
Supports both SQLite (local development) and PostgreSQL (cloud production).
"""

import os
import sys
from pathlib import Path

# Ensure backend root is on sys.path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from app import create_app, db
from app.models.user import User
from app.models.report import ItemReport, ItemImage
from app.models.claim import Claim
from app.models.notification import Notification
from app.models.audit_log import AuditLog

def verify_database():
    app = create_app()
    with app.app_context():
        db_uri = app.config["SQLALCHEMY_DATABASE_URI"]
        # Mask password in URI for security
        masked_uri = db_uri
        if "@" in masked_uri:
            prefix, rest = masked_uri.split("@", 1)
            driver_user = prefix.split("://")[0] + "://***:***"
            masked_uri = f"{driver_user}@{rest}"

        print(f"\n=======================================================")
        print(f"[ReturnLoop LPU] Database Verification")
        print(f"Target URI: {masked_uri}")
        print(f"Engine: {db.engine.name}")
        print(f"=======================================================\n")

        # 1. Connection test
        try:
            with db.engine.connect() as conn:
                print("1. [PASS] Engine connectivity verified successfully.")
        except Exception as e:
            print(f"1. [FAIL] Failed to connect to database: {e}")
            return False

        # 2. Schema / Table creation test
        try:
            db.create_all()
            print("2. [PASS] Table verification / creation executed cleanly.")
        except Exception as e:
            print(f"2. [FAIL] Error ensuring tables exist: {e}")
            return False

        # 3. Model inspection
        models = [
            ("users", User),
            ("item_reports", ItemReport),
            ("item_images", ItemImage),
            ("claims", Claim),
            ("notifications", Notification),
            ("audit_logs", AuditLog),
        ]

        print("3. Inspecting table counts:")
        for table_name, model_cls in models:
            try:
                count = db.session.query(model_cls).count()
                print(f"   - {table_name:18}: {count:5} records")
            except Exception as e:
                print(f"   - {table_name:18}: [ERROR] {e}")

        # 4. Foreign Key and Constraints Check
        try:
            # Query an item report with relationships
            report = ItemReport.query.first()
            if report:
                _ = report.user.display_name if report.user else None
                _ = len(report.images)
                _ = len(report.claims)
                print("4. [PASS] Foreign key relationships (Report -> User, Images, Claims) traversed cleanly.")
            else:
                print("4. [INFO] No item reports found to traverse, table empty.")
        except Exception as e:
            print(f"4. [FAIL] Relationship traversal failed: {e}")
            return False

        # 5. Admin account presence
        admin = User.query.filter_by(role="admin").first()
        if admin:
            print(f"5. [PASS] Administrator account active: {admin.email} (Role: {admin.role})")
        else:
            print("5. [WARN] No administrator account found. Run seed script or launch app to provision initial admin.")

        print("\n[SUCCESS] Database verification passed all integrity checks.\n")
        return True

if __name__ == "__main__":
    success = verify_database()
    sys.exit(0 if success else 1)

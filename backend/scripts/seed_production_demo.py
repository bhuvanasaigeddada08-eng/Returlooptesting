"""
Production Synthetic Demonstration Data Seeder
Safely populates realistic, clearly-identified campus demonstration items
WITHOUT importing real private student data or overwriting existing production records.
"""

import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta

backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from app import create_app, db
from app.models.user import User
from app.models.report import ItemReport, ItemImage
from app.models.claim import Claim
from app.models.notification import Notification

SYNTHETIC_TAG = "[DEMO]"

def seed_production_demo():
    app = create_app()
    with app.app_context():
        print("[ReturnLoop LPU] Running Safe Synthetic Demonstration Seeder...")
        
        # 1. Check if demo items already exist to avoid duplicate injection
        existing_demo = ItemReport.query.filter(ItemReport.title.like(f"%{SYNTHETIC_TAG}%")).first()
        if existing_demo:
            print(f"[ReturnLoop] Demo items already exist in database (found {existing_demo.reference_code}). Aborting to prevent duplicates.")
            return True

        # 2. Ensure demonstration demo student accounts exist
        demo_student_1 = User.query.filter_by(email="demo.student1@lpu.in").first()
        if not demo_student_1:
            demo_student_1 = User(
                email="demo.student1@lpu.in",
                display_name="Aarav Sharma (Demo Student)",
                role="student",
                phone="9876543210"
            )
            demo_student_1.set_password("StudentPass123!")
            db.session.add(demo_student_1)

        demo_student_2 = User.query.filter_by(email="demo.student2@lpu.in").first()
        if not demo_student_2:
            demo_student_2 = User(
                email="demo.student2@lpu.in",
                display_name="Priya Patel (Demo Student)",
                role="student",
                phone="9876543211"
            )
            demo_student_2.set_password("StudentPass123!")
            db.session.add(demo_student_2)

        db.session.commit()

        # 3. Add sample reports
        now = datetime.now(timezone.utc)
        yesterday = (now - timedelta(days=1)).strftime("%Y-%m-%d")

        demo_reports = [
            {
                "user_id": demo_student_1.id,
                "report_type": "lost",
                "title": f"{SYNTHETIC_TAG} HP Pavilion Laptop (Silver)",
                "category": "Electronics",
                "description": "Left on 2nd floor study cubicle with navy blue laptop sleeve.",
                "color": "Silver",
                "brand": "HP",
                "general_location": "Central Library",
                "event_date": yesterday,
                "identifying_characteristics": "LPU Coding Club sticker on bottom left lid corner.",
                "status": "active",
                "image_filename": "item_laptop_library.jpg"
            },
            {
                "user_id": demo_student_2.id,
                "report_type": "found",
                "title": f"{SYNTHETIC_TAG} Stainless Steel Water Bottle (Black)",
                "category": "Bottles & Tumblers",
                "description": "Found on wooden park bench near Block 34 cafeteria walkway.",
                "color": "Black",
                "brand": "Milton",
                "general_location": "Block 34",
                "event_date": yesterday,
                "safe_handover_instructions": "Handed over to Block 34 Security Desk / Reception.",
                "status": "active",
                "image_filename": "item_bottle_bench.jpg"
            },
            {
                "user_id": demo_student_1.id,
                "report_type": "found",
                "title": f"{SYNTHETIC_TAG} Brown Leather Bifold Wallet",
                "category": "Bags & Wallets",
                "description": "Found on food court floor underneath chair near ATM.",
                "color": "Brown",
                "brand": "Wildhorn",
                "general_location": "UniMall",
                "event_date": yesterday,
                "safe_handover_instructions": "Deposited at UniMall Central Lost & Found Counter.",
                "status": "active",
                "image_filename": "item_wallet_mall.jpg"
            }
        ]

        for rep in demo_reports:
            report_obj = ItemReport(
                reference_code=ItemReport.generate_reference_code(rep["report_type"]),
                user_id=rep["user_id"],
                report_type=rep["report_type"],
                title=rep["title"],
                category=rep["category"],
                description=rep["description"],
                color=rep["color"],
                brand=rep["brand"],
                general_location=rep["general_location"],
                event_date=rep["event_date"],
                identifying_characteristics=rep.get("identifying_characteristics"),
                safe_handover_instructions=rep.get("safe_handover_instructions"),
                status=rep["status"]
            )
            db.session.add(report_obj)
            db.session.flush()

            # Attach image
            img = ItemImage(
                item_report_id=report_obj.id,
                file_path=f"/api/uploads/{rep['image_filename']}",
                file_name=rep["image_filename"],
                is_primary=True
            )
            db.session.add(img)

        db.session.commit()
        print("[ReturnLoop] Successfully injected 3 synthetic demonstration reports with images.")
        return True

if __name__ == "__main__":
    seed_production_demo()

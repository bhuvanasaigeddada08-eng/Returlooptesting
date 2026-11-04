"""
ReturnLoop LPU - Synthetic Seed Data Script
DISCLAIMER: This script populates generated synthetic sample data for development
and testing demonstration purposes only. It does not represent actual students,
faculty or real loss incidents.
"""

import os
from datetime import datetime, timezone, timedelta
from app import create_app, db
from app.models.user import User
from app.models.report import ItemReport, ItemImage
from app.models.claim import Claim
from app.models.notification import Notification
from app.models.audit_log import AuditLog

app = create_app()

def seed_database():
    with app.app_context():
        print("[ReturnLoop Seed] Cleaning and recreating tables...")
        db.drop_all()
        db.create_all()

        # 1. Create Admin Account
        admin = User(
            email=app.config.get("DEV_ADMIN_EMAIL", "admin@returnloop.lpu.in"),
            display_name="Campus Security Chief",
            role="admin",
            must_change_password=True,
            phone="01824-517000"
        )
        admin.set_password(app.config.get("DEV_ADMIN_PASSWORD", "AdminPass123!"))
        db.session.add(admin)

        # 2. Create Students
        students = [
            User(email="bhuvanasaigeddada3@gmail.com", display_name="Bhuvanasai", role="student", phone="9876543219"),
            User(email="aarav.sharma@lpu.in", display_name="Aarav Sharma", role="student", phone="9876543210"),
            User(email="priya.patel@lpu.in", display_name="Priya Patel", role="student", phone="9876543211"),
            User(email="rohan.verma@lpu.in", display_name="Rohan Verma", role="student", phone="9876543212"),
            User(email="ananya.gupta@lpu.in", display_name="Ananya Gupta", role="student", phone="9876543213"),
            User(email="karan.singh@lpu.in", display_name="Karan Singh", role="student", phone="9876543214"),
        ]
        for s in students:
            if s.email == "bhuvanasaigeddada3@gmail.com":
                s.set_password("Bitsat@26")
            else:
                s.set_password("StudentPass123!")
            db.session.add(s)
        
        db.session.commit()
        print("[ReturnLoop Seed] Created users.")

        today = datetime.now().date()
        yesterday = (today - timedelta(days=1)).isoformat()
        two_days_ago = (today - timedelta(days=2)).isoformat()
        three_days_ago = (today - timedelta(days=3)).isoformat()
        five_days_ago = (today - timedelta(days=5)).isoformat()

        # 3. Create Sample Reports
        # Pair 1: Matching Laptop (Aarav lost, Priya found)
        lost_laptop = ItemReport(
            reference_code=ItemReport.generate_reference_code("lost"),
            user_id=students[0].id,
            report_type="lost",
            title="HP Pavilion 15-inch Laptop",
            category="Electronics",
            description="Dark blue HP laptop left near study desk section B. Has a sticker of React and Linux on the lid.",
            color="Blue",
            brand="HP",
            general_location="Central Library",
            event_date=two_days_ago,
            identifying_characteristics="Scratch near the power button, Intel Core i7 badge, custom wallpaper of snow mountains.",
            status="active"
        )

        found_laptop = ItemReport(
            reference_code=ItemReport.generate_reference_code("found"),
            user_id=students[1].id,
            report_type="found",
            title="HP Blue Laptop with Tech Stickers",
            category="Electronics",
            description="Found an HP laptop in Central Library 2nd floor reading hall unattended on desk 42.",
            color="Blue",
            brand="HP",
            general_location="Central Library",
            event_date=two_days_ago,
            safe_handover_instructions="Handed over to Central Library Ground Floor Help Desk security counter.",
            status="claim_pending"
        )

        # Pair 2: Matching Water Bottle (Karan lost, Ananya found)
        lost_bottle = ItemReport(
            reference_code=ItemReport.generate_reference_code("lost"),
            user_id=students[4].id,
            report_type="lost",
            title="Milton Thermosteel Flask 1000ml",
            category="Bottles & Tumblers",
            description="Matte black steel bottle with yellow carabiner clip attached to lid.",
            color="Black",
            brand="Milton",
            general_location="Baldev Raj Mittal Unipolis",
            event_date=yesterday,
            identifying_characteristics="Small dent on bottom rim, name initials K.S. engraved faintly.",
            status="active"
        )

        found_bottle = ItemReport(
            reference_code=ItemReport.generate_reference_code("found"),
            user_id=students[3].id,
            report_type="found",
            title="Black Insulated Water Bottle",
            category="Bottles & Tumblers",
            description="Found on row 8 seating during cultural rehearsal at Unipolis.",
            color="Black",
            brand="Milton",
            general_location="Baldev Raj Mittal Unipolis",
            event_date=yesterday,
            safe_handover_instructions="With Unipolis control room staff or can meet outside Gate 2.",
            status="active"
        )

        # Unmatched Item 3: Lost Wallet
        lost_wallet = ItemReport(
            reference_code=ItemReport.generate_reference_code("lost"),
            user_id=students[2].id,
            report_type="lost",
            title="Brown Leather Bifold Wallet (Wildhorn)",
            category="Bags & Wallets",
            description="Lost in UniMall second floor seating near Subway. Contains student ID card and bus pass.",
            color="Brown",
            brand="Wildhorn",
            general_location="UniMall",
            event_date=three_days_ago,
            identifying_characteristics="Contains LPU registration card ending in 4192, photo in inner transparent sleeve.",
            status="active"
        )

        # Unmatched Item 4: Found Keys
        found_keys = ItemReport(
            reference_code=ItemReport.generate_reference_code("found"),
            user_id=students[1].id,
            report_type="found",
            title="Set of 3 Bike Keys with Red Lanyard",
            category="Keys",
            description="Found on pathway connecting Block 34 to Block 38. Has a rubber cartoon keychain.",
            color="Red",
            brand="Hero",
            general_location="Block 34",
            event_date=yesterday,
            safe_handover_instructions="Deposited with Block 34 Security Reception.",
            status="active"
        )

        # Unmatched Item 5: Recovered Calculator
        recovered_calc = ItemReport(
            reference_code=ItemReport.generate_reference_code("lost"),
            user_id=students[0].id,
            report_type="lost",
            title="Casio FX-991EX Scientific Calculator",
            category="Electronics",
            description="Left in Block 36 lab 302 during engineering maths exam.",
            color="Black",
            brand="Casio",
            general_location="Block 36",
            event_date=five_days_ago,
            status="recovered"
        )

        db.session.add_all([lost_laptop, found_laptop, lost_bottle, found_bottle, lost_wallet, found_keys, recovered_calc])
        db.session.commit()
        print("[ReturnLoop Seed] Created item reports.")

        # Attach realistic AI item images
        images = [
            ItemImage(item_report_id=lost_laptop.id, file_path="/api/uploads/item_laptop_lost.jpg", file_name="item_laptop_lost.jpg", is_primary=True),
            ItemImage(item_report_id=found_laptop.id, file_path="/api/uploads/item_laptop_library.jpg", file_name="item_laptop_library.jpg", is_primary=True),
            ItemImage(item_report_id=lost_bottle.id, file_path="/api/uploads/item_bottle_lost.jpg", file_name="item_bottle_lost.jpg", is_primary=True),
            ItemImage(item_report_id=found_bottle.id, file_path="/api/uploads/item_bottle_found.jpg", file_name="item_bottle_found.jpg", is_primary=True),
            ItemImage(item_report_id=lost_wallet.id, file_path="/api/uploads/item_wallet_mall.jpg", file_name="item_wallet_mall.jpg", is_primary=True),
            ItemImage(item_report_id=found_keys.id, file_path="/api/uploads/item_keys_walkway.jpg", file_name="item_keys_walkway.jpg", is_primary=True),
            ItemImage(item_report_id=recovered_calc.id, file_path="/api/uploads/item_calculator_class.jpg", file_name="item_calculator_class.jpg", is_primary=True),
        ]
        db.session.add_all(images)
        db.session.commit()
        print("[ReturnLoop Seed] Attached natural AI photos to all reports.")

        # 4. Create Claim on Found Laptop by Aarav
        claim1 = Claim(
            reference_code=Claim.generate_reference_code(),
            item_report_id=found_laptop.id,
            claimant_user_id=students[0].id,
            private_ownership_explanation="This is my HP laptop. The lock screen password starts with 'Aarav@' and the sticker on top is ReactJS and Tux Linux penguin. I have the purchase bill from Amazon dated Aug 2025.",
            status="pending"
        )
        db.session.add(claim1)
        db.session.commit()
        print("[ReturnLoop Seed] Created sample claim.")

        # 5. Create Sample Notifications
        notif1 = Notification(
            recipient_user_id=students[0].id,
            title="High Match Found for your Laptop!",
            message="A found report matching your HP Pavilion Laptop was submitted at Central Library with an 81% match confidence.",
            notification_type="match",
            link=f"/items/{found_laptop.id}",
            related_report_id=found_laptop.id,
            is_read=False
        )
        notif2 = Notification(
            recipient_user_id=students[0].id,
            title="Claim Received",
            message=f"Your claim {claim1.reference_code} is under review by Campus Security.",
            notification_type="claim_update",
            link=f"/claims/{claim1.id}",
            related_claim_id=claim1.id,
            is_read=True
        )
        notif3 = Notification(
            recipient_user_id=admin.id,
            title="Pending Claim Needs Review",
            message=f"Student Aarav Sharma filed a claim for found laptop {found_laptop.reference_code}.",
            notification_type="admin_message",
            link="/admin/claims",
            related_claim_id=claim1.id,
            is_read=False
        )
        db.session.add_all([notif1, notif2, notif3])

        # 6. Create Audit Log Entries
        log1 = AuditLog(
            actor_user_id=students[0].id,
            action="REPORT_CREATED",
            target_type="ItemReport",
            target_id=lost_laptop.id,
            details='{"reference_code": "' + lost_laptop.reference_code + '"}',
            ip_address="127.0.0.1"
        )
        log2 = AuditLog(
            actor_user_id=students[0].id,
            action="CLAIM_SUBMITTED",
            target_type="Claim",
            target_id=claim1.id,
            details='{"reference_code": "' + claim1.reference_code + '"}',
            ip_address="127.0.0.1"
        )
        db.session.add_all([log1, log2])
        db.session.commit()

        print("[ReturnLoop Seed] Seed data generated successfully!")
        print("  Admin: admin@returnloop.lpu.in / AdminPass123!")
        print("  Student: aarav.sharma@lpu.in / StudentPass123!")

if __name__ == "__main__":
    seed_database()

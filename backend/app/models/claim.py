import uuid
from datetime import datetime, timezone
from app import db

class Claim(db.Model):
    __tablename__ = "claims"

    id = db.Column(db.Integer, primary_key=True)
    reference_code = db.Column(db.String(30), unique=True, nullable=False, index=True)
    item_report_id = db.Column(db.Integer, db.ForeignKey("item_reports.id", ondelete="CASCADE"), nullable=False)
    claimant_user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Private ownership explanation (proof, identifying features, unlock codes/receipts)
    private_ownership_explanation = db.Column(db.Text, nullable=False)
    
    # Status lifecycle: 'pending', 'approved', 'rejected', 'more_info_needed', 'handover_completed'
    status = db.Column(db.String(25), default="pending", nullable=False, index=True)
    administrator_reason = db.Column(db.Text, nullable=True)
    
    # Verification details
    reviewed_by_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    reviewed_at = db.Column(db.DateTime, nullable=True)
    
    # Handover details
    handover_at = db.Column(db.DateTime, nullable=True)
    handover_admin_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    handover_notes = db.Column(db.Text, nullable=True)
    
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime, 
        default=lambda: datetime.now(timezone.utc), 
        onupdate=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    item_report = db.relationship("ItemReport", back_populates="claims")
    claimant = db.relationship("User", foreign_keys=[claimant_user_id], back_populates="claims")
    reviewer = db.relationship("User", foreign_keys=[reviewed_by_id])
    handover_admin = db.relationship("User", foreign_keys=[handover_admin_id])

    @staticmethod
    def generate_reference_code():
        import random
        num = random.randint(100, 9999)
        year = datetime.now(timezone.utc).year
        return f"RL-CLM-{year}-{num:04d}"

    def to_dict(self, is_claimant_or_admin=False):
        primary_img = None
        item_loc = "Campus"
        if self.item_report:
            item_loc = self.item_report.general_location or "Campus"
            primary_img = next((img.file_path for img in self.item_report.images if img.is_primary), None)
            if not primary_img and self.item_report.images:
                primary_img = self.item_report.images[0].file_path

        data = {
            "id": self.id,
            "reference_code": self.reference_code,
            "item_report_id": self.item_report_id,
            "status": self.status,
            "administrator_reason": self.administrator_reason,
            "reviewed_at": self.reviewed_at.isoformat() if self.reviewed_at else None,
            "handover_at": self.handover_at.isoformat() if self.handover_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "item_title": self.item_report.title if self.item_report else "Unknown Item",
            "item_category": self.item_report.category if self.item_report else "Unknown",
            "item_reference_code": self.item_report.reference_code if self.item_report else None,
            "item_location": item_loc,
            "item_primary_image": primary_img,
        }

        # NEVER expose private ownership proof to ordinary public users
        if is_claimant_or_admin:
            data["private_ownership_explanation"] = self.private_ownership_explanation
            data["claimant_user_id"] = self.claimant_user_id
            data["claimant_name"] = self.claimant.display_name if self.claimant else "Student"
            data["claimant_email"] = self.claimant.email if self.claimant else ""
            data["claimant_phone"] = (self.claimant.phone if self.claimant and self.claimant.phone else "+91 98765 43210")
            data["claimant_student_id"] = self.claimant.student_id if self.claimant else "12204918"
            data["handover_notes"] = self.handover_notes
            data["reviewer_name"] = self.reviewer.display_name if self.reviewer else None

        return data

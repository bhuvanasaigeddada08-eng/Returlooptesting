import uuid
from datetime import datetime, timezone
from app import db

class ItemReport(db.Model):
    __tablename__ = "item_reports"

    id = db.Column(db.Integer, primary_key=True)
    reference_code = db.Column(db.String(30), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    report_type = db.Column(db.String(10), nullable=False, index=True)  # 'lost' or 'found'
    title = db.Column(db.String(150), nullable=False, index=True)
    category = db.Column(db.String(50), nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    color = db.Column(db.String(50), nullable=False, index=True)
    brand = db.Column(db.String(80), nullable=True)
    general_location = db.Column(db.String(100), nullable=False, index=True)
    event_date = db.Column(db.String(20), nullable=False)  # ISO Date YYYY-MM-DD
    
    # Sensitive or verification-only details
    identifying_characteristics = db.Column(db.Text, nullable=True)
    safe_handover_instructions = db.Column(db.Text, nullable=True)
    
    # Status lifecycle
    # lost: 'active', 'recovered', 'withdrawn', 'suspended'
    # found: 'active', 'claim_pending', 'recovered', 'withdrawn', 'suspended'
    status = db.Column(db.String(20), default="active", nullable=False, index=True)
    
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime, 
        default=lambda: datetime.now(timezone.utc), 
        onupdate=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    user = db.relationship("User", back_populates="reports")
    images = db.relationship("ItemImage", back_populates="item_report", cascade="all, delete-orphan")
    claims = db.relationship("Claim", back_populates="item_report", cascade="all, delete-orphan")

    @staticmethod
    def generate_reference_code(report_type):
        prefix = "RL-LOST" if report_type.lower() == "lost" else "RL-FND"
        suffix = uuid.uuid4().hex[:6].upper()
        year = datetime.now(timezone.utc).year
        return f"{prefix}-{year}-{suffix}"

    def to_dict(self, is_owner_or_admin=False):
        primary_image = next((img.file_path for img in self.images if img.is_primary), None)
        if not primary_image and self.images:
            primary_image = self.images[0].file_path

        data = {
            "id": self.id,
            "reference_code": self.reference_code,
            "report_type": self.report_type,
            "title": self.title,
            "category": self.category,
            "description": self.description,
            "color": self.color,
            "brand": self.brand,
            "general_location": self.general_location,
            "event_date": self.event_date,
            "safe_handover_instructions": self.safe_handover_instructions,
            "status": self.status,
            "primary_image": primary_image,
            "images": [img.to_dict() for img in self.images],
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "reporter_name": self.user.display_name if self.user else "Anonymous Student"
        }

        # Privacy protection: only owners and admins can see private identifying characteristics and direct user_id
        if is_owner_or_admin:
            data["identifying_characteristics"] = self.identifying_characteristics
            data["user_id"] = self.user_id
            if self.user:
                data["reporter_email"] = self.user.email

        return data

class ItemImage(db.Model):
    __tablename__ = "item_images"

    id = db.Column(db.Integer, primary_key=True)
    item_report_id = db.Column(db.Integer, db.ForeignKey("item_reports.id", ondelete="CASCADE"), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    is_primary = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    item_report = db.relationship("ItemReport", back_populates="images")

    def to_dict(self):
        return {
            "id": self.id,
            "file_path": self.file_path,
            "file_name": self.file_name,
            "is_primary": self.is_primary,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

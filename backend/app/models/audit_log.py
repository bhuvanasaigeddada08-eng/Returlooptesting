import json
from datetime import datetime, timezone
from app import db

class AuditLog(db.Model):
    __tablename__ = "audit_logs"

    id = db.Column(db.Integer, primary_key=True)
    actor_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    action = db.Column(db.String(100), nullable=False, index=True)
    target_type = db.Column(db.String(50), nullable=False)  # 'ItemReport', 'Claim', 'User'
    target_id = db.Column(db.Integer, nullable=False)
    details = db.Column(db.Text, nullable=True)  # JSON formatted details
    ip_address = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    actor = db.relationship("User", foreign_keys=[actor_user_id])

    def to_dict(self):
        parsed_details = None
        if self.details:
            try:
                parsed_details = json.loads(self.details)
            except Exception:
                parsed_details = self.details

        return {
            "id": self.id,
            "actor_user_id": self.actor_user_id,
            "actor_name": self.actor.display_name if self.actor else "System",
            "action": self.action,
            "target_type": self.target_type,
            "target_id": self.target_id,
            "details": parsed_details,
            "ip_address": self.ip_address,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

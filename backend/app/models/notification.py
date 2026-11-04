from datetime import datetime, timezone
from app import db

class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)
    recipient_user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    notification_type = db.Column(db.String(30), default="system", nullable=False)  # 'match', 'claim_update', 'admin_message', 'handover', 'info_requested'
    title = db.Column(db.String(150), nullable=False)
    message = db.Column(db.Text, nullable=False)
    related_report_id = db.Column(db.Integer, db.ForeignKey("item_reports.id", ondelete="SET NULL"), nullable=True)
    related_claim_id = db.Column(db.Integer, db.ForeignKey("claims.id", ondelete="SET NULL"), nullable=True)
    link = db.Column(db.String(200), nullable=True)
    is_read = db.Column(db.Boolean, default=False, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationship to user
    user = db.relationship("User", foreign_keys=[recipient_user_id], back_populates="notifications")
    related_report = db.relationship("ItemReport", foreign_keys=[related_report_id])
    related_claim = db.relationship("Claim", foreign_keys=[related_claim_id])

    # Backward compatibility property for user_id
    @property
    def user_id(self):
        return self.recipient_user_id

    @user_id.setter
    def user_id(self, val):
        self.recipient_user_id = val

    def to_dict(self):
        return {
            "id": self.id,
            "recipient_user_id": self.recipient_user_id,
            "user_id": self.recipient_user_id,
            "title": self.title,
            "message": self.message,
            "notification_type": self.notification_type,
            "related_report_id": self.related_report_id,
            "related_claim_id": self.related_claim_id,
            "link": self.link,
            "is_read": self.is_read,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

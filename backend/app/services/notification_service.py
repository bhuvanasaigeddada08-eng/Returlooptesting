from app import db
from app.models.notification import Notification
from app.models.user import User
from app.services.email_service import send_notification_email

def create_notification(
    recipient_user_id, 
    title, 
    message, 
    notification_type="system", 
    link=None,
    related_report_id=None,
    related_claim_id=None
):
    """
    Creates an in-app notification in SQLite.
    Also dispatches to optional email notification service if enabled.
    """
    try:
        notif = Notification(
            recipient_user_id=recipient_user_id,
            title=title,
            message=message,
            notification_type=notification_type,
            link=link,
            related_report_id=related_report_id,
            related_claim_id=related_claim_id
        )
        db.session.add(notif)
        db.session.commit()

        # Optional Email Notification (non-blocking fallback)
        user = db.session.get(User, recipient_user_id)
        if user and user.email:
            send_notification_email(
                recipient_email=user.email,
                subject=title,
                message_body=f"Hello {user.display_name},\n\n{message}\n\nView details: {link or 'https://returnloop.lpu.in'}\n\nBest regards,\nReturnLoop LPU Team"
            )

        return notif
    except Exception as e:
        db.session.rollback()
        print(f"Failed to create notification: {e}")
        return None

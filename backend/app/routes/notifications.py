from flask import Blueprint, jsonify, g
from app import db
from app.models.notification import Notification
from app.utils.auth_middleware import login_required

notifications_bp = Blueprint("notifications", __name__)

@notifications_bp.route("", methods=["GET"])
@login_required
def get_user_notifications():
    notifications = Notification.query.filter_by(
        recipient_user_id=g.current_user.id
    ).order_by(Notification.created_at.desc()).limit(50).all()

    unread_count = Notification.query.filter_by(
        recipient_user_id=g.current_user.id,
        is_read=False
    ).count()

    return jsonify({
        "notifications": [n.to_dict() for n in notifications],
        "unread_count": unread_count
    }), 200

@notifications_bp.route("/<int:notif_id>/read", methods=["POST"])
@login_required
def mark_read(notif_id):
    notif = db.session.get(Notification, notif_id)
    if not notif:
        return jsonify({"error": "Notification not found."}), 404

    if notif.recipient_user_id != g.current_user.id:
        return jsonify({"error": "Unauthorized."}), 403

    notif.is_read = True
    db.session.commit()
    return jsonify({"message": "Notification marked as read."}), 200

@notifications_bp.route("/read-all", methods=["POST"])
@login_required
def mark_all_read():
    Notification.query.filter_by(
        recipient_user_id=g.current_user.id,
        is_read=False
    ).update({"is_read": True})
    db.session.commit()
    return jsonify({"message": "All notifications marked as read."}), 200

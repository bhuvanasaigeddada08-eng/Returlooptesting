from datetime import datetime, timezone
from flask import Blueprint, request, jsonify, g
from sqlalchemy import func
from app import db
from app.models.user import User
from app.models.report import ItemReport
from app.models.claim import Claim
from app.models.audit_log import AuditLog
from app.utils.auth_middleware import admin_required
from app.services.audit_service import log_audit_event
from app.services.notification_service import create_notification

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/dashboard", methods=["GET"])
@admin_required
def get_dashboard_metrics():
    total_reports = ItemReport.query.count()
    active_lost = ItemReport.query.filter_by(report_type="lost", status="active").count()
    active_found = ItemReport.query.filter_by(report_type="found", status="active").count()
    pending_claims = Claim.query.filter_by(status="pending").count()
    completed_recoveries = ItemReport.query.filter_by(status="recovered").count()
    suspended_reports = ItemReport.query.filter_by(status="suspended").count()

    # Category breakdown
    categories = db.session.query(
        ItemReport.category, func.count(ItemReport.id)
    ).group_by(ItemReport.category).all()
    category_counts = {cat: count for cat, count in categories}

    # Recent activity
    recent_reports = ItemReport.query.order_by(ItemReport.created_at.desc()).limit(5).all()
    recent_claims = Claim.query.order_by(Claim.created_at.desc()).limit(5).all()
    recent_logs = AuditLog.query.order_by(AuditLog.created_at.desc()).limit(8).all()

    return jsonify({
        "metrics": {
            "total_reports": total_reports,
            "active_lost": active_lost,
            "active_found": active_found,
            "pending_claims": pending_claims,
            "completed_recoveries": completed_recoveries,
            "suspended_reports": suspended_reports
        },
        "category_breakdown": category_counts,
        "recent_reports": [r.to_dict(is_owner_or_admin=True) for r in recent_reports],
        "recent_claims": [c.to_dict(is_claimant_or_admin=True) for c in recent_claims],
        "recent_logs": [log.to_dict() for log in recent_logs]
    }), 200

@admin_bp.route("/reports", methods=["GET"])
@admin_required
def admin_get_reports():
    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 20, type=int), 100)
    status_filter = request.args.get("status", "").strip()
    report_type = request.args.get("type", "").strip()
    category = request.args.get("category", "").strip()
    search = request.args.get("q", "").strip()

    query = ItemReport.query
    if status_filter:
        query = query.filter_by(status=status_filter)
    if report_type:
        query = query.filter_by(report_type=report_type)
    if category:
        query = query.filter_by(category=category)
    if search:
        pattern = f"%{search}%"
        query = query.filter(
            ItemReport.title.ilike(pattern) | 
            ItemReport.reference_code.ilike(pattern) | 
            ItemReport.general_location.ilike(pattern)
        )

    pagination = query.order_by(ItemReport.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "reports": [r.to_dict(is_owner_or_admin=True) for r in pagination.items],
        "total": pagination.total,
        "page": pagination.page,
        "pages": pagination.pages
    }), 200

@admin_bp.route("/reports/<int:report_id>/status", methods=["PATCH"])
@admin_required
def update_report_status(report_id):
    report = db.session.get(ItemReport, report_id)
    if not report:
        return jsonify({"error": "Item report not found."}), 404

    data = request.get_json() or {}
    new_status = data.get("status", "").strip()
    reason = data.get("reason", "").strip()

    valid_statuses = ["active", "claim_pending", "recovered", "withdrawn", "suspended"]
    if new_status not in valid_statuses:
        return jsonify({"error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"}), 400

    old_status = report.status
    report.status = new_status
    db.session.commit()

    log_audit_event(
        "ADMIN_STATUS_CHANGE",
        "ItemReport",
        report.id,
        actor_id=g.current_user.id,
        details={"old_status": old_status, "new_status": new_status, "reason": reason}
    )

    create_notification(
        recipient_user_id=report.user_id,
        title="Report Status Updated by Administrator",
        message=f"Your report '{report.title}' status was changed from {old_status} to {new_status}. {f'Reason: {reason}' if reason else ''}",
        notification_type="admin_message",
        link=f"/items/{report.id}",
        related_report_id=report.id
    )

    return jsonify({
        "message": f"Report status changed to {new_status}.",
        "report": report.to_dict(is_owner_or_admin=True)
    }), 200

@admin_bp.route("/claims", methods=["GET"])
@admin_required
def admin_get_claims():
    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 20, type=int), 100)
    status_filter = request.args.get("status", "").strip()

    query = Claim.query
    if status_filter:
        query = query.filter_by(status=status_filter)

    pagination = query.order_by(Claim.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "claims": [c.to_dict(is_claimant_or_admin=True) for c in pagination.items],
        "total": pagination.total,
        "page": pagination.page,
        "pages": pagination.pages
    }), 200

@admin_bp.route("/claims/<int:claim_id>/approve", methods=["POST"])
@admin_required
def approve_claim(claim_id):
    claim = db.session.get(Claim, claim_id)
    if not claim:
        return jsonify({"error": "Claim not found."}), 404

    data = request.get_json() or {}
    reason = data.get("reason", "").strip() or "Ownership proof verified against item attributes."

    claim.status = "approved"
    claim.administrator_reason = reason
    claim.reviewed_by_id = g.current_user.id
    claim.reviewed_at = datetime.now(timezone.utc)

    db.session.commit()

    log_audit_event(
        "CLAIM_APPROVED",
        "Claim",
        claim.id,
        actor_id=g.current_user.id,
        details={"reason": reason, "reference_code": claim.reference_code}
    )

    create_notification(
        recipient_user_id=claim.claimant_user_id,
        title="Claim Approved!",
        message=f"Your claim {claim.reference_code} for '{claim.item_report.title}' has been APPROVED! Please visit Campus Security (Block 34 Helpdesk) with your Student ID for verification and physical handover.",
        notification_type="claim_update",
        link=f"/claims/{claim.id}",
        related_report_id=claim.item_report_id,
        related_claim_id=claim.id
    )

    return jsonify({
        "message": "Claim approved. The student has been notified to proceed with handover verification.",
        "claim": claim.to_dict(is_claimant_or_admin=True)
    }), 200

@admin_bp.route("/claims/<int:claim_id>/reject", methods=["POST"])
@admin_required
def reject_claim(claim_id):
    claim = db.session.get(Claim, claim_id)
    if not claim:
        return jsonify({"error": "Claim not found."}), 404

    data = request.get_json() or {}
    reason = data.get("reason", "").strip()
    if not reason:
        return jsonify({"error": "A clear reason must be provided when rejecting a claim."}), 400

    claim.status = "rejected"
    claim.administrator_reason = reason
    claim.reviewed_by_id = g.current_user.id
    claim.reviewed_at = datetime.now(timezone.utc)

    # Check if there are other pending claims on this item
    remaining_pending = Claim.query.filter(
        Claim.item_report_id == claim.item_report_id,
        Claim.id != claim.id,
        Claim.status == "pending"
    ).count()

    if remaining_pending == 0 and claim.item_report.status == "claim_pending":
        claim.item_report.status = "active"

    db.session.commit()

    log_audit_event(
        "CLAIM_REJECTED",
        "Claim",
        claim.id,
        actor_id=g.current_user.id,
        details={"reason": reason, "reference_code": claim.reference_code}
    )

    create_notification(
        recipient_user_id=claim.claimant_user_id,
        title="Claim Not Approved",
        message=f"Your claim {claim.reference_code} for '{claim.item_report.title}' was not approved. Reason: {reason}",
        notification_type="claim_update",
        link=f"/claims/{claim.id}",
        related_report_id=claim.item_report_id,
        related_claim_id=claim.id
    )

    return jsonify({
        "message": "Claim rejected and reason logged.",
        "claim": claim.to_dict(is_claimant_or_admin=True)
    }), 200

@admin_bp.route("/claims/<int:claim_id>/request-information", methods=["POST"])
@admin_required
def request_more_information(claim_id):
    claim = db.session.get(Claim, claim_id)
    if not claim:
        return jsonify({"error": "Claim not found."}), 404

    data = request.get_json() or {}
    message = data.get("message", "").strip()
    if not message:
        return jsonify({"error": "Please provide specific details on what additional information is required."}), 400

    claim.status = "more_info_needed"
    claim.administrator_reason = message
    claim.reviewed_by_id = g.current_user.id
    claim.reviewed_at = datetime.now(timezone.utc)

    db.session.commit()

    log_audit_event(
        "CLAIM_INFO_REQUESTED",
        "Claim",
        claim.id,
        actor_id=g.current_user.id,
        details={"message": message, "reference_code": claim.reference_code}
    )

    create_notification(
        recipient_user_id=claim.claimant_user_id,
        title="Additional Information Needed for Claim",
        message=f"Campus Security requested more proof for claim {claim.reference_code}: {message}",
        notification_type="info_requested",
        link=f"/claims/{claim.id}",
        related_report_id=claim.item_report_id,
        related_claim_id=claim.id
    )

    return jsonify({
        "message": "Information request sent to student.",
        "claim": claim.to_dict(is_claimant_or_admin=True)
    }), 200

@admin_bp.route("/claims/<int:claim_id>/handover", methods=["POST"])
@admin_required
def record_handover(claim_id):
    claim = db.session.get(Claim, claim_id)
    if not claim:
        return jsonify({"error": "Claim not found."}), 404

    if claim.status not in ["approved", "pending"]:
        return jsonify({"error": f"Cannot complete handover for a claim with status '{claim.status}'."}), 400

    data = request.get_json() or {}
    handover_notes = data.get("notes", "").strip()
    if not handover_notes:
        return jsonify({"error": "Handover notes (e.g. Student ID verified, physical signature collected) are required."}), 400

    now = datetime.now(timezone.utc)
    claim.status = "handover_completed"
    claim.handover_at = now
    claim.handover_admin_id = g.current_user.id
    claim.handover_notes = handover_notes

    # Update item report status to recovered
    report = claim.item_report
    report.status = "recovered"

    # Reject any other pending claims for this item
    other_claims = Claim.query.filter(
        Claim.item_report_id == report.id,
        Claim.id != claim.id,
        Claim.status.in_(["pending", "more_info_needed"])
    ).all()

    for oc in other_claims:
        oc.status = "rejected"
        oc.administrator_reason = "Item has already been verified and handed over to another verified claimant."
        create_notification(
            recipient_user_id=oc.claimant_user_id,
            title="Claim Closed",
            message=f"Item '{report.title}' has been successfully handed over to its verified owner.",
            notification_type="claim_update",
            link=f"/claims/{oc.id}",
            related_report_id=report.id,
            related_claim_id=oc.id
        )

    db.session.commit()

    log_audit_event(
        "HANDOVER_COMPLETED",
        "Claim",
        claim.id,
        actor_id=g.current_user.id,
        details={
            "item_id": report.id,
            "claimant_id": claim.claimant_user_id,
            "notes": handover_notes
        }
    )

    create_notification(
        recipient_user_id=claim.claimant_user_id,
        title="Belonging Handover Completed!",
        message=f"Your handover for '{report.title}' has been recorded and the case is now safely resolved. Thank you for using ReturnLoop LPU!",
        notification_type="handover",
        link=f"/claims/{claim.id}",
        related_report_id=report.id,
        related_claim_id=claim.id
    )

    # Also notify reporter if someone else found it
    if report.user_id != claim.claimant_user_id:
        create_notification(
            recipient_user_id=report.user_id,
            title="Found Item Successfully Handed Over",
            message=f"The item '{report.title}' you reported finding has been verified and returned to its rightful owner. Thank you for your honesty!",
            notification_type="system",
            link=f"/items/{report.id}",
            related_report_id=report.id,
            related_claim_id=claim.id
        )

    return jsonify({
        "message": "Physical handover successfully recorded. Case marked as recovered.",
        "claim": claim.to_dict(is_claimant_or_admin=True)
    }), 200

@admin_bp.route("/audit-logs", methods=["GET"])
@admin_required
def get_audit_logs():
    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 25, type=int), 100)

    pagination = AuditLog.query.order_by(AuditLog.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "logs": [log.to_dict() for log in pagination.items],
        "total": pagination.total,
        "page": pagination.page,
        "pages": pagination.pages
    }), 200

# =========================================================================
# User Account Management (Admin Full Control)
# =========================================================================

@admin_bp.route("/users", methods=["GET"])
@admin_required
def get_admin_users():
    q = request.args.get("q", "").strip()
    role = request.args.get("role", "").strip()
    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 20, type=int), 100)

    query = User.query
    if role in ("student", "admin"):
        query = query.filter(User.role == role)
    if q:
        query = query.filter(
            db.or_(
                User.display_name.ilike(f"%{q}%"),
                User.email.ilike(f"%{q}%"),
                User.phone.ilike(f"%{q}%")
            )
        )

    pagination = query.order_by(User.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)

    users_data = []
    for u in pagination.items:
        d = u.to_dict()
        d["reports_count"] = ItemReport.query.filter_by(user_id=u.id).count()
        d["claims_count"] = Claim.query.filter_by(claimant_user_id=u.id).count()
        users_data.append(d)

    return jsonify({
        "users": users_data,
        "total": pagination.total,
        "page": pagination.page,
        "pages": pagination.pages
    }), 200

@admin_bp.route("/users", methods=["POST"])
@admin_required
def create_admin_user():
    data = request.get_json() or {}
    email = data.get("email", "").strip().lower()
    display_name = data.get("display_name", "").strip()
    password = data.get("password", "")
    role = data.get("role", "student")
    phone = data.get("phone", "").strip()

    if not email or "@" not in email:
        return jsonify({"error": "Valid email address is required."}), 400
    if not display_name:
        return jsonify({"error": "Full name is required."}), 400
    if not password or len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters."}), 400
    if role not in ("student", "admin"):
        role = "student"

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "An account with this email already exists."}), 409

    new_user = User(
        email=email,
        display_name=display_name,
        phone=phone or None,
        role=role,
        is_active=True
    )
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    log_audit_event(
        actor_user_id=g.current_user.id,
        action="admin_create_user",
        target_type="User",
        target_id=new_user.id,
        details={"created_email": email, "role": role, "name": display_name}
    )

    return jsonify({
        "message": f"Account for {display_name} created successfully.",
        "user": new_user.to_dict()
    }), 201

@admin_bp.route("/users/<int:user_id>", methods=["PUT", "PATCH"])
@admin_required
def update_admin_user(user_id):
    target_user = db.session.get(User, user_id)
    if not target_user:
        return jsonify({"error": "User not found."}), 404

    data = request.get_json() or {}
    if "email" in data:
        new_email = data["email"].strip().lower()
        if new_email != target_user.email:
            if User.query.filter_by(email=new_email).first():
                return jsonify({"error": "Email is already taken by another user."}), 409
            target_user.email = new_email

    if "display_name" in data and data["display_name"].strip():
        target_user.display_name = data["display_name"].strip()

    if "phone" in data:
        target_user.phone = data["phone"].strip() or None

    if "role" in data and data["role"] in ("student", "admin"):
        if target_user.id == g.current_user.id and data["role"] != "admin":
            return jsonify({"error": "You cannot demote your own active admin account."}), 400
        target_user.role = data["role"]

    if "is_active" in data:
        if target_user.id == g.current_user.id and not data["is_active"]:
            return jsonify({"error": "You cannot deactivate your own active admin account."}), 400
        target_user.is_active = bool(data["is_active"])

    if "password" in data and data["password"]:
        if len(data["password"]) < 6:
            return jsonify({"error": "Password must be at least 6 characters."}), 400
        target_user.set_password(data["password"])

    db.session.commit()

    log_audit_event(
        actor_user_id=g.current_user.id,
        action="admin_update_user",
        target_type="User",
        target_id=target_user.id,
        details={"updated_email": target_user.email, "role": target_user.role, "name": target_user.display_name}
    )

    return jsonify({
        "message": "User account updated successfully.",
        "user": target_user.to_dict()
    }), 200

@admin_bp.route("/users/<int:user_id>", methods=["DELETE"])
@admin_required
def delete_admin_user(user_id):
    if user_id == g.current_user.id:
        return jsonify({"error": "You cannot delete your own admin account."}), 400

    target_user = db.session.get(User, user_id)
    if not target_user:
        return jsonify({"error": "User not found."}), 404

    user_name = target_user.display_name
    user_email = target_user.email

    AuditLog.query.filter_by(actor_user_id=user_id).update({"actor_user_id": None})
    
    db.session.delete(target_user)
    db.session.commit()

    log_audit_event(
        actor_user_id=g.current_user.id,
        action="admin_delete_user",
        target_type="User",
        target_id=user_id,
        details={"deleted_email": user_email, "name": user_name}
    )

    return jsonify({
        "message": f"Account for {user_name} ({user_email}) has been permanently removed."
    }), 200

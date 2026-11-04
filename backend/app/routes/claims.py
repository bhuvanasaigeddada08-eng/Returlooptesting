from flask import Blueprint, request, jsonify, g
from app import db
from app.models.claim import Claim
from app.models.report import ItemReport
from app.models.user import User
from app.utils.auth_middleware import login_required
from app.utils.validators import validate_claim
from app.services.audit_service import log_audit_event
from app.services.notification_service import create_notification

claims_bp = Blueprint("claims", __name__)

@claims_bp.route("/<int:report_id>", methods=["POST"])
@login_required
def submit_claim(report_id):
    report = db.session.get(ItemReport, report_id)
    if not report:
        return jsonify({"error": "Item report not found."}), 404

    if report.report_type != "found":
        return jsonify({"error": "Claims can only be filed against 'found' item reports."}), 400

    if report.status in ["recovered", "withdrawn", "suspended"]:
        return jsonify({"error": f"Cannot submit a claim for an item marked as {report.status}."}), 400

    if report.user_id == g.current_user.id:
        return jsonify({"error": "You cannot submit a claim for an item you reported as found."}), 400

    # Prevent duplicate active claims by same user for same item
    existing = Claim.query.filter_by(
        item_report_id=report.id,
        claimant_user_id=g.current_user.id
    ).filter(Claim.status.in_(["pending", "approved"])).first()

    if existing:
        return jsonify({
            "error": "You already have an active claim submitted for this item.",
            "claim_reference": existing.reference_code,
            "status": existing.status
        }), 409

    data = request.get_json() or {}
    errors = validate_claim(data)
    if errors:
        return jsonify({"errors": errors}), 400

    claim = Claim(
        reference_code=Claim.generate_reference_code(),
        item_report_id=report.id,
        claimant_user_id=g.current_user.id,
        private_ownership_explanation=data["private_ownership_explanation"].strip(),
        status="pending"
    )

    # Update item status to indicate claim in progress
    if report.status == "active":
        report.status = "claim_pending"

    db.session.add(claim)
    db.session.commit()

    log_audit_event("CLAIM_SUBMITTED", "Claim", claim.id, actor_id=g.current_user.id, details={"reference_code": claim.reference_code, "item_id": report.id})

    # Notify student
    create_notification(
        recipient_user_id=g.current_user.id,
        title="Claim Submitted",
        message=f"Your claim ({claim.reference_code}) for '{report.title}' has been received and is queued for verification.",
        notification_type="claim_update",
        link=f"/claims/{claim.id}",
        related_report_id=report.id,
        related_claim_id=claim.id
    )

    # Notify admins
    admins = User.query.filter_by(role="admin").all()
    for admin in admins:
        create_notification(
            recipient_user_id=admin.id,
            title="New Claim Awaiting Review",
            message=f"Student {g.current_user.display_name} submitted claim {claim.reference_code} for item '{report.title}'.",
            notification_type="admin_message",
            link="/admin/claims",
            related_report_id=report.id,
            related_claim_id=claim.id
        )

    return jsonify({
        "message": "Claim submitted successfully. Campus security/admin will review your proof.",
        "claim": claim.to_dict(is_claimant_or_admin=True)
    }), 201

@claims_bp.route("/my", methods=["GET"])
@login_required
def get_my_claims():
    claims = Claim.query.filter_by(
        claimant_user_id=g.current_user.id
    ).order_by(Claim.created_at.desc()).all()

    return jsonify({
        "claims": [c.to_dict(is_claimant_or_admin=True) for c in claims]
    }), 200

@claims_bp.route("/<int:claim_id>", methods=["GET"])
@login_required
def get_claim_details(claim_id):
    claim = db.session.get(Claim, claim_id)
    if not claim:
        return jsonify({"error": "Claim not found."}), 404

    is_claimant = claim.claimant_user_id == g.current_user.id
    is_admin = g.current_user.role == "admin"

    if not is_claimant and not is_admin:
        return jsonify({"error": "Unauthorized access to private claim details."}), 403

    return jsonify({
        "claim": claim.to_dict(is_claimant_or_admin=True),
        "item": claim.item_report.to_dict(is_owner_or_admin=is_admin)
    }), 200

@claims_bp.route("/<int:claim_id>/withdraw", methods=["POST"])
@login_required
def withdraw_claim(claim_id):
    claim = db.session.get(Claim, claim_id)
    if not claim:
        return jsonify({"error": "Claim not found."}), 404

    is_claimant = claim.claimant_user_id == g.current_user.id
    is_admin = g.current_user.role == "admin"

    if not is_claimant and not is_admin:
        return jsonify({"error": "Unauthorized to withdraw this claim."}), 403

    if claim.status in ["handover_completed", "rejected"]:
        return jsonify({"error": f"Cannot withdraw a claim that is {claim.status}."}), 400

    claim.status = "withdrawn"
    
    # Check if report still has other active/pending claims
    other_claims = Claim.query.filter(
        Claim.item_report_id == claim.item_report_id,
        Claim.id != claim.id,
        Claim.status == "pending"
    ).count()

    if other_claims == 0 and claim.item_report.status == "claim_pending":
        claim.item_report.status = "active"

    db.session.commit()
    log_audit_event("CLAIM_WITHDRAWN", "Claim", claim.id, actor_id=g.current_user.id)

    return jsonify({
        "message": "Claim withdrawn successfully.",
        "claim": claim.to_dict(is_claimant_or_admin=True)
    }), 200

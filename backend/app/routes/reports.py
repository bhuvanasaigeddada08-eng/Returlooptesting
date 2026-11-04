from flask import Blueprint, request, jsonify, g
from sqlalchemy import or_
from app import db
from app.models.report import ItemReport, ItemImage
from app.utils.auth_middleware import login_required, optional_auth
from app.utils.validators import validate_report
from app.utils.file_upload import save_uploaded_image
from app.services.audit_service import log_audit_event
from app.services.match_service import find_matches_for_report
from app.services.notification_service import create_notification

reports_bp = Blueprint("reports", __name__)

@reports_bp.route("", methods=["GET"])
@optional_auth
def get_reports():
    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 12, type=int), 50)
    query_str = request.args.get("q", "").strip()
    category = request.args.get("category", "").strip()
    report_type = request.args.get("type", "").strip()  # 'lost' or 'found'
    location = request.args.get("location", "").strip()
    status_filter = request.args.get("status", "").strip()
    sort_by = request.args.get("sort", "newest")

    query = ItemReport.query

    # Guests and students only see non-suspended and non-withdrawn items in public explore
    is_admin = g.current_user and g.current_user.role == "admin"
    if not is_admin:
        if status_filter:
            query = query.filter(ItemReport.status == status_filter)
        else:
            query = query.filter(ItemReport.status.in_(["active", "claim_pending", "recovered"]))
    elif status_filter:
        query = query.filter(ItemReport.status == status_filter)

    if report_type in ["lost", "found"]:
        query = query.filter(ItemReport.report_type == report_type)

    if category:
        query = query.filter(ItemReport.category == category)

    if location:
        query = query.filter(ItemReport.general_location.ilike(f"%{location}%"))

    if query_str:
        pattern = f"%{query_str}%"
        query = query.filter(
            or_(
                ItemReport.title.ilike(pattern),
                ItemReport.description.ilike(pattern),
                ItemReport.color.ilike(pattern),
                ItemReport.brand.ilike(pattern),
                ItemReport.reference_code.ilike(pattern)
            )
        )

    if sort_by == "oldest":
        query = query.order_by(ItemReport.created_at.asc())
    else:
        query = query.order_by(ItemReport.created_at.desc())

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "reports": [
            r.to_dict(is_owner_or_admin=(g.current_user and (g.current_user.id == r.user_id or is_admin)))
            for r in pagination.items
        ],
        "total": pagination.total,
        "page": pagination.page,
        "pages": pagination.pages,
        "per_page": pagination.per_page
    }), 200

@reports_bp.route("/my", methods=["GET"])
@login_required
def get_my_reports():
    report_type = request.args.get("type", "").strip()
    query = ItemReport.query.filter_by(user_id=g.current_user.id)
    if report_type in ["lost", "found"]:
        query = query.filter_by(report_type=report_type)
    
    reports = query.order_by(ItemReport.created_at.desc()).all()
    return jsonify({
        "reports": [r.to_dict(is_owner_or_admin=True) for r in reports]
    }), 200

@reports_bp.route("", methods=["POST"])
@login_required
def create_report():
    data = request.get_json() or {}
    errors = validate_report(data)
    if errors:
        return jsonify({"errors": errors}), 400

    report_type = data["report_type"].strip()
    ref_code = ItemReport.generate_reference_code(report_type)

    report = ItemReport(
        reference_code=ref_code,
        user_id=g.current_user.id,
        report_type=report_type,
        title=data["title"].strip(),
        category=data["category"].strip(),
        description=data["description"].strip(),
        color=data["color"].strip(),
        brand=data.get("brand", "").strip() or None,
        general_location=data["general_location"].strip(),
        event_date=data["event_date"].strip(),
        identifying_characteristics=data.get("identifying_characteristics", "").strip() or None,
        safe_handover_instructions=data.get("safe_handover_instructions", "").strip() or None,
        status="active"
    )

    db.session.add(report)
    db.session.commit()

    log_audit_event("REPORT_CREATED", "ItemReport", report.id, actor_id=g.current_user.id, details={"reference_code": ref_code})

    # Check for immediate potential matches and notify user
    matches = find_matches_for_report(report, limit=3)
    if matches and matches[0]["match_score"] >= 60.0:
        create_notification(
            recipient_user_id=g.current_user.id,
            title="Potential Match Found!",
            message=f"We found a potential match for your {report.report_type} item '{report.title}' with a {matches[0]['match_score']}% confidence score.",
            notification_type="match",
            link=f"/items/{report.id}",
            related_report_id=report.id
        )

    return jsonify({
        "message": f"{report_type.capitalize()} report submitted successfully.",
        "report": report.to_dict(is_owner_or_admin=True)
    }), 201

@reports_bp.route("/<int:report_id>", methods=["GET"])
@optional_auth
def get_report(report_id):
    report = db.session.get(ItemReport, report_id)
    if not report:
        return jsonify({"error": "Item report not found."}), 404

    is_owner_or_admin = g.current_user and (
        g.current_user.id == report.user_id or g.current_user.role == "admin"
    )

    # If item is suspended and user is neither owner nor admin, hide it
    if report.status == "suspended" and not is_owner_or_admin:
        return jsonify({"error": "This listing is currently suspended or unavailable."}), 404

    return jsonify({"report": report.to_dict(is_owner_or_admin=is_owner_or_admin)}), 200

@reports_bp.route("/<int:report_id>", methods=["PATCH"])
@login_required
def update_report(report_id):
    report = db.session.get(ItemReport, report_id)
    if not report:
        return jsonify({"error": "Item report not found."}), 404

    is_admin = g.current_user.role == "admin"
    if report.user_id != g.current_user.id and not is_admin:
        return jsonify({"error": "You do not have permission to edit this report."}), 403

    data = request.get_json() or {}
    updatable_fields = [
        "title", "category", "description", "color", "brand", 
        "general_location", "event_date", "identifying_characteristics", 
        "safe_handover_instructions"
    ]

    for field in updatable_fields:
        if field in data:
            setattr(report, field, data[field].strip() if isinstance(data[field], str) else data[field])

    db.session.commit()
    log_audit_event("REPORT_UPDATED", "ItemReport", report.id, actor_id=g.current_user.id)

    return jsonify({
        "message": "Report updated successfully.",
        "report": report.to_dict(is_owner_or_admin=True)
    }), 200

@reports_bp.route("/<int:report_id>/recover", methods=["POST"])
@login_required
def recover_report(report_id):
    report = db.session.get(ItemReport, report_id)
    if not report:
        return jsonify({"error": "Item report not found."}), 404

    is_admin = g.current_user.role == "admin"
    if report.user_id != g.current_user.id and not is_admin:
        return jsonify({"error": "You do not have permission to update this report status."}), 403

    if report.status in ["recovered", "withdrawn"]:
        return jsonify({"error": f"Report is already {report.status}."}), 400

    report.status = "recovered"
    db.session.commit()

    log_audit_event("REPORT_MARKED_RECOVERED", "ItemReport", report.id, actor_id=g.current_user.id)
    create_notification(
        recipient_user_id=report.user_id,
        title="Item Marked as Recovered",
        message=f"Your {report.report_type} report for '{report.title}' has been marked as recovered.",
        notification_type="system",
        link=f"/items/{report.id}",
        related_report_id=report.id
    )

    return jsonify({
        "message": "Item report successfully marked as recovered.",
        "report": report.to_dict(is_owner_or_admin=True)
    }), 200

@reports_bp.route("/<int:report_id>/withdraw", methods=["POST"])
@login_required
def withdraw_report(report_id):
    report = db.session.get(ItemReport, report_id)
    if not report:
        return jsonify({"error": "Item report not found."}), 404

    is_admin = g.current_user.role == "admin"
    if report.user_id != g.current_user.id and not is_admin:
        return jsonify({"error": "You do not have permission to withdraw this report."}), 403

    report.status = "withdrawn"
    db.session.commit()

    log_audit_event("REPORT_WITHDRAWN", "ItemReport", report.id, actor_id=g.current_user.id)
    return jsonify({
        "message": "Report has been withdrawn.",
        "report": report.to_dict(is_owner_or_admin=True)
    }), 200

@reports_bp.route("/<int:report_id>/images", methods=["POST"])
@login_required
def upload_report_image(report_id):
    report = db.session.get(ItemReport, report_id)
    if not report:
        return jsonify({"error": "Item report not found."}), 404

    is_admin = g.current_user.role == "admin"
    if report.user_id != g.current_user.id and not is_admin:
        return jsonify({"error": "You do not have permission to add images to this report."}), 403

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded."}), 400

    file = request.files["file"]
    res, err = save_uploaded_image(file)
    if err:
        return jsonify({"error": err}), 400

    web_path, filename = res
    is_first = len(report.images) == 0

    image = ItemImage(
        item_report_id=report.id,
        file_path=web_path,
        file_name=filename,
        is_primary=is_first
    )
    db.session.add(image)
    db.session.commit()

    return jsonify({
        "message": "Image uploaded successfully.",
        "image": image.to_dict()
    }), 201

@reports_bp.route("/images/<int:image_id>", methods=["DELETE"])
@login_required
def delete_report_image(image_id):
    image = db.session.get(ItemImage, image_id)
    if not image:
        return jsonify({"error": "Image not found."}), 404

    report = image.item_report
    is_admin = g.current_user.role == "admin"
    if report.user_id != g.current_user.id and not is_admin:
        return jsonify({"error": "You do not have permission to remove this image."}), 403

    db.session.delete(image)
    db.session.commit()

    return jsonify({"message": "Image deleted successfully."}), 200

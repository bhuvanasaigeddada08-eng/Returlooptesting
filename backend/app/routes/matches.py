from flask import Blueprint, jsonify, request
from app.models.report import ItemReport
from app.services.match_service import find_matches_for_report
from app.utils.auth_middleware import optional_auth

matches_bp = Blueprint("matches", __name__)

@matches_bp.route("/<int:report_id>", methods=["GET"])
@optional_auth
def get_matches(report_id):
    report = ItemReport.query.get(report_id)
    if not report:
        return jsonify({"error": "Item report not found."}), 404

    limit = request.args.get("limit", 10, type=int)
    matches = find_matches_for_report(report, limit=limit)

    return jsonify({
        "target_report": {
            "id": report.id,
            "title": report.title,
            "report_type": report.report_type,
            "category": report.category,
            "reference_code": report.reference_code
        },
        "matches": matches,
        "count": len(matches)
    }), 200

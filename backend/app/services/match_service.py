import re
from datetime import datetime
from app.models.report import ItemReport

STOP_WORDS = {
    "a", "an", "the", "in", "on", "at", "by", "for", "with", "about", 
    "against", "between", "into", "through", "during", "before", "after",
    "above", "below", "to", "from", "up", "down", "is", "was", "are", 
    "were", "be", "been", "being", "have", "has", "had", "having", "do", 
    "does", "did", "doing", "and", "but", "if", "or", "because", "as", 
    "until", "while", "of", "it", "its", "my", "lost", "found", "item", "please"
}

def extract_keywords(text):
    if not text:
        return set()
    words = re.findall(r"\b[a-zA-Z0-9]{3,}\b", text.lower())
    return {w for w in words if w not in STOP_WORDS}

def calculate_match_score(lost_report, found_report):
    """
    Transparent weighted matching algorithm:
    1. Category Match (Weight: 35%)
    2. Keywords in Title and Description (Weight: 25%)
    3. Color Compatibility (Weight: 15%)
    4. Campus Location Proximity (Weight: 15%)
    5. Date Proximity (Weight: 10%)
    Total maximum score: 100%
    """
    breakdown = {}
    total_score = 0.0

    # 1. Category (35%)
    if lost_report.category.lower() == found_report.category.lower():
        category_score = 35.0
        breakdown["category"] = {
            "score": category_score,
            "max": 35.0,
            "detail": f"Exact category match ({lost_report.category})"
        }
    else:
        category_score = 0.0
        breakdown["category"] = {
            "score": 0.0,
            "max": 35.0,
            "detail": f"Different categories ({lost_report.category} vs {found_report.category})"
        }
    total_score += category_score

    # 2. Keywords in Title and Description (25%)
    lost_keywords = extract_keywords(f"{lost_report.title} {lost_report.description} {lost_report.brand or ''}")
    found_keywords = extract_keywords(f"{found_report.title} {found_report.description} {found_report.brand or ''}")

    common_keywords = lost_keywords.intersection(found_keywords)
    if lost_keywords and found_keywords:
        # Jaccard / overlap fraction
        overlap_ratio = len(common_keywords) / max(1, min(len(lost_keywords), len(found_keywords)))
        keyword_score = round(min(25.0, overlap_ratio * 25.0), 1)
    else:
        keyword_score = 0.0

    breakdown["keywords"] = {
        "score": keyword_score,
        "max": 25.0,
        "common_terms": list(common_keywords)[:5],
        "detail": f"{len(common_keywords)} matching keyword(s): {', '.join(list(common_keywords)[:3]) if common_keywords else 'None'}"
    }
    total_score += keyword_score

    # 3. Color Compatibility (15%)
    lost_color = lost_report.color.strip().lower()
    found_color = found_report.color.strip().lower()

    if lost_color == found_color:
        color_score = 15.0
        color_detail = f"Identical color reported ({lost_report.color})"
    elif lost_color in found_color or found_color in lost_color:
        color_score = 10.0
        color_detail = f"Partial color match ({lost_report.color} ~ {found_report.color})"
    else:
        color_score = 0.0
        color_detail = f"Different colors ({lost_report.color} vs {found_report.color})"

    breakdown["color"] = {
        "score": color_score,
        "max": 15.0,
        "detail": color_detail
    }
    total_score += color_score

    # 4. Campus Location Proximity (15%)
    lost_loc = lost_report.general_location.strip().lower()
    found_loc = found_report.general_location.strip().lower()

    if lost_loc == found_loc:
        location_score = 15.0
        loc_detail = f"Exact campus location match ({lost_report.general_location})"
    elif any(block in lost_loc and block in found_loc for block in ["block", "library", "unimall", "hostel", "food"]):
        location_score = 8.0
        loc_detail = f"Related campus zone or shared facility ({lost_report.general_location} ~ {found_report.general_location})"
    else:
        location_score = 0.0
        loc_detail = f"Different campus locations ({lost_report.general_location} vs {found_report.general_location})"

    breakdown["location"] = {
        "score": location_score,
        "max": 15.0,
        "detail": loc_detail
    }
    total_score += location_score

    # 5. Date Proximity (10%)
    try:
        lost_dt = datetime.strptime(lost_report.event_date, "%Y-%m-%d").date()
        found_dt = datetime.strptime(found_report.event_date, "%Y-%m-%d").date()
        diff_days = abs((found_dt - lost_dt).days)

        if diff_days <= 1:
            date_score = 10.0
            date_detail = f"Dates are within 24 hours ({diff_days} day difference)"
        elif diff_days <= 3:
            date_score = 8.0
            date_detail = f"Dates are within 3 days ({diff_days} days difference)"
        elif diff_days <= 7:
            date_score = 5.0
            date_detail = f"Dates are within 1 week ({diff_days} days difference)"
        elif diff_days <= 14:
            date_score = 2.0
            date_detail = f"Dates are within 2 weeks ({diff_days} days difference)"
        else:
            date_score = 0.0
            date_detail = f"Dates are {diff_days} days apart"
    except Exception:
        date_score = 0.0
        date_detail = "Date proximity could not be evaluated"

    breakdown["date"] = {
        "score": date_score,
        "max": 10.0,
        "detail": date_detail
    }
    total_score += date_score

    final_score = round(total_score, 1)

    return {
        "match_score": final_score,
        "is_potential_match": final_score >= 35.0,  # Minimum confidence threshold
        "breakdown": breakdown,
        "disclaimer": "This score is an algorithmic heuristic suggestion based on reported item traits, not verified proof of ownership."
    }

def find_matches_for_report(target_report, limit=10):
    """
    If target is 'lost', search across active 'found' reports.
    If target is 'found', search across active 'lost' reports.
    """
    opposite_type = "found" if target_report.report_type == "lost" else "lost"
    
    candidates = ItemReport.query.filter(
        ItemReport.report_type == opposite_type,
        ItemReport.status.in_(["active", "claim_pending"]),
        ItemReport.id != target_report.id
    ).all()

    matches = []
    for candidate in candidates:
        result = calculate_match_score(
            lost_report=target_report if target_report.report_type == "lost" else candidate,
            found_report=candidate if target_report.report_type == "lost" else target_report
        )
        if result["match_score"] >= 25.0:  # Include meaningful partial matches
            matches.append({
                "item": candidate.to_dict(is_owner_or_admin=False),
                "match_score": result["match_score"],
                "breakdown": result["breakdown"],
                "disclaimer": result["disclaimer"]
            })

    # Sort descending by match score
    matches.sort(key=lambda x: x["match_score"], reverse=True)
    return matches[:limit]

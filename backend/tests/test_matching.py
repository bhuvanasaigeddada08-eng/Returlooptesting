from app import db
from app.models.report import ItemReport
from app.services.match_service import calculate_match_score, find_matches_for_report

def test_matching_algorithm_high_match(app):
    with app.app_context():
        lost = ItemReport(
            reference_code="RL-LOST-TEST-1",
            user_id=1,
            report_type="lost",
            title="Apple iPad Air Silver with Pencil",
            category="Electronics",
            description="Silver iPad Air 11-inch with magnetic stylus left in Central Library 2nd floor.",
            color="Silver",
            brand="Apple",
            general_location="Central Library",
            event_date="2026-10-21"
        )
        found = ItemReport(
            reference_code="RL-FND-TEST-1",
            user_id=2,
            report_type="found",
            title="Silver Apple iPad Tablet with Pen",
            category="Electronics",
            description="Found Apple iPad in Central Library study carrel.",
            color="Silver",
            brand="Apple",
            general_location="Central Library",
            event_date="2026-10-21"
        )
        
        result = calculate_match_score(lost, found)
        assert result["match_score"] >= 75.0
        assert result["breakdown"]["category"]["score"] == 35.0
        assert result["breakdown"]["color"]["score"] == 15.0
        assert result["breakdown"]["location"]["score"] == 15.0
        assert result["breakdown"]["date"]["score"] == 10.0
        assert "disclaimer" in result

def test_matching_different_categories(app):
    with app.app_context():
        lost = ItemReport(
            reference_code="RL-LOST-TEST-2",
            user_id=1,
            report_type="lost",
            title="Milton Black Water Bottle",
            category="Bottles & Tumblers",
            description="Black water flask.",
            color="Black",
            general_location="UniMall",
            event_date="2026-10-20"
        )
        found = ItemReport(
            reference_code="RL-FND-TEST-2",
            user_id=2,
            report_type="found",
            title="Black Dell Laptop Charger",
            category="Electronics",
            description="Charger left at UniMall food court.",
            color="Black",
            general_location="UniMall",
            event_date="2026-10-20"
        )

        result = calculate_match_score(lost, found)
        # Category score must be 0
        assert result["breakdown"]["category"]["score"] == 0.0
        # Total match should be at or below 45.0 (since 35 category points are lost)
        assert result["match_score"] <= 45.0

from app import db
from app.models.notification import Notification
from app.models.user import User
from app.models.report import ItemReport
from app.models.claim import Claim
from app.services.notification_service import create_notification
from app.services.email_service import send_notification_email, SENT_TEST_EMAILS

def test_google_oauth_status_when_unconfigured(client):
    res = client.get("/api/auth/google/config")
    assert res.status_code == 200
    data = res.get_json()
    assert "enabled" in data
    # When unconfigured, enabled must be False
    assert data["enabled"] is False

    # Attempting to call /api/auth/google when unconfigured returns 400
    post_res = client.post("/api/auth/google", json={"credential": "fake-google-id-token"})
    assert post_res.status_code == 400
    assert "Google OAuth is not configured" in post_res.get_json()["error"]

def test_normalized_email_duplicate_handling(client, student_user):
    # student_user has email "test.student@lpu.in"
    # Attempting to register "TEST.STUDENT@LPU.IN" with different case should be blocked
    res = client.post("/api/auth/register", json={
        "email": "TEST.STUDENT@LPU.IN",
        "display_name": "Test Student Uppercase",
        "password": "Password123!"
    })
    assert res.status_code == 409
    assert "already exists" in res.get_json()["error"]

def test_notification_with_related_ids(app, student_user):
    with app.app_context():
        notif = create_notification(
            recipient_user_id=student_user["id"],
            title="Potential Match",
            message="We found a potential match for your item.",
            notification_type="match",
            related_report_id=10,
            related_claim_id=5
        )
        assert notif is not None
        assert notif.recipient_user_id == student_user["id"]
        assert notif.related_report_id == 10
        assert notif.related_claim_id == 5

        # Verify to_dict includes related IDs
        d = notif.to_dict()
        assert d["recipient_user_id"] == student_user["id"]
        assert d["related_report_id"] == 10
        assert d["related_claim_id"] == 5

def test_email_service_test_mode(app):
    with app.app_context():
        # Clear test queue
        SENT_TEST_EMAILS.clear()

        # Send test notification email
        success, msg = send_notification_email(
            recipient_email="test.student@lpu.in",
            subject="Test Subject",
            message_body="Test message content"
        )
        assert success is True
        assert len(SENT_TEST_EMAILS) == 1
        assert SENT_TEST_EMAILS[0]["recipient"] == "test.student@lpu.in"
        assert SENT_TEST_EMAILS[0]["subject"] == "Test Subject"

from app import db
from app.models.report import ItemReport

def create_found_item(client, user_fixture):
    res = client.post("/api/reports", headers={"Authorization": f"Bearer {user_fixture['token']}"}, json={
        "report_type": "found",
        "title": "Blue Dell Backpack",
        "category": "Bags & Wallets",
        "description": "Found near Block 38 food court.",
        "color": "Blue",
        "brand": "Dell",
        "general_location": "Block 38",
        "event_date": "2026-10-21"
    })
    return res.get_json()["report"]["id"]

def test_submit_claim_success(client, student_user, other_student):
    item_id = create_found_item(client, other_student)

    res = client.post(f"/api/claims/{item_id}", headers={"Authorization": f"Bearer {student_user['token']}"}, json={
        "private_ownership_explanation": "This backpack has my student notebook and a blue Parker pen inside the front zipper pocket."
    })
    assert res.status_code == 201
    data = res.get_json()
    assert data["claim"]["status"] == "pending"
    assert "reference_code" in data["claim"]

def test_cannot_claim_own_reported_item(client, student_user):
    item_id = create_found_item(client, student_user)

    res = client.post(f"/api/claims/{item_id}", headers={"Authorization": f"Bearer {student_user['token']}"}, json={
        "private_ownership_explanation": "This is mine, I reported finding it."
    })
    assert res.status_code == 400

def test_prevent_duplicate_claims(client, student_user, other_student):
    item_id = create_found_item(client, other_student)

    # First claim
    res1 = client.post(f"/api/claims/{item_id}", headers={"Authorization": f"Bearer {student_user['token']}"}, json={
        "private_ownership_explanation": "Detailed explanation of my ownership proof here."
    })
    assert res1.status_code == 201

    # Second claim attempt by same user
    res2 = client.post(f"/api/claims/{item_id}", headers={"Authorization": f"Bearer {student_user['token']}"}, json={
        "private_ownership_explanation": "Trying again with duplicate claim."
    })
    assert res2.status_code == 409

def test_unauthorized_user_cannot_read_private_claim(client, student_user, other_student):
    item_id = create_found_item(client, other_student)

    claim_res = client.post(f"/api/claims/{item_id}", headers={"Authorization": f"Bearer {student_user['token']}"}, json={
        "private_ownership_explanation": "TOP SECRET PASSWORD ON DEVICE SCREEN: 88214"
    })
    claim_id = claim_res.get_json()["claim"]["id"]

    # Other student tries to view claimant's secret explanation
    third_student_res = client.get(f"/api/claims/{claim_id}", headers={"Authorization": f"Bearer {other_student['token']}"})
    assert third_student_res.status_code == 403

import io
import json

def test_create_report_success(client, student_user):
    res = client.post("/api/reports", headers={"Authorization": f"Bearer {student_user['token']}"}, json={
        "report_type": "lost",
        "title": "Dell XPS Laptop 15",
        "category": "Electronics",
        "description": "Silver Dell laptop forgotten at Central Library 3rd floor cubicle.",
        "color": "Silver",
        "brand": "Dell",
        "general_location": "Central Library",
        "event_date": "2026-10-20",
        "identifying_characteristics": "LPU student sticker on wrist rest"
    })
    assert res.status_code == 201
    data = res.get_json()
    assert data["report"]["title"] == "Dell XPS Laptop 15"
    assert data["report"]["reference_code"].startswith("RL-LOST-")

def test_create_report_validation_errors(client, student_user):
    res = client.post("/api/reports", headers={"Authorization": f"Bearer {student_user['token']}"}, json={
        "report_type": "invalid_type",
        "title": "",
        "category": "FakeCategory"
    })
    assert res.status_code == 400
    assert "errors" in res.get_json()

def test_privacy_safe_public_view(client, student_user, other_student):
    # Student creates report with private identifying details
    create_res = client.post("/api/reports", headers={"Authorization": f"Bearer {student_user['token']}"}, json={
        "report_type": "found",
        "title": "Titan Watch with leather strap",
        "category": "Clothing & Accessories",
        "description": "Found near Block 34 main entrance stairs.",
        "color": "Brown",
        "brand": "Titan",
        "general_location": "Block 34",
        "event_date": "2026-10-21",
        "identifying_characteristics": "Engraved serial code #TX88219"
    })
    report_id = create_res.get_json()["report"]["id"]

    # Public/Other student views item
    other_res = client.get(f"/api/reports/{report_id}", headers={"Authorization": f"Bearer {other_student['token']}"})
    assert other_res.status_code == 200
    other_data = other_res.get_json()["report"]
    assert "identifying_characteristics" not in other_data
    assert "reporter_email" not in other_data

    # Owner views item and sees private details
    owner_res = client.get(f"/api/reports/{report_id}", headers={"Authorization": f"Bearer {student_user['token']}"})
    assert owner_res.status_code == 200
    owner_data = owner_res.get_json()["report"]
    assert owner_data.get("identifying_characteristics") == "Engraved serial code #TX88219"

def test_report_editing_permissions(client, student_user, other_student):
    create_res = client.post("/api/reports", headers={"Authorization": f"Bearer {student_user['token']}"}, json={
        "report_type": "lost",
        "title": "Scientific Calculator",
        "category": "Electronics",
        "description": "Black calculator in Block 38 food court.",
        "color": "Black",
        "general_location": "Block 38",
        "event_date": "2026-10-22"
    })
    report_id = create_res.get_json()["report"]["id"]

    # Other student attempts to edit
    patch_res = client.patch(f"/api/reports/{report_id}", headers={"Authorization": f"Bearer {other_student['token']}"}, json={
        "title": "Hacked Calculator"
    })
    assert patch_res.status_code == 403

    # Owner edits successfully
    owner_patch = client.patch(f"/api/reports/{report_id}", headers={"Authorization": f"Bearer {student_user['token']}"}, json={
        "title": "Casio Scientific Calculator"
    })
    assert owner_patch.status_code == 200
    assert owner_patch.get_json()["report"]["title"] == "Casio Scientific Calculator"

def test_invalid_image_upload_rejected(client, student_user):
    create_res = client.post("/api/reports", headers={"Authorization": f"Bearer {student_user['token']}"}, json={
        "report_type": "lost",
        "title": "Room Keys",
        "category": "Keys",
        "description": "Bunch of two keys with blue tag.",
        "color": "Blue",
        "general_location": "Block 14 (Boys Hostel)",
        "event_date": "2026-10-22"
    })
    report_id = create_res.get_json()["report"]["id"]

    # Attempt to upload a fake executable disguised as image
    fake_file = (io.BytesIO(b"MALICIOUS_EXEC_DATA"), "exploit.exe")
    res = client.post(
        f"/api/reports/{report_id}/images",
        headers={"Authorization": f"Bearer {student_user['token']}"},
        data={"file": fake_file},
        content_type="multipart/form-data"
    )
    assert res.status_code == 400

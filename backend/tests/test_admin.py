def test_admin_dashboard_metrics(client, admin_user):
    res = client.get("/api/admin/dashboard", headers={"Authorization": f"Bearer {admin_user['token']}"})
    assert res.status_code == 200
    data = res.get_json()
    assert "metrics" in data
    assert "total_reports" in data["metrics"]
    assert "category_breakdown" in data

def test_admin_claim_approval_workflow(client, student_user, other_student, admin_user):
    # Student 2 reports found phone
    rep_res = client.post("/api/reports", headers={"Authorization": f"Bearer {other_student['token']}"}, json={
        "report_type": "found",
        "title": "OnePlus 11 Smartphone",
        "category": "Electronics",
        "description": "Found on lawn near Shanti Devi Mittal Auditorium.",
        "color": "Black",
        "brand": "OnePlus",
        "general_location": "Shanti Devi Mittal Auditorium",
        "event_date": "2026-10-21"
    })
    item_id = rep_res.get_json()["report"]["id"]

    # Student 1 files claim
    claim_res = client.post(f"/api/claims/{item_id}", headers={"Authorization": f"Bearer {student_user['token']}"}, json={
        "private_ownership_explanation": "Lock pattern is a Z shape, wallpaper is cosmic nebula, IMEI ends in 4102."
    })
    claim_id = claim_res.get_json()["claim"]["id"]

    # Admin approves claim
    appr_res = client.post(
        f"/api/admin/claims/{claim_id}/approve",
        headers={"Authorization": f"Bearer {admin_user['token']}"},
        json={"reason": "Wallpaper and lock pattern verified in presence of security officer."}
    )
    assert appr_res.status_code == 200
    assert appr_res.get_json()["claim"]["status"] == "approved"

    # Admin completes physical handover
    ho_res = client.post(
        f"/api/admin/claims/{claim_id}/handover",
        headers={"Authorization": f"Bearer {admin_user['token']}"},
        json={"notes": "Student ID card checked: Reg 12104523, physical signature obtained in logbook."}
    )
    assert ho_res.status_code == 200
    ho_data = ho_res.get_json()
    assert ho_data["claim"]["status"] == "handover_completed"

    # Verify item status is now 'recovered'
    item_check = client.get(f"/api/reports/{item_id}")
    assert item_check.get_json()["report"]["status"] == "recovered"

def test_admin_claim_rejection_requires_reason(client, student_user, other_student, admin_user):
    rep_res = client.post("/api/reports", headers={"Authorization": f"Bearer {other_student['token']}"}, json={
        "report_type": "found",
        "title": "USB Flash Drive 64GB",
        "category": "Electronics",
        "description": "Found in computer lab.",
        "color": "Black",
        "general_location": "Block 34",
        "event_date": "2026-10-22"
    })
    item_id = rep_res.get_json()["report"]["id"]

    claim_res = client.post(f"/api/claims/{item_id}", headers={"Authorization": f"Bearer {student_user['token']}"}, json={
        "private_ownership_explanation": "It has my name on it."
    })
    claim_id = claim_res.get_json()["claim"]["id"]

    # Rejection without reason fails
    rej_fail = client.post(
        f"/api/admin/claims/{claim_id}/reject",
        headers={"Authorization": f"Bearer {admin_user['token']}"},
        json={"reason": ""}
    )
    assert rej_fail.status_code == 400

    # Rejection with reason succeeds
    rej_ok = client.post(
        f"/api/admin/claims/{claim_id}/reject",
        headers={"Authorization": f"Bearer {admin_user['token']}"},
        json={"reason": "Files on flash drive belong to another student with different registration number."}
    )
    assert rej_ok.status_code == 200
    assert rej_ok.get_json()["claim"]["status"] == "rejected"

def test_admin_suspends_item_report(client, student_user, admin_user):
    rep_res = client.post("/api/reports", headers={"Authorization": f"Bearer {student_user['token']}"}, json={
        "report_type": "lost",
        "title": "Inappropriate Spam Post",
        "category": "Other",
        "description": "Spam promotional text not a real lost item.",
        "color": "None",
        "general_location": "Other Campus Area",
        "event_date": "2026-10-22"
    })
    item_id = rep_res.get_json()["report"]["id"]

    # Admin suspends report
    sus_res = client.patch(
        f"/api/admin/reports/{item_id}/status",
        headers={"Authorization": f"Bearer {admin_user['token']}"},
        json={"status": "suspended", "reason": "Violates university community guidelines (spam)."}
    )
    assert sus_res.status_code == 200
    assert sus_res.get_json()["report"]["status"] == "suspended"

import json

def test_register_student_success(client):
    res = client.post("/api/auth/register", json={
        "email": "new.student@lpu.in",
        "display_name": "New Student",
        "password": "SecurePassword123"
    })
    assert res.status_code == 201
    data = res.get_json()
    assert "token" in data
    assert data["user"]["email"] == "new.student@lpu.in"
    assert data["user"]["role"] == "student"

def test_register_duplicate_email(client, student_user):
    res = client.post("/api/auth/register", json={
        "email": student_user["email"],
        "display_name": "Duplicate Student",
        "password": "SecurePassword123"
    })
    assert res.status_code == 409

def test_register_weak_password(client):
    res = client.post("/api/auth/register", json={
        "email": "weak@lpu.in",
        "display_name": "Weak Pass",
        "password": "pass"
    })
    assert res.status_code == 400

def test_login_success(client, student_user):
    res = client.post("/api/auth/login", json={
        "email": student_user["email"],
        "password": "StudentPass123!"
    })
    assert res.status_code == 200
    data = res.get_json()
    assert "token" in data
    assert data["user"]["email"] == student_user["email"]

def test_login_invalid_password(client, student_user):
    res = client.post("/api/auth/login", json={
        "email": student_user["email"],
        "password": "WrongPassword999"
    })
    assert res.status_code == 401

def test_protected_route_unauthenticated(client):
    res = client.get("/api/auth/me")
    assert res.status_code == 401

def test_protected_route_authenticated(client, student_user):
    res = client.get("/api/auth/me", headers={"Authorization": f"Bearer {student_user['token']}"})
    assert res.status_code == 200
    assert res.get_json()["user"]["email"] == student_user["email"]

def test_change_password(client, student_user):
    res = client.post("/api/auth/change-password", headers={"Authorization": f"Bearer {student_user['token']}"}, json={
        "current_password": "StudentPass123!",
        "new_password": "BrandNewPassword123"
    })
    assert res.status_code == 200

    # Verify login with new password
    login_res = client.post("/api/auth/login", json={
        "email": student_user["email"],
        "password": "BrandNewPassword123"
    })
    assert login_res.status_code == 200

def test_unauthorized_student_access_admin_route(client, student_user):
    res = client.get("/api/admin/dashboard", headers={"Authorization": f"Bearer {student_user['token']}"})
    assert res.status_code == 403

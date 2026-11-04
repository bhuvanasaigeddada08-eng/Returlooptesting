import json
import uuid
import urllib.request
import urllib.parse
from flask import Blueprint, request, jsonify, g, current_app
from app import db
from app.models.user import User
from app.utils.auth_middleware import login_required, generate_auth_token
from app.utils.validators import validate_registration
from app.services.audit_service import log_audit_event

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    errors = validate_registration(data)
    if errors:
        return jsonify({"errors": errors}), 400

    email = data["email"].strip().lower()
    
    # Check normalized email duplicate
    existing_user = User.query.filter(db.func.lower(User.email) == email).first()
    if existing_user:
        return jsonify({"error": "An account with this email address already exists. Please sign in."}), 409

    user = User(
        email=email,
        display_name=data["display_name"].strip(),
        phone=data.get("phone", "").strip() or None,
        role="student"
    )
    user.set_password(data["password"])
    
    db.session.add(user)
    db.session.commit()

    token = generate_auth_token(user)
    return jsonify({
        "message": "Registration successful! Welcome to ReturnLoop LPU.",
        "token": token,
        "user": user.to_dict(include_private=True)
    }), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({"error": "Email and password are required."}), 400

    user = User.query.filter(db.func.lower(User.email) == email).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid email or password. Please verify your credentials and try again."}), 401

    if not user.is_active:
        return jsonify({"error": "Your account has been deactivated. Please contact campus security support."}), 403

    token = generate_auth_token(user)
    return jsonify({
        "message": "Login successful.",
        "token": token,
        "user": user.to_dict(include_private=True)
    }), 200

@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    return jsonify({"message": "Successfully logged out."}), 200

@auth_bp.route("/me", methods=["GET"])
@login_required
def get_current_profile():
    return jsonify({"user": g.current_user.to_dict(include_private=True)}), 200

@auth_bp.route("/change-password", methods=["POST"])
@login_required
def change_password():
    data = request.get_json() or {}
    current_password = data.get("current_password", "")
    new_password = data.get("new_password", "")

    if not g.current_user.check_password(current_password):
        return jsonify({"error": "Current password is incorrect."}), 400

    if len(new_password) < 8:
        return jsonify({"error": "New password must be at least 8 characters long."}), 400
    if not any(c.isdigit() for c in new_password) or not any(c.isalpha() for c in new_password):
        return jsonify({"error": "New password must contain both letters and numbers."}), 400

    g.current_user.set_password(new_password)
    g.current_user.must_change_password = False
    db.session.commit()

    log_audit_event("PASSWORD_CHANGED", "User", g.current_user.id, actor_id=g.current_user.id)
    return jsonify({"message": "Password updated successfully."}), 200

@auth_bp.route("/profile", methods=["PATCH"])
@login_required
def update_profile():
    data = request.get_json() or {}
    user = g.current_user

    if "display_name" in data:
        name = data["display_name"].strip()
        if len(name) >= 2:
            user.display_name = name

    if "phone" in data:
        user.phone = data["phone"].strip() or None

    if "notification_preferences" in data and isinstance(data["notification_preferences"], dict):
        user.notification_preferences = json.dumps(data["notification_preferences"])

    db.session.commit()
    return jsonify({
        "message": "Profile updated successfully.",
        "user": user.to_dict(include_private=True)
    }), 200

# ==================== Google OAuth Optional Integration ====================

@auth_bp.route("/google/config", methods=["GET"])
def get_google_oauth_config():
    client_id = current_app.config.get("GOOGLE_CLIENT_ID", "")
    return jsonify({
        "enabled": bool(client_id),
        "client_id": client_id if client_id else None,
        "message": "Google Sign-In is configured." if client_id else "Google Sign-In is not configured on this server. Set GOOGLE_CLIENT_ID in .env."
    }), 200

@auth_bp.route("/google", methods=["POST"])
def google_sign_in():
    client_id = current_app.config.get("GOOGLE_CLIENT_ID", "")
    if not client_id:
        return jsonify({
            "error": "Google OAuth is not configured on this server. To enable Google Sign-In, configure GOOGLE_CLIENT_ID in your environment."
        }), 400

    data = request.get_json() or {}
    id_token = data.get("credential") or data.get("id_token")
    if not id_token:
        return jsonify({"error": "Missing Google identity credential."}), 400

    try:
        # Validate ID token with Google's official public tokeninfo endpoint
        tokeninfo_url = f"https://oauth2.googleapis.com/tokeninfo?id_token={urllib.parse.quote(id_token)}"
        req = urllib.request.Request(tokeninfo_url, headers={"User-Agent": "ReturnLoop-LPU-Backend/1.0"})
        with urllib.request.urlopen(req, timeout=10) as response:
            payload = json.loads(response.read().decode())

        # Validate audience
        if payload.get("aud") != client_id:
            return jsonify({"error": "Invalid token audience. Google Client ID mismatch."}), 401

        # Validate issuer
        if payload.get("iss") not in ["accounts.google.com", "https://accounts.google.com"]:
            return jsonify({"error": "Invalid token issuer."}), 401

        email = payload.get("email", "").strip().lower()
        if not email:
            return jsonify({"error": "No verified email found in Google identity token."}), 400

        display_name = payload.get("name") or email.split("@")[0]

        # Link safely with existing account or create new student account
        user = User.query.filter(db.func.lower(User.email) == email).first()
        if not user:
            user = User(
                email=email,
                display_name=display_name,
                role="student"  # NEVER grant admin role via public Google OAuth!
            )
            # Set random strong password hash so account is protected
            user.set_password(uuid.uuid4().hex + uuid.uuid4().hex)
            db.session.add(user)
            db.session.commit()
            log_audit_event("USER_REGISTERED_GOOGLE", "User", user.id, actor_id=user.id)
        else:
            if not user.is_active:
                return jsonify({"error": "Your account has been deactivated. Contact campus security."}), 403
            log_audit_event("USER_LOGIN_GOOGLE", "User", user.id, actor_id=user.id)

        token = generate_auth_token(user)
        return jsonify({
            "message": "Google Sign-In successful.",
            "token": token,
            "user": user.to_dict(include_private=True)
        }), 200

    except Exception as e:
        print(f"[Google Auth Error] {e}")
        return jsonify({"error": "Google identity verification failed. Please try standard email login."}), 401

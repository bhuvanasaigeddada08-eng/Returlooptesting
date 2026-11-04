import functools
from flask import request, jsonify, g, current_app
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
from app import db
from app.models.user import User

TOKEN_MAX_AGE = 7 * 24 * 60 * 60  # 7 days

def get_serializer():
    return URLSafeTimedSerializer(current_app.config["SECRET_KEY"])

def generate_auth_token(user):
    s = get_serializer()
    return s.dumps({
        "user_id": user.id,
        "role": user.role,
        "email": user.email
    })

def verify_auth_token(token):
    s = get_serializer()
    try:
        data = s.loads(token, max_age=TOKEN_MAX_AGE)
        return data
    except (SignatureExpired, BadTimeSignature, Exception):
        return None

def get_token_from_header():
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        return auth_header.split(" ", 1)[1].strip()
    return None

def login_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        token = get_token_from_header()
        if not token:
            return jsonify({"error": "Authentication required. Please sign in."}), 401
        
        payload = verify_auth_token(token)
        if not payload:
            return jsonify({"error": "Session expired or invalid token. Please sign in again."}), 401

        user = db.session.get(User, payload.get("user_id"))
        if not user or not user.is_active:
            return jsonify({"error": "Account not found or inactive."}), 401

        g.current_user = user
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        token = get_token_from_header()
        if not token:
            return jsonify({"error": "Authentication required."}), 401
        
        payload = verify_auth_token(token)
        if not payload:
            return jsonify({"error": "Session expired or invalid token."}), 401

        user = db.session.get(User, payload.get("user_id"))
        if not user or not user.is_active or user.role != "admin":
            return jsonify({"error": "Access forbidden: Administrator privileges required."}), 403

        g.current_user = user
        return f(*args, **kwargs)
    return decorated_function

def optional_auth(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        token = get_token_from_header()
        g.current_user = None
        if token:
            payload = verify_auth_token(token)
            if payload:
                user = db.session.get(User, payload.get("user_id"))
                if user and user.is_active:
                    g.current_user = user
        return f(*args, **kwargs)
    return decorated_function

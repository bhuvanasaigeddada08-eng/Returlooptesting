import pytest
import os
import sys

# Ensure backend root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app, db
from app.models.user import User
from app.models.report import ItemReport
from app.models.claim import Claim
from app.utils.auth_middleware import generate_auth_token
from config import TestConfig

@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def student_user(app):
    with app.app_context():
        user = User(
            email="test.student@lpu.in",
            display_name="Test Student",
            role="student"
        )
        user.set_password("StudentPass123!")
        db.session.add(user)
        db.session.commit()
        # Refresh to obtain generated ID
        user_id = user.id
    
    with app.app_context():
        user = db.session.get(User, user_id)
        token = generate_auth_token(user)
        return {"id": user_id, "token": token, "email": user.email}

@pytest.fixture
def other_student(app):
    with app.app_context():
        user = User(
            email="other.student@lpu.in",
            display_name="Other Student",
            role="student"
        )
        user.set_password("StudentPass123!")
        db.session.add(user)
        db.session.commit()
        user_id = user.id

    with app.app_context():
        user = db.session.get(User, user_id)
        token = generate_auth_token(user)
        return {"id": user_id, "token": token, "email": user.email}

@pytest.fixture
def admin_user(app):
    with app.app_context():
        user = User(
            email="admin.security@lpu.in",
            display_name="Security Admin",
            role="admin"
        )
        user.set_password("AdminPass123!")
        db.session.add(user)
        db.session.commit()
        user_id = user.id

    with app.app_context():
        user = db.session.get(User, user_id)
        token = generate_auth_token(user)
        return {"id": user_id, "token": token, "email": user.email}

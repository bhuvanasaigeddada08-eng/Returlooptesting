import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production-returnloop-lpu-2026")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-jwt-key-returnloop-2026")

    # Database URI normalization: cloud providers often supply 'postgres://', SQLAlchemy 2.0 requires 'postgresql://'
    _raw_db_url = os.getenv("DATABASE_URL", "")
    if _raw_db_url:
        if _raw_db_url.startswith("postgres://"):
            _raw_db_url = _raw_db_url.replace("postgres://", "postgresql://", 1)
        SQLALCHEMY_DATABASE_URI = _raw_db_url
    else:
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{BASE_DIR / 'instance' / 'returnloop.db'}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Connection pooling: vital for cloud PostgreSQL (Supabase / Neon)
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    } if "sqlite" not in SQLALCHEMY_DATABASE_URI else {}

    # File / Object Storage
    STORAGE_BACKEND = os.getenv("STORAGE_BACKEND", "supabase" if os.getenv("SUPABASE_URL") else "local")
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", str(BASE_DIR / "uploads"))
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB max
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

    # Cloud Object Storage (Supabase Storage ₹0 Tier)
    SUPABASE_URL = os.getenv("SUPABASE_URL", "").rstrip("/")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
    SUPABASE_STORAGE_BUCKET = os.getenv("SUPABASE_STORAGE_BUCKET", "returnloop-public")
    SUPABASE_PRIVATE_BUCKET = os.getenv("SUPABASE_PRIVATE_BUCKET", "returnloop-private")
    
    # CORS - Allow any local/LAN IP and capacitor origin in dev
    _raw_cors = os.getenv("CORS_ORIGINS", "")
    if _raw_cors:
        CORS_ORIGINS = [origin.strip() for origin in _raw_cors.split(",")]
    else:
        import re
        CORS_ORIGINS = [re.compile(r"^https?://.*"), "capacitor://localhost"]

    
    # Dev Admin Provisioning
    DEV_ADMIN_EMAIL = os.getenv("DEV_ADMIN_EMAIL", "admin@returnloop.lpu.in")
    DEV_ADMIN_PASSWORD = os.getenv("DEV_ADMIN_PASSWORD", "AdminPass123!")
    DEV_ADMIN_NAME = os.getenv("DEV_ADMIN_NAME", "Campus Security Admin")

    # Optional Google OAuth
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")

    # Optional Email Service
    EMAIL_ENABLED = os.getenv("EMAIL_ENABLED", "false").lower() in ("true", "1", "yes")
    EMAIL_TEST_MODE = os.getenv("EMAIL_TEST_MODE", "false").lower() in ("true", "1", "yes")
    SMTP_HOST = os.getenv("SMTP_HOST", "")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
    SMTP_USER = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
    SMTP_USE_TLS = os.getenv("SMTP_USE_TLS", "true").lower() in ("true", "1", "yes")
    SMTP_FROM_EMAIL = os.getenv("SMTP_FROM_EMAIL", "notifications@returnloop.lpu.in")

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    UPLOAD_FOLDER = str(BASE_DIR / "test_uploads")
    SECRET_KEY = "test-secret-key"
    EMAIL_ENABLED = True
    EMAIL_TEST_MODE = True

import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

from app import create_app, db
from app.models.user import User

app = create_app()

def init_dev_admin():
    with app.app_context():
        db.create_all()
        admin_email = app.config.get("DEV_ADMIN_EMAIL", "admin@returnloop.lpu.in").lower()
        existing_admin = User.query.filter_by(email=admin_email).first()
        
        if not existing_admin:
            admin = User(
                email=admin_email,
                display_name=app.config.get("DEV_ADMIN_NAME", "Campus Security Admin"),
                role="admin",
                must_change_password=True,
                phone="01824-517000"
            )
            admin.set_password(app.config.get("DEV_ADMIN_PASSWORD", "AdminPass123!"))
            db.session.add(admin)
            db.session.commit()
            print(f"[ReturnLoop] Provisioned initial admin account: {admin_email}")
            print("[ReturnLoop] Initial password change is required upon first login.")
        else:
            print(f"[ReturnLoop] Admin account '{admin_email}' already present.")

# Initialize DB tables and seed admin on startup (works with both local dev and gunicorn)
init_dev_admin()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "True").lower() in ("true", "1", "yes")
    print(f"[ReturnLoop LPU API] Running on http://127.0.0.1:{port}")
    app.run(host="0.0.0.0", port=port, debug=debug)

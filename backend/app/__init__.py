import os
from flask import Flask, send_from_directory, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=None):
    app = Flask(__name__)
    if config_class is None:
        from config import Config
        app.config.from_object(Config)
    else:
        app.config.from_object(config_class)

    # Ensure instance and upload folders exist
    os.makedirs(os.path.join(app.root_path, "..", "instance"), exist_ok=True)
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(
        app,
        resources={r"/api/*": {"origins": "*"}},
        expose_headers=["Content-Type", "Authorization"]
    )

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.reports import reports_bp
    from app.routes.matches import matches_bp
    from app.routes.claims import claims_bp
    from app.routes.notifications import notifications_bp
    from app.routes.admin import admin_bp
    from app.routes.translate import translate_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(reports_bp, url_prefix="/api/reports")
    app.register_blueprint(matches_bp, url_prefix="/api/matches")
    app.register_blueprint(claims_bp, url_prefix="/api/claims")
    app.register_blueprint(notifications_bp, url_prefix="/api/notifications")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")
    app.register_blueprint(translate_bp, url_prefix="/api/translate")

    # Serve uploaded images safely with graceful fallback for ephemeral instances
    @app.route("/api/uploads/<path:filename>")
    def uploaded_file(filename):
        upload_dir = app.config["UPLOAD_FOLDER"]
        file_path = os.path.join(upload_dir, filename)
        if os.path.isfile(file_path):
            return send_from_directory(upload_dir, filename)

        # Smart fallback: resolve the item and serve matching realistic image
        try:
            from app.models.report import ItemImage
            img_rec = ItemImage.query.filter(
                (ItemImage.file_name == filename) | (ItemImage.file_path.endswith(filename))
            ).first()
            if img_rec and img_rec.report:
                report = img_rec.report
                title = (report.title or "").lower()
                cat = (report.category or "").lower()
                candidate = None
                if any(k in title or k in cat for k in ["calc", "casio"]):
                    candidate = "item_calculator_class.jpg"
                elif any(k in title or k in cat for k in ["laptop", "pavilion", "macbook", "computer", "notebook"]):
                    candidate = "item_laptop_lost.jpg" if report.report_type == "lost" else "item_laptop_library.jpg"
                elif any(k in title or k in cat for k in ["bottle", "flask", "tumbler", "water"]):
                    candidate = "item_bottle_lost.jpg" if report.report_type == "lost" else "item_bottle_found.jpg"
                elif any(k in title or k in cat for k in ["wallet", "purse", "card", "money"]):
                    candidate = "item_wallet_mall.jpg"
                elif any(k in title or k in cat for k in ["key", "lanyard"]):
                    candidate = "item_keys_walkway.jpg"

                if candidate:
                    cand_path = os.path.join(upload_dir, candidate)
                    if os.path.isfile(cand_path):
                        return send_from_directory(upload_dir, candidate)
        except Exception as e:
            app.logger.warning(f"Fallback image resolution error: {e}")

        # Modern branded SVG placeholder
        placeholder_svg = (
            '<svg xmlns="http://www.w3.org/2000/svg" width="600" height="400" viewBox="0 0 600 400">'
            '<defs>'
            '<linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">'
            '<stop offset="0%" stop-color="#0f172a"/>'
            '<stop offset="100%" stop-color="#1e293b"/>'
            '</linearGradient>'
            '</defs>'
            '<rect width="600" height="400" fill="url(#bg)"/>'
            '<circle cx="300" cy="180" r="44" fill="#334155"/>'
            '<path d="M285 180a15 15 0 0 1 30 0v10h-30z" fill="#38bdf8"/>'
            '<text x="300" y="260" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif" font-weight="700" font-size="16" fill="#f8fafc" text-anchor="middle">ReturnLoop LPU Verified</text>'
            '<text x="300" y="285" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif" font-size="12" fill="#94a3b8" text-anchor="middle">Campus Belongs Network</text>'
            '</svg>'
        )
        return Response(placeholder_svg, mimetype="image/svg+xml")

    # Health check endpoint
    @app.route("/api/health")
    def health_check():
        return jsonify({
            "status": "healthy",
            "service": "ReturnLoop LPU API",
            "version": "1.0.0"
        }), 200

    # Global error handlers
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({"error": "Internal server error"}), 500

    return app

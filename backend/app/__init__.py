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
        if not os.path.isfile(file_path):
            placeholder_svg = (
                '<svg xmlns="http://www.w3.org/2000/svg" width="400" height="300" viewBox="0 0 400 300">'
                '<rect width="400" height="300" fill="#f1f5f9"/>'
                '<text x="50%" y="48%" font-family="sans-serif" font-weight="600" font-size="14" fill="#475569" text-anchor="middle">ReturnLoop LPU</text>'
                '<text x="50%" y="56%" font-family="sans-serif" font-size="12" fill="#94a3b8" text-anchor="middle">Photo Preview Unavailable</text>'
                '</svg>'
            )
            return Response(placeholder_svg, mimetype="image/svg+xml")
        return send_from_directory(upload_dir, filename)

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

import os
import uuid
import requests
from werkzeug.utils import secure_filename
from flask import current_app

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}
ALLOWED_MIME_TYPES = {
    "png": "image/png",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "webp": "image/webp"
}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_image_header(stream):
    pos = stream.tell()
    header = stream.read(32)
    stream.seek(pos)
    
    if not header:
        return False
    # PNG
    if header.startswith(b"\x89PNG\r\n\x1a\n"):
        return True
    # JPEG
    if header.startswith(b"\xff\xd8\xff"):
        return True
    # WEBP: starts with RIFF, bytes 8-12 is WEBP
    if header.startswith(b"RIFF") and b"WEBP" in header[:16]:
        return True
    return False

def upload_to_supabase(file_bytes, filename, content_type, is_private=False):
    """
    Uploads a file to Supabase Storage REST API.
    Zero-cost REST integration ensuring 100% free tier compatibility.
    """
    supabase_url = current_app.config.get("SUPABASE_URL", "").rstrip("/")
    supabase_key = current_app.config.get("SUPABASE_KEY", "")
    
    if not supabase_url or not supabase_key:
        return None, "Supabase credentials not configured"

    bucket = (
        current_app.config.get("SUPABASE_PRIVATE_BUCKET", "returnloop-private")
        if is_private
        else current_app.config.get("SUPABASE_STORAGE_BUCKET", "returnloop-public")
    )

    url = f"{supabase_url}/storage/v1/object/{bucket}/{filename}"
    headers = {
        "apikey": supabase_key,
        "Authorization": f"Bearer {supabase_key}",
        "Content-Type": content_type,
        "x-upsert": "true"
    }

    try:
        response = requests.post(url, headers=headers, data=file_bytes, timeout=10)
        if response.status_code in (200, 201):
            if is_private:
                # Private file path returned for internal access/signed URL generation
                return f"/api/claims/evidence/{filename}", None
            else:
                # Direct CDN URL for public images
                public_url = f"{supabase_url}/storage/v1/object/public/{bucket}/{filename}"
                return public_url, None
        return None, f"Supabase storage error: {response.text}"
    except Exception as e:
        return None, f"Failed connecting to Supabase storage: {str(e)}"

def save_uploaded_image(file_storage, is_private=False):
    if not file_storage or not file_storage.filename:
        return None, "No file provided"

    filename = secure_filename(file_storage.filename)
    if not allowed_file(filename):
        return None, "Invalid file format. Allowed formats: PNG, JPG, JPEG, WEBP."

    # Validate file size
    file_storage.seek(0, os.SEEK_END)
    size = file_storage.tell()
    file_storage.seek(0)
    
    max_size = current_app.config.get("MAX_CONTENT_LENGTH", 5 * 1024 * 1024)
    if size > max_size:
        return None, "File too large. Maximum size is 5MB."

    if not validate_image_header(file_storage.stream):
        return None, "File content is not a valid image format."

    ext = filename.rsplit(".", 1)[1].lower()
    random_filename = f"{uuid.uuid4().hex}.{ext}"
    content_type = ALLOWED_MIME_TYPES.get(ext, "application/octet-stream")

    # If Supabase storage is configured, upload to cloud object storage
    backend = current_app.config.get("STORAGE_BACKEND", "local")
    if backend == "supabase" and current_app.config.get("SUPABASE_URL") and current_app.config.get("SUPABASE_KEY"):
        file_bytes = file_storage.read()
        file_storage.seek(0)
        web_path, err = upload_to_supabase(file_bytes, random_filename, content_type, is_private=is_private)
        if not err and web_path:
            return (web_path, random_filename), None
        # If cloud upload fails or falls back, log and save locally as fallback
        current_app.logger.warning(f"Cloud storage upload fallback: {err}")

    # Local filesystem storage (default for development and fallback)
    upload_folder = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(upload_folder, exist_ok=True)
    
    dest_path = os.path.join(upload_folder, random_filename)
    file_storage.save(dest_path)
    
    # Return web-accessible path
    web_path = f"/api/uploads/{random_filename}"
    return (web_path, random_filename), None

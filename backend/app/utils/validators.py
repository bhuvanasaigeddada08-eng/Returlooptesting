import re
from datetime import datetime

ALLOWED_CATEGORIES = [
    "Electronics",
    "ID & Cards",
    "Bags & Wallets",
    "Keys",
    "Books & Stationery",
    "Clothing & Accessories",
    "Bottles & Tumblers",
    "Other"
]

CAMPUS_LOCATIONS = [
    "Block 34",
    "Block 38",
    "Central Library",
    "UniMall",
    "Baldev Raj Mittal Unipolis",
    "Block 14 (Boys Hostel)",
    "Block 28 (Girls Hostel)",
    "Block 55",
    "Block 36",
    "Block 29",
    "Shanti Devi Mittal Auditorium",
    "Food Court / Kiosk Area",
    "Sports Stadium / Complex",
    "Main Gate / Security Post",
    "Other Campus Area"
]

EMAIL_REGEX = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")

def validate_registration(data):
    errors = []
    email = data.get("email", "").strip()
    display_name = data.get("display_name", "").strip()
    password = data.get("password", "")

    if not email or not EMAIL_REGEX.match(email):
        errors.append("A valid email address is required.")
    
    if not display_name or len(display_name) < 2 or len(display_name) > 100:
        errors.append("Display name must be between 2 and 100 characters.")
        
    if not password or len(password) < 8:
        errors.append("Password must be at least 8 characters long.")
    elif not any(c.isdigit() for c in password) or not any(c.isalpha() for c in password):
        errors.append("Password must contain at least one letter and one number.")

    return errors

def validate_report(data):
    errors = []
    title = data.get("title", "").strip()
    category = data.get("category", "").strip()
    description = data.get("description", "").strip()
    color = data.get("color", "").strip()
    general_location = data.get("general_location", "").strip()
    event_date = data.get("event_date", "").strip()
    report_type = data.get("report_type", "").strip()

    if report_type not in ["lost", "found"]:
        errors.append("Report type must be either 'lost' or 'found'.")

    if not title or len(title) < 3 or len(title) > 150:
        errors.append("Title must be between 3 and 150 characters.")

    if not category or category not in ALLOWED_CATEGORIES:
        errors.append(f"Invalid category. Must be one of: {', '.join(ALLOWED_CATEGORIES)}.")

    if not description or len(description) < 10:
        errors.append("Description must be at least 10 characters.")

    if not color:
        errors.append("Color is required.")

    if not general_location:
        errors.append("Campus location is required.")

    if not event_date:
        errors.append("Event date is required.")
    else:
        try:
            parsed_date = datetime.strptime(event_date, "%Y-%m-%d").date()
            if parsed_date > datetime.now().date():
                errors.append("Event date cannot be in the future.")
        except ValueError:
            errors.append("Event date must be in YYYY-MM-DD format.")

    return errors

def validate_claim(data):
    errors = []
    explanation = data.get("private_ownership_explanation", "").strip()
    if not explanation or len(explanation) < 15:
        errors.append("Private ownership explanation must be at least 15 characters detailing verifiable proof.")
    return errors

import json
from flask import request
from app import db
from app.models.audit_log import AuditLog

def log_audit_event(action, target_type, target_id, actor_id=None, details=None):
    try:
        ip = request.remote_addr if request else None
        details_str = json.dumps(details) if isinstance(details, (dict, list)) else (str(details) if details else None)
        
        audit_entry = AuditLog(
            actor_user_id=actor_id,
            action=action,
            target_type=target_type,
            target_id=target_id,
            details=details_str,
            ip_address=ip
        )
        db.session.add(audit_entry)
        db.session.commit()
        return audit_entry
    except Exception as e:
        db.session.rollback()
        print(f"Failed to write audit log: {e}")
        return None

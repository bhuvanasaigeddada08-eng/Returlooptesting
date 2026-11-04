import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# In-memory test queue to record emails in test mode without sending over network
SENT_TEST_EMAILS = []

def get_email_config():
    from flask import has_app_context, current_app
    app_cfg = {}
    if has_app_context():
        app_cfg = current_app.config

    def _val(key, default):
        v = app_cfg.get(key)
        if v is not None:
            return v
        return os.getenv(key, default)

    def _bool(val):
        if isinstance(val, bool):
            return val
        return str(val).lower() in ("true", "1", "yes")

    return {
        "enabled": _bool(_val("EMAIL_ENABLED", "false")),
        "test_mode": _bool(_val("EMAIL_TEST_MODE", "false")),
        "smtp_host": str(_val("SMTP_HOST", "") or ""),
        "smtp_port": int(_val("SMTP_PORT", 587)),
        "smtp_user": str(_val("SMTP_USER", "") or ""),
        "smtp_password": str(_val("SMTP_PASSWORD", "") or ""),
        "use_tls": _bool(_val("SMTP_USE_TLS", "true")),
        "from_email": str(_val("SMTP_FROM_EMAIL", "notifications@returnloop.lpu.in"))
    }

def send_notification_email(recipient_email, subject, message_body, html_body=None):
    """
    Sends an optional notification email.
    If email is not enabled or not configured, it gracefully skips without raising an exception.
    If in test mode, it records the message in SENT_TEST_EMAILS.
    Returns (success: bool, status_message: str)
    """
    cfg = get_email_config()

    if not cfg["enabled"]:
        return (False, "Email notifications are disabled (EMAIL_ENABLED=false). In-app notification created.")

    # Test mode: safe mock for automated testing and local debugging
    if cfg["test_mode"]:
        SENT_TEST_EMAILS.append({
            "recipient": recipient_email,
            "subject": subject,
            "body": message_body,
            "html": html_body
        })
        return (True, f"Email recorded in test queue for {recipient_email} (Test mode active).")

    # If enabled for real sending, ensure SMTP host is configured
    if not cfg["smtp_host"] or not cfg["smtp_user"]:
        return (False, "SMTP host or credentials not configured. In-app notification preserved.")

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"[ReturnLoop LPU] {subject}"
        msg["From"] = cfg["from_email"]
        msg["To"] = recipient_email

        text_part = MIMEText(message_body, "plain")
        msg.attach(text_part)

        if html_body:
            html_part = MIMEText(html_body, "html")
            msg.attach(html_part)

        server = smtplib.SMTP(cfg["smtp_host"], cfg["smtp_port"], timeout=10)
        if cfg["use_tls"]:
            server.starttls()
        if cfg["smtp_password"]:
            server.login(cfg["smtp_user"], cfg["smtp_password"])

        server.sendmail(cfg["from_email"], [recipient_email], msg.as_string())
        server.quit()
        return (True, f"Email delivered to {recipient_email}.")
    except Exception as e:
        # Never crash the calling application if SMTP fails
        error_msg = f"Email delivery failed: {str(e)}"
        print(f"[ReturnLoop EmailService Error] {error_msg}")
        return (False, error_msg)

import smtplib
from email.message import EmailMessage
from config import settings

from auth.exceptions import SendEmailMessageException


def send_email(email_message: EmailMessage) -> None:
    try:
        with smtplib.SMTP_SSL(host=settings.SMTP_HOST, port=settings.SMTP_PORT) as server:
            server.login(settings.SMTP_USER, settings.SMTP_PASS)
            server.send_message(email_message)
    except smtplib.SMTPException:
        raise SendEmailMessageException


def get_email_message(title: str, message: str, to: str, subtype: str = "html") -> EmailMessage:
    email_message = EmailMessage()
    email_message["Subject"] = title
    email_message["From"] = settings.SMTP_USER
    email_message["To"] = to
    email_message.set_content(message, subtype=subtype)
    return email_message

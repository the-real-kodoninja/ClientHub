# backend/api/notifications.py
import smtplib
from email.mime.text import MIMEText
from twilio.rest import Client
from ..utils.config import Config
from fastapi import HTTPException

class NotificationService:
    def __init__(self):
        self.twilio_client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)

    def send_email(self, subject: str, body: str):
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = Config.EMAIL_USER
        msg["To"] = Config.EMAIL_TO

        try:
            with smtplib.SMTP(Config.EMAIL_HOST, Config.EMAIL_PORT) as server:
                server.starttls()
                server.login(Config.EMAIL_USER, Config.EMAIL_PASSWORD)
                server.send_message(msg)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")

    def send_sms(self, body: str):
        try:
            message = self.twilio_client.messages.create(
                body=body,
                from_=Config.TWILIO_PHONE_NUMBER,
                to=Config.PHONE_TO
            )
            return message.sid
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to send SMS: {str(e)}")

    def notify_new_client(self, client_name: str, platform: str):
        subject = f"New Client Added: {client_name}"
        body = f"A new client, {client_name}, has been added from {platform}. Hire me: {Config.FREELANCER_PROFILE_URL}"
        self.send_email(subject, body)
        self.send_sms(body)

# Singleton instance
notification_service = NotificationService()
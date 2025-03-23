# backend/utils/config.py
import os

class Config:
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")
    FREELANCER_API_KEY = os.getenv("FREELANCER_API_KEY", "your_freelancer_api_key")
    FIVERR_API_KEY = os.getenv("FIVERR_API_KEY", "your_fiverr_api_key")
    EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
    EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
    EMAIL_USER = os.getenv("EMAIL_USER", "your_email@gmail.com")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "your_email_password")
    EMAIL_TO = os.getenv("EMAIL_TO", "your_personal_email@example.com")
    TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "your_twilio_sid")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "your_twilio_token")
    TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER", "+1234567890")
    PHONE_TO = os.getenv("PHONE_TO", "+1987654321")
    NIMBUS_DID_PATH = os.getenv("NIMBUS_DID_PATH", "../nimbus.did")
    NIMBUS_CANISTER_ID = os.getenv("NIMBUS_CANISTER_ID", "your_canister_id")
    FREELANCER_PROFILE_URL = os.getenv("FREELANCER_PROFILE_URL", "https://www.freelancer.com/u/yourusername")
    FIVERR_PROFILE_URL = os.getenv("FIVERR_PROFILE_URL", "https://www.fiverr.com/yourusername")
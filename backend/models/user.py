from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_bas

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True)
    password_hash = Column(String)
    social_media_configs = Column(JSON, default={})  # e.g., {"twitter": {"api_key": "..."}, "facebook": {...}}
    freelance_accounts = Column(JSON, default={})   # e.g., {"freelancer": "url", "upwork": "url"}
    twitter_api_key = Column(String)
    twitter_api_secret = Column(String)
    twitter_access_token = Column(String)
    twitter_access_token_secret = Column(String)
    linkedin_email = Column(String)
    linkedin_password = Column(String)
    instagram_username = Column(String)
    instagram_password = Column(String)
    freelancer_url = Column(String)
    fiverr_url = Column(String)
    portfolio_url = Column(String)
    //
    wallet_address = Column(String, nullable=True)
# backend/models/log.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Log(Base):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))  # We’ll add users later
    action = Column(String)  # e.g., "Tweet posted", "Client added"
    details = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
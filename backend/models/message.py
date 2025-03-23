# backend/models/message.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=True)
    assignment_id = Column(String, nullable=True)  # For nimbus.ai messages
    sender = Column(String)  # "user", "client", "nimbus"
    content = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
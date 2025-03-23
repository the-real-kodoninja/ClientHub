# backend/api/messages.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models.message import Message
from ..models.client import Client
from ..main import get_db
from ..api.auth import get_current_user
from ..api.ai_integration import nimbus_service
from pydantic import BaseModel

app = FastAPI()

class MessageCreate(BaseModel):
    client_id: int | None = None
    assignment_id: str | None = None
    content: str

@app.post("/messages/")
async def send_message(
    message: MessageCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if message.client_id:
        client = db.query(Client).filter(Client.id == message.client_id).first()
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")
        db_message = Message(
            user_id=user.id,
            client_id=message.client_id,
            sender="user",
            content=message.content
        )
        db.add(db_message)
        # Simulate client communication (e.g., via email or platform API in future)
        nimbus_service.auto_communicate(client.name, message.content)
    elif message.assignment_id:
        db_message = Message(
            user_id=user.id,
            assignment_id=message.assignment_id,
            sender="user",
            content=message.content
        )
        db.add(db_message)
        nimbus_service.send_nimbus_message(message.assignment_id, message.content)
    else:
        raise HTTPException(status_code=400, detail="Must specify client_id or assignment_id")
    db.commit()
    return {"message": "Sent", "content": message.content}

@app.get("/messages/")
async def get_messages(
    client_id: int | None = None,
    assignment_id: str | None = None,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Message).filter(Message.user_id == user.id)
    if client_id:
        query = query.filter(Message.client_id == client_id)
    if assignment_id:
        query = query.filter(Message.assignment_id == assignment_id)
    messages = query.order_by(Message.timestamp.asc()).all()
    return [{"sender": m.sender, "content": m.content, "timestamp": m.timestamp} for m in messages]
# backend/main.py
from fastapi import FastAPI, Depends, WebSocket
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .utils.config import Config
from .api import clients, promotions
from .api.ai_integration import nimbus_service
import asyncio

app = FastAPI()
engine = create_engine(Config.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.include_router(clients.app)
app.include_router(promotions.app)

@app.get("/")
def read_root():
    return {"message": "ClientHub API is running"}

@app.websocket("/ws/assignment/{assignment_id}")
async def websocket_endpoint(websocket: WebSocket, assignment_id: str):
    await websocket.accept()
    try:
        while True:
            status = nimbus_service.get_assignment_status(assignment_id)
            await websocket.send_text(status)
            await asyncio.sleep(5)
    except Exception:
        await websocket.close()

from .models.client import Base
Base.metadata.create_all(bind=engine)
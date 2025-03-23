# backend/main.py
from fastapi import FastAPI, Depends, WebSocket
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .utils.config import Config
from .api import clients, promotions, auth
from .api.ai_integration import nimbus_service
from .models.user import Base as UserBase
from .models.client import Base as ClientBase
from .models.assignment import Base as AssignmentBase
from .models.log import Base as LogBase
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
app.include_router(auth.app)

@app.get("/")
def read_root():
    return {"message": "ClientHub API is running"}

@app.websocket("/ws/assignment/{assignment_id}")
async def websocket_endpoint(websocket: WebSocket, assignment_id: str, user_id: int = 1, db: Session = Depends(get_db)):
    await websocket.accept()
    try:
        while True:
            status = nimbus_service.get_assignment_status(assignment_id)
            await websocket.send_text(status)
            if status == "Completed":
                promotion_service.promote_everywhere("assignment_done", user_id, db)
                db.add(Log(user_id=user_id, action="Assignment completed", details=f"ID: {assignment_id}"))
                await db.commit()
            await asyncio.sleep(5)
    except Exception:
        await websocket.close()

UserBase.metadata.create_all(bind=engine)
ClientBase.metadata.create_all(bind=engine)
AssignmentBase.metadata.create_all(bind=engine)
LogBase.metadata.create_all(bind=engine)
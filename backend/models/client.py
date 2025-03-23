# backend/api/clients.py
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from ..models.client import Client
from ..models.assignment import Assignment
from ..main import get_db
from .freelance_platforms import platform_service
from .notifications import notification_service
from .ai_integration import nimbus_service
import asyncio

app = FastAPI()

async def process_client(client_data, platform_name, db: Session):
    client = Client(name=client_data["name"], platform=platform_name, priority=client_data.get("priority", 1.0))
    db.add(client)
    await db.commit()
    await db.refresh(client)
    notification_service.notify_new_client(client_data["name"], platform_name)
    assignment_id = nimbus_service.create_assignment(client_data["name"], f"Task for {client_data['name']}")
    assignment = Assignment(client_id=client.id, assignment_id=assignment_id, details=f"Task for {client_data['name']}")
    db.add(assignment)
    await db.commit()
    return {"client": client_data["name"], "assignment_id": assignment_id}

@app.post("/clients/")
async def create_client(name: str, platform: str, priority: float = 1.0, db: Session = Depends(get_db)):
    client_data = {"name": name, "priority": priority}
    result = await process_client(client_data, platform, db)
    return result

@app.get("/clients/sync/{platform_name}")
async def sync_clients(platform_name: str, db: Session = Depends(get_db)):
    clients_data = platform_service.fetch_clients(platform_name)
    tasks = [process_client(client_data, platform_name, db) for client_data in clients_data.get("clients", [])]
    results = await asyncio.gather(*tasks)
    return {"message": f"Synced {len(results)} clients from {platform_name}", "clients": results}

@app.get("/clients/")
async def list_clients(db: Session = Depends(get_db)):
    clients = db.query(Client).order_by(Client.priority.desc()).all()
    return [{"id": c.id, "name": c.name, "platform": c.platform, "priority": c.priority} for c in clients]
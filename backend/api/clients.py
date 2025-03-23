# backend/api/clients.py
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from ..models.client import Client
from ..main import get_db
from .freelance_platforms import platform_service
from .notifications import notification_service
from .ai_integration import nimbus_service

app = FastAPI()

@app.post("/clients/")
def create_client(name: str, platform: str, db: Session = Depends(get_db)):
    client = Client(name=name, platform=platform)
    db.add(client)
    db.commit()
    db.refresh(client)
    notification_service.notify_new_client(name, platform)
    assignment_id = nimbus_service.create_assignment(name, f"Task for {name} from {platform}")
    return {"client": client, "assignment_id": assignment_id}

@app.get("/clients/sync/{platform_name}")
def sync_clients(platform_name: str, db: Session = Depends(get_db)):
    clients_data = platform_service.fetch_clients(platform_name)
    synced_clients = []
    for client_data in clients_data.get("clients", []):
        client = Client(name=client_data["name"], platform=platform_name)
        db.add(client)
        notification_service.notify_new_client(client_data["name"], platform_name)
        assignment_id = nimbus_service.create_assignment(
            client_data["name"], f"Task for {client_data['name']} from {platform_name}"
        )
        synced_clients.append({"client": client_data["name"], "assignment_id": assignment_id})
    db.commit()
    return {"message": f"Synced clients from {platform_name}", "clients": synced_clients}
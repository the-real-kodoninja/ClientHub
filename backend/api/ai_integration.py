# backend/api/ai_integration.py
from ic import Client, Identity, Agent, Canister
from ..utils.config import Config
from fastapi import HTTPException

class NimbusAI:
    def __init__(self):
        with open(Config.NIMBUS_DID_PATH, "r") as f:
            self.nimbus_did = f.read()
        self.identity = Identity()
        self.client = Client(url="https://ic0.app")
        self.agent = Agent(self.identity, self.client)
        self.canister = Canister(
            agent=self.agent,
            canister_id=Config.NIMBUS_CANISTER_ID,
            candid=self.nimbus_did
        )

    def create_assignment(self, client_name: str, assignment_details: str):
        try:
            result = self.canister.create_assignment(client_name, assignment_details)
            return result[0] if result else None
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to create assignment: {str(e)}")

    def get_assignment_status(self, assignment_id: str):
        try:
            status = self.canister.get_status(assignment_id)
            return status[0] if status else "Unknown"
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get status: {str(e)}")

nimbus_service = NimbusAI()
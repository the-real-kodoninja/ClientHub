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

    def auto_communicate(self, client_name: str, message: str):
        try:
            return self.canister.send_message(client_name, message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Communication failed: {str(e)}")

    def prioritize_tasks(self, client_list: list):
        try:
            return self.canister.prioritize_tasks(client_list)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Prioritization failed: {str(e)}")

    def batch_process(self, clients: list):
        try:
            return self.canister.batch_process(clients)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Batch processing failed: {str(e)}")

    def send_nimbus_message(self, assignment_id: str, message: str):
        try:
            return self.canister.send_nimbus_message(assignment_id, message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Nimbus message failed: {str(e)}")

nimbus_service = NimbusAI()
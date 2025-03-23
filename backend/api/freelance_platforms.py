# backend/api/freelance_platforms.py
import requests
from fastapi import HTTPException
from ..utils.config import Config

class FreelancePlatform:
    def __init__(self):
        self.platforms = {
            "freelancer": {
                "api_url": "https://api.freelancer.com/v1",
                "api_key": Config.FREELANCER_API_KEY  # Add to config.py
            },
            "fiverr": {
                "api_url": "https://api.fiverr.com/v1",  # Hypothetical URL
                "api_key": Config.FIVERR_API_KEY      # Add to config.py
            }
        }

    def fetch_clients(self, platform_name: str):
        if platform_name not in self.platforms:
            raise HTTPException(status_code=400, detail="Unsupported platform")
        
        platform = self.platforms[platform_name]
        headers = {"Authorization": f"Bearer {platform['api_key']}"}
        response = requests.get(f"{platform['api_url']}/clients", headers=headers)
        
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch clients")
        
        return response.json()

# Singleton instance
platform_service = FreelancePlatform()
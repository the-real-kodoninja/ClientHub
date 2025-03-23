# backend/api/promotions.py
from fastapi import FastAPI
from ..utils.config import Config

app = FastAPI()

class PromotionService:
    def get_promo_message(self, context: str = "general"):
        base_message = "Need freelance help? Hire me for top-notch [your skill] services!"
        links = {
            "Freelancer": Config.FREELANCER_PROFILE_URL,
            "Fiverr": Config.FIVERR_PROFILE_URL,
            "Portfolio": "https://yourwebsite.com"  # Add your site
        }
        if context == "new_client":
            return {"message": f"{base_message} Just added a client – join them!", "links": links}
        return {"message": base_message, "links": links}

promotion_service = PromotionService()

@app.get("/promotions/")
def get_promotions(context: str = "general"):
    return promotion_service.get_promo_message(context)
# backend/api/promotions.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from ..utils.config import Config
from ..main import get_db
from ..models.log import Log
from ..models.user import User
import tweepy
from linkedin_api import Linkedin
from instagrapi import Client as InstaClient
import facebook
from tiktokapi import TikTokAPI

app = FastAPI()

class PromotionService:
    def __init__(self):
        self.clients = {}

    def get_user_config(self, user_id: int, db: Session):
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return Config.get_user_config(user_id, db)
        return {
            "social_media": user.social_media_configs,
            "profiles": user.freelance_accounts
        }

    def initialize_client(self, platform: str, config: dict):
        if platform == "twitter":
            return tweepy.Client(
                consumer_key=config["api_key"],
                consumer_secret=config["api_secret"],
                access_token=config["access_token"],
                access_token_secret=config["access_token_secret"]
            )
        elif platform == "linkedin":
            return Linkedin(config["email"], config["password"])
        elif platform == "instagram":
            client = InstaClient()
            client.login(config["username"], config["password"])
            return client
        elif platform == "facebook":
            return facebook.GraphAPI(access_token=config["access_token"])
        elif platform == "tiktok":
            return TikTokAPI(username=config["username"], password=config["password"])
        return None

    def get_promo_message(self, context: str, user_id: int, db: Session):
        config = self.get_user_config(user_id, db)
        profiles = config["profiles"]
        portfolio = profiles.get("portfolio", Config.DEFAULT_PROFILE_URLS["Portfolio"])
        base_message = "Need top freelance services? Hire me now!"
        if context == "new_client":
            return f"{base_message} Just added a new client – join them! {portfolio}"
        elif context == "assignment_done":
            return f"{base_message} Just completed a project – book me! {portfolio}"
        return f"{base_message} {portfolio}"

    def log_activity(self, action: str, details: str, user_id: int, db: Session):
        log = Log(user_id=user_id, action=action, details=details)
        db.add(log)
        db.commit()

    def post_to_platform(self, platform: str, message: str, user_id: int, db: Session):
        config = self.get_user_config(user_id, db)["social_media"].get(platform, {})
        if not config:
            return {"platform": platform, "status": "Not configured"}
        client = self.initialize_client(platform, config)
        try:
            if platform == "twitter":
                client.create_tweet(text=message[:280])
            elif platform == "linkedin":
                client.post(message)
            elif platform == "instagram":
                client.photo_upload_to_story("promo_image.jpg", caption=message[:2200])
            elif platform == "facebook":
                client.put_object(parent_object="me", connection_name="feed", message=message)
            elif platform == "tiktok":
                client.upload_video("promo_video.mp4", description=message[:150])  # Requires a video file
            self.log_activity(f"{platform} posted", message, user_id, db)
            return {"platform": platform, "status": "Posted"}
        except Exception as e:
            self.log_activity(f"{platform} failed", str(e), user_id, db)
            return {"platform": platform, "status": "Failed", "error": str(e)}

    def promote_everywhere(self, context: str, user_id: int, db: Session):
        message = self.get_promo_message(context, user_id, db)
        config = self.get_user_config(user_id, db)["social_media"]
        results = [
            self.post_to_platform(platform, f"{message} #{platform.capitalize()} #Freelance", user_id, db)
            for platform in config.keys()
        ]
        return results

promotion_service = PromotionService()

@app.get("/promotions/")
def get_promotions(context: str = "general", user_id: int = 1, db: Session = Depends(get_db)):
    return promotion_service.get_promo_message(context, user_id, db)

@app.post("/promotions/everywhere/")
def promote_everywhere(context: str, user_id: int = 1, db: Session = Depends(get_db)):
    return promotion_service.promote_everywhere(context, user_id, db)
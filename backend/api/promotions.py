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

app = FastAPI()

class PromotionService:
    def __init__(self):
        self.clients = {}

    def get_user_config(self, user_id: int, db: Session):
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return Config.get_user_config(user_id, db)
        return {
            "TWITTER_API_KEY": user.twitter_api_key,
            "TWITTER_API_SECRET": user.twitter_api_secret,
            "TWITTER_ACCESS_TOKEN": user.twitter_access_token,
            "TWITTER_ACCESS_TOKEN_SECRET": user.twitter_access_token_secret,
            "LINKEDIN_EMAIL": user.linkedin_email,
            "LINKEDIN_PASSWORD": user.linkedin_password,
            "INSTAGRAM_USERNAME": user.instagram_username,
            "INSTAGRAM_PASSWORD": user.instagram_password,
            "PROFILE_URLS": {
                "Freelancer": user.freelancer_url or Config.DEFAULT_PROFILE_URLS["Freelancer"],
                "Fiverr": user.fiverr_url or Config.DEFAULT_PROFILE_URLS["Fiverr"],
                "Portfolio": user.portfolio_url or Config.DEFAULT_PROFILE_URLS["Portfolio"]
            }
        }

    def initialize_client(self, user_id: int, db: Session):
        if user_id not in self.clients:
            config = self.get_user_config(user_id, db)
            self.clients[user_id] = {
                "twitter": tweepy.Client(
                    consumer_key=config["TWITTER_API_KEY"],
                    consumer_secret=config["TWITTER_API_SECRET"],
                    access_token=config["TWITTER_ACCESS_TOKEN"],
                    access_token_secret=config["TWITTER_ACCESS_TOKEN_SECRET"]
                ),
                "linkedin": Linkedin(config["LINKEDIN_EMAIL"], config["LINKEDIN_PASSWORD"]),
                "instagram": InstaClient()
            }
            self.clients[user_id]["instagram"].login(config["INSTAGRAM_USERNAME"], config["INSTAGRAM_PASSWORD"])
        return self.clients[user_id]

    def get_promo_message(self, context: str, user_id: int, db: Session):
        config = self.get_user_config(user_id, db)
        profiles = config["PROFILE_URLS"]
        base_message = "Need top freelance services? Hire me now!"
        if context == "new_client":
            return f"{base_message} Just added a new client – join them! {profiles['Portfolio']}"
        elif context == "assignment_done":
            return f"{base_message} Just completed a project – book me! {profiles['Portfolio']}"
        return f"{base_message} {profiles['Portfolio']}"

    def log_activity(self, action: str, details: str, user_id: int, db: Session):
        log = Log(user_id=user_id, action=action, details=details)
        db.add(log)
        db.commit()

    def post_to_twitter(self, message: str, user_id: int, db: Session):
        clients = self.initialize_client(user_id, db)
        try:
            clients["twitter"].create_tweet(text=message[:280])
            self.log_activity("Tweet posted", message, user_id, db)
            return {"platform": "Twitter", "status": "Posted"}
        except Exception as e:
            self.log_activity("Tweet failed", str(e), user_id, db)
            return {"platform": "Twitter", "status": "Failed", "error": str(e)}

    def post_to_linkedin(self, message: str, user_id: int, db: Session):
        clients = self.initialize_client(user_id, db)
        try:
            clients["linkedin"].post(message)
            self.log_activity("LinkedIn post", message, user_id, db)
            return {"platform": "LinkedIn", "status": "Posted"}
        except Exception as e:
            self.log_activity("LinkedIn failed", str(e), user_id, db)
            return {"platform": "LinkedIn", "status": "Failed", "error": str(e)}

    def post_to_instagram(self, message: str, user_id: int, db: Session):
        clients = self.initialize_client(user_id, db)
        try:
            clients["instagram"].photo_upload_to_story("promo_image.jpg", caption=message[:2200])
            self.log_activity("Instagram story posted", message, user_id, db)
            return {"platform": "Instagram", "status": "Posted"}
        except Exception as e:
            self.log_activity("Instagram failed", str(e), user_id, db)
            return {"platform": "Instagram", "status": "Failed", "error": str(e)}

    def promote_everywhere(self, context: str, user_id: int, db: Session):
        message = self.get_promo_message(context, user_id, db)
        results = [
            self.post_to_twitter(f"{message} #Freelance #HireMe", user_id, db),
            self.post_to_linkedin(message, user_id, db),
            self.post_to_instagram(f"{message} #FreelanceLife", user_id, db)
        ]
        return results

promotion_service = PromotionService()

@app.get("/promotions/")
def get_promotions(context: str = "general", user_id: int = 1, db: Session = Depends(get_db)):
    return promotion_service.get_promo_message(context, user_id, db)

@app.post("/promotions/everywhere/")
def promote_everywhere(context: str, user_id: int = 1, db: Session = Depends(get_db)):
    return promotion_service.promote_everywhere(context, user_id, db)
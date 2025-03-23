# backend/api/promotions.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from ..utils.config import Config
from ..main import get_db
from ..models.log import Log
import tweepy
from linkedin_api import Linkedin
from instagrapi import Client as InstaClient

app = FastAPI()

class PromotionService:
    def __init__(self):
        # Twitter
        self.twitter_client = tweepy.Client(
            consumer_key=Config.TWITTER_API_KEY,
            consumer_secret=Config.TWITTER_API_SECRET,
            access_token=Config.TWITTER_ACCESS_TOKEN,
            access_token_secret=Config.TWITTER_ACCESS_TOKEN_SECRET
        )
        # LinkedIn
        self.linkedin_client = Linkedin(Config.LINKEDIN_EMAIL, Config.LINKEDIN_PASSWORD)
        # Instagram
        self.insta_client = InstaClient()
        self.insta_client.login(Config.INSTAGRAM_USERNAME, Config.INSTAGRAM_PASSWORD)

    def get_promo_message(self, context: str = "general", user_profiles: dict = None):
        profiles = user_profiles or Config.DEFAULT_PROFILE_URLS
        base_message = "Need top freelance services? Hire me now!"
        if context == "new_client":
            return f"{base_message} Just added a new client – join them! {profiles['Portfolio']}"
        elif context == "assignment_done":
            return f"{base_message} Just completed a project – book me! {profiles['Portfolio']}"
        return f"{base_message} {profiles['Portfolio']}"

    def log_activity(self, action: str, details: str, user_id: int = 1, db: Session = None):
        log = Log(user_id=user_id, action=action, details=details)
        db.add(log)
        db.commit()

    def post_to_twitter(self, message: str, db: Session):
        try:
            self.twitter_client.create_tweet(text=message[:280])
            self.log_activity("Tweet posted", message, db=db)
            return {"platform": "Twitter", "status": "Posted"}
        except Exception as e:
            self.log_activity("Tweet failed", str(e), db=db)
            return {"platform": "Twitter", "status": "Failed", "error": str(e)}

    def post_to_linkedin(self, message: str, db: Session):
        try:
            self.linkedin_client.post(message)
            self.log_activity("LinkedIn post", message, db=db)
            return {"platform": "LinkedIn", "status": "Posted"}
        except Exception as e:
            self.log_activity("LinkedIn failed", str(e), db=db)
            return {"platform": "LinkedIn", "status": "Failed", "error": str(e)}

    def post_to_instagram(self, message: str, db: Session):
        try:
            self.insta_client.photo_upload_to_story("promo_image.jpg", caption=message[:2200])  # Requires an image
            self.log_activity("Instagram story posted", message, db=db)
            return {"platform": "Instagram", "status": "Posted"}
        except Exception as e:
            self.log_activity("Instagram failed", str(e), db=db)
            return {"platform": "Instagram", "status": "Failed", "error": str(e)}

    def promote_everywhere(self, context: str, user_id: int = 1, user_profiles: dict = None, db: Session = None):
        message = self.get_promo_message(context, user_profiles)
        results = [
            self.post_to_twitter(f"{message} #Freelance #HireMe", db),
            self.post_to_linkedin(message, db),
            self.post_to_instagram(f"{message} #FreelanceLife", db)
        ]
        return results

promotion_service = PromotionService()

@app.get("/promotions/")
def get_promotions(context: str = "general"):
    return promotion_service.get_promo_message(context)

@app.post("/promotions/everywhere/")
def promote_everywhere(context: str, user_id: int = 1, db: Session = Depends(get_db)):
    return promotion_service.promote_everywhere(context, user_id, db=db)
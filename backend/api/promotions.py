# backend/api/promotions.py
from fastapi import FastAPI, Depends, HTTPException
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
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import stripe
import os
from dotenv import load_dotenv
from pinterest_api import Pinterest
from github import Github
import smtplib
from email.mime.text import MIMEText

load_dotenv()

app = FastAPI()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

class PromotionService:
    def __init__(self):
        self.clients = {}

    def get_user_config(self, user_id: int, db: Session):
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return Config.get_user_config(user_id, db)
        return {
            "social_media": user.social_media_configs,
            "profiles": user.freelance_accounts,
            "stripe_customer_id": user.stripe_customer_id
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
        elif platform == "youtube":
            creds = Credentials.from_authorized_user_info(config)
            return build("youtube", "v3", credentials=creds)
        elif platform == "pinterest":
            return Pinterest(access_token=config["access_token"])
        elif platform == "github":
            return Github(config["access_token"])
        return None

    def get_promo_message(self, context: str, user_id: int, db: Session):
        config = self.get_user_config(user_id, db)
        profiles = config["profiles"]
        portfolio = profiles.get("portfolio", Config.DEFAULT_PROFILE_URLS["Portfolio"])
        github_url = profiles.get("github", "https://github.com/user")
        base_message = "Need top freelance services? Hire me now!"
        if context == "new_client":
            return f"{base_message} Just added a new client – join them! {portfolio} | GitHub: {github_url}"
        elif context == "assignment_done":
            return f"{base_message} Just completed a project – book me! {portfolio} | GitHub: {github_url}"
        elif context == "portfolio":
            return f"Check out my freelance portfolio! {portfolio} | GitHub: {github_url} Hire me on Fiverr: [your_fiverr_url]"
        return f"{base_message} {portfolio} | GitHub: {github_url}"

    def log_activity(self, action: str, details: str, user_id: int, db: Session):
        log = Log(user_id=user_id, action=action, details=details)
        db.add(log)
        db.commit()

    def log_analytics(self, platform: str, post_id: str, user_id: int, db: Session):
        config = self.get_user_config(user_id, db)["social_media"].get(platform, {})
        client = self.initialize_client(platform, config)
        try:
            if platform == "twitter" and client:
                tweet = client.get_tweet(post_id)
                analytics = f"Retweets: {tweet.data['public_metrics']['retweet_count']}, Likes: {tweet.data['public_metrics']['like_count']}"
            elif platform == "pinterest" and client:
                pin = client.get_pin(post_id)
                analytics = f"Saves: {pin['counts']['saves']}, Clicks: {pin['counts']['clicks']}"
            elif platform == "youtube" and client:
                video = client.videos().list(id=post_id, part="statistics").execute()
                analytics = f"Views: {video['items'][0]['statistics']['viewCount']}, Likes: {video['items'][0]['statistics']['likeCount']}"
            else:
                analytics = "Analytics not available"
            self.log_activity(f"{platform} analytics", analytics, user_id, db)
            return analytics
        except Exception as e:
            self.log_activity(f"{platform} analytics failed", str(e), user_id, db)
            return "Failed to fetch analytics"

    def send_email_notification(self, user_id: int, message: str, db: Session):
        user = db.query(User).filter(User.id == user_id).first()
        msg = MIMEText(f"Promotion posted: {message}")
        msg["Subject"] = "ClientHub Promotion Update"
        msg["From"] = os.getenv("EMAIL_SENDER")
        msg["To"] = user.email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(os.getenv("EMAIL_SENDER"), os.getenv("EMAIL_PASSWORD"))
            server.send_message(msg)

    def post_to_platform(self, platform: str, message: str, user_id: int, db: Session):
        config = self.get_user_config(user_id, db)["social_media"].get(platform, {})
        if not config:
            return {"platform": platform, "status": "Not configured"}
        client = self.initialize_client(platform, config)
        try:
            post_id = None
            if platform == "twitter":
                response = client.create_tweet(text=message[:280])
                post_id = response.data["id"]
            elif platform == "linkedin":
                client.post(message)
            elif platform == "instagram":
                client.photo_upload_to_story("promo_image.jpg", caption=message[:2200])
            elif platform == "facebook":
                response = client.put_object(parent_object="me", connection_name="feed", message=message)
                post_id = response["id"]
            elif platform == "tiktok":
                client.upload_video("promo_video.mp4", description=message[:150])
            elif platform == "youtube":
                request = client.videos().insert(
                    part="snippet,status",
                    body={
                        "snippet": {"title": "ClientHub Promo", "description": message},
                        "status": {"privacyStatus": "public"}
                    },
                    media_body="promo_video.mp4"
                )
                response = request.execute()
                post_id = response["id"]
            elif platform == "pinterest":
                response = client.create_pin(
                    board_id=config["board_id"],
                    title="Freelance Portfolio",
                    description=message[:500],
                    link=config.get("portfolio_url", "https://fiverr.com/your_profile"),
                    media="promo_image.jpg"
                )
                post_id = response["id"]
            self.log_activity(f"{platform} posted", message, user_id, db)
            if post_id:
                analytics = self.log_analytics(platform, post_id, user_id, db)
                self.send_email_notification(user_id, f"{message} (Analytics: {analytics})", db)
            else:
                self.send_email_notification(user_id, message, db)
            return {"platform": platform, "status": "Posted", "post_id": post_id}
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

    def create_subscription(self, user_id: int, db: Session):
        config = self.get_user_config(user_id, db)
        customer_id = config.get("stripe_customer_id")
        if not customer_id:
            customer = stripe.Customer.create(email=config["email"])
            user = db.query(User).filter(User.id == user_id).first()
            user.stripe_customer_id = customer.id
            db.commit()
            customer_id = customer.id
        subscription = stripe.Subscription.create(
            customer=customer_id,
            items=[{"price": os.getenv("STRIPE_PRICE_ID")}]
        )
        return {"status": "Subscribed", "subscription_id": subscription.id}

    def promote_portfolio(self, user_id: int, db: Session):
        config = self.get_user_config(user_id, db)
        github_client = self.initialize_client("github", config["social_media"].get("github", {}))
        if github_client:
            repos = github_client.get_user().get_repos()
            portfolio_message = f"Check my latest GitHub projects: {', '.join([repo.html_url for repo in repos[:3]])} | Hire me on Fiverr!"
        else:
            portfolio_message = self.get_promo_message("portfolio", user_id, db)
        return self.promote_everywhere("portfolio", user_id, db)

promotion_service = PromotionService()

@app.get("/promotions/")
def get_promotions(context: str = "general", user_id: int = 1, db: Session = Depends(get_db)):
    return promotion_service.get_promo_message(context, user_id, db)

@app.post("/promotions/everywhere/")
def promote_everywhere(context: str, user_id: int = 1, db: Session = Depends(get_db)):
    return promotion_service.promote_everywhere(context, user_id, db)

@app.post("/payments/subscribe/")
def subscribe(user_id: int = 1, db: Session = Depends(get_db)):
    return promotion_service.create_subscription(user_id, db)

@app.post("/promotions/portfolio/")
def promote_portfolio(user_id: int = 1, db: Session = Depends(get_db)):
    return promotion_service.promote_portfolio(user_id, db)
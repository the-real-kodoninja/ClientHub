# ClientHub Code Explanation

This document explains the key components of the ClientHub application as of March 23, 2025.

## Backend (`backend/api/promotions.py`)

### Overview
The backend uses FastAPI to manage social media promotions, payments, analytics, and notifications.

### Key Components

#### Dependencies
- **Social Media**: `tweepy` (Twitter), `linkedin-api`, `instagrapi` (Instagram), `facebook-sdk`, `tiktokapi`, `google-api-python-client` (YouTube), `pinterest-api`, `PyGithub`.
- **Payments**: `stripe`.
- **Utilities**: `sqlalchemy`, `python-dotenv`, `smtplib`.

#### `PromotionService` Class
- **Initialization**: `self.clients` stores API clients.
- **`get_user_config`**: Fetches user settings (social media, profiles, Stripe ID).
- **`initialize_client`**:
  - Twitter: OAuth 1.0a.
  - LinkedIn: Email/password (unofficial).
  - Instagram: Username/password.
  - Facebook: Graph API.
  - TikTok: Unofficial API.
  - YouTube: OAuth 2.0 (Google Cloud Console).
  - Pinterest: Access token + board ID (Pinterest Developers).
  - GitHub: Access token (GitHub Settings > Developer Settings).
- **`get_promo_message`**: Context-based messages with portfolio/GitHub links.
- **`log_activity`**: Logs to database.
- **`log_analytics`**: Real metrics from Twitter (likes/retweets), Pinterest (saves/clicks), YouTube (views/likes).
- **`send_email_notification`**: SMTP email via Gmail.
- **`post_to_platform`**: Posts to platforms, logs analytics, sends emails.
- **`promote_everywhere`**: Posts to all configured platforms.
- **`create_subscription`**: Stripe subscription for premium features.
- **`promote_portfolio`**: Promotes GitHub repos and Fiverr links.

#### API Endpoints
- **GET `/promotions/`**: Returns promo message.
- **POST `/promotions/everywhere/`**: Posts everywhere.
- **POST `/payments/subscribe/`**: Subscribes via Stripe.
- **POST `/promotions/portfolio/`**: Promotes portfolio/GitHub/Fiverr.

#### Environment Variables (`.env`)
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PRICE_ID=price_...
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password

text




## Frontend (`frontend/src/components/Settings.js`)
- **Features**: Manages social media configs, freelance accounts, MetaMask wallet, with add/delete, validation, and error handling.
- **API**: Uses `axios` for `/users/me`.

## Mobile (`ClientHubMobile/screens/SettingsScreen.js`)
- **Features**: Mirrors web Settings with React Native components, navigation via `@react-navigation/drawer`.
- **Storage**: `AsyncStorage` for tokens.

## Setup (`setup.sh`)
- **Steps**: Installs Python, Node.js, PostgreSQL, dependencies, and starts services.
- **Usage**: `chmod +x setup.sh && ./setup.sh`

## Additional Features
- **Pinterest**: Promotes visual portfolio pins.
- **Real Analytics**: Tracks engagement from supported platforms.
- **Portfolio Promotion**: Showcases GitHub work and Fiverr links.

## Next Steps
- Add confirmation dialogs for deletes.
- Integrate more platforms (e.g., Discord).
- Enhance analytics with more platforms.
How This Enhances ClientHub
Pinterest: Boosts visibility with visual pins, perfect for portfolio promotion.
Real Analytics: Provides actionable insights into post performance.
Portfolio Promotion: Drives freelance clients to Fiverr via GitHub/Portfolio links.
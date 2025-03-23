#!/bin/bash
# setup.sh

# Exit on error
set -e

echo "Setting up ClientHub..."

# Install system dependencies (Ubuntu/Debian assumed)
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv postgresql postgresql-contrib

# Set up Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install -r backend/requirements.txt

# Set up PostgreSQL (example config, adjust as needed)
sudo -u postgres psql -c "CREATE DATABASE clienthub;"
sudo -u postgres psql -c "CREATE USER clienthub_user WITH PASSWORD 'your_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE clienthub TO clienthub_user;"

# Set environment variables (edit these!)
cat << EOF > .env
DATABASE_URL=postgresql://clienthub_user:your_password@localhost/clienthub
FREELANCER_API_KEY=your_freelancer_api_key
FIVERR_API_KEY=your_fiverr_api_key
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_email_password
EMAIL_TO=your_personal_email@example.com
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_PHONE_NUMBER=+1234567890
PHONE_TO=+1987654321
NIMBUS_DID_PATH=../nimbus.did
NIMBUS_CANISTER_ID=your_canister_id
FREELANCER_PROFILE_URL=https://www.freelancer.com/u/yourusername
FIVERR_PROFILE_URL=https://www.fiverr.com/yourusername
PORTFOLIO_URL=https://yourwebsite.com
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret
TWITTER_ACCESS_TOKEN=your_twitter_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret
EOF

# Install Node.js and frontend dependencies
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
cd frontend
npm install
cd ..

# Install React Native CLI (optional, for mobile)
npm install -g react-native-cli

echo "Setup complete! Edit .env with your credentials, then run:"
echo "source venv/bin/activate && uvicorn main:app --reload (backend)"
echo "cd frontend && npm start (frontend)"
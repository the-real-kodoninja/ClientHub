#!/bin/bash

# ClientHub Setup Script
# Run this to install all dependencies and start the application

echo "Starting ClientHub setup..."

# Update system
sudo apt update -y

# Install Python and pip
sudo apt install python3 python3-pip -y

# Install Node.js and npm
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Install PostgreSQL
sudo apt install postgresql postgresql-contrib -y
sudo -u postgres psql -c "CREATE DATABASE clienthub;"
sudo -u postgres psql -c "CREATE USER clienthub_user WITH PASSWORD 'your_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE clienthub TO clienthub_user;"

# Backend setup
cd backend
pip3 install -r requirements.txt
python3 -m uvicorn main:app --reload &

# Frontend setup
cd ../frontend
npm install
npm install axios @metamask/detect-provider
npm start &

# Mobile setup
cd ../ClientHubMobile
npm install
npm install @react-navigation/native @react-navigation/drawer react-native-reanimated react-native-gesture-handler react-native-screens react-native-safe-area-context @react-native-async-storage/async-storage axios
npx expo start &

echo "Setup complete! Backend at http://localhost:8000, Frontend at http://localhost:3000, Mobile via Expo."
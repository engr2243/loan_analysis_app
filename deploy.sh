#!/bin/bash

# Script to deploy Streamlit App with Nginx on Ubuntu 22.04
# Author: [Your Name]
# Date: [Today's Date]

# Exit immediately if any command fails
set -e

# Variables
APP_DIR="/home/ubuntu/loan_analysis_app"  # Change this to your app's directory
VENV_DIR="$APP_DIR/.venv"
STREAMLIT_APP="app.py"  # Your Streamlit app filename
NGINX_CONFIG="/etc/nginx/sites-available/streamlit"
NGINX_SYMLINK="/etc/nginx/sites-enabled/streamlit"
SERVICE_NAME="loan_analysis_app"
DOMAIN_NAME="157.175.69.249"  # Change to your domain or public IP

# Update and install necessary packages
echo "Updating and installing dependencies..."
sudo apt update
sudo apt install -y python3-pip python3-venv nginx

# Navigate to application directory
cd "$APP_DIR"

# Set up virtual environment
if [ ! -d "$VENV_DIR" ]; then
  echo "Creating Python virtual environment..."
  python3 -m venv "$VENV_DIR"
fi

# Activate virtual environment and install requirements
echo "Activating virtual environment and installing requirements..."
source "$VENV_DIR/bin/activate"

if [ -f "requirements.txt" ]; then
  pip install --upgrade pip
  pip install -r requirements.txt
else
  echo "No requirements.txt found. Skipping dependencies installation."
fi

# Deactivate virtual environment
deactivate

# Set up systemd service for Streamlit
echo "Creating systemd service for Streamlit..."
sudo tee /etc/systemd/system/$SERVICE_NAME.service > /dev/null <<EOL
[Unit]
Description=Streamlit App
After=network.target

[Service]
User=ubuntu
WorkingDirectory=$APP_DIR
ExecStart=$VENV_DIR/bin/streamlit run $STREAMLIT_APP --server.port 8501 --server.headless true --server.enableCORS false
Restart=always

[Install]
WantedBy=multi-user.target
EOL

# Reload systemd and start the service
sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME
sudo systemctl restart $SERVICE_NAME

# Set up Nginx as a reverse proxy
echo "Configuring Nginx..."
sudo tee $NGINX_CONFIG > /dev/null <<EOL
server {
    listen 80;
    server_name $DOMAIN_NAME;

    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOL

# Enable the Nginx configuration
if [ -f "$NGINX_SYMLINK" ]; then
  sudo rm "$NGINX_SYMLINK"
fi
sudo ln -s "$NGINX_CONFIG" "$NGINX_SYMLINK"

# Test Nginx configuration and restart
sudo nginx -t
sudo systemctl restart nginx

# Print deployment status
echo "--------------------------------------------------"
echo "Streamlit Application Deployment Complete!"
echo "Access your app at http://$DOMAIN_NAME"
echo "--------------------------------------------------"

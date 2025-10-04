#!/bin/bash

# AWS EC2 Deployment Script for Trust-First Agentic Web Explainer
# Run this script on your Ubuntu 22.04 EC2 instance

set -e  # Exit on any error

echo "🚀 Starting AWS EC2 deployment for Trust-First Agentic Web Explainer..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    print_error "Please don't run this script as root. Use a regular user with sudo privileges."
    exit 1
fi

# Update system
print_status "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install required packages
print_status "Installing required packages..."
sudo apt install -y python3-pip python3-venv git nginx certbot python3-certbot-nginx curl

# Create project directory
print_status "Setting up project directory..."
cd /home/$USER
if [ -d "nanda-agent" ]; then
    print_warning "nanda-agent directory already exists. Backing up..."
    mv nanda-agent nanda-agent-backup-$(date +%Y%m%d_%H%M%S)
fi

# Clone repository (replace with your actual repository URL)
print_status "Cloning repository..."
git clone https://github.com/yourusername/nanda-agent.git
cd nanda-agent

# Set up Python environment
print_status "Setting up Python virtual environment..."
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Configure environment variables
print_status "Setting up environment variables..."
if [ ! -f ".env" ]; then
    cp env.example .env
    print_warning "Please edit .env file with your API keys and configuration:"
    print_warning "nano .env"
    print_warning "Required: OPENAI_API_KEY, ANTHROPIC_API_KEY, DOMAIN_NAME"
    read -p "Press Enter after you've configured the .env file..."
fi

# Test the application
print_status "Testing the application..."
python test_agent.py

# Create systemd service for the main application
print_status "Creating systemd service for main application..."
sudo tee /etc/systemd/system/nanda-agent.service > /dev/null <<EOF
[Unit]
Description=NANDA Agent Service
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=/home/$USER/nanda-agent
Environment=PATH=/home/$USER/nanda-agent/.venv/bin
ExecStart=/home/$USER/nanda-agent/.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Create systemd service for NANDA integration
print_status "Creating systemd service for NANDA integration..."
sudo tee /etc/systemd/system/nanda-integration.service > /dev/null <<EOF
[Unit]
Description=NANDA Integration Service
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=/home/$USER/nanda-agent
Environment=PATH=/home/$USER/nanda-agent/.venv/bin
ExecStart=/home/$USER/nanda-agent/.venv/bin/python nanda_integration.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start services
print_status "Enabling and starting services..."
sudo systemctl daemon-reload
sudo systemctl enable nanda-agent
sudo systemctl start nanda-agent

# Check if domain is configured
if grep -q "DOMAIN_NAME=" .env && ! grep -q "DOMAIN_NAME=localhost" .env; then
    print_status "Domain configured, enabling NANDA integration..."
    sudo systemctl enable nanda-integration
    sudo systemctl start nanda-integration
else
    print_warning "No domain configured. NANDA integration will be skipped."
    print_warning "To enable later, set DOMAIN_NAME in .env and run:"
    print_warning "sudo systemctl enable nanda-integration && sudo systemctl start nanda-integration"
fi

# Configure Nginx
print_status "Configuring Nginx..."

# Get domain name from .env file
DOMAIN_NAME=$(grep "DOMAIN_NAME=" .env | cut -d'=' -f2 | tr -d '"' | tr -d "'")

if [ -z "$DOMAIN_NAME" ] || [ "$DOMAIN_NAME" = "localhost" ]; then
    print_warning "No domain configured. Using IP-based configuration."
    DOMAIN_NAME="_"
fi

sudo tee /etc/nginx/sites-available/nanda-agent > /dev/null <<EOF
server {
    listen 80;
    server_name $DOMAIN_NAME;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    location /health {
        proxy_pass http://127.0.0.1:8000/health;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Enable Nginx site
sudo ln -sf /etc/nginx/sites-available/nanda-agent /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx

# Set up firewall
print_status "Configuring firewall..."
sudo ufw --force enable
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'

# Create backup directory and script
print_status "Setting up backup system..."
mkdir -p /home/$USER/backups

sudo tee /home/$USER/backup.sh > /dev/null <<EOF
#!/bin/bash
DATE=\$(date +%Y%m%d_%H%M%S)
tar -czf /home/$USER/backups/nanda-agent-\$DATE.tar.gz /home/$USER/nanda-agent
find /home/$USER/backups -name "*.tar.gz" -mtime +7 -delete
EOF

chmod +x /home/$USER/backup.sh

# Add backup to crontab
(crontab -l 2>/dev/null; echo "0 2 * * * /home/$USER/backup.sh") | crontab -

# Check service status
print_status "Checking service status..."
sudo systemctl status nanda-agent --no-pager

if systemctl is-enabled --quiet nanda-integration; then
    sudo systemctl status nanda-integration --no-pager
fi

# Get public IP
PUBLIC_IP=$(curl -s http://checkip.amazonaws.com/)

print_status "Deployment completed successfully! 🎉"
echo ""
echo "📋 Deployment Summary:"
echo "====================="
echo "• Application: Running on port 8000"
echo "• Nginx: Configured as reverse proxy"
echo "• Services: Enabled and started"
echo "• Firewall: Configured"
echo "• Backups: Scheduled daily at 2 AM"
echo ""
echo "🌐 Access URLs:"
echo "• Health Check: http://$PUBLIC_IP/health"
echo "• Chat API: http://$PUBLIC_IP/chat"
if [ "$DOMAIN_NAME" != "_" ] && [ "$DOMAIN_NAME" != "localhost" ]; then
    echo "• Domain: http://$DOMAIN_NAME"
    echo ""
    echo "🔒 SSL Certificate:"
    echo "Run: sudo certbot --nginx -d $DOMAIN_NAME"
fi
echo ""
echo "📊 Monitoring:"
echo "• Application logs: sudo journalctl -u nanda-agent -f"
echo "• Nginx logs: sudo tail -f /var/log/nginx/access.log"
echo "• Service status: sudo systemctl status nanda-agent"
echo ""
echo "🔧 Next Steps:"
echo "1. Test your endpoints"
echo "2. Set up SSL certificate (if using domain)"
echo "3. Configure monitoring alerts"
echo "4. Set up log rotation"
echo ""
print_status "Your Trust-First Agentic Web Explainer is now live! 🤖🌐"

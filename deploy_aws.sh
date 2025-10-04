#!/bin/bash

# AWS EC2 Deployment Script for Trust-First Agentic Web Explainer
#
# This helper automates dependency installation, FastAPI + NANDA services,
# and the Nginx reverse proxy configuration on an Ubuntu 22.04 host. Copy
# the repository (or at least this file) to your EC2 instance and execute it
# as the non-root user (e.g. `ubuntu`) after setting the repository URL and
# environment secrets.
#
# Usage examples:
#   REPO_URL="https://github.com/my-org/nanda-agent.git" ./deploy_aws.sh
#   ./deploy_aws.sh --repo https://github.com/my-org/nanda-agent.git --branch main
#
# Required application secrets (see README for full list):
#   OPENAI_API_KEY, and for NANDA integration, ANTHROPIC_API_KEY & DOMAIN_NAME.
# These should be populated in the `.env` file the script prepares from
# `env.example`.

set -e

echo "🚀 Starting AWS EC2 deployment for Trust-First Agentic Web Explainer..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging helpers
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

usage() {
    cat <<USAGE
Usage: ${0##*/} [--repo <git-url>] [--branch <name>]

Options:
  -r, --repo      Git repository to clone on the EC2 host. Defaults to the
                  value of $REPO_URL or https://github.com/yourusername/nanda-agent.git.
  -b, --branch    Branch to checkout after cloning. Defaults to $REPO_BRANCH or main.
  -h, --help      Show this help message and exit.

Run this script as a non-root user with sudo privileges.
USAGE
}

REPO_URL_DEFAULT="https://github.com/yourusername/nanda-agent.git"
REPO_URL="${REPO_URL:-$REPO_URL_DEFAULT}"
REPO_BRANCH="${REPO_BRANCH:-main}"

while [ "$#" -gt 0 ]; do
    case "$1" in
        -r|--repo)
            shift
            [ -n "${1:-}" ] || { print_error "Missing value for --repo"; exit 1; }
            REPO_URL="$1"
            ;;
        -b|--branch)
            shift
            [ -n "${1:-}" ] || { print_error "Missing value for --branch"; exit 1; }
            REPO_BRANCH="$1"
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
    shift
done

if [ -z "$REPO_URL" ]; then
    print_error "A Git repository URL is required. Provide it via --repo or $REPO_URL."
    exit 1
fi

# Guardrails
if [ "$EUID" -eq 0 ]; then
    print_error "Please don't run this script as root. Use a regular user with sudo privileges."
    exit 1
fi

if command -v lsb_release >/dev/null 2>&1; then
    UBUNTU_VERSION=$(lsb_release -rs)
    if [ "$UBUNTU_VERSION" != "22.04" ]; then
        print_warning "This script was tested on Ubuntu 22.04. You are on ${UBUNTU_VERSION}."
    fi
else
    print_warning "Unable to detect Ubuntu version (lsb_release missing). Proceed with caution."
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

# Clone repository
print_status "Cloning repository..."
git clone "$REPO_URL" nanda-agent
cd nanda-agent

if [ -n "$REPO_BRANCH" ]; then
    print_status "Checking out branch $REPO_BRANCH..."
    if git fetch origin "$REPO_BRANCH"; then
        git checkout "$REPO_BRANCH"
    else
        print_warning "Unable to fetch branch $REPO_BRANCH. Continuing with the default branch."
    fi
fi

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
    print_warning "Required: OPENAI_API_KEY, optional: ANTHROPIC_API_KEY, DOMAIN_NAME"
    read -p "Press Enter after you've configured the .env file..."
fi

# Test the application
print_status "Testing the application..."
if ! python test_agent.py; then
    print_warning "Tests failed. Investigate before exposing the service publicly."
fi

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
ExecStart=/home/$USER/nanda-agent/.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8080
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
EnvironmentFile=/home/$USER/nanda-agent/.env
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
if grep -q "^DOMAIN_NAME=" .env && ! grep -q "^DOMAIN_NAME=localhost" .env; then
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
DOMAIN_NAME=$(grep "^DOMAIN_NAME=" .env | cut -d'=' -f2- | tr -d '"' | tr -d "'" )

if [ -z "$DOMAIN_NAME" ] || [ "$DOMAIN_NAME" = "localhost" ]; then
    print_warning "No domain configured. Using IP-based configuration."
    DOMAIN_NAME="_"
fi

sudo tee /etc/nginx/sites-available/nanda-agent > /dev/null <<EOF
server {
    listen 80;
    server_name $DOMAIN_NAME;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    location /health {
        proxy_pass http://127.0.0.1:8080/health;
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

sudo tee /home/$USER/backup.sh > /dev/null <<'EOS'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
tar -czf /home/$USER/backups/nanda-agent-$DATE.tar.gz /home/$USER/nanda-agent
find /home/$USER/backups -name "*.tar.gz" -mtime +7 -delete
EOS

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
echo "• Application: Running on port 8080"
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

# NANDA Agent - Trust-First Agentic Web Explainer

A LangChain-powered agent that answers questions about MCP/A2A/agentic web concepts and can read URLs to provide summaries with trust/interop themes.

## Features

- **Trust-First Focus**: Specializes in MCP, A2A, agent interoperability, trust/reputation layers
- **URL Reading**: Can fetch, extract, and summarize content from provided URLs
- **Citation-Aware**: Provides clear citations and marks assumptions/limitations
- **NANDA Compatible**: Wrapped with FastAPI for NANDA adapter integration

## Quick Start

### Local Development

**Quick Setup (Windows)**
```cmd
# Run the automated setup script
setup_windows.bat
```

**Manual Setup**
1. **Setup Environment**
   ```bash
   # Create virtual environment
   python -m venv .venv
   
   # Activate virtual environment
   # On Windows (PowerShell/CMD):
   .venv\Scripts\activate
   # On Unix/Linux/macOS:
   source .venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   ```bash
   # On Windows (PowerShell/CMD):
   copy env.example .env
   # On Unix/Linux/macOS:
   cp env.example .env
   
   # Edit .env and add your OpenAI API key
   ```

3. **Run the Agent**
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8080
   ```

4. **Test the Agent**
   ```bash
   # Test the agent directly
   python test_agent.py
   
   # Or test via API (if server is running)
   curl -X POST http://127.0.0.1:8080/chat \
     -H "Content-Type: application/json" \
     -d '{"messages":[{"role":"user","content":"In 3 bullets, what is MCP?"}]}'
   ```

### NANDA Adapter Integration

The project includes a complete NANDA integration that makes your agent globally discoverable and interoperable.

1. **Setup Environment Variables**
   ```bash
   export ANTHROPIC_API_KEY="your-anthropic-key-here"
   export DOMAIN_NAME="your-domain.com"  # Must point to your server IP
   ```

2. **Generate SSL Certificates** (for production)
   ```bash
   sudo certbot certonly --standalone -d your-domain.com
   sudo cp -L /etc/letsencrypt/live/your-domain.com/fullchain.pem .
   sudo cp -L /etc/letsencrypt/live/your-domain.com/privkey.pem .
   sudo chown $USER:$USER fullchain.pem privkey.pem
   chmod 600 fullchain.pem privkey.pem
   ```

3. **Run with NANDA Integration**
   ```bash
   python nanda_integration.py
   ```

4. **Get Your Agent Enrollment Link**
   - Check the console output for your agent's enrollment link
   - Visit the link to register your agent in the global NANDA network
   - Your agent will be discoverable by other agents worldwide!

## API Endpoints

- `GET /health` - Health check
- `POST /chat` - Chat with the agent

### Chat Request Format
```json
{
  "messages": [
    {"role": "user", "content": "Your question here"}
  ]
}
```

### Chat Response Format
```json
{
  "reply": "Agent response here"
}
```

## Environment Variables

### For Local Development (FastAPI)
- `OPENAI_API_KEY` - Your OpenAI API key (required)
- `MODEL` - OpenAI model to use (default: gpt-4o-mini)
- `HOST` - Server host (default: 0.0.0.0)
- `PORT` - Server port (default: 8080)
- `NANDA_SHARED_SECRET` - Optional shared secret for adapter authentication

### For NANDA Integration (Global Agent Network)
- `ANTHROPIC_API_KEY` - Your Anthropic API key (required for NANDA)
- `DOMAIN_NAME` - Your domain name for SSL certificates (required for NANDA)
- `AGENT_ID` - Custom agent ID (optional, auto-generated if not provided)
- `PORT` - Agent bridge port (optional, default: 6000)

## Deployment Options

You have two deployment options:

### Option 1: Local FastAPI Server
- **Use case**: Local development, testing, or private deployment
- **Features**: REST API endpoints, health checks
- **Command**: `uvicorn app.main:app --host 0.0.0.0 --port 8080`

### Option 2: NANDA Global Agent Network
- **Use case**: Global agent interoperability, public agent discovery
- **Features**: SSL certificates, global agent registry, A2A communication
- **Command**: `python nanda_integration.py`

## Deployment

### AWS EC2 (Ubuntu 22.04)

1. **Provision EC2**
   - Instance: t3.small
   - OS: Ubuntu 22.04 LTS
   - Security Group: Open ports 22, 80, 443, 8080

2. **System Setup**
   ```bash
   sudo apt update && sudo apt -y install git python3.10-venv python3-pip nginx
   git clone https://github.com/youruser/nanda-agent.git
   cd nanda-agent
   python3 -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   cp env.example .env
   # Edit .env with your API key
   ```

3. **Choose Deployment Mode**

   **Option A: FastAPI Server (Local/Private)**
   ```bash
   sudo tee /etc/systemd/system/nanda-agent.service > /dev/null <<EOF
   [Unit]
   Description=Nanda Agent (FastAPI)
   After=network.target

   [Service]
   User=ubuntu
   WorkingDirectory=/home/ubuntu/nanda-agent
   Environment="PATH=/home/ubuntu/nanda-agent/.venv/bin"
   ExecStart=/home/ubuntu/nanda-agent/.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8080
   Restart=always

   [Install]
   WantedBy=multi-user.target
   EOF
   ```

   **Option B: NANDA Global Agent (Public/Interoperable)**
   ```bash
   # Set environment variables
   export ANTHROPIC_API_KEY="your-anthropic-key"
   export DOMAIN_NAME="your-domain.com"
   
   # Generate SSL certificates
   sudo certbot certonly --standalone -d your-domain.com
   sudo cp -L /etc/letsencrypt/live/your-domain.com/fullchain.pem .
   sudo cp -L /etc/letsencrypt/live/your-domain.com/privkey.pem .
   sudo chown $USER:$USER fullchain.pem privkey.pem
   chmod 600 fullchain.pem privkey.pem
   
   # Create systemd service for NANDA
   sudo tee /etc/systemd/system/nanda-agent.service > /dev/null <<EOF
   [Unit]
   Description=Nanda Agent (Global Network)
   After=network.target

   [Service]
   User=ubuntu
   WorkingDirectory=/home/ubuntu/nanda-agent
   Environment="PATH=/home/ubuntu/nanda-agent/.venv/bin"
   Environment="ANTHROPIC_API_KEY=your-anthropic-key"
   Environment="DOMAIN_NAME=your-domain.com"
   ExecStart=/home/ubuntu/nanda-agent/.venv/bin/python nanda_integration.py
   Restart=always

   [Install]
   WantedBy=multi-user.target
   EOF
   ```

   **Start the Service**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable --now nanda-agent
   sudo systemctl status nanda-agent
   ```

4. **Optional Nginx Reverse Proxy**
   ```bash
   sudo tee /etc/nginx/sites-available/nanda > /dev/null <<EOF
   server {
     listen 80;
     server_name _;

     location / {
       proxy_pass http://127.0.0.1:8080;
       proxy_set_header Host \$host;
       proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
     }
   }
   EOF

   sudo ln -s /etc/nginx/sites-available/nanda /etc/nginx/sites-enabled/nanda
   sudo nginx -t && sudo systemctl restart nginx
   ```

## Architecture

```
nanda-agent/
├─ adapter/                         # NANDA adapter (git submodule)
├─ app/
│  ├─ main.py                       # FastAPI server
│  ├─ agent.py                      # LangChain agent
│  ├─ tools.py                      # URL fetch + extract
│  ├─ config.py                     # Environment config
│  ├─ prompts.py                    # System prompts
│  └─ __init__.py
├─ requirements.txt
├─ .env.example
└─ README.md
```

## Demo

The agent can:
- Answer questions about MCP, A2A, agent interoperability
- Fetch and summarize content from URLs
- Highlight trust, governance, and interoperability themes
- Provide citation-aware responses with clear limitations

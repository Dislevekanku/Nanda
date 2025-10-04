# Deploying the NANDA Agent to AWS EC2

This guide walks through provisioning an Ubuntu 22.04 EC2 instance and using the bundled `deploy_aws.sh` helper to configure the FastAPI service, optional NANDA bridge, and Nginx reverse proxy.

## 1. Provision the Instance

1. Log into the AWS console and launch an EC2 instance:
   - **AMI**: Ubuntu Server 22.04 LTS (HVM), 64-bit (x86)
   - **Instance Type**: `t3.small` or larger
   - **Storage**: 20 GB gp3 (adjust for your workload)
   - **Security Group**: allow inbound TCP 22 (SSH), 80 (HTTP), 443 (HTTPS), and 8080 (direct API access if desired).
2. Generate or select an SSH key pair and note the public IP address once the instance is running.

## 2. Prepare the Host

1. SSH into the instance using the `ubuntu` user:
   ```bash
   ssh -i /path/to/key.pem ubuntu@<public-ip>
   ```
2. Copy the repository (or at minimum `deploy_aws.sh`) to the instance. Example using `scp`:
   ```bash
   scp -i /path/to/key.pem -r . ubuntu@<public-ip>:~/nanda-agent
   ```
3. If you copied just the script, make it executable:
   ```bash
   chmod +x deploy_aws.sh
   ```

## 3. Run the Deployment Script

The script can infer the Git repository from the `REPO_URL` environment variable or accept flags. Run it as the `ubuntu` user (not root):

```bash
REPO_URL="https://github.com/<your-org>/nanda-agent.git" \
REPO_BRANCH="main" \
./deploy_aws.sh
```

### Script Features

- System updates and dependency installation (Python, Nginx, Certbot)
- Project checkout, virtual environment creation, and dependency install
- Prompts to populate `.env` secrets (OpenAI, Anthropic, domain)
- Systemd services for `uvicorn` (port 8080) and optional `nanda_integration.py`
- Nginx reverse proxy + health route
- UFW firewall configuration
- Rolling backup script scheduled via cron

> **Note:** The script pauses until you finish editing the `.env` file. Open it in `nano` (or your editor) and set the required API keys before continuing.

## 4. Post-Deployment Checks

1. Confirm the services are active:
   ```bash
   sudo systemctl status nanda-agent
   sudo systemctl status nanda-integration  # only if DOMAIN_NAME is set
   ```
2. Hit the health endpoint from your local machine:
   ```bash
   curl http://<public-ip>/health
   ```
3. (Optional) If you configured a domain, request an SSL certificate:
   ```bash
   sudo certbot --nginx -d <your-domain>
   ```

## 5. Updating the Deployment

When you push updates to the repository, SSH into the instance and deploy the latest code:

```bash
cd ~/nanda-agent
source .venv/bin/activate
git pull
pip install -r requirements.txt
sudo systemctl restart nanda-agent
sudo systemctl restart nanda-integration  # if enabled
```

For larger changes, you can rerun `deploy_aws.sh`; it will back up the existing directory before recloning.

## 6. Troubleshooting Tips

- Check FastAPI logs: `sudo journalctl -u nanda-agent -f`
- Check NANDA bridge logs: `sudo journalctl -u nanda-integration -f`
- Inspect Nginx access logs: `sudo tail -f /var/log/nginx/access.log`
- Validate firewall rules: `sudo ufw status`

If the health check fails, ensure the `.env` file contains a valid `OPENAI_API_KEY` and rerun the tests manually with `python test_agent.py`.

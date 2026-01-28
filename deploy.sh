#!/bin/bash
# deploy.sh - Deploy to Cloudflare Workers

set -e

echo "==================================="
echo "Runna to Intervals.icu Converter"
echo "Cloudflare Workers Deployment"
echo "==================================="
echo ""

# Check if wrangler is installed
if ! command -v wrangler &> /dev/null; then
    echo "Error: wrangler CLI not found"
    echo "Install it with: npm install -g wrangler"
    exit 1
fi

# Check if logged in
if ! wrangler whoami &> /dev/null; then
    echo "Logging in to Cloudflare..."
    wrangler login
fi

echo "Setting up secrets..."
echo ""

# Prompt for ICS URL if not set
if ! wrangler secret list | grep -q "ICS_URL"; then
    echo "ICS_URL secret not found."
    read -p "Enter your Runna calendar ICS URL: " ics_url
    if [ -n "$ics_url" ]; then
        echo "$ics_url" | wrangler secret put ICS_URL
    else
        echo "Warning: ICS_URL not set"
    fi
else
    echo "ICS_URL already set"
fi

# Optional: Set output path
read -p "Set custom output path? (leave empty to skip): " output_path
if [ -n "$output_path" ]; then
    echo "$output_path" | wrangler secret put OUTPUT_PATH
fi

echo ""
echo "Deploying to Cloudflare Workers..."
wrangler deploy

echo ""
echo "==================================="
echo "Deployment complete!"
echo "==================================="
echo ""
echo "Your worker is now scheduled to run based on the cron trigger."
echo "View logs with: wrangler tail"
echo "Test manually: wrangler dispatch scheduled"
echo ""

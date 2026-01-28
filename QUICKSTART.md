# Quick Start Guide

## Local Execution (Recommended for Testing)

### Option 1: API Upload (Recommended)
```bash
# Direct upload to intervals.icu
python3 runna_to_intervals.py \
  --url "https://cal.runna.com/your-calendar.ics" \
  --api-upload \
  --athlete-id "i12345" \
  --api-key "your_api_key"
```

### Option 2: Save to JSON File
```bash
# Save as JSON for manual import
python3 runna_to_intervals.py \
  --url "https://cal.runna.com/your-calendar.ics" \
  --output "workouts.json"
```

### Option 3: Interactive Mode
```bash
python3 runna_to_intervals.py --interactive
```

### Option 4: With Environment Variables
```bash
export ICS_URL="https://cal.runna.com/your-calendar.ics"
export INTERVALS_ATHLETE_ID="i12345"
export INTERVALS_API_KEY="your_api_key"
python3 runna_to_intervals.py --api-upload
```

### Option 5: Using the Shell Script
```bash
# Edit env.example and save as .env
cp env.example .env
# Edit .env with your credentials

# Run the script
./run.sh
```

## Get Your intervals.icu Credentials

**Athlete ID:**
- URL: `https://intervals.icu/athletes/i12345` → ID is `i12345`

**API Key:**
- Go to https://intervals.icu/settings
- Generate API Key under "Developer Settings"

## Cloudflare Workers Deployment

### Prerequisites
```bash
npm install -g wrangler
```

### Quick Deploy
```bash
# Login to Cloudflare
wrangler login

# Set your ICS URL
echo "https://your-calendar.ics" | wrangler secret put ICS_URL

# Deploy
wrangler deploy

# Verify deployment
wrangler tail
```

### Test Scheduled Trigger
```bash
# Manually trigger scheduled event
wrangler dispatch scheduled

# View logs
wrangler tail --format pretty
```

## Log Levels

### DEBUG - Detailed Information
```bash
python3 runna_to_intervals.py --url "$ICS_URL" --log-level DEBUG
```
Shows: HTTP details, parsing steps, intensity matching, interval detection

### INFO - Standard Operation (Default)
```bash
python3 runna_to_intervals.py --url "$ICS_URL" --log-level INFO
```
Shows: Major operations, workout counts, file confirmations

### ERROR - Errors Only
```bash
python3 runna_to_intervals.py --url "$ICS_URL" --log-level ERROR
```
Shows: Only errors

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `ICS_URL` | Yes | - | URL to ICS calendar file |
| `INTERVALS_ATHLETE_ID` | For API | - | Your intervals.icu athlete ID |
| `INTERVALS_API_KEY` | For API | - | Your intervals.icu API key |
| `OUTPUT_PATH` | No | `intervals_icu_workouts.json` | Output file path |
| `LOG_LEVEL` | No | `INFO` | Logging level |
| `LOG_JSON` | No | `false` | Use JSON logging |

## Comparison: API Upload vs JSON Export

### API Upload (Recommended)
✅ Automatic - workouts appear in intervals.icu immediately
✅ No manual import needed
✅ Can be automated with cron/scheduler
✅ Error feedback in real-time

### JSON Export
✅ Review workouts before importing
✅ Can be edited manually
✅ No API credentials needed
✅ Portable format

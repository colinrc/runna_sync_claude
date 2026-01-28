# Using the intervals.icu API

The converter now supports direct upload to intervals.icu via their API, eliminating the need for manual JSON file imports.

## Setup

### 1. Get Your intervals.icu Credentials

**Athlete ID:**
- Log in to intervals.icu
- Look at your profile URL: `https://intervals.icu/athletes/i12345`
- Your athlete ID is `i12345`

**API Key:**
- Go to https://intervals.icu/settings
- Scroll to "Developer Settings"
- Click "Generate API Key" or copy your existing key
- Save this securely - you won't be able to see it again

### 2. Configure Environment Variables

```bash
# Add to your .env file
INTERVALS_ATHLETE_ID=i12345
INTERVALS_API_KEY=your_api_key_here
```

## Usage

### Command Line with API Upload

```bash
# Upload workouts directly to intervals.icu
python3 runna_to_intervals.py \
  --url "https://cal.runna.com/your-calendar.ics" \
  --api-upload \
  --athlete-id "i12345" \
  --api-key "your_api_key"

# Or using environment variables
export INTERVALS_ATHLETE_ID="i12345"
export INTERVALS_API_KEY="your_api_key"
python3 runna_to_intervals.py \
  --url "https://cal.runna.com/your-calendar.ics" \
  --api-upload
```

### Save to JSON (Traditional Method)

```bash
# Save as JSON file for manual import
python3 runna_to_intervals.py \
  --url "https://cal.runna.com/your-calendar.ics" \
  --output "workouts.json"
```

### Programmatic Usage

```python
from runna_to_intervals import RunnaWorkoutConverter, IntervalsICUAPI, StructuredLogger

# Setup
logger = StructuredLogger(level='INFO', use_json=False)
api_client = IntervalsICUAPI(
    athlete_id='i12345',
    api_key='your_api_key',
    logger=logger
)

# Convert and upload
converter = RunnaWorkoutConverter(
    ics_url='https://cal.runna.com/your-calendar.ics',
    logger=logger,
    api_client=api_client
)

# This will automatically upload to intervals.icu
workouts = converter.process_calendar(upload_to_api=True)

print(f"Uploaded {len(workouts)} workouts")
```

### Upload a Single Workout

```python
from runna_to_intervals import IntervalsICUAPI

api = IntervalsICUAPI('i12345', 'your_api_key')

workout = {
    "name": "Easy Run",
    "description": "30 min easy",
    "workout_date": "2026-02-05",
    "steps": [
        {
            "duration": 1800,
            "durationType": "time",
            "targetType": "pace",
            "target": 1,
            "text": "30min easy"
        }
    ]
}

result = api.create_workout(workout)
if result:
    print(f"Workout created with ID: {result['id']}")
```

## API Operations

The `IntervalsICUAPI` class supports:

### Create Workout
```python
api.create_workout(workout_dict)
```

### Update Workout
```python
api.update_workout(workout_id, updated_workout_dict)
```

### Get Workouts
```python
# Get all workouts
workouts = api.get_workouts()

# Get workouts in date range
workouts = api.get_workouts(
    start_date='2026-02-01',
    end_date='2026-02-28'
)
```

### Delete Workout
```python
api.delete_workout(workout_id)
```

## Cloudflare Workers with API

Update your Cloudflare Worker secrets:

```bash
# Add API credentials
echo "i12345" | wrangler secret put INTERVALS_ATHLETE_ID
echo "your_api_key" | wrangler secret put INTERVALS_API_KEY

# Enable API upload
echo "true" | wrangler secret put API_UPLOAD
```

## Troubleshooting

### Authentication Errors

**Error:** "401 Unauthorized"
- Check your API key is correct
- Regenerate API key in intervals.icu settings if needed

**Error:** "403 Forbidden"
- Verify your athlete ID is correct
- Ensure API key has necessary permissions

### Upload Failures

**Error:** "422 Unprocessable Entity"
- Workout data format is incorrect
- Check that required fields are present
- Enable `--log-level DEBUG` to see request details

### Rate Limiting

intervals.icu may rate limit API requests. The script handles this gracefully but you may see:
- Slower uploads with many workouts
- Temporary failures that retry automatically

## Advantages of API Upload

✅ **Automatic:** No manual import required
✅ **Batch Processing:** Upload multiple workouts at once
✅ **Scheduled:** Can be automated with cron or Cloudflare Workers
✅ **Error Handling:** Immediate feedback on success/failure
✅ **Integration:** Easy to integrate into other workflows

## Security Notes

- **Never commit API keys** to version control
- Use environment variables or secrets management
- Rotate API keys periodically
- Limit API key permissions if possible

## API Documentation

Full intervals.icu API documentation:
https://intervals.icu/api/

## Example: Scheduled Daily Upload

```bash
#!/bin/bash
# daily-upload.sh

export ICS_URL="https://cal.runna.com/your-calendar.ics"
export INTERVALS_ATHLETE_ID="i12345"
export INTERVALS_API_KEY="your_api_key"

python3 runna_to_intervals.py --api-upload --log-level INFO

# Add to crontab for daily 2 AM runs:
# 0 2 * * * /path/to/daily-upload.sh >> /var/log/runna-sync.log 2>&1
```

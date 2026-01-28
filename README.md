# runna_sync_claude

Automatically sync your Runna workouts to intervals.icu with structured interval parsing and direct API upload.

## 🎯 Features

- ✅ **Automatic sync** from Runna calendar (ICS) to intervals.icu
- ✅ **Direct API upload** - no manual import needed
- ✅ **Intelligent parsing** - converts workout descriptions to structured intervals
- ✅ **Multiple execution modes** - CLI, scheduled (cron/Cloudflare), or programmatic
- ✅ **Structured logging** - JSON or text format with DEBUG/INFO levels
- ✅ **Handles complex workouts** - intervals, tempo, strides, progressive runs
- ✅ **Preserves original descriptions** - keeps Runna links and details
- ✅ **Flexible output** - API upload or JSON export

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get Your Credentials

**Runna Calendar URL:**
- Open Runna app → Settings → Calendar Sync
- Copy the ICS calendar URL

**intervals.icu Credentials:**
- **Athlete ID:** From your profile URL: `https://intervals.icu/athletes/i12345`
- **API Key:** Generate at [intervals.icu/settings](https://intervals.icu/settings) → Developer Settings

### 3. Configure

```bash
cp env.example .env
# Edit .env with your credentials
```

### 4. Run

**API Upload (Recommended):**
```bash
python3 runna_to_intervals.py \
  --url "https://cal.runna.com/your-calendar.ics" \
  --api-upload \
  --athlete-id "i12345" \
  --api-key "your_api_key"
```

**JSON Export:**
```bash
python3 runna_to_intervals.py \
  --url "https://cal.runna.com/your-calendar.ics" \
  --output "workouts.json"
```

## 📚 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Quick reference guide
- **[API_USAGE.md](API_USAGE.md)** - Complete API integration guide
- **[api_examples.py](api_examples.py)** - Interactive code examples

## 🔧 Usage Examples

### Command Line

```bash
# Upload all workouts to intervals.icu
python3 runna_to_intervals.py \
  --url "$ICS_URL" \
  --api-upload \
  --athlete-id "$ATHLETE_ID" \
  --api-key "$API_KEY" \
  --log-level INFO

# Save as JSON with debug logging
python3 runna_to_intervals.py \
  --url "$ICS_URL" \
  --output workouts.json \
  --log-level DEBUG

# Interactive mode
python3 runna_to_intervals.py --interactive
```

### Programmatic

```python
from runna_to_intervals import RunnaWorkoutConverter, IntervalsICUAPI

# Setup API client
api = IntervalsICUAPI(
    athlete_id='i12345',
    api_key='your_api_key'
)

# Convert and upload
converter = RunnaWorkoutConverter(
    ics_url='https://cal.runna.com/your-calendar.ics',
    api_client=api
)

workouts = converter.process_calendar(upload_to_api=True)
print(f"Uploaded {len(workouts)} workouts")
```

### Scheduled Sync (Cron)

```bash
# Add to crontab for daily 2 AM sync
0 2 * * * cd /path/to/runna_sync_claude && python3 runna_to_intervals.py --api-upload >> /var/log/runna-sync.log 2>&1
```

## 🏃 Workout Parsing

The converter intelligently parses Runna workout descriptions into structured intervals:

### Supported Formats

- **Structured intervals:** `5x(1km @ tempo, 2min recovery)`
- **Duration-based:** `30min easy`, `1h 15min moderate`
- **Distance-based:** `5km tempo`, `10x400m @ 5K pace`
- **Progressive runs:** Multiple pace segments
- **Strides/bursts:** `3x15s fast with 20s recovery`
- **Warm-up/cool-down:** Automatically detected

### Example Conversion

**Runna Description:**
```
3km warm up at conversational pace, add 3x 15s fast bursts
4 reps of:
• 1km at 4:50/km
• 200m at 4:20/km, 120s walking rest
2.2km cool down
```

**Converted to intervals.icu (with pace targets):**
- 3km warm-up @ Z1-Z3 (5:37-8:33/km)
- 3 × (15s fast @ 4:20/km + 20s recovery)
- 90s rest @ Z1 (5:50-8:33/km)
- 4 × (1km @ 4:50/km + 200m @ 4:20/km + 120s rest @ Z1)
- 2.2km cool-down @ Z1-Z3 (4:20-7:20/km)

### Pace Target System

The converter uses **pace targets** instead of perceived effort zones:

**Specific Pace Workouts:**
```
Runna: "1km at 4:50/km"
→ intervals.icu: 1km @ 4:50/km (290 sec/km target pace)
```

**Recovery/Rest Periods:**
- Calculated as Z1 recovery range (adds 1:00-2:30 to workout pace)
```
Runna: "120s walking rest" (after 4:50/km work)
→ intervals.icu: 120s Z1 @ 5:50-7:20/km (~0.26km)
```

**Warm-up/Cool-down:**
- Calculated as Z1-Z3 easy range (±0:30 to +2:30 from workout pace)
```
Runna: "3km warm up at conversational pace"
→ intervals.icu: 3km Z1-Z3 @ 4:20-7:20/km
```

| Workout Type | Runna Description | intervals.icu Output |
|--------------|-------------------|---------------------|
| Work Interval | "1km at 4:50/km" | 1km @ 4:50/km target |
| Recovery | "120s rest" | 120s Z1 range (calculated) |
| Easy/Warmup | "3km easy" | 3km Z1-Z3 range (calculated) |
| Fast Burst | "15s fast" | 15s @ specific pace |

## 🔐 Configuration

### Environment Variables

```bash
# Required
ICS_URL=https://cal.runna.com/your-calendar.ics

# For API Upload
INTERVALS_ATHLETE_ID=i12345
INTERVALS_API_KEY=your_api_key

# Optional
OUTPUT_PATH=workouts.json
LOG_LEVEL=INFO
LOG_JSON=false
```

### Command Line Arguments

```
--url              ICS calendar URL
--api-upload       Upload directly to intervals.icu
--athlete-id       Your intervals.icu athlete ID
--api-key          Your intervals.icu API key
--output           JSON output file (default: intervals_icu_workouts.json)
--log-level        DEBUG, INFO, WARNING, ERROR
--log-json         Use JSON log format
--interactive      Prompt for missing values
```

## 📊 Logging

### Text Format (Human-Readable)
```bash
[2026-01-28T10:00:00Z] INFO: Fetching calendar | url=https://...
[2026-01-28T10:00:01Z] INFO: Converted workout | name=K200s date=2026-02-04 steps=5
[2026-01-28T10:00:02Z] INFO: Workout created successfully | workout_id=12345
```

### JSON Format (Machine-Readable)
```json
{"timestamp":"2026-01-28T10:00:00Z","level":"INFO","message":"Fetching calendar","url":"https://..."}
{"timestamp":"2026-01-28T10:00:01Z","level":"INFO","message":"Converted workout","name":"K200s","date":"2026-02-04","steps":5}
```

## 🌐 Deployment Options

### Local / Server
```bash
# One-time sync
./run.sh

# Scheduled via cron
0 2 * * * /path/to/run.sh
```

### Cloudflare Workers
```bash
# Deploy scheduled worker
./deploy.sh

# Configure secrets
wrangler secret put ICS_URL
wrangler secret put INTERVALS_ATHLETE_ID
wrangler secret put INTERVALS_API_KEY

# Test
wrangler dispatch scheduled
```

See [wrangler.toml](wrangler.toml) for configuration.

## 🛠️ API Operations

The `IntervalsICUAPI` class provides full CRUD operations:

```python
from runna_to_intervals import IntervalsICUAPI

api = IntervalsICUAPI('i12345', 'your_api_key')

# Create workout
workout = api.create_workout(workout_dict)

# Update workout
api.update_workout(workout_id, updated_dict)

# Get workouts
workouts = api.get_workouts(start_date='2026-02-01', end_date='2026-02-28')

# Delete workout
api.delete_workout(workout_id)
```

## 📁 Project Structure

```
runna_sync_claude/
├── runna_to_intervals.py    # Main converter script
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── API_USAGE.md             # API integration guide
├── QUICKSTART.md            # Quick reference
├── api_examples.py          # Code examples
├── env.example              # Environment template
├── run.sh                   # Local execution helper
├── deploy.sh                # Cloudflare deployment
└── wrangler.toml            # Cloudflare config
```

## 🐛 Troubleshooting

### No workouts found
```bash
# Check calendar URL is accessible
curl -I "$ICS_URL"

# Use debug logging to see parsing
python3 runna_to_intervals.py --url "$ICS_URL" --log-level DEBUG
```

### API upload fails
```bash
# Verify credentials
# Athlete ID: Check your intervals.icu profile URL
# API Key: Regenerate at intervals.icu/settings

# Check error details
python3 runna_to_intervals.py --api-upload --log-level DEBUG
```

### Parsing issues
```bash
# Enable debug logging to see workout parsing
python3 runna_to_intervals.py --url "$ICS_URL" --log-level DEBUG

# Look for "Parsing workout" and "Found structured interval" messages
```

## 🔄 Syncing Strategy

### Initial Setup
1. Export all workouts to JSON first
2. Review the conversions
3. Manually import to intervals.icu
4. Verify workouts look correct

### Ongoing Sync
1. Set up scheduled sync (cron or Cloudflare)
2. Run daily or weekly
3. Check logs for errors
4. Workouts auto-upload to intervals.icu

### Handling Duplicates
The script doesn't check for duplicates. Options:
- Sync only future workouts (filter by date)
- Manually delete duplicates in intervals.icu
- Use date ranges with `--start-date` flag (future feature)

## 📝 License

MIT License

## 🙏 Acknowledgments

- **Runna** - For the excellent training app
- **intervals.icu** - For the powerful training platform
- **icalendar** - For ICS parsing capabilities

## 🔗 Useful Links

- [Runna App](https://runna.com)
- [intervals.icu](https://intervals.icu)
- [intervals.icu API Documentation](https://intervals.icu/api/)

---

**Made with ❤️ for runners who love data**

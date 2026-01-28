# Complete File Manifest for runna_sync_claude

This document lists all files in the project and their purposes.

## 📁 Project Structure

```
runna_sync_claude/
│
├── Core Files
│   ├── runna_to_intervals.py      # Main converter script with API integration
│   ├── requirements.txt            # Python dependencies
│   └── .gitignore                  # Git ignore rules (protects secrets)
│
├── Documentation
│   ├── README.md                   # Main project documentation
│   ├── API_USAGE.md               # Detailed API integration guide
│   ├── QUICKSTART.md              # Quick reference guide
│   ├── GITHUB_SETUP.md            # GitHub repository setup guide
│   └── LICENSE                    # MIT License
│
├── Configuration
│   ├── env.example                # Environment variable template
│   └── wrangler.toml              # Cloudflare Workers configuration
│
├── Scripts
│   ├── run.sh                     # Local execution helper script
│   ├── deploy.sh                  # Cloudflare deployment script
│   └── setup_git.sh               # Git repository setup script
│
└── Examples
    ├── api_examples.py            # Interactive API usage examples
    ├── example_usage.py           # General usage examples
    └── cloudflare_example.py      # Cloudflare integration notes
```

## 📄 File Details

### Core Files

#### `runna_to_intervals.py` (Main Script)
**Size:** ~800+ lines
**Purpose:** Primary converter script
**Features:**
- Fetches Runna ICS calendars
- Parses workout descriptions intelligently
- Converts to intervals.icu format
- Direct API upload capability
- Structured logging (JSON/text)
- Multiple execution modes

**Key Classes:**
- `StructuredLogger` - Logging with JSON support
- `IntervalsICUAPI` - API client for intervals.icu
- `RunnaWorkoutConverter` - Main conversion logic

**Usage:**
```bash
python3 runna_to_intervals.py --api-upload --athlete-id i12345 --api-key KEY
```

#### `requirements.txt`
**Purpose:** Python package dependencies
**Contents:**
- `requests>=2.31.0` - HTTP client
- `icalendar>=5.0.11` - ICS parsing
- `python-dateutil>=2.8.2` - Date utilities

**Usage:**
```bash
pip install -r requirements.txt
```

#### `.gitignore`
**Purpose:** Prevents committing sensitive files
**Protects:**
- `.env` files (secrets)
- API keys
- Virtual environments
- Output JSON files
- IDE settings
- Log files

### Documentation Files

#### `README.md` (Main Documentation)
**Sections:**
- Features overview
- Quick start guide
- Usage examples (CLI, programmatic, scheduled)
- Workout parsing explanation
- Configuration options
- Deployment strategies
- Troubleshooting
- API operations reference

#### `API_USAGE.md`
**Purpose:** Comprehensive API integration guide
**Covers:**
- Getting intervals.icu credentials
- Setup and configuration
- All API operations (CRUD)
- Security best practices
- Cloudflare Workers integration
- Error handling
- Programmatic examples

#### `QUICKSTART.md`
**Purpose:** Quick reference for common tasks
**Includes:**
- One-liner commands
- Environment variables table
- API vs JSON comparison
- Common troubleshooting

#### `GITHUB_SETUP.md`
**Purpose:** Guide for pushing to GitHub
**Includes:**
- Automated setup instructions
- Manual setup steps
- Troubleshooting authentication
- Repository configuration tips
- Branch management

#### `LICENSE`
**Type:** MIT License
**Permissions:**
- ✅ Commercial use
- ✅ Modification
- ✅ Distribution
- ✅ Private use

### Configuration Files

#### `env.example`
**Purpose:** Template for environment variables
**Variables:**
- `ICS_URL` - Runna calendar URL
- `INTERVALS_ATHLETE_ID` - Your athlete ID
- `INTERVALS_API_KEY` - Your API key
- `OUTPUT_PATH` - JSON output path
- `LOG_LEVEL` - Logging level
- `LOG_JSON` - JSON logging flag

**Setup:**
```bash
cp env.example .env
# Edit .env with your values
```

#### `wrangler.toml`
**Purpose:** Cloudflare Workers configuration
**Settings:**
- Worker name
- Cron schedule (default: daily 2 AM)
- Environment variables
- Limits and compatibility flags

### Script Files

#### `run.sh`
**Purpose:** Local execution helper
**Features:**
- Creates virtual environment
- Installs dependencies
- Runs converter with environment variables
- Interactive mode support

**Usage:**
```bash
./run.sh
```

#### `deploy.sh`
**Purpose:** Cloudflare Workers deployment
**Features:**
- Checks for wrangler CLI
- Manages authentication
- Sets up secrets
- Deploys worker
- Provides testing commands

**Usage:**
```bash
./deploy.sh
```

#### `setup_git.sh`
**Purpose:** Initialize and push to GitHub
**Features:**
- Initializes git repository
- Configures git user
- Stages and commits files
- Adds remote repository
- Pushes to GitHub
- Interactive prompts

**Usage:**
```bash
./setup_git.sh
```

### Example Files

#### `api_examples.py`
**Purpose:** Interactive API examples
**Includes:**
- Upload all workouts from calendar
- Export to JSON
- Upload single custom workout
- Get existing workouts
- Interactive menu

**Usage:**
```bash
python3 api_examples.py
```

#### `example_usage.py`
**Purpose:** General usage demonstrations
**Includes:**
- Test workout parsing
- Sample calendar creation
- Custom intensity mappings
- intervals.icu format examples

**Usage:**
```bash
python3 example_usage.py
```

#### `cloudflare_example.py`
**Purpose:** Cloudflare integration notes
**Contains:**
- JavaScript wrapper example
- Pages Functions example
- Deployment recommendations
- Architecture notes

## 🔐 Security Notes

### Files That Should NEVER Be Committed:
- `.env` - Contains your secrets
- `*_api_key*` - Any file with API keys
- `intervals_icu_workouts.json` - May contain personal data

### Protected by .gitignore:
✅ All sensitive files are in .gitignore
✅ Virtual environments excluded
✅ Output files excluded

## 📦 Complete File Checklist

Before pushing to GitHub, ensure you have:

- [x] runna_to_intervals.py
- [x] requirements.txt
- [x] .gitignore
- [x] README.md
- [x] API_USAGE.md
- [x] QUICKSTART.md
- [x] GITHUB_SETUP.md
- [x] LICENSE
- [x] env.example
- [x] wrangler.toml
- [x] run.sh
- [x] deploy.sh
- [x] setup_git.sh
- [x] api_examples.py
- [x] example_usage.py
- [x] cloudflare_example.py

**Total:** 16 files

## 📊 File Statistics

- **Python scripts:** 4 files (~1500+ lines)
- **Shell scripts:** 3 files (~300+ lines)
- **Documentation:** 5 files (~2000+ lines)
- **Configuration:** 4 files (~200+ lines)

**Total project:** ~4000+ lines of code and documentation

## 🚀 Quick Setup

1. **Download all files**
2. **Review .gitignore** - Ensure secrets are protected
3. **Configure environment:**
   ```bash
   cp env.example .env
   # Edit .env
   ```
4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
5. **Test locally:**
   ```bash
   ./run.sh
   ```
6. **Push to GitHub:**
   ```bash
   ./setup_git.sh
   ```

## 📝 Notes

- All scripts are executable (chmod +x applied)
- All documentation uses Markdown
- Python scripts follow PEP 8 guidelines
- Comprehensive error handling included
- Structured logging throughout
- Type hints where applicable

## 🔄 Keeping Updated

To update the repository after changes:

```bash
git add .
git commit -m "Description of changes"
git push origin main
```

## 🎯 Next Steps After Setup

1. ✅ Push to GitHub using setup_git.sh
2. Add badges to README (optional)
3. Set up GitHub Actions (optional)
4. Create initial release/tag
5. Share with community!

---

**Project ready for deployment! 🚀**

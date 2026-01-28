# GitHub Setup Guide

This guide will help you push this project to GitHub.

## Prerequisites

- Git installed on your system
- GitHub account
- GitHub repository created (or will create one)

## Option 1: Automated Setup (Recommended)

### Step 1: Run the setup script

```bash
./setup_git.sh
```

The script will:
1. Initialize git repository (if needed)
2. Configure git user (if needed)
3. Stage all files
4. Commit changes
5. Add remote repository
6. Push to GitHub

### Step 2: Follow the prompts

You'll be asked for:
- Your name and email (for git commits)
- Commit message
- GitHub repository URL
- Branch name preference (main/master)

## Option 2: Manual Setup

### Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `runna_sync_claude`
3. Description: `Sync Runna workouts to intervals.icu with API integration`
4. Choose Public or Private
5. **Do NOT initialize with README, .gitignore, or license**
6. Click "Create repository"

### Step 2: Initialize Local Repository

```bash
# Navigate to project directory
cd /path/to/runna_sync_claude

# Initialize git
git init

# Configure git user (if not already done)
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

### Step 3: Add Files

```bash
# Stage all files
git add .

# Check what will be committed
git status

# Commit
git commit -m "Initial commit: Runna to intervals.icu sync tool with API integration"
```

### Step 4: Connect to GitHub

**For HTTPS:**
```bash
git remote add origin https://github.com/YOUR_USERNAME/runna_sync_claude.git
git branch -M main
git push -u origin main
```

**For SSH:**
```bash
git remote add origin git@github.com:YOUR_USERNAME/runna_sync_claude.git
git branch -M main
git push -u origin main
```

### Step 5: Verify

Visit your repository on GitHub and verify all files are present.

## Files That Will Be Committed

```
runna_sync_claude/
├── .gitignore                    # Ignores secrets and temp files
├── README.md                     # Main documentation
├── API_USAGE.md                  # API integration guide
├── QUICKSTART.md                 # Quick reference
├── GITHUB_SETUP.md              # This file
├── runna_to_intervals.py         # Main script
├── requirements.txt              # Dependencies
├── env.example                   # Environment template
├── wrangler.toml                 # Cloudflare config
├── run.sh                        # Local execution helper
├── deploy.sh                     # Cloudflare deployment
├── setup_git.sh                  # Git setup helper
├── api_examples.py               # Code examples
├── example_usage.py              # Usage examples
└── cloudflare_example.py         # Cloudflare integration
```

## Important Security Notes

⚠️ **NEVER commit these files:**
- `.env` (contains secrets)
- Any files with API keys
- `intervals_icu_workouts.json` (may contain personal data)

These are already in `.gitignore`, but double-check before committing!

## Troubleshooting

### Authentication Issues

**HTTPS Authentication:**
- GitHub now requires personal access tokens
- Create one at: https://github.com/settings/tokens
- Use token as password when prompted

**SSH Authentication:**
- Set up SSH key: https://docs.github.com/en/authentication/connecting-to-github-with-ssh
- Add key to GitHub account

### Push Rejected

If push is rejected due to existing content:

```bash
# Option 1: Force push (overwrites remote)
git push -u origin main --force

# Option 2: Pull and merge first
git pull origin main --allow-unrelated-histories
git push -u origin main
```

### Wrong Branch Name

GitHub now defaults to `main` instead of `master`:

```bash
# Rename local branch
git branch -M main

# Push to new branch name
git push -u origin main
```

## Repository Settings (Optional)

After pushing, configure your repository:

### 1. Add Description
Settings → General → Description:
```
Automatically sync Runna workouts to intervals.icu with intelligent parsing and direct API upload
```

### 2. Add Topics
Settings → General → Topics:
```
running, intervals-icu, runna, workout-sync, python, icalendar, training, fitness
```

### 3. Enable Features
Settings → General → Features:
- ✅ Issues
- ✅ Discussions (optional)
- ✅ Wiki (optional)

### 4. Set Default Branch
Settings → Branches → Default branch: `main`

### 5. Branch Protection (Optional)
Settings → Branches → Add rule:
- Branch name: `main`
- ✅ Require pull request reviews before merging
- ✅ Require status checks to pass

## GitHub Actions (Optional)

Consider adding CI/CD:

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - run: pip install -r requirements.txt
      - run: python -m pytest
```

## Useful Git Commands

```bash
# View commit history
git log --oneline

# View remote URL
git remote -v

# Change remote URL
git remote set-url origin NEW_URL

# Pull latest changes
git pull origin main

# Create new branch
git checkout -b feature-name

# Push new branch
git push -u origin feature-name
```

## Next Steps

1. ✅ Push code to GitHub
2. Add README badges (optional)
3. Write CONTRIBUTING.md (optional)
4. Add LICENSE file
5. Create first release/tag
6. Share with community!

## Support

For GitHub-specific issues:
- [GitHub Docs](https://docs.github.com)
- [Git Documentation](https://git-scm.com/doc)

For project issues:
- Open an issue in your repository
- Check README.md for troubleshooting

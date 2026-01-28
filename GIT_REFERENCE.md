# Git Commands Reference

Quick reference for common git operations with this repository.

## 🚀 Quick Start

### First Time Setup

```bash
# Use the automated script
./git_push.sh
```

This will:
1. Initialize git repository
2. Add all files
3. Create first commit
4. Connect to GitHub
5. Push everything

### Manual Setup

```bash
# Initialize repo
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Runna to intervals.icu sync with pace targets"

# Add remote (replace USERNAME with your GitHub username)
git remote add origin https://github.com/USERNAME/runna_sync_claude.git

# Push
git branch -M main
git push -u origin main
```

## 📝 Daily Workflow

### Check Status
```bash
git status
```

### Add Changes
```bash
# Add all changes
git add .

# Add specific file
git add runna_to_intervals.py

# Add multiple files
git add README.md API_USAGE.md
```

### Commit Changes
```bash
# With message
git commit -m "fix: Correct pace calculation for recovery intervals"

# With detailed message
git commit -m "feat: Add support for mile-based paces" -m "Extended pace parser to handle min/mile format"
```

### Push to GitHub
```bash
# Push to current branch
git push

# First push of new branch
git push -u origin feature-name
```

## 🔍 Viewing Changes

### See What Changed
```bash
# Show unstaged changes
git diff

# Show staged changes
git diff --staged

# Show changes in specific file
git diff runna_to_intervals.py
```

### View History
```bash
# Recent commits
git log --oneline

# Last 5 commits with stats
git log -5 --stat

# Commits by author
git log --author="Your Name"

# Graphical history
git log --graph --oneline --all
```

## 🌿 Branch Management

### Create Branch
```bash
# Create and switch to new branch
git checkout -b feature-zone-ranges

# Create from specific commit
git checkout -b bugfix abc123
```

### Switch Branches
```bash
# Switch to existing branch
git checkout main

# Switch to previous branch
git checkout -
```

### List Branches
```bash
# Local branches
git branch

# Remote branches
git branch -r

# All branches
git branch -a
```

### Delete Branch
```bash
# Delete local branch (safe)
git branch -d feature-name

# Force delete
git branch -D feature-name

# Delete remote branch
git push origin --delete feature-name
```

## ↩️ Undoing Changes

### Unstage Files
```bash
# Unstage specific file
git restore --staged runna_to_intervals.py

# Unstage all
git restore --staged .
```

### Discard Changes
```bash
# Discard changes in file
git restore runna_to_intervals.py

# Discard all changes
git restore .
```

### Undo Last Commit
```bash
# Keep changes staged
git reset --soft HEAD~1

# Keep changes unstaged
git reset HEAD~1

# Discard changes (DANGER!)
git reset --hard HEAD~1
```

### Amend Last Commit
```bash
# Change commit message
git commit --amend -m "New message"

# Add forgotten files to last commit
git add forgotten_file.py
git commit --amend --no-edit
```

## 🔄 Syncing with Remote

### Pull Changes
```bash
# Pull from current branch
git pull

# Pull with rebase
git pull --rebase

# Pull specific branch
git pull origin main
```

### Fetch Changes
```bash
# Fetch all branches
git fetch

# Fetch specific remote
git fetch origin

# Fetch and prune deleted branches
git fetch -p
```

### Update Fork
```bash
# Add upstream remote (once)
git remote add upstream https://github.com/ORIGINAL/runna_sync_claude.git

# Fetch upstream
git fetch upstream

# Merge upstream changes
git checkout main
git merge upstream/main
git push
```

## 🏷️ Tags & Releases

### Create Tag
```bash
# Lightweight tag
git tag v1.0.0

# Annotated tag (recommended)
git tag -a v1.0.0 -m "Release version 1.0.0 with pace targets"

# Tag specific commit
git tag v1.0.0 abc123
```

### Push Tags
```bash
# Push specific tag
git push origin v1.0.0

# Push all tags
git push --tags
```

### List Tags
```bash
git tag

# With descriptions
git tag -n
```

## 🔧 Configuration

### Set User Info
```bash
# Global (all repos)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Local (this repo only)
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

### Set Default Branch
```bash
git config --global init.defaultBranch main
```

### View Config
```bash
# All settings
git config --list

# Specific setting
git config user.name
```

## 🛠️ Useful Aliases

Add to `~/.gitconfig`:

```ini
[alias]
    st = status
    co = checkout
    br = branch
    ci = commit
    unstage = restore --staged
    last = log -1 HEAD
    visual = log --graph --oneline --all
    amend = commit --amend --no-edit
```

Usage:
```bash
git st          # Instead of git status
git co main     # Instead of git checkout main
git visual      # See graph
```

## 🔐 Security

### Check for Secrets
```bash
# View what will be committed
git status

# Check if .env is ignored
git check-ignore .env

# List tracked files
git ls-files
```

### Remove Accidentally Committed File
```bash
# Remove from git but keep local file
git rm --cached .env

# Remove from history (DANGER - rewrites history)
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all
```

## 🆘 Common Issues

### "Permission denied (publickey)"
```bash
# Check SSH key
ssh -T git@github.com

# Generate new SSH key
ssh-keygen -t ed25519 -C "your.email@example.com"

# Add to GitHub: https://github.com/settings/keys
```

### "Updates were rejected"
```bash
# Pull first
git pull --rebase

# Or force push (DANGER if collaborating)
git push --force
```

### "Merge conflict"
```bash
# See conflicted files
git status

# Edit files to resolve conflicts
# Look for <<<<<<< HEAD markers

# Mark as resolved
git add resolved_file.py

# Continue
git commit
```

## 📚 Learning Resources

- [Git Documentation](https://git-scm.com/doc)
- [GitHub Guides](https://guides.github.com/)
- [Oh Shit, Git!?!](https://ohshitgit.com/)
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)

## ✅ Pre-Commit Checklist

Before committing:
- [ ] Code works and is tested
- [ ] No secrets in commit (.env, API keys)
- [ ] Meaningful commit message
- [ ] Files are staged correctly
- [ ] README updated if needed

Before pushing:
- [ ] Pulled latest changes
- [ ] No merge conflicts
- [ ] Tests pass
- [ ] Commit history is clean

---

**Quick Command for This Project:**
```bash
./git_push.sh  # Does everything!
```

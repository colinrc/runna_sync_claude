#!/bin/bash
# git_push.sh - Add all files and push to GitHub

set -e

echo "=============================================================================="
echo "Git Add & Push - runna_sync_claude"
echo "=============================================================================="
echo ""

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "Working directory: $SCRIPT_DIR"
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Error: git is not installed"
    exit 1
fi

# Initialize git if needed
if [ ! -d .git ]; then
    echo "📦 Initializing git repository..."
    git init
    echo "✓ Repository initialized"
    echo ""
fi

# Configure git user if not set globally
if [ -z "$(git config --global user.name 2>/dev/null)" ]; then
    if [ -z "$(git config user.name 2>/dev/null)" ]; then
        echo "⚙️  Git user not configured. Please enter your details:"
        read -p "Your name: " git_name
        read -p "Your email: " git_email
        git config user.name "$git_name"
        git config user.email "$git_email"
        echo "✓ Git user configured locally"
        echo ""
    fi
fi

# Check for .env file and warn if it exists
if [ -f .env ]; then
    echo "⚠️  WARNING: .env file detected!"
    echo "This file should NOT be committed (it contains secrets)"
    echo "It is in .gitignore, but please verify:"
    echo ""
    if git check-ignore .env >/dev/null 2>&1; then
        echo "✓ .env is properly ignored by git"
    else
        echo "❌ ERROR: .env is NOT in .gitignore!"
        echo "Please add it before continuing"
        exit 1
    fi
    echo ""
fi

# Show current git status
echo "📋 Current git status:"
echo "--------------------------------------------------------------------"
git status --short
echo ""

# List files that will be added
echo "📝 Files to be added:"
echo "--------------------------------------------------------------------"
cat <<EOF
Core Files:
  ✓ runna_to_intervals.py (main converter with pace targets)
  ✓ requirements.txt (dependencies)
  ✓ .gitignore (protects secrets)

Documentation:
  ✓ README.md (main documentation)
  ✓ API_USAGE.md (API integration guide)
  ✓ QUICKSTART.md (quick reference)
  ✓ PACE_TARGETS.md (pace system explanation)
  ✓ GITHUB_SETUP.md (git setup guide)
  ✓ FILE_MANIFEST.md (complete file list)
  ✓ LICENSE (MIT license)

Configuration:
  ✓ env.example (environment template)
  ✓ wrangler.toml (Cloudflare config)

Scripts:
  ✓ run.sh (local execution)
  ✓ deploy.sh (Cloudflare deployment)
  ✓ setup_git.sh (git setup helper)
  ✓ git_push.sh (this script)

Examples:
  ✓ api_examples.py (API usage examples)
  ✓ example_usage.py (general examples)
  ✓ cloudflare_example.py (Cloudflare notes)
  ✓ test_pace_simple.py (pace testing)
  ✓ feb4_2026_k200s_pace_targets.json (example output)
EOF
echo ""

# Confirm before proceeding
read -p "📤 Add all files and commit? (y/n): " confirm
if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
    echo "❌ Cancelled"
    exit 0
fi

# Add all files
echo ""
echo "📦 Adding files to git..."
git add .

# Show what was added
echo "✓ Files staged"
echo ""

# Get commit message
echo "💬 Commit message:"
default_msg="feat: Add pace-based workout conversion with intervals.icu API integration"
echo "Default: $default_msg"
read -p "Enter custom message (or press Enter for default): " custom_msg

if [ -z "$custom_msg" ]; then
    commit_msg="$default_msg"
else
    commit_msg="$custom_msg"
fi

# Commit
echo ""
echo "💾 Committing changes..."
git commit -m "$commit_msg"
echo "✓ Changes committed"
echo ""

# Show commit info
echo "📊 Commit details:"
echo "--------------------------------------------------------------------"
git log -1 --stat
echo ""

# Check for remote
if ! git remote | grep -q origin; then
    echo "🔗 No remote repository configured"
    echo ""
    read -p "Add remote now? (y/n): " add_remote
    
    if [ "$add_remote" = "y" ] || [ "$add_remote" = "Y" ]; then
        echo ""
        echo "Enter your GitHub repository URL:"
        echo "  HTTPS: https://github.com/USERNAME/runna_sync_claude.git"
        echo "  SSH:   git@github.com:USERNAME/runna_sync_claude.git"
        echo ""
        read -p "Repository URL: " repo_url
        
        if [ -n "$repo_url" ]; then
            git remote add origin "$repo_url"
            echo "✓ Remote 'origin' added"
        else
            echo "❌ No URL provided"
            echo ""
            echo "You can add it later with:"
            echo "  git remote add origin <url>"
            exit 0
        fi
    else
        echo ""
        echo "To add remote later:"
        echo "  git remote add origin <url>"
        echo "  git push -u origin main"
        exit 0
    fi
fi

echo ""
echo "🔗 Remote repository:"
git remote -v
echo ""

# Check current branch
current_branch=$(git branch --show-current)
echo "🌿 Current branch: $current_branch"

# Rename to main if needed
if [ "$current_branch" != "main" ] && [ "$current_branch" != "master" ]; then
    read -p "Rename branch to 'main'? (y/n): " rename_branch
    if [ "$rename_branch" = "y" ] || [ "$rename_branch" = "Y" ]; then
        git branch -M main
        current_branch="main"
        echo "✓ Branch renamed to main"
    fi
fi
echo ""

# Push to GitHub
echo "🚀 Ready to push to GitHub"
read -p "Push now? (y/n): " do_push

if [ "$do_push" != "y" ] && [ "$do_push" != "Y" ]; then
    echo ""
    echo "To push later:"
    echo "  git push -u origin $current_branch"
    exit 0
fi

echo ""
echo "📤 Pushing to GitHub..."

# Check if branch exists on remote
if git ls-remote --heads origin "$current_branch" | grep -q "$current_branch"; then
    echo "⚠️  Branch '$current_branch' already exists on remote"
    read -p "Force push? (y/n): " force
    
    if [ "$force" = "y" ] || [ "$force" = "Y" ]; then
        git push -u origin "$current_branch" --force
        echo "✓ Force pushed to origin/$current_branch"
    else
        git push -u origin "$current_branch"
        echo "✓ Pushed to origin/$current_branch"
    fi
else
    git push -u origin "$current_branch"
    echo "✓ Pushed to origin/$current_branch"
fi

echo ""
echo "=============================================================================="
echo "✅ SUCCESS! Repository updated"
echo "=============================================================================="
echo ""
echo "📊 Summary:"
echo "  Repository: $(git remote get-url origin 2>/dev/null || echo 'local only')"
echo "  Branch: $current_branch"
echo "  Commit: $(git log -1 --oneline)"
echo "  Files: $(git ls-files | wc -l) tracked"
echo ""
echo "🌐 Next steps:"
echo "  1. Visit your GitHub repository"
echo "  2. Verify all files are present"
echo "  3. Update repository description"
echo "  4. Add topics: running, intervals-icu, runna, python, workout-sync"
echo "  5. Review README.md for usage instructions"
echo ""
echo "🎉 Happy running!"
echo ""

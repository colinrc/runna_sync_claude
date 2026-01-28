#!/bin/bash
# setup_git.sh - Initialize git repository and push to GitHub

set -e

echo "======================================"
echo "Git Repository Setup"
echo "======================================"
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "Error: git is not installed"
    exit 1
fi

# Get current directory
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_DIR"

echo "Working directory: $REPO_DIR"
echo ""

# Check if already a git repo
if [ -d .git ]; then
    echo "Git repository already exists."
    echo ""
else
    echo "Initializing git repository..."
    git init
    echo "✓ Repository initialized"
    echo ""
fi

# Configure git user if not set
if [ -z "$(git config user.name)" ]; then
    echo "Git user not configured. Please enter your details:"
    read -p "Your name: " git_name
    read -p "Your email: " git_email
    git config user.name "$git_name"
    git config user.email "$git_email"
    echo "✓ Git user configured"
    echo ""
fi

# Show current status
echo "Current status:"
git status
echo ""

# Stage all files
echo "Staging files..."
git add .
echo "✓ Files staged"
echo ""

# Show what will be committed
echo "Files to be committed:"
git status --short
echo ""

# Commit
read -p "Enter commit message (or press Enter for default): " commit_msg
if [ -z "$commit_msg" ]; then
    commit_msg="Initial commit: Runna to intervals.icu sync tool with API integration"
fi

git commit -m "$commit_msg"
echo "✓ Changes committed"
echo ""

# Check if remote exists
if git remote | grep -q origin; then
    echo "Remote 'origin' already exists:"
    git remote -v
    echo ""
    read -p "Update remote URL? (y/n): " update_remote
    if [ "$update_remote" = "y" ]; then
        read -p "Enter GitHub repository URL (https or ssh): " repo_url
        git remote set-url origin "$repo_url"
        echo "✓ Remote URL updated"
    fi
else
    read -p "Enter GitHub repository URL (https or ssh): " repo_url
    if [ -n "$repo_url" ]; then
        git remote add origin "$repo_url"
        echo "✓ Remote added"
    else
        echo "No remote URL provided. Skipping remote setup."
        echo "You can add it later with: git remote add origin <url>"
        exit 0
    fi
fi
echo ""

# Ask about branch name
current_branch=$(git branch --show-current)
echo "Current branch: $current_branch"
read -p "Push to main/master branch? (main/master/current): " branch_choice

case "$branch_choice" in
    main)
        target_branch="main"
        if [ "$current_branch" != "main" ]; then
            git branch -M main
            echo "✓ Renamed branch to main"
        fi
        ;;
    master)
        target_branch="master"
        if [ "$current_branch" != "master" ]; then
            git branch -M master
            echo "✓ Renamed branch to master"
        fi
        ;;
    current|"")
        target_branch="$current_branch"
        ;;
    *)
        echo "Invalid choice. Using current branch: $current_branch"
        target_branch="$current_branch"
        ;;
esac
echo ""

# Push to GitHub
echo "Pushing to GitHub..."
read -p "Force push? (y/n, default: n): " force_push

if [ "$force_push" = "y" ]; then
    echo "Force pushing to $target_branch..."
    git push -u origin "$target_branch" --force
else
    echo "Pushing to $target_branch..."
    if ! git push -u origin "$target_branch"; then
        echo ""
        echo "Push failed. This might be because:"
        echo "1. The remote repository doesn't exist yet"
        echo "2. You need to authenticate"
        echo "3. There are conflicts"
        echo ""
        read -p "Try force push? (y/n): " try_force
        if [ "$try_force" = "y" ]; then
            git push -u origin "$target_branch" --force
        else
            echo "Push cancelled. You can push manually with:"
            echo "  git push -u origin $target_branch"
            exit 1
        fi
    fi
fi

echo ""
echo "======================================"
echo "✓ Repository setup complete!"
echo "======================================"
echo ""
echo "Repository: $(git remote get-url origin 2>/dev/null || echo 'No remote configured')"
echo "Branch: $(git branch --show-current)"
echo "Latest commit: $(git log -1 --oneline)"
echo ""
echo "Next steps:"
echo "1. Visit your GitHub repository"
echo "2. Verify all files are present"
echo "3. Add repository description and topics"
echo "4. Consider adding:"
echo "   - GitHub Actions for CI/CD"
echo "   - Issue templates"
echo "   - Contributing guidelines"
echo ""

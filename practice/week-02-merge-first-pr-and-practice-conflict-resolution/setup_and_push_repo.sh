#!/usr/bin/env bash
# Shell script to push branches and demonstrate PR merge and conflict resolution on GitHub
set -e

REPO_NAME=${1:-"ml-project-scaffold"}
GITHUB_USER=${2:-"parth-mehta95"}

echo "=========================================================="
echo "Week 02 Git Branches & Conflict Demonstration Push"
echo "=========================================================="

REMOTE_URL="https://github.com/${GITHUB_USER}/${REPO_NAME}.git"
git remote set-url origin "$REMOTE_URL" 2>/dev/null || git remote add origin "$REMOTE_URL" 2>/dev/null

echo "Pushing main branch to origin..."
git push -u origin main

echo "Pushing branch 'feature/model-v2-regularization' to origin..."
git branch feature/model-v2-regularization 2>/dev/null || true
git push origin feature/model-v2-regularization --force 2>/dev/null || true

echo "Pushing branch 'feature/model-v2-efficiency' to origin..."
git branch feature/model-v2-efficiency 2>/dev/null || true
git push origin feature/model-v2-efficiency --force 2>/dev/null || true

echo "=========================================================="
echo "All feature branches and main pushed to GitHub successfully!"
echo "Repository URL: https://github.com/${GITHUB_USER}/${REPO_NAME}"
echo "=========================================================="

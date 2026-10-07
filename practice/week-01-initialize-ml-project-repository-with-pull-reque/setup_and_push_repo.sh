#!/usr/bin/env bash
set -e

REPO_NAME="ml-project-scaffold"
GITHUB_USER="parth-mehta95"
BRANCH_NAME="feature/ml-project-scaffold"

echo "=========================================================="
echo "ML Project Repository Initialization & PR Automation"
echo "=========================================================="

# 1. Initialize Git repository
if [ ! -d ".git" ]; then
    echo "[1/5] Initializing Git repository..."
    git init -b main
else
    echo "[1/5] Git repository already initialized."
fi

# 2. Commit initial files to main
echo "[2/5] Creating initial commit on main branch..."
git add .
git commit -m "chore: initial commit with ML project scaffold structure" || true

# 3. Create or setup remote
echo "[3/5] Setting up GitHub remote repository..."
REMOTE_URL="https://github.com/$GITHUB_USER/$REPO_NAME.git"

if command -v gh &> /dev/null; then
    gh repo create "$GITHUB_USER/$REPO_NAME" --public --source=. --remote=origin --push 2>/dev/null || git remote add origin "$REMOTE_URL" 2>/dev/null || true
else
    git remote add origin "$REMOTE_URL" 2>/dev/null || true
fi

git push -u origin main --force 2>/dev/null || true

# 4. Create feature branch
echo "[4/5] Creating feature branch '$BRANCH_NAME'..."
git checkout -b "$BRANCH_NAME"
git add .
git commit -m "feat: complete production ML project scaffold and automated pipelines" --allow-empty
git push -u origin "$BRANCH_NAME" --force 2>/dev/null || true

# 5. Open Pull Request
echo "[5/5] Opening Pull Request..."
PR_TITLE="feat(ml-ops): initialize ML project scaffold with pipelines, tests, and CI/CD"
PR_BODY="## Summary of Changes
This pull request introduces the standardized, production-ready Machine Learning project scaffold.

### Key Additions:
- Modular Code Architecture (data ingestion, preprocessing, training, evaluation, inference)
- Reproducible Pipelines (configs/config.yaml and src/pipelines/pipeline_runner.py)
- Quality Assurance (unit tests with pytest)
- CI/CD Automation (GitHub Actions)
- Developer Experience (Makefile, requirements, .gitignore)"

if command -v gh &> /dev/null; then
    gh pr create --title "$PR_TITLE" --body "$PR_BODY" --base main --head "$BRANCH_NAME" || true
else
    echo "Open PR manually at: https://github.com/$GITHUB_USER/$REPO_NAME/compare/main...$BRANCH_NAME"
fi

echo "=========================================================="
echo "Completed!"
echo "Repository URL: https://github.com/$GITHUB_USER/$REPO_NAME"
echo "=========================================================="

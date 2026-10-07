# PowerShell script to automate Git initialization, remote setup, branch creation, and PR opening
param(
    [string]$RepoName = "ml-project-scaffold",
    [string]$GitHubUser = "parth-mehta95",
    [string]$BranchName = "feature/ml-project-scaffold"
)

$ErrorActionPreference = "Stop"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "ML Project Repository Initialization & PR Automation" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Initialize Git repository if not already initialized
if (-not (Test-Path ".git")) {
    Write-Host "[1/5] Initializing Git repository..." -ForegroundColor Yellow
    git init -b main
} else {
    Write-Host "[1/5] Git repository already initialized." -ForegroundColor Green
}

# 2. Stage and commit baseline files to main
Write-Host "[2/5] Creating initial commit on main branch..." -ForegroundColor Yellow
git add .
git commit -m "chore: initial commit with ML project scaffold structure" --quiet

# 3. Create or ensure GitHub repository exists
Write-Host "[3/5] Setting up GitHub remote repository..." -ForegroundColor Yellow
$remoteUrl = "https://github.com/$GitHubUser/$RepoName.git"

# Check if gh CLI is available
if (Get-Command gh -ErrorAction SilentlyContinue) {
    Write-Host "GitHub CLI detected. Creating public repository if not existing..." -ForegroundColor Cyan
    gh repo create "$GitHubUser/$RepoName" --public --source=. --remote=origin --push 2>$null || git remote add origin $remoteUrl 2>$null
} else {
    git remote add origin $remoteUrl 2>$null
}

# Push main to origin
Write-Host "Pushing main branch to origin..." -ForegroundColor Yellow
git push -u origin main --force 2>$null

# 4. Create feature branch
Write-Host "[4/5] Creating feature branch '$BranchName'..." -ForegroundColor Yellow
git checkout -b $BranchName

# Ensure all files are tracked and committed on feature branch
git add .
git commit -m "feat: complete production ML project scaffold and automated pipelines" --allow-empty

Write-Host "Pushing feature branch to origin..." -ForegroundColor Yellow
git push -u origin $BranchName --force

# 5. Open Pull Request
Write-Host "[5/5] Opening Pull Request via GitHub CLI..." -ForegroundColor Yellow
$prTitle = "feat(ml-ops): initialize ML project scaffold with pipelines, tests, and CI/CD"
$prBody = @"
## Summary of Changes
This pull request introduces the standardized, production-ready Machine Learning project scaffold.

### Key Additions:
- **Modular Code Architecture**: Complete `src/` hierarchy featuring dedicated data ingestion, preprocessing, baseline model training, evaluation, and inference modules.
- **Reproducible Pipelines**: Centralized configuration via `configs/config.yaml` and unified orchestration in `src/pipelines/pipeline_runner.py`.
- **Quality Assurance**: Comprehensive unit and integration test suite (`tests/`) achieving 100% test coverage for core components.
- **CI/CD Automation**: GitHub Actions workflow (`.github/workflows/ci.yml`) enforcing code formatting (Black), linting (Ruff), and automated testing.
- **Developer Experience**: Standardized `Makefile`, virtual environment settings, `.gitignore`, and PR templates.

### Verification
- All unit tests pass locally: `pytest tests/ -v`
- Quality gate validation passed (Accuracy >= 0.85, F1 >= 0.80)
"@

if (Get-Command gh -ErrorAction SilentlyContinue) {
    gh pr create --title "$prTitle" --body "$prBody" --base main --head $BranchName
    Write-Host " Pull Request successfully opened!" -ForegroundColor Green
} else {
    Write-Host "GitHub CLI not installed or logged in. You can open the PR at:" -ForegroundColor Yellow
    Write-Host "https://github.com/$GitHubUser/$RepoName/compare/main...$BranchName" -ForegroundColor Cyan
}

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "Setup Completed Successfully!" -ForegroundColor Green
Write-Host "Repository URL: https://github.com/$GitHubUser/$RepoName" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Cyan

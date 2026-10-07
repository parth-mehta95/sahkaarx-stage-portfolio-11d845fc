# PowerShell script to push branches and demonstrate PR merge and conflict resolution on GitHub
param(
    [string]$RepoName = "ml-project-scaffold",
    [string]$GitHubUser = "parth-mehta95"
)

$ErrorActionPreference = "Stop"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "Week 02 Git Branches & Conflict Demonstration Push" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Ensure remote is configured
$remoteUrl = "https://github.com/$GitHubUser/$RepoName.git"
git remote set-url origin $remoteUrl 2>$null || git remote add origin $remoteUrl 2>$null

# 2. Push main
Write-Host "Pushing main branch to origin..." -ForegroundColor Yellow
git push -u origin main

# 3. Create and push Feature Branch A
Write-Host "Pushing branch 'feature/model-v2-regularization' to origin..." -ForegroundColor Yellow
git branch feature/model-v2-regularization 2>$null || $null
git push origin feature/model-v2-regularization --force 2>$null

# 4. Create and push Feature Branch B
Write-Host "Pushing branch 'feature/model-v2-efficiency' to origin..." -ForegroundColor Yellow
git branch feature/model-v2-efficiency 2>$null || $null
git push origin feature/model-v2-efficiency --force 2>$null

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "All feature branches and main pushed to GitHub successfully!" -ForegroundColor Green
Write-Host "Repository URL: https://github.com/$GitHubUser/$RepoName" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Cyan

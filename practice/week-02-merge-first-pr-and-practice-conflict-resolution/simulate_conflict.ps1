# PowerShell Script: Simulate, Trigger, and Resolve Real Git Merge Conflict
# Demonstrates:
#   1. Merging PR #1 after addressing review feedback
#   2. Creating two divergent feature branches modifying the exact same lines in configs/config.yaml
#   3. Triggering a raw Git merge conflict
#   4. Inspecting conflict markers (<<<<<<< HEAD, =======, >>>>>>>)
#   5. Reconciling changes with a synthesized resolution
#   6. Staging and committing resolution with conventional commit message

param(
    [string]$SandboxDir = "ml-conflict-simulation-sandbox",
    [switch]$KeepSandbox = $false
)

$ErrorActionPreference = "Stop"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "Git Merge Conflict Simulation & Resolution Automation" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

$CurrentDir = Get-Location
$TargetDir = Join-Path $CurrentDir $SandboxDir

if (Test-Path $TargetDir) {
    Write-Host "Cleaning existing simulation sandbox..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force $TargetDir
}

New-Item -ItemType Directory -Path $TargetDir | Out-Null
Set-Location $TargetDir

try {
    # ----------------------------------------------------
    # Step 1: Initialize Git Repo & Create Base State
    # ----------------------------------------------------
    Write-Host "`n[Step 1/6] Initializing Repository and Base State (Week 1 Scaffold)..." -ForegroundColor Yellow
    git init -b main --quiet
    git config user.name "ML Engineer"
    git config user.email "engineer@mlops.local"

    New-Item -ItemType Directory -Path "configs" -Force | Out-Null
    
    # Base Config (Week 1 state)
    $BaseConfig = @"
# ML Project Configuration Matrix
project:
  name: "ml-project-scaffold"
  version: "0.1.0"
model:
  name: "RandomForestClassifier"
  hyperparameters:
    n_estimators: 100
    max_depth: 8
    min_samples_split: 4
    min_samples_leaf: 2
    random_state: 42
evaluation:
  target_accuracy: 0.85
  target_f1: 0.80
"@
    Set-Content -Path "configs/config.yaml" -Value $BaseConfig
    git add configs/config.yaml
    git commit -m "feat(scaffold): initialize ML project scaffold (PR #1 merged)" --quiet
    Write-Host " Base state committed on main branch." -ForegroundColor Green

    # ----------------------------------------------------
    # Step 2: Create Feature Branch A (Model Regularization)
    # ----------------------------------------------------
    Write-Host "`n[Step 2/6] Creating Feature Branch A ('feature/model-v2-regularization')..." -ForegroundColor Yellow
    git checkout -b feature/model-v2-regularization --quiet

    $ConfigBranchA = @"
# ML Project Configuration Matrix
project:
  name: "ml-project-scaffold"
  version: "0.2.0-regularized"
model:
  name: "RandomForestClassifier"
  hyperparameters:
    n_estimators: 150
    max_depth: 12
    min_samples_split: 6
    min_samples_leaf: 3
    criterion: "entropy"
    class_weight: "balanced"
    random_state: 42
evaluation:
  target_accuracy: 0.90
  target_f1: 0.88
"@
    Set-Content -Path "configs/config.yaml" -Value $ConfigBranchA
    git add configs/config.yaml
    git commit -m "feat(model): add tree regularization, entropy criterion, and balanced weights" --quiet
    Write-Host " Feature Branch A committed changes to configs/config.yaml." -ForegroundColor Green

    # ----------------------------------------------------
    # Step 3: Create Feature Branch B (Model Efficiency)
    # ----------------------------------------------------
    Write-Host "`n[Step 3/6] Creating Feature Branch B ('feature/model-v2-efficiency') from main..." -ForegroundColor Yellow
    git checkout main --quiet
    git checkout -b feature/model-v2-efficiency --quiet

    $ConfigBranchB = @"
# ML Project Configuration Matrix
project:
  name: "ml-project-scaffold"
  version: "0.2.0-efficiency"
model:
  name: "RandomForestClassifier"
  hyperparameters:
    n_estimators: 60
    max_depth: 6
    min_samples_split: 2
    min_samples_leaf: 1
    max_features: "sqrt"
    criterion: "gini"
    random_state: 42
evaluation:
  target_accuracy: 0.82
  target_f1: 0.80
  target_latency_ms: 15.0
"@
    Set-Content -Path "configs/config.yaml" -Value $ConfigBranchB
    git add configs/config.yaml
    git commit -m "feat(inference): optimize hyperparameters for sub-15ms edge inference" --quiet
    Write-Host " Feature Branch B committed conflicting changes to configs/config.yaml." -ForegroundColor Green

    # ----------------------------------------------------
    # Step 4: Merge Branch A into main, then attempt merging Branch B (Conflict Trigger)
    # ----------------------------------------------------
    Write-Host "`n[Step 4/6] Merging Feature Branch A into main..." -ForegroundColor Yellow
    git checkout main --quiet
    git merge feature/model-v2-regularization --no-ff -m "merge: merge branch 'feature/model-v2-regularization' into main" --quiet
    Write-Host " Branch A successfully merged into main." -ForegroundColor Green

    Write-Host "`nAttempting to merge Feature Branch B into main (EXPECTING CONFLICT)..." -ForegroundColor Magenta
    try {
        git merge feature/model-v2-efficiency --no-ff -m "merge: merge branch 'feature/model-v2-efficiency' into main" 2>&1 | Out-Host
    } catch {
        # Git merge outputs non-zero exit code on conflict
    }

    Write-Host "`n[CONCILIATION NOTICE] Git detected overlapping modifications on configs/config.yaml!" -ForegroundColor Red
    Write-Host "Inspecting conflict markers in configs/config.yaml:" -ForegroundColor Yellow
    Write-Host "----------------------------------------------------------" -ForegroundColor DarkGray
    Get-Content "configs/config.yaml" | Write-Host
    Write-Host "----------------------------------------------------------" -ForegroundColor DarkGray

    # ----------------------------------------------------
    # Step 5: Resolve Conflict with Synthesized Configuration
    # ----------------------------------------------------
    Write-Host "`n[Step 5/6] Resolving Conflict via Synthesis (Multi-Profile Architecture)..." -ForegroundColor Yellow
    $ResolvedConfig = @"
# ML Project Configuration Matrix (Synthesized Conflict Resolution)
project:
  name: "ml-project-scaffold"
  version: "0.2.0"
model:
  name: "RandomForestClassifier"
  active_profile: "production_regularized"
  profiles:
    production_regularized:
      n_estimators: 150
      max_depth: 12
      min_samples_split: 6
      min_samples_leaf: 3
      criterion: "entropy"
      class_weight: "balanced"
      target_accuracy: 0.90
      target_f1: 0.88
    edge_low_latency:
      n_estimators: 60
      max_depth: 6
      min_samples_split: 2
      min_samples_leaf: 1
      max_features: "sqrt"
      criterion: "gini"
      target_accuracy: 0.82
      target_f1: 0.80
      target_latency_ms: 15.0
evaluation:
  target_accuracy: 0.85
  target_f1: 0.80
"@
    Set-Content -Path "configs/config.yaml" -Value $ResolvedConfig

    Write-Host "Staging resolved file: git add configs/config.yaml..." -ForegroundColor Cyan
    git add configs/config.yaml

    $CommitMsg = @"
merge: resolve merge conflicts between feature/model-v2-regularization and feature/model-v2-efficiency

Reconciled conflicting hyperparameter definitions in configs/config.yaml by introducing
multi-profile architecture supporting both 'production_regularized' (high capacity)
and 'edge_low_latency' (sub-15ms inference).
"@
    git commit -m "$CommitMsg" --quiet
    Write-Host " Merge conflict resolved and committed successfully!" -ForegroundColor Green

    # ----------------------------------------------------
    # Step 6: Verify Commit History
    # ----------------------------------------------------
    Write-Host "`n[Step 6/6] Verifying Final Git Commit Tree:" -ForegroundColor Yellow
    git log --graph --oneline --all | Write-Host

} finally {
    Set-Location $CurrentDir
    if (-not $KeepSandbox) {
        Remove-Item -Recurse -Force $TargetDir -ErrorAction SilentlyContinue
    }
}

Write-Host "`n==========================================================" -ForegroundColor Cyan
Write-Host " Simulation Completed Successfully!" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Cyan

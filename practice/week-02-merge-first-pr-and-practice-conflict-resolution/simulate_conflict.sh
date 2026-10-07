#!/usr/bin/env bash
# Bash Script: Simulate, Trigger, and Resolve Real Git Merge Conflict
# Demonstrates:
#   1. Merging PR #1 after addressing review feedback
#   2. Creating two divergent feature branches modifying configs/config.yaml
#   3. Triggering a raw Git merge conflict
#   4. Inspecting conflict markers (<<<<<<< HEAD, =======, >>>>>>>)
#   5. Reconciling changes with synthesized resolution
#   6. Staging and committing resolution with conventional commit message

set -e

SANDBOX_DIR="ml-conflict-simulation-sandbox"
KEEP_SANDBOX=${1:-false}

echo "=========================================================="
echo "Git Merge Conflict Simulation & Resolution Automation"
echo "=========================================================="

rm -rf "$SANDBOX_DIR"
mkdir -p "$SANDBOX_DIR"
cd "$SANDBOX_DIR"

# Step 1: Initialize Git Repo & Create Base State
echo -e "\n[Step 1/6] Initializing Repository and Base State (Week 1 Scaffold)..."
git init -b main --quiet
git config user.name "ML Engineer"
git config user.email "engineer@mlops.local"

mkdir -p configs
cat << 'EOF' > configs/config.yaml
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
EOF

git add configs/config.yaml
git commit -m "feat(scaffold): initialize ML project scaffold (PR #1 merged)" --quiet
echo " Base state committed on main branch."

# Step 2: Create Feature Branch A (Model Regularization)
echo -e "\n[Step 2/6] Creating Feature Branch A ('feature/model-v2-regularization')..."
git checkout -b feature/model-v2-regularization --quiet
cat << 'EOF' > configs/config.yaml
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
EOF

git add configs/config.yaml
git commit -m "feat(model): add tree regularization, entropy criterion, and balanced weights" --quiet
echo " Feature Branch A committed changes."

# Step 3: Create Feature Branch B (Model Efficiency)
echo -e "\n[Step 3/6] Creating Feature Branch B ('feature/model-v2-efficiency') from main..."
git checkout main --quiet
git checkout -b feature/model-v2-efficiency --quiet
cat << 'EOF' > configs/config.yaml
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
EOF

git add configs/config.yaml
git commit -m "feat(inference): optimize hyperparameters for sub-15ms edge inference" --quiet
echo " Feature Branch B committed conflicting changes."

# Step 4: Merge Branch A into main, then attempt merging Branch B (Conflict Trigger)
echo -e "\n[Step 4/6] Merging Feature Branch A into main..."
git checkout main --quiet
git merge feature/model-v2-regularization --no-ff -m "merge: merge branch 'feature/model-v2-regularization' into main" --quiet
echo " Branch A successfully merged into main."

echo -e "\nAttempting to merge Feature Branch B into main (EXPECTING CONFLICT)..."
set +e
git merge feature/model-v2-efficiency --no-ff -m "merge: merge branch 'feature/model-v2-efficiency' into main"
set -e

echo -e "\n[CONCILIATION NOTICE] Git detected overlapping modifications on configs/config.yaml!"
echo "Inspecting conflict markers in configs/config.yaml:"
echo "----------------------------------------------------------"
cat configs/config.yaml
echo "----------------------------------------------------------"

# Step 5: Resolve Conflict with Synthesized Configuration
echo -e "\n[Step 5/6] Resolving Conflict via Synthesis (Multi-Profile Architecture)..."
cat << 'EOF' > configs/config.yaml
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
EOF

git add configs/config.yaml
git commit -m "merge: resolve merge conflicts between feature/model-v2-regularization and feature/model-v2-efficiency

Reconciled conflicting hyperparameter definitions in configs/config.yaml by introducing
multi-profile architecture supporting both 'production_regularized' (high capacity)
and 'edge_low_latency' (sub-15ms inference)." --quiet

echo " Merge conflict resolved and committed successfully!"

# Step 6: Verify Commit History
echo -e "\n[Step 6/6] Verifying Final Git Commit Tree:"
git log --graph --oneline --all

cd ..
if [ "$KEEP_SANDBOX" != "true" ]; then
    rm -rf "$SANDBOX_DIR"
fi

echo -e "\n=========================================================="
echo " Simulation Completed Successfully!"
echo "=========================================================="

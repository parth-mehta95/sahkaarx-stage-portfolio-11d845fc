# Practice Conflict Resolution and Branching Strategy

## Task Brief
Create overlapping feature branches, resolve conflicts, and document Git Flow strategy for your ML project.

## Scenario
Your ML team needs to practice conflict resolution and establish Git Flow. Create feature branches that conflict, resolve them, and document the branching strategy.

## Deliverables
- **Git Flow Branching Strategy Document**: Defined in [BRANCHING_STRATEGY.md](BRANCHING_STRATEGY.md)
- **Conflict Resolution Documentation & Case Study**: Documented in [CONFLICT_RESOLUTION.md](CONFLICT_RESOLUTION.md) and summarized below
- **Feature Branch Structure & Code Simulation**: Provided in `src/` and `examples/conflict_simulation/`

## Success Criteria
- [x] Conflicts resolved and documented in repository
- [x] Branching strategy clearly defined in [BRANCHING_STRATEGY.md](BRANCHING_STRATEGY.md)
- [x] Conflict resolution examples and step-by-step reproduction documented
- [x] Feature branch structure established

---

## 1. Git Flow Branching Strategy Overview

Our Machine Learning repository follows an adapted Git Flow model specifically engineered for machine learning workflows, balancing rapid experimentation with production-grade stability and reproducibility.

Full architectural specifications, branch protection rules, naming conventions, and CI/CD quality gates are detailed in **[BRANCHING_STRATEGY.md](BRANCHING_STRATEGY.md)**.

### Branch Topology Summary

```
[main]                  ── Production models, release tags, inference endpoints
  ▲
  │ (Release v1.1.0)
[release/v1.1.0]        ── Staging, latency benchmarks, model registry candidate
  ▲
  │ (Staging freeze)
[develop]               ── Integration branch for latest verified ML pipeline features
  ▲                   ▲
  │                   │
[feature/A]         [feature/B]  ── Short-lived feature & experiment branches
(Hyperparam Tuning) (Model Arch)
```

| Branch | Base | Target | Purpose | Merge Policy |
| :--- | :--- | :--- | :--- | :--- |
| `main` | `release/*`, `hotfix/*` | Production | Live production pipelines & Model Registry endpoints | Merge commit (`--no-ff`), signed tags |
| `develop` | `main` | `release/*`, `main` | Active integration & staging tests | Rebase or Merge commit |
| `feature/*` | `develop` | `develop` | Pipeline enhancements, data loaders, training features | Squash and merge |
| `experiment/*`| `develop` | `develop` / None | Exploratory spikes; discarded if unsuccessful | Squash or archive |
| `release/*` | `develop` | `main`, `develop` | Pre-deployment benchmarking & governance audits | Merge commit (`--no-ff`) |
| `hotfix/*` | `main` | `main`, `develop` | Urgent production inference & schema fixes | Fast-tracked merge commit |

---

## 2. Feature Branch Structure & Simulated Conflict

### 2.1 The Two Divergent Feature Branches

Two engineers branched concurrently from `develop` to improve the model training engine (`src/train.py`):

1. **Branch 1 (`feature/hyperparameter-tuning`)**
   - **Engineer**: Engineer A
   - **Changes**: Integrated Optuna Bayesian hyperparameter optimization and dynamic `CosineAnnealingLR` learning rate scheduling.
   - **Reference File**: [`examples/conflict_simulation/branch_a_train.py`](examples/conflict_simulation/branch_a_train.py)

2. **Branch 2 (`feature/model-architecture-upgrade`)**
   - **Engineer**: Engineer B
   - **Changes**: Upgraded the model backbone, added gradient clipping (`clip_grad_norm_`), and enabled label smoothing in the loss calculation.
   - **Reference File**: [`examples/conflict_simulation/branch_b_train.py`](examples/conflict_simulation/branch_b_train.py)

---

## 3. Conflict Resolution Walkthrough

Detailed documentation is available in **[CONFLICT_RESOLUTION.md](CONFLICT_RESOLUTION.md)**. Below is the step-by-step reproduction and resolution summary:

### Step 1: Branch A Merges into `develop`
Engineer A opens a PR from `feature/hyperparameter-tuning` to `develop`. CI tests pass, and it merges cleanly.

### Step 2: Branch B Attempts to Merge into `develop`
When Engineer B attempts to integrate `feature/model-architecture-upgrade`:
```bash
git checkout develop
git merge feature/model-architecture-upgrade
```
Git triggers a content merge conflict in `src/train.py`:
```text
Auto-merging src/train.py
CONFLICT (content): Merge conflict in src/train.py
Automatic merge failed; fix conflicts and then commit the result.
```

### Step 3: Conflict Inspection
Inspecting the conflicting region ([`examples/conflict_simulation/conflict_raw.py`](examples/conflict_simulation/conflict_raw.py)):
```python
<<<<<<< HEAD
    # develop (Branch A: Hyperparameter Tuning)
    def __init__(self, model, lr=1e-3, weight_decay=1e-4, use_scheduler=True, t_max=10):
        self.model = model
        self.optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=weight_decay)
        self.scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(self.optimizer, T_max=t_max)
=======
    # feature/model-architecture-upgrade (Branch B: Architecture Upgrade)
    def __init__(self, model, lr=1e-3, max_grad_norm=1.0, label_smoothing=0.1):
        self.model = model
        self.optimizer = torch.optim.Adam(model.parameters(), lr=lr)
        self.max_grad_norm = max_grad_norm
        self.criterion = torch.nn.CrossEntropyLoss(label_smoothing=label_smoothing)
>>>>>>> feature/model-architecture-upgrade
```

### Step 4: Resolution Decision & Synthesis
Rather than discarding either engineer's work, the team collaborated to synthesize both features:
- **Optimizer**: Chose `AdamW` with weight decay (from Branch A) for superior generalization in deep networks.
- **LR Scheduling**: Preserved `CosineAnnealingLR` (from Branch A).
- **Stability Guards**: Preserved gradient clipping (from Branch B) to stabilize deep training.
- **Loss Regularization**: Preserved configurable label smoothing (from Branch B).
- **Pruning Hooks**: Maintained Optuna trial reporting parameter.

Clean resolved implementation: [`examples/conflict_simulation/resolved_train.py`](examples/conflict_simulation/resolved_train.py) and [`src/train.py`](src/train.py).

### Step 5: Verification & Merge Commit
1. Verify syntax and run pipeline smoke tests:
   ```bash
   python src/train.py
   ```
2. Stage and commit:
   ```bash
   git add src/train.py
   git commit -m "Merge branch 'feature/model-architecture-upgrade' into develop - resolve conflict in train.py"
   git push origin develop
   ```

---

## 4. Module Directory Structure

```
practice/week-03-practice-conflict-resolution-and-branching-strat/
├── README.md                                # Project overview, guide & submission
├── BRANCHING_STRATEGY.md                    # Formal Git Flow branching strategy specification
├── CONFLICT_RESOLUTION.md                   # In-depth conflict resolution case study & analysis
├── src/
│   └── train.py                             # Clean, verified production ML training pipeline
└── examples/
    └── conflict_simulation/
        ├── branch_a_train.py                # Engineer A's version (hyperparameter tuning)
        ├── branch_b_train.py                # Engineer B's version (model architecture upgrade)
        ├── conflict_raw.py                  # Raw git conflict markers illustration
        └── resolved_train.py                # Unified conflict-resolved script
```

---

## 5. ML Engineering Best Practices for Conflict Prevention

1. **Decouple Component Responsibilities**: Structure pipelines with modular interfaces (`Trainer`, `ModelBackbone`, `OptimizerBuilder`).
2. **Rebase Frequently**: Feature branches should rebase onto `develop` regularly (`git pull --rebase origin develop`).
3. **Atomic Pull Requests**: Keep pull requests small and focused on a single responsibility.
4. **Data & Artifact Isolation**: Track datasets and model weights via DVC or cloud registries, never committing large binaries to Git.
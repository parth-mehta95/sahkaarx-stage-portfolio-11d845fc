# Machine Learning Pipeline Conflict Resolution Guide & Case Study

## 1. Overview & Scenario Background

In a fast-paced Machine Learning team, multiple engineers often iterate on the core training and modeling pipeline simultaneously. When branches diverge and touch the same model training script or data loader logic, **merge conflicts** occur.

This case study documents a real-world scenario where two concurrent feature branches modified `src/train.py`:

- **Branch 1 (`feature/hyperparameter-tuning`)**: Authored by Engineer A. Introduces Optuna Bayesian hyperparameter optimization, dynamic learning rate scheduling (`CosineAnnealingLR`), and validation loss tracking.
- **Branch 2 (`feature/model-architecture-upgrade`)**: Authored by Engineer B. Upgrades the base neural network to an enhanced deep architecture with residual skip connections, layer normalization, dropout regularization, and gradient clipping.

Both engineers modified the same class definition (`MLTrainer`) and training execution block in `src/train.py`.

---

## 2. Feature Branch Structure & Divergence

### 2.1 Timeline of Events

```
        C1 (Initial ML Pipeline)
        │
        ├───[feature/hyperparameter-tuning]────────► C2 (Add Optuna & LR Scheduler) ──┐ (Merged into develop first)
        │                                                                             ▼
develop ┴─────────────────────────────────────────────────────────────────────────────► M1 (Merged cleanly)
        │                                                                             ▲
        └───[feature/model-architecture-upgrade]───► C3 (Add Deep Model & Clip) ──────┘ (CONFLICT DETECTED!)
```

1. Both branches branched off `develop` at commit `C1`.
2. **Branch 1 (`feature/hyperparameter-tuning`)** finished first, submitted a Pull Request, passed CI, and merged into `develop` at commit `M1`.
3. **Branch 2 (`feature/model-architecture-upgrade`)** attempted to merge into `develop`. Git detected conflicting edits in `src/train.py`.

---

## 3. The Merge Conflict

### 3.1 Git Commands Triggering the Conflict

When merging `feature/model-architecture-upgrade` into `develop`:

```bash
# Checkout the target integration branch
git checkout develop
git pull origin develop

# Attempt to merge the incoming feature branch
git merge feature/model-architecture-upgrade
```

**Git Terminal Output:**
```text
Auto-merging src/train.py
CONFLICT (content): Merge conflict in src/train.py
Automatic merge failed; fix conflicts and then commit the result.
```

### 3.2 Checking Conflict Status

```bash
git status
```

**Status Output:**
```text
On branch develop
You have unmerged paths.
  (fix conflicts and run "git commit")
  (use "git merge --abort" to abort the merge)

Unmerged paths:
  (use "git add <file>..." to mark resolution)
	both modified:   src/train.py

no changes added to commit (use "git add" to track)
```

---

## 4. Conflict Inspection & Analysis

Inspecting the conflicting section in `src/train.py` using `git diff`:

```python
<<<<<<< HEAD
    # =========================================================================
    # Branch: feature/hyperparameter-tuning (develop upstream)
    # Added: Optuna Study trial integration & Cosine Annealing LR Scheduler
    # =========================================================================
    def __init__(self, model, lr=1e-3, weight_decay=1e-4, use_scheduler=True, t_max=10):
        self.model = model
        self.optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=weight_decay)
        self.scheduler = (
            torch.optim.lr_scheduler.CosineAnnealingLR(self.optimizer, T_max=t_max)
            if use_scheduler else None
        )
        self.criterion = torch.nn.CrossEntropyLoss()

    def train_epoch(self, dataloader, trial=None):
        self.model.train()
        total_loss = 0.0
        for batch_idx, (data, targets) in enumerate(dataloader):
            self.optimizer.zero_grad()
            outputs = self.model(data)
            loss = self.criterion(outputs, targets)
            loss.backward()
            self.optimizer.step()
            total_loss += loss.item()

        if self.scheduler:
            self.scheduler.step()
            
        return total_loss / len(dataloader)
=======
    # =========================================================================
    # Branch: feature/model-architecture-upgrade (incoming feature branch)
    # Added: Deep Architecture with Residual Skip & Gradient Clipping
    # =========================================================================
    def __init__(self, model, lr=1e-3, max_grad_norm=1.0, label_smoothing=0.1):
        self.model = model
        self.optimizer = torch.optim.Adam(model.parameters(), lr=lr)
        self.max_grad_norm = max_grad_norm
        self.criterion = torch.nn.CrossEntropyLoss(label_smoothing=label_smoothing)

    def train_epoch(self, dataloader):
        self.model.train()
        total_loss = 0.0
        for batch_idx, (data, targets) in enumerate(dataloader):
            self.optimizer.zero_grad()
            outputs = self.model(data)
            loss = self.criterion(outputs, targets)
            loss.backward()
            
            # Gradient clipping to prevent exploding gradients
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), self.max_grad_norm)
            
            self.optimizer.step()
            total_loss += loss.item()
            
        return total_loss / len(dataloader)
>>>>>>> feature/model-architecture-upgrade
```

---

## 5. Resolution Strategy & Decision Matrix

In ML engineering, resolving conflicts is **not** a matter of blindly accepting "ours" (`HEAD`) or "theirs" (`feature/model-architecture-upgrade`). Doing so would discard either the hyperparameter tuning capability or the architectural robustness.

### 5.1 Synthesis Decision Matrix

| Dimension | Branch A (`HEAD` / Tuning) | Branch B (Incoming / Arch) | Unified Resolution Decision | Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **Optimizer** | `AdamW` with weight decay | `Adam` standard | **`AdamW` with weight decay** | `AdamW` decouples weight decay and produces superior generalization in deep architectures. |
| **LR Scheduler** | `CosineAnnealingLR` | None | **Retain `CosineAnnealingLR`** | Dynamic scheduling improves convergence when training deep models. |
| **Gradient Clipping**| None | `clip_grad_norm_` (1.0) | **Retain Gradient Clipping** | Essential guard against gradient explosion in deep networks with residual connections. |
| **Loss Function** | Standard `CrossEntropyLoss` | Label Smoothing (0.1) | **Parametrized `CrossEntropyLoss`** | Make `label_smoothing` configurable with default `0.1` for regularization. |
| **Pruning Hooks** | `trial` parameter for Optuna | None | **Retain `trial=None` hook** | Enables early stopping of unpromising trials during hyperparameter sweeps. |

---

## 6. The Cleanly Resolved Code

The conflicting markers were manually removed, and the logic was unified cleanly:

```python
    # =========================================================================
    # UNIFIED RESOLUTION: Integrated both architecture guards & tuning hooks
    # =========================================================================
    def __init__(
        self,
        model,
        lr: float = 1e-3,
        weight_decay: float = 1e-4,
        max_grad_norm: float = 1.0,
        label_smoothing: float = 0.1,
        use_scheduler: bool = True,
        t_max: int = 10,
    ):
        self.model = model
        self.max_grad_norm = max_grad_norm
        # AdamW with weight decay (from Branch A)
        self.optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=weight_decay)
        # Cosine Annealing Scheduler (from Branch A)
        self.scheduler = (
            torch.optim.lr_scheduler.CosineAnnealingLR(self.optimizer, T_max=t_max)
            if use_scheduler else None
        )
        # Loss with label smoothing (from Branch B)
        self.criterion = torch.nn.CrossEntropyLoss(label_smoothing=label_smoothing)

    def train_epoch(self, dataloader, trial=None) -> float:
        """
        Executes one training epoch with gradient clipping and scheduler stepping.
        Supports Optuna trial pruning hooks.
        """
        self.model.train()
        total_loss = 0.0
        
        for batch_idx, (data, targets) in enumerate(dataloader):
            self.optimizer.zero_grad()
            outputs = self.model(data)
            loss = self.criterion(outputs, targets)
            loss.backward()
            
            # Gradient clipping from Branch B
            if self.max_grad_norm > 0:
                torch.nn.utils.clip_grad_norm_(self.model.parameters(), self.max_grad_norm)
                
            self.optimizer.step()
            total_loss += loss.item()

        # Step scheduler at epoch boundary from Branch A
        if self.scheduler is not None:
            self.scheduler.step()
            
        avg_loss = total_loss / max(len(dataloader), 1)
        return avg_loss
```

---

## 7. Verification & Commit Steps

### 7.1 Local Verification

Before finalizing the merge commit, execute the unit test and pipeline smoke verification to verify both components function in harmony:

```bash
# Verify Python syntax
python -m py_compile src/train.py

# Run test suite
pytest tests/ -v

# Run verification smoke test
python src/train.py --smoke-test
```

### 7.2 Finalizing the Merge Commit

Once verification passes:

```bash
# 1. Stage the resolved file
git add src/train.py

# 2. Verify staging status
git status

# 3. Complete the merge commit with descriptive message
git commit -m "Merge branch 'feature/model-architecture-upgrade' into develop

Resolved conflict in src/train.py:
- Preserved AdamW optimizer and CosineAnnealingLR scheduler from feature/hyperparameter-tuning
- Incorporated gradient clipping and label smoothing from feature/model-architecture-upgrade
- Verified end-to-end training pipeline with smoke test suite"

# 4. Push the resolved integration branch to remote
git push origin develop
```

---

## 8. Best Practices for Preventing Merge Conflicts in ML Projects

1. **Modular Architecture**: Separate model definitions (`src/models/`), optimizers/schedulers (`src/optim/`), and training orchestration (`src/trainer.py`). When different engineers touch different concerns, Git can merge them automatically.
2. **Frequent Synchronizations**: Rebase feature branches onto `develop` at least once daily (`git pull --rebase origin develop`).
3. **Small, Atomic Pull Requests**: Keep PRs focused on a single responsibility (e.g. PR for optimizer, separate PR for model architecture).
4. **Configuration-Driven Design**: Use YAML/Hydra configuration files for hyperparameters rather than hardcoding them into trainer classes.

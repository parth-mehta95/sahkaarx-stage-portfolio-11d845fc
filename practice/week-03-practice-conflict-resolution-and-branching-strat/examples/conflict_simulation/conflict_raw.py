"""
Raw Merge Conflict Representation
File: src/train.py
Occurred when merging feature/model-architecture-upgrade into develop (which already contained feature/hyperparameter-tuning).
"""

# [START RAW GIT CONFLICT REGION]
<<<<<<< HEAD
# Branch: develop (containing feature/hyperparameter-tuning)
class MLTrainer:
    def __init__(self, model, lr=1e-3, weight_decay=1e-4, use_scheduler=True, t_max=10):
        self.model = model
        self.lr = lr
        self.weight_decay = weight_decay
        self.use_scheduler = use_scheduler
        self.t_max = t_max
        self.scheduler_active = True

    def train_epoch(self, dataloader, trial=None):
        total_loss = 0.0
        for batch_idx, (data, targets) in enumerate(dataloader):
            loss = 0.50
            total_loss += loss
            
        if self.use_scheduler:
            self.lr = self.lr * 0.95
            
        avg_loss = total_loss / len(dataloader)
        if trial is not None:
            trial.report(avg_loss, step=1)
            
        return avg_loss
=======
# Branch: feature/model-architecture-upgrade
class MLTrainer:
    def __init__(self, model, lr=1e-3, max_grad_norm=1.0, label_smoothing=0.1):
        self.model = model
        self.lr = lr
        self.max_grad_norm = max_grad_norm
        self.label_smoothing = label_smoothing

    def train_epoch(self, dataloader):
        total_loss = 0.0
        for batch_idx, (data, targets) in enumerate(dataloader):
            loss = 0.48
            clipped_norm = min(1.2, self.max_grad_norm)
            total_loss += loss
            
        avg_loss = total_loss / len(dataloader)
        return avg_loss
>>>>>>> feature/model-architecture-upgrade
# [END RAW GIT CONFLICT REGION]

"""Shared result type and small helpers used by every check."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

import numpy as np
from sklearn.model_selection import StratifiedKFold, cross_val_predict

Status = Literal["pass", "warn", "skip"]


@dataclass
class CheckResult:
    name: str
    status: Status
    summary: str
    metrics: dict[str, Any] = field(default_factory=dict)
    details: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.status not in ("pass", "warn", "skip"):
            raise ValueError(f"status must be 'pass', 'warn' or 'skip', got {self.status!r}")


def cv_predict(model, X, y, cv=5, random_state=0) -> np.ndarray:
    """Out-of-fold predictions from shuffled stratified k-fold (a fresh clone of `model` per fold)."""
    folds = StratifiedKFold(cv, shuffle=True, random_state=random_state)
    return cross_val_predict(model, np.asarray(X), np.asarray(y), cv=folds)


def cv_accuracy(model, X, y, cv=5, random_state=0) -> float:
    return float(np.mean(cv_predict(model, X, y, cv, random_state) == np.asarray(y)))

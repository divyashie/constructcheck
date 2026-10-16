"""Shared result type and small helpers used by every check."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

import numpy as np
from sklearn.base import clone
from sklearn.model_selection import StratifiedKFold

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


def cv_accuracy(model, X, y, cv=5, random_state=0) -> float:
    """Stratified k-fold accuracy with out-of-fold predictions pooled, fitting a fresh clone per fold."""
    X, y = np.asarray(X), np.asarray(y)
    folds = StratifiedKFold(cv, shuffle=True, random_state=random_state)
    correct = 0
    for tr, te in folds.split(X, y):
        pred = clone(model).fit(X[tr], y[tr]).predict(X[te])
        correct += int((pred == y[te]).sum())
    return correct / len(y)

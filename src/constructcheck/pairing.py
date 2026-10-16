"""Check 1: pairing test. Does the model need modality A and B to come from the same person?

Shuffle modality B's rows relative to A (labels stay with A) and retrain. If the modalities are
genuinely paired, accuracy should fall. With shuffle="within_class" (default) B rows are only swapped
between rows of the same label, so B keeps its label signal and only the person-level pairing is broken.
This catches fused datasets built by matching rows on label, where an across-class shuffle would
show a large drop even though no real pairing exists.
"""

from __future__ import annotations

import numpy as np

from .result import CheckResult, cv_accuracy


def shuffle_index(y, rng, within_class=True) -> np.ndarray:
    """Row permutation; with within_class, rows are only permuted among rows sharing a label."""
    y = np.asarray(y)
    if not within_class:
        return rng.permutation(len(y))
    idx = np.arange(len(y))
    for c in np.unique(y):
        pos = np.flatnonzero(y == c)
        idx[pos] = rng.permutation(pos)
    return idx


def pairing_test(
    df, modality_a_cols, modality_b_cols, label_col, model,
    cv=5, min_drop=0.10, random_state=0, shuffle="within_class",
) -> CheckResult:
    if shuffle not in ("within_class", "across"):
        raise ValueError("shuffle must be 'within_class' or 'across'")
    name = "pairing_test"
    A, B = df[list(modality_a_cols)].to_numpy(), df[list(modality_b_cols)].to_numpy()
    y = df[label_col].to_numpy()

    def acc(X):
        return cv_accuracy(model, X, y, cv, random_state)

    rng = np.random.default_rng(random_state)
    perm = shuffle_index(y, rng, within_class=shuffle == "within_class")
    paired, shuffled = acc(np.hstack([A, B])), acc(np.hstack([A, B[perm]]))
    drop = paired - shuffled

    metrics = {
        "paired_acc": paired,
        "shuffled_acc": shuffled,
        "drop": drop,
        "modality_a_only_acc": acc(A),
        "modality_b_only_acc": acc(B),
    }
    details = {"shuffle": shuffle, "cv": cv, "min_drop": min_drop, "n": len(y)}

    if drop < min_drop:
        effect = f"drops accuracy by only {drop:.3f}" if drop >= 0 else f"raises accuracy by {-drop:.3f}"
        summary = (f"Breaking the A-B pairing ({shuffle} shuffle) {effect} "
                   f"(threshold {min_drop:.3f}); the modalities may not be contributing jointly.")
        return CheckResult(name, "warn", summary, metrics, details)
    summary = f"Breaking the A-B pairing ({shuffle} shuffle) drops accuracy by {drop:.3f}; pairing carries signal."
    return CheckResult(name, "pass", summary, metrics, details)

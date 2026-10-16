"""Check 3: out-of-population. Does performance hold when a whole group (site, source, cohort) is unseen?"""

from __future__ import annotations

import numpy as np
from sklearn.model_selection import LeaveOneGroupOut, cross_val_predict

from .result import CheckResult, cv_predict


def out_of_population(df, feature_cols, label_col, group_col, model, max_drop=0.10, cv=5, random_state=0) -> CheckResult:
    name = "out_of_population"
    groups = df[group_col].to_numpy()
    unique = list(dict.fromkeys(groups))
    if len(unique) < 2:
        return CheckResult(name, "skip", f"Only {len(unique)} group in '{group_col}'; need at least 2.")

    X, y = df[list(feature_cols)].to_numpy(), df[label_col].to_numpy()
    within = cv_predict(model, X, y, cv, random_state) == y
    logo = cross_val_predict(model, X, y, groups=groups, cv=LeaveOneGroupOut()) == y

    per_group = {}
    for g in unique:
        m = groups == g
        w, o = float(within[m].mean()), float(logo[m].mean())
        per_group[str(g)] = {"n": int(m.sum()), "within_acc": w, "held_out_acc": o, "drop": w - o}

    worst = max(per_group, key=lambda g: per_group[g]["drop"])
    metrics = {
        "within_population_acc": float(within.mean()),
        "leave_one_group_out_acc": float(logo.mean()),
        "drop": float(within.mean() - logo.mean()),
        "worst_group": worst,
        "worst_group_drop": per_group[worst]["drop"],
        "n_groups": len(unique),
    }
    details = {"per_group": per_group, "group_col": group_col, "max_drop": max_drop}

    d = per_group[worst]["drop"]
    if d > max_drop:
        summary = f"Accuracy drops by {d:.2f} when group '{worst}' is held out (threshold {max_drop:.2f})."
        return CheckResult(name, "warn", summary, metrics, details)
    summary = f"Held-out-group accuracy stays within {max_drop:.2f} of within-population accuracy for all {len(unique)} groups."
    return CheckResult(name, "pass", summary, metrics, details)

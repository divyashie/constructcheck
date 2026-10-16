"""Check 2: subject overlap. Do the two modality tables describe the same people, labelled the same way?"""

from __future__ import annotations

from .result import CheckResult


def subject_overlap(df_a, df_b, subject_col, label_col, min_agreement=0.9) -> CheckResult:
    name = "subject_overlap"
    ids_a, ids_b = set(df_a[subject_col]), set(df_b[subject_col])
    shared = ids_a & ids_b
    overlap_fraction = len(shared) / len(ids_a | ids_b) if ids_a | ids_b else 0.0

    values_a, values_b = set(df_a[label_col].dropna()), set(df_b[label_col].dropna())
    dist_a = df_a[label_col].value_counts(normalize=True)
    dist_b = df_b[label_col].value_counts(normalize=True)
    tvd = float(0.5 * dist_a.sub(dist_b, fill_value=0).abs().sum())

    # On shared subjects, compare each subject's most common label in A vs B.
    agreement = None
    if shared:
        mode_a = df_a[df_a[subject_col].isin(shared)].groupby(subject_col)[label_col].agg(lambda s: s.mode().iloc[0])
        mode_b = df_b[df_b[subject_col].isin(shared)].groupby(subject_col)[label_col].agg(lambda s: s.mode().iloc[0])
        agreement = float((mode_a == mode_b.reindex(mode_a.index)).mean())

    metrics = {
        "n_subjects_a": len(ids_a),
        "n_subjects_b": len(ids_b),
        "n_shared": len(shared),
        "overlap_fraction": overlap_fraction,
        "label_tvd": tvd,
        "shared_label_agreement": agreement,
    }
    details = {
        "label_values_a": sorted(map(str, values_a)),
        "label_values_b": sorted(map(str, values_b)),
        "label_distribution_a": {str(k): float(v) for k, v in dist_a.items()},
        "label_distribution_b": {str(k): float(v) for k, v in dist_b.items()},
    }

    problems = []
    if not shared:
        problems.append("the two tables share no subject IDs")
    if values_a != values_b:
        problems.append(f"label values differ ({details['label_values_a']} vs {details['label_values_b']})")
    if agreement is not None and agreement < min_agreement:
        problems.append(f"only {agreement:.0%} of shared subjects have the same label in both tables")

    if problems:
        return CheckResult(name, "warn", "Possible construct mismatch: " + "; ".join(problems) + ".", metrics, details)
    summary = f"{len(shared)} shared subjects ({overlap_fraction:.0%} of all IDs) with consistent label definitions."
    return CheckResult(name, "pass", summary, metrics, details)

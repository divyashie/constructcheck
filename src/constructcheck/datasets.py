"""Synthetic datasets: one where the modalities really describe the same people, one where they don't.

Both return a dict with:
    "a", "b"   per-modality tables (subject_id, features, label[, source])
    "fused"    the row-aligned table a practitioner would train on
    "a_cols", "b_cols"  feature column names
"""

from __future__ import annotations

import numpy as np
import pandas as pd

A_COLS = ["a0", "a1"]
B_COLS = ["b0", "b1"]


def _out(df_a, df_b, fused):
    return {"a": df_a, "b": df_b, "fused": fused, "a_cols": list(A_COLS), "b_cols": list(B_COLS)}


def make_linked(n=500, seed=0):
    """Two modalities measured on the same subjects, generated from a shared latent.

    Each subject has a baseline `s` seen by both modalities plus a modality-specific state (e1, e2).
    The label is the contrast e1 > e2, so it is only recoverable from correctly paired A and B rows.
    `source` holds two sites drawn from the same population.
    """
    rng = np.random.default_rng(seed)
    ids = [f"S{i:04d}" for i in range(n)]
    s, e1, e2 = 2 * rng.normal(size=n), rng.normal(size=n), rng.normal(size=n)
    label = (e1 > e2).astype(int)
    source = rng.choice(["site_1", "site_2"], size=n)

    df_a = pd.DataFrame({"subject_id": ids, "a0": s + e1 + 0.3 * rng.normal(size=n),
                         "a1": rng.normal(size=n), "label": label, "source": source})
    df_b = pd.DataFrame({"subject_id": ids, "b0": s + e2 + 0.3 * rng.normal(size=n),
                         "b1": rng.normal(size=n), "label": label})
    fused = df_a.merge(df_b.drop(columns="label"), on="subject_id")
    return _out(df_a, df_b, fused)


def make_mismatched(n=500, seed=0):
    """Two modalities from unrelated populations, fused by matching rows on label.

    - Modality A comes from two sources whose feature distributions differ (site_2 is shifted, and its
      label is defined relative to its own norm); the label is driven by A only.
    - Modality B comes from a different cohort with disjoint subject IDs and its own label prevalence;
      its features relate only to its own label.
    - `fused` pairs each A row with a random B row of the same label (label-conditional pairing).
    """
    rng = np.random.default_rng(seed)
    source = np.repeat(["site_1", "site_2"], [n // 2, n - n // 2])
    shift = np.where(source == "site_2", 1.5, 0.0)
    signal = rng.normal(size=n)
    df_a = pd.DataFrame({
        "subject_id": [f"A{i:04d}" for i in range(n)],
        "a0": signal + shift + 0.3 * rng.normal(size=n),
        "a1": shift + 0.3 * rng.normal(size=n),  # site/device calibration offset
        "label": (signal > 0).astype(int),
        "source": source,
    })

    b_label = (rng.random(n) < 0.7).astype(int)
    df_b = pd.DataFrame({
        "subject_id": [f"B{i:04d}" for i in range(n)],
        "b0": 5 + 0.8 * b_label + rng.normal(size=n),
        "b1": rng.exponential(2.0, size=n),
        "label": b_label,
    })

    b_rows = np.empty(n, dtype=int)
    for c in (0, 1):
        a_pos = np.flatnonzero(df_a["label"].to_numpy() == c)
        b_rows[a_pos] = rng.choice(np.flatnonzero(b_label == c), size=len(a_pos), replace=True)
    fused = pd.concat([df_a.reset_index(drop=True),
                       df_b.iloc[b_rows][B_COLS].reset_index(drop=True)], axis=1)
    return _out(df_a, df_b, fused)

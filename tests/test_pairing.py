import numpy as np
import pandas as pd
import pytest

from constructcheck import pairing_test
from constructcheck.pairing import shuffle_index


def _paired(linked, n=600):
    # Shared per-person baseline s; label depends on the A-vs-B contrast, so only true pairs reveal it.
    rng = np.random.default_rng(0)
    s, e1, e2 = 2 * rng.normal(size=n), rng.normal(size=n), rng.normal(size=n)
    y = (e1 > e2).astype(int) if linked else (e1 > 0).astype(int)
    a = (s if linked else 0) + e1
    b = s + e2 if linked else rng.normal(size=n)
    return pd.DataFrame({"a0": a, "b0": b, "y": y})


def test_shuffle_index_keeps_labels():
    y = np.array([0, 0, 1, 1, 1, 2])
    idx = shuffle_index(y, np.random.default_rng(0))
    assert (y[idx] == y).all() and sorted(idx) == list(range(len(y)))


@pytest.mark.parametrize("data, expected", [("linked", "pass"), ("mismatched", "warn")])
def test_synthetic_datasets(data, expected, model, request):
    d = request.getfixturevalue(data)
    r = pairing_test(d["fused"], d["a_cols"], d["b_cols"], "label", model)
    assert r.status == expected, r.summary


def test_linked_passes(model):
    r = pairing_test(_paired(True), ["a0"], ["b0"], "y", model)
    assert r.status == "pass", r.summary


def test_unlinked_warns(model):
    r = pairing_test(_paired(False), ["a0"], ["b0"], "y", model)
    assert r.status == "warn", r.summary
    assert set(r.metrics) >= {"paired_acc", "shuffled_acc", "modality_a_only_acc", "modality_b_only_acc"}


def test_warn_summary_states_unsigned_drop(model, mismatched):
    r = pairing_test(mismatched["fused"], mismatched["a_cols"], mismatched["b_cols"], "label", model)
    assert f"drops accuracy by only {r.metrics['drop']:.3f}" in r.summary


def test_warn_summary_when_shuffling_raises_accuracy(model, monkeypatch):
    # Paired fit first, then shuffled, then A-only and B-only.
    accs = iter([0.70, 0.712, 0.6, 0.6])
    monkeypatch.setattr("constructcheck.pairing.cv_accuracy", lambda *a: next(accs))
    r = pairing_test(_paired(False), ["a0"], ["b0"], "y", model)
    assert r.status == "warn"
    assert r.summary.startswith("Accuracy rises by 0.012 when the A-B pairing is broken"), r.summary

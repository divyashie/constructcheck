import pandas as pd

from constructcheck import subject_overlap


def _table(ids, labels):
    return pd.DataFrame({"sid": ids, "y": labels})


def test_shared_subjects_same_labels_pass():
    a = _table(["p1", "p2", "p3", "p4"], [0, 1, 0, 1])
    b = _table(["p1", "p2", "p3", "p4"], [0, 1, 0, 1])
    r = subject_overlap(a, b, "sid", "y")
    assert r.status == "pass", r.summary
    assert r.metrics["overlap_fraction"] == 1.0


def test_disjoint_subjects_and_label_sets_warn():
    a = _table(["p1", "p2"], [0, 1])
    b = _table(["q1", "q2"], ["low", "high"])
    r = subject_overlap(a, b, "sid", "y")
    assert r.status == "warn"
    assert r.metrics["n_shared"] == 0
    assert "share no subject" in r.summary and "label values differ" in r.summary


def test_shared_subjects_disagreeing_labels_warn():
    a = _table(["p1", "p2", "p3", "p4"], [0, 1, 0, 1])
    b = _table(["p1", "p2", "p3", "p4"], [1, 0, 0, 1])
    r = subject_overlap(a, b, "sid", "y")
    assert r.status == "warn"
    assert r.metrics["shared_label_agreement"] == 0.5

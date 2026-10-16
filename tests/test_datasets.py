def test_linked_shares_subjects(linked):
    assert set(linked["a"]["subject_id"]) == set(linked["b"]["subject_id"])
    assert len(linked["fused"]) == 500 and linked["fused"]["source"].nunique() == 2


def test_mismatched_is_disjoint_and_row_aligned(mismatched):
    assert not set(mismatched["a"]["subject_id"]) & set(mismatched["b"]["subject_id"])
    f = mismatched["fused"]
    assert len(f) == 500 and set(mismatched["a_cols"] + mismatched["b_cols"]) <= set(f.columns)

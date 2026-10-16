import numpy as np
import pandas as pd
import pytest

from constructcheck import out_of_population


@pytest.mark.parametrize("data, expected", [("linked", "pass"), ("mismatched", "warn")])
def test_synthetic_datasets(data, expected, model, request):
    d = request.getfixturevalue(data)
    r = out_of_population(d["fused"], d["a_cols"] + d["b_cols"], "label", "source", model)
    assert r.status == expected, r.summary


def _two_sites(flip_second):
    rng = np.random.default_rng(0)
    n = 300
    x = rng.normal(size=(2 * n, 2))
    site = np.repeat(["s1", "s2"], n)
    sign = np.where((site == "s2") & flip_second, -1, 1)
    y = (sign * x[:, 0] > 0).astype(int)
    return pd.DataFrame({"f0": x[:, 0], "f1": x[:, 1], "y": y, "site": site})


def test_same_population_passes(model):
    r = out_of_population(_two_sites(False), ["f0", "f1"], "y", "site", model)
    assert r.status == "pass", r.summary
    assert set(r.details["per_group"]) == {"s1", "s2"}


def test_shifted_population_warns(model):
    r = out_of_population(_two_sites(True), ["f0", "f1"], "y", "site", model)
    assert r.status == "warn", r.summary


def test_single_group_skips(model):
    df = _two_sites(False).assign(site="only")
    assert out_of_population(df, ["f0", "f1"], "y", "site", model).status == "skip"

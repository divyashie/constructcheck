import pytest

from constructcheck import CheckResult


def test_check_result_rejects_bad_status():
    assert CheckResult("x", "pass", "ok").metrics == {}
    with pytest.raises(ValueError):
        CheckResult("x", "fail", "nope")

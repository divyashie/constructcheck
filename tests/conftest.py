import pytest
from sklearn.linear_model import LogisticRegression

from constructcheck.datasets import make_linked, make_mismatched


@pytest.fixture
def model():
    return LogisticRegression(max_iter=1000)


@pytest.fixture(scope="session")
def linked():
    return make_linked()


@pytest.fixture(scope="session")
def mismatched():
    return make_mismatched()

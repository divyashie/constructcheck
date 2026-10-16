import pytest
from sklearn.linear_model import LogisticRegression


@pytest.fixture
def model():
    return LogisticRegression(max_iter=1000)

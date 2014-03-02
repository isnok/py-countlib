import pytest

from countlib import ExtremeCounter
from collections import Counter
from pivot import PivotCounter

@pytest.fixture
def abc():
    return ExtremeCounter("abc")

@pytest.fixture
def abctwo():
    return ExtremeCounter("abcabbcccddeefgggggghiii")

def test__getitem__(abc, abctwo):
    assert ExtremeCounter()["x"] == 0
    assert abc["x"] == 0
    assert abctwo["b"] == 3

    assert abc["a"] == abc["b"] == abc["c"] == 1
    #assert len(abc[1:2]) == 3

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
    assert not abc[0:1]
    assert len(abc[1:2]) == 3
    assert len(abc[:2]) == 3
    assert len(abc[1:]) == 3
    assert len(abc[:]) == 3

    assert len(abc[0:1:-1]) == 3
    assert len(abc[1:2:-1]) == 0
    assert len(abc[:2:-1]) == 0
    assert len(abc[1::-1]) == 0
    assert len(abc[::-1]) == 0

    assert not abctwo[0:1]
    assert len(abctwo[1:2]) == 2
    assert len(abctwo[2:]) == 7
    assert len(abctwo[:]) == 9

    assert len(abctwo[0:1:-1]) == 9
    assert len(abctwo[1:2:-1]) == 7
    assert len(abctwo[2::-1]) == 2
    assert len(abctwo[::-1]) == 0

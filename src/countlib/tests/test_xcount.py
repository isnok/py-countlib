import pytest

from countlib import ExtremeCounter
from collections import Counter
from countlib import PivotCounter

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

def test_pivot():
    x = ExtremeCounter("yay? nice!! this thing works!")
    x.update("etsttseststttsetsetse ")
    assert x.transpose().pivot(PivotCounter) == PivotCounter({1: [5, 6, 9, 11], 2: [3], 3: [2], 8: [1]})
    x.__pivot__ = PivotCounter
    assert x.pivot() + x.pivot() == PivotCounter(
            {10: [' '], 12: ['e'], 18: ['s'], 22: ['t'],
              2: ['?', 'a', 'c', 'g', 'k', 'o', 'r', 'w'],
              4: ['h', 'n', 'y'], 6: ['!', 'i']})
    lol = ExtremeCounter("lollofant!!")
    troll = ExtremeCounter("trollofant")
    assert lol.pivot() - troll.pivot() == PivotCounter({1: ['l'], 2: ['!']})
    assert lol.pivot() + troll.pivot() == PivotCounter({1: ['r'], 2: ['!', 'a', 'f', 'n'], 3: ['t'], 4: ['o'], 5: ['l']})

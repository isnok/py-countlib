import pytest

from countlib import AdvancedCounter
from countlib import ExtremeCounter
from countlib import PivotCounter
from countlib import CoolPivotCounter

advanced_counters = (AdvancedCounter, ExtremeCounter)

pivot_classes = set([PivotCounter, CoolPivotCounter])

@pytest.fixture
def test_generator():
    return (x for x in "test haha tst hehehe")

test_strings = (
    "abc", "abcabc", "abcbcc",
    "vnuiabve;uerv nvao;vna!!",
    "lalalladrhg",
    ".".join(list("lolllomat")),
)
test_lists = (
    range(3), list("bads"), list("multikulti"),
)
test_tuples = (
    tuple("baaam"), tuple("zooom"),
    tuple(range(12) * 4 + range(3,8)),
)
test_sets = (
    set(["fii", "beer"]), frozenset("testomat"),
)
test_dicts = (
    {"foo": 2, "bar": 5, "lol": -1},
    {"arg": 0, "neg": -199, "pos": 213872},
)
test_iterables = test_strings + test_lists + test_tuples + test_sets + test_dicts

##
#  Pivot data
##

@pytest.fixture
def other_pivots(TestPivotCounter):
    return pivot_classes.difference([TestPivotCounter])

@pytest.fixture
def TestSet(TestPivotCounter):
    if TestPivotCounter == PivotCounter:
        return set
    elif TestPivotCounter == CoolPivotCounter:
        return frozenset

##
#  to be deprecated
##

@pytest.fixture
def cnt_abc(TestCounter):
    return advanced_counters[TestCounter == AdvancedCounter]("abc")

@pytest.fixture
def cnt_ab2(TestCounter):
    return advanced_counters[TestCounter == AdvancedCounter]("abcabbcccddeefgggggghiii")

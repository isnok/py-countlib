import pytest

from countlib import AdvancedCounter
from countlib import ExtremeCounter
from countlib import PivotCounter
from countlib import CoolPivotCounter
from collections import Counter

advanced_counters = (AdvancedCounter, ExtremeCounter)

pivot_classes = set([PivotCounter, CoolPivotCounter])

test_iterables = (
    "abc", "abcabc", "abcbcc",
    "vnuiabve;uerv nvao;vna!!",
    ".".join(list("lolllomat")),
    range(3), tuple(range(12) * 4 + range(3,8)),
    tuple("baaam"), tuple("zooom"),
    list("bads"), list("multikulti"),
    set(["fii", "beer"]), frozenset("testomat"),
    {"foo": 2, "bar": 5, "lol": -1},
    {"arg": 0, "neg": -199, "pos": 213872},
    None, # magic to insert a generator
)


custom_fixtures = {
    "TestCounter": advanced_counters,
    "TestPivotCounter" : pivot_classes,
    "_test_iterable": test_iterables,
}


def pytest_generate_tests(metafunc):
    for name, values in custom_fixtures.items():
        if name in metafunc.fixturenames:
            metafunc.parametrize(name, values)

@pytest.fixture
def test_iterable(_test_iterable):
    if _test_iterable is None:
        return (x for x in "test haha tst hehehe")
    return _test_iterable

@pytest.fixture
def other_pivots(TestPivotCounter):
    return pivot_classes.difference([TestPivotCounter])

@pytest.fixture
def TestSet(TestPivotCounter):
    if TestPivotCounter == PivotCounter:
        return set
    elif TestPivotCounter == CoolPivotCounter:
        return frozenset

@pytest.fixture
def cnt_abc(TestCounter):
    return advanced_counters[TestCounter == AdvancedCounter]("abc")

@pytest.fixture
def cnt_ab2(TestCounter):
    return advanced_counters[TestCounter == AdvancedCounter]("abcabbcccddeefgggggghiii")


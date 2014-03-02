import pytest

from countlib import AdvancedCounter
from countlib import ExtremeCounter
from countlib import PivotCounter
from countlib import CoolPivotCounter
from collections import Counter

advanced_counters = (AdvancedCounter, ExtremeCounter)

pivot_classes = set([PivotCounter, CoolPivotCounter])

def pytest_generate_tests(metafunc):
    if 'TestCounter' in metafunc.fixturenames:
        metafunc.parametrize('TestCounter', advanced_counters)
    if 'TestPivotCounter' in metafunc.fixturenames:
        metafunc.parametrize('TestPivotCounter', pivot_classes)

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


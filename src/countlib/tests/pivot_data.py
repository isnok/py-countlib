import pytest

from countlib import PivotCounter
from countlib import CoolPivotCounter

pivot_classes = set([PivotCounter, CoolPivotCounter])

pivot_data_fixtures = {
    "TestPivotCounter": pivot_classes,
}

@pytest.fixture
def other_pivots(TestPivotCounter):
    return pivot_classes.difference([TestPivotCounter])

@pytest.fixture
def TestSet(TestPivotCounter):
    if TestPivotCounter == PivotCounter:
        return set
    elif TestPivotCounter == CoolPivotCounter:
        return frozenset


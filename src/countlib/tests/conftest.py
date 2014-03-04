import pytest
from count_data import *
from pivot_data import *

def pytest_generate_tests(metafunc):
    custom_fixtures = {}
    custom_fixtures.update(count_data_fixtures)
    custom_fixtures.update(pivot_data_fixtures)
    for name, values in custom_fixtures.items():
        if name in metafunc.fixturenames:
            metafunc.parametrize(name, values)


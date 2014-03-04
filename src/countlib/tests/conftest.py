import pytest
from count_data import *
from pivot_data import *

custom_fixtures = {}
custom_fixtures.update(count_data_fixtures)
custom_fixtures.update(pivot_data_fixtures)

def return_returner(values):
    def returner():
        return values
    return returner

for name, values in custom_fixtures.items():
    names = name + 's' # test_iterable + s
    locals()[names] = return_returner(values)
    pytest.fixture(locals()[names])

def pytest_generate_tests(metafunc):
    for name, values in custom_fixtures.items():
        if name in metafunc.fixturenames:
            metafunc.parametrize(name, values)

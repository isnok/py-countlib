import pytest
from data import *

custom_fixtures = {
    "TestCounter"     : advanced_counters,
    "TestPivotCounter": pivot_classes,
    "test_iterable"   : test_iterables,
    "test_string"     : test_strings,
    "test_list"       : test_lists,
    "test_tuple"      : test_tuples,
    "test_set"        : test_sets,
    "test_dict"       : test_dicts,
}


def pytest_generate_tests(metafunc):
    for name, values in custom_fixtures.items():
        if name in metafunc.fixturenames:
            metafunc.parametrize(name, values)


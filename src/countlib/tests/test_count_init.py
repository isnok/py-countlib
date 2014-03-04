import pytest

from collections import Mapping
from types import IntType
from types import LongType

def test_class(TestCounter):
    tst = TestCounter()
    assert isinstance(tst, object)
    assert isinstance(tst, dict)
    assert isinstance(tst, TestCounter)
    assert isinstance(tst, Mapping)
    assert tst.__class__ == TestCounter

def test_dict(TestCounter):
    testval = TestCounter("true")
    assert testval
    assert bool(testval)
    assert (not testval) == False
    assert not TestCounter()
    assert (not TestCounter()) == True
    assert testval.keys()
    assert testval.items()
    assert testval.values()

def test_init_iterable(TestCounter, test_iterable):
    testval = TestCounter(test_iterable)
    sth = next(iter(test_iterable))
    assert sth in testval
    if not isinstance(test_iterable, Mapping):
        assert testval[sth] > 0
    v = testval[sth]
    assert isinstance(v, IntType) or isinstance(v, LongType)

def test_counting(TestCounter, test_listlike):
    tst = TestCounter(test_listlike)
    for k in test_listlike:
        assert tst[k] == test_listlike.count(k)

def test_init_generator(TestCounter, test_generator):
    testval = TestCounter(test_generator)
    assert testval == TestCounter({'a': 2, ' ': 3, 'e': 4, 'h': 5, 's': 2, 't': 4})

def test_init_counterlike(TestCounter, test_iterable):
    from collections import Counter
    assert TestCounter(test_iterable) == Counter(test_iterable)

def test_init_counterlike_generator(TestCounter):
    from collections import Counter
    assert TestCounter((x for x in "foo")) == Counter((x for x in "foo"))

def test_init_kwds_direct(TestCounter):
    val = TestCounter(a=4, more=9, test=-3)
    assert val == TestCounter({'a': 4, 'more': 9, 'test': -3})

def test_init_kwds(TestCounter, test_dict):
    assert TestCounter(**test_dict) == TestCounter(test_dict)


import pytest

from collections import Mapping
from types import GeneratorType
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

def test_elements(TestCounter, test_string):
    a = TestCounter(test_string)
    assert sorted(a.elements()) == sorted(test_string)

def test___missing__(TestCounter, test_key):
    value = TestCounter()
    assert test_key not in value
    assert value[test_key] is 0
    assert test_key not in value

def test__reduce__(TestCounter, test_dict):
    tst_counter = TestCounter(test_dict)
    import pickle
    pickled = pickle.dumps(tst_counter)
    assert pickled
    assert pickle.loads(pickled) == tst_counter

def test___delitem__(test_counter):
    del test_counter["not there"]
    for key in test_counter.keys():
        assert key in test_counter
        del test_counter[key]
        assert key not in test_counter

def test_most_common_static(TestCounter):
    p = TestCounter('abracadabra!')
    assert isinstance(p.most_common(), list)
    assert isinstance(p.most_common(1), list)
    assert not p.most_common(0)
    assert p.most_common(3) == [('a', 5), ('b', 2), ('r', 2)]
    assert p.most_common(2, inverse=True) == [('!', 1), ('c', 1)]
    assert p.most_common(2, count_func=lambda i: -i[1]) == [('!', 1), ('c', 1)]
    assert p.most_common(2, count_func=lambda i: -i[1], inverse=True) == [('a', 5), ('b', 2)]

def test_most_common_dynamic(TestCounter, test_string):
    tst = TestCounter(test_string)
    common, most = tst.most_common(1).pop()
    assert common in test_string
    assert most == test_string.count(common)
    for i in range(1,5):
        assert len(tst.most_common(i)) <= i

def test_most_common_counts_static(TestCounter):
    x = TestCounter("yay? nice!! this thing works!")
    x.add("etsttseststttsetsetse ")
    assert x.most_common_counts(1) == [('t', 11)]
    assert x.most_common_counts(5) == [('t', 11), ('s', 9), ('e', 6), (' ', 5), ('i', 3), ('!', 3)]
    assert x.most_common_counts(1)[0] == x.most_common(1).pop()

def test_most_common_counts_dynamic(TestCounter, test_string):
    tst = TestCounter(test_string)
    mc = sorted(tst.most_common())
    assert sorted(tst.most_common_counts(len(tst))) == mc
    assert tst.most_common_counts(len(tst)-1) != mc

def test_transpose(TestCounter):
    x = TestCounter("yay? nice!! this thing works!")
    assert isinstance(x.transpose(), TestCounter)
    x.add("etsttseststttsetsetse ")
    tp_chain = [
        TestCounter({1: 1}),
        TestCounter({2: 1}),
        TestCounter({1: 2}),
        TestCounter({1: 1, 3: 1}),
        TestCounter({1: 3, 4: 1}),
        TestCounter({1: 4, 2: 1, 3: 1, 8: 1}),
        TestCounter({11: 1, 1: 8, 2: 3, 3: 2, 5: 1, 6: 1, 9: 1}),
        TestCounter("yay? nice!! this thing works!" + "etsttseststttsetsetse "),
    ]
    old_x = None
    while old_x != x:
        old_x = x
        x = x.transpose()
        assert old_x == tp_chain.pop()

def test_fromkeys(TestCounter):
    assert TestCounter.fromkeys('bumm') == TestCounter({'b': 0, 'm': 0, 'u': 0})
    x = TestCounter.fromkeys('bubb', ['a'])
    assert x == TestCounter({'b': ['a'], 'u': ['a']})
    x["b"].append("x")
    assert x == TestCounter({'b': ['a', 'x'], 'u': ['a', 'x']})


def test___repr__(TestCounter, TestCounters):
    for cls in TestCounters:
        locals()[cls.__name__] = cls
    assert repr(TestCounter('b')) == "%s({'b': 1})" % TestCounter.__name__
    assert TestCounter("bumm") == eval("%s({'b': 1, 'm': 2, 'u': 1})" % TestCounter.__name__)
    for stuff in ('abc', 'bcccnnno', (12,12,3,4,5,3,3)):
        x = TestCounter(stuff)
        assert x == eval(repr(x))

def test___repr__dynamic(TestCounter, TestCounters, test_keys):
    from random import randint
    for cls in TestCounters:
        locals()[cls.__name__] = cls
    t = TestCounter()
    big = 1<<200
    for k in test_keys:
        t[k] = randint(-big, big)
    assert t == eval(repr(t))

def test___str__(TestCounter, TestCounters):
    for cls in TestCounters:
        locals()[cls.__name__] = cls
    for stuff in ('abc', 'bcccnnno', (12,12,3,4,5,3,3)):
        x = TestCounter(stuff)
        assert x == eval(str(x))

def test___str__dynamic(TestCounter, TestCounters, test_iterables):
    from random import randint
    for cls in TestCounters:
        locals()[cls.__name__] = cls
    strings = [ TestCounter(i).__str__() for i in test_iterables ]
    things = [ TestCounter(i) for i in test_iterables ]
    for a, b in zip(strings, things):
        assert a == str(b)
        assert eval(a) == b

def test_copy(TestCounter):
    a = TestCounter("holla")
    b = a.copy()
    assert b == a
    assert b is not a
    del a["o"]
    assert "o" in b
    assert b != a


if __name__ == '__main__':
    import pytest
    pytest.main()

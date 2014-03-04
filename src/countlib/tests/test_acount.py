import pytest

from collections import Counter
from types import GeneratorType

def test_init(TestCounter, test_iterable):
    testval = TestCounter(test_iterable)
    assert testval == Counter(test_iterable)

def test_init_generator(TestCounter, test_generator):
    testval = TestCounter(test_generator)
    assert testval == TestCounter({'a': 2, ' ': 3, 'e': 4, 'h': 5, 's': 2, 't': 4})

def test_class(TestCounter):
    assert TestCounter().__class__ == TestCounter
    assert isinstance(TestCounter(), dict)

def test_elements(TestCounter, test_string):
    a = TestCounter(test_string)
    assert sorted(a.elements()) == sorted(test_string)

def test_bool(TestCounter):
    testval = TestCounter("true")
    assert testval
    assert bool(testval)
    assert (not testval) == False
    assert not TestCounter()
    assert (not TestCounter()) == True

def test_most_common(TestCounter):
    p = TestCounter('abracadabra!')
    assert p.most_common(3) == [('a', 5), ('b', 2), ('r', 2)]
    assert p.most_common(2, inverse=True) == [('!', 1), ('c', 1)]
    assert p.most_common(2, count_func=lambda i: -i[1]) == [('!', 1), ('c', 1)]
    assert p.most_common(2, count_func=lambda i: -i[1], inverse=True) == [('a', 5), ('b', 2)]

def test_most_common_counts(TestCounter):
    x = TestCounter("yay? nice!! this thing works!")
    x.add("etsttseststttsetsetse ")
    assert x.most_common_counts(1) == [('t', 11)]
    assert x.most_common_counts(5) == [('t', 11), ('s', 9), ('e', 6), (' ', 5), ('i', 3), ('!', 3)]

def test_transpose(TestCounter):
    x = TestCounter("yay? nice!! this thing works!")
    x.add("etsttseststttsetsetse ")
    tp_chain = [
        TestCounter({1: 1}),
        TestCounter({2: 1}),
        TestCounter({1: 2}),
        TestCounter({1: 1, 3: 1}),
        TestCounter({1: 3, 4: 1}),
        TestCounter({1: 4, 2: 1, 3: 1, 8: 1}),
        TestCounter({11: 1, 1: 8, 2: 3, 3: 2, 5: 1, 6: 1, 9: 1}),
        TestCounter({' ': 5, '!': 3, '?': 1, 'a': 1, 'c': 1, 'e': 6, 'g': 1, 'h': 2, 'i': 3, 'k': 1, 'n': 2, 'o': 1, 'r': 1, 's': 9, 't': 11, 'w': 1, 'y': 2}),
    ]
    old_x = None
    while old_x != x:
        old_x = x
        x = x.transpose()
        assert old_x == tp_chain.pop()

def test_fromkeys(TestCounter):
    assert TestCounter.fromkeys('bumm') == TestCounter({'b': 0, 'm': 0, 'u': 0})
    x = TestCounter.fromkeys('bumm', 50)
    assert x == TestCounter({'b': 50, 'm': 50, 'u': 50})
    assert x + x == TestCounter({'b': 100, 'm': 100, 'u': 100})
    assert x + x == TestCounter.fromkeys(x, 50+50)

def test___repr__(TestCounter):
    from countlib import AdvancedCounter
    from countlib import ExtremeCounter
    assert TestCounter('bumm') == TestCounter({'b': 1, 'm': 2, 'u': 1})
    assert TestCounter({'b': 1, 'm': 2, 'u': 1}) == TestCounter({'b': 1, 'm': 2, 'u': 1})
    for stuff in ('abc', 'bcccnnno', (12,12,3,4,5,3,3)):
        x = TestCounter(stuff)
        assert x == eval(repr(x))

if __name__ == '__main__':
    import pytest
    pytest.main()

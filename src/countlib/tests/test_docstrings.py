import pytest

def test_class(TestCounter):
    c = TestCounter('abcdeabcdabcaba')

    assert sorted(c) == ['a', 'b', 'c', 'd', 'e']
    assert ''.join(sorted(c.elements()))   == 'aaaaabbbbcccdde'
    assert sum(c.values()) == 15

    assert c.most_common(3) == [('a', 5), ('b', 4), ('c', 3)]
    assert c.most_common_counts(1) == [('a', 5)]
    assert c.most_common_counts(2) == [('a', 5), ('b', 4)]

    assert c['a'] == 5
    for elem in 'shazam':
        c[elem] += 1
    assert c['a'] == 7

    del c['b']
    assert c['b'] == 0

    d = TestCounter('simsalabim')
    c.add(d)
    assert c['a'] == 9

    c.clear()
    assert c == TestCounter()

    c = TestCounter('aaabbc')
    c['b'] -= 2
    assert c.most_common() == [('a', 3), ('c', 1), ('b', 0)]

from collections import Counter

def test_features(TestCounter):
    assert TestCounter('zyzygy') == TestCounter({'g': 1, 'y': 3, 'z': 2})
    y = TestCounter("yay.")
    assert y + TestCounter.fromkeys('zab.', 3) == TestCounter({'.': 4, 'a': 4, 'b': 3, 'y': 2, 'z': 3})
    assert y - TestCounter.fromkeys('zab.', 3) == TestCounter({'y': 2})
    y.subtract(TestCounter.fromkeys('zab.', 3))
    assert y == TestCounter({'.': -2, 'a': -2, 'b': -3, 'y': 2, 'z': -3})
    y.add(TestCounter.fromkeys('zab.', 3))
    assert y == TestCounter({'.': 1, 'a': 1, 'b': 0, 'y': 2, 'z': 0})
    assert y + Counter() == TestCounter({'.': 1, 'a': 1, 'y': 2})
    assert y.transpose() == TestCounter({0: 2, 1: 2, 2: 1})


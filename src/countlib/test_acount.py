import pytest

from countlib import AdvancedCounter
from collections import Counter
from pivot import PivotCounter

@pytest.fixture
def abc():
    return AdvancedCounter("abc")

@pytest.fixture
def abctwo():
    return AdvancedCounter("abcabbcccddeefgggggghiii")

def test_class():
    assert AdvancedCounter('zyzygy') == AdvancedCounter({'g': 1, 'y': 3, 'z': 2})
    y = AdvancedCounter("yay.")
    assert y + AdvancedCounter.fromkeys('zab.', 3) == AdvancedCounter({'.': 4, 'a': 4, 'b': 3, 'y': 2, 'z': 3})
    assert y - AdvancedCounter.fromkeys('zab.', 3) == AdvancedCounter({'y': 2})
    y.subtract(AdvancedCounter.fromkeys('zab.', 3))
    assert y == AdvancedCounter({'.': -2, 'a': -2, 'b': -3, 'y': 2, 'z': -3})
    y.add(AdvancedCounter.fromkeys('zab.', 3))
    assert y == AdvancedCounter({'.': 1, 'a': 1, 'b': 0, 'y': 2, 'z': 0})
    assert y + Counter() == AdvancedCounter({'.': 1, 'a': 1, 'y': 2})
    assert y.pivot() == PivotCounter({0: ['b', 'z'], 1: ['.', 'a'], 2: ['y']})
    assert y.transpose() == AdvancedCounter({0: 2, 1: 2, 2: 1})

def test_bool(abc):
    assert abc
    assert bool(abc)
    assert (not abc) == False
    assert not AdvancedCounter()
    assert (not AdvancedCounter()) == True

def test_most_common():
    p = AdvancedCounter('abracadabra!')
    assert p.most_common(3) == [('a', 5), ('b', 2), ('r', 2)]
    assert p.most_common(2, inverse=True) == [('!', 1), ('c', 1)]
    assert p.most_common(2, count_func=lambda i: -i[1]) == [('!', 1), ('c', 1)]
    assert p.most_common(2, count_func=lambda i: -i[1], inverse=True) == [('a', 5), ('b', 2)]

def test_most_common_counts():
    x = AdvancedCounter("yay? nice!! this thing works!")
    x.update("etsttseststttsetsetse ")
    assert x.most_common_counts(1) == [('t', 11)]
    assert x.most_common_counts(5) == [('t', 11), ('s', 9), ('e', 6), (' ', 5), ('i', 3), ('!', 3)]

def test_pivot():
    x = AdvancedCounter("yay? nice!! this thing works!")
    x.update("etsttseststttsetsetse ")
    assert x.transpose().pivot(PivotCounter) == PivotCounter({1: [5, 6, 9, 11], 2: [3], 3: [2], 8: [1]})
    x.__pivot__ = PivotCounter
    assert x.pivot() + x.pivot() == PivotCounter(
            {10: [' '], 12: ['e'], 18: ['s'], 22: ['t'],
              2: ['?', 'a', 'c', 'g', 'k', 'o', 'r', 'w'],
              4: ['h', 'n', 'y'], 6: ['!', 'i']})
    lol = AdvancedCounter("lollofant!!")
    troll = AdvancedCounter("trollofant")
    assert lol.pivot() - troll.pivot() == PivotCounter({1: ['l'], 2: ['!']})
    assert lol.pivot() + troll.pivot() == PivotCounter({1: ['r'], 2: ['!', 'a', 'f', 'n'], 3: ['t'], 4: ['o'], 5: ['l']})

def test_transpose():
    x = AdvancedCounter("yay? nice!! this thing works!")
    x.update("etsttseststttsetsetse ")
    tp_chain = [
        AdvancedCounter({1: 1}),
        AdvancedCounter({2: 1}),
        AdvancedCounter({1: 2}),
        AdvancedCounter({1: 1, 3: 1}),
        AdvancedCounter({1: 3, 4: 1}),
        AdvancedCounter({1: 4, 2: 1, 3: 1, 8: 1}),
        AdvancedCounter({11: 1, 1: 8, 2: 3, 3: 2, 5: 1, 6: 1, 9: 1}),
        AdvancedCounter({' ': 5, '!': 3, '?': 1, 'a': 1, 'c': 1, 'e': 6, 'g': 1, 'h': 2, 'i': 3, 'k': 1, 'n': 2, 'o': 1, 'r': 1, 's': 9, 't': 11, 'w': 1, 'y': 2}),
    ]
    old_x = None
    while old_x != x:
        old_x = x
        x = x.transpose()
        assert old_x == tp_chain.pop()

def test_fromkeys():
    assert AdvancedCounter.fromkeys('bumm') == AdvancedCounter({'b': 0, 'm': 0, 'u': 0})
    x = AdvancedCounter.fromkeys('bumm', 50)
    assert x == AdvancedCounter({'b': 50, 'm': 50, 'u': 50})
    assert x + x == AdvancedCounter({'b': 100, 'm': 100, 'u': 100})
    assert x + x == AdvancedCounter.fromkeys(x, 50+50)

def test___repr__():
    assert AdvancedCounter('bumm') == AdvancedCounter({'b': 1, 'm': 2, 'u': 1})
    assert AdvancedCounter({'b': 1, 'm': 2, 'u': 1}) == AdvancedCounter({'b': 1, 'm': 2, 'u': 1})
    for stuff in ('abc', 'bcccnnno', (12,12,3,4,5,3,3)):
        x = AdvancedCounter(stuff)
        assert x == eval(repr(x))

if __name__ == '__main__':
    import pytest
    pytest.main()

import pytest

from countlib import ExtremeCounter
from collections import Counter
from pivot import PivotCounter

def test_class():
    assert ExtremeCounter('zyzygy') == ExtremeCounter({'g': 1, 'y': 3, 'z': 2})
    y = ExtremeCounter("yay.")
    assert y + ExtremeCounter.fromkeys('zab.', 3) == ExtremeCounter({'.': 4, 'a': 4, 'b': 3, 'y': 2, 'z': 3})
    assert y - ExtremeCounter.fromkeys('zab.', 3) == ExtremeCounter({'y': 2})
    y.subtract(ExtremeCounter.fromkeys('zab.', 3))
    assert y == ExtremeCounter({'.': -2, 'a': -2, 'b': -3, 'y': 2, 'z': -3})
    y.add(ExtremeCounter.fromkeys('zab.', 3))
    assert y == ExtremeCounter({'.': 1, 'a': 1, 'b': 0, 'y': 2, 'z': 0})
    assert y + Counter() == ExtremeCounter({'.': 1, 'a': 1, 'y': 2})
    assert y.pivot() == PivotCounter({0: ['b', 'z'], 1: ['.', 'a'], 2: ['y']})
    assert y.transpose() == ExtremeCounter({0: 2, 1: 2, 2: 1})

def test_most_common():
    p = ExtremeCounter('abracadabra!')
    assert p.most_common(3) == [('a', 5), ('b', 2), ('r', 2)]
    assert p.most_common(2, inverse=True) == [('!', 1), ('c', 1)]
    assert p.most_common(2, count_func=lambda i: -i[1]) == [('!', 1), ('c', 1)]
    assert p.most_common(2, count_func=lambda i: -i[1], inverse=True) == [('a', 5), ('b', 2)]

def test_most_common_counts():
    x = ExtremeCounter("yay? nice!! this thing works!")
    x.update("etsttseststttsetsetse ")
    assert x.most_common_counts(1) == [('t', 11)]
    assert x.most_common_counts(5) == [('t', 11), ('s', 9), ('e', 6), (' ', 5), ('i', 3), ('!', 3)]

def test_pivot():
    x = ExtremeCounter("yay? nice!! this thing works!")
    x.update("etsttseststttsetsetse ")
    assert x.transpose().pivot(PivotCounter) == PivotCounter({1: [5, 6, 9, 11], 2: [3], 3: [2], 8: [1]})
    x.__pivot__ = PivotCounter
    assert x.pivot() + x.pivot() == PivotCounter(
            {10: [' '], 12: ['e'], 18: ['s'], 22: ['t'],
              2: ['?', 'a', 'c', 'g', 'k', 'o', 'r', 'w'],
              4: ['h', 'n', 'y'], 6: ['!', 'i']})
    lol = ExtremeCounter("lollofant!!")
    troll = ExtremeCounter("trollofant")
    assert lol.pivot() - troll.pivot() == PivotCounter({1: ['l'], 2: ['!']})
    assert lol.pivot() + troll.pivot() == PivotCounter({1: ['r'], 2: ['!', 'a', 'f', 'n'], 3: ['t'], 4: ['o'], 5: ['l']})

def test_transpose():
    x = ExtremeCounter("yay? nice!! this thing works!")
    x.update("etsttseststttsetsetse ")
    tp_chain = [
        ExtremeCounter({1: 1}),
        ExtremeCounter({2: 1}),
        ExtremeCounter({1: 2}),
        ExtremeCounter({1: 1, 3: 1}),
        ExtremeCounter({1: 3, 4: 1}),
        ExtremeCounter({1: 4, 2: 1, 3: 1, 8: 1}),
        ExtremeCounter({11: 1, 1: 8, 2: 3, 3: 2, 5: 1, 6: 1, 9: 1}),
        ExtremeCounter({' ': 5, '!': 3, '?': 1, 'a': 1, 'c': 1, 'e': 6, 'g': 1, 'h': 2, 'i': 3, 'k': 1, 'n': 2, 'o': 1, 'r': 1, 's': 9, 't': 11, 'w': 1, 'y': 2}),
    ]
    old_x = None
    while old_x != x:
        old_x = x
        x = x.transpose()
        assert old_x == tp_chain.pop()

def test_fromkeys():
    assert ExtremeCounter.fromkeys('bumm') == ExtremeCounter({'b': 0, 'm': 0, 'u': 0})
    x = ExtremeCounter.fromkeys('bumm', 50)
    assert x == ExtremeCounter({'b': 50, 'm': 50, 'u': 50})
    assert x + x == ExtremeCounter({'b': 100, 'm': 100, 'u': 100})
    assert x + x == ExtremeCounter.fromkeys(x, 50+50)

def test___repr__():
    assert ExtremeCounter('bumm') == ExtremeCounter({'b': 1, 'm': 2, 'u': 1})
    assert ExtremeCounter({'b': 1, 'm': 2, 'u': 1}) == ExtremeCounter({'b': 1, 'm': 2, 'u': 1})
    for stuff in ('abc', 'bcccnnno', (12,12,3,4,5,3,3)):
        x = ExtremeCounter(stuff)
        assert x == eval(repr(x))

def test___add__():
    assert ExtremeCounter('abbb') + ExtremeCounter('bcc') == ExtremeCounter({'a': 1, 'b': 4, 'c': 2})
    assert ExtremeCounter('abbb') + Counter('bcc') == ExtremeCounter({'a': 1, 'b': 4, 'c': 2})
    assert ExtremeCounter('aaa') + ExtremeCounter.fromkeys('a', -1) == ExtremeCounter({'a': 2})
    assert ExtremeCounter('aaa') + ExtremeCounter.fromkeys('a', -3) == ExtremeCounter()

def test___sub__():
    assert ExtremeCounter('abbbc') - ExtremeCounter('bccd') == ExtremeCounter({'a': 1, 'b': 2})
    assert ExtremeCounter('abbbc') - Counter('bccd') == ExtremeCounter({'a': 1, 'b': 2})

def test_add():
    a = ExtremeCounter('abbb')
    assert a == ExtremeCounter({'a': 1, 'b': 3})
    a.add(ExtremeCounter('bcc'))
    assert a == ExtremeCounter({'a': 1, 'b': 4, 'c': 2})
    assert a + ExtremeCounter.fromkeys('ab', -12) == ExtremeCounter({'c': 2})
    a.add(ExtremeCounter.fromkeys('ab', -12))
    assert a == ExtremeCounter({'a': -11, 'b': -8, 'c': 2})
    a.add(a)
    a.subtract(a)
    assert a == ExtremeCounter({'a': 0, 'b': 0, 'c': 0})

def test___or__():
    assert ExtremeCounter('abbb') | ExtremeCounter('bcc') == ExtremeCounter({'a': 1, 'b': 3, 'c': 2})
    assert ExtremeCounter('abbb') | Counter('bcc') == ExtremeCounter({'a': 1, 'b': 3, 'c': 2})

def test___and__():
    assert ExtremeCounter('abbb') & ExtremeCounter('bcc') == ExtremeCounter({'b': 1})
    assert ExtremeCounter('abbb') & Counter('bcc') == ExtremeCounter({'b': 1})
    assert Counter('abbb') & ExtremeCounter('bcc') == Counter({'b': 1})

if __name__ == '__main__':
    import pytest
    pytest.main()

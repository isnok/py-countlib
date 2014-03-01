import pytest

from countlib import PivotCounter
from countlib import CoolPivotCounter

from collections import Counter

def test_class():
    assert CoolPivotCounter('zyzygy') == CoolPivotCounter({1: ['g'], 2: ['z'], 3: ['y']})
    assert CoolPivotCounter(Counter('zyzygy')) == CoolPivotCounter({1: ['g'], 2: ['z'], 3: ['y']})
    assert CoolPivotCounter('lalalohoe') == CoolPivotCounter(Counter('lalalohoe'))
    assert CoolPivotCounter('lllaaoohe') == CoolPivotCounter('lalalohoe')
    assert not CoolPivotCounter('lllaaoohe') == CoolPivotCounter(frozenset('lalalohoe'))


def test_init():
    # a new, empty counter
    assert not CoolPivotCounter()
    assert CoolPivotCounter() == {}

    # a new counter from an iterable
    assert CoolPivotCounter('gallahad') == CoolPivotCounter({1: ['d', 'g', 'h'], 2: ['l'], 3: ['a']})

    # a new counter from a mapping
    assert CoolPivotCounter({'a': 4, 'b': 2}) == CoolPivotCounter({2: ['b'], 4: ['a']})

    # a new counter from keyword args
    assert CoolPivotCounter(a=4, b=2) == CoolPivotCounter({2: ['b'], 4: ['a']})

def test_missing():
    assert CoolPivotCounter()["x"] == frozenset([])

def test_most_common():
    p = CoolPivotCounter('abracadabra!')
    assert p.most_common(3) == [(1, frozenset(['!', 'c', 'd'])), (2, frozenset(['r', 'b'])), (5, frozenset(['a']))]
    assert p.most_common(2, reverse=True) == [(5, frozenset(['a'])), (2, frozenset(['r', 'b']))]
    assert p.most_common(2, count_func=lambda i: -len(i[1])) == [(5, frozenset(['a'])), (2, frozenset(['r', 'b']))]
    assert p.most_common(2, count_func=lambda i: -len(i[1]), reverse=True) == [(1, frozenset(['!', 'c', 'd'])), (2, frozenset(['r', 'b']))]

def test_elements():
    c = CoolPivotCounter('ABCABC')
    assert str(sorted(c.elements())) == "['A', 'A', 'B', 'B', 'C', 'C']"

def test_unpivot():
    assert CoolPivotCounter('ABCABC').unpivot() == Counter({'A': 2, 'C': 2, 'B': 2})
    assert Counter("lollofant") == CoolPivotCounter("lollofant").unpivot()
    fant = CoolPivotCounter("lollofant")
    assert fant.unpivot(clean=True) == fant.unpivot(check=True)
    for x in xrange(5, 99):
        fant[x] = set(['B'])
    assert not fant.unpivot(clean=True) == fant.unpivot(check=True) # may statisically fail ~5% of the time

def test_unpivot_items():
    c = CoolPivotCounter('ABCABC')
    assert sorted(c.unpivot_items()) == [('A', 2), ('B', 2), ('C', 2)]
    assert sorted(c.unpivot_items()) == sorted(Counter('ABCABC').items())

def test_count_sets():
    p = CoolPivotCounter('ABCABC')
    assert p.count_sets() == Counter({2: 3})
    assert p.count_sets(count_func=lambda s: 20 - len(s)) == Counter({2: 17})

def test_fromkeys():
    assert CoolPivotCounter.fromkeys('watch') == CoolPivotCounter({'a': [], 'c': [], 'h': [], 't': [], 'w': []})
    assert CoolPivotCounter.fromkeys('watchhhh') == CoolPivotCounter({'a': [], 'c': [], 'h': [], 't': [], 'w': []})
    assert CoolPivotCounter.fromkeys('not supplying a v_func means nothing.').unpivot() == Counter()
    assert CoolPivotCounter.fromkeys([1,2,3], lambda n: frozenset(range(n))) == CoolPivotCounter({1: [0], 2: [0, 1], 3: [0, 1, 2]})

def test_update():
    d = CoolPivotCounter('watch')
    d.update('boofittii')          # add in elements via another counter-like
    assert d == CoolPivotCounter({1: ['a', 'b', 'c', 'f', 'h', 't', 'w'], 2: ['o', 't'], 3: ['i']})
    assert CoolPivotCounter(d.unpivot()) == CoolPivotCounter({1: ['a', 'b', 'c', 'f', 'h', 'w'], 2: ['o'], 3: ['i', 't']})

    c = CoolPivotCounter('which')
    c.update(CoolPivotCounter('boof')) # update the dict way
    assert c == CoolPivotCounter({1: ['b', 'f'], 2: ['o']})

def test_delitem():
    c = CoolPivotCounter('which')
    del c[2]
    assert c == CoolPivotCounter({1: ['c', 'i', 'w']})
    del c["not there"]

def test_copy():
    c = CoolPivotCounter('which')
    d = c.copy()
    del c[2]
    assert c, d == (CoolPivotCounter({1: ['c', 'i', 'w']}), CoolPivotCounter({1: ['c', 'i', 'w'], 2: ['h']}))

    try:
        d[1].discard('c')
        assert False
    except AttributeError:
        assert True

    assert c, d == (CoolPivotCounter({1: ['c', 'i', 'w']}), CoolPivotCounter({1: ['c', 'i', 'w'], 2: ['h']}))
    assert not c == d

def test_repr():
    assert CoolPivotCounter('bumm') == CoolPivotCounter({1: ['b', 'u'], 2: ['m']})
    assert eval("CoolPivotCounter({1: ['b', 'u'], 2: ['m']})") == CoolPivotCounter({1: ['b', 'u'], 2: ['m']})

def test__add_():
    assert CoolPivotCounter('abbb') + CoolPivotCounter('bcc') == CoolPivotCounter({1: ['a'], 2: ['c'], 4: ['b']})
    assert CoolPivotCounter(Counter('abbb') + Counter('bcc')) == CoolPivotCounter({1: ['a'], 2: ['c'], 4: ['b']})

def test__sub_():
    assert CoolPivotCounter('abbbc') - CoolPivotCounter('bccd') == CoolPivotCounter({1: ['a'], 2: ['b']})
    assert CoolPivotCounter(Counter('abbbc') - Counter('bccd')) == CoolPivotCounter({1: ['a'], 2: ['b']})

def test__or_():
    assert CoolPivotCounter('abbb') | CoolPivotCounter('bcc') == CoolPivotCounter({1: ['a', 'b'], 2: ['c'], 3: ['b']})

def test__and_():
    assert CoolPivotCounter('hello') & CoolPivotCounter('hallo') == CoolPivotCounter({1: ['h', 'o'], 2: ['l']})
    assert CoolPivotCounter('abbb') & CoolPivotCounter('bcc') == CoolPivotCounter()

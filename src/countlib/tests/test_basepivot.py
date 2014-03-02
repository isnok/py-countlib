import pytest
import random
import string

from countlib import PivotCounter
from countlib import CoolPivotCounter

from collections import Counter

def test_mutation(TestPivotCounter, other_pivots):
    t = TestPivotCounter("floosh!!!")
    for cls in other_pivots:
        x = cls(t)
        assert not x.__class__ == t.__class__
        assert x == t
        assert x + t
        assert not x - t
        assert x.add(t)
        assert x.subtract(t)
        assert x | t
        assert x & t

        assert x.pop(1)
        assert x + t
        assert not x - t
        assert t - x
        assert x.add(t)
        assert x.subtract(t)
        assert x | t
        assert x & t

def test_bool(TestPivotCounter):
    assert TestPivotCounter
    assert not TestPivotCounter()
    assert TestPivotCounter("something")

def test_class(TestPivotCounter):
    assert TestPivotCounter('zyzygy') == TestPivotCounter({1: ['g'], 2: ['z'], 3: ['y']})
    assert TestPivotCounter(Counter('zyzygy')) == TestPivotCounter({1: ['g'], 2: ['z'], 3: ['y']})
    assert TestPivotCounter('lalalohoe') == TestPivotCounter(Counter('lalalohoe'))
    assert TestPivotCounter('lllaaoohe') == TestPivotCounter('lalalohoe')
    assert not TestPivotCounter('lllaaoohe') == TestPivotCounter(frozenset('lalalohoe'))


def test_init_empty(TestPivotCounter):
    assert not TestPivotCounter()
    assert TestPivotCounter() == {}

def test_init_iterable(TestPivotCounter):
    assert TestPivotCounter('gallahad') == TestPivotCounter({1: ['d', 'g', 'h'], 2: ['l'], 3: ['a']})

def test_init_mapping(TestPivotCounter):
    assert TestPivotCounter({'a': 4, 'b': 2}) == TestPivotCounter({2: ['b'], 4: ['a']})

def test_init_kwd(TestPivotCounter):
    assert TestPivotCounter(a=4, b=2) == TestPivotCounter({2: ['b'], 4: ['a']})

def test_fromkeys(TestPivotCounter):
    assert TestPivotCounter.fromkeys('watch') == TestPivotCounter({'a': [], 'c': [], 'h': [], 't': [], 'w': []})
    assert TestPivotCounter.fromkeys('watchhhh') == TestPivotCounter({'a': [], 'c': [], 'h': [], 't': [], 'w': []})
    assert TestPivotCounter.fromkeys('not supplying a v_func means nothing.').unpivot() == Counter()
    assert TestPivotCounter.fromkeys([1,2,3], lambda n: frozenset(range(n))) == TestPivotCounter({1: [0], 2: [0, 1], 3: [0, 1, 2]})

def test_repr(TestPivotCounter):
    assert TestPivotCounter('bumm') == TestPivotCounter({1: ['b', 'u'], 2: ['m']})
    assert eval("TestPivotCounter({1: ['b', 'u'], 2: ['m']})") == TestPivotCounter({1: ['b', 'u'], 2: ['m']})
    t = TestPivotCounter()
    for r in range(random.randint(5,25)):
        cnt = random.randint(-10, 100)
        rnd = "".join(random.sample(string.letters, random.randint(1,5)))
        t[cnt] = t[cnt].union(rnd)
        assert eval(repr(t)) == t

def test_delitem(TestPivotCounter):
    c = TestPivotCounter('which')
    del c[2]
    assert c == TestPivotCounter({1: ['c', 'i', 'w']})
    del c["not there"]


def test_most_common(TestPivotCounter):
    p = TestPivotCounter('abracadabra!')
    assert p.most_common(3) == [(1, frozenset(['!', 'c', 'd'])), (2, frozenset(['r', 'b'])), (5, frozenset(['a']))]
    assert p.most_common(2, reverse=True) == [(5, frozenset(['a'])), (2, frozenset(['r', 'b']))]
    assert p.most_common(2, count_func=lambda i: -len(i[1])) == [(5, frozenset(['a'])), (2, frozenset(['r', 'b']))]
    assert p.most_common(2, count_func=lambda i: -len(i[1]), reverse=True) == [(1, frozenset(['!', 'c', 'd'])), (2, frozenset(['r', 'b']))]

def test_elements(TestPivotCounter, TestCounter):
    c = TestPivotCounter('ABCABC')
    assert str(sorted(c.elements())) == "['A', 'A', 'B', 'B', 'C', 'C']"
    d = TestPivotCounter(TestCounter.fromkeys("hejo, test", 0))
    assert list(d.elements()) == []
    d = TestPivotCounter(TestCounter.fromkeys("hejo, test", -100))
    assert not set(d.elements())

def test_iter_dirty(TestPivotCounter):
    assert [] == list(TestPivotCounter('ABCABC').iter_dirty())
    a = TestPivotCounter('aa')
    a.update(TestPivotCounter('a'))
    assert list(a.iter_dirty()) == [set(['a'])]

def test_is_clean(TestPivotCounter):
    assert TestPivotCounter(range(3)).is_clean()
    a = TestPivotCounter('aa')
    a.update(TestPivotCounter('a'))
    assert not a.is_clean()

def test_unpivot(TestPivotCounter):
    assert TestPivotCounter('ABCABC').unpivot() == Counter({'A': 2, 'C': 2, 'B': 2})
    assert Counter("lollofant") == TestPivotCounter("lollofant").unpivot()
    fant = TestPivotCounter("lollofant")
    assert fant.unpivot(clean=True) == fant.unpivot(check=True)
    for x in xrange(5, 99):
        fant[x] = set(['B'])
    assert not fant.unpivot(clean=True) == fant.unpivot(check=True) # may statisically fail ~5% of the time

def test_unpivot_items(TestPivotCounter):
    c = TestPivotCounter('ABCABC')
    assert sorted(c.unpivot_items()) == [('A', 2), ('B', 2), ('C', 2)]
    assert sorted(c.unpivot_items()) == sorted(Counter('ABCABC').items())

def test_count_sets(TestPivotCounter):
    p = TestPivotCounter('ABCABC')
    assert p.count_sets() == Counter({2: 3})
    assert p.count_sets(count_func=lambda s: 20 - len(s)) == Counter({2: 17})

def test___neg__(TestPivotCounter, TestSet):
    neg = -TestPivotCounter.fromkeys([-1,0,1,2], lambda c: TestSet([c]))
    assert neg[2] == TestSet()
    assert neg[1] == TestSet([-1])
    assert neg[0] == TestSet([0])
    assert neg[-1] == TestSet([1])
    assert neg[-2] == TestSet([2])

def test___add__(TestPivotCounter):
    assert TestPivotCounter('abbb') + TestPivotCounter('bcc') == TestPivotCounter({1: ['a'], 2: ['c'], 4: ['b']})
    assert TestPivotCounter(Counter('abbb') + Counter('bcc')) == TestPivotCounter({1: ['a'], 2: ['c'], 4: ['b']})

def test___sub__(TestPivotCounter):
    assert TestPivotCounter('abbbc') - TestPivotCounter('bccd') == TestPivotCounter({1: ['a'], 2: ['b']})
    assert TestPivotCounter(Counter('abbbc') - Counter('bccd')) == TestPivotCounter({1: ['a'], 2: ['b']})

def test_add(TestPivotCounter):
    a, b = TestPivotCounter('abbbc'), TestPivotCounter('bccd')
    assert a.subtract(b) == TestPivotCounter({-1: ['c', 'd'], 1: ['a'], 2: ['b']})
    assert a.subtract(b).add("xxx") == NotImplemented
    assert a.subtract(b).add(TestPivotCounter("xxx")) == TestPivotCounter({1: ['a'], 2: ['b'], 3: ['x']})

def test_subtract(TestPivotCounter):
    assert TestPivotCounter('test').subtract(Counter('tst')) == NotImplemented
    assert TestPivotCounter('test').subtract(TestPivotCounter('tst')) == TestPivotCounter({0: ['s', 't'], 1: ['e']})

    assert PivotCounter('abbbc').subtract(PivotCounter('bccd')) == PivotCounter({-1: ['c', 'd'], 1: ['a'], 2: ['b']})

def test___or__(TestPivotCounter):
    assert TestPivotCounter('abbb') | TestPivotCounter('bcc') == TestPivotCounter({1: ['a', 'b'], 2: ['c'], 3: ['b']})

def test___and__(TestPivotCounter):
    assert TestPivotCounter('hello') & TestPivotCounter('hallo') == TestPivotCounter({1: ['h', 'o'], 2: ['l']})
    assert TestPivotCounter('abbb') & TestPivotCounter('bcc') == TestPivotCounter()

if __name__ == '__main__':
    import pytest
    pytest.main()

import pytest

from pivot import PivotCounter
from pivot import CoolPivotCounter
from collections import Counter

def test_mutable_class():
    assert isinstance(PivotCounter('abbb')[1], set)
    assert not isinstance(PivotCounter('abbb')[1], frozenset)
    assert isinstance(PivotCounter('abbb')[10], set)
    assert not isinstance(PivotCounter('abbb')[10], frozenset)

def test_mutable_update():
    d = PivotCounter('watch')
    d.update('boofittii')                 # add in elements via another counter-like
    assert d                              #                 v------- o_O -------v
    assert d == PivotCounter({1: ['a', 'b', 'c', 'f', 'h', 't', 'w'], 2: ['o', 't'], 3: ['i']})
    assert PivotCounter(d.unpivot())      # to fix it regenerate the PivotCounter ==
    assert PivotCounter(d.unpivot()) == PivotCounter({1: ['a', 'b', 'c', 'f', 'h', 'w'], 2: ['o'], 3: ['i', 't']})
    c = PivotCounter('which')
    c.update(PivotCounter('boof'))        # update the dict way
    assert c == PivotCounter({1: ['b', 'f'], 2: ['o']})

def test_mutable_missing():
    c = PivotCounter()
    assert not "x" in c
    assert not len(c["x"])
    assert "x" in c
    assert isinstance(c["x"], set)

def test_mutable_copy():
    c = PivotCounter('which')
    d = c.copy()
    assert d == c
    assert not c is d
    d[2].discard('h')
    assert not c == d
    e = c.copy()
    assert e == c
    assert not e is c and not e is d
    del e[2]
    assert not e == c
    assert not e == d
    assert e == d + PivotCounter()

###### CoolPivot tests ######

def test_frozen_class():
    assert not isinstance(CoolPivotCounter('abbb')[1], set)
    assert isinstance(CoolPivotCounter('abbb')[1], frozenset)
    assert not isinstance(CoolPivotCounter('abbb')[10], set)
    assert isinstance(CoolPivotCounter('abbb')[10], frozenset)

def test_frozen_values():
    d = CoolPivotCounter("bamm")
    try:
        d[1].discard('c')
        assert False
    except AttributeError:
        assert True

def test_frozen_update():
    d = CoolPivotCounter('watch')
    d.update('boofittii')
    assert d == CoolPivotCounter({1: ['a', 'b', 'c', 'f', 'h', 't', 'w'], 2: ['o', 't'], 3: ['i']})
    assert CoolPivotCounter(d.unpivot()) == CoolPivotCounter({1: ['a', 'b', 'c', 'f', 'h', 'w'], 2: ['o'], 3: ['i', 't']})

    c = CoolPivotCounter('which')
    c.update(CoolPivotCounter('boof'))
    assert c == CoolPivotCounter({1: ['b', 'f'], 2: ['o']})

def test_frozen_missing():
    c = CoolPivotCounter()
    assert not "x" in c
    assert not len(c["x"])
    assert not "x" in c
    assert isinstance(c["x"], frozenset)

def test_frozen_copy():
    c = CoolPivotCounter('which')
    d = c.copy()
    assert c == d
    assert not c is d
    del c[2]
    assert c != d
    assert c, d == (
        CoolPivotCounter({1: ['c', 'i', 'w']}),
        CoolPivotCounter({1: ['c', 'i', 'w'], 2: ['h']})
    )

if __name__ == '__main__':
    import doctest
    print doctest.testmod()

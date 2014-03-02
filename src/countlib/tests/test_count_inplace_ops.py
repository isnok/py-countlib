import pytest

from collections import Counter

def test_add(TestCounter, cnt_ab2):
    a = TestCounter('abbb')
    assert a == TestCounter({'a': 1, 'b': 3})
    a.add(TestCounter('bcc'))
    assert a == TestCounter({'a': 1, 'b': 4, 'c': 2})
    assert a + TestCounter.fromkeys('ab', -12) == TestCounter({'c': 2})
    a.add(TestCounter.fromkeys('ab', -12))
    assert a == TestCounter({'a': -11, 'b': -8, 'c': 2})
    a.add(a)
    a.subtract(a)
    assert a == TestCounter({'a': 0, 'b': 0, 'c': 0})
    a.add(a=-10)
    assert a["a"] == -10
    cnt_abc = TestCounter("abc")
    cnt_abm = cnt_ab2.copy()
    cnt_abm.add(cnt_abc)
    assert "d" not in cnt_abc
    cnt_abm.subtract(TestCounter("abc"))
    assert "d" not in cnt_abc


def test_subtract(TestCounter):
    c = TestCounter('which')
    c.subtract('witch')             # subtract elements from another iterable
    c.subtract(Counter('watch'))    # subtract elements from another counter
    assert c['h'] == 0              # 2 in which, minus 1 in witch, minus 1 in watch
    assert c['w'] == -1             # 1 in which, minus 1 in witch, minus 1 in watch
    c.subtract(w=-6)
    assert c['w'] == 5

def test__iadd__(cnt_abc):
    cnt_inp = cnt_abc.copy()
    cnt_inp += 2
    assert cnt_inp == Counter("abc" * 3)

def test__isub__(cnt_abc):
    cnt_inp = cnt_abc.copy()
    assert cnt_inp
    cnt_inp -= 2
    assert cnt_inp
    assert not +cnt_inp

def test__imul__(cnt_abc):
    cnt_inp = cnt_abc.copy()
    cnt_inp *= 4
    assert cnt_inp == Counter("abc" * 4)

def test__idiv__(TestCounter, cnt_abc):
    cnt_inp = cnt_abc.copy()
    cnt_inp /= 2
    for c in "acb":
        assert cnt_inp[c] == 0
    cnt_inp += 3
    cnt_inp /= 2
    for c in "acb":
        assert cnt_inp[c] == 1
    assert cnt_inp == TestCounter("abc")

def test__irshift__(TestCounter, cnt_abc):
    cnt_inp = cnt_abc.copy()
    cnt_inp >>= 2
    assert cnt_inp == (TestCounter("abc") * 0)

def test__ilshift__(TestCounter, cnt_abc):
    cnt_inp = cnt_abc.copy()
    cnt_inp <<= 2
    assert cnt_inp == TestCounter("abc") * 4

def test__imod__(cnt_ab2):
    cnt_ab2 = cnt_ab2.copy()
    t = 1 % cnt_ab2
    assert t
    assert set(t.values()) == set([0,1])
    assert Counter("abcabc") % +(Counter("abcabc") % cnt_ab2)

def test__ipow__(cnt_ab2):
    cnt_ab2 = cnt_ab2.copy()
    tmp = cnt_ab2.copy()
    cnt_ab2 **= 3
    assert cnt_ab2
    tmp **= 2
    assert tmp
    for i in tmp:
        assert tmp[i] <= cnt_ab2[i]

def test___ior__(cnt_ab2, cnt_abc):
    cnt_inp = cnt_abc.copy()
    tmp = cnt_inp.copy()
    cnt_inp |= cnt_ab2
    assert cnt_inp != tmp
    tmp = cnt_ab2.copy()
    cnt_ab2 |= cnt_inp * 3
    assert cnt_ab2 != tmp

def test___iand__(cnt_ab2, cnt_abc):
    cnt_inp = cnt_abc.copy()
    tmp = cnt_ab2.copy()
    tmp &= cnt_inp
    assert cnt_ab2 != tmp
    tmp = cnt_inp.copy()
    assert (cnt_ab2 - 2)["a"] == -2
    tmp &= (cnt_ab2 - 2)
    assert tmp != cnt_inp

def test___ixor__(cnt_abc):
    cnt_inp = cnt_abc.copy()
    tmp = cnt_inp.copy()
    cnt_inp ^= 1
    assert not tmp == cnt_inp
    assert cnt_inp
    assert not +cnt_inp


import pytest

from collections import Counter

def test_add(TestCounter, cnt_abc, cnt_ab2):
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
    cnt_ab2.add(cnt_abc)
    assert "d" not in cnt_abc


def test_subtract(TestCounter):
    c = TestCounter('which')
    c.subtract('witch')             # subtract elements from another iterable
    c.subtract(Counter('watch'))    # subtract elements from another counter
    assert c['h'] == 0              # 2 in which, minus 1 in witch, minus 1 in watch
    assert c['w'] == -1             # 1 in which, minus 1 in witch, minus 1 in watch
    c.subtract(w=-6)
    assert c['w'] == 5


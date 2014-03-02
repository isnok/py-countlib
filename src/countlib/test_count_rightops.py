import pytest

from collections import Counter

def test__radd__(cnt_abc):
    assert 2 + cnt_abc == Counter("abcabc") + cnt_abc

def test__rsub__(cnt_abc):
    assert 2 - cnt_abc == Counter("aabbcc") - (Counter("abcabc") - cnt_abc)

def test__rmul__(cnt_abc):
    assert 4 * cnt_abc == Counter("abcabc") * (Counter("abcabc") * cnt_abc)

def test__rdiv__(cnt_abc):
    assert 1 / cnt_abc == Counter("abcabc") / (Counter("abcabc") / cnt_abc)

def test__rrshift__(cnt_abc):
    assert 2 >> cnt_abc == cnt_abc
    assert Counter("abc") >> cnt_abc == {}

def test__rlshift__(cnt_abc):
    assert 1 << cnt_abc == cnt_abc + cnt_abc
    assert Counter("abc") << cnt_abc == 2 * cnt_abc

def test__rmod__(cnt_ab2):
    t = 1 % cnt_ab2
    assert t
    assert set(t.values()) == set([0,1])
    assert Counter("abcabc") % +(Counter("abcabc") % cnt_ab2)

def test__rpow__(cnt_abc):
    assert 2 ** 2 ** cnt_abc == Counter("abcabc") ** (Counter("abcabc") ** cnt_abc)

def test___ror__(TestCounter):
    assert Counter('bcc') | TestCounter('abbb') == TestCounter({'a': 1, 'b': 3, 'c': 2})
    assert 4 | TestCounter('a') == TestCounter("aaaa")

def test___rand__(TestCounter):
    assert Counter('abbb') & TestCounter('bcc') == Counter({'b': 1})
    assert 4 & TestCounter("aa") == dict(a=2)

def test___rxor__(TestCounter):
    assert Counter('cabc') ^ TestCounter('abbbcc') == Counter({'b': 2})
    assert 1 ^ TestCounter('abbbcc') == TestCounter({'a': 0, 'b': 2, 'c': 3})


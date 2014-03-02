import pytest

from countlib import AdvancedCounter
from countlib import ExtremeCounter
from collections import Counter

base_implementations = (AdvancedCounter, ExtremeCounter)

def test__radd__(cnt_abc):
    assert 2 + cnt_abc == Counter("abcabc") + cnt_abc

def test_value_magic(cnt_abc, cnt_ab2):
    assert (cnt_abc * "l" + "o" + "l")["b"] == "lol"

def test___add__(TestCounter):
    assert TestCounter('abbb') + TestCounter('bcc') == TestCounter({'a': 1, 'b': 4, 'c': 2})
    assert TestCounter('abbb') + Counter('bcc') == TestCounter({'a': 1, 'b': 4, 'c': 2})
    assert TestCounter('aaa') + TestCounter.fromkeys('a', -1) == TestCounter({'a': 2})
    assert TestCounter('aaa') + TestCounter.fromkeys('a', -3) == TestCounter()

def test___sub__(TestCounter):
    assert TestCounter('abbbc') - TestCounter('bccd') == TestCounter({'a': 1, 'b': 2})
    assert TestCounter('abbbc') - Counter('bccd') == TestCounter({'a': 1, 'b': 2})

def test__rsub__(cnt_abc):
    assert 2 - cnt_abc == Counter("aabbcc") - (Counter("abcabc") - cnt_abc)

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

def test___mul__(cnt_abc, cnt_ab2):
    d = (cnt_abc * 2) * cnt_ab2
    assert d
    assert d["a"] == 4
    assert d["g"] == 0
    assert set(d.keys()) == set("abc")

def test__rmul__(cnt_abc):
    assert 4 * cnt_abc == Counter("abcabc") * (Counter("abcabc") * cnt_abc)

def test___div__(cnt_abc, cnt_ab2):
    d = cnt_abc / cnt_ab2
    assert not d
    assert d["a"] == 0
    assert not d + 1
    e = cnt_ab2 / cnt_abc
    assert e
    assert e["a"] == 2
    assert "f" not in e
    assert e + 0

def test__rdiv__(cnt_abc):
    assert 1 / cnt_abc == Counter("abcabc") / (Counter("abcabc") / cnt_abc)

def test___floordiv__(cnt_abc, cnt_ab2):
    d = cnt_abc // cnt_ab2
    assert not d
    assert d["a"] == 0
    assert not d + 1
    e = cnt_ab2 // cnt_abc
    assert e
    assert e["a"] == 2
    assert "f" not in e
    assert e + 0

def test___truediv__(cnt_abc, cnt_ab2):
    d = cnt_abc.__truediv__(cnt_ab2)
    assert d
    assert not +(d - 1)
    assert d["a"] > 0
    assert d + 1
    e = cnt_ab2.__truediv__(cnt_abc)
    assert e
    assert e["a"] == 2
    assert "f" not in e
    assert e + 0

def test___invert__(cnt_abc, cnt_ab2):
    d = ~cnt_abc
    assert d
    assert not +d
    e = ~cnt_ab2
    assert e
    assert not +e
    assert +e["b"] == -4

def test___rshift__(cnt_abc, cnt_ab2):
    d = (cnt_abc>>1)
    assert d
    assert not +d
    e = cnt_ab2 >> 1
    assert e
    assert +e
    f = (cnt_abc+cnt_abc) >> cnt_abc
    assert f == cnt_abc
    assert (cnt_abc+cnt_abc)>>2 == cnt_abc * 0

def test__rrshift__(cnt_abc):
    assert 2 >> cnt_abc == cnt_abc
    assert Counter("abc") >> cnt_abc == {}

def test___lshift__(cnt_abc, cnt_ab2):
    d = (cnt_abc<<1)+cnt_abc
    assert d == cnt_abc * 3
    assert d << 4
    e = cnt_ab2 << 1
    assert e
    assert +e
    f = cnt_abc << cnt_abc
    assert f
    assert f == cnt_abc * 2
    assert not cnt_ab2 * 2 - (cnt_ab2 << cnt_ab2)

def test__rlshift__(cnt_abc):
    assert 1 << cnt_abc == cnt_abc + cnt_abc
    assert Counter("abc") << cnt_abc == 2 * cnt_abc

def test___mod__(cnt_abc, cnt_ab2):
    assert cnt_abc % cnt_ab2
    assert cnt_abc % cnt_ab2 == cnt_abc
    assert not (cnt_ab2 % cnt_abc) == cnt_abc
    assert (cnt_abc % cnt_ab2)["b"] == 1

def test__rmod__(cnt_ab2):
    t = 1 % cnt_ab2
    assert t
    assert set(t.values()) == set([0,1])
    assert Counter("abcabc") % +(Counter("abcabc") % cnt_ab2)

def test___pow__(cnt_abc, cnt_ab2):
    d = cnt_abc ** cnt_ab2
    assert d
    assert d == cnt_abc
    e = cnt_ab2 ** cnt_abc
    assert ( (e - 1 + Counter() + 1) ** (cnt_abc - 1) ) == cnt_abc

def test__rpow__(cnt_abc):
    assert 2 ** 2 ** cnt_abc == Counter("abcabc") ** (Counter("abcabc") ** cnt_abc)

def test___or__(TestCounter):
    assert TestCounter('abbb') | TestCounter('bcc') == TestCounter({'a': 1, 'b': 3, 'c': 2})
    assert TestCounter('abbb') | Counter('bcc') == TestCounter({'a': 1, 'b': 3, 'c': 2})

def test___ror__(TestCounter):
    assert Counter('bcc') | TestCounter('abbb') == TestCounter({'a': 1, 'b': 3, 'c': 2})
    assert 4 | TestCounter('a') == TestCounter("aaaa")

def test___and__(TestCounter):
    assert TestCounter('abbb') & TestCounter('bcc') == TestCounter({'b': 1})
    assert TestCounter('abbb') & Counter('bcc') == TestCounter({'b': 1})

def test___rand__(TestCounter):
    assert Counter('abbb') & TestCounter('bcc') == Counter({'b': 1})
    assert 4 & TestCounter("aa") == dict(a=2)

def test___xor__(TestCounter):
    lol = TestCounter('110abbbc') ^ TestCounter('bccdeeef')
    assert lol
    assert lol["0"] == 1
    assert lol["1"] == 2
    assert lol["b"] == 2
    assert lol["a"] == 1
    assert lol["f"] == 1
    assert lol["e"] == 3
    assert TestCounter('abbb') ^ Counter('bcc') == TestCounter('abbcc')
    assert TestCounter('abbbcc') ^ Counter('bcac') == Counter({'b': 2})

def test___rxor__(TestCounter):
    assert Counter('cabc') ^ TestCounter('abbbcc') == Counter({'b': 2})
    assert 1 ^ TestCounter('abbbcc') == TestCounter({'a': 0, 'b': 2, 'c': 3})

if __name__ == '__main__':
    import pytest
    pytest.main()

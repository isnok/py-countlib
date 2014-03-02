import pytest

from countlib import AdvancedCounter
from countlib import ExtremeCounter
from collections import Counter

base_implementations = (AdvancedCounter, ExtremeCounter)

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

def test___mul__(cnt_abc, cnt_ab2):
    d = (cnt_abc * 2) * cnt_ab2
    assert d
    assert d["a"] == 4
    assert d["g"] == 0
    assert set(d.keys()) == set("abc")

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

def test___mod__(cnt_abc, cnt_ab2):
    assert cnt_abc % cnt_ab2
    assert cnt_abc % cnt_ab2 == cnt_abc
    assert not (cnt_ab2 % cnt_abc) == cnt_abc
    assert (cnt_abc % cnt_ab2)["b"] == 1

def test___pow__(cnt_abc, cnt_ab2):
    d = cnt_abc ** cnt_ab2
    assert d
    assert d == cnt_abc
    e = cnt_ab2 ** cnt_abc
    assert e != cnt_ab2
    assert set(e) == set(cnt_ab2)

def test___or__(TestCounter):
    assert TestCounter('abbb') | TestCounter('bcc') == TestCounter({'a': 1, 'b': 3, 'c': 2})
    assert TestCounter('abbb') | Counter('bcc') == TestCounter({'a': 1, 'b': 3, 'c': 2})

def test___and__(TestCounter):
    assert TestCounter('abbb') & TestCounter('bcc') == TestCounter({'b': 1})
    assert TestCounter('abbb') & Counter('bcc') == TestCounter({'b': 1})

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

if __name__ == '__main__':
    import pytest
    pytest.main()

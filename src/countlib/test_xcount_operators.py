import pytest

from countlib import ExtremeCounter
from collections import Counter

@pytest.fixture
def abc():
    return ExtremeCounter("abc")

@pytest.fixture
def abctwo():
    return ExtremeCounter("abcabbcccddeefgggggghiii")


def test___neg__(abc, abctwo):
    neg = -abc
    assert neg == ExtremeCounter({'a': -1, 'b': -1, 'c': -1})

def test___abs__(abc, abctwo):
    neg = -abc
    assert abs(neg) == abc
    neg = -abctwo
    assert abs(neg) == abctwo

def test___pos__(abc, abctwo):
    neg = -abc
    assert not +neg

def test___add__magic(abc, abctwo):
    assert abc + 2
    assert abc + (-100)
    assert not +(abctwo + (-10))

def test__radd__(abc):
    assert 2 + abc == Counter("abcabc") + abc


def test___sub__magic(abc, abctwo):
    assert abc - 2
    assert not abc - 2 + Counter()
    assert abc - (-100)
    assert not +(abctwo - 10)

def test_value_magic(abc, abctwo):
    assert (abc * "l" + "o" + "l")["b"] == "lol"

def test___add__():
    assert ExtremeCounter('abbb') + ExtremeCounter('bcc') == ExtremeCounter({'a': 1, 'b': 4, 'c': 2})
    assert ExtremeCounter('abbb') + Counter('bcc') == ExtremeCounter({'a': 1, 'b': 4, 'c': 2})
    assert ExtremeCounter('aaa') + ExtremeCounter.fromkeys('a', -1) == ExtremeCounter({'a': 2})
    assert ExtremeCounter('aaa') + ExtremeCounter.fromkeys('a', -3) == ExtremeCounter()

def test___sub__():
    assert ExtremeCounter('abbbc') - ExtremeCounter('bccd') == ExtremeCounter({'a': 1, 'b': 2})
    assert ExtremeCounter('abbbc') - Counter('bccd') == ExtremeCounter({'a': 1, 'b': 2})

def test__rsub__(abc):
    assert 2 - abc == Counter("aabbcc") - (Counter("abcabc") - abc)

def test_add(abc, abctwo):
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
    a.add(a=-10)
    assert a["a"] == -10
    abctwo.add(abc)
    assert "d" not in abc


def test_subtract():
    c = Counter('which')
    c.subtract('witch')             # subtract elements from another iterable
    c.subtract(Counter('watch'))    # subtract elements from another counter
    assert c['h'] == 0              # 2 in which, minus 1 in witch, minus 1 in watch
    assert c['w'] == -1             # 1 in which, minus 1 in witch, minus 1 in watch
    c.subtract(w=-6)
    assert c['w'] == 5

def test___mul__magic(abc, abctwo):
    assert abc * 2
    assert abctwo * 0
    assert not (abctwo * 0) + Counter()
    try:
        assert 0 * abctwo
        assert not (0 * abctwo) + Counter()
        assert "Yippie, found a way!"
    except:
        assert "hmpf. impossible?"
    assert abctwo * []
    wow = abctwo * ["peng"]
    assert wow["peng"] == 0
    assert wow["a"] == ["peng", "peng"]

def test___mul__(abc, abctwo):
    d = (abc * 2) * abctwo
    assert d
    assert d["a"] == 4
    assert d["g"] == 0
    assert set(d.keys()) == set("abc")

def test__rmul__(abc):
    assert 4 * abc == Counter("abcabc") * (Counter("abcabc") * abc)

def test___div__magic(abc, abctwo):
    assert ((abc * 3) / 3) == abc
    a = abctwo / 2
    b = abctwo - abctwo / 2
    for elem, cnt in abctwo.items():
        if cnt % 2:
            assert a[elem] + 1 == b[elem]
        else:
            assert a[elem] == b[elem]

def test___div__(abc, abctwo):
    d = abc / abctwo
    assert not d
    assert d["a"] == 0
    assert not d + 1
    e = abctwo / abc
    assert e
    assert e["a"] == 2
    assert "f" not in e
    assert e + 0

def test__rdiv__(abc):
    assert 1 / abc == Counter("abcabc") / (Counter("abcabc") / abc)

def test___floordiv__magic(abc, abctwo):
    assert ((abc * 3) // 3) == abc
    a = abctwo // 2
    b = abctwo - abctwo // 2
    for elem, cnt in abctwo.items():
        if cnt % 2:
            assert a[elem] + 1 == b[elem]
        else:
            assert a[elem] == b[elem]

def test___floordiv__(abc, abctwo):
    d = abc // abctwo
    assert not d
    assert d["a"] == 0
    assert not d + 1
    e = abctwo // abc
    assert e
    assert e["a"] == 2
    assert "f" not in e
    assert e + 0

def test___truediv__(abc, abctwo):
    d = abc.__truediv__(abctwo)
    assert d
    assert not +(d - 1)
    assert d["a"] > 0
    assert d + 1
    e = abctwo.__truediv__(abc)
    assert e
    assert e["a"] == 2
    assert "f" not in e
    assert e + 0

def test___invert__(abc, abctwo):
    d = ~abc
    assert d
    assert not +d
    e = ~abctwo
    assert e
    assert not +e
    assert +e["b"] == -4

def test___rshift__(abc, abctwo):
    d = (abc>>1)
    assert d
    assert not +d
    e = abctwo >> 1
    assert e
    assert +e
    f = (abc+abc) >> abc
    assert f == abc
    assert (abc+abc)>>2 == abc * 0

def test__rrshift__(abc):
    assert 2 >> abc == abc
    assert Counter("abc") >> abc == {}

def test___lshift__(abc, abctwo):
    d = (abc<<1)+abc
    assert d == abc * 3
    assert d << 4
    e = abctwo << 1
    assert e
    assert +e
    f = abc << abc
    assert f
    assert f == abc * 2
    assert not abctwo * 2 - (abctwo << abctwo)

def test__rlshift__(abc):
    assert 1 << abc == abc + abc
    assert Counter("abc") << abc == 2 * abc

def test___mod__magic(abc, abctwo):
    hehe = abc * "l%sl"
    hoho = abc * "o"
    assert hehe % hoho == hehe % "o" == abc * "lol"

def test___mod__(abc, abctwo):
    assert abc % abctwo
    assert abc % abctwo == abc
    assert not (abctwo % abc) == abc
    assert (abc % abctwo)["b"] == 1

def test__rmod__(abctwo):
    t = 1 % abctwo
    assert t
    assert set(t.values()) == set([0,1])
    assert Counter("abcabc") % +(Counter("abcabc") % abctwo)

def test___pow__magic(abc, abctwo):
    assert (abc ** 1.0) ** 2 == (abc ** 1) ** 2

def test___pow__(abc, abctwo):
    d = abc ** abctwo
    assert d
    assert d == abc
    e = abctwo ** abc
    assert ( (e - 1 + Counter() + 1) ** (abc - 1) ) == abc

def test__rpow__(abc):
    assert 2 ** 2 ** abc == Counter("abcabc") ** (Counter("abcabc") ** abc)

def test___or__():
    assert ExtremeCounter('abbb') | ExtremeCounter('bcc') == ExtremeCounter({'a': 1, 'b': 3, 'c': 2})
    assert ExtremeCounter('abbb') | Counter('bcc') == ExtremeCounter({'a': 1, 'b': 3, 'c': 2})

def test___or__magic(abc):
    assert (abc | 4)["b"] == 4
    assert (abc | 4)["r"] == 0
    assert (abc | -4)["b"] == 1
    assert (abc | -4)["r"] == 0

def test___ror__():
    assert Counter('bcc') | ExtremeCounter('abbb') == ExtremeCounter({'a': 1, 'b': 3, 'c': 2})
    assert 4 | ExtremeCounter('a') == ExtremeCounter("aaaa")

def test___and__():
    assert ExtremeCounter('abbb') & ExtremeCounter('bcc') == ExtremeCounter({'b': 1})
    assert ExtremeCounter('abbb') & Counter('bcc') == ExtremeCounter({'b': 1})

def test___rand__():
    assert Counter('abbb') & ExtremeCounter('bcc') == Counter({'b': 1})
    assert 4 & ExtremeCounter("aa") == dict(a=2)

def test___and__magic(abc):
    assert (abc & 4)["b"] == 1
    assert (abc & 4)["r"] == 0
    assert (abc & -4)["b"] == -4
    assert (abc & -4)["r"] == 0

def test___xor__():
    lol = ExtremeCounter('110abbbc') ^ ExtremeCounter('bccdeeef')
    assert lol
    assert lol["0"] == 1
    assert lol["1"] == 2
    assert lol["b"] == 2
    assert lol["a"] == 1
    assert lol["f"] == 1
    assert lol["e"] == 3
    assert ExtremeCounter('abbb') ^ Counter('bcc') == ExtremeCounter('abbcc')
    assert ExtremeCounter('abbbcc') ^ Counter('bcac') == Counter({'b': 2})

def test___rxor__():
    assert Counter('cabc') ^ ExtremeCounter('abbbcc') == Counter({'b': 2})
    assert 1 ^ ExtremeCounter('abbbcc') == ExtremeCounter({'a': 0, 'b': 2, 'c': 3})

def test___xor__magic(abc):
    assert (abc ^ 4)["b"] == 5
    assert (abc ^ 4)["r"] == 0
    assert (abc ^ -4)["b"] == -3
    assert (abc ^ -4)["r"] == 0

if __name__ == '__main__':
    import pytest
    pytest.main()

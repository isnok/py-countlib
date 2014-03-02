import pytest

from countlib import AdvancedCounter
from countlib import ExtremeCounter
from collections import Counter

base_implementations = (AdvancedCounter, ExtremeCounter)

@pytest.fixture
def abc(TestCounter):
    return TestCounter("abc")

@pytest.fixture
def abctwo(TestCounter):
    return TestCounter("abcabbcccddeefgggggghiii")

def pytest_generate_tests(metafunc):
    if 'TestCounter' in metafunc.fixturenames:
        metafunc.parametrize('TestCounter', base_implementations)

def test___neg__(TestCounter, abc, abctwo):
    neg = -abc
    assert neg == TestCounter({'a': -1, 'b': -1, 'c': -1})

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

def test___add__(TestCounter):
    assert TestCounter('abbb') + TestCounter('bcc') == TestCounter({'a': 1, 'b': 4, 'c': 2})
    assert TestCounter('abbb') + Counter('bcc') == TestCounter({'a': 1, 'b': 4, 'c': 2})
    assert TestCounter('aaa') + TestCounter.fromkeys('a', -1) == TestCounter({'a': 2})
    assert TestCounter('aaa') + TestCounter.fromkeys('a', -3) == TestCounter()

def test___sub__(TestCounter):
    assert TestCounter('abbbc') - TestCounter('bccd') == TestCounter({'a': 1, 'b': 2})
    assert TestCounter('abbbc') - Counter('bccd') == TestCounter({'a': 1, 'b': 2})

def test__rsub__(abc):
    assert 2 - abc == Counter("aabbcc") - (Counter("abcabc") - abc)

def test_add(TestCounter, abc, abctwo):
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
    abctwo.add(abc)
    assert "d" not in abc


def test_subtract(TestCounter):
    c = TestCounter('which')
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

def test___or__(TestCounter):
    assert TestCounter('abbb') | TestCounter('bcc') == TestCounter({'a': 1, 'b': 3, 'c': 2})
    assert TestCounter('abbb') | Counter('bcc') == TestCounter({'a': 1, 'b': 3, 'c': 2})

def test___or__magic(abc):
    assert (abc | 4)["b"] == 4
    assert (abc | 4)["r"] == 0
    assert (abc | -4)["b"] == 1
    assert (abc | -4)["r"] == 0

def test___ror__(TestCounter):
    assert Counter('bcc') | TestCounter('abbb') == TestCounter({'a': 1, 'b': 3, 'c': 2})
    assert 4 | TestCounter('a') == TestCounter("aaaa")

def test___and__(TestCounter):
    assert TestCounter('abbb') & TestCounter('bcc') == TestCounter({'b': 1})
    assert TestCounter('abbb') & Counter('bcc') == TestCounter({'b': 1})

def test___rand__(TestCounter):
    assert Counter('abbb') & TestCounter('bcc') == Counter({'b': 1})
    assert 4 & TestCounter("aa") == dict(a=2)

def test___and__magic(abc):
    assert (abc & 4)["b"] == 1
    assert (abc & 4)["r"] == 0
    assert (abc & -4)["b"] == -4
    assert (abc & -4)["r"] == 0

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

def test___xor__magic(abc):
    assert (abc ^ 4)["b"] == 5
    assert (abc ^ 4)["r"] == 0
    assert (abc ^ -4)["b"] == -3
    assert (abc ^ -4)["r"] == 0

if __name__ == '__main__':
    import pytest
    pytest.main()

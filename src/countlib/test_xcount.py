import pytest

from countlib import ExtremeCounter
from collections import Counter
from pivot import PivotCounter

@pytest.fixture
def abc():
    return ExtremeCounter("abc")

@pytest.fixture
def abctwo():
    return ExtremeCounter("abcabbcccddeefgggggghiii")

def test_class():
    assert ExtremeCounter('zyzygy') == ExtremeCounter({'g': 1, 'y': 3, 'z': 2})
    y = ExtremeCounter("yay.")
    assert y + ExtremeCounter.fromkeys('zab.', 3) == ExtremeCounter({'.': 4, 'a': 4, 'b': 3, 'y': 2, 'z': 3})
    assert y - ExtremeCounter.fromkeys('zab.', 3) == ExtremeCounter({'y': 2})
    y.subtract(ExtremeCounter.fromkeys('zab.', 3))
    assert y == ExtremeCounter({'.': -2, 'a': -2, 'b': -3, 'y': 2, 'z': -3})
    y.add(ExtremeCounter.fromkeys('zab.', 3))
    assert y == ExtremeCounter({'.': 1, 'a': 1, 'b': 0, 'y': 2, 'z': 0})
    assert y + Counter() == ExtremeCounter({'.': 1, 'a': 1, 'y': 2})
    assert y.pivot() == PivotCounter({0: ['b', 'z'], 1: ['.', 'a'], 2: ['y']})
    assert y.transpose() == ExtremeCounter({0: 2, 1: 2, 2: 1})

def test_bool(abc):
    assert abc
    assert bool(abc)
    assert (not abc) == False
    assert not ExtremeCounter()
    assert (not ExtremeCounter()) == True

def test_most_common():
    p = ExtremeCounter('abracadabra!')
    assert p.most_common(3) == [('a', 5), ('b', 2), ('r', 2)]
    assert p.most_common(2, inverse=True) == [('!', 1), ('c', 1)]
    assert p.most_common(2, count_func=lambda i: -i[1]) == [('!', 1), ('c', 1)]
    assert p.most_common(2, count_func=lambda i: -i[1], inverse=True) == [('a', 5), ('b', 2)]

def test_most_common_counts():
    x = ExtremeCounter("yay? nice!! this thing works!")
    x.update("etsttseststttsetsetse ")
    assert x.most_common_counts(1) == [('t', 11)]
    assert x.most_common_counts(5) == [('t', 11), ('s', 9), ('e', 6), (' ', 5), ('i', 3), ('!', 3)]

def test_pivot():
    x = ExtremeCounter("yay? nice!! this thing works!")
    x.update("etsttseststttsetsetse ")
    assert x.transpose().pivot(PivotCounter) == PivotCounter({1: [5, 6, 9, 11], 2: [3], 3: [2], 8: [1]})
    x.__pivot__ = PivotCounter
    assert x.pivot() + x.pivot() == PivotCounter(
            {10: [' '], 12: ['e'], 18: ['s'], 22: ['t'],
              2: ['?', 'a', 'c', 'g', 'k', 'o', 'r', 'w'],
              4: ['h', 'n', 'y'], 6: ['!', 'i']})
    lol = ExtremeCounter("lollofant!!")
    troll = ExtremeCounter("trollofant")
    assert lol.pivot() - troll.pivot() == PivotCounter({1: ['l'], 2: ['!']})
    assert lol.pivot() + troll.pivot() == PivotCounter({1: ['r'], 2: ['!', 'a', 'f', 'n'], 3: ['t'], 4: ['o'], 5: ['l']})

def test_transpose():
    x = ExtremeCounter("yay? nice!! this thing works!")
    x.update("etsttseststttsetsetse ")
    tp_chain = [
        ExtremeCounter({1: 1}),
        ExtremeCounter({2: 1}),
        ExtremeCounter({1: 2}),
        ExtremeCounter({1: 1, 3: 1}),
        ExtremeCounter({1: 3, 4: 1}),
        ExtremeCounter({1: 4, 2: 1, 3: 1, 8: 1}),
        ExtremeCounter({11: 1, 1: 8, 2: 3, 3: 2, 5: 1, 6: 1, 9: 1}),
        ExtremeCounter({' ': 5, '!': 3, '?': 1, 'a': 1, 'c': 1, 'e': 6, 'g': 1, 'h': 2, 'i': 3, 'k': 1, 'n': 2, 'o': 1, 'r': 1, 's': 9, 't': 11, 'w': 1, 'y': 2}),
    ]
    old_x = None
    while old_x != x:
        old_x = x
        x = x.transpose()
        assert old_x == tp_chain.pop()

def test_fromkeys():
    assert ExtremeCounter.fromkeys('bumm') == ExtremeCounter({'b': 0, 'm': 0, 'u': 0})
    x = ExtremeCounter.fromkeys('bumm', 50)
    assert x == ExtremeCounter({'b': 50, 'm': 50, 'u': 50})
    assert x + x == ExtremeCounter({'b': 100, 'm': 100, 'u': 100})
    assert x + x == ExtremeCounter.fromkeys(x, 50+50)

def test___repr__():
    assert ExtremeCounter('bumm') == ExtremeCounter({'b': 1, 'm': 2, 'u': 1})
    assert ExtremeCounter({'b': 1, 'm': 2, 'u': 1}) == ExtremeCounter({'b': 1, 'm': 2, 'u': 1})
    for stuff in ('abc', 'bcccnnno', (12,12,3,4,5,3,3)):
        x = ExtremeCounter(stuff)
        assert x == eval(repr(x))

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

def test___mod__magic(abc, abctwo):
    hehe = abc * "l%sl"
    hoho = abc * "o"
    assert hehe % hoho == hehe % "o" == abc * "lol"

def test___mod__(abc, abctwo):
    assert abc % abctwo
    assert abc % abctwo == abc
    assert not (abctwo % abc) == abc
    assert (abc % abctwo)["b"] == 1

def test___pow__magic(abc, abctwo):
    assert (abc ** 1.0) ** 2 == (abc ** 1) ** 2

def test___pow__(abc, abctwo):
    d = abc ** abctwo
    assert d
    assert d == abc
    e = abctwo ** abc
    assert ( (e - 1 + Counter() + 1) ** (abc - 1) ) == abc

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

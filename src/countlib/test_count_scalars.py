import pytest
from collections import Counter

def test___add__magic(cnt_abc, cnt_ab2):
    assert cnt_abc + 2
    assert cnt_abc + (-100)
    assert not +(cnt_ab2 + (-10))

def test___sub__magic(cnt_abc, cnt_ab2):
    assert cnt_abc - 2
    assert not cnt_abc - 2 + Counter()
    assert cnt_abc - (-100)
    assert not +(cnt_ab2 - 10)

def test___mul__magic(cnt_abc, cnt_ab2):
    assert cnt_abc * 2
    assert cnt_ab2 * 0
    assert not (cnt_ab2 * 0) + Counter()
    try:
        assert 0 * cnt_ab2
        assert not (0 * cnt_ab2) + Counter()
        assert "Yippie, found a way!"
    except:
        assert "hmpf. impossible?"
    assert cnt_ab2 * []
    wow = cnt_ab2 * ["peng"]
    assert wow["peng"] == 0
    assert wow["a"] == ["peng", "peng"]

def test___div__magic(cnt_abc, cnt_ab2):
    assert ((cnt_abc * 3) / 3) == cnt_abc
    a = cnt_ab2 / 2
    b = cnt_ab2 - cnt_ab2 / 2
    for elem, cnt in cnt_ab2.items():
        if cnt % 2:
            assert a[elem] + 1 == b[elem]
        else:
            assert a[elem] == b[elem]

def test___floordiv__magic(cnt_abc, cnt_ab2):
    assert ((cnt_abc * 3) // 3) == cnt_abc
    a = cnt_ab2 // 2
    b = cnt_ab2 - cnt_ab2 // 2
    for elem, cnt in cnt_ab2.items():
        if cnt % 2:
            assert a[elem] + 1 == b[elem]
        else:
            assert a[elem] == b[elem]

def test___mod__magic(cnt_abc, cnt_ab2):
    hehe = cnt_abc * "l%sl"
    hoho = cnt_abc * "o"
    assert hehe % hoho == hehe % "o" == cnt_abc * "lol"

def test___pow__magic(cnt_abc, cnt_ab2):
    assert (cnt_abc ** 1.0) ** 2 == (cnt_abc ** 1) ** 2

def test___or__magic(cnt_abc):
    assert (cnt_abc | 4)["b"] == 4
    assert (cnt_abc | 4)["r"] == 0
    assert (cnt_abc | -4)["b"] == 1
    assert (cnt_abc | -4)["r"] == 0

def test___and__magic(cnt_abc):
    assert (cnt_abc & 4)["b"] == 1
    assert (cnt_abc & 4)["r"] == 0
    assert (cnt_abc & -4)["b"] == -4
    assert (cnt_abc & -4)["r"] == 0

def test___xor__magic(cnt_abc):
    assert (cnt_abc ^ 4)["b"] == 5
    assert (cnt_abc ^ 4)["r"] == 0
    assert (cnt_abc ^ -4)["b"] == -3
    assert (cnt_abc ^ -4)["r"] == 0


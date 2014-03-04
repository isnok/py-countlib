import pytest

def test___neg__(TestCounter, cnt_abc, cnt_ab2):
    neg = -cnt_abc
    assert neg == TestCounter({'a': -1, 'b': -1, 'c': -1})
    assert -cnt_ab2 == TestCounter({'a': -2, 'b': -3, 'c': -4, 'd': -2, 'e': -2, 'f': -1, 'g': -6, 'h': -1, 'i': -3})
    assert -(neg * 4 + cnt_ab2) == TestCounter({'e': -2, 'd': -2, 'g': -6, 'f': -1, 'i': -3, 'h': -1})

def test___abs__(cnt_abc, cnt_ab2):
    neg = -cnt_abc
    assert abs(neg) == cnt_abc
    neg = -cnt_ab2
    assert abs(neg) == cnt_ab2

def test___pos__(cnt_abc, cnt_ab2):
    neg = -cnt_abc
    assert not +neg
    neg += neg
    neg += neg
    neg += cnt_ab2
    assert +neg == {'a': 2, 'c': 4, 'b': 3, 'e': 2, 'd': 2, 'g': 6, 'f': 1, 'i': 3, 'h': 1}

def test___invert__(cnt_abc, cnt_ab2):
    d = ~cnt_abc
    assert d
    assert not +d
    e = ~cnt_ab2
    assert e
    assert not +e
    assert +e["b"] == -4

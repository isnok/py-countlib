import pytest

def test___neg__(TestCounter, cnt_abc, cnt_ab2):
    neg = -cnt_abc
    assert neg == TestCounter({'a': -1, 'b': -1, 'c': -1})

def test___abs__(cnt_abc, cnt_ab2):
    neg = -cnt_abc
    assert abs(neg) == cnt_abc
    neg = -cnt_ab2
    assert abs(neg) == cnt_ab2

def test___pos__(cnt_abc, cnt_ab2):
    neg = -cnt_abc
    assert not +neg


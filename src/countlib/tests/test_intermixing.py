import pytest

from xcount import ExtremeCounter
from pivot import PivotCounter
from pivot import CoolPivotCounter

@pytest.fixture
def x():
    return ExtremeCounter("yay? nice!! this thing works!!")


def test_features(x):
    assert ExtremeCounter("countlib") == ExtremeCounter({'b': 1, 'c': 1, 'i': 1, 'l': 1, 'n': 1, 'o': 1, 't': 1, 'u': 1})
    assert x.most_common_counts(1) == [(' ', 4), ('!', 4)]
    assert x.most_common_counts(1, inverse=True) == [('a', 1), ('c', 1), ('e', 1), ('g', 1), ('k', 1), ('o', 1), ('w', 1), ('r', 1), ('?', 1)]

def test_variants(x):
    x_1 = x.pivot()
    assert x_1 == PivotCounter({1: ['?', 'a', 'c', 'e', 'g', 'k', 'o', 'r', 'w'], 2: ['h', 'n', 's', 't', 'y'], 3: ['i'], 4: [' ', '!']})
    assert x_1.unpivot() == ExtremeCounter({' ': 4, '!': 4, '?': 1, 'a': 1, 'c': 1, 'e': 1, 'g': 1, 'h': 2, 'i': 3, 'k': 1, 'n': 2, 'o': 1, 'r': 1, 's': 2, 't': 2, 'w': 1, 'y': 2})
    x_2 = x.pivot(CoolPivotCounter)
    assert x_2 == CoolPivotCounter({1: ['?', 'a', 'c', 'e', 'g', 'k', 'o', 'r', 'w'], 2: ['h', 'n', 's', 't', 'y'], 3: ['i'], 4: [' ', '!']})
    assert x_2.unpivot() == x
    assert isinstance(x_2.unpivot(), x.__class__)
    assert x_2.unpivot().__class__ == x.__class__
    assert x_1 == x_2
    assert x.transpose() == ExtremeCounter({1: 9, 2: 5, 3: 1, 4: 2})

if __name__ == '__main__':
    import pytest
    pytest.main("-x countlib")

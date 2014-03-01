""" countlib - Charged up Counters.

    >>> ExtremeCounter("countlib")
    ExtremeCounter({'b': 1, 'c': 1, 'i': 1, 'l': 1, 'n': 1, 'o': 1, 't': 1, 'u': 1})
    >>> x = ExtremeCounter("yay? nice!! this thing works!!")
    >>> x.most_common_counts(1)
    [(' ', 4), ('!', 4)]
    >>> x.most_common_counts(1, inverse=True)
    [('a', 1), ('c', 1), ('e', 1), ('g', 1), ('k', 1), ('o', 1), ('w', 1), ('r', 1), ('?', 1)]
    >>> x_1 = x.pivot()
    >>> x_1
    PivotCounter({1: ['?', 'a', 'c', 'e', 'g', 'k', 'o', 'r', 'w'], 2: ['h', 'n', 's', 't', 'y'], 3: ['i'], 4: [' ', '!']})
    >>> x_1.unpivot()
    ExtremeCounter({' ': 4, '!': 4, '?': 1, 'a': 1, 'c': 1, 'e': 1, 'g': 1, 'h': 2, 'i': 3, 'k': 1, 'n': 2, 'o': 1, 'r': 1, 's': 2, 't': 2, 'w': 1, 'y': 2})
    >>> x_2 = x.pivot(CoolPivotCounter)
    >>> x_2
    CoolPivotCounter({1: ['?', 'a', 'c', 'e', 'g', 'k', 'o', 'r', 'w'], 2: ['h', 'n', 's', 't', 'y'], 3: ['i'], 4: [' ', '!']})
    >>> x_2.unpivot() == x
    True
    >>> isinstance(x_2.unpivot(), x.__class__)
    True
    >>> x_2.unpivot().__class__ == x.__class__
    True
    >>> x_1 == x_2
    True
    >>> x.transpose()
    ExtremeCounter({1: 9, 2: 5, 3: 1, 4: 2})

"""
from xcount import ExtremeCounter
from pivot import PivotCounter
from pivot import CoolPivotCounter

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    for module in ('xcount', 'pivot',): # 'basepivot'):
        print "%s: %s" % (module, doctest.testmod(__import__(module)))

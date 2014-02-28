from xcount import ExtremeCounter
from pivot import PivotCounter
from coolpivot import CoolPivotCounter

if __name__ == '__main__':
    import doctest
    for module in ('xcount', 'pivot', 'coolpivot'):
        print "%s: %s" % (module, doctest.testmod(__import__(module)))

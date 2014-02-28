from xcount import ExtremeCounter
from pivot import PivotCounter

if __name__ == '__main__':
    import doctest
    for module in ('xcount', 'pivot'):
        print "%s: %s" % (module, doctest.testmod(__import__(module)))

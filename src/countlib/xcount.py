""" Counters strike! """
from collections import Counter
from collections import Mapping
from pivot import CoolPivotCounter
from acount import AdvancedCounter

from operator import itemgetter
from heapq import nlargest, nsmallest

class ExtremeCounter(AdvancedCounter):
    """ Even more extreme! This version supports slicing by values (counts).
    """
    __pivot__ = CoolPivotCounter

    def __getitem__(self, key):
        if isinstance(key, slice):
            start, stop, step = key.start, key.stop, key.step
            if step is None:
                if start is not None and stop is not None:
                    return [ i for i in self.iteritems() if start <= i[1] < stop ]
                if start is not None and stop is None:
                    return [ i for i in self.iteritems() if start <= i[1] ]
                if start is None and stop is not None:
                    return [ i for i in self.iteritems() if i[1] < stop ]
                if start is None and stop is None:
                    return self.items()
            elif step == -1:
                if start is not None and stop is not None:
                    return [ i for i in self.iteritems() if not start <= i[1] < stop ]
                if start is not None and stop is None:
                    return [ i for i in self.iteritems() if not start <= i[1] ]
                if start is None and stop is not None:
                    return [ i for i in self.iteritems() if not i[1] < stop ]
                if start is None and stop is None:
                    return []

            raise KeyError(key)
        else:
            return dict.__getitem__(self, key)

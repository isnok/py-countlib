""" Counters strike! """
from collections import Counter
from collections import Mapping
from pivot import PivotCounter
from acount import AdvancedCounter

from operator import itemgetter
from heapq import nlargest, nsmallest

class ExtremeCounter(AdvancedCounter):
    """ Even more extreme! This version supports slicing by values (counts).
        Getting and deleting via slices is supported.
        Setting items via slicing makes little sense, since one counted item
        has only one count, and thus cannot be assigned a range of counts.
    """
    __pivot__ = PivotCounter

    def __getitem__(self, key):
        if isinstance(key, slice):
            start, stop, step = key.start, key.stop, key.step
            if step is None:
                if start is not None and stop is not None:
                    return self.__class__(**dict([ i for i in self.iteritems() if start <= i[1] < stop ]))
                if start is not None and stop is None:
                    return self.__class__(**dict([ i for i in self.iteritems() if start <= i[1] ]))
                if start is None and stop is not None:
                    return self.__class__(**dict([ i for i in self.iteritems() if i[1] < stop ]))
                if start is None and stop is None:
                    return self.copy()
            elif step == -1:
                if start is not None and stop is not None:
                    return self.__class__(**dict([ i for i in self.iteritems() if not start <= i[1] < stop ]))
                if start is not None and stop is None:
                    return self.__class__(**dict([ i for i in self.iteritems() if not start <= i[1] ]))
                if start is None and stop is not None:
                    return self.__class__(**dict([ i for i in self.iteritems() if not i[1] < stop ]))
                if start is None and stop is None:
                    return self.__class__()

            raise KeyError(key)
        else:
            return dict.__getitem__(self, key)

    def __delitem__(self, key):
        """ Like dict.__delitem__() but does not raise KeyError for missing values.
            Also this supports slicing by values (counts).
        """
        if isinstance(key, slice):
            start, stop, step = key.start, key.stop, key.step
            if step is None:
                if start is not None and stop is not None:
                    for k, v in [ i for i in self.iteritems() if start <= i[1] < stop ]:
                        dict.__delitem__(self, k)
                if start is not None and stop is None:
                    for k, v in [ i for i in self.iteritems() if start <= i[1] ]:
                        dict.__delitem__(self, k)
                if start is None and stop is not None:
                    for k, v in [ i for i in self.iteritems() if i[1] < stop ]:
                        dict.__delitem__(self, k)
                if start is None and stop is None:
                    for k in self.keys():
                        dict.__delitem__(self, k)
            elif step == -1:
                if start is not None and stop is not None:
                    for k, v in [ i for i in self.iteritems() if not start <= i[1] < stop ]:
                        dict.__delitem__(self, k)
                if start is not None and stop is None:
                    for k, v in [ i for i in self.iteritems() if not start <= i[1] ]:
                        dict.__delitem__(self, k)
                if start is None and stop is not None:
                    for k, v in [ i for i in self.iteritems() if not i[1] < stop ]:
                        dict.__delitem__(self, k)
                if start is None and stop is None:
                    return
        elif key in self:
            dict.__delitem__(self, key)

    def pivot(self, cls=None):
        """ The pivot table of the Counter.
        """
        if cls:
            return cls(self)
        return self.__pivot__(self)


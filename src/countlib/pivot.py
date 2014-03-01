""" Pivot table variants. """

from basepivot import PivotCounterBase
from collections import Counter

class PivotCounter(PivotCounterBase):
    """ Uses normal sets to store values.
    """

    def update(self, iterable=None, **kwds):
        """ Like Counter.update() but union sets instead of adding counts.
            Source can be a dictionary or Counter instance or another PivotCounter.
        """
        if iterable is not None:
            if isinstance(iterable, PivotCounterBase):
                self.__unpivot__ = iterable.__unpivot__
                dict.update(self, iterable) # update from other PivotCounter
            elif hasattr(iterable, 'iteritems'): # assumed Counters and dicts
                self.__unpivot__ = iterable.__class__
                self_sdf = self.setdefault
                for elem, count in iterable.iteritems():
                    try: # a normal Counter entry
                        self_sdf(count, set()).add(elem)
                    except TypeError: # another PivotCounter?
                        self_sdf(elem, set()).update(count)
            else: # slow mem eater path (by now)
                self.update(Counter(iterable))
        if kwds:
            self.update(kwds)

    def __missing__(self, key):
        """ Create a new key if it is requested. Since values are mutable they
            need to be stored for the case of modification somewhere outside.
            This differs from the behaviour of the frozen variant.
        """
        return self.setdefault(key, set())

    def copy(self):
        """ Like dict.copy() but returns a PivotCounter instance instead of a dict.
            The sets acting as values are copied as well.
        """
        result = PivotCounter()
        for count in self:
            result[count] = self[count].copy()
        return result


class CoolPivotCounter(PivotCounterBase):
    """ Uses frozensets to store values.
    """

    def update(self, iterable=None, **kwds):
        """ Like Counter.update() but union sets instead of adding counts.
            Source can be a dictionary or Counter instance or another CoolPivotCounter.
        """
        if iterable is not None:
            if isinstance(iterable, PivotCounterBase):
                self.__unpivot__ = iterable.__unpivot__
                dict.update(self, iterable) # fast path when counter is empty
            elif hasattr(iterable, 'iteritems'): # assumed Counters and dicts
                self.__unpivot__ = iterable.__class__
                self_get = self.get
                for elem, count in iterable.iteritems():
                    try: # a normal Counter entry
                        self[count] = self_get(count, frozenset()).union([elem])
                    except TypeError: # another CoolPivotCounter?
                        self[elem] = self_get(elem, frozenset()).union(count)
            else: # slow mem eater path (by now)
                self.update(Counter(iterable))
        if kwds:
            self.update(kwds)

    def __missing__(self, key):
        """ Return an empty set if asked for a missing key, but don't store it.
            Since the values are immutable, the key is not added to the dict.
            This differs from the behaviour of the mutable variant.
        """
        return frozenset()

    def copy(self):
        """ Like dict.copy() but returns a CoolPivotCounter instance instead of a dict.
            The sets acting as values are copied as well.
        """
        return dict.copy(self)

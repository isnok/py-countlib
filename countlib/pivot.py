""" Pivot table variants. """

from basepivot import PivotCounterBase
from collections import Counter

class PivotCounter(PivotCounterBase):
    """ Uses normal sets to store values.

    >>> isinstance(PivotCounter('abbb')[1], set)
    True
    >>> isinstance(PivotCounter('abbb')[1], frozenset)
    False
    >>> isinstance(PivotCounter('abbb')[10], set)
    True
    >>> isinstance(PivotCounter('abbb')[10], frozenset)
    False

    """

    def update(self, iterable=None, **kwds):
        """ Like Counter.update() but union sets instead of adding counts.
            Source can be a dictionary or Counter instance or another PivotCounter.

        >>> d = PivotCounter('watch')
        >>> d.update('boofittii')          # add in elements via another counter-like
        >>> d                              #        v------- o_O -------v
        PivotCounter({1: ['a', 'b', 'c', 'f', 'h', 't', 'w'], 2: ['o', 't'], 3: ['i']})
        >>> PivotCounter(d.unpivot())      # to fix it regenerate the PivotCounter
        PivotCounter({1: ['a', 'b', 'c', 'f', 'h', 'w'], 2: ['o'], 3: ['i', 't']})
        >>> c = PivotCounter('which')
        >>> c.update(PivotCounter('boof')) # update the dict way
        >>> c
        PivotCounter({1: ['b', 'f'], 2: ['o']})

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
        """ Create a new, empty PivotCounter object. And if given, count elements
            from an input Counter or dict. Or, initialize from another PivotCounter.

        >>> PivotCounter()["x"]
        set([])
        """
        return set()

    def copy(self):
        """ Like dict.copy() but returns a PivotCounter instance instead of a dict.
            The sets acting as values are copied as well.

        >>> c = PivotCounter('which')
        >>> d = c.copy()
        >>> del c[2]
        >>> c == d
        False
        >>> c, d
        (PivotCounter({1: ['c', 'i', 'w']}), PivotCounter({1: ['c', 'i', 'w'], 2: ['h']}))
        >>> d[1].discard('c')
        >>> c == d
        False
        >>> c, d
        (PivotCounter({1: ['c', 'i', 'w']}), PivotCounter({1: ['i', 'w'], 2: ['h']}))
        """
        result = PivotCounter()
        for count in self:
            result[count] = self[count].copy()
        return result


class CoolPivotCounter(PivotCounterBase):
    """ Uses frozensets to store values.

    >>> isinstance(CoolPivotCounter('abbb')[1], set)
    False
    >>> isinstance(CoolPivotCounter('abbb')[1], frozenset)
    True
    >>> isinstance(CoolPivotCounter('abbb')[10], set)
    False
    >>> isinstance(CoolPivotCounter('abbb')[10], frozenset)
    True

    """

    def update(self, iterable=None, **kwds):
        """ Like Counter.update() but union sets instead of adding counts.
            Source can be a dictionary or Counter instance or another CoolPivotCounter.

        >>> d = CoolPivotCounter('watch')
        >>> d.update('boofittii')          # add in elements via another counter-like
        >>> d                              #  v---- notice the now existing duplicate -----v
        CoolPivotCounter({1: ['a', 'b', 'c', 'f', 'h', 't', 'w'], 2: ['o', 't'], 3: ['i']})
        >>> CoolPivotCounter(d.unpivot())      # to fix it regenerate the CoolPivotCounter
        CoolPivotCounter({1: ['a', 'b', 'c', 'f', 'h', 'w'], 2: ['o'], 3: ['i', 't']})
        >>> c = CoolPivotCounter('which')
        >>> c.update(CoolPivotCounter('boof')) # update the dict way
        >>> c
        CoolPivotCounter({1: ['b', 'f'], 2: ['o']})

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
        """ Create a new, empty CoolPivotCounter object. And if given, count elements
            from an input Counter or dict. Or, initialize from another CoolPivotCounter.

        >>> CoolPivotCounter()["x"]
        frozenset([])
        """
        return frozenset()

    def copy(self):
        """ Like dict.copy() but returns a CoolPivotCounter instance instead of a dict.
            The sets acting as values are copied as well.

        >>> c = CoolPivotCounter('which')
        >>> d = c.copy()
        >>> del c[2]
        >>> c, d
        (CoolPivotCounter({1: ['c', 'i', 'w']}), CoolPivotCounter({1: ['c', 'i', 'w'], 2: ['h']}))
        >>> d[1].discard('c')
        Traceback (most recent call last):
        ...
        AttributeError: 'frozenset' object has no attribute 'discard'
        >>> c, d
        (CoolPivotCounter({1: ['c', 'i', 'w']}), CoolPivotCounter({1: ['c', 'i', 'w'], 2: ['h']}))
        >>> c == d
        False
        """
        result = CoolPivotCounter()
        for count in self:
            result[count] = self[count].copy()
        return result


if __name__ == '__main__':
    import doctest
    print doctest.testmod()

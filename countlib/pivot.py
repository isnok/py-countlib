""" Pivot table of a Counter. """
from collections import Counter

from operator import itemgetter
from heapq import nlargest, nsmallest
from itertools import repeat, ifilter


class PivotCounterBase(dict):
    """ Counter variant to act as pivot tables to Counters.
        Counts are used as keys and their keys are aggregated
        in sets as dictionary values. Where integer values make
        sense, the set sizes are used by default (most_common).

        This variant gets along without overriding __setitem__,
        since no statistics about the content are kept, yet.
        All other means of manipulating values (including init)
        are channelled through the update() method.

        The dict interface is extended by 

    >>> PivotCounter()
    PivotCounter()
    >>> PivotCounter('zyzygy')
    PivotCounter({1: ['g'], 2: ['z'], 3: ['y']})
    >>> PivotCounter(Counter('zyzygy'))
    PivotCounter({1: ['g'], 2: ['z'], 3: ['y']})
    >>> PivotCounter('lalalohoe') == PivotCounter(Counter('lalalohoe'))
    True
    >>> PivotCounter('lllaaoohe') == PivotCounter('lalalohoe')
    True
    >>> PivotCounter('lllaaoohe') == PivotCounter(set('lalalohoe'))
    False
    >>> PivotCounter('test').subtract(Counter('tst'))
    NotImplemented
    >>> PivotCounter('test').subtract(PivotCounter('tst'))
    PivotCounter({0: ['s', 't'], 1: ['e']})

    """
    __unpivot__ = Counter

    def __init__(self, iterable=None, **kwds):
        """ Create a new, empty PivotCounter object. And if given, count elements
            from an input Counter or dict. Or, initialize from another PivotCounter.

        >>> PivotCounter() == {}             # a new, empty counter
        True
        >>> PivotCounter('gallahad')         # a new counter from an iterable
        PivotCounter({1: ['d', 'g', 'h'], 2: ['l'], 3: ['a']})
        >>> PivotCounter({'a': 4, 'b': 2})   # a new counter from a mapping
        PivotCounter({2: ['b'], 4: ['a']})
        >>> PivotCounter(a=4, b=2)           # a new counter from keyword args
        PivotCounter({2: ['b'], 4: ['a']})

        """
        dict.__init__(self)
        self.update(iterable, **kwds)

    def update(self, iterable=None, **kwds):
        """ Like Counter.update() but union sets instead of adding counts.
            Source can be a dictionary or Counter instance or another PivotCounter.

        >>> d = PivotCounter('watch')
        >>> d.update('boofittii')          # add in elements via another counter-like
        >>> d                              #  v---- notice the now existing duplicate -----v
        PivotCounter({1: ['a', 'b', 'c', 'f', 'h', 't', 'w'], 2: ['o', 't'], 3: ['i']})
        >>> PivotCounter(d.unpivot())      # to fix it regenerate the PivotCounter
        PivotCounter({1: ['a', 'b', 'c', 'f', 'h', 'w'], 2: ['o'], 3: ['i', 't']})
        >>> c = PivotCounter('which')
        >>> c.update(PivotCounter('boof')) # update the dict way
        >>> c
        PivotCounter({1: ['b', 'f'], 2: ['o']})

        """
        if iterable is not None:
            if isinstance(iterable, PivotCounter):
                self.__unpivot__ = iterable.__unpivot__
                dict.update(self, iterable) # update from other PivotCounter
            elif hasattr(iterable, 'iteritems'): # assumed Counters and dicts
                self.__unpivot__ = iterable.__class__
                add_count = self.__add_count__
                add_pivot = self.__add_pivot__
                for elem, count in iterable.iteritems():
                    try: # a normal Counter entry
                        add_count(count, elem)
                    except TypeError: # another PivotCounter?
                        add_pivot(elem, count)
            else: # slow mem eater path (by now)
                self.update(Counter(iterable))
        if kwds:
            self.update(kwds)

    @classmethod
    def fromkeys(cls, iterable, v_func=None):
        """ Initialize a pivot table from an iterable delivering counts.
            The values can be constructed from the keys via the v_func argument.

        >>> PivotCounter.fromkeys('watch')
        PivotCounter({'a': [], 'c': [], 'h': [], 't': [], 'w': []})
        >>> PivotCounter.fromkeys('watchhhh')
        PivotCounter({'a': [], 'c': [], 'h': [], 't': [], 'w': []})
        >>> PivotCounter.fromkeys('not supplying a v_func means nothing.').unpivot()
        Counter()
        >>> PivotCounter.fromkeys([1,2,3], lambda n: set(range(n)))
        PivotCounter({1: [0], 2: [0, 1], 3: [0, 1, 2]})

        """
        new = cls()
        if v_func is None:
            v_func = new.__missing__
        for count in iterable:
            new[count] = v_func(count)
        return new

    def __repr__(self):
        """ Output like defaultdict or other dict variants.
            Thanks to the try-catch behaviour of the update
            method, PivotCounters can be copy-pasted.

        >>> PivotCounter('bumm')
        PivotCounter({1: ['b', 'u'], 2: ['m']})
        >>> PivotCounter({1: ['b', 'u'], 2: ['m']})
        PivotCounter({1: ['b', 'u'], 2: ['m']})

        """
        def stable_output():
            for count, elem_set in self.iteritems():
                yield '%r: %r' % (count, sorted(elem_set))

        if not self:
            return '%s()' % self.__class__.__name__
        items = ', '.join(sorted(stable_output()))
        return '%s({%s})' % (self.__class__.__name__, items)

    def __delitem__(self, elem):
        """ Like dict.__delitem__() but does not raise KeyError for missing values.

        >>> c = PivotCounter('which')
        >>> d = PivotCounter(c)
        >>> c == d
        True
        >>> del c[2]
        >>> c
        PivotCounter({1: ['c', 'i', 'w']})
        >>> c == d
        False
        >>> del c["not there"]

        """

        if elem in self:
            dict.__delitem__(self, elem)

    def most_common(self, n=None, count_func=None, reverse=False):
        """ List the n biggest bags and their counts from the most common
            to the least. If n is None, then list all bags and counts.
            The sorting can be reversed and customized via the arguments
            reverse and count_func.

        >>> p = PivotCounter('abracadabra!')
        >>> p.most_common(3)
        [(1, set(['!', 'c', 'd'])), (2, set(['r', 'b'])), (5, set(['a']))]
        >>> p.most_common(2, reverse=True)
        [(5, set(['a'])), (2, set(['r', 'b']))]
        >>> p.most_common(2, count_func=lambda i: -len(i[1]))
        [(5, set(['a'])), (2, set(['r', 'b']))]
        >>> p.most_common(2, count_func=lambda i: -len(i[1]), reverse=True)
        [(1, set(['!', 'c', 'd'])), (2, set(['r', 'b']))]

        """
        if count_func is None:
            def count_func(item):
                return len(item[1])
        if n is None:
            return sorted(self.iteritems(), key=count_func, reverse=reverse)
        if reverse:
            return nsmallest(n, self.iteritems(), key=count_func)
        else:
            return nlargest(n, self.iteritems(), key=count_func)

    def elements(self):
        """ Iterator over elements repeating each as many times as its count.
            This relies on values to be iterable and keys to be integers.

        >>> c = PivotCounter('ABCABC')
        >>> sorted(c.elements())
        ['A', 'A', 'B', 'B', 'C', 'C']

        If an element's count has been set to zero or is a negative number,
        elements() will ignore it.

        """
        for count, elem_set in self.iteritems():
            for elem in elem_set:
                for _ in repeat(None, count):
                    yield elem

    def iter_dirty(self):
        """ Iterator over the overlapping value pairs, if any.

        >>> list(PivotCounter('ABCABC').iter_dirty())
        []
        >>> a = PivotCounter('aa')
        >>> a.update(PivotCounter('a'))
        >>> list(a.iter_dirty())
        [set(['a'])]
        """
        acc = set()
        sec = acc.intersection
        add = acc.update
        for elem_set in self.itervalues():
            cur = sec(elem_set)
            if cur:
                yield cur
            add(elem_set)

    def is_clean(self):
        """ True if no values overlap. Reliably returns a boolean.

        >>> PivotCounter(range(3)).is_clean()
        True
        >>> a = PivotCounter('aa')
        >>> a.update(PivotCounter('a'))
        >>> a.is_clean()
        False
        """
        try:
            next(self.iter_dirty())
            return False
        except StopIteration:
            return True

    def unpivot(self, check=None, clean=None):
        """ Turn the PivotCounter back into a Counter.
        >>> PivotCounter().unpivot()
        Counter()
        >>> PivotCounter('ABCABC').unpivot()
        Counter({'A': 2, 'C': 2, 'B': 2})
        >>> Counter("lollofant") == PivotCounter("lollofant").unpivot()
        True
        >>> fant = PivotCounter("lollofant")
        >>> fant.unpivot(clean=True) == fant.unpivot(check=True)
        True
        >>> for x in xrange(5, 99):
        ...     fant[x] = set(['B'])
        >>> fant.unpivot(clean=True) == fant.unpivot(check=True)
        False

        """
        if clean or (check and self.is_clean()):
            counter = self.__unpivot__()
            for elem, cnt in self.unpivot_items():
                counter[elem] = cnt
            return counter
        return self.__unpivot__(self.elements())

    def unpivot_items(self):
        """ Iterator over (element, count) tuples of underlying Counter.
            This only relies on values to be iterable.

        >>> c = PivotCounter('ABCABC')
        >>> sorted(c.unpivot_items())
        [('A', 2), ('B', 2), ('C', 2)]
        >>> sorted(c.unpivot_items()) == sorted(Counter('ABCABC').items())
        True

        """
        for count, elem_set in self.iteritems():
            for elem in elem_set:
                yield (elem, count)

    def count_sets(self, count_func=len):
        """ By default, a Counter whose counts are the lengths of this
            PivotCounters sets. count_func is called once for every value
            and is required to return an integer.

        >>> p = PivotCounter('ABCABC')
        >>> p.count_sets()
        Counter({2: 3})
        >>> p.count_sets(count_func=lambda s: 20 - len(s))
        Counter({2: 17})

        """
        def iter_counts():
            for count, elem_set in self.iteritems():
                for _ in repeat(None, count_func(elem_set)):
                    yield count

        return Counter(iter_counts())


    # Multiset-style mathematical operations discussed in:
    #       Knuth TAOCP Volume II section 4.6.3 exercise 19
    #       and at http://en.wikipedia.org/wiki/Multiset
    #
    # Canonical extension to pivot tables by Konstantin Martini.
    #
    # Outputs guaranteed to only include non-empty counts.
    #
    # To strip empty sets, add-in an empty pivot counter:
    #       c += PivotCounter()

    def __add__(self, other):
        """ Add two pivots by adding the underlying Counters.
            Non-zero counts are discarded.  Not optimied, so
            keep the original ExtremeCounter around if you want
            to be faster or save memory.

        >>> PivotCounter('abbb') + PivotCounter('bcc')
        PivotCounter({1: ['a'], 2: ['c'], 4: ['b']})
        >>> PivotCounter(Counter('abbb') + Counter('bcc'))
        PivotCounter({1: ['a'], 2: ['c'], 4: ['b']})


        """
        if not isinstance(other, PivotCounter):
            return NotImplemented
        return PivotCounter(self.unpivot() + other.unpivot())

    def __sub__(self, other):
        """ Subtract the underlying Counters discarding
            non-positive counts and return a new PivotCounter.

        >>> PivotCounter('abbbc') - PivotCounter('bccd')
        PivotCounter({1: ['a'], 2: ['b']})
        >>> PivotCounter(Counter('abbbc') - Counter('bccd'))
        PivotCounter({1: ['a'], 2: ['b']})
        """
        if not isinstance(other, PivotCounter):
            return NotImplemented
        return PivotCounter(self.unpivot() - other.unpivot())

    def add(self, other):
        ''' Add the underlying Counters without discarding
            non-positive counts. Other than it's counterpart
            the Counter, a new PivotCounter is returned from this
            method.

        >>> a, b = PivotCounter('abbbc'), PivotCounter('bccd')
        >>> a.subtract(b)
        PivotCounter({-1: ['c', 'd'], 1: ['a'], 2: ['b']})
        >>> a.subtract(b).add("xxx")
        NotImplemented
        >>> a.subtract(b).add(PivotCounter("xxx"))
        PivotCounter({1: ['a'], 2: ['b'], 3: ['x']})
        '''
        if not isinstance(other, PivotCounter):
            return NotImplemented
        otherc = other.unpivot()
        result = self.unpivot()
        for k, v in otherc.iteritems():
            result[k] += v
        return PivotCounter(result)

    def subtract(self, other):
        ''' Subtract the underlying Counters without discarding
            non-positive counts. Other than it's counterpart
            the Counter, a new PivotCounter is returned from this
            method.

        >>> PivotCounter('abbbc').subtract(PivotCounter('bccd'))
        PivotCounter({-1: ['c', 'd'], 1: ['a'], 2: ['b']})
        '''
        if not isinstance(other, PivotCounter):
            return NotImplemented
        result = self.unpivot()
        result.subtract(other.unpivot())
        return PivotCounter(result)

    def __or__(self, other):
        '''Union is about the easiest to convert, but it does not
        respect the structure of the underlying Counters.

        >>> PivotCounter('abbb') | PivotCounter('bcc')
        PivotCounter({1: ['a', 'b'], 2: ['c'], 3: ['b']})

        '''
        if not isinstance(other, PivotCounter):
            return NotImplemented
        result = PivotCounter()
        for elem in set(self) | set(other):
            newcount = self[elem] | other[elem]
            if newcount:
                result[elem] = newcount
        return result

    def __and__(self, other):
        ''' Intersection leaves only the counts (keys) and
        things (sets), that have an equal count in each pivot.

        >>> PivotCounter('hello') & PivotCounter('hallo')
        PivotCounter({1: ['h', 'o'], 2: ['l']})
        >>> PivotCounter('abbb') & PivotCounter('bcc')
        PivotCounter()

        '''
        if not isinstance(other, PivotCounter):
            return NotImplemented
        result = PivotCounter()
        if len(self) < len(other):
            self, other = other, self
        for elem in ifilter(self.__contains__, other):
            newcount = self[elem] & other[elem]
            if newcount:
                result[elem] = newcount
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

    def __add_count__(self, count, elem):
        self[count] = self.get(count, frozenset()).union([elem])

    def __add_pivot__(self, count, elem_set):
        self[count] = self.get(count, frozenset()).union(elem_set)

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

    def __add_count__(self, count, elem):
        self.setdefault(count, set()).add(elem)

    def __add_pivot__(self, count, elem_set):
        self.setdefault(count, set()).update(elem_set)

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



if __name__ == '__main__':
    import doctest
    print doctest.testmod()

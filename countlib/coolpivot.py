""" Pivot table of a Counter. """
from collections import Counter

from operator import itemgetter
from heapq import nlargest, nsmallest
from itertools import repeat, ifilter

class CoolPivotCounter(dict):
    """ Counter variant to act as pivot tables to Counters.
        Counts are used as keys and their keys are aggregated
        in sets as dictionary values. Where integer values make
        sense, the set sizes are used by default (most_common).

    >>> CoolPivotCounter('zyzygy')
    CoolPivotCounter({1: ['g'], 2: ['z'], 3: ['y']})
    >>> CoolPivotCounter(Counter('zyzygy'))
    CoolPivotCounter({1: ['g'], 2: ['z'], 3: ['y']})
    >>> CoolPivotCounter('lalalohoe') == CoolPivotCounter(Counter('lalalohoe'))
    True
    >>> CoolPivotCounter('lllaaoohe') == CoolPivotCounter('lalalohoe')
    True
    >>> CoolPivotCounter('lllaaoohe') == CoolPivotCounter(frozenset('lalalohoe'))
    False

    """

    def __init__(self, iterable=None, **kwds):
        """ Create a new, empty CoolPivotCounter object. And if given, count elements
            from an input Counter or dict. Or, initialize from another CoolPivotCounter.

        >>> CoolPivotCounter() == {}             # a new, empty counter
        True
        >>> CoolPivotCounter('gallahad')         # a new counter from an iterable
        CoolPivotCounter({1: ['d', 'g', 'h'], 2: ['l'], 3: ['a']})
        >>> CoolPivotCounter({'a': 4, 'b': 2})   # a new counter from a mapping
        CoolPivotCounter({2: ['b'], 4: ['a']})
        >>> CoolPivotCounter(a=4, b=2)           # a new counter from keyword args
        CoolPivotCounter({2: ['b'], 4: ['a']})

        """
        self.update(iterable, **kwds)

    def __missing__(self, key):
        """ Create a new, empty CoolPivotCounter object. And if given, count elements
            from an input Counter or dict. Or, initialize from another CoolPivotCounter.

        >>> CoolPivotCounter()["x"]
        frozenset([])
        """
        return frozenset()

    def most_common(self, n=None, count_func=None, reverse=False):
        """ List the n biggest bags and their counts from the most common
            to the least. If n is None, then list all bags and counts.
            The sorting can be reversed and customized via the arguments
            reverse and count_func.

        >>> p = CoolPivotCounter('abracadabra!')
        >>> p.most_common(3)
        [(1, frozenset(['!', 'c', 'd'])), (2, frozenset(['r', 'b'])), (5, frozenset(['a']))]
        >>> p.most_common(2, reverse=True)
        [(5, frozenset(['a'])), (2, frozenset(['r', 'b']))]
        >>> p.most_common(2, count_func=lambda i: -len(i[1]))
        [(5, frozenset(['a'])), (2, frozenset(['r', 'b']))]
        >>> p.most_common(2, count_func=lambda i: -len(i[1]), reverse=True)
        [(1, frozenset(['!', 'c', 'd'])), (2, frozenset(['r', 'b']))]

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

        >>> c = CoolPivotCounter('ABCABC')
        >>> sorted(c.elements())
        ['A', 'A', 'B', 'B', 'C', 'C']

        If an element's count has been set to zero or is a negative number,
        elements() will ignore it.

        """
        for count, elem_set in self.iteritems():
            for elem in elem_set:
                for _ in repeat(None, count):
                    yield elem

    def unpivot(self, onerror=None):
        """ Turn the CoolPivotCounter back into a Counter.
        >>> CoolPivotCounter('ABCABC').unpivot()
        Counter({'A': 2, 'C': 2, 'B': 2})
        >>> Counter("lollofant") == CoolPivotCounter("lollofant").unpivot()
        True
        >>> CoolPivotCounter("lollofant").unpivot(onerror=True)
        Traceback (most recent call last):
        ...
        NotImplementedError: Pivot verification not (yet) implemented.

        """
        if onerror:
            "Verify, that no key overwrites happen"
            raise NotImplementedError("Pivot verification not (yet) implemented.")

        return Counter(self.elements())

    def unpivot_items(self):
        """ Iterator over (element, count) tuples of underlying Counter.
            This only relies on values to be iterable.

        >>> c = CoolPivotCounter('ABCABC')
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
            CoolPivotCounters sets. count_func is called once for every value
            and is required to return an integer.

        >>> p = CoolPivotCounter('ABCABC')
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

    @classmethod
    def fromkeys(cls, iterable, v_func=None):
        """ Initialize a pivot table from an iterable delivering counts.
            The values can be constructed from the keys via the v_func argument.

        >>> CoolPivotCounter.fromkeys('watch')
        CoolPivotCounter({'a': [], 'c': [], 'h': [], 't': [], 'w': []})
        >>> CoolPivotCounter.fromkeys('watchhhh')
        CoolPivotCounter({'a': [], 'c': [], 'h': [], 't': [], 'w': []})
        >>> CoolPivotCounter.fromkeys('not supplying a v_func means nothing.').unpivot()
        Counter()
        >>> CoolPivotCounter.fromkeys([1,2,3], lambda n: frozenset(range(n)))
        CoolPivotCounter({1: [0], 2: [0, 1], 3: [0, 1, 2]})

        """
        new = cls()
        if v_func is None:
            v_func = new.__missing__
        for count in iterable:
            new[count] = v_func(count)
        return new

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
            if isinstance(iterable, CoolPivotCounter):
                dict.update(self, iterable) # fast path when counter is empty
            elif hasattr(iterable, 'iteritems'): # assumed Counters and dicts
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

    def __delitem__(self, elem):
        """ Like dict.__delitem__() but does not raise KeyError for missing values.

        >>> c = CoolPivotCounter('which')
        >>> del c[2]
        >>> c
        CoolPivotCounter({1: ['c', 'i', 'w']})
        >>> del c["not there"]

        """

        if elem in self:
            dict.__delitem__(self, elem)

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


    def __repr__(self):
        """ Output like defaultdict or other dict variants.
            Thanks to the try-catch behaviour of the update
            method, CoolPivotCounters can be copy-pasted.

        >>> CoolPivotCounter('bumm')
        CoolPivotCounter({1: ['b', 'u'], 2: ['m']})
        >>> CoolPivotCounter({1: ['b', 'u'], 2: ['m']})
        CoolPivotCounter({1: ['b', 'u'], 2: ['m']})

        """
        def stable_output():
            for count, elem_set in self.iteritems():
                yield '%r: %r' % (count, sorted(elem_set))

        if not self:
            return '%s()' % self.__class__.__name__
        items = ', '.join(sorted(stable_output()))
        return '%s({%s})' % (self.__class__.__name__, items)


    # Multiset-style mathematical operations discussed in:
    #       Knuth TAOCP Volume II section 4.6.3 exercise 19
    #       and at http://en.wikipedia.org/wiki/Multiset
    #
    # Canonical extension to pivot tables by Konstantin Martini.
    #
    # Outputs guaranteed to only include non-empty counts.
    #
    # To strip empty sets, add-in an empty pivot counter:
    #       c += CoolPivotCounter()

    def __add__(self, other):
        '''Add two pivots by adding the underlying Counters.
        Slow by now, and may be hard to optimize.

        >>> CoolPivotCounter('abbb') + CoolPivotCounter('bcc')
        CoolPivotCounter({1: ['a'], 2: ['c'], 4: ['b']})
        >>> CoolPivotCounter(Counter('abbb') + Counter('bcc'))
        CoolPivotCounter({1: ['a'], 2: ['c'], 4: ['b']})


        '''
        if not isinstance(other, CoolPivotCounter):
            return NotImplemented
        return CoolPivotCounter(self.unpivot() + other.unpivot())

    def __sub__(self, other):
        ''' Subtract the underlying Counters.

        >>> CoolPivotCounter('abbbc') - CoolPivotCounter('bccd')
        CoolPivotCounter({1: ['a'], 2: ['b']})
        >>> CoolPivotCounter(Counter('abbbc') - Counter('bccd'))
        CoolPivotCounter({1: ['a'], 2: ['b']})
        '''
        if not isinstance(other, CoolPivotCounter):
            return NotImplemented
        return CoolPivotCounter(self.unpivot() - other.unpivot())

    def __or__(self, other):
        '''Union is about the easiest to convert, but it does not
        respect the structure of the underlying Counters.

        >>> CoolPivotCounter('abbb') | CoolPivotCounter('bcc')
        CoolPivotCounter({1: ['a', 'b'], 2: ['c'], 3: ['b']})

        '''
        if not isinstance(other, CoolPivotCounter):
            return NotImplemented
        result = CoolPivotCounter()
        for elem in frozenset(self) | frozenset(other):
            newcount = self[elem] | other[elem]
            if newcount:
                result[elem] = newcount
        return result

    def __and__(self, other):
        ''' Intersection leaves only the counts (keys) and
        things (sets), that have an equal count in each pivot.

        >>> CoolPivotCounter('hello') & CoolPivotCounter('hallo')
        CoolPivotCounter({1: ['h', 'o'], 2: ['l']})
        >>> CoolPivotCounter('abbb') & CoolPivotCounter('bcc')
        CoolPivotCounter()

        '''
        if not isinstance(other, CoolPivotCounter):
            return NotImplemented
        result = CoolPivotCounter()
        if len(self) < len(other):
            self, other = other, self
        for elem in ifilter(self.__contains__, other):
            newcount = self[elem] & other[elem]
            if newcount:
                result[elem] = newcount
        return result


if __name__ == '__main__':
    import doctest
    print doctest.testmod()

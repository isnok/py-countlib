""" Pivot table of a Counter. """
from collections import Counter

from operator import itemgetter
from heapq import nlargest, nsmallest
from itertools import repeat, ifilter

class PivotCounter(dict):
    """ Counter variant to act as pivot tables to Counters.
        Counts are used as keys and their keys are aggregated
        in sets as dictionary values. Where integer values make
        sense, the set sizes are used by default (most_common).

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

    """

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
        self.update(iterable, **kwds)

    def __missing__(self, key):
        """ Create a new, empty PivotCounter object. And if given, count elements
            from an input Counter or dict. Or, initialize from another PivotCounter.

        >>> PivotCounter()["x"]
        set([])
        """
        return set()

    def most_common(self, n=None, count_func=None, reverse=False):
        """ List the n most common elements and their counts from the most
            common to the least.  If n is None, then list all element counts.

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

    def counter_items(self):
        """ Iterator over (element, count) tuples of underlying Counter.
            This only relies on values to be iterable.

        >>> c = PivotCounter('ABCABC')
        >>> sorted(c.counter_items())
        [('A', 2), ('B', 2), ('C', 2)]

        """
        for count, elem_set in self.iteritems():
            for elem in elem_set:
                yield (elem, count)

    def unpivot(self, onerror=None):
        """ Turn the PivotCounter back into a Counter.
        >>> PivotCounter('ABCABC').unpivot()
        Counter({'A': 2, 'C': 2, 'B': 2})
        >>> Counter("lollofant") == PivotCounter("lollofant").unpivot()
        True
        >>> PivotCounter("lollofant").unpivot(onerror=True)
        Traceback (most recent call last):
        ...
        NotImplementedError: Pivot verification not (yet) implemented.

        """
        if onerror:
            "Verify, that no key overwrites happen"
            raise NotImplementedError("Pivot verification not (yet) implemented.")

        return Counter(self.elements())

    def distribution(self, count_func=len):
        """ A Counters whose counts are the lengths of my values.

        >>> p = PivotCounter('ABCABC')
        >>> p.distribution()
        Counter({2: 3})
        >>> p.distribution(count_func=lambda s: 20 - len(s))
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

        >>> PivotCounter.fromkeys('watch')
        PivotCounter({'a': [], 'h': [], 'c': [], 't': [], 'w': []})
        >>> PivotCounter.fromkeys('watchhhh')
        PivotCounter({'a': [], 'h': [], 'c': [], 't': [], 'w': []})
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
                dict.update(self, iterable) # fast path when counter is empty
            elif hasattr(iterable, 'iteritems'): # assumed Counters and dicts
                for elem, count in iterable.iteritems():
                    self.setdefault(count, set()).add(elem)
            else: # slow path (by now)
                self.update(Counter(iterable))
        if kwds:
            self.update(kwds)

    def __delitem__(self, elem):
        """ Like dict.__delitem__() but does not raise KeyError for missing values.

        >>> c = PivotCounter('which')
        >>> del c[2]
        >>> c
        PivotCounter({1: ['c', 'i', 'w']})
        >>> del c["not there"]

        """

        if elem in self:
            dict.__delitem__(self, elem)

    def copy(self):
        """ Like dict.copy() but returns a PivotCounter instance instead of a dict.
            The sets acting as values are copied as well.

        >>> c = PivotCounter('which')
        >>> d = c.copy()
        >>> del c[2]
        >>> c, d
        (PivotCounter({1: ['c', 'i', 'w']}), PivotCounter({1: ['c', 'i', 'w'], 2: ['h']}))
        >>> d[1].discard('c')
        >>> c, d
        (PivotCounter({1: ['c', 'i', 'w']}), PivotCounter({1: ['i', 'w'], 2: ['h']}))
        """
        result = PivotCounter()
        for count in self:
            result[count] = self[count].copy()
        return result


    def __repr__(self):
        """ Output like defaultdict or other dict variants.
            But copy-pasting the String will not work.

        >>> PivotCounter('bumm')
        PivotCounter({1: ['b', 'u'], 2: ['m']})
        >>> PivotCounter({1: ['b', 'u'], 2: ['m']})
        Traceback (most recent call last):
        ...
        TypeError: unhashable type: 'list'
        """
        def stable_output():
            for count, elem_set in self.iteritems():
                yield '%r: %r' % (count, sorted(elem_set))

        if not self:
            return '%s()' % self.__class__.__name__
        items = ', '.join(stable_output())
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
    #       c += PivotCounter()

    def __add__(self, other):
        '''Add two pivots by adding the underlying Counters.
        Slow by now, and may be hard to optimize.

        >>> PivotCounter('abbb') + PivotCounter('bcc')
        PivotCounter({1: ['a'], 2: ['c'], 4: ['b']})
        >>> PivotCounter(Counter('abbb') + Counter('bcc'))
        PivotCounter({1: ['a'], 2: ['c'], 4: ['b']})


        '''
        if not isinstance(other, PivotCounter):
            return NotImplemented
        return PivotCounter(self.unpivot() + other.unpivot())

    def __sub__(self, other):
        ''' Subtract the underlying Counters.

        >>> PivotCounter('abbbc') - PivotCounter('bccd')
        PivotCounter({1: ['a'], 2: ['b']})
        >>> PivotCounter(Counter('abbbc') - Counter('bccd'))
        PivotCounter({1: ['a'], 2: ['b']})
        '''
        if not isinstance(other, PivotCounter):
            return NotImplemented
        return PivotCounter(self.unpivot() - other.unpivot())

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


if __name__ == '__main__':
    import doctest
    print doctest.testmod()

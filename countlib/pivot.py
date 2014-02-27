""" Pivot table of a Counter. """
from collections import Counter

from operator import itemgetter
from heapq import nlargest
from itertools import repeat, ifilter

class PivotCounter(dict):
    '''Counter variant to act as pivot tables to Counters.
    Counts are stored as dictionary keys and their keys
    are stored in sets as dictionary values.  Where integer
    values make sense, sets are replaced by their lenght.

    >>> PivotCounter('zyzygy')
    PivotCounter({1: set(['g']), 2: set(['z']), 3: set(['y'])})
    >>> PivotCounter(Counter('zyzygy'))
    PivotCounter({1: set(['g']), 2: set(['z']), 3: set(['y'])})
    >>> PivotCounter('lalalohoe') == PivotCounter(Counter('lalalohoe'))
    True
    >>> PivotCounter('lllaaoohe') == PivotCounter('lalalohoe')
    True
    >>> PivotCounter('lllaaoohe') == PivotCounter(set('lalalohoe'))
    False

    '''

    def __init__(self, iterable=None, **kwds):
        '''Create a new, empty PivotCounter object. And if given, count elements
        from an input Counter or dict. Or, initialize from another PivotCounter.

        >>> c = PivotCounter()                   # a new, empty counter
        >>> c = PivotCounter('gallahad')         # a new counter from an iterable
        >>> c = PivotCounter({'a': 4, 'b': 2})   # a new counter from a mapping
        >>> c = PivotCounter(a=4, b=2)           # a new counter from keyword args

        '''
        self.update(iterable, **kwds)

    def __missing__(self, key):
        return set()

    def most_common(self, n=None):
        '''List the n most common elements and their counts from the most
        common to the least.  If n is None, then list all element counts.

        >>> PivotCounter('abracadabra').most_common(3)
        [('a', 5), ('r', 2), ('b', 2)]

        '''
        def get_set_len(item):
            return len(item[1])
        if n is None:
            return sorted(self.iteritems(), key=get_set_len)
        return nlargest(n, self.iteritems(), key=get_set_len)

    def elements(self):
        '''Iterator over elements repeating each as many times as its count.
        This relies on values to be iterable and keys to be integers.

        >>> c = PivotCounter('ABCABC')
        >>> sorted(c.elements())
        ['A', 'A', 'B', 'B', 'C', 'C']

        If an element's count has been set to zero or is a negative number,
        elements() will ignore it.

        '''
        for count, elem_set in self.iteritems():
            for elem in elem_set:
                for _ in repeat(None, count):
                    yield elem

    def counter_items(self):
        '''Iterator over (element, count) tuples of underlying Counter.
        This only relies on values to be iterable.

        >>> c = PivotCounter('ABCABC')
        >>> sorted(c.counter_items())
        [('A', 2), ('B', 2), ('C', 2)]

        '''
        for count, elem_set in self.iteritems():
            for elem in elem_set:
                yield (elem, count)

    def unpivot(self, onerror=None):
        'Turn back into a Counter'
        if onerror:
            raise NotImplementedError("Pivot verification not (yet) implemented.")
            "Verify, that no key overwrites happen"
        return Counter(dict(self.counter_items()))

    def counter(self):
        """ Counts are the lengths of values. """
        return Counter(dict(self.counter_items()))

    # Override dict methods where the meaning changes for Counter objects.

    #@classmethod
    #def fromkeys(cls, iterable, v=None):
        #raise NotImplementedError(
            #'Counter.fromkeys() is undefined.  Use Counter(iterable) instead.')

    def update(self, iterable=None, **kwds):
        '''Like Counter.update() but union sets instead of adding counts.

        Source can be a dictionary or Counter instance or another PivotCounter.

        >>> c = PivotCounter('which')
        >>> c.update('witch')           # add elements from another iterable
        >>> d = PivotCounter('watch')
        >>> c.update(d)                 # add elements from another counter
        >>> c['h']                      # four 'h' in which, witch, and watch
        4

        '''
        if iterable is not None:
            if isinstance(iterable, PivotCounter):
                if self:
                    self_get = self.setdefault
                    for elem, count in iterable.iteritems():
                        self[elem] = self_get(elem, set()).update(count)
                else:
                    dict.update(self, iterable) # fast path when counter is empty
            elif hasattr(iterable, 'iteritems'):
                for elem, count in iterable.iteritems():
                    self.setdefault(count, set()).add(elem)
            else: # slow path (by now)
                self.update(Counter(iterable))
        if kwds:
            self.update(kwds)

    def copy(self):
        ''' Like dict.copy() but returns a PivotCounter instance instead of a dict.
            The sets actinng as values are copied as well.
        '''
        return PivotCounter(self)


    def __delitem__(self, elem):
        'Like dict.__delitem__() but does not raise KeyError for missing values.'
        if elem in self:
            dict.__delitem__(self, elem)

    def __repr__(self):
        if not self:
            return '%s()' % self.__class__.__name__
        items = ', '.join(map('%r: %r'.__mod__, self.most_common()))
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
        PivotCounter({1: set(['a']), 2: set(['c']), 4: set(['b'])})
        >>> PivotCounter(Counter('abbb') + Counter('bcc'))
        PivotCounter({1: set(['a']), 2: set(['c']), 4: set(['b'])})


        '''
        if not isinstance(other, PivotCounter):
            return NotImplemented
        return PivotCounter(self.counter() + other.counter())

    def __sub__(self, other):
        ''' Subtract the underlying Counters.

        >>> PivotCounter('abbbc') - PivotCounter('bccd')
        PivotCounter({1: set(['a']), 2: set(['b'])})
        >>> PivotCounter(Counter('abbbc') - Counter('bccd'))
        PivotCounter({1: set(['a']), 2: set(['b'])})
        '''
        if not isinstance(other, PivotCounter):
            return NotImplemented
        return PivotCounter(self.counter() - other.counter())

    def __or__(self, other):
        '''Union is about the easiest to convert, but it does not
        respect the structure of the underlying Counters.

        >>> PivotCounter('abbb') | PivotCounter('bcc')
        PivotCounter({2: set(['c']), 3: set(['b']), 1: set(['a', 'b'])})

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
        PivotCounter({2: set(['l']), 1: set(['h', 'o'])})
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

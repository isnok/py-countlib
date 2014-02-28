""" Counters strike! """
from collections import Counter
from pivot import PivotCounter
from coolpivot import CoolPivotCounter

from operator import itemgetter
from heapq import nlargest, nsmallest
from itertools import ifilter

class ExtremeCounter(Counter):
    """ Buffed Counter class. Extreme usefulness to be expected.

    >>> ExtremeCounter('zyzygy')
    ExtremeCounter({'g': 1, 'y': 3, 'z': 2})
    >>> x = ExtremeCounter("yay? nice!! this thing works!!")
    >>> x.most_common_counts(1)
    [(' ', 4), ('!', 4)]
    >>> x.most_common_counts(1, inverse=True)
    [('a', 1), ('c', 1), ('e', 1), ('g', 1), ('k', 1), ('o', 1), ('w', 1), ('r', 1), ('?', 1)]
    >>> x.pivot()
    PivotCounter({1: ['?', 'a', 'c', 'e', 'g', 'k', 'o', 'r', 'w'], 2: ['h', 'n', 's', 't', 'y'], 3: ['i'], 4: [' ', '!']})
    >>> x.cool_pivot() == x.pivot()
    True
    >>> x.transpose()
    ExtremeCounter({1: 9, 2: 5, 3: 1, 4: 2})
    >>> y = ExtremeCounter("yay.")
    >>> y + ExtremeCounter.fromkeys('zab.', 3)
    ExtremeCounter({'.': 4, 'a': 4, 'b': 3, 'y': 2, 'z': 3})
    >>> y - ExtremeCounter.fromkeys('zab.', 3)
    ExtremeCounter({'y': 2})
    >>> y.subtract(ExtremeCounter.fromkeys('zab.', 3))
    >>> y
    ExtremeCounter({'.': -2, 'a': -2, 'b': -3, 'y': 2, 'z': -3})
    >>> y.add(ExtremeCounter.fromkeys('zab.', 3))
    >>> y
    ExtremeCounter({'.': 1, 'a': 1, 'b': 0, 'y': 2, 'z': 0})
    >>> y + Counter()
    ExtremeCounter({'.': 1, 'a': 1, 'y': 2})

    """

    def most_common(self, n=None, count_func=None, inverse=False):
        """ List the n most common elements and their counts from the most
            common to the least.  If n is None, then list all element counts.
            The way counting is done can be customized via the count_func
            argument, that is passed to the sorting as the key function.


        >>> p = ExtremeCounter('abracadabra!')
        >>> p.most_common(3)
        [('a', 5), ('b', 2), ('r', 2)]
        >>> p.most_common(2, inverse=True)
        [('!', 1), ('c', 1)]
        >>> p.most_common(2, count_func=lambda i: -i[1])
        [('!', 1), ('c', 1)]
        >>> p.most_common(2, count_func=lambda i: -i[1], inverse=True)
        [('a', 5), ('b', 2)]

        """
        if count_func is None:
            count_func = itemgetter(1)
        if n is None:
            return sorted(self.iteritems(), key=count_func, reverse=not inverse)
        if inverse:
            return nsmallest(n, self.iteritems(), key=count_func)
        else:
            return nlargest(n, self.iteritems(), key=count_func)


    def most_common_counts(self, n, *args, **kw):
        """ Get all items with the n highest counts.
            Much like most_common but limit is applied to values (counts).

        >>> x = ExtremeCounter("yay? nice!! this thing works!")
        >>> x.update("etsttseststttsetsetse ")
        >>> x.most_common_counts(1)
        [('t', 11)]
        >>> x.most_common_counts(5)
        [('t', 11), ('s', 9), ('e', 6), (' ', 5), ('i', 3), ('!', 3)]

        """
        def limit_most_common(limit):
            for elem, count in self.most_common(*args, **kw):
                if not "last_count" in locals():
                    last_count = count
                else:
                    if count != last_count:
                        limit -= 1
                        last_count = count
                if limit <= 0:
                    break
                yield (elem, count)

        return list(limit_most_common(n))

    def pivot(self):
        """ The pivot table of the Counter.

        >>> x = ExtremeCounter("yay? nice!! this thing works!")
        >>> x.update("etsttseststttsetsetse ")
        >>> x.transpose().pivot()
        PivotCounter({1: [5, 6, 9, 11], 2: [3], 3: [2], 8: [1]})
        >>> x.pivot() + x.pivot()
        PivotCounter({10: [' '], 12: ['e'], 18: ['s'], 22: ['t'], 2: ['?', 'a', 'c', 'g', 'k', 'o', 'r', 'w'], 4: ['h', 'n', 'y'], 6: ['!', 'i']})
        >>> ExtremeCounter("lollofant!!").pivot() - ExtremeCounter("trollofant").pivot()
        PivotCounter({1: ['l'], 2: ['!']})
        >>> ExtremeCounter("lollofant!!").pivot() + ExtremeCounter("trollofant").pivot()
        PivotCounter({1: ['r'], 2: ['!', 'a', 'f', 'n'], 3: ['t'], 4: ['o'], 5: ['l']})
        """
        return PivotCounter(self)

    def cool_pivot(self):
        """ Cool pivot table of the Counter.

        >>> x = ExtremeCounter("yay? nice!! this thing works!")
        >>> x.update("etsttseststttsetsetse ")
        >>> x.transpose().cool_pivot()
        CoolPivotCounter({1: [5, 6, 9, 11], 2: [3], 3: [2], 8: [1]})
        >>> x.cool_pivot() + x.cool_pivot()
        CoolPivotCounter({10: [' '], 12: ['e'], 18: ['s'], 22: ['t'], 2: ['?', 'a', 'c', 'g', 'k', 'o', 'r', 'w'], 4: ['h', 'n', 'y'], 6: ['!', 'i']})
        >>> ExtremeCounter("lollofant!!").cool_pivot() - ExtremeCounter("trollofant").cool_pivot()
        CoolPivotCounter({1: ['l'], 2: ['!']})
        >>> ExtremeCounter("lollofant!!").cool_pivot() + ExtremeCounter("trollofant").cool_pivot()
        CoolPivotCounter({1: ['r'], 2: ['!', 'a', 'f', 'n'], 3: ['t'], 4: ['o'], 5: ['l']})
        """
        return CoolPivotCounter(self)

    def transpose(self):
        """ Use my counts as keys, and as values the list of elements,
            that have that count.

        >>> x = ExtremeCounter("yay? nice!! this thing works!")
        >>> x.update("etsttseststttsetsetse ")
        >>> old_x = None
        >>> while old_x != x:
        ...     old_x = x
        ...     x = x.transpose()
        ...     print old_x
        ExtremeCounter({' ': 5, '!': 3, '?': 1, 'a': 1, 'c': 1, 'e': 6, 'g': 1, 'h': 2, 'i': 3, 'k': 1, 'n': 2, 'o': 1, 'r': 1, 's': 9, 't': 11, 'w': 1, 'y': 2})
        ExtremeCounter({11: 1, 1: 8, 2: 3, 3: 2, 5: 1, 6: 1, 9: 1})
        ExtremeCounter({1: 4, 2: 1, 3: 1, 8: 1})
        ExtremeCounter({1: 3, 4: 1})
        ExtremeCounter({1: 1, 3: 1})
        ExtremeCounter({1: 2})
        ExtremeCounter({2: 1})
        ExtremeCounter({1: 1})
        """
        return ExtremeCounter(self.itervalues())

    @classmethod
    def fromkeys(cls, iterable, v=0):
        """ Init a constant Counter. Useful for Counter arithmetic.

        >>> ExtremeCounter.fromkeys('bumm')
        ExtremeCounter({'b': 0, 'm': 0, 'u': 0})
        >>> x = ExtremeCounter.fromkeys('bumm', 50)
        >>> x
        ExtremeCounter({'b': 50, 'm': 50, 'u': 50})
        >>> x + x
        ExtremeCounter({'b': 100, 'm': 100, 'u': 100})
        >>> x + x == ExtremeCounter.fromkeys(x, 50+50)
        True
        """
        return cls(dict.fromkeys(iterable, v))

    def __repr__(self):
        """ Output like defaultdict or other dict variants.
            Of course ExtremeCounters can be copy-pasted.

        >>> ExtremeCounter('bumm')
        ExtremeCounter({'b': 1, 'm': 2, 'u': 1})
        >>> ExtremeCounter({'b': 1, 'm': 2, 'u': 1})
        ExtremeCounter({'b': 1, 'm': 2, 'u': 1})
        >>> for stuff in ('abc', 'bcccnnno', (12,12,3,4,5,3,3)):
        ...     x = ExtremeCounter(stuff)
        ...     print x == eval(repr(x))
        True
        True
        True

        """
        def stable_output():
            for elem, count in self.iteritems():
                yield '%r: %r' % (elem, count)

        if not self:
            return '%s()' % self.__class__.__name__
        items = ', '.join(sorted(stable_output()))
        return '%s({%s})' % (self.__class__.__name__, items)


    # Multiset-style mathematical operations discussed in:
    #       Knuth TAOCP Volume II section 4.6.3 exercise 19
    #       and at http://en.wikipedia.org/wiki/Multiset
    #
    # Outputs guaranteed to only include positive counts.
    # To strip negative and zero counts, add-in an empty counter:
    #
    #       c += ExtremeCounter()

    def __add__(self, other):
        """ Union the keys, add the counts.

        >>> ExtremeCounter('abbb') + ExtremeCounter('bcc')
        ExtremeCounter({'a': 1, 'b': 4, 'c': 2})
        >>> ExtremeCounter('abbb') + Counter('bcc')
        ExtremeCounter({'a': 1, 'b': 4, 'c': 2})
        >>> ExtremeCounter('aaa') + ExtremeCounter.fromkeys('a', -1)
        ExtremeCounter({'a': 2})
        >>> ExtremeCounter('aaa') + ExtremeCounter.fromkeys('a', -3)
        ExtremeCounter()

        """
        if not isinstance(other, Counter):
            return NotImplemented
        result = ExtremeCounter()
        for elem in set(self) | set(other):
            newcount = self[elem] + other[elem]
            if newcount > 0:
                result[elem] = newcount
        return result

    def __sub__(self, other):
        """ Subtract count, but keep only results with positive counts.

        >>> ExtremeCounter('abbbc') - ExtremeCounter('bccd')
        ExtremeCounter({'a': 1, 'b': 2})
        >>> ExtremeCounter('abbbc') - Counter('bccd')
        ExtremeCounter({'a': 1, 'b': 2})

        """
        if not isinstance(other, Counter):
            return NotImplemented
        result = ExtremeCounter()
        for elem in set(self) | set(other):
            newcount = self[elem] - other[elem]
            if newcount > 0:
                result[elem] = newcount
        return result

    def add(self, other):
        """ Add in Counts without discarding non-positive.
            The (strangely missing) eqivalent of Counter.subtract.
            Iteration is limited to the key set of other, so default
            values that are not iterated over will be skipped.

        >>> a = ExtremeCounter('abbb')
        >>> a
        ExtremeCounter({'a': 1, 'b': 3})
        >>> a.add(ExtremeCounter('bcc'))
        >>> a
        ExtremeCounter({'a': 1, 'b': 4, 'c': 2})
        >>> a + ExtremeCounter.fromkeys('ab', -12)
        ExtremeCounter({'c': 2})
        >>> a.add(ExtremeCounter.fromkeys('ab', -12))
        >>> a
        ExtremeCounter({'a': -11, 'b': -8, 'c': 2})
        >>> a.add(a)
        >>> a.subtract(a)
        >>> a
        ExtremeCounter({'a': 0, 'b': 0, 'c': 0})

        """
        if not isinstance(other, Counter):
            return NotImplemented
        for elem in set(other):
            self[elem] += other[elem]

    def __or__(self, other):
        """ Union is the maximum of value in either of the input counters.

        >>> ExtremeCounter('abbb') | ExtremeCounter('bcc')
        ExtremeCounter({'a': 1, 'b': 3, 'c': 2})
        >>> ExtremeCounter('abbb') | Counter('bcc')
        ExtremeCounter({'a': 1, 'b': 3, 'c': 2})

        """
        if not isinstance(other, Counter):
            return NotImplemented
        _max = max
        result = ExtremeCounter()
        for elem in set(self) | set(other):
            newcount = _max(self[elem], other[elem])
            if newcount > 0:
                result[elem] = newcount
        return result

    def __and__(self, other):
        """ Intersection is the minimum of corresponding counts.

        >>> ExtremeCounter('abbb') & ExtremeCounter('bcc')
        ExtremeCounter({'b': 1})
        >>> ExtremeCounter('abbb') & Counter('bcc')
        ExtremeCounter({'b': 1})
        >>> Counter('abbb') & ExtremeCounter('bcc')
        Counter({'b': 1})

        """
        if not isinstance(other, Counter):
            return NotImplemented
        _min = min
        result = ExtremeCounter()
        if len(self) < len(other):
            self, other = other, self
        for elem in ifilter(self.__contains__, other):
            newcount = _min(self[elem], other[elem])
            if newcount > 0:
                result[elem] = newcount
        return result

if __name__ == '__main__':
    import doctest
    print doctest.testmod()

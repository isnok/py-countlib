""" Counters strike! """
from collections import Counter
from pivot import PivotCounter

from operator import itemgetter
from heapq import nlargest, nsmallest

class ExtremeCounter(Counter):
    """ Buffed Counter class. Extreme usefulness to be expected.

    >>> ExtremeCounter('zyzygy')
    ExtremeCounter({'g': 1, 'y': 3, 'z': 2})
    >>> x = ExtremeCounter("yay? nice!! this thing works!!")
    >>> x.most_common_counts(1)
    [(' ', 4), ('!', 4)]
    >>> x.most_common_counts(1, inverse=True)
    [('a', 1), ('c', 1), ('e', 1), ('g', 1), ('k', 1), ('o', 1), ('w', 1), ('r', 1), ('?', 1)]

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

    def pivold(self):
        """ return the pivot table as a counter  """
        pivot = ListCounter()
        for elem, count in self.iteritems():
            if count in pivot:
                pivot[count].append(elem)
            else:
                pivot[count] = [elem]
        return pivot

    @classmethod
    def fromkeys(cls, iterable, v=0):
        """ Init a constant Counter. Useful for Counter arithmetic. """
        return cls(dict.fromkeys(iterable, v))

    def __repr__(self):
        """ Output like defaultdict or other dict variants.
            Of course ExtremeCounters can be copy-pasted.

        >>> ExtremeCounter('bumm')
        ExtremeCounter({'b': 1, 'm': 2, 'u': 1})
        >>> ExtremeCounter({'b': 1, 'm': 2, 'u': 1})
        ExtremeCounter({'b': 1, 'm': 2, 'u': 1})

        """
        def stable_output():
            for elem, count in self.iteritems():
                yield '%r: %r' % (elem, count)

        if not self:
            return '%s()' % self.__class__.__name__
        items = ', '.join(sorted(stable_output()))
        return '%s({%s})' % (self.__class__.__name__, items)

class ListCounter(Counter):
    """ A Counter that uses list instead of int objects to count. """

    def __missing__(self, key):
        return []


if __name__ == '__main__':
    import doctest
    print doctest.testmod()

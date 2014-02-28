""" Counters strike! """
from collections import Counter
from pivot import PivotCounter

from operator import itemgetter
from heapq import nlargest, nsmallest

class ExtremeCounter(Counter):
    """ Buffed Counter class. Extreme usefulness to be expected.

    >>> ExtremeCounter('zyzygy')
    ExtremeCounter({'g': 1, 'z': 2, 'z': 3})
    >>> x = ExtremeCounter("yay? nice!! this thing works!!")
    >>> x.most_common_counts(1)
    [(' ', 4), ('!', 4)]
    >>> x.most_common_counts(1, reverse=True)
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
        >>> p.most_common(2, reverse=True)
        [('!', 1), ('c', 1)]
        >>> p.most_common(2, count_func=lambda i: -i[1])
        [('!', 1), ('c', 1)]
        >>> p.most_common(2, count_func=lambda i: -i[1], inverse=True)
        [('!', 1), ('c', 1)]

        """
        if count_func is None:
            count_func = itemgetter(1)
        if n is None:
            return sorted(self.iteritems(), key=count_func, reverse=not inverse)
        if inverse:
            return nsmallest(n, self.iteritems(), key=count_func)
        else:
            return nlargest(n, self.iteritems(), key=count_func)


    def iter_most_common_counts(self, limit, *args, **kw):
        for thing, count in self.most_common(*args, **kw):
            if "last_count" in locals():
                if count != last_count:
                    limit -= 1
                    last_count = count
            else:
                last_count = count
            if limit <= 0:
                break
            yield (thing, count)

    def most_common_counts(self, *args, **kw):
        """ get the most common counts as a list of (elem, cnt) tuples.
            like most_common() but limit is applied to values (counts) """
        return list(self.iter_most_common_counts(*args, **kw))

    def pivot(self):
        return PivotCounter(self)

    def pivot_counter(self):
        return ExtremeCounter(self.itervalues())

    def pivold(self):
        """ return the pivot table as a counter  """
        pivot = ListCounter()
        for thing, count in self.iteritems():
            if count in pivot:
                pivot[count].append(thing)
            else:
                pivot[count] = [thing]
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

    x = ExtremeCounter("yay? nice!! this thing works!")
    x.update("etsttseststttsetsetse ")
    print x.most_common_counts(1)
    print x.most_common_counts(5)
    print x.pivot_counter().pivot()
    print x.pivot() + x.pivot()
    ExtremeCounter("lollofant!!").pivot() - ExtremeCounter("trollofant").pivot()
    ExtremeCounter("lollofant!!").pivot() + ExtremeCounter("trollofant").pivot()


""" Counters strike! """
from collections import Counter
from pivot import PivotCounter

from operator import itemgetter
from heapq import nlargest, nsmallest
from itertools import ifilter

class ExtremeCounter(Counter):
    """ Buffed Counter class. Extreme usefulness to be expected.
    """
    __pivot__ = PivotCounter

    def most_common(self, n=None, count_func=None, inverse=False):
        """ List the n most common elements and their counts from the most
            common to the least.  If n is None, then list all element counts.
            The way counting is done can be customized via the count_func
            argument, that is passed to the sorting as the key function.
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

        return list(limit_most_common(n)) # don't keep whole list

    def pivot(self, cls=None):
        """ The pivot table of the Counter.
        """
        if cls:
            return cls(self)
        return self.__pivot__(self)

    def transpose(self):
        """ Use my counts as keys, and as values the list of elements,
            that have that count.
        """
        return ExtremeCounter(self.itervalues())

    @classmethod
    def fromkeys(cls, iterable, v=0):
        """ Init a constant Counter. Useful for Counter arithmetic.
        """
        return cls(dict.fromkeys(iterable, v))

    def __repr__(self):
        """ Output like defaultdict or other dict variants.
            Of course ExtremeCounters can be copy-pasted.
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
        """
        if not isinstance(other, Counter):
            return NotImplemented
        for elem in set(other):
            self[elem] += other[elem]

    def __or__(self, other):
        """ Union is the maximum of value in either of the input counters.
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

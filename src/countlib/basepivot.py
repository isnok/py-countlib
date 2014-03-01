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

        The dict interface is extended by some operations
        resembling Counter behaviour which means that negative
        and zero counts are stripped.
    """

    __unpivot__ = Counter

    def __init__(self, iterable=None, **kwds):
        """ Create a new, empty PivotCounter object. And if given, count elements
            from an input Counter or dict. Or, initialize from another PivotCounter.
        """

        dict.__init__(self)
        self.update(iterable, **kwds)

    def update(self, iterable=None, **kwds):
        raise NotImplementedError()

    @classmethod
    def fromkeys(cls, iterable, v_func=None):
        """ Initialize a pivot table from an iterable delivering counts.
            The values can be constructed from the keys via the v_func argument.
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
        """

        if elem in self:
            dict.__delitem__(self, elem)

    def most_common(self, n=None, count_func=None, reverse=False):
        """ List the n biggest bags and their counts from the most common
            to the least. If n is None, then list all bags and counts.
            The sorting can be reversed and customized via the arguments
            reverse and count_func.
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
            If an element's count has been set to zero or is a negative number,
            elements() will ignore it.
        """

        for count, elem_set in self.iteritems():
            for elem in elem_set:
                for _ in repeat(None, count):
                    yield elem

    def iter_dirty(self):
        """ Iterator over the overlapping value pairs, if any.
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
        """

        try:
            next(self.iter_dirty())
            return False
        except StopIteration:
            return True

    def unpivot(self, check=None, clean=None):
        """ Turn the PivotCounter back into a Counter.
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
        """

        for count, elem_set in self.iteritems():
            for elem in elem_set:
                yield (elem, count)

    def count_sets(self, count_func=len):
        """ By default, a Counter whose counts are the lengths of this
            PivotCounters sets. count_func is called once for every value
            and is required to return an integer.
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
        """
        if not isinstance(other, PivotCounterBase):
            return NotImplemented
        return self.__class__(self.unpivot() + other.unpivot())

    def __sub__(self, other):
        """ Subtract the underlying Counters discarding
            non-positive counts and return a new PivotCounter.
        """
        if not isinstance(other, PivotCounterBase):
            return NotImplemented
        return self.__class__(self.unpivot() - other.unpivot())

    def add(self, other):
        """ Add the underlying Counters without discarding
            non-positive counts. Other than it's counterpart
            the Counter, a new PivotCounter is returned from this
            method.
        """
        if not isinstance(other, PivotCounterBase):
            return NotImplemented
        otherc = other.unpivot()
        result = self.unpivot()
        for k, v in otherc.iteritems():
            result[k] += v
        return self.__class__(result)

    def subtract(self, other):
        """ Subtract the underlying Counters without discarding
            non-positive counts. Other than it's counterpart
            the Counter, a new PivotCounter is returned from this
            method.
        """
        if not isinstance(other, PivotCounterBase):
            return NotImplemented
        result = self.unpivot()
        result.subtract(other.unpivot())
        return self.__class__(result)

    def __or__(self, other):
        """ Union is about the easiest to convert, but it does not
            respect the structure of the underlying Counters.
        """
        if not isinstance(other, PivotCounterBase):
            return NotImplemented
        result = self.__class__()
        for elem in set(self) | set(other):
            newcount = self[elem] | other[elem]
            if newcount:
                result[elem] = newcount
        return result

    def __and__(self, other):
        """ Intersection leaves only the counts (keys) and
            things (sets), that have an equal count in each pivot.
        """
        if not isinstance(other, PivotCounterBase):
            return NotImplemented
        result = self.__class__()
        if len(self) < len(other):
            self, other = other, self
        for elem in ifilter(self.__contains__, other):
            newcount = self[elem] & other[elem]
            if newcount:
                result[elem] = newcount
        return result


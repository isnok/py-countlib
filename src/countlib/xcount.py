""" Counters strike! """
from collections import Counter
from collections import Mapping
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


    def most_common_counts(self, n, *args, **kwd):
        """ Get all items with the n highest counts.
            Much like most_common but limit is applied to values (counts).
        """
        def limit_most_common(limit):
            for elem, count in self.most_common(*args, **kwd):
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

    def __neg__(self):
        """ Negate all counts. Don't strip any.
        """
        result = self.__class__()
        for key, value in self.iteritems():
            result[key] = -value
        return result

    def __add__(self, other):
        """ Union the keys, add the counts, skip if <= 0.
        """
        result = self.__class__()
        if not isinstance(other, Mapping):
            for elem, count in self.items():
                result[elem] = count + other
            return result
        for elem, count in self.items():
            newcount = count + other[elem]
            if newcount > 0:
                result[elem] = newcount
        for elem, count in other.items():
            if elem not in self and count > 0:
                result[elem] = 0 + count
        return result

    def __sub__(self, other):
        """ Subtract count, but keep only results with positive counts.
        """
        result = self.__class__()
        if not isinstance(other, Mapping):
            for elem, count in self.items():
                result[elem] = count - other
            return result
        for elem, count in self.items():
            newcount = count - other[elem]
            if newcount > 0:
                result[elem] = newcount
        for elem, count in other.items():
            if elem not in self and count < 0:
                result[elem] = 0 - count
        return result

    def add(self, iterable=None, **kwds):
        """ Add in Counts without discarding non-positive.
            The (strangely missing) eqivalent of Counter.subtract.
            Iteration is limited to the key set of other, so default
            values that are not iterated over will be skipped.
        """
        if iterable is not None:
            self_get = self.get
            if isinstance(iterable, Mapping):
                for elem, count in iterable.items():
                    self[elem] = self_get(elem, 0) + count
            else:
                for elem in iterable:
                    self[elem] = self_get(elem, 0) + 1
        if kwds:
            self.add(kwds)

    def subtract(self, iterable=None, **kwds):
        """ Like dict.update() but subtracts counts instead of replacing them.
            Counts can be reduced below zero.  Both the inputs and outputs are
            allowed to contain zero and negative counts.

            Source can be an iterable, a dictionary, or another Counter instance.
        """
        if iterable is not None:
            self_get = self.get
            if isinstance(iterable, Mapping):
                for elem, count in iterable.items():
                    self[elem] = self_get(elem, 0) - count
            else:
                for elem in iterable:
                    self[elem] = self_get(elem, 0) - 1
        if kwds:
            self.subtract(kwds)

    def __mul__(self, other):
        """ Multiply elementwise on the intersection of keys, if the other is a Mapping,
            otherwise multiply all counts with other (in that order, to allow magic).
            Strip out zero and negative counts only if other is a Mapping.
        """
        result = self.__class__()

        if not isinstance(other, Mapping):
            for elem, count in self.items():
                result[elem] = count * other
            return result

        for elem, count in self.items():
            if not count or elem not in other:
                continue
            newcount = count * other[elem]
            if newcount > 0:
                result[elem] = newcount
        return result

    def __div__(self, other):
        """ Divide elementwise on the intersection of keys if other is a Mapping.
            If not, divide all counts with other (in that order, to allow magic).
            Zero or negative counts are only stripped if other is a Mapping.
        """
        result = self.__class__()

        if not isinstance(other, Mapping):
            for elem, count in self.items():
                result[elem] = count / other
            return result

        for elem, count in self.items():
            if elem not in other:
                continue
            newcount = count / other[elem]
            if newcount > 0:
                result[elem] = newcount
        return result

    def __floordiv__(self, other):
        """ Floordivide elements on the intersection of keys if other is a Mapping.
            If not, divide all counts with other (in that order, to allow magic).
            Zero or negative counts are only stripped if other is a Mapping.
        """
        result = self.__class__()

        if not isinstance(other, Mapping):
            for elem, count in self.items():
                result[elem] = count // other
            return result

        for elem, count in self.items():
            if elem not in other:
                continue
            newcount = count // other[elem]
            if newcount > 0:
                result[elem] = newcount
        return result

    def __pow__(self, other):
        """ Exponentiate elements on own keys (base), if other (exponent) is a Mapping.
            If not, exponentiate all counts with other (in that order, to allow magic).
            Zero or negative counts are not stripped since they are rarely results
            of exponentiation (and as such probably interesting to keep when they show up).
        """
        result = self.__class__()
        if not isinstance(other, Mapping):
            for elem, count in self.items():
                result[elem] = count ** other
            return result
        for elem, count in self.items():
            newcount = count ** other[elem]
            if newcount > 0:
                result[elem] = newcount
        return result

    def __mod__(self, other):
        """ Modulo elementwise on the intersection of keys if other is a Mapping.
            If not, modulo all counts with other (in that order, to allow magic).
            Zero counts are kept (since they make sense in modulo arithmetics).
        """
        result = self.__class__()

        if not isinstance(other, Mapping):
            for elem, count in self.items():
                result[elem] = count % other
            return result

        for elem, count in self.items():
            if elem not in other:
                continue
            newcount = count % other[elem]
            result[elem] = newcount
        return result

    def __or__(self, other):
        """ Union is the maximum of value in either of the input counters.
        """
        result = self.__class__()
        if not isinstance(other, Mapping):
            _max = max
            for elem, count in self.items():
                result[elem] = _max(count, other)
            return result
        for elem, count in self.items():
            other_count = other[elem]
            newcount = other_count if count < other_count else count
            if newcount > 0:
                result[elem] = newcount
        for elem, count in other.items():
            if elem not in self and count > 0:
                result[elem] = count
        return result

    def __and__(self, other):
        """ Intersection is the minimum of corresponding counts.
        """
        result = self.__class__()
        _min = min
        if not isinstance(other, Mapping):
            for elem, count in self.items():
                result[elem] = _min(count, other)
            return result
        if len(self) < len(other):
            self, other = other, self
        for elem in ifilter(self.__contains__, other):
            newcount = _min(self[elem], other[elem])
            if newcount > 0:
                result[elem] = newcount
        return result
""" Counters strike! """
from collections import Mapping
from pivot import PivotCounter

from itertools import chain, repeat, starmap
from operator import itemgetter
from heapq import nlargest, nsmallest

class AdvancedCounter(dict):
    """ Buffed Counter class. Advanced usefulness to be expected.
    """
    # cache methods for fast lookup
    __getitem__ = dict.__getitem__
    setdefault = dict.setdefault
    update = dict.update

    def __init__(self, iterable=None, **kwds):
        '''Create a new, empty Counter object.  And if given, count elements
        from an input iterable.  Or, initialize the count from another mapping
        of elements to their counts.

        '''
        super(AdvancedCounter, self).__init__()
        self.add(iterable, **kwds)

    def elements(self):
        '''Iterator over elements repeating each as many times as its count.

        >>> c = Counter('ABCABC')
        >>> sorted(c.elements())
        ['A', 'A', 'B', 'B', 'C', 'C']

        # Knuth's example for prime factors of 1836:  2**2 * 3**3 * 17**1
        >>> prime_factors = Counter({2: 2, 3: 3, 17: 1})
        >>> product = 1
        >>> for factor in prime_factors.elements():     # loop over factors
        ...     product *= factor                       # and multiply them
        >>> product
        1836

        Note, if an element's count has been set to zero or is a negative
        number, elements() will ignore it.

        '''
        # Emulate Bag.do from Smalltalk and Multiset.begin from C++.
        return chain.from_iterable(starmap(repeat, self.iteritems()))

    def __missing__(self, key):
        """ The count of elements not in the Counter is zero.
            Implemented so that self[missing_item] does not raise KeyError
            Also, the key is not inserted into the counter 'on read'.
        """
        return 0

    def __reduce__(self):
        """ To be dumpable via the pickle module. """
        return self.__class__, (dict(self),)

    def __delitem__(self, elem):
        """ Like dict.__delitem__() but does not raise KeyError for missing values.
        """
        if elem in self:
            super(AdvancedCounter, self).__delitem__(elem)

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

    def transpose(self):
        """ Use my counts as keys, and as values the list of elements,
            that have that count.
        """
        return self.__class__(self.itervalues())

    @classmethod
    def fromkeys(cls, iterable, v=0):
        """ Init a constant Counter. Useful for Counter arithmetic.
        """
        return cls(dict.fromkeys(iterable, v))

    def copy(self):
        'Return a shallow copy.'
        return self.__class__(self)

    def __str__(self):
        """ Output like defaultdict or other dict variants.
            Of course AdvancedCounters can be copy-pasted.
        """
        def stable_output():
            return map('%r: %r'.__mod__, sorted(self.items()))

        if not self:
            return '%s()' % self.__class__.__name__
        items = ', '.join(stable_output())
        return '%s({%s})' % (self.__class__.__name__, items)

    def __repr__(self):
        """ Output like defaultdict or other dict variants.
            Of course AdvancedCounters can be copy-pasted.
        """
        def just_output():
            return map('%r: %r'.__mod__, self.items())

        if not self:
            return '%s()' % self.__class__.__name__
        items = ', '.join(just_output())
        return '%s({%s})' % (self.__class__.__name__, items)

    def __neg__(self):
        """ Negate all counts. Don't strip any.
        """
        result = self.__class__()
        for key, value in self.iteritems():
            result[key] = -value
        return result

    def __abs__(self):
        """ Absolute of all counts. None are stripped.
        """
        result = self.__class__()
        _abs = abs
        for key, value in self.iteritems():
            result[key] = abs(value)
        return result

    def __pos__(self):
        """ Positive of all counts. Negative and zero outcomes are stripped.
        """
        result = self.__class__()
        for key, value in self.iteritems():
            newcount = +value
            if newcount > 0:
                result[key] = newcount
        return result

    def __invert__(self):
        """ Pass round to all values.
        """
        result = self.__class__()
        for elem, count in self.items():
            result[elem] = ~count
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
                result[elem] = count
        return result

    __radd__ = __add__ # commutative

    def __iadd__(self, other):
        """ Union the keys, add the counts, skip if <= 0.
        """
        if not isinstance(other, Mapping):
            for elem in self.keys():
                self[elem] += other
            return self
        for elem, count in self.items():
            newcount = count + other[elem]
            if newcount > 0:
                self[elem] = newcount
            else:
                del self[elem]
        for elem, count in other.items():
            if elem not in self and count > 0:
                self[elem] = count
        return self

    def __sub__(self, other):
        """ Subtract count, but keep only results with positive counts.
        """
        result = self.__class__()
        if not isinstance(other, Mapping):
            for elem, count in self.items():
                result[elem] = count - other
            return result
        for elem, count in other.items():
            if elem in self:
                newcount = self[elem] - count
                if newcount > 0:
                    result[elem] = newcount
            else:
                if count > 0 or not count:
                    continue
                else:
                    result[elem] = -count
        for elem, count in self.items():
            if count > 0 and elem not in other:
                result[elem] = count
        return result

    def __rsub__(self, other):
        """ Subtraction is not commutative.
        """
        result = self.__class__()
        if not isinstance(other, Mapping):
            for elem, count in self.items():
                result[elem] = other - count
            return result
        for elem, count in self.items():
            if elem in other:
                newcount = other[elem] - count
                if newcount > 0:
                    result[elem] = newcount
        for elem, count in other.items():
            if elem not in self and count > 0:
                result[elem] = count
        return result

    def __isub__(self, other):
        """ Subtract count, but keep only results with positive counts.
        """
        if not isinstance(other, Mapping):
            for elem in self.keys():
                self[elem] -= other
            return self
        for elem, count in other.items():
            if elem not in self:
                if count > 0: # don't compare other than gt 0
                    del self[elem]
                elif not count:
                    pass
                else:
                    self[elem] = -count
            else:
                newcount = count - other[elem]
                if newcount > 0:
                    self[elem] = newcount
                else:
                    del self[elem]
        for elem, count in self.items():
                if not count > 0:
                    del self[elem]
        return self

    def add(self, iterable=None, **kwds):
        '''Like dict.update() but add counts instead of replacing them.

        Source can be an iterable, a dictionary, or another Counter instance.

        >>> c = Counter('which')
        >>> c.update('witch')           # add elements from another iterable
        >>> d = Counter('watch')
        >>> c.update(d)                 # add elements from another counter
        >>> c['h']                      # four 'h' in which, witch, and watch
        4

        '''
        # The regular dict.update() operation makes no sense here because the
        # replace behavior results in the some of original untouched counts
        # being mixed-in with all of the other counts for a mismash that
        # doesn't have a straight-forward interpretation in most counting
        # contexts.  Instead, we implement straight-addition.  Both the inputs
        # and outputs are allowed to contain zero and negative counts.

        if iterable is not None:
            if isinstance(iterable, Mapping):
                if self:
                    self_get = self.get
                    for elem, count in iterable.iteritems():
                        self[elem] = self_get(elem, 0) + count
                else:
                    super(AdvancedCounter, self).update(iterable) # fast path when counter is empty
            else:
                self_get = self.get
                for elem in iterable:
                    self[elem] = self_get(elem, 0) + 1
        if kwds:
            self.add(kwds)

    #def add(self, iterable=None, **kwds):
        #""" Add in Counts without discarding non-positive.
            #The (strangely missing) eqivalent of Counter.subtract.
            #Iteration is limited to the key set of other, so default
            #values that are not iterated over will be skipped.
        #"""
        #if iterable is not None:
            #self_get = self.get
            #if isinstance(iterable, Mapping):
                #for elem, count in iterable.items():
                    #self[elem] = self_get(elem, 0) + count
            #else:
                #for elem in iterable:
                    #self[elem] = self_get(elem, 0) + 1
        #if kwds:
            #self.add(kwds)

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

    __rmul__ = __mul__ # commutative

    def __imul__(self, other):
        """ Multiply elementwise on the intersection of keys, if the other is a Mapping,
            otherwise multiply all counts with other (in that order, to allow magic).
            Strip out zero and negative counts only if other is a Mapping.
        """
        if not isinstance(other, Mapping):
            for elem in self.keys():
                self[elem] *= other
            return self

        for elem, count in self.items():
            if count and (elem in other):
                newcount = count * other[elem]
                if newcount > 0:
                    self[elem] = newcount
                else:
                    del self[elem]
        return self

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

    def __rdiv__(self, other):
        """ Divide elementwise on the intersection of keys if other is a Mapping.
            If not, divide all counts with other (in that order, to allow magic).
            Zero or negative counts are only stripped if other is a Mapping.
            This is the second version of this non-commutative operation.
        """
        result = self.__class__()

        if not isinstance(other, Mapping):
            for elem, count in self.items():
                result[elem] = other / count
            return result

        for elem, count in self.items():
            if elem not in other:
                continue
            newcount = other[elem] / count
            if newcount > 0:
                result[elem] = newcount
        return result

    def __idiv__(self, other):
        """ Divide elementwise on the intersection of keys if other is a Mapping.
            If not, divide all counts with other (in that order, to allow magic).
            Zero or negative counts are only stripped if other is a Mapping.
        """

        if not isinstance(other, Mapping):
            for elem in self.keys():
                self[elem] /= other
            return self

        for elem, count in self.items():
            if elem in other:
                newcount = count / other[elem]
                if newcount > 0:
                    self[elem] = newcount
                else:
                    del self[elem]
        return self

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

    def __rfloordiv__(self, other):
        """ Floordivide elements on the intersection of keys if other is a Mapping.
            If not, divide all counts with other (in that order, to allow magic).
            Zero or negative counts are only stripped if other is a Mapping.
        """
        result = self.__class__()

        if not isinstance(other, Mapping):
            for elem, count in self.items():
                result[elem] = other // count
            return result

        for elem, count in self.items():
            if elem not in other:
                continue
            newcount = other[elem] // count
            if newcount > 0:
                result[elem] = newcount
        return result

    def __ifloordiv__(self, other):
        """ Floordivide elements on the intersection of keys if other is a Mapping.
            If not, divide all counts with other (in that order, to allow magic).
            Zero or negative counts are only stripped if other is a Mapping.
        """

        if not isinstance(other, Mapping):
            for elem, count in self.items():
                self[elem] //= other
            return self

        for elem, count in self.items():
            if elem not in other:
                continue
            newcount = count // other[elem]
            if newcount > 0:
                self[elem] = newcount
            else:
                del self[elem]
        return self

    def __truediv__(self, other):
        """ Assuming how this works...
        """
        result = self.__class__()

        if not isinstance(other, Mapping):
            for elem, count in self.items():
                result[elem] = float(count) / other
            return result

        for elem, count in self.items():
            if elem not in other:
                continue
            newcount = float(count) / other[elem]
            if newcount > 0:
                result[elem] = newcount
        return result

    def __rtruediv__(self, other):
        """ Not exactly sure how this works...
        """
        result = self.__class__()

        if not isinstance(other, Mapping):
            for elem, count in self.items():
                result[elem] = other / float(count)
            return result

        for elem, count in self.items():
            if elem not in other:
                continue
            newcount = other[elem] / float(count)
            if newcount > 0:
                result[elem] = newcount
        return result

    def __itruediv__(self, other):
        """ Assuming how this should work...
        """
        if not isinstance(other, Mapping):
            for elem, count in self.items():
                self[elem] = float(count) / other
            return self

        for elem, count in self.items():
            if elem not in other:
                continue
            newcount = float(count) / other[elem]
            if newcount > 0:
                self[elem] = newcount
            else:
                del self[elem]
        return self

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

    def __rpow__(self, other):
        """ Exponentiate using own elements as exponents.
        """
        result = self.__class__()
        if not isinstance(other, Mapping):
            for elem, count in self.items():
                result[elem] = other ** count
            return result
        for elem, count in self.items():
            newcount = other[elem] ** count
            if newcount > 0:
                result[elem] = newcount
        return result

    def __ipow__(self, other):
        """ Exponentiate elements on own keys (base), if other (exponent) is a Mapping.
            If not, exponentiate all counts with other (in that order, to allow magic).
            Zero or negative counts are not stripped since they are rarely selfs
            of exponentiation (and as such probably interesting to keep when they show up).
        """
        if not isinstance(other, Mapping):
            for elem in self.keys():
                self[elem] **= other
            return self
        for elem, count in self.items():
            newcount = count ** other[elem]
            if newcount > 0:
                self[elem] = newcount
            else:
                del self[elem]
        return self

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
            if elem in other:
                newcount = count % other[elem]
                result[elem] = newcount
        return result

    def __rmod__(self, other):
        """ Modulo elementwise on the intersection of keys if other is a Mapping.
            If not, modulo all counts with other (in that order, to allow magic).
            Zero counts are kept (since they make sense in modulo arithmetics).
            Second variant, of this non-commutative operation.
        """
        result = self.__class__()

        if not isinstance(other, Mapping):
            for elem, count in self.items():
                result[elem] = other % count
            return result

        for elem, count in self.items():
            if elem in other:
                newcount = other[elem] % count
                result[elem] = newcount
        return result

    def __imod__(self, other):
        """ Modulo elementwise on the intersection of keys if other is a Mapping.
            If not, modulo all counts with other (in that order, to allow magic).
            Zero counts are kept (since they make sense in modulo arithmetics).
        """
        if not isinstance(other, Mapping):
            for elem in self.keys():
                self[elem] %= other
            return self

        for elem, count in self.items():
            if elem in other:
                self[elem] %= other[elem]
            else:
                del self[elem]
        return self

    def __or__(self, other):
        """ Union is the maximum of value in either of the input counters.
            Calculation needs to be done on the union of keys.
        """
        result = self.__class__()
        if not isinstance(other, Mapping):
            _max = max
            for elem, count in self.items():
                result[elem] = _max(count, other)
            return result
        for elem, count in self.items():
            if elem in other:
                other_count = other[elem]
                newcount = other_count if count < other_count else count
                if newcount > 0:
                    result[elem] = newcount
            elif count > 0:
                result[elem] = count
        for elem, count in other.items():
            if count > 0 and elem not in self:
                result[elem] = count
        return result

    __ror__ = __or__

    def __ior__(self, other):
        """ Union is the maximum of value in either of the input counters.
            Calculation needs to be done on the union of keys.
        """
        if not isinstance(other, Mapping):
            _max = max
            for elem, count in self.items():
                self[elem] = _max(count, other)
            return self
        for elem, count in other.items():
            if elem not in self:
                if count > 0:
                    self[elem] = count
            else:
                self_count = self[elem]
                if count > self_count:
                    self[elem] = count
                elif self_count > 0:
                    pass
                else:
                    del self[elem]
        for elem, count in self.items():
            if count <= 0: #and elem not in other: <- we just made that sure
                del self[elem]
        return self

    def __and__(self, other):
        """ Intersection is the minimum of corresponding counts.
            Calculation is only done on the intersection of keys
            if the other is a mapping.
        """
        result = self.__class__()
        if not isinstance(other, Mapping):
            _min = min
            for elem, count in self.items():
                result[elem] = _min(count, other)
            return result

        for elem, count in self.items():
            if elem in other:
                other_count = other[elem]
                newcount = count if count < other_count else other_count
                if newcount > 0:
                    result[elem] = newcount
        return result

    __rand__ = __and__

    def __iand__(self, other):
        """ Intersection is the minimum of corresponding counts.
            Calculation is only done on the intersection of keys
            if the other is a mapping.
        """
        if not isinstance(other, Mapping):
            _min = min
            for elem, count in self.items():
                self[elem] = _min(count, other)
            return self

        for elem, count in self.items():
            if elem in other:
                other_count = other[elem]
                if not other_count > 0:
                    del self[elem]
                elif other_count < count:
                    self[elem] = other_count
                elif not count > 0:
                    del self[elem]
                else: # count is correct
                    pass
            elif not count > 0:
                del self[elem]
        return self

    def __xor__(self, other):
        """ Elementwise xor with stripping on both key sets
            if other is a Mapping, without if other is treated
            as a constant.

            We implemented a commutative behaviuor for xor,
            so the fastest and savest way to archieve same
            beaviour is copying the methond to __rxor__.
        """
        result = self.__class__()
        if not isinstance(other, Mapping):
            for elem, count in self.items():
                result[elem] = count ^ other
            return result

        for elem, count in self.items():
            if elem in other:
                newcount = count ^ other[elem]
                if newcount > 0:
                    result[elem] = newcount
            elif count > 0:
                result[elem] = count
        for elem, count in other.items():
            if elem not in self and count > 0:
                result[elem] = count
        return result

    __rxor__ = __xor__

    def __ixor__(self, other):
        """ Elementwise xor with stripping on both key sets
            if other is a Mapping, without if other is treated
            as a constant.

            We implemented a commutative behaviuor for xor,
            so the fastest and savest way to archieve same
            beaviour is copying the methond to __rxor__.
        """
        if not isinstance(other, Mapping):
            for elem in self.keys():
                self[elem] ^= other
            return self

        for elem, count in other.items():
            if elem in self:
                newcount = self[elem] ^ count
                if newcount > 0:
                    self[elem] = newcount
                else:
                    del self[elem]
        for elem, count in self.items():
            if count < 0:# and elem not in other:
                del self[elem]
        return self

    def __rshift__(self, other):
        """ Shift own keys by the value of other's key if other is a Mapping
            throwing out non-positives. Don't throw out, if other is not a mapping.
        """
        result = self.__class__()
        if not isinstance(other, Mapping):
            for elem, count in self.items():
                result[elem] = count >> other
            return result
        for elem, count in self.items():
            if elem not in other:
                result[elem] = count
            else:
                newcount = count >> other[elem]
                if newcount > 0:
                    result[elem] = newcount
        return result

    def __rrshift__(self, other):
        """ Shift own keys by the value of other's key if other is a Mapping
            throwing out non-positives. Don't throw out, if other is not a mapping.
            Second version of non-commutative operation.
        """
        result = self.__class__()
        if not isinstance(other, Mapping):
            for elem, count in self.items():
                result[elem] = other >> count
            return result
        for elem, count in self.items():
            if elem not in other:
                result[elem] = count
            else:
                newcount = other[elem] >> count
                if newcount > 0:
                    result[elem] = newcount
        return result

    def __irshift__(self, other):
        """ Shift own keys by the value of other's key if other is a Mapping
            throwing out non-positives. Don't throw out, if other is not a mapping.
        """
        if not isinstance(other, Mapping):
            for elem in self.keys():
                self[elem] >>= other
            return self
        for elem, count in self.items():
            if elem not in other:
                self[elem] = count
            else:
                newcount = count >> other[elem]
                if newcount > 0:
                    self[elem] = newcount
                else:
                    del self[elem]
        return self

    def __lshift__(self, other):
        """ Shift own keys by the value of other's key if other is a Mapping
            throwing out non-positives. Don't throw out, if other is not a mapping.
        """
        result = self.__class__()
        if not isinstance(other, Mapping):
            for elem, count in self.items():
                result[elem] = count << other
            return result
        for elem, count in self.items():
            if elem not in other:
                result[elem] = count
            else:
                newcount = count << other[elem]
                if newcount > 0:
                    result[elem] = newcount
        return result

    def __rlshift__(self, other):
        """ Shift own keys by the value of other's key if other is a Mapping
            throwing out non-positives. Don't throw out, if other is not a mapping.
            Second version of non-commutative operation.
        """
        result = self.__class__()
        if not isinstance(other, Mapping):
            for elem, count in self.items():
                result[elem] = other << count
            return result
        for elem, count in self.items():
            if elem not in other:
                result[elem] = count
            else:
                newcount = other[elem] << count
                if newcount > 0:
                    result[elem] = newcount
        return result

    def __ilshift__(self, other):
        """ Shift own keys by the value of other's key if other is a Mapping
            throwing out non-positives. Don't throw out, if other is not a mapping.
        """
        if not isinstance(other, Mapping):
            for elem in self.keys():
                self[elem] <<= other
            return self
        for elem, count in self.items():
            if elem not in other:
                self[elem] = count
            else:
                newcount = count << other[elem]
                if newcount > 0:
                    self[elem] = newcount
                else:
                    del self[elem]
        return self

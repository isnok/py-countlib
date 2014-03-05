""" Counterstrike! """
from collections import Mapping
from pivot import PivotCounter

from itertools import chain, repeat, starmap
from operator import itemgetter
from heapq import nlargest, nsmallest

class VectorDict(dict):
    """ Buffed Counter class. Basically every key introduces a new dimension.
        (Advanced) Counter features are are available, though some renamed.
    """
    # cache methods for fast lookup
    __getitem__ = dict.__getitem__
    setdefault = dict.setdefault
    update = dict.update

    def __init__(self, iterable=None, **kwds):
        ''' Create a new, empty Counter object.  And if given, count elements
            from an input iterable.  Or, initialize the count from another
            mapping of elements to their counts.

        '''
        super(VectorDict, self).__init__()
        self.count(iterable, **kwds)

    def count(self, iterable=None, **kwds):
        ''' Like dict.update() but add counts instead of replacing them.
            Source can be an iterable, a dictionary, or another Counter
            instance.

        '''
        if iterable is not None:
            if isinstance(iterable, Mapping):
                if self:
                for elem, count in iterable.items():
                    self[elem] = self_get(elem, 0) + count
                else:
                    super(VectorDict, self).update(iterable)
            else:
                self_get = self.get
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

    def __getitem__(self, key):
        """ Get a component, or subvector, if sliced.
            Getting and deleting via slices is supported.
            Setting items via slicing makes little sense, since one counted item
            has only one count, and thus cannot be assigned a range of counts.
            If slicing recieves a step of None, then it will return an ExtremeCounter
            with only the keys, whoes values lie in the requested slicing range.
            Currently only one other step arument is implemented:
            If step is -1, then the slicing range is inverted.
        """
        try:
            return dict.__getitem__(self, key)
        except TypeError, ex:
            if ex.message == "unhashable type" and isinstance(key, slice):
                start, stop, step = key.start, key.stop, key.step
                if step is None:
                    if start is not None and stop is not None:
                        return self.__class__(**dict([ i for i in self.iteritems() if start <= i[1] < stop ]))
                    if start is not None and stop is None:
                        return self.__class__(**dict([ i for i in self.iteritems() if start <= i[1] ]))
                    if start is None and stop is not None:
                        return self.__class__(**dict([ i for i in self.iteritems() if i[1] < stop ]))
                    if start is None and stop is None:
                        return self.copy()
                elif step == -1:
                    if start is not None and stop is not None:
                        return self.__class__(**dict([ i for i in self.iteritems() if not start <= i[1] < stop ]))
                    if start is not None and stop is None:
                        return self.__class__(**dict([ i for i in self.iteritems() if not start <= i[1] ]))
                    if start is None and stop is not None:
                        return self.__class__(**dict([ i for i in self.iteritems() if not i[1] < stop ]))
                    if start is None and stop is None:
                        return self.__class__()
                raise KeyError(key)
            raise ex
        raise KeyError(key)


    def __delitem__(self, key):
        """ Like dict.__delitem__() but does not raise KeyError for missing values.
            Also this supports slicing by values (counts).
        """
        try:
            if key in self:
                dict.__delitem__(self, key)
        except TypeError, ex:
            if ex.message == 'unhashable type' and isinstance(key, slice):
                start, stop, step = key.start, key.stop, key.step
                if step is None:
                    if start is not None and stop is not None:
                        for k, v in [ i for i in self.iteritems() if start <= i[1] < stop ]:
                            dict.__delitem__(self, k)
                    if start is not None and stop is None:
                        for k, v in [ i for i in self.iteritems() if start <= i[1] ]:
                            dict.__delitem__(self, k)
                    if start is None and stop is not None:
                        for k, v in [ i for i in self.iteritems() if i[1] < stop ]:
                            dict.__delitem__(self, k)
                    if start is None and stop is None:
                        for k in self.keys():
                            dict.__delitem__(self, k)
                elif step == -1:
                    if start is not None and stop is not None:
                        for k, v in [ i for i in self.iteritems() if not start <= i[1] < stop ]:
                            dict.__delitem__(self, k)
                    if start is not None and stop is None:
                        for k, v in [ i for i in self.iteritems() if not start <= i[1] ]:
                            dict.__delitem__(self, k)
                    if start is None and stop is not None:
                        for k, v in [ i for i in self.iteritems() if not i[1] < stop ]:
                            dict.__delitem__(self, k)
                    if start is None and stop is None:
                        pass

    def maximal_items(self, n=None, count_func=None, inverse=False):
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


    def maximal_values_items(self, n, count_func=None, inverse=False):
        """ Get all items with the n highest counts.
            Looks like maximal_items but limit is applied to values (counts).
            n cannot be omitted (use maximal_items without n instead), but all

        """
        def limit_most_common(limit):
            for elem, count in self.most_common(count_func=count_func, inverse=inverse):
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
            Of course VectorDicts can be copy-pasted.
        """
        def stable_output():
            return map('%r: %r'.__mod__, sorted(self.items()))

        if not self:
            return '%s()' % self.__class__.__name__
        items = ', '.join(stable_output())
        return '%s({%s})' % (self.__class__.__name__, items)

    def __repr__(self):
        """ Output like defaultdict or other dict variants.
            Of course VectorDicts can be copy-pasted.
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
        for elem, count in self.iteritems():
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
            if elem in other:
                result[elem] = count + other[elem]
            else:
                result[elem] = count
        for elem, count in other.items():
            if elem not in self:
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
        for elem, count in other.items():
            if elem in self:
                self[elem] += count
            else:
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
        for elem, count in self.items():
            if elem in other:
                result[elem] = self[elem] - count
            else:
                result[elem] = count
        for elem, count in other.items():
            if elem not in self:
                result[elem] = -count
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
                result[elem] = other[elem] - count
            else:
                result[elem] = -count
        for elem, count in other.items():
            if elem not in self:
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
            if elem in self:
                self[elem] -= count
            else:
                self[elem] = -count
        return self

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

        for elem, count in other.items():
            if elem in self:
                result[elem] = self[elem] * count
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

        for elem, count in other.items():
            if elem in self:
                self[elem] *= count
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

        for elem, count in other.items():
            if elem in other:
                result[elem] = self[elem] / count
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

        for elem, count in other.items():
            if elem in self:
                result[elem] = count / self[elem]
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

        for elem, count in other.items():
            if elem in self:
                self[elem] /= count
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

        for elem, count in other.items():
            if elem in self:
                result[elem] = self[elem] // count
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

        for elem, count in other.items():
            if elem in self:
                result[elem] = count // self[elem]
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

        for elem, count in other.items():
            if elem in self:
                self[elem] //= count
        return self

    def __truediv__(self, other):
        """ Assuming how this works...
        """
        result = self.__class__()

        if not isinstance(other, Mapping):
            for elem, count in self.items():
                result[elem] = float(count) / other
            return result

        for elem, count in other.items():
            if elem in self:
                result[elem] = float(self[elem]) / count
        return result

    def __rtruediv__(self, other):
        """ Not exactly sure how this works...
        """
        result = self.__class__()

        if not isinstance(other, Mapping):
            for elem, count in self.items():
                result[elem] = other / float(count)
            return result

        for elem, count in other.items():
            if elem in self:
                result[elem] = count / float(self[elem])
        return result

    def __itruediv__(self, other):
        """ Assuming how this should work...
        """
        if not isinstance(other, Mapping):
            for elem, count in self.items():
                self[elem] = float(count) / other
            return self

        for elem, count in other.items():
            if elem in self:
                self[elem] = float(self[elem]) / count
        return self

    def __pow__(self, other):
        """ Exponentiate elements on own keys (base), if other (exponent) is a Mapping.
            If not, exponentiate all counts with other (in that order, to allow magic).
            Result keys are restricted to the intersection of operand keys.
        """
        result = self.__class__()
        if not isinstance(other, Mapping):
            for elem, count in self.items():
                result[elem] = count ** other
            return result
        for elem, count in other.items():
            if elem in self:
                result[elem] = self[elem] ** count
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
            if elem in other:
                result[elem] = other[elem] ** count
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
            if elem in other:
                self[elem] = count ** other[elem]
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
                result[elem] = other_count if count < other_count else count
            else:
                result[elem] = count
        for elem, count in other.items():
            if elem not in self:
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

        for elem, count in self.items():
            if elem in other:
                other_count = other[elem]
                self[elem] = other if count < other_count else count
            else:
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
                result[elem] =  count if count < other_count else other_count
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
                self[elem] = count if count < other_count else other_count
            else:
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
                result[elem] = count ^ other[elem]
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

        for elem, count in self.items():
            if elem in other:
                self[elem] = count ^ other[elem]
            else:
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
            if elem in other:
                result[elem] = result[elem] >> count
            else:
                del self[elem]
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
            if elem in other:
                result[elem] = count
            else:
                newcount = other[elem] >> count
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
            if elem in other:
                newcount = count >> other[elem]
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
            if elem in other:
                newcount = count << other[elem]
                self[elem] = newcount
            else:
                del self[elem]
        return self

""" Counters strike! """
from collections import Counter
from pivot import PivotCounter

class ExtremeCounter(Counter):

    def iter_most_common_counts(self, limit, *args, **kw):
        """ like most_common() but limit is applied to values (counts) """
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
        """ get the most common counts as a list of (elem, cnt) tuples """
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


class ListCounter(Counter):
    """ A Counter that uses list instead of int objects to count. """

    def __missing__(self, key):
        return []

if __name__ == "__main__":
    x = ExtremeCounter("yay? nice!! this thing works!")
    print x.most_common_counts(1)
    x.update("etsttseststttsetsetse ")
    print x.most_common_counts(1)
    print x.most_common_counts(5)
    print x.pivot_counter().pivot()
    print x.pivot() + x.pivot()
    ExtremeCounter("lollofant!!").pivot() - ExtremeCounter("trollofant").pivot()
    ExtremeCounter("lollofant!!").pivot() + ExtremeCounter("trollofant").pivot()


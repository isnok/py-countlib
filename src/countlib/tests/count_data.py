import pytest

import string

from countlib import AdvancedCounter
from countlib import ExtremeCounter

count_data_fixtures = {}

##
#  Counter Implementations to be tested
##

advanced_counters = (AdvancedCounter, ExtremeCounter)

count_data_fixtures.update({
    "TestCounter"     : advanced_counters,
})

##
#  Iterables
##

@pytest.fixture
def test_generator():
    return (x for x in "test haha tst hehehe")

test_strings = (
    "abc", "abcabc", "abcbcc",
    "vnuiabve;uerv nvao;vna!!",
    "lalalladrhg",
    ".hehehax.".join(list("lolllomat")),
    string.letters, string.ascii_letters,
)
test_lists = (
    range(3), list("bads"), list("multikulti"),
    [ frozenset([n]) for n in range(14)],
    [ frozenset(), frozenset(["h"]), frozenset() ] * 9,
)
test_tuples = (
    tuple("baaam"), tuple("zooom"),
    tuple(range(12) * 4 + range(3,8)),
)
test_sets = (
    set(["fii", "beer"]),
    frozenset("testomat"),
)
test_dicts = (
    {"foo": 2, "bar": 5, "lol": -1},
    {"arg": 0, "neg": -199, "pos": 213872},
    {"foo": 1<<123, "bar": -(1<<89), "lol": 103},
)
test_listlikes = test_strings + test_lists + test_tuples
test_iterables = test_strings + test_lists + test_tuples + test_sets + test_dicts

count_data_fixtures.update({
    "test_string"     : test_strings,
    "test_list"       : test_lists,
    "test_tuple"      : test_tuples,
    "test_set"        : test_sets,
    "test_dict"       : test_dicts,
    "test_listlike"   : test_listlikes,
    "test_iterable"   : test_iterables,
})

@pytest.fixture
def test_counter(TestCounter, test_iterable):
    return TestCounter(test_iterable)


test_keys = (
    "a", "abc",
    0, 1, 2, -1,
    0.3, 1<<100,
    frozenset(), frozenset(["bam"]),
)


count_data_fixtures.update({
    "test_key": test_keys
})


##
#  to be deprecated
##

@pytest.fixture
def cnt_abc(TestCounter):
    return advanced_counters[TestCounter == AdvancedCounter]("abc")

@pytest.fixture
def cnt_ab2(TestCounter):
    return advanced_counters[TestCounter == AdvancedCounter]("abcabbcccddeefgggggghiii")

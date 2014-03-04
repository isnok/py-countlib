import pytest

def test_opchar(TestCounter, TestCounters, elementwise_binop, left_operand, right_operand):
    t = TestCounter()
    t[1] = left_operand
    x = eval("t %s %s" % (elementwise_binop, right_operand))
    assert x[1] == eval('%s %s %s' % (left_operand, elementwise_binop, right_operand))

def test_op(TestCounter, TestCounters, binop):
    char, fname, op_func, op_emul = binop
    t = TestCounter("aabcccdde")
    r = TestCounter("cddeeefgg")
    try:
        x = op_func(t, r)
    except Exception, ex:
        try:
            for c in "abcdefgh":
                op_emul(t[c], r[c])
            assert False
        except Exception, ex2:
            assert type(ex) == type(ex2)
            assert ex.message == ex2.message

    assert "h" not in x

    for c in "abcdefg":
        try:
            xe = op_emul(t[c], r[c])
        except Exception, ex:
            if (c not in r) or (c not in t) and (char in "//"):
                xe = 0
            else:
                raise ex
        if char == "^":
            assert (c in x) == (r[c] != t[c])
            assert xe == x[c]
        elif char in ("%",):
            assert (c in x) == (c in r and c in t)
            assert xe == x[c]
        elif char in ("|",):
            assert (c in x) == ((c in r) or (c in t) and xe == x[c])
        elif char == "&":
            assert (c in x) == ((c in r) and (c in t))
            assert xe == x[c]
        elif xe > 0:
            assert c in x
            assert xe == x[c]
        else:
            assert c not in x

def test_scalar_op(TestCounter, TestCounters, binop, right_operand):
    char, fname, op_func, op_emul = binop
    t = TestCounter("aabcccdde")
    for c in "abcde":
        try:
            x = op_func(t, right_operand)
            assert x[c] == op_emul(t[c], right_operand)
        except Exception, ex:
            try:
                op_emul(t[c], right_operand)
                assert False
            except Exception, ex2:
                assert type(ex) == type(ex2)
                assert ex.message == ex2.message
            assert False


def test_inplace_op(binop, cnt_abc):
    """ Test misses count > 0 drops."""
    char, fname, op_func, op_emul = binop
    fname = "__i" + fname[2:]
    cnt_inp = cnt_abc.copy()
    assert hasattr(cnt_inp, fname)
    getattr(cnt_inp, fname)(1)
    emu = op_emul(1,1)
    assert sorted(cnt_inp.keys()) == sorted(cnt_abc.keys())
    assert sorted(set(cnt_inp.values())) == [emu]
    getattr(cnt_inp, fname)(cnt_abc)
    try:
        double_op = op_emul(op_emul(1,1),1)
        if char != "^":
            double_op = max(0, double_op)
        if double_op:
            assert sorted(cnt_inp.keys()) == sorted(cnt_abc.keys())
            assert sorted(set(cnt_inp.values())) == [double_op]
        else:
            if char == "%":
                assert cnt_inp == cnt_inp.__class__.fromkeys(cnt_abc.keys())
            else:
                assert not cnt_inp
    except ZeroDivisionError:
        if char in "//":
            assert not cnt_inp
        elif char == "%":
            assert cnt_inp == cnt_inp.__class__.fromkeys(cnt_abc.keys())
        else:
            assert False

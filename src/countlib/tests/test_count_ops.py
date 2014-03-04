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
        except Exception, ex2:
            assert type(ex) == type(ex2)
            assert ex.message == ex2.message

    assert "h" not in x

    for c in "abcdefg":
        xc = x[c]
        try:
            xe = op_emul(t[c], r[c])
        except Exception, ex:
            if c not in r or c not in t and char in "//":
                continue
            else:
                raise ex
        if xe != xc:
            if char != "~":
                xe = max(0, xe)
        assert xe == xc

def test_scalar_op(TestCounter, TestCounters, binop, right_operand):
    char, fname, op_func, op_emul = binop
    t = TestCounter("aabcccdde")
    try:
        x = op_func(t, right_operand)
    except Exception, ex:
        try:
            for c in "abcde":
                op_emul(t[c], right_operand)
            assert False
        except Exception, ex2:
            assert type(ex) == type(ex2)
            assert ex.message == ex2.message

    for c in "abcde":
        assert x[c] == op_emul(t[c], right_operand)

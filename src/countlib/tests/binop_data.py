import pytest
import operator

binop_data_fixtures = {}

binops = (
    ("+",  "__add__",      operator.add,      operator.add,       ),
    ("-",  "__sub__",      operator.sub,      operator.sub,       ),
    ("*",  "__mul__",      operator.mul,      operator.mul,       ),
    ("/",  "__div__",      operator.div,      operator.div,       ),
    ("//", "__floordiv__", operator.floordiv, operator.floordiv,  ),
    (None, "__truediv__",  operator.truediv,  operator.truediv,   ),
    ("**", "__pow__",      operator.pow,      operator.pow,       ),
    ("%",  "__mod__",      operator.mod,      operator.mod,       ),
    ("|",  "__or__",       operator.or_,      max,                ),
    ("&",  "__and__",      operator.and_,     min,                ),
    ("^",  "__xor__",      operator.xor,      operator.xor,       ),
    (">>", "__rshift__",   operator.rshift,   operator.rshift,    ),
    ("<<", "__lshift__",   operator.lshift,   operator.lshift,    ),
)
binop_chars = ( "+", "-", "*", "/", "//", "**", "%", "|", "&", "^", ">>", "<<" )
elementwise_binops = ( "+", "-", "*", "/", "//", "**", "%", "^", ">>", "<<" )
binop_chars = {
    "+": "__add__",
    "-": "__sub__",
    "*": "__mul__",
    "/": "__div__",
    "//": "__floordiv__",
    "**": "__pow__",
    "%": "__mod__",
    "|": "__or__",
    "&": "__and__",
    "^": "__xor__",
    ">>": "__rshift__",
    "<<": "__lshift__",
}

binop_data_fixtures.update({
    "elementwise_binop" : elementwise_binops,
    "binop"             : binops
})


left_operands = tuple(range(1,10,2))
right_operands = left_operands

binop_data_fixtures.update({
    "left_operand"  : left_operands,
    "right_operand" : right_operands,
})


from sloperator.lexer import tokenize
from sloperator.parser import parse
from sloperator.parser.ast import Call, ExprStmt, Literal, Variable
from sloperator.runner import run_source


def test_nested_call_ast_shape():
    (statement,) = parse(tokenize("hallucinate(add(1, 2))✨"))
    assert isinstance(statement, ExprStmt)

    outer = statement.expression
    assert isinstance(outer, Call)
    assert isinstance(outer.callee, Variable)
    assert outer.callee.name.lexeme == "hallucinate"
    assert len(outer.arguments) == 1

    (inner,) = outer.arguments
    assert isinstance(inner, Call)
    assert isinstance(inner.callee, Variable)
    assert inner.callee.name.lexeme == "add"
    left, right = inner.arguments
    assert isinstance(left, Literal) and isinstance(right, Literal)
    assert (left.value, right.value) == (1, 2)


def test_call_as_argument_to_another_call():
    source = """clanker add(left, right) {
    ship left + right✨
}
hallucinate(add(1, 2))✨"""
    result = run_source(source)
    assert (result.stdout, result.stderr, result.exit_code) == ("3\n", "", 0)

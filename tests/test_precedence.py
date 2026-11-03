from sloperator.lexer import TokenType, tokenize
from sloperator.parser import parse
from sloperator.parser.ast import Binary, ExprStmt
from sloperator.runner import run_source


def test_multiplication_binds_tighter_than_addition():
    (statement,) = parse(tokenize("1 + 2 * 3✨"))
    assert isinstance(statement, ExprStmt)

    expression = statement.expression
    assert isinstance(expression, Binary)
    assert expression.operator.type is TokenType.PLUS
    assert isinstance(expression.right, Binary)
    assert expression.right.operator.type is TokenType.STAR

    result = run_source("hallucinate(1 + 2 * 3)✨")
    assert (result.stdout, result.stderr) == ("7\n", "")

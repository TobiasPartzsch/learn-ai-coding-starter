import pytest

from sloperator.lexer import TokenType, tokenize
from sloperator.parser import parse
from sloperator.parser.ast import Binary, ExprStmt, Literal
from sloperator.runner import run_source


def test_comparison_binds_tighter_than_equality():
    (statement,) = parse(tokenize("1 < 2 == ✅✨"))
    assert isinstance(statement, ExprStmt)

    expression = statement.expression
    assert isinstance(expression, Binary)
    assert expression.operator.type is TokenType.EQUAL_EQUAL
    assert isinstance(expression.left, Binary)
    assert expression.left.operator.type is TokenType.LESS
    assert isinstance(expression.right, Literal)
    assert expression.right.value is True

    result = run_source("hallucinate(1 < 2 == ✅)✨")
    assert (result.stdout, result.stderr) == ("✅\n", "")


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("1 < 2", "✅"),
        ("2 < 1", "❌"),
        ("2 <= 2", "✅"),
        ("3 <= 2", "❌"),
        ("3 > 2", "✅"),
        ("2 > 3", "❌"),
        ("2 >= 2", "✅"),
        ("1 >= 2", "❌"),
    ],
)
def test_comparison_operators(expression: str, expected: str):
    result = run_source(f"hallucinate({expression})✨")
    assert (result.stdout, result.stderr) == (f"{expected}\n", "")


def test_equality_has_lower_precedence_than_comparison():
    result = run_source("hallucinate(1 == 1 < 2)✨")
    assert (result.stdout, result.stderr) == ("❌\n", "")

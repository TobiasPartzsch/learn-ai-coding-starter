import pytest

from sloperator.errors import SlopSyntaxError
from sloperator.lexer import Token, TokenType, tokenize
from sloperator.parser import parse
from sloperator.parser.ast import Assign, Binary, Literal, Variable


def parse_source(source: str):
    return parse(tokenize(source))


def test_plus_equal_is_a_single_token():
    assert tokenize("+=") == [
        Token(TokenType.PLUS_EQUAL, "+=", None, 1),
        Token(TokenType.EOF, "", None, 1),
    ]


def test_plus_equal_is_greedy_without_whitespace():
    assert [token.type for token in tokenize("x+=1")] == [
        TokenType.IDENTIFIER,
        TokenType.PLUS_EQUAL,
        TokenType.NUMBER,
        TokenType.EOF,
    ]


def test_plus_without_equal_is_still_plus():
    assert [token.type for token in tokenize("x + 1")] == [
        TokenType.IDENTIFIER,
        TokenType.PLUS,
        TokenType.NUMBER,
        TokenType.EOF,
    ]


def test_compound_assignment_is_an_assign_statement():
    (statement,) = parse_source("x += 1✨")
    assert isinstance(statement, Assign)
    assert statement.name.lexeme == "x"
    assert statement.operator.type is TokenType.PLUS_EQUAL
    assert isinstance(statement.value, Literal) and statement.value.value == 1


def test_compound_assignment_value_is_a_full_expression():
    (statement,) = parse_source("x += 1 + 2 * 3✨")
    assert isinstance(statement, Assign)
    assert isinstance(statement.value, Binary)
    assert statement.value.operator.type is TokenType.PLUS
    assert isinstance(statement.value.left, Literal) and statement.value.left.value == 1
    assert isinstance(statement.value.right, Binary)
    assert statement.value.right.operator.type is TokenType.STAR


def test_compound_assignment_target_is_a_variable_name():
    (statement,) = parse_source("score += bonus✨")
    assert isinstance(statement, Assign)
    assert statement.name.lexeme == "score"
    assert isinstance(statement.value, Variable) and statement.value.name.lexeme == "bonus"


def test_compound_assignment_is_not_an_expression():
    with pytest.raises(SlopSyntaxError, match=r"expected '\)' after arguments, found '\+='"):
        parse_source("hallucinate(x += 1)✨")


def test_compound_assignment_requires_a_terminator():
    with pytest.raises(
        SlopSyntaxError, match=r"expected ✨ after assignment, but reached end of file"
    ):
        parse_source("x += 1")

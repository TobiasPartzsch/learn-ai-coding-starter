import pytest

from sloperator.runner import run_source


def test_unary_not_flips_booleans_and_nests():
    result = run_source("hallucinate(!✅, !❌, !!✅)✨")

    assert (result.stdout, result.stderr, result.exit_code) == ("❌ ✅ ✅\n", "", 0)


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("!✅", "❌"),
        ("!❌", "✅"),
        ("!!✅", "✅"),
        ("!!❌", "❌"),
    ],
)
def test_unary_not(expression: str, expected: str):
    result = run_source(f"hallucinate({expression})✨")

    assert (result.stdout, result.stderr, result.exit_code) == (f"{expected}\n", "", 0)


def test_unary_not_binds_tighter_than_equality():
    result = run_source("hallucinate(!❌ == ✅)✨")

    assert (result.stdout, result.stderr, result.exit_code) == ("✅\n", "", 0)


@pytest.mark.parametrize(("operand", "kind"), [("1", "number"), ("“slop”", "string")])
def test_unary_not_rejects_non_booleans(operand: str, kind: str):
    result = run_source(f"hallucinate(!{operand})✨")

    assert result.exit_code == 1
    assert result.stderr == (
        f"SlopLang runtime error at line 1: operand of unary '!' must be a boolean, got {kind}\n"
    )

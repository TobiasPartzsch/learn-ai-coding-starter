import pytest

from sloperator.runner import run_source


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("“” + “slop”", "slop"),
        ("“slop” + “”", "slop"),
        ("“café” + “✨”", "café✨"),
    ],
)
def test_string_addition(expression: str, expected: str):
    result = run_source(f"hallucinate({expression})✨")

    assert (result.stdout, result.stderr, result.exit_code) == (f"{expected}\n", "", 0)

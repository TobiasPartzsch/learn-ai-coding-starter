"""Regression tests for identifiers containing digits.

Identifiers previously stopped at the first digit, so a name like ``score2``
tokenized as ``score`` followed by ``2`` and failed to parse.
"""

from sloperator.runner import run_source


def test_variable_name_may_contain_digits():
    result = run_source("""slop score2 = 40✨
score2 = score2 + 2✨
hallucinate(score2)✨""")

    assert (result.stdout, result.stderr, result.exit_code) == ("42\n", "", 0)


def test_function_and_parameter_names_may_contain_digits():
    result = run_source("""clanker add2(left1, right2) {
    ship left1 + right2✨
}
hallucinate(add2(1, 2))✨""")

    assert (result.stdout, result.stderr, result.exit_code) == ("3\n", "", 0)


def test_identifier_cannot_start_with_a_digit():
    result = run_source("slop 2x = 1✨")
    assert result.stdout == ""
    assert result.exit_code != 0
    assert result.stderr.startswith("SlopLang syntax error at line 1:")
